"""Exercise the security-surface inventory through its CLI with isolated local fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_security_surface.py"

TRIFECTA_AGENT = '''
import httpx
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.apps import App
from google.adk.tools import FunctionTool, AgentTool, google_search, url_context
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams
from google.adk.code_executors import UnsafeLocalCodeExecutor
from google.adk.plugins import LoggingPlugin


def search_customer_records(query: str, user_id: str, tool_context) -> dict:
    """Look up customer records for the current user."""
    return {"status": "success"}


def send_email(to: str, body: str) -> dict:
    """Send an email to a recipient."""
    httpx.post("https://mail.invalid", json={"to": to, "body": body})
    return {"status": "success"}


def delete_order(order_id: str) -> dict:
    return {"status": "success"}


def refund_payment(order_id: str) -> dict:
    return {"status": "pending_approval"}


def lookup_weather(city: str) -> dict:
    return {"status": "success", "city": city}


quarantine = LlmAgent(name="summariser", model="m", include_contents="none", mode="single_turn",
                      description="Summarise fetched pages", tools=[google_search])
stdio = McpToolset(connection_params=StdioConnectionParams(server_params=None),
                   tool_filter=["read_page", "post_message"])
root = LlmAgent(
    name="root", model="m", instruction="help",
    tools=[search_customer_records, FunctionTool(send_email),
           FunctionTool(delete_order, require_confirmation=True),
           McpToolset(connection_params=StreamableHTTPConnectionParams(url="https://x.invalid")),
           stdio, AgentTool(quarantine), url_context, missing_tool],
    sub_agents=[quarantine], code_executor=UnsafeLocalCodeExecutor(),
    before_model_callback=lambda c, r: None)
gated = LlmAgent(name="gated", model="m", tools=[refund_payment], before_tool_callback=lambda **kw: None)
clean = LlmAgent(name="clean", model="m", tools=[lookup_weather])
flow = SequentialAgent(name="flow", sub_agents=[root, clean])
app = App(name="a", root_agent=flow, plugins=[LoggingPlugin()])
'''

WORKFLOW_SPLIT = '''
from google.adk.agents import LlmAgent, SequentialAgent


def read_inbox(folder: str) -> dict:
    return {"status": "success"}


def lookup_account_balance(account_id: str) -> dict:
    return {"status": "success"}


def send_payment(amount: int) -> dict:
    return {"status": "success"}


reader = LlmAgent(name="reader", model="m", tools=[read_inbox, lookup_account_balance])
payer = LlmAgent(name="payer", model="m", tools=[send_payment], before_tool_callback=lambda **kw: None)
pipeline = SequentialAgent(name="pipeline", sub_agents=[reader, payer])
'''


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def run_cli(self, *args, project=True):
        command = [sys.executable, str(SCRIPT)]
        if project:
            command += ["--project", str(self.root)]
        return subprocess.run(command + list(args), capture_output=True, text=True, check=False)

    def scan(self, *args):
        result = self.run_cli(*args)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result, json.loads(result.stdout)

    def findings(self, data, kind):
        return [item for item in data["findings"] if item["finding"] == kind]

    def agent(self, data, name):
        return next(item for item in data["agents"] if item["name"] == name)

    def test_help_and_invalid_arguments_exit_two(self):
        result = self.run_cli("--help", project=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--dry-run", result.stdout)
        self.assertEqual(self.run_cli(project=False).returncode, 2)
        for option in ("--max-files", "--max-bytes", "--max-depth", "--max-entries"):
            for value in ("0", "-1", "not-a-number"):
                self.assertEqual(self.run_cli(option, value).returncode, 2)
        self.assertEqual(self.run_cli("--project", str(self.root / "absent")).returncode, 2)
        file_path = self.write("plain.py", "x = 1\n")
        self.assertEqual(self.run_cli("--project", str(file_path)).returncode, 2)

    def test_dry_run_is_read_only_and_repeatable(self):
        marker = self.root / "executed.txt"
        self.write("agent.py", f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n")
        before = {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.root.rglob("*") if p.is_file()}
        first, data = self.scan("--dry-run")
        second, _ = self.scan("--dry-run")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(data["read_only"])
        self.assertTrue(data["dry_run"])
        self.assertFalse(data["changes_made"])
        regular, regular_data = self.scan()
        regular_data["dry_run"] = True
        self.assertEqual(data, regular_data)
        after = {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse(marker.exists())

    def test_clean_read_only_agent_has_no_findings(self):
        self.write("agent.py", '''
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool


def lookup_weather(city: str, tool_context) -> dict:
    """Return the forecast for a city from the configured provider."""
    return {"status": "success", "city": city}


root = LlmAgent(name="weather", model="m", instruction="Answer weather questions.",
                tools=[FunctionTool(lookup_weather)])
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["findings"], [])
        self.assertEqual(data["counts"], {})
        agent = self.agent(data, "weather")
        self.assertEqual(agent["flags"], [])
        self.assertFalse(agent["trifecta"]["all_three"])
        self.assertEqual([tool["kind"] for tool in agent["tools"]], ["function_tool"])
        self.assertTrue(agent["instruction_present"])

    def test_each_finding_kind_fires_on_the_trifecta_fixture(self):
        self.write("agent.py", TRIFECTA_AGENT)
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        counts = data["counts"]
        for kind in ("mcp_unfiltered", "mcp_stdio_transport", "write_tool_without_gate", "unsafe_code_executor",
                     "identity_parameter_review", "egress_capable_tool", "untrusted_content_source",
                     "trifecta_present", "unresolved_tool_reference"):
            self.assertIn(kind, counts, kind)
        self.assertEqual({f["subject"] for f in self.findings(data, "write_tool_without_gate")},
                         {"send_email", "post_message (mcp)"})
        self.assertEqual(self.findings(data, "identity_parameter_review")[0]["subject"], "search_customer_records")
        self.assertIn("user_id", self.findings(data, "identity_parameter_review")[0]["detail"])
        egress = {f["subject"] for f in self.findings(data, "egress_capable_tool")}
        self.assertEqual(egress, {"send_email", "post_message (mcp)", "url_context"})
        self.assertIn("httpx.post", next(f for f in self.findings(data, "egress_capable_tool")
                                          if f["subject"] == "send_email")["detail"])
        untrusted = {f["subject"] for f in self.findings(data, "untrusted_content_source")}
        self.assertTrue({"google_search", "url_context", "root", "search_customer_records"} <= untrusted)
        self.assertNotIn("send_email", untrusted)
        self.assertEqual(self.findings(data, "unsafe_code_executor")[0]["subject"], "root")
        self.assertEqual([f["subject"] for f in self.findings(data, "trifecta_present")], ["root"])
        self.assertEqual(self.findings(data, "unresolved_tool_reference")[0]["subject"], "missing_tool")
        self.assertNotIn("trifecta_across_workflow", counts)

    def test_agent_inventory_fields(self):
        self.write("agent.py", TRIFECTA_AGENT)
        _, data = self.scan()
        root = self.agent(data, "root")
        self.assertEqual(root["class"], "LlmAgent")
        self.assertEqual(root["code_executor"], "UnsafeLocalCodeExecutor")
        self.assertEqual(root["callbacks"], ["before_model_callback"])
        kinds = {tool["name"]: tool["kind"] for tool in root["tools"]}
        self.assertEqual(kinds, {"search_customer_records": "function", "send_email": "function_tool",
                                 "delete_order": "function_tool", "quarantine": "agent_tool",
                                 "url_context": "builtin", "missing_tool": "unresolved"})
        delete = next(t for t in root["tools"] if t["name"] == "delete_order")
        self.assertEqual(delete["gate"], ["require_confirmation:enabled"])
        self.assertEqual([t["kind"] for t in root["toolsets"]], ["mcp_toolset", "mcp_toolset"])
        by_transport = {t["transport"]: t for t in root["toolsets"]}
        self.assertEqual(by_transport["StdioConnectionParams"]["tool_filter"], "list")
        self.assertEqual(by_transport["StdioConnectionParams"]["allowed_tools"], ["post_message", "read_page"])
        self.assertEqual(by_transport["StreamableHTTPConnectionParams"]["tool_filter"], "absent")
        self.assertEqual(root["sub_agents"], [{"variable": "quarantine", "name": "summariser",
                                               "include_contents": "none", "mode": "single_turn",
                                               "resolved": True}])
        trifecta = root["trifecta"]
        self.assertTrue(trifecta["has_private_data_source"])
        self.assertTrue(trifecta["has_untrusted_content_source"])
        self.assertTrue(trifecta["has_egress"])
        self.assertTrue(trifecta["has_code_execution"])
        self.assertEqual(trifecta["sources"]["sub_agents"], {"quarantine": ["untrusted"]})
        gated = self.agent(data, "gated")
        self.assertEqual(gated["tools"][0]["gate"], ["before_tool_callback"])
        self.assertEqual(self.agent(data, "flow")["class"], "SequentialAgent")
        self.assertEqual(data["plugins"], [{"line": 49, "name": "LoggingPlugin", "path": "agent.py", "runner": "App"}])

    def test_module_attribute_and_imported_tool_references_resolve(self):
        self.write("support/__init__.py", "")
        self.write("support/tools.py", '''
import httpx


def fetch_email(message_id: str) -> dict:
    resp = httpx.get(f"https://mail.invalid/{message_id}")
    return {"status": "success", "body": resp.text}


def search_kb(query: str) -> str:
    return httpx.get("https://kb.invalid", params={"q": query}).text


def get_order(order_ref: str) -> dict:
    return {"status": "success"}


def issue_refund(order_id: str, amount: float, user_id: str) -> dict:
    httpx.post("https://orders.invalid/refunds", json={"order_id": order_id, "user": user_id})
    return {"status": "success"}


def send_email(to: str, body: str) -> dict:
    httpx.post("https://mail.invalid/send", json={"to": to, "body": body})
    return {"status": "success"}
''')
        self.write("support/agent.py", '''
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import tools
from .tools import search_kb as kb
from support import tools as t

triage = LlmAgent(name="triage", model="m", tools=[tools.fetch_email, kb])
refunds = LlmAgent(name="refunds", model="m", tools=[FunctionTool(t.issue_refund), tools.get_order, t.send_email])
root = LlmAgent(name="support_root", model="m", sub_agents=[triage, refunds],
                tools=[tools.fetch_email, tools.search_kb, tools.get_order, tools.send_email, tools.not_there])
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({f["subject"] for f in self.findings(data, "write_tool_without_gate")} & {"issue_refund", "send_email"},
                         {"issue_refund", "send_email"})
        self.assertEqual([f["subject"] for f in self.findings(data, "identity_parameter_review")], ["issue_refund"])
        self.assertTrue({"fetch_email", "search_kb"} <= {f["subject"] for f in self.findings(data, "untrusted_content_source")})
        self.assertTrue({"send_email", "issue_refund"} <= {f["subject"] for f in self.findings(data, "egress_capable_tool")})
        self.assertIn("support_root", {f["subject"] for f in self.findings(data, "trifecta_present")})
        refunds = self.agent(data, "refunds")
        self.assertEqual({tool["name"]: tool["kind"] for tool in refunds["tools"]},
                         {"issue_refund": "function_tool", "get_order": "function", "send_email": "function"})
        self.assertEqual(next(t for t in refunds["tools"] if t["name"] == "issue_refund")["defined_at"], "support/tools.py:18")
        self.assertEqual([f["subject"] for f in self.findings(data, "unresolved_tool_reference")], ["tools.not_there"])

    def test_workflow_combining_legs_is_flagged_once(self):
        self.write("agent.py", WORKFLOW_SPLIT)
        _, data = self.scan()
        self.assertEqual([f["subject"] for f in self.findings(data, "trifecta_across_workflow")], ["pipeline"])
        self.assertEqual(self.findings(data, "trifecta_present"), [])
        self.assertEqual(self.findings(data, "write_tool_without_gate"), [])
        reader = self.agent(data, "reader")
        self.assertEqual(reader["flags"], ["private", "untrusted"])
        self.assertFalse(reader["trifecta"]["all_three"])

    def test_dynamic_tools_and_unresolved_sub_agents_are_reported(self):
        self.write("agent.py", '''
from google.adk.agents import LlmAgent
root = LlmAgent(name="root", model="m", tools=build_tools(), sub_agents=[elsewhere])
''')
        _, data = self.scan()
        self.assertEqual(data["counts"], {"tools_not_literal": 1, "unresolved_agent_reference": 1})
        self.assertFalse(self.agent(data, "root")["tools_literal"])

    def test_openapi_and_database_toolsets(self):
        self.write("agent.py", '''
from google.adk.agents import LlmAgent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.bigquery import BigQueryToolset
root = LlmAgent(name="root", model="m", tools=[OpenAPIToolset(spec_str="{}"), BigQueryToolset()])
''')
        _, data = self.scan()
        root = self.agent(data, "root")
        self.assertEqual({t["kind"] for t in root["toolsets"]}, {"openapi_toolset", "BigQueryToolset"})
        self.assertEqual(root["flags"], ["egress", "private", "untrusted"])
        self.assertEqual([f["subject"] for f in self.findings(data, "trifecta_present")], ["root"])

    def test_version_pins_below_cve_floor(self):
        self.write("requirements.txt", "google-adk==2.6.3\nhttpx>=0.28\n")
        self.write("pyproject.toml", '[project]\ndependencies = ["google-adk>=2.8.0,<3"]\n[tool.poetry.dependencies]\ngoogle-adk = {version = "~2.4"}\n')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        statuses = {(item["path"], item["lowest_version"]): item["status"] for item in data["adk_pins"]}
        self.assertEqual(statuses, {("requirements.txt", "2.6.3"): "below_cve_floor",
                                    ("pyproject.toml", "2.8.0"): "at_or_above_cve_floor",
                                    ("pyproject.toml", "2.4.0"): "below_cve_floor"})
        self.assertEqual(data["counts"]["known_cve_range"], 2)
        self.assertNotIn("httpx", result.stdout)

    def test_bash_policy_container_network_and_confirmation_flags(self):
        self.write("agent.py", '''
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.tools.bash_tool import BashTool, BashToolPolicy
from google.adk.code_executors import ContainerCodeExecutor


def pay_invoice(invoice_id: str) -> dict:
    return {"status": "success"}


def needs_confirmation(**kwargs):
    return "maybe"


open_policy = BashToolPolicy()
star_policy = BashToolPolicy(allowed_command_prefixes=("ls", "*"))
tight_policy = BashToolPolicy(allowed_command_prefixes=("ls", "cat"))
root = LlmAgent(name="root", model="m",
                tools=[BashTool(), BashTool(policy=tight_policy),
                       FunctionTool(pay_invoice, require_confirmation=needs_confirmation)],
                code_executor=ContainerCodeExecutor(image="python:3.11-slim", network_enabled=True))
safe = LlmAgent(name="safe", model="m", code_executor=ContainerCodeExecutor(image="python:3.11-slim"))
''')
        _, data = self.scan()
        self.assertEqual(data["counts"]["bash_policy_allow_all"], 3)
        self.assertEqual([f["subject"] for f in self.findings(data, "container_executor_network_enabled")], ["ContainerCodeExecutor"])
        self.assertEqual([f["subject"] for f in self.findings(data, "confirmation_callable_review")], ["pay_invoice"])
        self.assertEqual(self.findings(data, "write_tool_without_gate"), [])
        root = self.agent(data, "root")
        self.assertEqual(root["code_executor"], "ContainerCodeExecutor")
        self.assertNotIn("unsafe_code_executor", data["counts"])
        self.assertEqual([t["kind"] for t in root["tools"]], ["bash_tool", "bash_tool", "function_tool"])
        self.assertEqual(root["tools"][2]["gate"], ["require_confirmation:dynamic"])

    def test_custom_base_tool_confirmation_and_remote_agents(self):
        self.write("agent.py", '''
from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools import BaseTool


class ForgetfulTool(BaseTool):
    def __init__(self):
        super().__init__(name="forgetful", description="d", require_confirmation=True)

    async def run_async(self, *, args, tool_context):
        return {"status": "ran"}


class CarefulTool(BaseTool):
    def __init__(self):
        super().__init__(name="careful", description="d", require_confirmation=True)

    async def run_async(self, *, args, tool_context):
        if not tool_context.tool_confirmation or not tool_context.tool_confirmation.confirmed:
            tool_context.request_confirmation(hint="approve")
            return {"status": "pending_approval"}
        return {"status": "ran"}


def delete_record(record_id: str) -> dict:
    return {"status": "success"}


def lookup_hours(store: str) -> dict:
    return {"status": "success"}


peer = RemoteA2aAgent(name="peer", description="remote", agent_card="https://peer.invalid/card")
root = LlmAgent(name="root", model="m", tools=[delete_record], sub_agents=[peer])
reader = LlmAgent(name="reader", model="m", tools=[lookup_hours],
                  sub_agents=[RemoteA2aAgent(name="inline_peer", description="remote", agent_card="https://p.invalid")])
''')
        _, data = self.scan()
        self.assertEqual([f["subject"] for f in self.findings(data, "custom_tool_ignores_confirmation")], ["ForgetfulTool"])
        self.assertEqual([f["subject"] for f in self.findings(data, "remote_content_with_write_tools")], ["root"])
        root = self.agent(data, "root")
        self.assertEqual(root["remote_sub_agents"], ["peer"])
        self.assertEqual(root["sub_agents"], [])
        self.assertEqual(root["flags"], ["remote", "untrusted"])
        self.assertTrue(root["trifecta"]["has_remote_agent_content"])
        reader = self.agent(data, "reader")
        self.assertEqual(reader["remote_sub_agents"], ["inline_peer"])
        self.assertNotIn("unresolved_agent_reference", data["counts"])
        self.assertIn("write_tool_without_gate", data["counts"])

    def test_unauthenticated_exposure_hints(self):
        self.write("deploy.sh", "gcloud run deploy agent --allow-unauthenticated --region=europe-west1\n")
        self.write("safe.sh", "gcloud run deploy agent --no-allow-unauthenticated\n")
        self.write("cloudbuild.yaml", "args: ['run', 'deploy', '--allow-unauthenticated']\n")
        self.write("deploy.py", 'COMMAND = "gcloud run deploy x --allow-unauthenticated"\ndeploy(service, allow_unauthenticated=True)\nsafe(allow_unauthenticated=False)\n')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        hints = self.findings(data, "unauthenticated_exposure_hint")
        self.assertEqual(sorted((h["path"], h["line"]) for h in hints),
                         [("cloudbuild.yaml", 1), ("deploy.py", 1), ("deploy.py", 2), ("deploy.sh", 1)])
        self.assertNotIn("europe-west1", result.stdout)

    def test_output_never_echoes_source_text_or_absolute_paths(self):
        marker = "PRIVATE_SOURCE_TEXT_THAT_MUST_NOT_APPEAR"
        self.write("agent.py", f'''
from google.adk.agents import LlmAgent
SECRET = "{marker}"
def send_report(to: str) -> dict:
    """{marker}"""
    return {{"status": "success"}}
root = LlmAgent(name="root", model="m", instruction="{marker}", tools=[send_report])
''')
        for name in (".env", "credentials.json", "secrets.py", ".venv/leak.py"):
            self.write(name, marker)
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout)
        self.assertEqual(data["files_inspected"], 1)

    def test_bounds_report_partial_scan_with_exit_one(self):
        self.write("a.py", "a = 1\n")
        self.write("b.py", "b = 2\n")
        result, data = self.scan("--max-files", "1")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(data["partial"])
        self.assertIn("file_count_limit", {item["reason"] for item in data["issues"]})
        result, data = self.scan("--max-bytes", "1")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(all(item["reason"] == "file_size_limit" for item in data["issues"]))
        self.write("one/two/hidden.py", "pass\n")
        result, data = self.scan("--max-depth", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn({"path": "one/two", "reason": "depth_limit"}, data["issues"])
        result, data = self.scan("--max-entries", "2")
        self.assertEqual(result.returncode, 1)
        self.assertIn("entry_count_limit", {item["reason"] for item in data["issues"]})

    def test_malformed_and_symlinked_files_are_partial(self):
        marker = "PRIVATE_SOURCE_TEXT"
        self.write("bad.py", f"def {marker}(\n")
        (self.root / "binary.py").write_bytes(b"\xff")
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("x = 1\n")
        (self.root / "link.py").symlink_to(outside)
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertEqual({item["reason"] for item in data["issues"]}, {"malformed_file", "unreadable_file", "symlink_skipped"})
        (self.root / "directory").symlink_to(self.root, target_is_directory=True)
        self.assertEqual(self.run_cli("--project", str(self.root / "directory")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
