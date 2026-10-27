# Travel agent

An ADK 2.12.0 agent that books flights for staff travel: it searches the flight API, books the
chosen flight (with an idempotency key, so a retried booking is not charged twice) and sends the
confirmation email.

- `travel_agent/agent.py` builds the agent; `travel_agent/tools.py` holds the three tools;
  `travel_agent/flight_api.py` is the flight API client with an injectable transport.
- `tests/test_tools.py` tests the tools against `tests/flight_double.py` (offline).
- `tests/test_resilience.py` is a scripted-model Runner test using ADK's Environment Simulation
  to inject a 503 on search. Runner tests skip when google-adk is not installed (it is not
  installed in this environment).
- Live Gemini runs need the product owner's approval.

`python -m unittest discover -s tests -t .`
