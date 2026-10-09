# REPORT — T-201 "Demo: cancel an order from chat"

**Specialist: `safe-api-tool-calls`**, because the ticket adds a state-changing call to an external API
(`POST /orders/{id}/cancel`). With a write like that, the risks are duplicate or ambiguous outcomes,
retry behaviour and confirmation. The ticket named no `Primary skill`, so I picked from the table
in `adk-engineer`. I added no supporting skill. `adk-operational-guardrails` (human approval) was
considered, but ADK's per-tool confirmation is already covered by safe-api-tool-calls (writes-and-confirmation §4).

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-engineer` (invoked by the user): `.claude/skills/adk-engineer/SKILL.md`.
2. `.claude/skills/safe-api-tool-calls/SKILL.md` (read directly from the sibling directory, as `adk-engineer` directs).
3. `.claude/skills/safe-api-tool-calls/references/writes-and-confirmation.md`
4. `.claude/skills/safe-api-tool-calls/references/compatibility.md`
5. `.claude/skills/safe-api-tool-calls/references/validation.md`
6. `.claude/skills/safe-api-tool-calls/references/adk-verification.md`
7. Ran helper `.claude/skills/safe-api-tool-calls/scripts/inspect_project.py --project . --dry-run`. The first try with Python 3.9 was refused; it ran under Python 3.12. Output is saved in `.adk-evidence/inspect_project.txt`.

Not opened: `references/reads-and-deadlines.md`, `references/adk-operations.md`, `references/inspection.md`, and `adk-engineer/references/composition.md` (there is no `agents-cli-manifest.yaml`).

## 2. Questions I would have asked, and the answer I assumed

| # | Question | Assumed answer |
|---|---|---|
| 1 | Does the staging orders API deduplicate repeated `POST /cancel` calls (idempotency key, or does cancel become a no-op/409 once already cancelled)? | Unknown. So there is **one attempt with no retries**, and a lost response is reported as `unknown`. |
| 2 | Which agent should own cancellation: root, `refunds_agent`, or a new sub-agent? | `support_root`, next to `get_order`. It is the agent the customer talks to, so the demo needs no transfer. |
| 3 | Should the agent ask the human before cancelling? | Yes, through ADK `require_confirmation=True`. It is cheap and demos well, and it is the minimum before productionising. |
| 4 | Must the demo also *look up* orders on staging? Today `ORDERS_API` points at `orders.internal.example`, where the fake orders do not exist. | Yes. `ORDERS_API` is now read from `ORDERS_API_URL`, with the same default. The demo sets it to staging. |
| 5 | Could this ship to production by accident? (`main` is released weekly to Cloud Run.) | It must not cancel real orders. `cancel_order` dispatches only when `ORDERS_API` is in `CANCEL_ALLOWED_APIS` (staging only). Everywhere else it returns `not_cancelled` and sends nothing. |
| 6 | Must the caller own the order (authorisation)? Which customer identity applies? | Not for the demo, since all orders are fake. This is recorded as a production gap; the model-supplied ID is the only input. |
| 7 | What does the cancel endpoint return, and what are its order-ID format, auth headers and status codes? | 2xx means cancelled, with a JSON body echoed if it is an object. 4xx means refused. 5xx or a lost response means unknown. IDs match `[A-Za-z0-9_-]{1,64}`. No auth header, matching the other order tools. |
| 8 | Which ADK session service does the demo use? (Confirmation is documented as unsupported on `DatabaseSessionService`/`VertexAiSessionService`, per compatibility.md:81-87.) | Local `adk web` (SQLite-backed) for the demo. This was not verified for the Cloud Run deployment. |

## 3. Files written or changed, and what is not finished

Changed:
- `support_agent/tools.py`
  - Added `cancel_order` and `CANCEL_ALLOWED_APIS`.
  - `ORDERS_API` is now overridable through `ORDERS_API_URL`, with an unchanged default.
  - Added `os` and `re` imports.
- `support_agent/agent.py`: imported `FunctionTool`, registered `FunctionTool(tools.cancel_order, require_confirmation=True)` on `support_root`, and added a three-sentence cancel instruction.
- `tickets/T-201.md`: added an Evidence section.
- `.gitignore`: created, containing `.adk-evidence/`.

Written:
- `tests/test_cancel_order.py`: 12 offline tests covering success, the non-staging guard, invalid IDs, 409 refusal, unknown outcome without retry (read timeout, dropped connection, 503) and connect failure.
- `tests/test_agent_wiring.py`: an SDK test asserting that `cancel_order` is registered only behind confirmation.
- `.adk-evidence/inspect_project.txt` and `.adk-evidence/pytest_offline.txt`.

Not finished, or left out on purpose for a ~3 h PoC:
- The **ADK HTTP/session confirmation test** from adk-verification.md §1 was not written. It would use `/run_sse`, an `adk_request_confirmation` round trip, and check that rejection makes zero provider calls.
- `tests/test_agent_wiring.py` asserts the private attribute `_require_confirmation`. I took that name from my knowledge of ADK, not from the installed 2.8.0 source, so it may need adjusting.
- No reconciliation for `unknown` outcomes. A person checks by hand. There is no durable operation record or idempotency key, no caller authorisation, and no check of order state before cancelling.
- `support_agent/__init__.py` still imports `google.adk` through `.agent`. As a result, even `tests/test_tools.py` cannot import `support_agent` without ADK installed. I did not change it: that would change how ADK discovers the agent, which is outside this ticket and could not be verified here.
- The instruction text follows the existing prompt's style. It was not reviewed with `adk-agent-instructions`.

## 4. Checks run, and checks not run

Run:
- `python3 -m pytest -q tests/test_cancel_order.py tests/test_tools.py tests/test_agent_wiring.py` gave **13 passed, 1 skipped** (offline simulated).
  - Interpreter: Python 3.9.13 (anaconda), the only local interpreter with httpx 0.28.1 and pytest 7.1.2. The project declares `>=3.11`, so this is a version mismatch.
  - Run through `python3 -I -c …`, which pre-registers `support_agent` as a bare package path so the ADK-importing `__init__` is skipped. Only `tools.py` is loaded, and it does not import ADK.
  - The provider is replaced at `httpx.post`. No network was used.
- `python3.11|3.12|3.13 -m py_compile` on `support_agent/tools.py`, `support_agent/agent.py` and `tests/*.py`: all OK. This only checks syntax.
- `inspect_project.py --dry-run` (Python 3.12): ran, but returned no signals and no issues.

Not run:
- `tests/test_agent_wiring.py`: skipped because google-adk is not installed. **Not run.**
- The full CI command `pip install -e . pytest && pytest`: package installs are forbidden here. **Not run.**
- ADK confirmation pause, approve and reject through Runner or `adk web`. **Not run.**
- A live call to the staging orders API. **Not run** (network is forbidden).
- Live model behaviour (does the model pick `cancel_order`, and does it describe a rejection accurately?). **Not run.**

## 5. Friction log

- **Unsure:** whether to put `google.adk` imports outside `__init__.py`. `adk-engineer/SKILL.md:124-126` says to keep them out of package `__init__` files. This project's `__init__.py` re-exports `root_agent`, the usual ADK layout. Changing it is a refactor outside the ticket. I kept it and worked around it in the test command instead.
- **Unsure:** whether a "proof of concept, ~3 h" ticket still needs the full ADK HTTP confirmation test. `safe-api-tool-calls/references/validation.md:24-25` and `references/adk-verification.md:9-56` call for it. `adk-engineer/SKILL.md:29-32` asks me to size the work by artifact type. I sized it as a demo and left the HTTP test as owed verification.
- **Heavier than needed:** `references/writes-and-confirmation.md:19-21` (durable ledger, abandoned claims, balance races) and `compatibility.md:58-74` were long for a fake-order demo. The useful part was §1 at lines 7-8 (unknown replay means no retries) and §4 at lines 37-41.
- **Heavier than needed / unhelpful:** the inspection helper refused Python 3.9 (`safe-api-tool-calls/scripts/inspect_project.py:12-15`). That is fine, but on 3.12 it reported `"signals": []` for a repo with an unguarded `httpx.post` refund and no retries or confirmation. The empty result added nothing; manual inspection did the work.
- **Unsure:** the `compatibility.md:81-87` warning that confirmation is unsupported on `DatabaseSessionService` and `VertexAiSessionService` matters for the post-demo Cloud Run deployment, but the README does not say which session service is used. Recorded as question 8.
- **Genuinely helpful:** `safe-api-tool-calls/SKILL.md:47-50` and `references/writes-and-confirmation.md:7` together settled the key choice: no retries, and an honest `unknown` result. `references/writes-and-confirmation.md:37` gives ADK's exact rejection string to plan the instruction around. `references/validation.md:17` led directly to the "lost response is called once and reported unknown" test.
- **Helpful:** `adk-engineer/SKILL.md:53` (announce the specialist before editing) and `adk-engineer/SKILL.md:38-43` (write evidence into the ticket and end with a follow-up prompt) gave a clear finishing checklist.

## 6. Next prompt the skills told the user to type

None given verbatim. `adk-engineer/SKILL.md:40-43` tells the agent to compose one: when no ready ticket follows, it should be the verification still owed, written so the user can paste it. That composed prompt is:

> Take ticket T-201 and run the verification still owed: install the project's pinned dependencies (google-adk 2.8.0), run `pytest` including tests/test_agent_wiring.py, then add an offline ADK `/run_sse` test showing that cancel_order emits `adk_request_confirmation`, makes zero orders-API calls when rejected and exactly one when approved, and record the results in the ticket's Evidence section.
