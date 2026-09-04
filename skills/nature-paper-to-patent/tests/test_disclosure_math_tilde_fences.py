from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "math_render.py"
SPEC = importlib.util.spec_from_file_location("math_render", SCRIPT)
MATH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATH)


class TildeFenceMathTests(unittest.TestCase):
    def test_math_inside_tilde_fence_is_not_rendered(self) -> None:
        markdown = "~~~python\nformula = '$x^2$'\n~~~\n"
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(
            MATH, "_try_render"
        ) as render:
            output = Path(directory) / "disclosure.md"

            result, ok, failed = MATH.render_markdown_math(
                markdown, out_md_path=output
            )

        self.assertEqual(result, markdown)
        self.assertEqual((ok, failed), (0, 0))
        render.assert_not_called()


if __name__ == "__main__":
    unittest.main()
