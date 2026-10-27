# instructions-routing-and-templating-repair: what the fixture holds

Bases: support-assistant; overlay pins `google-adk==2.8.0` and turns the agent
into a chat-mode coordinator (`app/agent.py`) with three sub-agents whose
descriptions are "Billing", "Refunds" and "Order help" (one or two words, A1).

`app/prompts.py` COORDINATOR_INSTRUCTION:

- names the three colleagues but gives no conditions for delegation; billing's
  own instruction talks about "charges on the customer's card", so "I was charged
  twice, I want my money back" plausibly routes to billing (the misroute).
- contains `Customer profile: {customer_profile}` — a state key written only by the
  `load_profile` tool (`app/tools/profile.py`), so the first turn of a session,
  before the tool has run, raises `KeyError('Context variable not found: ...')`.
- contains a JSON hand-over example
  `{"route": "orders_agent", "order": {order_id}, "summary": ...}`: the inner
  `{order_id}` is identifier-shaped, so 2.8.0 templating looks it up in state and
  raises KeyError (the outer braces contain quotes and are left alone).

A2 expects the agent to explain 2.8.0's templating (identifier-like braces are
state variables; `\{` and `${` escapes only exist from 2.10.0) and fix it with
an InstructionProvider or optional placeholders (`{customer_profile?}`), not an
escape. A3: a render test against fixture state with no unresolved placeholders
(needs the SDK's templating to be exact; a test that renders through the SDK
should be reported as not run without it) and a scripted-model transfer check
(not run without the SDK). A4: hands routing-accuracy measurement to
adk-agent-evaluation and separates rendered, mocked and not-run evidence.

The stdlib suite passes offline. Context unchanged from scenarios.json.
