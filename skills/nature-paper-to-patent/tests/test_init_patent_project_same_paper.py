from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_patent_project.py"


class PatentProjectSamePaperTests(unittest.TestCase):
    def test_existing_project_paper_can_be_passed_again(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "patent-project"
            paper_dir = project / "paper"
            paper_dir.mkdir(parents=True)
            paper = paper_dir / "source.pdf"
            paper.write_bytes(b"paper content")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(project),
                    "--force",
                    "--paper",
                    str(paper),
                    "--no-embed-skill",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(paper.read_bytes(), b"paper content")


if __name__ == "__main__":
    unittest.main()
