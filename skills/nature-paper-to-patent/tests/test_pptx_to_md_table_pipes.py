from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "pptx_to_md.py"
SPEC = importlib.util.spec_from_file_location("pptx_to_md", SCRIPT)
CONVERTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONVERTER)


class PptxTablePipeTests(unittest.TestCase):
    def test_pipe_in_table_cell_is_escaped(self) -> None:
        row = SimpleNamespace(
            cells=[
                SimpleNamespace(text="Input | output"),
                SimpleNamespace(text="A\\B"),
            ]
        )
        shape = SimpleNamespace(
            has_text_frame=False,
            has_table=True,
            table=SimpleNamespace(rows=[row]),
        )

        result = CONVERTER._shape_text(shape)

        self.assertEqual(result, "| Input \\| output | A\\\\B |")


if __name__ == "__main__":
    unittest.main()
