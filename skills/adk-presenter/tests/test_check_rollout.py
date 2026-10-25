"""Exercise the rollout pack check through its public CLI."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_rollout.py"

DESIGN = """| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | answers cite the claims system | user | claims | tool | refusal | G01/A1 |
| C2 | R2 | nothing sent without approval | user | approvals | gate | blocked | G02/A1 |
| C3 | R3 | refunds over 500 go to a lead | user | policy | gate | queued | G03/A1 |
"""

MESSAGE = ("From Monday your team can ask the claims assistant for the status of any open claim. "
           "It drafts, you check and send. Training is on Tuesday at ten.")

PACK = """# Rollout pack: Claims assistant

## 0. Assumptions and gaps

| Item | Assumption or gap | What depends on it | Who settles it |
| --- | --- | --- | --- |
| A1 | go-live on 2026-11-09 | dates | sponsor |

## 1. What it will and will not do

| Statement for users | Contract |
| --- | --- |
| Will: find the status of a claim from the claims system | {will_contract} |
| Won't: send anything to a customer; it drafts, you send | C2 |
{hands_over}

## 4. Training plan

| Session | Audience | Minutes | Objectives | Practice on | Trainer | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Managers | team leads, 6 | 60 | coach week one | real claims | ops lead | {training_date} |

## 5. Rollout messages

### Sponsor

Sender: COO · Date: 2026-11-02

{sponsor}

### Middle managers

Sender: Ops lead

{message}

### Frontline users

Sender: Team leads

{message}

## 6. AI disclosure

{status}
{text}

## 7. Adoption metrics

| Metric | Definition | Source | Target | Window |
| --- | --- | --- | --- | --- |
| Active user | {active} | analytics | 60% of assigned | {active_window} |
{counter}

## 8. Feedback channel

| User action | Record category | Route | Owner | Response |
| --- | --- | --- | --- | --- |
| Wrong or made-up answer | {category} | POST /feedback | {owner} | weekly |

## 9. Hypercare exit test

{agreed}

| Criterion | Threshold | Window | Source | Owner |
| --- | --- | --- | --- | --- |
| Severity 1 or 2 incidents open | 0 | 10 consecutive working days | incident log | ops lead |
| Weekly active rate | {threshold} | {window} | analytics | ops lead |
"""

GOOD = dict(will_contract="C1", hands_over="| Hands over: refunds over 500 go to a team lead | C3 |",
            training_date="2026-11-03", sponsor=MESSAGE, message=MESSAGE, status="Status: applies",
            text='Text: "You are chatting with an AI assistant. It can make mistakes."',
            active="distinct user_id with at least 1 completed invocation", active_window="7 days rolling",
            counter="| Counter-metric | reopened claims rate, at most 2 points over baseline | claims | flat | 4 weeks |",
            category="wrong_answer", owner="ops lead", threshold="≥ 60% of assigned", window="last 2 weeks",
            agreed="Agreed with the Head of Claims Operations on 2026-11-02.")


class CheckRolloutTest(unittest.TestCase):
    def run_check(self, design=False, **overrides):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pack.md").write_text(PACK.format(**dict(GOOD, **overrides)), encoding="utf-8")
            (root / "design.md").write_text(DESIGN, encoding="utf-8")
            args = [sys.executable, str(SCRIPT), "--pack", str(root / "pack.md"), "--json"]
            if design:
                args += ["--design", str(root / "design.md")]
            proc = subprocess.run(args, capture_output=True, text=True)
            data = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {"problems": [proc.stderr]}
            return proc.returncode, " | ".join(data["problems"] + data.get("notes", []))

    def test_complete_pack_passes(self):
        code, text = self.run_check(design=True)
        self.assertEqual(code, 0, text)

    def test_statement_without_contract_fails(self):
        code, text = self.run_check(will_contract="-")
        self.assertEqual(code, 1)
        self.assertIn("cites no contract", text)

    def test_unknown_contract_fails_with_design(self):
        code, text = self.run_check(design=True, will_contract="C9")
        self.assertIn("cites C9, which is not in the design", text)

    def test_missing_hands_over_fails(self):
        code, text = self.run_check(hands_over="")
        self.assertIn("no 'Hands over:' statement", text)

    def test_disclosure_needs_status_and_text(self):
        code, text = self.run_check(status="Status: maybe", text="Text: AI")
        self.assertIn("set 'Status: applies'", text)
        self.assertIn("exact quoted text", text)
        code, text = self.run_check(status="Status: not legally required: users in the US only")
        self.assertEqual(code, 0, text)

    def test_active_user_needs_window_and_counter_metric(self):
        code, text = self.run_check(active="anyone who logs in", active_window="", counter="")
        self.assertIn("'Active user' needs a threshold and a window", text)
        self.assertIn("name the counter-metric", text)

    def test_feedback_must_map_to_record_categories_with_owner(self):
        code, text = self.run_check(category="email us", owner="")
        self.assertIn("map user actions to the feedback record categories", text)
        self.assertIn("no owner", text)

    def test_exit_criterion_needs_number_and_window(self):
        code, text = self.run_check(threshold="high adoption", window="soon")
        self.assertIn("needs a number and a comparator", text)
        self.assertIn("needs a period", text)

    def test_placeholder_message_and_training_date_fail(self):
        code, text = self.run_check(sponsor="<message>", training_date="<YYYY-MM-DD>")
        self.assertIn("sponsor message is empty or still a placeholder", text)
        self.assertIn("placeholder '<YYYY-MM-DD>'", text)

    def test_exit_test_must_be_agreed_or_marked_proposed(self):
        code, text = self.run_check(agreed="We think these are fine.")
        self.assertIn("'Agreed with <name> on YYYY-MM-DD' or 'Status: proposed'", text)
        code, text = self.run_check(agreed="Status: proposed")
        self.assertEqual(code, 0, text)
        self.assertIn("proposed, not yet agreed", text)

    def test_placeholder_outside_tables_fails(self):
        code, text = self.run_check(agreed="Agreed with <sponsor> on <date>.")
        self.assertIn("placeholder '<sponsor>' left in the text", text)


if __name__ == "__main__":
    unittest.main()
