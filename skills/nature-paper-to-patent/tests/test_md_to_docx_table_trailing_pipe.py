from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "md_to_docx.py"
SPEC = importlib.util.spec_from_file_location("md_to_docx", SCRIPT)
CONVERTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONVERTER)


class MarkdownTableTrailingPipeTests(unittest.TestCase):
    def test_table_without_trailing_pipes_keeps_all_columns(self) -> None:
        markdown = (
            "| Parameter | Value\n"
            "| --- | ---\n"
            "| Threshold | 0.8\n"
        )

        document = CONVERTER.convert_md_to_docx(markdown, base_dir=None)

        self.assertEqual(len(document.tables), 1)
        self.assertEqual(
            [[cell.text for cell in row.cells] for row in document.tables[0].rows],
            [["Parameter", "Value"], ["Threshold", "0.8"]],
        )


if __name__ == "__main__":
    unittest.main()
