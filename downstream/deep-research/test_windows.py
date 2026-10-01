import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.research_state import ValidationError, cleanup_run, create_run


@unittest.skipUnless(os.name == "nt", "Native Windows contracts")
class WindowsResearchTest(unittest.TestCase):
    def test_powershell_helper_creates_and_validates_run_in_profile(self):
        skill = Path(__file__).resolve().parents[1]
        helper = skill / "scripts/research.ps1"
        runtime = json.loads((skill / "windows-runtime.json").read_text())
        result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                                 str(helper), "create", "windows-helper-check", "--query",
                                 "Native Windows smoke check", "--mode", "quick", "--axis", "Evidence"],
                                capture_output=True, text=True, check=True)
        run = Path(result.stdout.strip())
        self.assertEqual(run.parent, Path(runtime["profile_home"]) / "research/hermes-deep-research")
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(helper), "validate", str(run)], capture_output=True, text=True, check=True)
        self.assertTrue((run / "sources.json").is_file())

    def test_unsupported_cleanup_refuses_without_touching_report_or_temporary_file(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(os.environ, {"HERMES_HOME": temporary}):
            run, state = create_run("windows-refusal", "Question", "quick", ["Evidence"])
            state["status"] = "partial"
            (run / "state.json").write_text(json.dumps(state))
            (run / "report.md").write_text("Partial report with an unresolved gap.")
            transient = run / "tmp/workspace/keep.txt"
            transient.write_text("preserve")
            for apply in (False, True):
                with self.assertRaises(ValidationError):
                    cleanup_run(run, apply=apply)
                self.assertEqual(transient.read_text(), "preserve")
                self.assertTrue((run / "report.md").is_file())
