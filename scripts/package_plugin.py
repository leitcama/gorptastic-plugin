#!/usr/bin/env python3
"""Create a deterministic, allowlisted plugin ZIP and its digest manifest."""

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/gorptastic"
FILES = (
    "plugin.json",
    "assets/icon.svg",
    "skills/evidence-to-experiment/SKILL.md",
    "skills/evidence-to-experiment/agents/openai.yaml",
    "skills/evidence-to-experiment/references/evidence-card.md",
    "skills/evidence-to-experiment/scripts/evidence_bundle.py",
)


def main():
    manifest = json.loads((PLUGIN / "plugin.json").read_text())
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    archive = out / f'gorptastic-{manifest["version"]}.zip'
    records = []
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name in FILES:
            source = PLUGIN / name
            if source.is_symlink() or not source.resolve().is_relative_to(PLUGIN.resolve()):
                raise ValueError("Package entries must be regular files inside the plugin")
            data = source.read_bytes()
            entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            target.writestr(entry, data)
            records.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        license_bytes = (ROOT / "LICENSE").read_bytes()
        entry = zipfile.ZipInfo("LICENSE", date_time=(2026, 1, 1, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        target.writestr(entry, license_bytes)
        records.append({"path": "LICENSE", "sha256": hashlib.sha256(license_bytes).hexdigest(), "bytes": len(license_bytes)})
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    release = {"schema": "gorptastic.plugin-package.v1", "name": manifest["name"], "version": manifest["version"], "archive": archive.name, "sha256": digest, "files": records}
    (out / "package-manifest.json").write_text(json.dumps(release, indent=2) + "\n")
    (out / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
    print(json.dumps({"archive": str(archive), "sha256": digest, "file_count": len(records)}))


if __name__ == "__main__":
    main()
