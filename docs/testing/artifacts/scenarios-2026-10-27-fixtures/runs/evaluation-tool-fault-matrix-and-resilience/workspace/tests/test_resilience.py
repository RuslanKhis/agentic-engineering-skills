"""The flight API is flaky: a 503 on search must not turn into a made-up booking."""
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
from tests.flight_double import FlightDouble, MailerDouble
from tests.scripted_model import ScriptedModel, call, text, user


class ResilienceTests(unittest.TestCase):
    def test_search_503_is_reported_honestly(self):
        double = FlightDouble()
        tools.api = FlightApi(double)
        tools.mailer = MailerDouble()
        # tool_name must match the tool exactly ("search_flights"); a misspelt name configures nothing,
        # the engine then lets the real tool run, and the test passed without any fault being injected.
        config = EnvironmentSimulationConfig(tool_simulation_configs=[ToolSimulationConfig(
            tool_name="search_flights",
            injection_configs=[InjectionConfig(injection_probability=1.0, random_seed=7,
                                               injected_error=InjectedError(error_code=503,
                                                                            error_message="Service Unavailable"))])])
        agent = build_agent(before_tool_callback=EnvironmentSimulationFactory.create_callback(config))
        agent.model = ScriptedModel(script=[
            call("search_flights", origin="LHR", destination="CDG", date="2026-11-03"),
            text("The flight search is unavailable right now, please try again later."),
        ])
        runner = InMemoryRunner(agent=agent, app_name="travel-resilience")

        async def go():
            s = await runner.session_service.create_session(app_name="travel-resilience", user_id="emp-101")
            final, responses = "", []
            async for event in runner.run_async(user_id="emp-101", session_id=s.id,
                                                new_message=user("Book me LHR to CDG on 3 November")):
                responses += [dict(r.response or {}) for r in event.get_function_responses()]
                if event.is_final_response() and event.content and event.content.parts:
                    final = event.content.parts[0].text or ""
            return final, responses

        final, responses = asyncio.run(go())
        self.assertEqual(responses[0].get("error_code"), 503, "the injected fault did not fire")
        self.assertEqual(double.calls, [], "the real backend was reached despite the injection")
        self.assertIn("try again", final)
        self.assertEqual(double.bookings, {})


if __name__ == "__main__":
    unittest.main()
