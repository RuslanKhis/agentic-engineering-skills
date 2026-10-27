# Research agent

Answers market and competitor research questions for the sales team. The root
agent delegates to two specialists that each answer in a single turn and can
open a procurement request for a paid report when the user agrees.

Planned hosting: Cloud Run (europe-west1), private ingress. Gemini Enterprise
users in the same project should be able to invoke it.

Tests: `python -m unittest discover -s tests -t .`. google-adk and a2a-sdk are
not installed in this environment.
