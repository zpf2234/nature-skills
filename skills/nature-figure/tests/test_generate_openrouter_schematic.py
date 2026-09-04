from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generate_openrouter_schematic",
    ROOT / "scripts" / "generate_openrouter_schematic.py",
)
assert SPEC and SPEC.loader
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


class SaveOutputsTests(unittest.TestCase):
    def test_empty_or_invalid_data_fails_without_creating_output(self) -> None:
        for response in ({}, {"data": None}, {"data": []}, {"data": ["invalid"]}):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as directory:
                outdir = Path(directory) / "output"
                args = SimpleNamespace(
                    outdir=str(outdir),
                    basename="figure",
                    output_format="png",
                    timeout=1,
                    api_url="https://example.test/images",
                )

                with self.assertRaises(SystemExit):
                    GENERATOR.save_outputs(response, {}, args)

                self.assertFalse(outdir.exists())


if __name__ == "__main__":
    unittest.main()
