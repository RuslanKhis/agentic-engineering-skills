"""Runs tests/adversarial/cases.json through the real Runner with a scripted model."""
import asyncio
import json
from pathlib import Path
import unittest

from tests.fakes import BASE_STATE, FakeDrive, FakeMail, install
from tests.runner_harness import HAVE_ADK

CASES = json.loads((Path(__file__).parent / "adversarial" / "cases.json").read_text())


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class AdversarialCaseTests(unittest.TestCase):
    def run_case(self, case):
        from app.agent import build_agent
        from tests.runner_harness import run_script

        fixtures = CASES["fixtures"]
        mail = FakeMail({"msg-1": fixtures["supplier-mail"]})
        drive = FakeDrive({"f-agenda": {"name": "Q4 planning agenda", "text": fixtures["agenda-file"]["text"]},
                           "f-payroll": {"name": "Payroll 2026", "text": "salaries"}})
        wired = install(mail=mail, drive=drive)
        asyncio.run(run_script(build_agent(), case["scripted_model_attempt"], case["context"],
                               state=dict(BASE_STATE)))
        return wired

    def test_cases(self):
        for case in CASES["cases"]:
            with self.subTest(case=case["case_id"]):
                wired = self.run_case(case)
                recorded = json.dumps({"sent": wired.mail.sent, "shared": wired.drive.shared,
                                       "paid": wired.bank.payments, "events": wired.calendar.created})
                for needle in case["must_not_egress"]:
                    self.assertNotIn(needle, recorded)


if __name__ == "__main__":
    unittest.main()
