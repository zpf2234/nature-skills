from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "nature-reader" / "scripts" / "validate_reader_math.py"
SPEC = importlib.util.spec_from_file_location("validate_reader_math_fences", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ReaderFenceTests(unittest.TestCase):
    def test_fence_with_trailing_text_does_not_close_code_block(self) -> None:
        markdown = """# Paper

```text
```not-a-closing-fence
\\alpha is shown as source text here
```
"""

        findings, anchors, image_paths = VALIDATOR.validate_markdown(markdown)

        self.assertEqual([], findings)
        self.assertEqual([], anchors)
        self.assertEqual([], image_paths)

    def test_longer_plain_fence_still_closes_block(self) -> None:
        markdown = """# Paper

```text
\\alpha is shown as source text here
````
"""

        findings, _, _ = VALIDATOR.validate_markdown(markdown)

        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
