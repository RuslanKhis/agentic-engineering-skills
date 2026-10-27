# Research assistant

Internal research assistant for the strategy team. The root agent plans a
research turn and calls two specialist agents as tools: a literature scout and
a numbers analyst. Models are served through LiteLLM from our OpenAI-compatible
gateway (`o-reasoner-2` for the root and analyst, `o-mini-2` for the scout).

Cost reporting: `research/cost.py` reads saved ADK sessions (exported nightly
from the session database to `sessions/`) and prices the token usage with
`prices.json`. The Looker dashboard runs the same arithmetic over the same
exports. Finance compares it with the gateway invoice each month
(`billing/`).

Tests: `python -m unittest discover -s tests -t .` (no SDK needed).
google-adk, litellm and the gateway are not reachable from this environment.
