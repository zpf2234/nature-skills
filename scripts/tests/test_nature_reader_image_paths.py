from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "nature-reader" / "scripts" / "validate_reader_math.py"


class ReaderImagePathTests(unittest.TestCase):
    def test_angle_bracket_image_path_can_contain_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "assets" / "equations" / "E 001.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"equation image")
            paper = root / "paper.md"
            paper.write_text(
                '# Paper\n\n<a id="E001"></a>\n'
                '![Original equation](<assets/equations/E 001.png>)\n',
                encoding="utf-8",
            )
            source_map = root / "source_map.json"
            source_map.write_text(
                json.dumps(
                    {
                        "equations": [
                            {
                                "id": "E001",
                                "page": 1,
                                "confidence": "low",
                                "image_path": "assets/equations/E 001.png",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(paper),
                    "--source-map",
                    str(source_map),
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["ready"])


if __name__ == "__main__":
    unittest.main()
