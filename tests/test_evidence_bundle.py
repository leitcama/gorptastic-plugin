import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/gorptastic/skills/evidence-to-experiment/scripts/evidence_bundle.py"
spec = importlib.util.spec_from_file_location("evidence_bundle", SCRIPT)
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)
CARD = json.loads((ROOT / "examples/card.json").read_text())
SOURCE = (ROOT / "examples/sources/pilot-report.txt").read_bytes()


class EvidenceBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / "sources"
        self.sources.mkdir()
        (self.sources / "pilot-report.txt").write_bytes(SOURCE)

    def test_portable_bundle_verifies_after_source_relocation(self):
        record = bundle.freeze(copy.deepcopy(CARD), self.sources)
        relocated = self.root / "relocated"
        relocated.mkdir()
        (relocated / "pilot-report.txt").write_bytes(SOURCE)
        result = bundle.verify(record, relocated)
        self.assertEqual(result["byte_integrity"], "matches_recorded_files")
        self.assertEqual(result["factual_support"], "not_evaluated")
        self.assertEqual(result["outcome"], "not_evaluated")
        self.assertNotIn(str(self.root), json.dumps(record))
        self.assertNotIn(SOURCE.decode(), json.dumps(record))

    def test_changed_source_bytes_rejected(self):
        record = bundle.freeze(copy.deepcopy(CARD), self.sources)
        (self.sources / "pilot-report.txt").write_text("changed")
        with self.assertRaisesRegex(bundle.InvalidEvidence, "bytes have changed"):
            bundle.verify(record, self.sources)

    def test_changed_card_rejected_even_when_files_match(self):
        record = bundle.freeze(copy.deepcopy(CARD), self.sources)
        record["payload"]["card"]["claim"] = "A different claim"
        with self.assertRaisesRegex(bundle.InvalidEvidence, "digest mismatch"):
            bundle.verify(record, self.sources)

    def test_path_traversal_absolute_paths_and_symlink_escape_rejected(self):
        outside = self.root / "private.txt"
        outside.write_text("PRIVATE")
        (self.sources / "escape.txt").symlink_to(outside)
        for artifact in ("../private.txt", str(outside), "escape.txt", "a\\b.txt"):
            with self.subTest(artifact=artifact):
                card = copy.deepcopy(CARD)
                card["sources"][0]["artifact"] = artifact
                with self.assertRaises(bundle.InvalidEvidence):
                    bundle.freeze(card, self.sources)

    def test_unknown_status_flags_cannot_promote_a_claim(self):
        for flag in ("verified", "public_opt_in", "outcome_verified"):
            card = copy.deepcopy(CARD)
            card[flag] = True
            with self.subTest(flag=flag), self.assertRaises(bundle.InvalidEvidence):
                bundle.validate_card(card)

    def test_missing_scope_and_timezone_rejected_unknown_source_date_preserved(self):
        card = copy.deepcopy(CARD)
        del card["scope"]["population"]
        with self.assertRaises(bundle.InvalidEvidence):
            bundle.validate_card(card)
        card = copy.deepcopy(CARD)
        card["sources"][0]["observed_at"] = "2026-09-30T18:00:00"
        with self.assertRaises(bundle.InvalidEvidence):
            bundle.validate_card(card)
        card["sources"][0]["observed_at"] = "2026-09-30T18:00:00Z"
        card["sources"][0]["source_time"] = None
        self.assertIsNone(bundle.validate_card(card)["sources"][0]["source_time"])

    def test_existing_output_is_preserved_on_freeze_failure(self):
        target = self.root / "output.json"
        target.write_text("existing work")
        card = self.root / "card.json"
        card.write_text(json.dumps(CARD))
        result = subprocess.run([sys.executable, str(SCRIPT), "freeze", str(card), "--source-root", str(self.sources), "--output", str(target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(target.read_text(), "existing work")

    def test_duplicate_json_keys_and_oversized_files_rejected(self):
        path = self.root / "duplicate.json"
        path.write_text('{"claim":"one", "claim":"two"}')
        with self.assertRaises(bundle.InvalidEvidence):
            bundle.read_json(path)
        with (self.sources / "pilot-report.txt").open("wb") as handle:
            handle.truncate(bundle.MAX_BYTES + 1)
        with self.assertRaisesRegex(bundle.InvalidEvidence, "8 MiB"):
            bundle.freeze(copy.deepcopy(CARD), self.sources)


if __name__ == "__main__":
    unittest.main()
