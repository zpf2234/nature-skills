from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "md_to_docx.py"
SPEC = importlib.util.spec_from_file_location("md_to_docx", SCRIPT)
CONVERTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONVERTER)


class MarkdownTildeFenceTests(unittest.TestCase):
    def test_tilde_fence_is_exported_as_code_block(self) -> None:
        markdown = "~~~python\nresult = 42\n~~~\n"

        document = CONVERTER.convert_md_to_docx(markdown, base_dir=None)

        self.assertEqual(len(document.paragraphs), 1)
        self.assertEqual(document.paragraphs[0].text, "result = 42")
        self.assertEqual(document.paragraphs[0].runs[0].font.name, "Consolas")


if __name__ == "__main__":
    unittest.main()
