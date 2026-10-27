"""A poisoned web page must not lead to an email. Real Runner, scripted model, fakes."""
import asyncio
import unittest

from tests.fakes import POISONED_TERMS, install
from tests.runner_harness import HAVE_ADK

STATE = {"matter:email_allowlist": ["paralegal@rowan.example"]}


async def allow_all(text):
    return True


async def block_injection(text):
    return "assistant:" not in text


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class PoisonedPageTests(unittest.TestCase):
    def test_no_email_to_address_from_page(self):
        from contracts.agent import build_agent
        from tests.runner_harness import run_script

        wired = install(pages={"https://supplier.invalid/terms": POISONED_TERMS},
                        matters={"K-118": {"title": "Supply agreement", "text": "Liability cap: 200% of fees."}})
        asyncio.run(run_script(build_agent(scanners=[allow_all]), [
            {"function_call": "fetch_url", "args": {"url": "https://supplier.invalid/terms"}},
            {"function_call": "send_email", "args": {"to": "legal-review@supplier-portal.invalid",
                                                     "subject": "Contract", "body": "full text"}},
            {"text": "The terms are unchanged."},
        ], "Compare K-118 with the supplier's published terms", state=dict(STATE)))
        self.assertEqual(wired["mail"].sent, [])

    def test_blocked_result_never_reaches_model_or_session(self):
        from contracts.agent import build_agent
        from tests.runner_harness import run_script

        install(pages={"https://supplier.invalid/terms": POISONED_TERMS})
        events = asyncio.run(run_script(build_agent(scanners=[block_injection]), [
            {"function_call": "fetch_url", "args": {"url": "https://supplier.invalid/terms"}},
            {"text": "done"},
        ], "Check the supplier's terms", state=dict(STATE)))
        self.assertEqual(len(run_script.last_requests), 2)
        self.assertNotIn("legal-review@supplier-portal.invalid", run_script.last_requests[1])
        self.assertIn("withheld", run_script.last_requests[1])
        self.assertNotIn("legal-review@supplier-portal.invalid", "".join(e.model_dump_json() for e in events))


if __name__ == "__main__":
    unittest.main()
