from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_claims", ROOT / "scripts" / "audit_claims.py"
)
assert SPEC and SPEC.loader
AUDITOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDITOR
SPEC.loader.exec_module(AUDITOR)


class ClaimReferenceTests(unittest.TestCase):
    def test_multiple_claim_references_are_all_returned(self) -> None:
        self.assertEqual(
            [1, 2, 3],
            AUDITOR.references("根据权利要求1、2或3所述的方法"),
        )

    def test_range_and_list_can_be_combined(self) -> None:
        self.assertEqual(
            [1, 2, 3, 5],
            AUDITOR.references("根据权利要求1至3或5所述的方法"),
        )

    def test_all_forward_references_are_reported(self) -> None:
        text = (
            "1. 一种数据处理方法，其特征在于，包括获取数据并处理所述数据。\n"
            "2. 根据权利要求1、3或4所述的方法，其特征在于，进一步输出处理结果。"
        )

        findings = AUDITOR.audit(text)

        messages = [item.message for item in findings if item.code == "FORWARD_REFERENCE"]
        self.assertEqual(
            ["引用了非在先权利要求3。", "引用了非在先权利要求4。"],
            messages,
        )


if __name__ == "__main__":
    unittest.main()
