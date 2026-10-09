---
goal: G02
title: Asking a runbook question returns the steps with links to the source Confluence pages, or "no runbook found"
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-instructions, adk-agent-evaluation]
blocked_by: [G01, "A4: list of runbook spaces", "read-only Atlassian bot token"]
phase: 1
profile: internal tool
estimate: 8-11 h
status: blocked
---

# G02 Cited runbook search from real Confluence

## Outcome

A helpdesk agent asks "VPN client says certificate expired" and gets the
runbook steps with links to the pages they came from; when nothing matches,
the assistant says so instead of guessing. Implements D2, D3, I2, I3.

## Scope

- In: `search_runbooks(query)` function tool in `confluence.py`; CQL built in
  code from an allowlist of spaces, excluding label `restricted`; top 5
  results, excerpt ≤ 1,500 characters, title, URL, last-modified; result dict
  with `status` and actionable errors. Token from Secret Manager (env var when
  local). Instruction: answer only from tool results, cite URLs, otherwise
  "no runbook found". 15–20 labelled questions with expected pages in
  `eval/regression.yaml`.
- Out: semantic index (Later), per-user Confluence permissions (Later), ticket
  drafts (G04).
- Depth: internal-tool build for retrieval with a small regression set;
  read-only shared credential (A4). Verify the Confluence Cloud search
  endpoint and fields against current Atlassian docs before coding (not
  verified during design).

## Acceptance

- [ ] Regression set: expected page in top 5 for ≥ 80% of questions
      (provisional target); every cited URL is among that turn's tool results.
- [ ] Confluence down or token missing: tool returns `status: error`, the
      agent says search is unavailable, and invents no answer.
- [ ] Model-supplied text such as `x" OR space = HR` is quoted into the text
      search and never changes the space filter; no page outside the
      allowlist or labelled `restricted` is returned.

Verification: offline `pytest tests/test_confluence.py` with recorded JSON
fixtures; local integration: regression run against the real Confluence spaces
(read-only).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-cited-runbook-search.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
