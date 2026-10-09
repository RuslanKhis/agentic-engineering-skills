---
goal: G02
title: Ask an HR policy question in adk web and get an answer citing document and page
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-memory-architecture
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-model-and-output-contracts, adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted, x1.5 new-to-ADK applied
  hands_on: 0.5-0.75
  review_and_verify: 0.5-0.75
  total: 1-1.5
  calendar_waits: none
owner: the builder
status: ready
---

# G02 Ask an HR policy question in adk web and get an answer citing document and page

## Outcome

In `adk web` the builder asks "How many days of parental leave do I get?" and
gets a short answer citing document and page. Off-corpus questions get a
fixed "I couldn't find this in the HR policies; please contact HR" reply.
Implements D2, D3, D4, D5 and the spend stop from section 4.

## Scope

- In: `hr_agent/agent.py` exposing `root_agent`, an `LlmAgent` with model from
  `config.py`; one function tool `search_policies(query: str)` wrapping G01's
  `search`, returning `{"status": "ok"|"no_results", "passages": [{doc, page,
  text}]}` with at most 5 passages of at most 1,500 characters each; the
  instruction: answer only from returned passages, cite `(document, p. N)` for
  each claim, use the fixed reply when nothing supports an answer, and run at most
  two searches per question; a `before_model_callback` that ends the turn with a
  short message after 6 model calls in one invocation (`adk web` owns the
  Runner, so a `RunConfig` set elsewhere would not apply there).
- Out: the scripted gold-question run (G03); identity, deployment and logs (phase 2).
- Depth: POC. Floor kept: no write or egress tools; pinned model ID; call cap.

## Acceptance

- [ ] Offline: the tool returns `ok` with ≤ 5 bounded passages for a fixture
      hit and `no_results` for a miss; an oversize page is truncated.
- [ ] Offline: the agent's tools are exactly `[search_policies]`, and its model
      equals `config.MODEL_ID` (`gemini-3.8-flash`).
- [ ] Offline: the callback stops the turn on the 7th model call (scripted model or stubbed context).
- [ ] Live, local `adk web`: one corpus question is answered with a doc+page
      citation that matches the PDF when opened.
- [ ] Live: one off-corpus question ("What is the canteen menu?") gets the fixed reply.

Verification: `pytest tests/test_agent.py` (offline; imports `google.adk`);
`adk web` locally for the two live checks (authorised live, a few calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G02-cited-answer-in-adk-web.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
