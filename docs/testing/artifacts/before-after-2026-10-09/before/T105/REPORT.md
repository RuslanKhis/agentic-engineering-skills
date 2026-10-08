# T-105 report: Triage output arrives as prose

## 1. Skills invoked and reference files opened (in order)

1. `adk-engineer` (`/adk-engineer`): `.claude/skills/adk-engineer/SKILL.md`, which was loaded by the slash command
2. `.claude/skills/adk-model-and-output-contracts/SKILL.md`, read from the sibling directory
3. `.claude/skills/adk-model-and-output-contracts/references/validation-and-repair.md`
4. `.claude/skills/adk-model-and-output-contracts/references/output-schema-and-tools.md`
5. Ran `scripts/audit_model_config.py` and `scripts/check_response_schema.py`. I listed `scripts/`, `assets/` and `tests/` but did not read them.

Project files read: `tickets/T-105.md`, `README.md`, `pyproject.toml`, `support_agent/{agent,tools,__init__}.py`, `tests/test_tools.py`, `.github_workflows_ci.yml`, and `tickets/T-101..104.md` (to keep the scope separate from the other tickets).

## 2. Specialist chosen and why

**`adk-model-and-output-contracts`, mode (b) "Harden an existing contract".** The adk-engineer routing table sends "Structured output arrives as prose or invalid JSON" to this skill (`adk-engineer/SKILL.md:63`). That is the ticket almost word for word. No second specialist was needed:
- the model choice is T-103;
- the prompt wording only changed as far as the agent split required;
- the SequentialAgent wiring is the skill's own recommended design 2 (`output-schema-and-tools.md:30`), so I did not consult `adk-workflow-design`.

**Root cause, from the code and the skill's verified 2.8.0 facts.** The README says the service runs on the API-key backend (`GOOGLE_GENAI_USE_VERTEXAI` unset). `triage_agent` set both `tools` and `output_schema`. On that backend ADK 2.8.0 does not send `response_schema`. Instead it adds a `set_model_response` tool and an instruction, which is best-effort. When the model answers in prose instead, `validate_schema` raises during the `output_key` save, and the exception leaves the agent run. The audit helper flagged the same combination as `schema_with_tools_path_depends_on_backend` at `support_agent/agent.py:35`.

## 3. Files changed, and what is not finished

- `support_agent/triage.py` (new):
  - `Triage` moved here, with a new `status: Literal["triaged","cannot_triage"] = "triaged"` field. It defaults to `"triaged"`, so existing producers and consumers keep working.
  - `cannot_triage()` builds the explicit failure shape: `category="needs_human"`, `priority=1`.
  - `parse_triage()` mirrors 2.8.0 `validate_schema`, which strips a fence only when it wraps the whole payload.
  - `guard_triage` is an `after_model_callback`. It replaces an invalid, empty or error response with a valid `cannot_triage` record, counts failures in `temp:triage_contract_failures`, and marks the response with `custom_metadata.contract_failure`.
- `support_agent/agent.py`: `triage_agent` is now a `SequentialAgent` that keeps the same name and description, so the root's routing is unchanged. It runs:
  - `triage_reader`: has the tools and writes free-text notes to `triage_notes`.
  - `triage_formatter`: no tools, `output_schema=Triage`, `output_key="triage"`, `include_contents="none"`, the instruction templated from `{triage_notes}`, and `guard_triage`.
  - With no tools, the formatter gets the native `response_schema` on every backend.
  - `build_triage_formatter(model=...)` exists so tests can inject a scripted model. `Triage` is still re-exported from `agent.py`.
  - Model, temperature and thinking budget are unchanged.
- `tests/test_triage_contract.py` (new):
  - parse tests: whole-payload fence, prose, missing fields;
  - Runner tests with a scripted `BaseLlm`: valid output is saved; prose and wrong-type JSON become `cannot_triage` without raising;
  - a request-capture test: `response_schema` set, MIME type `application/json`, no `set_model_response` tool, notes templated into the instruction;
  - a structural test that tools and schema sit on different agents.

**Not finished or deliberately out of scope**

- **No real retry.** The guard turns a contract failure into an explicit, valid failure outcome on the first bad response, so the effective budget is 1. The skill says a genuine retry in 2.8.0 needs a caller that owns the `Runner` and re-invokes the agent (`validation-and-repair.md:71`). This repo has no Runner code; it presumably runs under `adk api_server`/`adk web`. A bounded 2–3 attempt loop around the formatter, a LoopAgent with a checker, is adk-workflow-design work and was not done.
- **Model and settings left alone.** `gemini-2.5-pro` (flagged `model_limited` by the audit) and `temperature=0.2` (flagged `temperature_below_default`) are not changed. That belongs to T-103.
- **No measured comparison.** There is no development-set run of schema validity versus wrong-valid-schema through adk-agent-evaluation (the skill's third check), because that needs live model calls.
- **Prompt injection not addressed.** The email body now flows into the formatter instruction through `{triage_notes}`, so injected text reaches it the same way it already reached the triage agent. That is part of T-104.

**Assumptions, and the questions I would have asked**

1. *Is the deployment definitely the API-key backend?* I assumed yes, per the README. On Vertex, the old single agent would have used the native path. The split is still correct there and works on both backends.
2. *What does the priority scale mean?* I assumed 1 is the most urgent, so failures go to a human fast. If 1 is lowest, change `cannot_triage()` in `support_agent/triage.py`.
3. *Can the `Triage` schema gain a `status` field?* I assumed yes, because it has a default and nothing downstream in the repo reads `state["triage"]`.
4. *Is a `cannot_triage` record acceptable when the model fails, or does product want a real retry first?* I assumed the explicit failure is acceptable for now, with the retry left as a follow-up.
5. *Is an extra model call per triage (reader plus formatter) acceptable for latency and cost?* I assumed yes.

## 4. Checks run and not run

**Run**

| Check | Result |
|---|---|
| `py_compile` (Python 3.12) on `support_agent/*.py`, `tests/*.py` | Passed |
| `audit_model_config.py --project . --dry-run` (Python 3.12) | Passed; project findings below |
| `check_response_schema.py --pydantic-json` on the new `Triage` schema | `findings: []`, exit 0 |

Audit findings in the project code:
- `gemini-2.5-pro` reported `model_limited` at lines 18, 26, 37, 48;
- `temperature_below_default` at lines 35, 46;
- `schema_with_tools_path_depends_on_backend` at line 35, which is the cause of this ticket.

The schema checker needed a schema JSON. I generated it with Python 3.9, the only interpreter with pydantic installed, using `Optional[str]`, which produces the same schema as `str | None`. Stats: 5 properties, depth 1, 1 anyOf-null.

**Not run**

- `pytest`, both `tests/test_triage_contract.py` and the existing `tests/test_tools.py`. `google.adk` is not installed and installing it was not allowed. `test_tools.py` also imports `google.adk` indirectly through `support_agent/__init__.py`. The new tests were written against the 2.8.0 API as the skill describes it (`BaseLlm.generate_content_async`, `Runner`, `InMemorySessionService`, `llm_request.config.response_schema`) and have never been executed.
- Live model or provider verification, and the dev-set evaluation (adk-agent-evaluation).

## 5. Friction log

- **Helpful:** `adk-engineer/SKILL.md:63` routed the ticket in one step, with nothing left to decide.
- **Helpful:** `adk-model-and-output-contracts/references/output-schema-and-tools.md:9-17,25,30` explained the exact root cause (the backend-gated `set_model_response` workaround) and prescribed the fix. Together with `validation-and-repair.md:39-67` (guard callback pattern) and `SKILL.md:56-60` (which tests to write), this got me to the implementation with no guesswork.
- **Unsure / environment assumption:** `SKILL.md:22` says "Python 3.11+", but the default `python3` here is 3.9. `audit_model_config.py:11` does `import tomllib` and failed with a bare traceback instead of a version message. I had to find `/opt/homebrew/bin/python3.12` myself.
- **Assumed something I could not provide:** the example at `SKILL.md:26` (`python -c 'from app.schemas import ...'`) assumes the project's schema module can be imported. Here it cannot: importing `support_agent` pulls in `google.adk`, and no interpreter has both pydantic and 3.10+ syntax support. I rebuilt the schema by hand in a 3.9 one-liner.
- **Heavier than needed:** `audit_model_config.py` with `--project .` scanned `.claude/skills/**` (the skills' own tests and scripts). Most of the roughly 25 KB of output was about other skills' fixtures, and I had to filter by path. Excluding `.claude/` by default, or adding a `--path` filter, would help.
- **Unsure:** `validation-and-repair.md:71` says the only genuine retry is a caller around the Runner. The project has no Runner code, so I could not tell where an attempt budget should live. `SKILL.md:58` asks for a test proving "the attempt budget", which my budget-of-1 design only trivially satisfies. A recipe for a 2.8.0 in-ADK bounded retry, or a pointer to the exact adk-workflow-design reference, would have closed this.
- **Unsure:** `SKILL.md:48` and `validation-and-repair.md:63` say to give refusal a first-class shape (`Decision(status="CANNOT_DECIDE", ...)`). The existing `Triage` has required `category` and `priority`, so a failure value had to be invented (`needs_human`, priority 1) without knowing the priority semantics.
- **Minor:** the `SKILL.md:30` audit output's `issues` list was empty while the relevant problems appeared under `signals`. It was not obvious at first which list to read.
- **Minor:** `adk-engineer/SKILL.md:77-80` says to find the specialist "through the available-skills catalogue" or the sibling directory. The sibling path worked immediately.

## 6. Rating and top three changes

**4 / 5.** The routing and references were accurate and specific enough to diagnose and fix the ticket without outside research. The friction was in the helper scripts and the retry gap.

Three changes that would help most:
1. Make the helper scripts check the Python version and print "requires Python ≥3.11" instead of a traceback. Have the audit exclude `.claude/` (and other skill directories) by default.
2. Add a 2.8.0 recipe for a bounded in-ADK retry of a formatter agent, for example a LoopAgent plus checker with `max_iterations`, or link the exact adk-workflow-design section. As written, "build it at a boundary you own" leaves projects that use `adk api_server` with no owned boundary.
3. Give a fallback for producing the schema JSON when the project cannot be imported. For example, let `check_response_schema.py` accept a `--model module:Class` path and load only that file.

## 7. Next prompt the skills told the user to type

None given.
