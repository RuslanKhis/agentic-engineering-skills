# REPORT — T-201 "Demo: cancel an order from chat"

Specialist: **safe-api-tool-calls**. The ticket adds a state-changing call to an external API (POST `/orders/{id}/cancel`). The main risks are hidden retries, duplicate writes and outcomes the agent can't confirm. The ticket names no `Primary skill`. No supporting skill was loaded; the controls that belong to other specialists are listed as deferred.

## 1. Skills invoked and reference files opened (in order)

1. Skill `adk-engineer` (`.claude/skills/adk-engineer/SKILL.md`, loaded by the slash command)
2. `.claude/skills/safe-api-tool-calls/SKILL.md`
3. `.claude/skills/safe-api-tool-calls/references/writes-and-confirmation.md`
4. `.claude/skills/safe-api-tool-calls/references/compatibility.md`
5. Ran `.claude/skills/safe-api-tool-calls/scripts/inspect_project.py --project . --dry-run` with python3.11. Result: no signals, no issues, `partial: false`.
6. `.claude/skills/safe-api-tool-calls/references/validation.md`
7. `.claude/skills/safe-api-tool-calls/references/adk-verification.md`

Not opened: `reads-and-deadlines.md`, `adk-operations.md`, `inspection.md`, `composition.md` (no `agents-cli-manifest.yaml`).

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
|---|---|---|
| 1 | Does the staging cancel endpoint support idempotency keys or replay, and is there a status lookup? | Unknown. So the tool makes one attempt, with no retries and no invented `Idempotency-Key`. An ambiguous result is reported as `unknown`. |
| 2 | Which status codes does the endpoint return (already cancelled, not found, shipped)? | 2xx means cancelled. 404 means not found. 409 or 422 means not cancellable. Other 4xx means refused. 5xx, timeouts and transport errors mean unknown. |
| 3 | Does the staging API need authentication? | No. The existing order tools send no credentials, so none were added and no secrets are in code. |
| 4 | Should the production orders API (`ORDERS_API`) also point at staging for the demo? | No. Cancellation uses a separate `CANCEL_ORDERS_API`, which defaults to staging and can be overridden by env. Production lookups are unchanged. |
| 5 | Must the customer approve before the cancel is sent, even with fake orders? | Yes. ADK `require_confirmation=True` costs little, makes the demo more convincing, and is needed for production anyway. |
| 6 | Which agent gets the tool? | `root_agent`, which already holds the order lookup tools. No new sub-agent was added. |
| 7 | How does the demo run: `adk web`, Cloud Run or an owned Runner? This decides where a spend stop can be enforced. | Undecided. No spend stop was built in code; see deferred controls. |
| 8 | Is it OK to change `support_agent/__init__.py` to a lazy `root_agent` import? | Yes. `from support_agent import root_agent` still works through module `__getattr__`. The change lets tool tests run without ADK, as adk-engineer SKILL.md:135 recommends. |
| 9 | Should the model move off `gemini-2.5-pro` first (T-103)? | No. It retires on 20 October, after the demo on Tuesday 13 October. That migration belongs to T-103. |

## 3. Files written or changed; what is not finished

- `support_agent/tools.py`: added `CANCEL_ORDERS_API`, order-ID validation, `_orders_client()` (httpx `retries=0`), `cancel_order()` and `_unknown()`.
- `support_agent/agent.py`: added `cancel_order_tool = FunctionTool(tools.cancel_order, require_confirmation=True)`, put it on `root_agent.tools`, and added one instruction sentence (call once; don't call again after `unknown`).
- `support_agent/__init__.py`: `root_agent` is now imported lazily.
- `tests/test_cancel_order.py` (new): 18 offline tests.
- `tests/test_agent_wiring.py` (new): checks the confirmation wiring. Needs google-adk.
- `tickets/T-201.md`: added an Evidence section.
- `REPORT.md`: this file.

Not finished:
- The ADK confirmation path is not exercised. Missing or rejected approval should send zero POSTs; that needs the HTTP/session test described in `adk-verification.md`.
- No live demo rehearsal against staging.
- No spend stop.
- Production controls deferred: a durable operation record with an idempotency key, reconciliation of `unknown`, an authenticated caller and ownership check, and a re-check of order state between approval and dispatch.
- `test_agent_wiring.py` reads the private attribute `_require_confirmation`. That attribute name in ADK 2.8.0 is unverified.

## 4. Checks run and not run

Run:
- `python3.11 .claude/skills/safe-api-tool-calls/scripts/inspect_project.py --project . --dry-run`: no signals or issues.
- `python3 -m pytest -q -p no:cacheprovider tests/` (Python 3.9.13, httpx 0.28.1, pytest 7.1.2): **19 passed, 1 skipped**. These are offline simulated results: the provider is replaced by `httpx.MockTransport` and real socket connections are blocked. The tests cover:
  - a successful single POST to the correct path;
  - invalid IDs make zero calls;
  - 404, 409 and 403 return `error` after one attempt;
  - a commit followed by a lost response returns `unknown`, with one attempt and one effect;
  - 5xx returns `unknown` after one attempt;
  - a connect error returns `error`;
  - the real client has transport retries set to 0;
  - the cancel URL defaults to staging, not production.
- The existing `tests/test_tools.py` now passes without ADK. Before, it could not import without ADK.
- `python3.11` AST parse of all changed `.py` files: ok.

Not run:
- `tests/test_agent_wiring.py`: skipped because google-adk is not installed.
- The ADK HTTP/SSE confirmation test: not written.
- The live model with `adk web`.
- The staging orders API: no network allowed.
- The suite on Python ≥3.11, the project's declared version: 3.11 has no httpx or pytest here, and installing is not allowed.

## 5. Friction log

- **Helpful:** `.claude/skills/adk-engineer/SKILL.md:120`. The line "infer them from the request ("demo next Tuesday", "3 hours")" fits this ticket almost exactly. The floor at `:123` (no secrets, spend stop, pinned model, a human before irreversible effects) and the deferred-controls instruction at `:125` gave a clear stopping point.
- **Helpful:** `.claude/skills/safe-api-tool-calls/references/writes-and-confirmation.md:7`. "Unknown write semantics mean no automatic retries, including hidden SDK retries" settled the main design choice. It also prompted setting httpx `retries=0` explicitly.
- **Helpful:** `.claude/skills/safe-api-tool-calls/references/compatibility.md:65`. It confirms that `FunctionTool(..., require_confirmation=True)` was observed on ADK 2.8.0, the project's pin, so I didn't need to guess the API.
- **Unsure:** `.claude/skills/adk-engineer/SKILL.md:123` lists "a spend stop" as part of the floor. But `.claude/skills/safe-api-tool-calls/references/adk-verification.md:82` says `RunConfig.max_llm_calls` is not inherited by `adk web`, and the ticket doesn't say how the demo runs. I deferred the spend stop rather than building one that might not apply. Neither skill says what to do at PoC depth when the run route is unknown.
- **Unsure:** `.claude/skills/adk-engineer/SKILL.md:135` says to keep `google.adk` out of package `__init__`. This project already had it there. Changing it is outside the ticket's literal scope, but without the change no test can run here. I chose a backward-compatible lazy `__getattr__`.
- **Unsure:** `.claude/skills/adk-engineer/SKILL.md:107` says helpers need Python 3.11+. It does not cover running the project's own tests when only an older interpreter has the test dependencies. I ran pytest on 3.9 and recorded that.
- **Heavier than needed for a PoC:** `.claude/skills/safe-api-tool-calls/references/validation.md:24-25` and `adk-verification.md:9-61` call for the full ADK ASGI/SSE confirmation test with a scripted model. That is a large share of a 3-hour budget, and it can't run here anyway. I wrote only a wiring test and recorded the full test as owed.
- **Heavier than needed:** `writes-and-confirmation.md:11-21` covers the durable ledger, exact money and competing workers. The opening note at `:3` and the PoC rule at `adk-engineer/SKILL.md:121-126` made it clear these could be deferred, which helped. Most of the section was still read with no effect on the work.
- **Unsure:** `.claude/skills/adk-engineer/SKILL.md:104-106` says to keep helper output in `.adk-evidence/`. The helper output was short and clean, so I recorded it here instead of creating the directory.

## 6. Next prompt the skills told the user to type

None given verbatim. `.claude/skills/adk-engineer/SKILL.md:39-44` tells the agent to write one, based on the verification still owed. The prompt I wrote:

> Install the project dependencies (google-adk==2.8.0) in a Python 3.11 venv and run `pytest tests/`, including `tests/test_agent_wiring.py`. Then, using safe-api-tool-calls, add an offline ADK HTTP/SSE test for `cancel_order` with a scripted model. Missing or rejected confirmation must send zero POSTs to the orders API, and an approved one exactly one. Record the results in the Evidence section of tickets/T-201.md.
