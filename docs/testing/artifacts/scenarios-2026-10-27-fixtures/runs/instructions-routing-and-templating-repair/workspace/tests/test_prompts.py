"""Offline checks of the instruction text and the routing contract. No SDK, no model."""
import re
import unittest

from app.prompts import (BILLING_DESCRIPTION, COORDINATOR_INSTRUCTION, ORDERS_DESCRIPTION,
                         REFUNDS_DESCRIPTION)

# google-adk 2.8.0 `inject_session_state` pattern and name rules, mirrored so the test runs without the SDK.
PLACEHOLDER = re.compile(r"{+[^{}]*}+")
STATE_NAME = re.compile(r"^(?:(?:app|user|temp):)?[A-Za-z_][A-Za-z0-9_]*$")


def render_28(template: str, state: dict) -> str:
    def replace(match: re.Match) -> str:
        name = match.group().strip("{} \t\n")
        optional = name.endswith("?")
        name = name.removesuffix("?")
        if not STATE_NAME.match(name):
            return match.group()
        if name not in state:
            if optional:
                return ""
            raise KeyError(f"Context variable not found: `{name}`.")
        return "" if state[name] is None else str(state[name])
    return PLACEHOLDER.sub(replace, template)


class CoordinatorInstructionTests(unittest.TestCase):
    def test_renders_before_load_profile_has_run(self):
        rendered = render_28(COORDINATOR_INSTRUCTION, {})
        self.assertIn('{"route": "orders_agent"', rendered)  # JSON example survives intact
        self.assertNotIn("{customer_profile", rendered)

    def test_renders_with_profile(self):
        rendered = render_28(COORDINATOR_INSTRUCTION, {"customer_profile": {"name": "Ana", "orders": 2}})
        self.assertIn("Ana", rendered)

    def test_only_optional_state_placeholders(self):
        # The profile is written by a tool after the first request, so every state placeholder must be optional.
        for match in PLACEHOLDER.finditer(COORDINATOR_INSTRUCTION):
            name = match.group().strip("{} ")
            if STATE_NAME.match(name.removesuffix("?")):
                self.assertTrue(name.endswith("?"), match.group())


# Labelled routing cases, reusable as a live evaluation set. The offline test below checks that the text
# the model reads carries the boundary; it cannot show which agent a model picks.
ROUTING_CASES = [
    ("I want my money back for order HO-10442", "refunds_agent"),
    ("Can I get a refund? I was charged twice", "refunds_agent"),
    ("Please cancel my order HO-10518", "refunds_agent"),
    ("What is the 4.50 line on my invoice?", "billing_agent"),
    ("Which card was charged for HO-10442?", "billing_agent"),
    ("Where is my parcel?", "orders_agent"),
]


class RoutingContractTests(unittest.TestCase):
    descriptions = {"billing_agent": BILLING_DESCRIPTION, "refunds_agent": REFUNDS_DESCRIPTION,
                    "orders_agent": ORDERS_DESCRIPTION}

    def test_descriptions_differentiate(self):
        for name, text in self.descriptions.items():
            self.assertGreaterEqual(len(text.split()), 8, name)
        tokens = {n: set(re.findall(r"[a-z]+", t.lower())) for n, t in self.descriptions.items()}
        for a in tokens:
            for b in tokens:
                if a < b:
                    overlap = len(tokens[a] & tokens[b]) / len(tokens[a] | tokens[b])
                    self.assertLess(overlap, 0.6, (a, b))

    def test_refund_words_point_at_refunds_agent(self):
        self.assertIn("refund", REFUNDS_DESCRIPTION.lower())
        self.assertIn("refunds_agent", BILLING_DESCRIPTION)  # billing names its boundary
        self.assertIn("refunds_agent", COORDINATOR_INSTRUCTION)

    def test_every_agent_has_a_routing_case(self):
        self.assertEqual({target for _, target in ROUTING_CASES}, set(self.descriptions))

    def test_coordinator_names_every_colleague(self):
        for name in self.descriptions:
            self.assertIn(name, COORDINATOR_INSTRUCTION)


if __name__ == "__main__":
    unittest.main()
