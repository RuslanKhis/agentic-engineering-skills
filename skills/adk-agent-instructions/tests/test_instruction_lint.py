"""Exercise the instruction lint through its public CLI using isolated local fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "instruction_lint.py"

CLEAN_AGENT = '''from google.adk.agents import LlmAgent

def lookup_order(order_id: str) -> dict:
    """Return the order record for an order id."""

INSTRUCTION = """You are the order assistant for {company}.
Decide whether the customer needs an order status or a policy explanation.
Call `lookup_order` when the customer gives an order number; otherwise ask for it.
Inputs: the current message and the plan {user:plan?}.
Answer in two short paragraphs and name the order id you used.
"""

orders = LlmAgent(name="order_agent", description="Looks up order status for an order number the customer provides",
                  instruction=INSTRUCTION, tools=[lookup_order])
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

    @staticmethod
    def agent(data, name):
        return next(a for a in data["agents"] if a["name"] == name)

    @staticmethod
    def codes(agent):
        return {f["code"] for f in agent["findings"]}

    def test_help_and_invalid_arguments(self):
        result = self.run_cli("--help", project=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--state-keys", result.stdout)
        self.assertIn("--prompt-file", result.stdout)
        self.assertEqual(self.run_cli(project=False).returncode, 2)
        self.assertEqual(self.run_cli("--project", str(self.root / "absent")).returncode, 2)
        for option in ("--max-words", "--max-files", "--max-bytes", "--max-depth", "--max-entries"):
            for value in ("0", "-1", "words"):
                self.assertEqual(self.run_cli(option, value).returncode, 2)
        self.assertEqual(self.run_cli("--prompt-file", str(self.root / "missing.md")).returncode, 2)

    def test_clean_fixture_is_read_only_and_deterministic(self):
        marker = self.root / "executed.txt"
        self.write("agent.py", CLEAN_AGENT + f"\nfrom pathlib import Path\nPath({str(marker)!r}).write_text('x')\n")
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        first, data = self.scan("--dry-run", "--state-keys", "company")
        second, _ = self.scan("--dry-run", "--state-keys", "company")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(data["read_only"] and data["dry_run"] and not data["changes_made"])
        regular, regular_data = self.scan("--state-keys", "company")
        regular_data["dry_run"] = True
        self.assertEqual(data, regular_data)
        agent = self.agent(data, "order_agent")
        self.assertEqual(agent["findings"], [])
        self.assertEqual(agent["placeholders"]["resolved"], ["company"])
        self.assertEqual(agent["placeholders"]["optional"], ["user:plan"])
        self.assertEqual(agent["tools"], ["lookup_order"])
        self.assertEqual(data["summary"]["finding_counts"], {})
        self.assertFalse(marker.exists())
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_placeholders_against_state_keys(self):
        self.write("agent.py", 'from google.adk.agents import Agent\n'
                   'a = Agent(name="a", instruction="Plan {app:plan} for {customer}; notes {notes?}; '
                   'doc {artifact.brief}; keep {not valid} and {{k: 1}}")\n')
        _, data = self.scan()
        agent = self.agent(data, "a")
        self.assertEqual(agent["placeholders"]["unresolved"], ["app:plan", "customer"])
        self.assertEqual(agent["placeholders"]["optional"], ["notes"])
        self.assertEqual(agent["placeholders"]["artifact"], ["artifact.brief"])
        self.assertEqual(agent["placeholders"]["literal_matches_left_unchanged"], 2)
        detail = next(f["detail"] for f in agent["findings"] if f["code"] == "unresolved_placeholder")
        self.assertIn("app:plan, customer", detail)
        _, data = self.scan("--state-keys", "app:plan, customer")
        self.assertNotIn("unresolved_placeholder", self.codes(self.agent(data, "a")))
        self.assertEqual(self.agent(data, "a")["placeholders"]["resolved"], ["app:plan", "customer"])

    def test_literal_braces_and_escape_syntax(self):
        self.write("agent.py", 'from google.adk.agents import LlmAgent\n'
                   'a = LlmAgent(name="a", instruction=\'Reply as {"status": "ok", "id": "{order_id}"}\')\n'
                   'b = LlmAgent(name="b", instruction="Literal \\\\{brace} and ${shell} stay as written")\n')
        _, data = self.scan()
        codes_a = self.codes(self.agent(data, "a"))
        self.assertIn("literal_braces_need_provider_or_escape", codes_a)
        self.assertIn("unresolved_placeholder", codes_a)
        self.assertIn("escape_syntax_requires_2_10", self.codes(self.agent(data, "b")))
        detail = next(f["detail"] for f in self.agent(data, "a")["findings"]
                      if f["code"] == "literal_braces_need_provider_or_escape")
        self.assertIn("2.10.0", detail)

    def test_instruction_kinds(self):
        self.write("agent.py", 'from google.adk.agents import LlmAgent\n'
                   'from prompts import load\n'
                   'import textwrap\n'
                   'TEXT = textwrap.dedent("""Answer about {topic}.""")\n'
                   'def provider(ctx):\n    return "x"\n'
                   'a = LlmAgent(name="a", instruction=provider)\n'
                   'b = LlmAgent(name="b", instruction=lambda ctx: "x")\n'
                   'c = LlmAgent(name="c", instruction=load("c"))\n'
                   'd = LlmAgent(name="d", instruction=TEXT)\n'
                   'e = LlmAgent(name="e", instruction=SOMEWHERE_ELSE)\n'
                   'f = LlmAgent(name="f", instruction=f"Hello {{name}} from {app}")\n')
        _, data = self.scan()
        for name in ("a", "b", "c"):
            agent = self.agent(data, name)
            self.assertEqual(agent["instruction_kind"], "provider")
            self.assertEqual(self.codes(agent), {"instruction_provider_detected"})
            self.assertNotIn("word_count", agent)
        d = self.agent(data, "d")
        self.assertEqual(d["instruction_kind"], "string")
        self.assertEqual(d["placeholders"]["unresolved"], ["topic"])
        self.assertEqual(self.codes(self.agent(data, "e")), {"instruction_unresolved_reference"})
        f = self.agent(data, "f")
        self.assertEqual(f["instruction_kind"], "fstring")
        self.assertIn("fstring_instruction", self.codes(f))
        self.assertEqual(f["placeholders"]["unresolved"], ["name"])

    def test_deprecated_global_static_and_mode(self):
        self.write("agent.py", 'from google.adk.agents import LlmAgent\n'
                   'root = LlmAgent(name="root", instruction="Route {topic?} work.", static_instruction="Persona.",\n'
                   '                global_instruction="Be brief.")\n'
                   'worker = LlmAgent(name="worker", mode="task", include_contents="none",\n'
                   '                  instruction="Finish then call transfer_to_agent to hand back.")\n')
        _, data = self.scan()
        root = self.agent(data, "root")
        self.assertEqual(self.codes(root), {"deprecated_global_instruction", "instruction_sent_as_dynamic_content"})
        worker = self.agent(data, "worker")
        self.assertEqual(worker["mode"], "task")
        self.assertEqual(worker["include_contents"], "none")
        self.assertIn("transfer_mentioned_in_non_chat_mode", self.codes(worker))

    def test_phrasing_signals(self):
        shouting = ("You MUST ALWAYS call search before responding. NEVER guess. CRITICAL: do not skip. "
                    "Do not mention prices. Always include the ticket id in the answer. "
                    "Never include the ticket id in the answer. Answer briefly.")
        self.write("agent.py", 'from google.adk.agents import LlmAgent\n'
                   f'a = LlmAgent(name="a", instruction={shouting!r})\n')
        _, data = self.scan("--max-words", "20")
        agent = self.agent(data, "a")
        codes = self.codes(agent)
        self.assertTrue({"shouting_modifier_density", "mandatory_tool_call_phrasing", "prohibition_only_sentences",
                         "possible_contradiction", "instruction_over_budget"} <= codes)
        mandates = next(f["detail"] for f in agent["findings"] if f["code"] == "mandatory_tool_call_phrasing")
        self.assertIn("always call", mandates)
        self.assertIn("before responding", mandates)
        contradiction = next(f["detail"] for f in agent["findings"] if f["code"] == "possible_contradiction")
        self.assertIn("human review", contradiction)
        self.assertGreater(agent["shouting_per_100_words"], 1.0)
        self.assertGreaterEqual(agent["prohibition_only_sentences"], 2)

    def test_tool_cross_references(self):
        self.write("agent.py", 'from google.adk.agents import LlmAgent\n'
                   'from google.adk.tools import FunctionTool\n'
                   'def lookup_order(order_id: str) -> dict:\n    """Doc."""\n'
                   'def issue_refund(order_id: str) -> dict:\n    """Doc."""\n'
                   'a = LlmAgent(name="a", instruction="Use `lookup_order` for status and call search_docs for '
                   'policy. Offer to help.", tools=[lookup_order, FunctionTool(func=issue_refund)])\n')
        _, data = self.scan()
        agent = self.agent(data, "a")
        self.assertEqual(agent["tools"], ["lookup_order", "issue_refund"])
        details = {f["code"]: f["detail"] for f in agent["findings"]}
        self.assertEqual(details["tool_never_mentioned"], "issue_refund")
        self.assertIn("search_docs", details["unknown_tool_reference"])
        self.assertNotIn("lookup_order", details["unknown_tool_reference"])

    def test_sub_agent_descriptions(self):
        self.write("agent.py", 'from google.adk.agents import LlmAgent\n'
                   'billing = LlmAgent(name="billing_agent", description="Billing agent", instruction="x")\n'
                   'support = LlmAgent(name="support_agent", description="Handles billing questions for users",\n'
                   '                   instruction="x")\n'
                   'clear = LlmAgent(name="shipping_agent", instruction="x",\n'
                   '                 description="Tracks shipments and explains delivery delays for an order number")\n'
                   'root = LlmAgent(name="root", instruction="Route.", sub_agents=[billing, support, clear,\n'
                   '                LlmAgent(name="inline", instruction="x")])\n')
        _, data = self.scan()
        root = self.agent(data, "root")
        self.assertEqual(root["sub_agents"], ["billing_agent", "support_agent", "shipping_agent", "inline"])
        similar = [f["detail"] for f in root["findings"] if f["code"] == "similar_sibling_descriptions"]
        self.assertEqual(len(similar), 1)
        self.assertIn("billing_agent vs support_agent", similar[0])
        self.assertEqual(self.codes(self.agent(data, "billing_agent")),
                         {"short_description", "description_equals_name"})
        self.assertEqual(self.codes(self.agent(data, "support_agent")), {"short_description"})
        self.assertEqual(self.codes(self.agent(data, "shipping_agent")), set())
        self.assertEqual(self.codes(self.agent(data, "inline")), {"missing_description"})

    def test_prompt_files_and_prompt_tree(self):
        secret = "PROMPT_BODY_THAT_MUST_NOT_BE_PRINTED"
        self.write("prompts/writer/instruction.md", f"# Role\nSummarise {{source_text}} as {{tone?}}. {secret}\n")
        self.write("prompts/writer/description.txt", "Writes summaries\n")
        extra = self.write("notes/reviewer.md", f"Review {{draft}} with care. {secret}\n")
        self.write("README.md", "not a prompt\n")
        result, data = self.scan("--prompt-file", str(extra), "--state-keys", "source_text")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout)
        writer = self.agent(data, "writer")
        self.assertEqual(writer["source"], "prompt_file")
        self.assertEqual(writer["path"], "prompts/writer/instruction.md")
        self.assertEqual(writer["placeholders"]["resolved"], ["source_text"])
        self.assertEqual(self.codes(writer), {"short_description"})
        reviewer = self.agent(data, "reviewer")
        self.assertEqual(reviewer["path"], "notes/reviewer.md")
        self.assertEqual(reviewer["placeholders"]["unresolved"], ["draft"])
        self.assertEqual(data["files_inspected"], 2)

    def test_bounds_and_malformed_files_are_partial(self):
        marker = "PRIVATE_SOURCE_TEXT"
        self.write("a.py", "a = 1\n")
        self.write("b.py", "b = 2\n")
        result, data = self.scan("--max-files", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("file_count_limit", {i["reason"] for i in data["issues"]})
        self.write("bad.py", f"def {marker}(\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertIn({"path": "bad.py", "reason": "malformed_file"}, data["issues"])
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("x = 1\n")
        (self.root / "link.py").symlink_to(outside)
        result, data = self.scan()
        self.assertIn({"path": "link.py", "reason": "symlink_skipped"}, data["issues"])
        self.assertEqual(self.run_cli("--prompt-file", str(self.root / "link.py")).returncode, 2)

    def test_sensitive_and_excluded_paths_are_skipped(self):
        marker = "SECRET_VALUE_THAT_MUST_NOT_APPEAR"
        for name in (".env", "secrets.py", "credentials.py", ".venv/agent.py", "node_modules/agent.py"):
            self.write(name, f'from google.adk.agents import LlmAgent\nx = LlmAgent(name="leak", instruction="{marker}")\n')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(marker, result.stdout)
        self.assertEqual(data["agents"], [])


if __name__ == "__main__":
    unittest.main()
