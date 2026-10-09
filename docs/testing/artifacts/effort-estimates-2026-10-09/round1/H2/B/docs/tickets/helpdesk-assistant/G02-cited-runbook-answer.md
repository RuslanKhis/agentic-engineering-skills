---
goal: G02
title: An engineer asks a question and gets cited runbook steps, or "no runbook found"
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-agent-evaluation, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate: 6-8 h
status: ready
---

# G02 An engineer asks a question and gets cited runbook steps, or "no runbook found"

## Outcome

Locally, "VPN client fails with error 809 on Windows 11" returns the fix with
links to the Confluence pages used. Implements D1, D2, D5, D7 and invariants
I2, I3, I6. The live check waits on G01; offline work does not.

## Scope

- In: `helpdesk_assistant/agent.py`, `prompts/runbook_assistant.md`,
  `tools/confluence.py` (`search_runbooks`, `get_runbook`), fake Confluence
  client, scripted-model Runner tests, `evals/regression.evalset.json` with
  ~15 real helpdesk questions supplied by the helpdesk lead.
- Out: hosting and auth (G03), tickets (G04), semantic index (later).
- Depth: internal tool. Floor: pinned model ID, `RunConfig(max_llm_calls=8)`,
  token from environment or Secret Manager, no runbook text in logs,
  credential-pattern masking on page text. SDP screening is G08.

## Acceptance

- [ ] Scripted model searches, fetches, and answers with a URL that came from
      the returned hits.
- [ ] Empty search → answer says no runbook was found; no invented steps.
- [ ] Model-supplied CQL operators are escaped; every captured Confluence
      request carries the configured space filter.
- [ ] `get_runbook` refuses a page ID that no search in this session returned.
- [ ] Page text over 8k characters is truncated and flagged `truncated: true`;
      search returns at most 5 hits.
- [ ] A looping scripted model stops at 8 model calls with a clear message.
- [ ] Live (after G01): at least 12 of 15 regression cases cite a correct page
      (provisional threshold).

Verification: `pytest tests/` offline; one bounded `adk eval` run of the
regression set against the pinned model (authorised live, ~15 cases × 1).
Tests importing `google.adk` need the pinned dependencies installed.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-cited-runbook-answer.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
