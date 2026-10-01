#!/usr/bin/env python3
"""Offline card validation and bounded source-file integrity records. No factual scoring."""

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

MAX_BYTES = 8 * 1024 * 1024
CARD_SCHEMA = "gorptastic.evidence-card.v1"
BUNDLE_SCHEMA = "gorptastic.evidence-bundle.v1"
NOT_ESTABLISHED = {
    "factual_support": "not_evaluated",
    "authorship": "not_evaluated",
    "outcome": "not_evaluated",
    "publication_consent": "not_evaluated",
}


class InvalidEvidence(ValueError):
    pass


def fields(value, required, optional=(), label="object"):
    if not isinstance(value, dict):
        raise InvalidEvidence(f"{label} must be an object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise InvalidEvidence(f"{label}: missing={sorted(missing)}, unexpected={sorted(extra)}")


def text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 16000:
        raise InvalidEvidence(f"{label} must be nonempty text of at most 16000 characters")


def timestamp(value, label):
    text(value, label)
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)", value):
        raise InvalidEvidence(f"{label} must be a timestamp with a timezone")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidEvidence(f"{label} is not a valid timestamp") from exc


def relative_artifact(value):
    text(value, "artifact")
    p = PurePosixPath(value)
    if p.is_absolute() or "\\" in value or any(s in {"", ".", ".."} for s in value.split("/")) or ":" in value:
        raise InvalidEvidence("artifact must be a relative path inside the source root")
    return p


def validate_card(card, require_artifacts=False):
    fields(card, ("schema", "id", "kind", "claim", "scope", "sources", "rival_explanation", "check", "limitations"), label="card")
    if card["schema"] != CARD_SCHEMA:
        raise InvalidEvidence("unsupported card schema")
    if not isinstance(card["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", card["id"]):
        raise InvalidEvidence("id must be a lowercase slug")
    if card["kind"] not in ("question", "correction", "reproduction", "source-check"):
        raise InvalidEvidence("invalid contribution kind")
    for key in ("claim", "rival_explanation", "limitations"):
        text(card[key], key)
    for group, keys in (("scope", ("population", "measure", "unit", "period")), ("check", ("action", "observable", "comparison", "horizon", "decision_rule", "falsifier"))):
        fields(card[group], keys, label=group)
        for key in keys:
            text(card[group][key], f"{group}.{key}")
    sources = card["sources"]
    if not isinstance(sources, list) or not 1 <= len(sources) <= 16:
        raise InvalidEvidence("sources must contain one to sixteen entries")
    seen = set()
    for source in sources:
        fields(source, ("id", "url", "title", "locator", "source_time", "observed_at", "supports", "limits"), ("artifact",), "source")
        for key in ("id", "url", "title", "locator", "supports", "limits"):
            text(source[key], f"source.{key}")
        if source["id"] in seen:
            raise InvalidEvidence("source ids must be unique")
        seen.add(source["id"])
        try:
            url = urlsplit(source["url"])
            if url.scheme != "https" or not url.hostname or url.username or url.password:
                raise ValueError()
            _ = url.port
        except ValueError as exc:
            raise InvalidEvidence("source URL must be HTTPS without credentials") from exc
        timestamp(source["observed_at"], "source.observed_at")
        if source["source_time"] is not None:
            try:
                if re.fullmatch(r"\d{4}-\d\d-\d\d", str(source["source_time"])):
                    date.fromisoformat(source["source_time"])
                else:
                    timestamp(source["source_time"], "source.source_time")
            except ValueError as exc:
                raise InvalidEvidence("source_time must be a date, zoned timestamp, or null") from exc
        if require_artifacts and "artifact" not in source:
            raise InvalidEvidence("freeze requires an artifact for every source")
        if "artifact" in source:
            relative_artifact(source["artifact"])
    return card


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def bounded_bytes(path):
    # The open file is bounded even if it grows after opening.
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise InvalidEvidence("input file exceeds the 8 MiB limit")
    return data


def read_json(path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InvalidEvidence(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    def invalid_constant(value):
        raise InvalidEvidence(f"nonfinite JSON number: {value}")
    return json.loads(bounded_bytes(path), object_pairs_hook=unique_object, parse_constant=invalid_constant)


def source_records(card, source_root):
    root = Path(source_root).resolve(strict=True)
    if not root.is_dir():
        raise InvalidEvidence("source root must be a directory")
    records = []
    for source in card["sources"]:
        relative = relative_artifact(source["artifact"])
        artifact = (root / str(relative)).resolve(strict=True)
        if not artifact.is_relative_to(root) or not artifact.is_file():
            raise InvalidEvidence("artifact resolves outside the source root or is not a file")
        data = bounded_bytes(artifact)
        records.append({"source_id": source["id"], "artifact": str(relative), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return records


def freeze(card, source_root):
    validate_card(card, require_artifacts=True)
    payload = {"card": card, "artifacts": source_records(card, source_root)}
    return {"schema": BUNDLE_SCHEMA, "recorded_at": datetime.now(timezone.utc).isoformat(), "payload": payload, "payload_sha256": digest(payload)}


def verify(bundle, source_root):
    fields(bundle, ("schema", "recorded_at", "payload", "payload_sha256"), label="bundle")
    if bundle["schema"] != BUNDLE_SCHEMA:
        raise InvalidEvidence("unsupported bundle schema")
    timestamp(bundle["recorded_at"], "recorded_at")
    fields(bundle["payload"], ("card", "artifacts"), label="payload")
    if digest(bundle["payload"]) != bundle["payload_sha256"]:
        raise InvalidEvidence("bundle payload digest mismatch")
    card = validate_card(bundle["payload"]["card"], require_artifacts=True)
    current = source_records(card, source_root)
    if current != bundle["payload"]["artifacts"]:
        raise InvalidEvidence("recorded source-file bytes have changed")
    return {"format_valid": True, "byte_integrity": "matches_recorded_files", "source_count": len(current), **NOT_ESTABLISHED}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check").add_argument("input", type=Path)
    frozen = sub.add_parser("freeze")
    frozen.add_argument("input", type=Path)
    frozen.add_argument("--source-root", required=True, type=Path)
    frozen.add_argument("--output", required=True, type=Path)
    verified = sub.add_parser("verify")
    verified.add_argument("input", type=Path)
    verified.add_argument("--source-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        value = read_json(args.input)
        if args.command == "check":
            validate_card(value)
            result = {"format_valid": True, "byte_integrity": "not_checked", **NOT_ESTABLISHED}
        elif args.command == "freeze":
            bundle = freeze(value, args.source_root)
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump(bundle, handle, ensure_ascii=False, indent=2, allow_nan=False)
                handle.write("\n")
            result = {"created": True, "output": str(args.output), "payload_sha256": bundle["payload_sha256"], "byte_integrity": "recorded_not_rechecked", **NOT_ESTABLISHED}
        else:
            result = verify(value, args.source_root)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (InvalidEvidence, OSError, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc), **NOT_ESTABLISHED}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
