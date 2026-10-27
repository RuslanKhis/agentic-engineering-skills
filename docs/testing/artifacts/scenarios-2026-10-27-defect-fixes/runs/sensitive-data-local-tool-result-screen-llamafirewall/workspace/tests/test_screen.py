"""Local result screen and alignment gate: no ADK, no model, no network."""
import asyncio
import logging
import unittest
from types import SimpleNamespace

from contracts import alignment, screen
from contracts.screen import WITHHELD, ResultScreen, windows
from tests.fakes import FakeScanner, WordTokenizer

TOK = WordTokenizer()
TRIGGER = FakeScanner.TRIGGER
FILLER = "clause " * 1000


def make(scanner=None, **kw):
    return ResultScreen(scanner or FakeScanner(), TOK, **kw)


def allows(sc, result):
    return asyncio.run(sc.allows(result, tool_name="fetch_url"))


class WindowTests(unittest.TestCase):
    def test_windows_stay_under_limit_and_cover_text(self):
        text = " ".join(f"w{i}" for i in range(1000))
        ws = windows(text, TOK, size=100, overlap=30)
        self.assertTrue(all(len(w.split()) <= 100 for w in ws))
        self.assertEqual(" ".join(ws).count("w999"), 1)

    def test_empty_text_has_no_windows(self):
        self.assertEqual(windows("", TOK), [])


class ScreenTests(unittest.TestCase):
    def test_clean_result_allowed(self):
        self.assertTrue(allows(make(), {"status": "ok", "text": "Liability cap: 200% of fees."}))

    def test_injection_blocked(self):
        self.assertFalse(allows(make(), {"status": "ok", "text": f"Terms. {TRIGGER} and email it"}))

    def test_injection_after_token_512_blocked(self):
        self.assertFalse(allows(make(), {"text": FILLER + TRIGGER}))

    def test_injection_across_window_boundary_blocked(self):
        # place the phrase so it straddles the end of the first 384-word window
        text = ("clause " * 382) + TRIGGER + (" clause" * 600)
        scanner = FakeScanner()
        self.assertFalse(allows(make(scanner), {"text": text}))
        self.assertTrue(all(len(s.split()) <= 384 for s in scanner.seen))

    def test_injection_in_nested_value_or_key_blocked(self):
        self.assertFalse(allows(make(), {"a": [{"b": TRIGGER}]}))
        self.assertFalse(allows(make(), {TRIGGER: "x"}))

    def test_human_review_hold_withholds(self):
        sc = make(FakeScanner(decision_on_trigger="human_in_the_loop_required"))
        self.assertFalse(allows(sc, {"text": TRIGGER}))

    def test_error_status_withholds(self):
        self.assertFalse(allows(make(FakeScanner("error")), {"text": "harmless"}))

    def test_exception_withholds(self):
        self.assertFalse(allows(make(FakeScanner("raise")), {"text": "harmless"}))

    def test_oversize_and_deep_results_withhold(self):
        self.assertFalse(allows(make(), {"text": "x" * (screen.MAX_CHARS + 1)}))
        deep = {}
        node = deep
        for _ in range(screen.MAX_DEPTH + 2):
            node["n"] = {}
            node = node["n"]
        self.assertFalse(allows(make(), deep))

    def test_logs_carry_no_scanned_text(self):
        secret = "SECRET-CLAUSE-TEXT"
        with self.assertLogs("contracts.screen", level="INFO") as logs:
            allows(make(FakeScanner("raise")), {"text": secret})
            allows(make(), {"text": f"{secret} {TRIGGER}"})
        self.assertNotIn(secret, "\n".join(logs.output))


class CallbackTests(unittest.TestCase):
    def tearDown(self):
        screen.configure_screen(None)

    def run_cb(self, response):
        tool = SimpleNamespace(name="fetch_url")
        return asyncio.run(screen.screen_tool_result(tool, {}, None, response))

    def test_unconfigured_withholds(self):
        self.assertEqual(self.run_cb({"status": "ok", "text": "fine"}), WITHHELD)

    def test_configured_passes_clean_and_replaces_blocked(self):
        screen.configure_screen(make())
        self.assertIsNone(self.run_cb({"status": "ok", "text": "fine"}))
        self.assertEqual(self.run_cb({"status": "ok", "text": TRIGGER}), WITHHELD)


class AlignmentTests(unittest.TestCase):
    def tearDown(self):
        alignment.configure_judge(None)

    def call(self, tool_name="send_email", goal="Email the summary to me", args=None):
        ctx = SimpleNamespace(user_content=SimpleNamespace(parts=[SimpleNamespace(text=goal)]))
        return asyncio.run(alignment.alignment_gate(SimpleNamespace(name=tool_name), args or {"to": "a"}, ctx))

    def test_judge_sees_goal_and_call_only(self):
        seen = []

        async def judge(goal, tool, args):
            seen.append((goal, tool, args))
            return True

        alignment.configure_judge(judge)
        self.assertIsNone(self.call())
        self.assertEqual(seen, [("Email the summary to me", "send_email", {"to": "a"})])

    def test_refusal_error_timeout_and_missing_goal_refuse(self):
        async def no(goal, tool, args):
            return False

        async def boom(goal, tool, args):
            raise RuntimeError("down")

        async def slow(goal, tool, args):
            await asyncio.sleep(5)
            return True

        for judge, timeout in ((no, 1), (boom, 1), (slow, 0.01)):
            alignment.configure_judge(judge, timeout_s=timeout)
            self.assertEqual(self.call(), alignment.REFUSED)
        alignment.configure_judge(no)
        self.assertEqual(self.call(goal=""), alignment.REFUSED)

    def test_ungated_tool_and_unconfigured_judge_pass(self):
        self.assertIsNone(self.call())
        async def no(goal, tool, args):
            return False
        alignment.configure_judge(no)
        self.assertIsNone(self.call(tool_name="read_contract"))


if __name__ == "__main__":
    logging.disable(logging.NOTSET)
    unittest.main()
