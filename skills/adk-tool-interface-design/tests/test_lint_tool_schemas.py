"""Exercise the tool-interface linter through its CLI with isolated fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lint_tool_schemas.py"

CLEAN = '''
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool, ToolContext


def lookup_order(order_id: str, tool_context: ToolContext) -> dict:
    """Return the status, items and shipping dates for one customer order.

    Use after the customer has confirmed the order number; order numbers look
    like ORD-123456. Returns a status key and an error hint on failure.
    """
    return {"status": "success", "order_id": order_id}


def cancel_order(order_id: str, reason: str = "customer_request") -> dict:
    """Cancel an order that has not shipped yet and return the refund outcome.

    Only call after the customer confirms cancellation. Shipped orders cannot be
    cancelled; use lookup_order first to check the status.
    """
    if not order_id:
        return {"status": "error", "error": "order_id is required", "hint": "ask the customer"}
    return {"status": "success", "refund": "pending"}


billing = LlmAgent(
    name="billing",
    description="Answers questions about invoices, refunds and payment methods for existing orders.",
)
root = LlmAgent(
    name="root",
    tools=[FunctionTool(lookup_order), cancel_order],
    sub_agents=[billing],
)
'''


class LintTests(unittest.TestCase):
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
        return [f for f in data["findings"] if f["finding"] == kind]

    def test_installed_skill_and_evidence_folders_are_not_scanned(self):
        bad = ('from google.adk.agents import LlmAgent\n'
               'def f(x):\n    return "s"\n'
               'agent = LlmAgent(name="a", description="d", tools=[f])\n')
        for folder in (".claude/skills/demo", ".agents/skills/demo", ".adk-evidence"):
            self.write(f"{folder}/agent.py", bad)
        _, data = self.scan()
        paths = {f.get("path", "") for f in data["findings"]}
        self.assertFalse(any(part in p for p in paths for part in (".claude", ".agents", ".adk-evidence")), paths)
        self.assertEqual(data.get("tools", []), [])

    def test_help_and_invalid_arguments(self):
        result = self.run_cli("--help", project=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--max-tools", result.stdout)
        self.assertEqual(self.run_cli(project=False).returncode, 2)
        for option in ("--max-tools", "--max-files", "--max-bytes", "--max-depth", "--max-entries"):
            for value in ("0", "-1", "x"):
                self.assertEqual(self.run_cli(option, value).returncode, 2)
        self.assertEqual(self.run_cli("--project", str(self.root / "absent")).returncode, 2)

    def test_clean_fixture_has_no_findings_and_is_repeatable(self):
        self.write("agent.py", CLEAN)
        first, data = self.scan("--dry-run")
        second, _ = self.scan("--dry-run")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(data["read_only"] and data["dry_run"] and not data["changes_made"])
        self.assertEqual(data["findings"], [])
        self.assertEqual(data["counts"], {})
        self.assertEqual([t["name"] for t in data["tools"]], ["cancel_order", "lookup_order"])
        self.assertEqual(data["agents"][1]["tool_count"], 2)

    def test_docstring_findings(self):
        self.write("tools.py", '''
from google.adk.tools import FunctionTool

def no_doc(city: str) -> dict:
    return {"status": "success"}

def one_liner(city: str) -> dict:
    """Get weather."""
    return {"status": "success"}

a = FunctionTool(no_doc)
b = FunctionTool(one_liner)
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual([f["subject"] for f in self.findings(data, "missing_docstring")], ["no_doc"])
        self.assertEqual([f["subject"] for f in self.findings(data, "short_docstring")], ["one_liner"])
        self.assertEqual(self.findings(data, "missing_docstring")[0]["line"], 4)
        self.assertNotIn("Get weather", result.stdout)

    def test_parameter_findings(self):
        self.write("tools.py", '''
from google.adk.agents import Agent

def send_message(data, value: str, on: bool = False, off: bool = False,
                 enable_html: bool = False, disable_html: bool = False, *args, **kwargs) -> dict:
    """Send one message to the customer's preferred channel and return delivery status.

    Use only after the customer has agreed to be contacted. Returns status and a message id.
    """
    return {"status": "success"}

root = Agent(name="root", tools=[send_message])
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual({f["detail"] for f in self.findings(data, "untyped_parameter")}, {"data"})
        self.assertEqual({f["detail"] for f in self.findings(data, "generic_parameter_name")}, {"data", "value"})
        self.assertEqual(len(self.findings(data, "variadic_parameter")), 1)
        pairs = {f["detail"].split(":")[0] for f in self.findings(data, "exclusive_boolean_pair")}
        self.assertEqual(pairs, {"off/on", "disable_html/enable_html"})

    def test_identity_parameter_review(self):
        self.write("tools.py", '''
from google.adk.tools import FunctionTool, ToolContext

def get_profile(user_id: str, email: str, tool_context: ToolContext) -> dict:
    """Return the profile for a user, including name and contact preferences.

    Use when the agent needs to personalise a reply. Returns status and profile fields.
    """
    return {"status": "success"}

t = FunctionTool(get_profile)
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        details = sorted(f["detail"].split(":")[0] for f in self.findings(data, "identity_parameter_review"))
        self.assertEqual(details, ["email", "user_id"])
        self.assertEqual(self.findings(data, "untyped_parameter"), [])

    def test_return_findings(self):
        self.write("tools.py", '''
from google.adk.tools import LongRunningFunctionTool, FunctionTool

def as_text(city: str) -> str:
    """Return the weather for a city as a sentence the agent can relay.

    Use when the customer asks about current conditions. Returns plain text.
    """
    return f"Sunny in {city}"

def as_list(city: str) -> list:
    """Return the forecast for a city as a list of daily entries.

    Use when the customer asks about the coming days. Returns a list.
    """
    return [city]

def no_status(city: str) -> dict:
    """Return the forecast for a city with a dictionary keyed by day name.

    Use when the customer asks for a week view. Returns a dictionary.
    """
    def inner():
        return "ignored nested"
    if city:
        return {"forecast": []}
    return {"status": "error", "error": "city required", "hint": "ask for the city"}

a = LongRunningFunctionTool(as_text)
b = FunctionTool(as_list)
c = FunctionTool(no_status)
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        subjects = sorted(f["subject"] for f in self.findings(data, "non_dict_return"))
        self.assertEqual(subjects, ["as_list", "as_text"])
        self.assertEqual([f["subject"] for f in self.findings(data, "missing_status_key")], ["no_status"])
        self.assertEqual(len(self.findings(data, "missing_status_key")), 1)

    def test_near_duplicate_tools_and_duplicate_names(self):
        self.write("a.py", '''
from google.adk.tools import FunctionTool

def get_customer_orders(customer_ref: str) -> dict:
    """List the recent orders for a customer with their status and totals.

    Use when the customer asks about order history. Returns status and orders.
    """
    return {"status": "success"}

def get_customer_orders_v2(customer_ref: str) -> dict:
    """List the recent orders for a customer with their status and totals.

    Newer variant that includes shipping events. Returns status and orders.
    """
    return {"status": "success"}

x = FunctionTool(get_customer_orders)
y = FunctionTool(get_customer_orders_v2)
''')
        self.write("b.py", '''
from google.adk.tools import FunctionTool

def get_customer_orders(customer_ref: str) -> dict:
    """Return orders for a customer from the legacy store with their totals.

    Use only when the newer store has no record. Returns status and orders.
    """
    return {"status": "success"}

z = FunctionTool(get_customer_orders)
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(self.findings(data, "duplicate_tool_name")), 2)
        self.assertTrue(self.findings(data, "similar_tool_names"))
        self.assertTrue(self.findings(data, "similar_tool_descriptions"))
        self.assertNotIn("legacy store", result.stdout)

    def test_tool_count_and_toolsets(self):
        tools = "\n".join(
            f'def tool_{i}(query_{i}: str) -> dict:\n'
            f'    """Search source {i} for the query and return matching rows.\n\n'
            f'    Use for source {i} only. Returns status and rows.\n    """\n'
            f'    return {{"status": "success"}}\n' for i in range(4))
        self.write("agent.py", f'''
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
{tools}
root = LlmAgent(name="root", tools=[tool_0, tool_1, tool_2, tool_3, McpToolset(connection_params=None)])
dynamic = LlmAgent(name="dynamic", tools=build_tools())
''')
        result, data = self.scan("--max-tools", "3")
        self.assertEqual(result.returncode, 0)
        self.assertEqual([f["subject"] for f in self.findings(data, "tool_count_exceeds_max")], ["root"])
        self.assertEqual([f["subject"] for f in self.findings(data, "toolset_count_unknown")], ["root"])
        self.assertEqual([f["subject"] for f in self.findings(data, "tools_not_literal")], ["dynamic"])
        self.assertEqual(self.scan("--max-tools", "5")[1]["counts"].get("tool_count_exceeds_max"), None)
        self.assertEqual(self.findings(data, "similar_tool_names"), [])

    def test_sub_agent_descriptions(self):
        self.write("agents.py", '''
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

short = LlmAgent(name="short", description="short")
few = LlmAgent(name="few", description="Handles billing.")
good = LlmAgent(name="good", description="Answers questions about invoices, refunds and payment methods for orders.", mode="single_turn")
missing = LlmAgent(name="missing")
dynamic = LlmAgent(name="dynamic", description=build_description())
root = LlmAgent(name="root", tools=[AgentTool(good), AgentTool(agent=missing)], sub_agents=[short, few, dynamic, elsewhere])
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(sorted(f["subject"] for f in self.findings(data, "short_agent_description")), ["few", "short"])
        self.assertEqual([f["subject"] for f in self.findings(data, "missing_agent_description")], ["missing"])
        self.assertEqual([f["subject"] for f in self.findings(data, "unresolved_agent_reference")], ["elsewhere"])
        self.assertEqual(len(data["agents"]), 6)
        self.assertEqual([a["mode"] for a in data["agents"] if a["name"] == "good"], ["single_turn"])

    def test_type_raise_blocking_and_default_findings(self):
        self.write("tools.py", '''
from enum import Enum
from typing import Union
from pydantic import BaseModel
import requests
from google.adk.tools import FunctionTool, ToolContext

class Units(Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

class Profile(BaseModel):
    name: str

def weather(city: str = "Paris", units: Units = Units.METRIC, tags: list = None,
            days: int | None = None, when: Union[str, int] = 1, profile: Profile = None,
            fmt: str = "concise", tool_context: ToolContext = None) -> dict:
    """Return the weather for a city in the requested units for the coming days.

    Use when the customer asks about conditions; pass tool_context for state.
    """
    if not city:
        raise ValueError("city required")
    requests.get("https://example.invalid")
    return {"status": "success"}

async def forecast(city: str) -> dict:
    """Return the seven day forecast for a city as a list of daily summaries.

    Use when the customer asks about the coming week. Returns status and days.
    """
    if not city:
        return {"status": "error", "error_message": "city required", "hint": "ask"}
    raise RuntimeError("unexpected")

a = FunctionTool(weather)
b = FunctionTool(forecast)
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        details = {f["finding"]: sorted(x["detail"].split(":")[0] for x in self.findings(data, f["finding"]))
                   for f in data["findings"]}
        self.assertEqual(details["bare_container_annotation"], ["tags"])
        self.assertEqual(details["pep604_union_parameter"], ["days"])
        self.assertEqual(details["complex_parameter_type_review"], ["profile", "when"])
        self.assertEqual(details["domain_default_review"], ["city"])
        self.assertEqual([f["subject"] for f in self.findings(data, "raise_in_tool_body")], ["weather"])
        self.assertEqual([f["subject"] for f in self.findings(data, "sync_io_blocks_parallelism")], ["weather"])
        self.assertEqual([f["subject"] for f in self.findings(data, "docstring_mentions_context")], ["weather"])
        self.assertNotIn("example.invalid", result.stdout)

    def test_unresolved_tool_reference(self):
        self.write("agent.py", "from google.adk.agents import LlmAgent\nfrom lib import remote\nroot = LlmAgent(name='r', tools=[remote])\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual([f["subject"] for f in self.findings(data, "unresolved_tool_reference")], ["remote"])

    def test_module_attribute_and_imported_tool_references_resolve(self):
        self.write("pkg/__init__.py", "")
        self.write("pkg/tools.py", '''
def search_orders(value: str) -> dict:
    """Search orders."""
    return {"status": "success"}


def issue_refund(order_id: str, user_id: str) -> dict:
    """Issue a refund."""
    raise RuntimeError("refund failed")


def search_kb(query: str) -> str:
    """Search the knowledge base."""
    return "\\n\\n".join(article for article in [query])


def get_order(data: str) -> dict:
    """Get an order."""
    return {"status": "success"}
''')
        self.write("pkg/agent.py", '''
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import tools
from .tools import search_kb as kb
from pkg import tools as t

root = LlmAgent(name="root", tools=[tools.search_orders, FunctionTool(t.issue_refund), kb, tools.missing_fn])
other = LlmAgent(name="other", tools=[pkg.tools.get_order])
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(t["name"] for t in data["tools"]),
                         ["get_order", "issue_refund", "search_kb", "search_orders"])
        self.assertEqual(sorted(f["subject"] for f in self.findings(data, "generic_parameter_name")),
                         ["get_order", "search_orders"])
        self.assertEqual([f["subject"] for f in self.findings(data, "identity_parameter_review")], ["issue_refund"])
        self.assertEqual([f["subject"] for f in self.findings(data, "raise_in_tool_body")], ["issue_refund"])
        self.assertEqual([f["subject"] for f in self.findings(data, "non_dict_return")], ["search_kb"])
        self.assertEqual(len(self.findings(data, "short_docstring")), 4)
        self.assertEqual([f["subject"] for f in self.findings(data, "unresolved_tool_reference")], ["tools.missing_fn"])
        self.assertEqual(data["unresolved_tool_references"], 1)

    def test_partial_scan_exit_code_and_bounds(self):
        marker = "PRIVATE_SOURCE_TEXT"
        self.write("bad.py", f"def {marker}(\n")
        self.write("ok.py", CLEAN)
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertIn({"path": "bad.py", "reason": "malformed_file"}, data["issues"])
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertEqual(data["files_inspected"], 1)
        self.write("deep/one/two/hidden.py", "pass\n")
        result, data = self.scan("--max-depth", "1")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(i["reason"] == "depth_limit" for i in data["issues"]))
        result, data = self.scan("--max-files", "1")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(i["reason"] == "file_count_limit" for i in data["issues"]))

    def test_sensitive_and_excluded_paths_are_skipped(self):
        marker = "CREDENTIAL_VALUE_THAT_MUST_NOT_APPEAR"
        for name in (".env", "secrets.py", ".venv/leak.py", "node_modules/leak.py"):
            self.write(name, f"x = '{marker}'\n")
        self.write("agent.py", CLEAN)
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text(CLEAN)
        (self.root / "link.py").symlink_to(outside)
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertEqual({i["reason"] for i in data["issues"]}, {"symlink_skipped"})
        self.assertEqual(data["files_inspected"], 1)


if __name__ == "__main__":
    unittest.main()
