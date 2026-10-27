"""Screening and alignment gate, no google-adk needed."""
import asyncio
import unittest
from types import SimpleNamespace

from contracts import screening
from contracts.screening import alignment_gate, llamafirewall_alignment_judge, tool_result_screen
from tests.fakes import POISONED_TERMS

TOOL = SimpleNamespace(name="fetch_url")
OK = {"status": "ok", "url": "https://s.invalid", "text": "Liability is capped."}


def run(coro):
    return asyncio.run(coro)


async def allow(text):
    return True


async def deny(text):
    return False


async def boom(text):
    raise RuntimeError("scanner down with " + text[:10])


async def hang(text):
    await asyncio.sleep(60)


class ToolResultScreenTests(unittest.TestCase):
    def after(self, scanner, response):
        return run(tool_result_screen([scanner])(TOOL, {}, None, response))

    def test_allowed_result_is_left_alone(self):
        self.assertIsNone(self.after(allow, OK))

    def test_denied_result_is_replaced_without_its_content(self):
        out = self.after(deny, {"status": "ok", "text": POISONED_TERMS})
        self.assertEqual(out["status"], "blocked")
        self.assertNotIn("supplier-portal", str(out))

    def test_scanner_error_fails_closed(self):
        self.assertEqual(self.after(boom, OK)["status"], "blocked")

    def test_scanner_timeout_fails_closed(self):
        old, screening.SCAN_TIMEOUT_S = screening.SCAN_TIMEOUT_S, 0.05
        try:
            self.assertEqual(self.after(hang, OK)["status"], "blocked")
        finally:
            screening.SCAN_TIMEOUT_S = old

    def test_non_true_verdict_is_not_an_allow(self):
        async def maybe(text):
            return "allow"
        self.assertEqual(self.after(maybe, OK)["status"], "blocked")

    def test_every_string_field_is_screened_including_keys_and_nesting(self):
        seen = []

        async def spy(text):
            seen.append(text)
            return True
        self.after(spy, {"status": "ok", "nested": [{"k": "deep-value"}], "evil-key": 1})
        self.assertIn("deep-value", seen[0])
        self.assertIn("evil-key", seen[0])

    def test_unknown_types_and_oversize_are_blocked(self):
        self.assertEqual(self.after(allow, {"x": object()})["status"], "blocked")
        self.assertEqual(self.after(allow, {"text": "a" * (screening.MAX_SCREENED_CHARS + 1)})["status"], "blocked")

    def test_no_scanners_refused_at_build(self):
        with self.assertRaises(ValueError):
            tool_result_screen([])


def ctx(first="Compare K-118 with the terms", events=True):
    user = SimpleNamespace(author="user", content=SimpleNamespace(parts=[
        SimpleNamespace(text=first, function_call=None, function_response=None)]))
    resp = SimpleNamespace(author="contract_assistant", content=SimpleNamespace(parts=[SimpleNamespace(
        text=None, function_call=None, function_response=SimpleNamespace(response={"text": "terms"}))]))
    return SimpleNamespace(session=SimpleNamespace(events=[user, resp] if events else [resp]))


class AlignmentGateTests(unittest.TestCase):
    def before(self, judge, name="send_email", context=None):
        return run(alignment_gate(judge)(SimpleNamespace(name=name), {"to": "a@b.example"}, context or ctx()))

    def test_aligned_call_passes_and_judge_sees_goal_and_proposal(self):
        traces = []

        async def judge(trace):
            traces.append(trace)
            return True
        self.assertIsNone(self.before(judge))
        self.assertEqual(traces[0][0], {"role": "user", "content": "Compare K-118 with the terms"})
        self.assertIn("send_email", traces[0][-1]["content"])

    def test_misaligned_error_and_non_true_verdicts_block(self):
        async def no(trace):
            return False

        async def err(trace):
            raise RuntimeError("endpoint down")

        async def hitl(trace):
            return "HUMAN_IN_THE_LOOP_REQUIRED"
        for judge in (no, err, hitl):
            self.assertEqual(self.before(judge)["status"], "error")

    def test_missing_user_message_blocks(self):
        async def yes(trace):
            return True
        self.assertEqual(self.before(yes, context=ctx(events=False))["status"], "error")

    def test_unguarded_tool_skips_judge(self):
        async def never(trace):
            raise AssertionError("judge called")
        self.assertIsNone(self.before(never, name="read_contract"))


class AlignmentEndpointTests(unittest.TestCase):
    def test_third_party_and_plain_http_endpoints_refused(self):
        for url in ("https://api.together.xyz/v1", "http://europe-west3-aiplatform.googleapis.com/v1"):
            with self.assertRaises(ValueError):
                llamafirewall_alignment_judge(url, "m", "K")

    def test_in_project_endpoint_is_still_unwired(self):
        with self.assertRaises(NotImplementedError):
            llamafirewall_alignment_judge("https://europe-west3-aiplatform.googleapis.com/v1", "m", "K")


if __name__ == "__main__":
    unittest.main()
