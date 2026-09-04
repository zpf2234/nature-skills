from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "nature-reader" / "scripts" / "validate_reader_math.py"
SPEC = importlib.util.spec_from_file_location("validate_reader_math", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def equation(equation_id: str, **values: object) -> dict[str, object]:
    return {
        "id": equation_id,
        "page": 1,
        "confidence": "high",
        "latex": "x=1",
        **values,
    }


class SourceMapEquationIdTests(unittest.TestCase):
    def validate(self, source_map: dict[str, object]) -> list[object]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source_map.json"
            path.write_text(json.dumps(source_map), encoding="utf-8")
            return MODULE.validate_source_map(path, ["E001"], [])

    def test_duplicate_id_in_equations_is_reported(self) -> None:
        findings = self.validate(
            {"equations": [equation("E001"), equation("E001", page=2)]}
        )

        duplicate_codes = [item.code for item in findings if item.code == "DUPLICATE_SOURCE_MAP_ID"]
        self.assertEqual(duplicate_codes, ["DUPLICATE_SOURCE_MAP_ID"])

    def test_duplicate_equation_block_id_is_reported(self) -> None:
        first = equation("E001", type="equation")
        second = equation("E001", type="equation", page=2)

        findings = self.validate({"blocks": [first, second]})

        self.assertIn("DUPLICATE_SOURCE_MAP_ID", {item.code for item in findings})

    def test_matching_block_and_equation_entries_are_merged(self) -> None:
        findings = self.validate(
            {
                "blocks": [
                    {
                        "id": "E001",
                        "type": "equation",
                        "page": 1,
                        "confidence": "high",
                    }
                ],
                "equations": [{"id": "E001", "latex": "x=1"}],
            }
        )

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
