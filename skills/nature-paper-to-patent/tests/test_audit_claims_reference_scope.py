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


class AntecedentReferenceScopeTests(unittest.TestCase):
    def test_unreferenced_claim_does_not_supply_antecedent_basis(self) -> None:
        claims = (
            "1. 一种数据处理方法，其特征在于，包括获取数据并输出处理结果的步骤。\n"
            "2. 根据权利要求1所述的方法，其特征在于，还包括设置校准模块并执行参数校准。\n"
            "3. 根据权利要求1所述的方法，其特征在于，所述校准模块，用于修正输入数据。\n"
        )

        findings = AUDITOR.audit(claims)

        messages = [
            item.message
            for item in findings
            if item.claim == 3 and item.code == "ANTECEDENT_BASIS"
        ]
        self.assertEqual(["术语“校准模块”可能缺少清晰的前置基础。"], messages)


if __name__ == "__main__":
    unittest.main()
