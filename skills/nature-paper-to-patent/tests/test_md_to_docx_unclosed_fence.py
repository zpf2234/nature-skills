from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "md_to_docx.py"
SPEC = importlib.util.spec_from_file_location("md_to_docx", SCRIPT)
CONVERTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONVERTER)


class UnclosedFenceTests(unittest.TestCase):
    def test_unclosed_code_fence_is_rejected(self) -> None:
        markdown = "# 方案\n\n```python\nresult = 42\n后续内容\n"

        with self.assertRaisesRegex(ValueError, "Unclosed fenced code block"):
            CONVERTER.convert_md_to_docx(markdown, base_dir=None)


if __name__ == "__main__":
    unittest.main()
