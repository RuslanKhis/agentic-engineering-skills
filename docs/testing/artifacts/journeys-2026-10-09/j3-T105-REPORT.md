# T-105 report: triage output arrives as prose

Skill root for all pointers below: `/Users/ruslankhissamiyev/Documents/Coding Projects/skills/agentic-engineering-skills/skills/<name>/`.

## 1. Specialist selection

**Entry point:** `adk-engineer` (invoked by the user as `/adk-engineer`).

**Primary specialist:** `adk-model-and-output-contracts`, mode (b) "Harden an existing contract (fences, prose instead of JSON, nulls, validation failures)" (`adk-model-and-output-contracts/SKILL.md:37`), composed with the "output schema together with tools" reference because `triage_agent` has both `tools` and `output_schema`.

**Routing text relied on**

- `adk-engineer/SKILL.md:63` (repo copy): "| Structured output arrives as prose or invalid JSON, response-schema design, model selection, thinking or temperature settings, model failover | `adk-model-and-output-contracts` |". This row matches the ticket symptom word for word.
- Catalogue description of `adk-model-and-output-contracts`: "Use for structured output that arrives as prose, fenced JSON or invalid data ... output_schema together with tools".
- Caveat: the copy the Skill tool actually loaded for `/adk-engineer` was `~/.claude/skills/adk-engineer/SKILL.md` (90 lines, 11-row table). It has **no** row for structured output; the closest rows were "Agent behaviour tests, evaluation datasets" and "Workflow structure". I only confirmed the routing after diffing against the repo copy (123 lines, 20-row table). Had I trusted the loaded copy, the honest routing would have been "no specialist in the table; closest is adk-workflow-design", which is wrong.

**Secondary skill consulted (read only, not loaded as a mode):** `adk-workflow-design/references/orchestration.md:8-39`, because `output-schema-and-tools.md:30` says the sequential wiring of a formatting sub-agent "belongs to adk-workflow-design". I used it only to confirm the `output_key` -> `{key}` handoff convention and the "Sequential" acceptance contract; no further loading was needed for a two-step pipeline.

**Why not others:** `adk-agent-instructions` (prompt wording is not the cause; the mechanism is), `adk-agent-evaluation` (a development-set run is the follow-up, not the fix), `adk-tool-interface-design` (tool schemas are unchanged).

## 2. Changes

```
 README.md                        |  4 +-
 support_agent/agent.py           | 89 ++++++++++++++++++++++++++++++------
 support_agent/triage_contract.py | 70 ++++++++++++++++++++++++++++
 tests/test_triage_agent.py       | 99 ++++++++++++++++++++++++++++++++++++++++
 tests/test_triage_contract.py    | 86 ++++++++++++++++++++++++++++++++++
 tickets/T-105.md                 | 18 ++++++++
 6 files changed, 350 insertions(+), 16 deletions(-)
```
(`git diff --stat` after `git add -N .`; the three new files are untracked. Nothing committed.)

**Root cause (from the specialist, verified against its 2.8.0 notes, not against live code):** `triage_agent` combined `tools` with `output_schema`. The README says the service runs on the API-key backend (`GOOGLE_GENAI_USE_VERTEXAI` unset). In ADK 2.8.0 the native response schema is set alongside tools only on the Vertex/enterprise variant; on the API key path ADK appends a best-effort `set_model_response` tool plus an instruction. When the model answers in prose instead of calling that tool, the text reaches `validate_schema` on the `output_key` save path, which raises and ends the run. This is exactly the `output_key then raises` symptom in the ticket.

**What changed**

- `support_agent/triage_contract.py` (new, pydantic only): hardened `Triage` model with `status: Literal["TRIAGED","CANNOT_TRIAGE"]`, `reason`, and nullable `category/priority/summary/order_id` so a refusal is valid JSON; `strip_fence` (mirrors ADK's whole-payload fence strip); `parse_triage`; `triage_failure`; `repair_text` returning the explicit failure JSON for invalid output; `ATTEMPT_KEY = "temp:triage_attempts"`.
- `support_agent/agent.py`: `triage_agent` is now a `SequentialAgent` of `triage_reader` (tools `fetch_email`, `search_kb`, free-text notes to `output_key="triage_notes"`, transfers disabled) and `triage_formatter` (no tools, `output_schema=Triage`, `output_key="triage"`, reads `{triage_notes?}`, transfers disabled). `guard_triage_output` is an `after_model_callback` on the formatter that converts any remaining invalid final text into the `CANNOT_TRIAGE` shape (so the save path never raises), counts attempts in `temp:` state and records `custom_metadata={"contract_failure": True, "attempts": n}`. The name `triage_agent` and the root agent's routing instruction are unchanged. Model pins, `billing_agent`, `refunds_agent` and `root_agent` are untouched.
- `tests/test_triage_contract.py`: 8 tests without ADK: valid JSON, whole-payload fence stripped, fence with trailing prose fails closed, prose -> failure shape with attempt count and finish reason, schema-invalid JSON -> failure shape, refusal drops `None` fields, no repair for valid output, generated schema stays inside the Gemini documented keyword subset.
- `tests/test_triage_agent.py`: 5 scripted-model tests requiring `google.adk` (`importorskip`): pipeline structure; request capture asserting `response_schema` + `response_mime_type="application/json"` and no `set_model_response` on the formatter; prose saves `CANNOT_TRIAGE` without raising and `temp:` key does not persist; fenced JSON saves; valid JSON saves and drops `None`.
- `README.md`: one sentence on the two-step triage pipeline. `tickets/T-105.md`: resolution section with the consumer-facing contract change.

**Validation performed**

| Status | Item |
| --- | --- |
| Offline simulated | `audit_model_config.py --project . --dry-run` and without `--dry-run`, exit 0 both times (Python 3.11): signals `schema_with_tools_path_depends_on_backend` at `agent.py:35` (the bug), `temperature_below_default` x2, `model_limited` for `gemini-2.5-pro` x4, no `issues`. |
| Offline simulated | `check_response_schema.py --pydantic-json` on the new `Triage` schema, exit 0: no unsupported keywords, depth 1, 6 properties, one `info` finding `optional_fields_outnumber_required` (intentional: refusal shape). |
| Offline simulated | `tests/test_triage_contract.py`: 8 passed (CPython 3.9.13 + pydantic 2.11.2, the only interpreter here with pydantic; run with a scratchpad `sys.modules` shim because `support_agent/__init__.py` imports ADK). Project targets 3.11; all files byte-compile under 3.11. |
| Not run | `tests/test_triage_agent.py` (5 tests) and `tests/test_tools.py`: `google.adk` is not installed and installs are prohibited. Collected as skipped. |
| Not run | Live model call, request capture against the real backend, development-set comparison (schema validity / answer accuracy / actionable accuracy / wrong-valid-schema). |

**Unverified / assumptions / questions I would have asked**

1. Confirm production really runs on the API-key backend (README says so). On Vertex the single-agent design would have taken the native path and a one-line backend fix might have sufficed; the split is correct on both backends, so the change stands either way.
2. Who consumes `state["triage"]`? The shape gained `status` and `reason`, and `category/priority/summary` can now be absent on a refusal. No consumer exists in this repo; downstream code must check `status`.
3. Category taxonomy and priority scale: with them I would have constrained `category` to an enum and `priority` with `minimum/maximum` (both in the documented subset). Left as free `str`/`int`.
4. Thinking settings: reader keeps the original `thinking_budget=2048`; formatter uses 1024 (formatting, not deciding). Unmeasured; a development-set run should confirm. `temperature=0.2` kept as found (the Gemini 3 "keep 1.0" guidance does not apply to 2.5).
5. `gemini-2.5-pro` is `limited` in the lifecycle table with Vertex retirement 2026-10-20 (12 days from now). Out of ticket scope; needs its own ticket (mode (c) + `adk-release-engineering`).
6. `{triage_notes?}` relies on ADK's optional-placeholder syntax so a missing key does not raise `KeyError`; verify on 2.8.0 when the ADK suite runs.
7. Approval for any live verification (project, location, request count, cost ceiling) was not obtainable offline.

## 3. Skills, references and scripts used, in order

1. Skill `adk-engineer` (loaded from `~/.claude/skills/adk-engineer/SKILL.md`, older copy).
2. Skill `adk-model-and-output-contracts` (`SKILL.md`, loaded from `.claude/skills/...` symlink to repo).
3. `adk-engineer/SKILL.md` repo copy, lines 28-70 (diffed against the loaded copy to confirm routing).
4. `adk-model-and-output-contracts/references/validation-and-repair.md` (mode b, first).
5. `adk-model-and-output-contracts/references/output-schema-and-tools.md` (mode b, tools present).
6. `adk-model-and-output-contracts/references/compatibility.md`.
7. `adk-model-and-output-contracts/references/validation.md`.
8. `adk-model-and-output-contracts/references/output-contracts.md` (refusal shape, keyword subset).
9. `adk-model-and-output-contracts/references/reasoning-and-sampling.md`, lines 1-60.
10. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (grep for `gemini-2.5-pro`).
11. `adk-workflow-design/references/orchestration.md`, lines 1-60 and grep hits (sequential handoff convention).
12. Script `scripts/audit_model_config.py --project . --dry-run`: exit 1 under system `python3` (3.9, `tomllib` missing); exit 0 under `/opt/homebrew/bin/python3.11`; exit 0 again without `--dry-run`.
13. Script `scripts/check_response_schema.py --schema <before.json> --pydantic-json`: exit 2 (my schema file was empty because 3.9 cannot evaluate `str | None` outside `from __future__ import annotations`); second run on the empty file exit 2 again (the project package import failed on ADK); third run on the real new schema: exit 0.

Not read: `model-selection.md`, `failover-and-providers.md`, `sources.md`, `adk-engineer/references/composition.md` (no `agents-cli-manifest.yaml`), the `adk-workflow-design` SKILL.md.

## 4. Friction log

Unsure what to do next / routing

- F1. `adk-engineer` loaded copy (`~/.claude/skills/adk-engineer/SKILL.md`, 90 lines) has no row for this symptom; the repo copy has it at `adk-engineer/SKILL.md:63`. Two installs of the same skill with different tables; the Skill tool picked the stale one. I spent a round-trip diffing them. The skill's own fallback text (`adk-engineer/SKILL.md:77-79`, "check the sibling directory") assumes a single install.
- F2. `adk-engineer/SKILL.md:29-31` ("Note the time budget, who judges the result and the artifact type (exploration, assignment, pilot, production)") and `:33-37` ("When continuing a design or implementation plan ... canonical plan or tracker") read like instructions to the skill's maintainer or to a benchmark harness, not to a user who typed "take ticket T-105". Neither could be answered from the repo.
- F3. `adk-engineer/SKILL.md:88` shows an `npx skills add` install command. In an offline session with install prohibited this is dead text; fine as a fallback, but it sits before "Apply the guidance", so it reads before the real work.
- F4. `output-schema-and-tools.md:30` hands the sequential wiring to `adk-workflow-design` without saying how much of it to load. I had to decide alone that one reference section (`orchestration.md:8-39`) was enough and that loading the whole skill would be overkill. A one-line "for a two-agent sequence, `SequentialAgent` + `output_key`/`{key}` is enough; load adk-workflow-design only for loops, parallelism or graphs" would have saved the detour.

References that had to be read before useful work

- F5. Mode (b) requires two references (`validation-and-repair.md`, 86 lines; `output-schema-and-tools.md`, 57 lines) plus `SKILL.md` step 1 pushes `compatibility.md` (62 lines) and "Validate and finish" pushes `validation.md` (58 lines); the refusal-shape rule that I needed for the schema lives in a fifth file, `output-contracts.md:34-51`, which mode (b) does not list. About 330 lines before the first edit. The content was accurate and load-bearing, but mode (b) should list `output-contracts.md` "Give refusal a first-class shape" explicitly, or `SKILL.md:52` ("Give refusal a first-class shape ...") should carry the code sample itself.

Instructions that assumed things a maintainer cannot provide

- F6. `adk-model-and-output-contracts/SKILL.md:22`: "Run the two helpers with an available Python 3.11+ interpreter". The project's `requires-python = ">=3.11"`, but the machine's default `python3` is 3.9 and the helper dies on `import tomllib` (`audit_model_config.py:11`) with a bare traceback. A one-line version check with a clear message, or a `tomli` fallback, would help.
- F7. `SKILL.md:26`: `python -c 'from app.schemas import Decision; ...'` assumes the project imports without its dependencies. Here `support_agent/__init__.py` imports `google.adk`, so the one-liner cannot run offline; I had to write a `sys.modules` shim. The skill could suggest `python -I` with a dummy package path, or note "if the package imports the SDK at init, load the schema module by file path".
- F8. `SKILL.md:30`: "refresh it before trusting it" about the lifecycle table. Refreshing means fetching vendor pages; prohibited here and not something a maintainer of the target repo can do. The table's `checked_on: 2026-10-08` (today) made it trustworthy anyway; say "if `checked_on` is older than N days, refresh" so the instruction is decidable.
- F9. `SKILL.md:62` and `validation.md:46` require approval for live calls with project, location, request count and cost ceiling; nothing in the repo supplies those, so the live check is always "not run" in this workflow. Expected, but the skill could state up front that mode (b) is complete offline and the live check is a separate ticket.

Places the skill talks to a repo maintainer rather than a user

- F10. `compatibility.md:54` ("The Gemini models ... pages were re-read on 2026-10-08 ... `assets/model-lifecycle-2026-10-01.json` records that check") and the whole of `validation.md:48-58` "Completion report" table are skill-maintenance provenance. Useful for trust, noise for the task.
- F11. `validation-and-repair.md:3`, `output-schema-and-tools.md:3`, `compatibility.md:3` each repeat "verified in 2.8.0 source on 2026-10-06; recheck in the target's pinned version". Fine once; three times is noise.

Heavier than needed

- F12. The audit JSON prints the full `limits` block (19 excluded directories) and the lifecycle `note` paragraph on every run, twice the size of the actual signals. A `--quiet` or putting `limits` behind `--verbose` would help.
- F13. The audit emits three signals per model literal (`model_kwarg`, `model_string`, `model_limited`), 12 lines for one string used four times. Deduplicate per literal.
- F14. `validation.md:9` asks for a "schema-valid wrong data" test with a `selected_ids` example; the Triage contract has no identifier set to validate against, so that test does not apply, and the reference does not say when it may be skipped.

Inaccuracies found

- F15. `validation-and-repair.md:17` and `:60`: "A JSON decode failure raises `ValueError`; a Pydantic failure raises `ValidationError`". With `BaseModel.model_validate_json` (pydantic 2.11), invalid JSON raises `ValidationError` (type `json_invalid`), a `ValueError` subclass. The `except (ValueError, ValidationError)` clause still works, but the comment misled my first test assertion (fixed in `tests/test_triage_contract.py:44-46`).

Genuinely helpful

- H1. `output-schema-and-tools.md:5-17` (the backend-decides table) named the root cause in one read and matched the README's backend note; the "Known reports" paragraph at `:57` (#3969) is the exact community symptom.
- H2. `validation-and-repair.md:39-69` gave a drop-in `after_model_callback` with the right `partial`/`error_code` guards and `temp:` attempt counting; `:69` steered me off the internal `validate_schema` import.
- H3. `output-contracts.md:34-51` (status enum + nullable payload, `exclude_none` consequence) directly shaped the new schema and the ticket's consumer note.
- H4. The two helpers are read-only, fast and their JSON is parseable; `schema_with_tools_path_depends_on_backend` at the exact line was a good confirmation, and the schema checker's `optional_fields_outnumber_required` info finding is a sensible nudge.
- H5. `output-schema-and-tools.md:37-53` request-capture test became `tests/test_triage_agent.py::test_formatter_request_carries_native_schema_and_no_set_model_response` almost verbatim.

## 5. Rating and top three improvements

**Frictionless rating: 3 / 5.** The specialist content was right and the fix was unambiguous once loaded; the friction was all in getting there (stale entry-skill install, interpreter and import assumptions in the helper workflow, five references for one mode).

1. **Make `adk-engineer` routing robust to stale installs and complete:** the loaded copy lacked the row that matters here. Ship the full 20-row table in every install, and add a line to `adk-engineer/SKILL.md:77-79` saying "if the catalogue lists a specialist that is not in this table, the catalogue description wins".
2. **Make the helper workflow run on a cold machine:** check `sys.version_info >= (3, 11)` in `audit_model_config.py` with a clear message (or fall back to `tomli`), and replace the `from app.schemas import ...` one-liner at `SKILL.md:26` with a snippet that loads the schema module by file path so an SDK-importing package does not block it.
3. **Collapse mode (b)'s reading list:** list `output-contracts.md` "Give refusal a first-class shape" in the mode (b) row, move the three "verified in 2.8.0 on 2026-10-06" banners and the `validation.md` completion-report table into `compatibility.md`, and state in `SKILL.md` that mode (b) is finished offline (live check and development-set run are follow-up tickets).
