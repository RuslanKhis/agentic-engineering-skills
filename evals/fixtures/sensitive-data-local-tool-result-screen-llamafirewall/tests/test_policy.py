import unittest
from types import SimpleNamespace

from contracts.policy import tool_policy


def ctx(**state):
    return SimpleNamespace(state=state)


class PolicyTests(unittest.TestCase):
    def test_email_outside_allowlist_refused(self):
        result = tool_policy(SimpleNamespace(name="send_email"), {"to": "x@else.invalid"},
                             ctx(**{"matter:email_allowlist": ["pl@rowan.example"]}))
        self.assertEqual(result["status"], "error")

    def test_email_on_allowlist_passes(self):
        self.assertIsNone(tool_policy(SimpleNamespace(name="send_email"), {"to": "pl@rowan.example"},
                                      ctx(**{"matter:email_allowlist": ["pl@rowan.example"]})))

    def test_plain_http_refused(self):
        result = tool_policy(SimpleNamespace(name="fetch_url"), {"url": "http://terms.example"}, ctx())
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
