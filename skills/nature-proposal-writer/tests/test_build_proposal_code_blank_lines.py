from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_proposal_docx.py"


class ProposalCodeBlankLineTests(unittest.TestCase):
    def test_code_block_keeps_blank_lines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "proposal.md"
            output = root / "proposal.docx"
            source.write_text(
                "# Proposal\n\n```python\nfirst = 1\n\nsecond = 2\n```\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document = Document(output)
            code = next(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.startswith("first = 1")
            )
            self.assertEqual(code, "first = 1\n\nsecond = 2")


if __name__ == "__main__":
    unittest.main()
