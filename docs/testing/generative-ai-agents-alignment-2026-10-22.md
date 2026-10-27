# GoogleCloudPlatform/generative-ai `agents/` alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/generative-ai-agents-comparison-2026-10-22.md).
In the repository:

- **Facts** from the four ADK blueprints at commit `3a716a8` and two Google
  product pages read the same day, cited and labelled a vendor sample:
  Semantic Governance Policies as a Preview screening layer with the
  vendor's accuracy caveat and the eight-refund aggregate exploit in the
  security skill's agency reference; the aggregate bound keyed on the
  business object in the guardrails skill's token-budgets reference; the
  signed-write pattern in the safe-API skill's writes reference; the
  deterministic policy peer and the legacy card path in the interoperability
  skill's topology reference and the designer's handoff row; the
  rubric-plus-code metric pair and the `judge_model` omission in the
  evaluation skill's live-evaluations reference; the model-migration
  notebook pointer in the release skill.
- **No routing line**: the blueprints are samples.
- **One scenario case** (`security-refund-agent-build-time-controls-vs-screening`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the [testing log](index.md) entry for this date. After the trial, one helper
changed: the guardrails inspector now accepts a PEP 508 extras marker on
the `google-adk` pin, with a test, and the package's `last-tested` moved to
this date after its tests were re-run.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK installed, on a synthetic project, without the expected answers.

### Guardrails and security: hardening a refund path after two incidents

The project: an ADK 2.12 refund agent whose incident write-up showed eight
compliant refunds exceeding one order's total and a software line item
refunded without a human. The request: no session may exceed an order's
total across any number of calls, no software refund without a human, a
ledger that detects a tampered or fabricated row, offline tests only, and a
statement of what a managed policy layer adds and must not be trusted for.

What the agent did: an HMAC-signed, hash-chained ledger whose audit catches
edited amounts, fabricated and copied rows, deletions and reordering, with
the order-keyed aggregate enforced inside the append lock; an SDK-free
policy core and gate module; `require_confirmation` as a fail-closed
callable plus a `before_tool_callback`; approval read only from the tool
context; 45 deterministic tests run on the pin-meeting interpreter and 4
scripted-model Runner tests reported as not run; a notes file separating
proven, planned and the managed layer's limits, naming the Preview policy
product's self-declared inaccuracy.

Ease rating: **3 of 5**. The guidance named this exact incident and its
fix; the cost was reading twenty files to extract fifteen operative rules.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The guardrails inspector rejected `google-adk[gcp]>=2.12.0,<3` as an invalid constraint | The dependency pattern now accepts an extras marker; a test covers it; tests re-run |
| The signed-ledger pattern was reachable only through a parenthetical; the router's row for `safe-api-tool-calls` did not mention integrity | The routing row now names tamper-evident writes and a ledger that detects an edited row |
| Two skills described the `require_confirmation` callable without its calling convention; the order of `before_tool_callback` against the confirmation hold was left to inference | Both passages now state the 2.12.0 convention (validated arguments as keywords, `tool_context` by name, sync or async) and the order (plugin callback, agent callbacks, then `run_async` evaluating the confirmation; the confirmed resume re-dispatches through the same path) with the source file |
| The business-effect aggregate lived under a mode row about usage | A new mode row routes "a business effect must accumulate across calls" to the same reference |
| No guidance on a signing key for a development, in-memory store | One sentence in the human-review reference |
| The security inspector counted test-file agents in the after-inventory | The validation reference says so and what to compare |
| "Never imitate the SDK" read as forbidding duck-typed inputs to one's own callbacks | The engineer rule now scopes itself to the Runner, flow and confirmation protocol |
| The guardrails boundary fixture hard-fails on anything but 2.8.0; the engineer's apply section is long | Left as they are and recorded: the fixture is the 2.8.0 contract by design, and the apply section's ordering is a Phase D question |

## What this does not establish

The trial's Runner tests and the live policy layer did not run. The
blueprints were read, not run; their demos simulate the cloud services.
