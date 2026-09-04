from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    script = ROOT / "scripts" / "disclosure" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DOCX = load("docx_to_md")
PPTX = load("pptx_to_md")


class OfficeSourceOverwriteTests(unittest.TestCase):
    def test_output_cannot_reuse_office_input_path(self) -> None:
        cases = (
            (DOCX, "source.docx", "_require_mammoth"),
            (PPTX, "source.pptx", "_require_pptx"),
        )
        for module, filename, dependency_loader in cases:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / filename
                original = b"office source"
                source.write_bytes(original)

                with mock.patch.object(
                    module,
                    dependency_loader,
                    side_effect=AssertionError("dependency should not be loaded"),
                ):
                    result = module._run(source, source, None)

                self.assertEqual(result, 2)
                self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
