from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_patent_project.py"


class PatentProjectInputValidationTests(unittest.TestCase):
    def test_missing_paper_does_not_create_partial_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "patent-project"
            missing_paper = root / "missing.pdf"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(project),
                    "--paper",
                    str(missing_paper),
                    "--no-embed-skill",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("paper does not exist", result.stderr)
            self.assertFalse(project.exists())


if __name__ == "__main__":
    unittest.main()
