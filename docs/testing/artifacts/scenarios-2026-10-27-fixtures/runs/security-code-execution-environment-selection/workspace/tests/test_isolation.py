"""Isolation: model-written code never runs in the service process or on a non-Google backend."""
import re
import unittest

from tests.helpers import ROOT, app_sources, imported_and_named

FORBIDDEN_EXECUTION = {
    "UnsafeLocalCodeExecutor": "runs model code inside the serving process",
    "LocalEnvironment": "runs commands on the serving host",
    "BashTool": "shell access without a reviewed BashToolPolicy",
    "ContainerCodeExecutor": "needs a Docker daemon Cloud Run does not provide",
    "EnvironmentToolset": "second execution surface; not reviewed (workspace write and run tools)",
    "DaytonaEnvironment": "runs code outside Google Cloud",
    "daytona": "runs code outside Google Cloud",
    "e2b": "runs code outside Google Cloud",
    "OpenSandbox": "runs code outside Google Cloud",
    "exec": "in-process code execution",
    "eval": "in-process code execution",
    "subprocess": "spawns processes from the service",
}


class IsolationTests(unittest.TestCase):
    def test_no_forbidden_execution_surface_in_app(self):
        for path, source in app_sources().items():
            for name in imported_and_named(source) & FORBIDDEN_EXECUTION.keys():
                self.fail(f"{path.relative_to(ROOT)} uses {name}: {FORBIDDEN_EXECUTION[name]}")

    def test_agent_uses_the_managed_sandbox_executor(self):
        names = imported_and_named((ROOT / "app/agent.py").read_text())
        self.assertIn("AgentEngineSandboxCodeExecutor", names)
        self.assertIn("code_executor", (ROOT / "app/agent.py").read_text())

    def test_executor_is_given_the_validated_resource_name_only(self):
        source = (ROOT / "app/agent.py").read_text()
        self.assertRegex(
            source,
            r"AgentEngineSandboxCodeExecutor\(\s*sandbox_resource_name=sandbox_resource_name\(\)\s*\)",
        )

    def test_no_backend_dependency_outside_google_cloud(self):
        deps = (ROOT / "pyproject.toml").read_text().lower()
        for banned in ("daytona", "e2b", "opensandbox"):
            self.assertNotIn(banned, deps)

    def test_deploy_has_no_sandbox_vendor_credentials(self):
        text = (ROOT / "deploy/service.yaml").read_text().upper()
        for banned in ("DAYTONA", "E2B_"):
            self.assertNotIn(banned, text)

    def test_adk_pin_is_unchanged(self):
        self.assertRegex((ROOT / "pyproject.toml").read_text(), r'"google-adk\[extensions\]==2\.12\.0"')

    def test_email_tool_is_behind_confirmation(self):
        source = (ROOT / "app/agent.py").read_text()
        self.assertRegex(source, r"FunctionTool\(\s*email_report,\s*require_confirmation=True\s*\)")
        tools_list = re.search(r"tools=\[(.*)\]", source).group(1)
        self.assertNotRegex(tools_list.replace("FunctionTool(email_report, require_confirmation=True)", ""),
                            r"\bemail_report\b")


if __name__ == "__main__":
    unittest.main()
