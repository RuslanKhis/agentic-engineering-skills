"""The configuration Snyk Agent Scan reads must start exactly what the agent starts, and nothing secret."""
import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCAN_CONFIG = ROOT / "mcp-scan" / "freightline-shipping.json"


def agent_command() -> tuple[str, list[str]]:
    """Read command and args of the StdioServerParameters call in app/agent.py without importing it."""
    tree = ast.parse((ROOT / "app" / "agent.py").read_text())
    constants = {
        t.id: ast.literal_eval(n.value)
        for n in tree.body
        if isinstance(n, ast.Assign)
        for t in n.targets
        if isinstance(t, ast.Name) and isinstance(n.value, ast.Constant)
    }

    def resolve(node):
        if isinstance(node, ast.Name):
            return constants[node.id]
        return ast.literal_eval(node)

    calls = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", "")) == "StdioServerParameters"
    ]
    assert len(calls) == 1, "expected exactly one StdioServerParameters call in app/agent.py"
    kwargs = {k.arg: k.value for k in calls[0].keywords}
    return resolve(kwargs["command"]), [resolve(a) for a in kwargs["args"].elts]


class ScanConfigTests(unittest.TestCase):
    def setUp(self):
        self.servers = json.loads(SCAN_CONFIG.read_text())["mcpServers"]

    def test_scanned_command_equals_agent_command(self):
        command, args = agent_command()
        self.assertEqual(len(self.servers), 1)
        (server,) = self.servers.values()
        self.assertEqual((server["command"], server["args"]), (command, args))

    def test_scan_config_holds_no_credentials(self):
        (server,) = self.servers.values()
        self.assertEqual(set(server), {"command", "args"})

    def test_scanned_package_is_pinned_to_the_recorded_version(self):
        manifest = json.loads((ROOT / "mcp" / "freightline-shipping.tools.json").read_text())
        (server,) = self.servers.values()
        self.assertIn(f"{manifest['server']}@{manifest['version']}", server["args"])


if __name__ == "__main__":
    unittest.main()
