from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_proposal_docx.py"


class ProposalDocxOutputTests(unittest.TestCase):
    def test_default_output_never_reuses_non_md_source_path(self) -> None:
        for filename in ("proposal.markdown", "proposal"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / filename
                original = "# Research proposal\n\nThe source text must remain intact.\n"
                source.write_text(original, encoding="utf-8")

                result = subprocess.run(
                    [sys.executable, str(SCRIPT), str(source)],
                    text=True,
                    capture_output=True,
                    check=False,
                )

                output = source.with_suffix(".docx")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(source.read_text(encoding="utf-8"), original)
                self.assertTrue(output.is_file())
                self.assertTrue(zipfile.is_zipfile(output))


if __name__ == "__main__":
    unittest.main()
