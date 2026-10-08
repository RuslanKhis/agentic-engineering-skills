# T-101 report: wrong tool picked for order lookups (reconstructed)

> Reconstructed from the working tree after the trial was interrupted by a usage limit before it wrote its own report. The original agent's live friction log, the commands it ran and their output were lost with the interruption. Everything below is inferred from `git diff`, the new files and offline checks run during the reconstruction.

Skill root for pointers: `/Users/ruslankhissamiyev/Documents/Coding Projects/skills/agentic-engineering-skills/skills/<name>/`.

## 1. Specialist selection (inferred)

**Primary:** `adk-tool-interface-design`, mode (b) "Wrong tool or wrong parameter diagnosis" (`adk-tool-interface-design/SKILL.md:67`), with a light touch of `adk-agent-instructions` for the prompt text.

Evidence: the rewritten docstrings follow the template at `SKILL.md:78-82` (what it does and returns, when to use it and when not, one line per parameter with an example, return structure with `status` values and example dicts). The error returns carry `status`, `error_message`, `hint` and `retryable` (`SKILL.md:92-95`). `search_orders` got a tuning-knob default with a ceiling (`max_results`, default 10, at most 25). `prompts.py` says it was split out "so it can be tested without the SDK", and it rewrites the "ALWAYS call search_orders first" mandate as conditions.

**Routing row:** `adk-engineer/SKILL.md:62`: "Wrong tool or wrong arguments chosen, tool docstrings and parameter schemas ... | `adk-tool-interface-design`". This row matches the ticket word for word. Secondary row `:61` (instruction text, tool-use guidance) covers the prompt change.

## 2. Changes

```
 support_agent/agent.py   |   6 +-
 support_agent/prompts.py |  23 ++++++   (new; staged intent-to-add)
 support_agent/tools.py   | 179 ++++++++++++++++++++++++++++++++++++++++++++---
 3 files changed, 197 insertions(+), 11 deletions(-)
```
No other untracked files. Nothing committed.

- `tools.py`: `search_orders(value)` became `search_orders(customer_query, max_results=10)`, and `get_order(data)` became `get_order(order_id)`. Both have full docstrings that name the alternative tool. New `looks_like_order_id` uses a documented assumed shape: at least one digit, no whitespace, no `@`, 3 to 32 characters. Each tool refuses the other tool's kind of input with an actionable hint (`search_orders("ORD-123456")` returns "Call get_order with order_id=... instead"). HTTP failures, 404 and 5xx become error dicts instead of exceptions. Search results are bounded and labelled `complete/truncated/empty`. `_shape_order` makes sure every hit carries `order_id`. The unused `json` import is gone.
- `prompts.py` (new, stdlib only): `ORDER_LOOKUP_GUIDANCE`, the ID-to-`get_order` and name-to-`search_orders` conditions with "never cross" and "follow the hint", plus `BILLING_INSTRUCTION`.
- `agent.py`: `billing_agent` uses `BILLING_INSTRUCTION`, which replaces "ALWAYS call search_orders first. NEVER answer without calling a tool". The root instruction appends the guidance. Models, tool lists and the other agents are unchanged.

## 3. Completeness against the ticket

| Item | State |
| --- | --- |
| Model calls `get_order` when given an ID | **Done at the interface:** docstrings, parameter names, instruction and a defensive redirect in `search_orders`. |
| Name passed where the ID belongs | **Done:** `get_order` rejects non-ID shapes with a hint to use `search_orders`. |
| Root cause in the instruction ("ALWAYS call search_orders first") | **Done** for `billing_agent`. |
| Tests | **Missing.** No test file was added or changed. There is no unit test of the guards and no scripted-model Runner test (`SKILL.md:125-129` requires one per changed tool, including an error branch). |
| Before/after declaration dump and linter diff (`SKILL.md:55-56`, `:125-127`) | **Missing.** No artefacts. |
| Hand-off of the accuracy measurement to `adk-agent-evaluation` | **Missing.** No eval cases or note. |
| Order-ID format confirmation | **Open.** The regex is an explicit assumption in `tools.py`. |

Verdict: the code fix is plausible and coherent but unvalidated, so the trial is about 60% complete. The interruption most likely came before the tests.

**Validation run during reconstruction**

| Status | Item |
| --- | --- |
| Not run | `tests/test_tools.py` (baseline, 1 test). Collection fails under system Python 3.9 because `support_agent/__init__.py` imports `google.adk`, which is not installed. |
| Local (ad hoc) | Loaded `tools.py` by file path (system python 3.9, httpx present). `search_orders("ORD-123456")` and `get_order("Jane Doe")` return the designed hints. `get_order("")` returns "order_id is empty." No network was touched, because the guards return before `httpx`. |
| Local | `lint_tool_schemas.py --project .` (python3.11, read-only) reports only `short_agent_description` x3 and **zero tools**. See friction F1. |

## 4. Quality notes against `adk-tool-interface-design/SKILL.md`

1. **Docstring as the whole interface (`SKILL.md:78-82`): followed.** Both tools state the use and non-use case, name the alternative, give a parameter example and show a success and an error example dict.
2. **Status dicts, hints, never raise, bounded lists (`SKILL.md:92-95`): followed** for the two touched tools. `issue_refund` still raises (`tools.py`, untouched, out of scope).
3. **`async def` for I/O tools (`SKILL.md:96-97`): not followed.** Both tools remain sync `httpx.get`.
4. **Mode (b) "fix the description or name before touching the instruction" (`SKILL.md:67`): partly.** The trial changed both in one change set. That is defensible because the instruction mandate was a direct cause, but it confounds attribution of any later accuracy change.
5. **Parameter renames change the tool schema** (`value` became `customer_query`, `data` became `order_id`). Any recorded eval trajectory with the old argument names breaks. T-103's new eval set, for example, freezes `search_orders.args.value`. The skill does not warn that a rename is a schema version event (see the release-engineering "tool schema hash", `adk-release-engineering/SKILL.md:47`).

## 5. Friction the artefacts reveal

- **F1. The linter misses the most common tool-reference pattern, and the miss is silent.** On this repo (`from . import tools`, `tools=[tools.search_orders, ...]`) `lint_tool_schemas.py` returns `tools: []`, `partial: false`. `tool_entry` (`adk-tool-interface-design/scripts/lint_tool_schemas.py:348-366`) only resolves `ast.Name` and wrapper calls, so `ast.Attribute` references fall through to `"other"`. `SKILL.md:41-46` promises findings for one-line docstrings and generic parameters, which are exactly this ticket's bugs (`"""Search orders."""`, `value: str`, `data: str`), and the linter reports none of them. A maintainer gets a clean bill of health.
- **F2. Testability without the SDK pushed the agent into a layout change.** `prompts.py` exists "so it can be tested without the SDK", but the package `__init__` still imports `google.adk`, so even `tests/test_tools.py` cannot run offline. The skill's validation path (`SKILL.md:125-129`: live declaration dump, scripted-model Runner test) needs the SDK and gives no offline fallback. The other trials each invented a different workaround: T-102 used a lazy `__getattr__`, T-104 loaded by file path, and T-105 used a `sys.modules` shim.
- **F3. "Dump the live declarations" (`SKILL.md:67`) and "record the before" (`SKILL.md:55-56`)** both require importing the agent. With no SDK there is no "before" artefact, and none exists here.
- **F4. Identifier-format decision.** `SKILL.md:58-60` lists what to ask, but not "the format of user-supplied identifiers". The agent had to invent a regex and annotate it as an assumption.
- **F5. Routing overlap.** The ticket needs both `:61` (instructions) and `:62` (tools) in `adk-engineer`. `adk-engineer/SKILL.md:117-119` covers this ("name the primary, keep one change set"), and the trial followed it.

## 6. Note on lost evidence

The original agent's friction log, its skill-loading sequence, the helper commands it ran and their exit codes were lost when the session hit the usage limit. The specialist attribution above is inferred from code style and comments, not observed.
