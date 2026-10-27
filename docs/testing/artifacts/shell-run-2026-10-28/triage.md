# Triage of the shell run · 28 October 2026

Every assertion that failed by majority or had split votes in the valid runs (batches s1, s2, r3,
r4, s5, s6, t1; the spoiled s3 and s4 are not triaged). Classes as in Phases 9-11: (a) skill
defect, (b) fixture, assertion or runner defect, (c) run variance (the skill covers it and the
answer left it out, or split votes). Rows marked "spot-checked" were checked by the lead agent
against the workspace, the transcript's shell output and the skill text; the others follow the
judges' reasons and the earlier phases' triage of the same row.

| Scenario | Row | Votes | Class | Reason | Spot-checked |
| --- | --- | --- | --- | --- | --- |
| governance-pack-commonwealth-dta-assessment | A4 | FPP | c | Split pass: W4 names the referral; one judge read the 15 December date as attached to W3 | no |
| governance-pack-auckland-singapore-retailer | A4 | FFF | c | The pack treats the agent's CRM read as outside IPP 3A; `adk-governance-pack/references/new-zealand.md:154` lists "pulls information about people from a CRM" as a trigger | yes |
| presenter-monthly-value-report | A3 | FPP | c | Checker run to exit 0; the agent added "baseline 21 minutes (M1, brief §4)" to the M2 record, which the brief supports (`docs/discovery/claims.md` §4), and disclosed both gaps; one judge read the plan edit as hiding the gap | yes |
| engineer-resumes-from-progress-block | A3 | FPP | c | Split pass: Progress block rewritten rather than removed because G02 is unfinished | no |
| portability-ticket-carried-out | A8 | FFP | b | Two judges failed the G07 status change; the grader note allows only G07's Evidence to change, but `adk-portability-planning/SKILL.md:211` tells the agent to set the ticket's status. The assertion and its grader note disagree with the skill | yes |
| interoperability-verify-signed-agent-card | A1 | FPP | c | Split pass; the answer never says outright that RemoteA2aAgent skips verification on a URL-fetched card (`a2a-contracts.md:348`) | no |
| interoperability-verify-signed-agent-card | A4 | FFF | c | Untrusted card text and the bearer-token hand-off are in `a2a-contracts.md:384-385, :424`; the answer omits both (as in Phase 10) | no |
| interoperability-expose-mcp-server-with-conformance-baseline | A1 | FFF | c | With a shell the inventory helper could run; the agent read `mcp-exposure.md` (which names `mcp_tool_inventory.py`, :149) and neither ran nor named it | yes (commands) |
| interoperability-expose-mcp-server-with-conformance-baseline | A2 | FFF | c | Baseline entries without fixture-dependent scenarios and reasons | no |
| interoperability-expose-mcp-server-with-conformance-baseline | A3 | FPP | c | Split pass on wording (exit 1, shrinking baseline) | no |
| interoperability-expose-mcp-server-with-conformance-baseline | A4 | FFF | c | Approval gate not recorded as unsatisfiable by an MCP host | no |
| engineer-ticket-with-missing-companion | A1 | FFF | b | Runner: the agent read `adk-frontend-integration/SKILL.md` with `cd web; ...; cat .claude/skills/...`, which the parser did not count, and read lines 1-60 of `composition.md` (the companion rows are :40-41). Fixed in `05fd0e5`; re-judged on the same evidence: PPP | yes (re-judged) |
| engineer-ticket-with-missing-companion | A3 | FFF | b | The checks ran (`check_theme.py`: no theme tokens; lint impossible without `node_modules`). The theming the assertion requires is mapped "with the `shadcn` companion's DESIGN.md workflow" (`frontend-quality.md`, house theme), and `composition.md:41` says a missing companion is a setup step, not applied guidance; the agent followed both. The assertion contradicts the skills | yes |
| engineer-ticket-with-missing-companion | A4 | FFF | c | SB10 and C3 lines carry no tier ("none yet") | no |
| workflow-checkpoint-dependency-invalidation | A1 | FFF | c | Producer code and owner not in the dependency identity; `checkpoint-reuse.md:20-29` covers it (as in Phase 11) | no |
| workflow-checkpoint-dependency-invalidation | A2 | FFF | c | No per-dependency mutation tests for schema, code or projection (`checkpoint-reuse.md:54-63`) | no |
| workflow-checkpoint-dependency-invalidation | A3 | FPP | c | Split pass; frame, invocation and image changes not covered | no |
| workflow-checkpoint-dependency-invalidation | A5 | PFP | c | Split pass; the tests ran (12 OK) | yes (output) |
| designer-tickets-get-journey-goal-and-lint | A1 | FFF | b | Phase 9: the fixture plan marks only G01 and G03 ready and has no journey goal to promote, so the request steers away from the assertion | no (Phase 9 row) |
| designer-tickets-get-journey-goal-and-lint | A2 | FFF | b | Same steering: one ticket per ready goal was written (G01, G03); `check_tickets.py` was run from the root | no (Phase 9 row) |
| designer-tickets-get-journey-goal-and-lint | A3 | FFF | b | New: the four errors left are "skill '...' is not an installed skill" for protect-adk-sensitive-data, adk-model-and-output-contracts, adk-fastapi-backend and adk-tool-auth-and-secrets, which the fixture plan names and the scenario does not install; no ticket edit can clear them | yes |
| evaluation-underwriter-labelling-session | A1 | FFF | c | No decision-maker named; `expert-review.md` and SKILL.md say name one (Phase 9 row) | no |
| tool-interface-wrong-tool-diagnosis | A1 | FFF | b | The linter ran; the live declaration dump needs google-adk, which the fixture does not install and the run may not install; no escape for the SDK half | yes |
| tool-interface-wrong-tool-diagnosis | A3 | FFF | c | No scripted-model Runner test written (SKILL.md:102) | no |
| tool-interface-wrong-tool-diagnosis | A4 | FFF | c | Retry and idempotency hand-off to safe-api-tool-calls not stated | no |

| Class | Rows |
| --- | --- |
| (a) skill defect | 0 |
| (b) fixture, assertion or runner defect | 7 |
| (c) run variance | 18 |
| All | 25 |
