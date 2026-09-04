from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_paper_card", ROOT / "scripts" / "audit_paper_card.py"
)
assert SPEC and SPEC.loader
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)


class EvidenceMentionTests(unittest.TestCase):
    def test_longer_figure_number_does_not_cover_shorter_id(self) -> None:
        card = "Figure 10 and Fig. 12 are discussed together; 图13提供补充结果。"

        self.assertFalse(AUDITOR.evidence_item_mentioned(card, "Figure 1"))

    def test_longer_table_and_equation_numbers_do_not_match(self) -> None:
        card = "Table 20 summarizes the cohort and Equation 12 defines the loss."

        self.assertFalse(AUDITOR.evidence_item_mentioned(card, "Table 2"))
        self.assertFalse(AUDITOR.evidence_item_mentioned(card, "Equation 1"))

    def test_exact_id_before_punctuation_is_recognized(self) -> None:
        card = "The result is shown in Figure 1, Table 2，and Eq.3。"

        self.assertTrue(AUDITOR.evidence_item_mentioned(card, "Figure 1"))
        self.assertTrue(AUDITOR.evidence_item_mentioned(card, "Table 2"))
        self.assertTrue(AUDITOR.evidence_item_mentioned(card, "Equation 3"))

    def test_panel_suffix_must_match_exactly(self) -> None:
        card = "Figure 1A shows the first ablation."

        self.assertFalse(AUDITOR.evidence_item_mentioned(card, "Figure 1"))
        self.assertTrue(AUDITOR.evidence_item_mentioned(card, "Figure 1A"))


if __name__ == "__main__":
    unittest.main()
