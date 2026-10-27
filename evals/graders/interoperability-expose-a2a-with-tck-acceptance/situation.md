# Situation: interoperability-expose-a2a-with-tck-acceptance

Standalone project: one root agent (`triage/agent.py`), a2a-sdk >=1.0,<2 pinned, no card yet,
partner request with client-credentials tokens. A1 (card with securitySchemes and protocolVersion,
agent_card_check.py, manual checks), A2 (scoped TCK against local to_a2a as planned verification),
A3 (TCK sends no auth header; AUTH-SERVER-002 by own test), A4 (pins kept, origin pinning,
registration separate) graded from the answer and files. No shell: helper and TCK cannot run.
Context unchanged.
