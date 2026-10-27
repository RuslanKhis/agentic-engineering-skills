import json
import re
import tomllib
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CARD = json.loads((ROOT / "a2a" / "agent-card.json").read_text())
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text())


class CardTests(unittest.TestCase):
    def test_interface_is_https_with_protocol_version(self):
        ifaces = CARD["supportedInterfaces"]
        self.assertTrue(ifaces)
        for i in ifaces:
            self.assertEqual(urlparse(i["url"]).scheme, "https")
            self.assertRegex(i["protocolVersion"], r"^\d+\.\d+$")
            self.assertIn(i["protocolBinding"], {"JSONRPC", "GRPC", "HTTP+JSON"})

    def test_card_is_1_0_shape(self):
        for old in ("url", "protocolVersion", "preferredTransport", "security",
                    "supportsAuthenticatedExtendedCard"):
            self.assertNotIn(old, CARD)

    def test_version_matches_project_and_is_semver(self):
        self.assertRegex(CARD["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(CARD["version"], PYPROJECT["project"]["version"])

    def test_only_client_credentials_flow_declared(self):
        scheme = CARD["securitySchemes"]["partner_oauth"]["oauth2SecurityScheme"]
        self.assertEqual(set(scheme["flows"]), {"clientCredentials"})
        self.assertEqual(urlparse(scheme["flows"]["clientCredentials"]["tokenUrl"]).scheme, "https")

    def test_card_and_skill_requirements_name_declared_scheme_and_scope(self):
        scopes = CARD["securitySchemes"]["partner_oauth"]["oauth2SecurityScheme"][
            "flows"]["clientCredentials"]["scopes"]
        reqs = list(CARD["securityRequirements"])
        for skill in CARD["skills"]:
            reqs += skill.get("securityRequirements", [])
        self.assertGreaterEqual(len(reqs), 2)
        for req in reqs:
            for name, wanted in req["schemes"].items():
                self.assertIn(name, CARD["securitySchemes"])
                self.assertTrue(set(wanted["list"]) <= set(scopes))

    def test_card_does_not_leak_instruction_or_internals(self):
        text = json.dumps(CARD).lower()
        for needle in ("instruction", "gemini", "record_triage", "lookup_product", "api_key"):
            self.assertNotIn(needle, text)

    def test_skills_complete(self):
        ids = [s["id"] for s in CARD["skills"]]
        self.assertEqual(len(ids), len(set(ids)))
        for s in CARD["skills"]:
            for key in ("id", "name", "description", "tags"):
                self.assertTrue(s.get(key))

    def test_a2a_sdk_pin_is_1x(self):
        deps = " ".join(PYPROJECT["project"]["dependencies"])
        self.assertTrue(re.search(r"a2a-sdk\[http-server\]>=1\.0,<2", deps))


if __name__ == "__main__":
    unittest.main()
