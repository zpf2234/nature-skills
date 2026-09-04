from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "nature-reader" / "scripts" / "validate_reader_math.py"
SPEC = importlib.util.spec_from_file_location("validate_reader_math_inline_code", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ReaderInlineCodeTests(unittest.TestCase):
    def test_shell_variable_in_code_span_is_not_inline_math(self) -> None:
        findings, _, _ = VALIDATOR.validate_markdown("Use `$HOME` for this example.\n")

        self.assertNotIn("UNBALANCED_INLINE_MATH", {item.code for item in findings})

    def test_latex_command_in_code_span_is_not_prose(self) -> None:
        findings, _, _ = VALIDATOR.validate_markdown(r"The source contains `\alpha` here." + "\n")

        self.assertNotIn("BARE_LATEX", {item.code for item in findings})

    def test_image_example_in_code_span_is_not_collected(self) -> None:
        _, _, image_paths = VALIDATOR.validate_markdown(
            "Write `![equation](missing.png)` to embed an image.\n"
        )

        self.assertEqual([], image_paths)

    def test_long_code_delimiter_can_contain_single_backticks(self) -> None:
        findings, _, _ = VALIDATOR.validate_markdown(
            "The literal form is ``use `$HOME` here``.\n"
        )

        self.assertNotIn("UNBALANCED_INLINE_MATH", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
