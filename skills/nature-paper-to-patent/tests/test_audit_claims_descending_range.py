from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_claims.py"
SPEC = importlib.util.spec_from_file_location("audit_claims", SCRIPT)
AUDITOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDITOR
SPEC.loader.exec_module(AUDITOR)


class DescendingClaimRangeTests(unittest.TestCase):
    def test_descending_reference_range_is_an_error(self) -> None:
        claims = (
            "1. 一种数据处理方法，其特征在于，包括获取输入数据并输出处理结果。\n"
            "2. 根据权利要求1所述的方法，其特征在于，还包括对输入数据进行归一化。\n"
            "3. 根据权利要求1所述的方法，其特征在于，还包括提取输入数据的特征。\n"
            "4. 根据权利要求3至1任一项所述的方法，其特征在于，还包括保存处理结果。\n"
        )

        findings = AUDITOR.audit(claims)

        messages = [
            item.message
            for item in findings
            if item.claim == 4 and item.code == "INVALID_REFERENCE_RANGE"
        ]
        self.assertEqual(["引用范围起点3大于终点1。"], messages)
        self.assertFalse(
            any(item.claim == 4 and item.code == "NO_REFERENCE" for item in findings)
        )


if __name__ == "__main__":
    unittest.main()
