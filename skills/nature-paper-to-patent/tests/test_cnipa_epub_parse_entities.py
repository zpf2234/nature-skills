from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "cnipa_epub_parse.py"
SPEC = importlib.util.spec_from_file_location("cnipa_epub_parse", SCRIPT)
PARSER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PARSER
SPEC.loader.exec_module(PARSER)


class CnipaHtmlEntityTests(unittest.TestCase):
    def test_result_fields_decode_html_entities(self) -> None:
        source = (
            '<tr><td><a href="/patent/CN123456789A?x=1&amp;y=2" '
            'title="Method &amp; system">Method &amp; system</a></td></tr>'
        )

        hit = PARSER.parse_search_result_html(source)[0]

        self.assertEqual(hit.title, "Method & system")
        self.assertEqual(
            hit.link,
            "http://epub.cnipa.gov.cn/patent/CN123456789A?x=1&y=2",
        )

    def test_abstract_text_decodes_nonbreaking_spaces(self) -> None:
        item = "<dt>摘要：</dt><dd>alpha&nbsp;&amp;&nbsp;beta</dd>"

        self.assertEqual(
            PARSER._extract_abstract_from_item_html(item), "alpha & beta"
        )


if __name__ == "__main__":
    unittest.main()
