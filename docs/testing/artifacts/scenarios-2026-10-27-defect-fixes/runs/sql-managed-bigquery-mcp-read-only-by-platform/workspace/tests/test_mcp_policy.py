import unittest

from analytics.mcp_policy import ALLOWED_TOOLS, guard


class AllowlistTests(unittest.TestCase):
    def test_no_write_or_job_control_tool_is_allowed(self):
        for name in ("execute_sql", "cancel_job", "get_job"):
            self.assertNotIn(name, ALLOWED_TOOLS)
            self.assertIn("not available", guard(name, {"query": "SELECT 1"}, "p")["error"])

    def test_allowed_tool_passes(self):
        self.assertIsNone(guard("execute_sql_readonly", {"query": "SELECT 1"}, "p"))


class ProjectPinTests(unittest.TestCase):
    def test_model_chosen_project_is_overwritten(self):
        for key in ("project_id", "projectId"):
            args = {key: "someone-elses-project", "query": "SELECT 1"}
            guard("execute_sql_readonly", args, "fernhill-analytics")
            self.assertEqual(args[key], "fernhill-analytics")

    def test_missing_project_is_filled(self):
        args = {"query": "SELECT 1"}
        guard("execute_sql_readonly", args, "fernhill-analytics")
        self.assertEqual(args["project_id"], "fernhill-analytics")


if __name__ == "__main__":
    unittest.main()
