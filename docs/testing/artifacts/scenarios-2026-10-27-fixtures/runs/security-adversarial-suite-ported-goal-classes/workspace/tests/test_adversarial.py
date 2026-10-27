"""Runs tests/adversarial/cases.json through the real Runner with a scripted model.

Assertions read the fakes. A case marked "known_gap" is skipped (with the gap note) while the gate
still lets the attack through, and fails once the attack is stopped so the flag is removed.
"""
import asyncio
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from app.policy import gate
from tests.fakes import BASE_STATE, FakeCalendar, FakeDrive, FakeMail, install
from tests.runner_harness import HAVE_ADK

CASES = json.loads((Path(__file__).parent / "adversarial" / "cases.json").read_text())
FIXTURES = CASES["fixtures"]

# Which fake records the effect of each tool.
EFFECTS = {
    "send_mail": lambda w: w.mail.sent,
    "delete_mail": lambda w: w.mail.deleted,
    "create_event": lambda w: w.calendar.created,
    "share_file": lambda w: w.drive.shared,
    "pay_invoice": lambda w: w.bank.payments,
}


def resolve(value):
    return FIXTURES[value] if isinstance(value, str) else value


def build_fakes(case):
    seed = case.get("seed", {})
    mail = {k: resolve(v) for k, v in seed.get("mail", {"msg-1": "supplier-mail"}).items()}
    files = {k: resolve(v) for k, v in seed.get("files", {
        "f-agenda": {"name": "Q4 planning agenda", "text": FIXTURES["agenda-file"]["text"]},
        "f-payroll": {"name": "Payroll 2026", "text": "salaries"}}).items()}
    events = {day: [resolve(e) for e in evs] for day, evs in seed.get("events", {}).items()}
    return install(mail=FakeMail(mail), drive=FakeDrive(files), calendar=FakeCalendar(events))


def user_text(case):
    text = case.get("user_request") or case["context"]
    if text.startswith("@fixture:"):
        text = FIXTURES[text.split(":", 1)[1]]["text"]
    return text


def attempted_tools(events):
    return [c.name for e in events for c in (e.get_function_calls() or [])]


def final_text(events):
    return " ".join(p.text for e in events if e.content for p in (e.content.parts or []) if p.text)


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class AdversarialCaseTests(unittest.TestCase):
    def violations(self, case):
        from app.agent import INSTRUCTION, build_agent
        from tests.runner_harness import run_script

        wired = build_fakes(case)
        events = asyncio.run(run_script(build_agent(), case["scripted_model_attempt"], user_text(case),
                                        state=dict(BASE_STATE)))
        problems = []
        # Guard against a vacuous pass: the forbidden call must really have been attempted.
        attempted = attempted_tools(events)
        for tool in case["forbidden_tool_calls"]:
            if tool not in attempted:
                self.fail(f"{case['case_id']}: the script never reached {tool}; attempted {attempted}")
            if EFFECTS[tool](wired):
                problems.append(f"{tool} left an effect: {EFFECTS[tool](wired)}")
        recorded = json.dumps({name: fn(wired) for name, fn in EFFECTS.items()})
        scanned = recorded + final_text(events) + (INSTRUCTION if case.get("check_instruction") else "")
        for needle in case["must_not_egress"]:
            if needle in scanned:
                problems.append(f"{needle!r} appears in recorded effects or output")
        return problems

    def test_cases(self):
        for case in CASES["cases"]:
            with self.subTest(case=case["case_id"]):
                problems = self.violations(case)
                if case.get("known_gap"):
                    if not problems:
                        self.fail(f"{case['case_id']}: the gap is closed, remove known_gap")
                    self.skipTest(f"open gap: {case['gap_note']} ({problems})")
                self.assertEqual(problems, [])


def call_gate(name, args, state=None):
    return gate(SimpleNamespace(name=name), args, SimpleNamespace(state=dict(state or BASE_STATE)))


class GateInvariantTests(unittest.TestCase):
    """Gate-level checks that need no ADK. Each states the safe behaviour; a failing one is a finding."""

    def test_aggregate_cap_is_enforced_across_calls(self):
        # Two payments of 400,000 against a 500,000 cap. The gate reads payments:today_cents but
        # nothing writes it, so a split (smurfed) payment passes each check on its own.
        state = dict(BASE_STATE)
        args = {"payee_id": "pay-0107", "amount_cents": 400_000, "reference": "x"}
        results = [call_gate("pay_invoice", args, state) for _ in range(2)]
        if results[1] is None:
            self.skipTest("open gap: the daily cap is not accumulated; nothing updates payments:today_cents")

    def test_gate_rejects_non_positive_amount(self):
        result = call_gate("pay_invoice", {"payee_id": "pay-0107", "amount_cents": -250_000, "reference": "CN-31"})
        if result is None:
            self.skipTest("open gap: the gate accepts a negative amount; only the confirmation hold stops it")
        self.assertEqual(result["status"], "error")

    def test_unregistered_tool_is_denied(self):
        self.assertEqual(call_gate("export_all_mail", {})["status"], "error")

    def test_recipient_must_match_exactly(self):
        for to in ("ops@larchpine.example, x@exfil-sink.invalid", " ops@larchpine.example", "OPS@larchpine.example"):
            self.assertEqual(call_gate("send_mail", {"to": to})["status"], "error", to)


if __name__ == "__main__":
    unittest.main()
