import unittest

from ci.capability_gate import NEEDS_REVIEW, NOT_RUN, decide


class DecideTest(unittest.TestCase):
    def test_clean_run_passes(self):
        self.assertEqual(decide(0, {}, ["README.md"])[0], 0)

    def test_capability_change_needs_review(self):
        code, _ = decide(1, {"capability_changes": [{"kind": "tool_removed_gate"}]}, ["app/agent.py"])
        self.assertEqual(code, NEEDS_REVIEW)

    def test_partial_scan_blocks_only_when_unread_file_changed(self):
        report = {"unread_paths": ["app/reporting.py"]}
        self.assertEqual(decide(3, report, ["README.md"])[0], 0)
        self.assertEqual(decide(3, report, ["app/reporting.py"])[0], NEEDS_REVIEW)

    def test_inspector_failure_is_not_run_never_a_pass(self):
        for status in (2, 4, 127, -1):
            self.assertEqual(decide(status, {}, [])[0], NOT_RUN)


if __name__ == "__main__":
    unittest.main()
