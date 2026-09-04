from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_validation import valid_draft


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_patent_package.py"
SPEC = importlib.util.spec_from_file_location("build_patent_package", SCRIPT)
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class PatentPackageStagingTests(unittest.TestCase):
    def test_renderer_failure_leaves_no_partial_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "draft.json"
            output_dir = root / "output"
            output_dir.mkdir()
            sentinel = output_dir / "notes.txt"
            sentinel.write_text("keep", encoding="utf-8")
            source.write_text(
                json.dumps(valid_draft(), ensure_ascii=False), encoding="utf-8"
            )

            failure = subprocess.CalledProcessError(1, ["render_patent_docx.py"])
            with mock.patch.object(
                BUILD, "run", side_effect=[None, failure]
            ), mock.patch.object(
                sys,
                "argv",
                [str(SCRIPT), str(source), "--output-dir", str(output_dir)],
            ):
                with self.assertRaises(subprocess.CalledProcessError):
                    BUILD.main()

            self.assertEqual(list(output_dir.iterdir()), [sentinel])
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
