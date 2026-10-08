I've fixed T-105. Prose from the triage step can no longer crash the save, and the tests that don't need ADK pass. The tests that need the ADK SDK are written but not run, and nothing has been tried against a live model.

**Specialist: `adk-model-and-output-contracts`**, because the ticket matches its routing row word for word: "structured output arrives as prose or invalid JSON". I used no supporting skill.

**Cause:** `triage_agent` had both tools and an output schema. The README says you run on the API-key backend. In that setup ADK 2.8.0 doesn't make the model follow the schema; it only adds a `set_model_response` tool and asks the model to use it. When the model answers in prose instead, saving to `output_key` raises. The skill's audit script flagged this at `support_agent/agent.py:35`.

**Fix:**
- **Two steps instead of one:** `triage_agent` is now a `SequentialAgent` with the same name, so routing from the root agent is unchanged.
  - `triage_reader` uses the tools and writes plain-text notes.
  - `triage_formatter` has no tools, so the schema is enforced directly on any backend. It still saves to `"triage"`.
- **Guard:** `guard_triage` runs after the formatter. If the output is invalid JSON, JSON in a code block with extra text around it, or a provider error such as SAFETY, it saves a valid `CANNOT_TRIAGE` record instead of raising.
- **Contract change:** `Triage` (now in `support_agent/triage_contract.py`) gains a `status` field (`TRIAGED` or `CANNOT_TRIAGE`). `category` and `priority` can now be missing. Nothing in the repo reads `state["triage"]`, so check any consumers outside it.
- **Package import:** `support_agent/__init__.py` now loads `root_agent` only when it's asked for. That lets the tests import without ADK installed; before this, `tests/test_tools.py` couldn't even load without it. If ADK's agent loader doesn't accept this, deployment could break — I couldn't verify it here.
- **Tests and ticket:** new `tests/test_triage_contract.py` (no ADK needed) and `tests/test_triage_agent.py` (needs ADK). I added an Evidence section to `tickets/T-105.md` and wrote `REPORT.md`.

**Checks:**
- **pytest:** 11 passed, 1 file skipped. This ran on Python 3.9.13, because that's the only interpreter here with pydantic and pytest; the project needs 3.11 or later.
- **Schema check:** the new `Triage` schema uses only fields Gemini supports.
- **Not run:** the 6 tests in `tests/test_triage_agent.py` need google-adk and pytest-asyncio, which isn't in the dependencies. No live model call or measured comparison was run.

**Gaps and assumptions:**
- **No retry:** the guard only replaces bad output; it can't ask the model again. A real retry has to live in whatever code calls the agent on Cloud Run, which isn't in this repo.
- **Cost:** each triage now makes two model calls instead of one.
- **Assumptions recorded in `REPORT.md`:** that the backend is really the API key, the contract change, the priority scale, the extra call, where a retry should live, checking `order_id` in code, and the lazy-import risk.
- **Left alone:** the model name and temperature settings, since migrating off `gemini-2.5-pro` is ticket T-103.

**Report:** `REPORT.md` has the friction log with file and line pointers. I rated the run 4/5: the specialist choice and diagnosis were quick, but the audit script also scanned `.claude/skills` and needed filtering. Generating the schema assumed the project's dependencies were installed. For item (7), the skills gave no next prompt to type: "none given".