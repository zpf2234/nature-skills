from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_paper_card.py"


class AuditReportSourceOverwriteTests(unittest.TestCase):
    def test_report_cannot_overwrite_card_or_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card = root / "card.md"
            bundle = root / "bundle.json"
            card_text = "# Paper Card\n"
            bundle_text = json.dumps({"evidence_inventory": {}})
            card.write_text(card_text, encoding="utf-8")
            bundle.write_text(bundle_text, encoding="utf-8")

            for report in (card, bundle):
                with self.subTest(report=report.name):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(SCRIPT),
                            "--card",
                            str(card),
                            "--bundle",
                            str(bundle),
                            "--locator-mode",
                            "structure-grounded",
                            "--report",
                            str(report),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )

                    self.assertEqual(result.returncode, 2)
                    self.assertIn("cannot overwrite", result.stderr)
                    self.assertEqual(card.read_text(encoding="utf-8"), card_text)
                    self.assertEqual(bundle.read_text(encoding="utf-8"), bundle_text)


if __name__ == "__main__":
    unittest.main()
