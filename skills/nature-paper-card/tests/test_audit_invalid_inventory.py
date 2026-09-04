from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_paper_card_invalid_inventory", ROOT / "scripts" / "audit_paper_card.py"
)
assert SPEC and SPEC.loader
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)


class InvalidInventoryTests(unittest.TestCase):
    def test_non_object_inventory_produces_a_reported_error(self) -> None:
        report = AUDITOR.audit(
            "",
            {"evidence_inventory": []},
            "structure-grounded",
        )

        codes = {item["code"] for item in report["findings"]}
        self.assertIn("invalid_source_inventory", codes)
        self.assertEqual(report["metrics"]["figures_in_bundle"], 0)
        self.assertEqual(report["metrics"]["tables_in_bundle"], 0)
        self.assertEqual(report["metrics"]["equations_in_bundle"], 0)


if __name__ == "__main__":
    unittest.main()
