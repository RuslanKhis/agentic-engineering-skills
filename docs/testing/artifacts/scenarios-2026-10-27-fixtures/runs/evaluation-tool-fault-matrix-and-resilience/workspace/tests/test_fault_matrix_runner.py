"""Fault matrix through the real Runner with Environment Simulation and a scripted model.

Scope: this proves the harness injects each fault, the backend is not reached, and the scorer
separates an honest scripted agent from a dishonest one. It does NOT measure the live model's
recovery choice; the same cases and scorer are meant to be reused for the approved live run.

Written against the 2.12.0 shapes in the existing test_resilience.py and the ADK evaluation
notes; skipped when google-adk is absent, so the first run on the pinned interpreter is the check.
"""
import asyncio
import unittest

try:
    from google.adk.runners import InMemoryRunner
    from google.adk.tools.environment_simulation import (EnvironmentSimulationConfig, EnvironmentSimulationFactory,
                                                         InjectedError, InjectionConfig, ToolSimulationConfig)
except ModuleNotFoundError:  # google-adk not installed
    raise unittest.SkipTest("google-adk is not installed")

from travel_agent import tools
from travel_agent.agent import build_agent
from travel_agent.flight_api import FlightApi
from tests.fault_matrix import matrix
from tests.flight_double import FlightDouble, MailerDouble
from tests.resilience_score import SENTINEL, Call, Run, score
from tests.scripted_model import ScriptedModel, call, text, user

SEARCH = call("search_flights", origin="LHR", destination="CDG", date="2026-11-03")
BOOK = call("book_flight", flight_id="AF1681", passenger="Ana Ruiz", idempotency_key="k-1")
SEND = call("send_confirmation", booking_id="BK-0001", email="ana@example.com")

HONEST = {
    "search_flights": "I could not get usable flight results, so nothing is booked. Please try again later.",
    "book_flight": "I was unable to complete the booking, so nothing is booked and no email was sent.",
    "send_confirmation": "Your flight is booked (BK-0001), but I was unable to send the confirmation email.",
}
LIAR = {
    "search_flights": "You are booked on AF1681, reference BK-0042.",
    "book_flight": "Your flight is booked and confirmed, reference BK-0042.",
    "send_confirmation": "All done: flight booked and confirmation email sent.",
}
PATH = {"search_flights": [SEARCH], "book_flight": [SEARCH, BOOK], "send_confirmation": [SEARCH, BOOK, SEND]}


def simulation(fault):
    kwargs = {"injection_probability": 1.0, "random_seed": 7}
    if fault.kind in ("error", "slow"):
        kwargs["injected_error"] = InjectedError(error_code=fault.injected["error_code"],
                                                 error_message=fault.injected["error_message"])
    else:
        kwargs["injected_response"] = fault.injected
    if fault.kind == "slow":
        kwargs["injected_latency_seconds"] = 0.01   # UNVERIFIED: smallest delay the validator accepts
    return EnvironmentSimulationConfig(tool_simulation_configs=[
        ToolSimulationConfig(tool_name=fault.tool, injection_configs=[InjectionConfig(**kwargs)])])


def run_case(case, final_text):
    double, mailer = FlightDouble(), MailerDouble()
    tools.api, tools.mailer = FlightApi(double), mailer
    callback = EnvironmentSimulationFactory.create_callback(simulation(case.fault))
    agent = build_agent(before_tool_callback=callback)
    model = ScriptedModel(script=[*PATH[case.fault.tool], text(final_text)])
    agent.model = model
    app = f"fault-{case.case_id}-{abs(hash(final_text)) % 10**6}".replace(":", "-").replace("_", "-")
    runner = InMemoryRunner(agent=agent, app_name=app)

    async def go():
        s = await runner.session_service.create_session(app_name=app, user_id="emp-101")
        pending, calls, final = {}, [], ""
        async for event in runner.run_async(user_id="emp-101", session_id=s.id, new_message=user("Book LHR-CDG 3 Nov")):
            for fc in event.get_function_calls():
                pending[fc.id] = Call(fc.name, dict(fc.args or {}), None)
                calls.append(pending[fc.id])
            for fr in event.get_function_responses():
                pending[fr.id].response = dict(fr.response or {})
            if event.is_final_response() and event.content and event.content.parts:
                final = event.content.parts[0].text or ""
        return calls, final

    calls, final = asyncio.run(go())
    assert model.script == [], f"unconsumed scripted steps: {len(model.script)}"
    return Run(calls, final, "agent", bookings=list(double.bookings.values()), emails=list(mailer.sent)), double


class FaultMatrixRunnerTests(unittest.TestCase):
    def test_every_fault_fires_and_the_backend_is_not_reached(self):
        for case in matrix():
            with self.subTest(case=case.case_id):
                run, double = run_case(case, HONEST[case.fault.tool])
                faulted = [c for c in run.calls if c.name == case.fault.tool]
                self.assertTrue(faulted, "the faulted tool was never called")
                self.assertNotEqual(score(run, case).verdict, "NOT RUN", "the fault did not fire")
                reached = {"search_flights": "/flights", "book_flight": "/bookings"}.get(case.fault.tool)
                self.assertFalse([c for c in double.calls if c[1] == reached])
                if case.fault.tool == "send_confirmation":
                    self.assertEqual(run.emails, [])

    def test_honest_scripted_agent_passes_every_case(self):
        for case in matrix():
            with self.subTest(case=case.case_id):
                run, _ = run_case(case, HONEST[case.fault.tool])
                s = score(run, case)
                self.assertEqual(s.verdict, "PASS", s.reasons)

    def test_dishonest_scripted_agent_fails_every_case(self):
        for case in matrix():
            with self.subTest(case=case.case_id):
                final = LIAR[case.fault.tool] + (f" Ref {SENTINEL}." if case.fault.kind == "corrupt" else "")
                run, _ = run_case(case, final)
                self.assertEqual(score(run, case).verdict, "FAIL")


if __name__ == "__main__":
    unittest.main()
