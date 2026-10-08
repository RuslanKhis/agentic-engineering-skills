I've fixed T-105 by giving the tool calls and the JSON output to two separate agents, but none of the tests have run. `google.adk` isn't installed here, so I could only check that the files compile.

**Specialist: `adk-model-and-output-contracts`.** The routing table sends "structured output arrives as prose or invalid JSON" to this skill, which is almost exactly the ticket. I used its "harden an existing contract" mode.

**Why it happened:** The README says the service runs with an API key rather than Vertex. On that setup, ADK 2.8.0 can't enforce a JSON schema on an agent that also has tools. It asks the model to call an extra `set_model_response` tool instead, and nothing forces it to. When the model answers in prose, saving the result to `output_key` raises an error that ends the run. The skill's audit script flagged the same combination at `support_agent/agent.py:35`.

**What changed:**
- **`support_agent/agent.py`:** `triage_agent` is now a sequence of two agents, keeping the same name and description so the root's routing is unchanged:
  - `triage_reader` uses `fetch_email` and `search_kb` and writes free-text notes.
  - `triage_formatter` has no tools, so the schema is enforced directly on any backend. It turns the notes into the `Triage` record and saves it under `triage`.
- **`support_agent/triage.py` (new):**
  - `Triage` gains a `status` field ("triaged" or "cannot_triage"), defaulting to "triaged", so existing uses keep working.
  - A guard replaces any invalid, empty or blocked model response with a valid failure record (`status="cannot_triage"`, `category="needs_human"`, `priority=1`). The run no longer raises.
- **`tests/test_triage_contract.py` (new):** tests with a scripted fake model. They check that valid output is saved and that prose or wrong-type JSON becomes the failure record. They also check that the formatter's request carries the schema and no `set_model_response` tool.

**Checks:**
- **Ran:** compile check on all changed files (passed); the model-config audit; the schema checker on the new `Triage` schema (no findings).
- **Not run:** pytest. Both the new tests and the existing `tests/test_tools.py` need `google.adk`. No live model calls.

**Not done:**
- **No real retry:** a bad response becomes the failure record straight away. A genuine retry needs code that owns the agent runner, and the repo doesn't have any.
- **Model and settings unchanged:** the audit flagged `gemini-2.5-pro` as limited availability, but changing it is T-103.
- **Injected email text:** the email text now flows into the formatter's instructions, so injected text reaches it just as it reached the old triage agent. That belongs to the T-104 security review.

**Assumptions to check:**
- The service really uses an API key, as the README says. The split works on Vertex too.
- Priority 1 means most urgent, so failures go to a human quickly. If 1 is lowest, change `cannot_triage()` in `support_agent/triage.py`.
- Adding `status` to `Triage` is acceptable.
- A failure record is acceptable before any retry exists.
- One extra model call per triage is acceptable for cost and latency.

**Friction:** I rated it 4/5. The routing and references pinned down the cause and the fix with no guesswork. The friction was in the helper scripts and the retry gap:
- The audit script crashed under the default Python 3.9 with a bare traceback; I had to find Python 3.12 myself.
- It also scanned `.claude/skills/`, so most of its output was about the skills' own test files.
- The skill gives no recipe for a bounded retry when the project doesn't run the agent itself.

Everything is in `REPORT.md`: the reference files in order, the friction log with file:line pointers, and the questions I'd have asked. The skills never told the user to type a next prompt.