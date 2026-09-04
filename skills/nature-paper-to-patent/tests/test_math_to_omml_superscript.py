from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "math_to_omml.py"
SPEC = importlib.util.spec_from_file_location("math_to_omml", SCRIPT)
MATH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATH)


class SuperscriptOmmlTests(unittest.TestCase):
    def test_msup_uses_superscript_child(self) -> None:
        mathml = ElementTree.fromstring(
            '<msup xmlns="http://www.w3.org/1998/Math/MathML">'
            "<mi>x</mi><mn>2</mn></msup>"
        )
        target = MATH._element("oMath")

        MATH._append_mathml(target, mathml)

        superscript = target[0]
        self.assertTrue(superscript.tag.endswith("}sSup"))
        self.assertTrue(superscript[1].tag.endswith("}sup"))
        self.assertEqual("".join(superscript[1].itertext()), "2")


if __name__ == "__main__":
    unittest.main()
