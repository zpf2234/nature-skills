from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_patent_docx.py"


def draft() -> dict:
    return {
        "title": "一种检测方法",
        "claims": [{"number": 1, "text": "一种检测方法。"}],
        "specification": {},
        "abstract": "本发明公开一种检测方法。",
        "abstract_figure_number": 1,
        "figures": [{"number": 1, "title": "方法流程图"}],
    }


class MissingFigureRenderTests(unittest.TestCase):
    def test_missing_requested_figure_fails_before_writing_docx(self) -> None:
        for part in ("specification", "abstract-figure"):
            with self.subTest(part=part), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "draft.json"
                output = root / f"{part}.docx"
                figure_dir = root / "figures"
                figure_dir.mkdir()
                source.write_text(json.dumps(draft(), ensure_ascii=False), encoding="utf-8")

                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        str(source),
                        "--output",
                        str(output),
                        "--part",
                        part,
                        "--figure-dir",
                        str(figure_dir),
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("figure-1.png", result.stderr)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
