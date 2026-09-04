from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_proposal_docx.py"


class ProposalCodeFenceTests(unittest.TestCase):
    def test_unclosed_code_fence_fails_without_writing_docx(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "proposal.md"
            output = root / "proposal.docx"
            source.write_text(
                "# Proposal\n\n```python\nprint('result')\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(output)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unclosed fenced code block", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
