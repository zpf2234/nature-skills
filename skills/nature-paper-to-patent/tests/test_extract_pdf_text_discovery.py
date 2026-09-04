from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract_pdf_text.py"
SPEC = importlib.util.spec_from_file_location("extract_pdf_text", SCRIPT)
EXTRACTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXTRACTOR)


class PdfDiscoveryTests(unittest.TestCase):
    def test_directory_search_accepts_uppercase_pdf_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lower = root / "first.pdf"
            upper = root / "second.PDF"
            ignored = root / "notes.txt"
            for path in (lower, upper, ignored):
                path.touch()

            result = EXTRACTOR.collect_pdfs(root)

            self.assertEqual(result, sorted([lower, upper]))


if __name__ == "__main__":
    unittest.main()
