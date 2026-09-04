from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "disclosure" / "iteration_dialog_log.py"
SPEC = importlib.util.spec_from_file_location("iteration_dialog_log", SCRIPT)
LOG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOG)


class DialogLogAppendTests(unittest.TestCase):
    def test_existing_log_is_appended_without_rewriting_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            case_dir = Path(directory)
            log_path = case_dir / LOG.DEFAULT_LOG
            log_path.write_text("# Existing log\n", encoding="utf-8")
            arguments = [
                str(SCRIPT),
                "--case-dir",
                str(case_dir),
                "--kind",
                "correct",
                "--user",
                "补充参数范围",
            ]

            with mock.patch.object(sys, "argv", arguments), mock.patch.object(
                Path,
                "write_text",
                side_effect=AssertionError("existing log must not be rewritten"),
            ):
                result = LOG.main()

            self.assertEqual(result, 0)
            content = log_path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("# Existing log\n"))
            self.assertIn("补充参数范围", content)


if __name__ == "__main__":
    unittest.main()
