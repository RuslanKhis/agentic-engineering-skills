# REPORT — T-105 "Triage output arrives as prose"

## 1. Skills invoked and reference files opened (in order)
1. Skill `adk-engineer` (/adk-engineer): `.claude/skills/adk-engineer/SKILL.md`, loaded by the slash command.
2. Project files: `tickets/T-105.md`, `README.md`, `pyproject.toml`, `.github_workflows_ci.yml`, `support_agent/{__init__,agent,tools}.py`, `tests/test_tools.py`. Skimmed `tickets/T-101..T-104.md` for scope boundaries.
3. `.claude/skills/adk-model-and-output-contracts/SKILL.md` (specialist), read from the sibling directory.
4. `.claude/skills/adk-model-and-output-contracts/references/validation-and-repair.md` (mode b)
5. `.claude/skills/adk-model-and-output-contracts/references/output-schema-and-tools.md` (mode b, because tools are present)
6. `.claude/skills/adk-model-and-output-contracts/references/validation.md`
7. `.claude/skills/adk-model-and-output-contracts/references/output-contracts.md`, lines 1–60 (refusal shape, schema subset)
8. Helpers run: `scripts/audit_model_config.py` and `scripts/check_response_schema.py`.

Not opened: `adk-engineer/references/composition.md` (no agents-cli manifest), `adk-workflow-design` (see friction log), and the other references in the specialist.

## 2. Specialist chosen and why
**Specialist: `adk-model-and-output-contracts`.** The ticket ("returns a paragraph instead of the Triage JSON and output_key then raises") matches the routing-table row "Structured output arrives as prose or invalid JSON" word for word (`adk-engineer/SKILL.md:67`). Mode (b), "Harden an existing contract", applies, and tools are present on the agent. I loaded no supporting skill. The split into a SequentialAgent touches the area of `adk-workflow-design`, but the wiring is a standard two-step sequence, so I didn't read that skill (see friction log).

## 3. Files changed / not finished
- `support_agent/triage_contract.py` (new, imports no SDK): the `Triage` schema with a first-class refusal shape (`status: TRIAGED|CANNOT_TRIAGE`, nullable `category`/`priority`/`order_id`), plus `parse_triage` (strips a fence only when it wraps the whole payload, matching ADK 2.8.0), `cannot_triage` and `triage_or_failure`.
- `support_agent/agent.py`: `triage_agent` is now a `SequentialAgent(name="triage_agent")`, so routing from root is unchanged. It has two steps:
  - `triage_reader`: uses tools, has no schema, writes `output_key="triage_notes"`.
  - `triage_formatter`: has no tools, keeps `output_schema=Triage, output_key="triage"`, has the `guard_triage` after_model_callback, and fills `{triage_notes?}` from state.

  `guard_triage` turns invalid output and provider errors into a valid `CANNOT_TRIAGE` record with `custom_metadata={"contract_failure": True}`. The other agents and the model IDs are untouched.
- `support_agent/__init__.py`: `root_agent` is now loaded lazily through a module `__getattr__`, so SDK-free modules and tests import without google.adk. Before this change `tests/test_tools.py` could not even be collected without the SDK.
- `tests/test_triage_contract.py` (new, SDK-free): 10 cases covering prose, fence with prose, missing or bad fields, valid JSON, fenced JSON, the failure shape surviving `exclude_none`, and a refusal from the model.
- `tests/test_triage_agent.py` (new, skipped when google.adk is absent): agent structure, guard callback cases, a scripted-model run proving prose saves `CANNOT_TRIAGE` instead of raising, and a request-capture test asserting the formatter carries `response_schema` plus `application/json` with no `set_model_response`.
- `tickets/T-105.md`: Evidence section appended.

Not finished:
- No genuine retry. The in-agent budget is 0, because a callback cannot re-call the model; a retry needs the Runner owner (Cloud Run entrypoint, not in repo) to re-invoke on `contract_failure`.
- `pytest-asyncio` is not in the dependencies, so the async tests in `test_triage_agent.py` need it added (not done: no installs, and I left the dependency pins alone).
- No development-set measurement (adk-agent-evaluation) of whether two calls change triage accuracy or latency.
- Model migration (T-103) and the 0.2 temperature the audit flagged were left alone. The formatter copies the reader's existing config.

### Assumptions / questions I would have asked
1. Is the production backend really the API key (README), or Vertex? On Vertex the original single agent would have used the native path; I assumed the README is current.
2. Does anything downstream read `state["triage"]`? None does in the repo. Is changing it (new `status`, nullable `category`/`priority`, missing keys when None) acceptable?
3. What is the priority scale (1 = high or low, and the range)? I left it as an unconstrained int rather than inventing an enum.
4. Is an extra model call per triage (reader + formatter) acceptable for cost and latency?
5. Is there a Runner-owning caller where a re-invocation retry (budget 2) should live?
6. Should `order_id` be checked in code against the fetched email text ("model decides, code copies")? Not done, because the email body isn't available to the formatter's code without another fetch.
7. Does ADK 2.8.0's agent loader accept a lazy `root_agent` (via `hasattr` on the package)? I believe it does, but couldn't verify without the SDK.

## 4. Checks
Run:
- `audit_model_config.py --project . --dry-run` (python3.11): exit 1 = partial, because it also walked `.claude/skills` and hit a malformed file there. Project findings: `schema_with_tools_path_depends_on_backend` at agent.py:35 (the root cause), `gemini-2.5-pro` as `model_limited` on all four agents (T-103 territory), and `temperature_below_default` at agent.py:35 and :46.
- `check_response_schema.py --pydantic-json` on the new `Triage` schema: exit 0, no unsupported keywords; info: `optional_fields_outnumber_required` (3 vs 2).
- `pytest` with Python 3.9.13 + pydantic 2.11.2 (the only interpreter with pydantic/pytest; the project needs ≥3.11): **11 passed, 1 skipped** (`test_triage_agent.py`, no google.adk).
- `py_compile` of all changed files under python3.11: OK.
- Baseline comparison: before the change, `tests/test_tools.py` failed to collect without the SDK (`ModuleNotFoundError: google.adk`).

Not run:
- `tests/test_triage_agent.py`: all 6 tests (guard callback, scripted Runner save path, request capture). They need google-adk 2.8.0 and pytest-asyncio.
- Any live model call.
- The development-set comparison.
- The test suite under Python 3.11+ with the pinned dependencies.

## 5. Friction log
- **Helpful:** the routing table row "Structured output arrives as prose or invalid JSON" (`.claude/skills/adk-engineer/SKILL.md:67`) made the choice immediate.
- **Helpful:** the audit finding `schema_with_tools_path_depends_on_backend`, combined with `output-schema-and-tools.md:9-15` (backend table) and `:27-30` (choose the design), gave root cause and fix in a few minutes. The README's "API-key backend" line settled it.
- **Helpful:** `validation-and-repair.md:7-17` explained exactly why the save raises.
- **Helpful:** `validation.md:7-8` gave concrete test cases I could turn into tests directly.
- **Unsure / reading before useful work:** I read four references (~250 lines) before editing. `validation-and-repair.md` and `output-schema-and-tools.md` both needed to be read in full; `output-contracts.md` was only needed for the refusal shape (`:34-51`).
- **Assumed something I couldn't provide:** `adk-model-and-output-contracts/SKILL.md:26` shows `python -c 'from app.schemas import Decision ...'` to generate the schema. That requires the project's dependencies in a 3.11+ interpreter. None of the 3.11+ interpreters had pydantic, so I generated the schema with the 3.9 interpreter and ran the checker with 3.11. `adk-engineer/SKILL.md:101-103` covers the helper's interpreter but not this extraction step.
- **Heavier than needed:** `audit_model_config.py` (run per `SKILL.md:25`) walked `.claude/skills/**` (104 files, ~32 KB of JSON), reported the run as partial (exit 1) because of a malformed file in another skill, and offers no exclude/path flag. I had to filter the JSON myself to find the 15 project findings.
- **Unsure:** the callback example in `validation-and-repair.md:49-66` increments an attempt counter, yet the callback cannot retry (`:39`, `:71`). So "attempt budget" in `SKILL.md:50` doesn't map onto the recommended in-agent placement. I dropped the counter and documented a budget of 0 inside the agent.
- **Unsure:** `output-schema-and-tools.md:30` says the formatting-sub-agent wiring belongs to adk-workflow-design. Loading another skill for a plain SequentialAgent felt heavier than needed, so I skipped it. The cost is an unverified choice between SequentialAgent and AgentTool `single_turn`.
- **Unsure:** the `Triage` refusal shape (`SKILL.md:48`, `output-contracts.md:34-51`) forces a change to a contract with unknown consumers. The skill doesn't say how to handle a contract change when consumers can't be asked.
- **Assumed something I couldn't provide:** `adk-engineer/SKILL.md:118-123` asks for SDK-free tests and no google.adk in `__init__.py`. The existing package violated this, so honouring it meant changing the package entry point (lazy `__getattr__`), which carries a deployment risk I couldn't verify.
- **Unsure:** `adk-engineer/SKILL.md:39-40` says to "end with the run prompt for the next ready goal or ticket" but gives no template, and the tickets have no prerequisites or status, so "next ready" is undefined.
- **Assumed something I couldn't provide:** `validation.md:3` asks for scripted-model tests using the target's runner. The project has no pytest-asyncio, and the skill doesn't mention that async Runner tests need it.

## 6. Rating
**3.5 / 5**, rounded to **4**: routing and diagnosis were fast and accurate; the costs were extra reading, a noisy helper and some guesswork at the edges.

Three changes that would help most:
1. Give `audit_model_config.py` a `--path`/`--exclude` option (or skip `.claude/` and other skill directories by default), and don't mark the run partial for files outside the project.
2. Add a short "prose instead of JSON with tools" recipe to the SKILL.md itself: the backend check, the reader/formatter split with code, the guard callback without a fake attempt counter, and the tests. Mode (b) then needs one reference instead of four.
3. Give `adk-engineer` a template for the ticket Evidence section and the next-ticket prompt, plus guidance for SDK-free test setup (lazy `__init__`, pytest-asyncio) and for extracting the schema when project dependencies aren't installed.

## 7. Next prompt the skills told the user to type
None given. `adk-engineer/SKILL.md:40` says to "end with the run prompt for the next ready goal or ticket" but supplies no wording, and the tickets define no readiness order.
