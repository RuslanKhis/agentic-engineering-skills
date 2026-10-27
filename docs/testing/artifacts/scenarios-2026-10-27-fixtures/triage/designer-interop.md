# Triage: designer and interop/release/observability (des1, des2, int1, int2)

Graded rows only. des1's designer-names-google-product-skills and the eight int1/int2 rows with
status agent-error (usage limit) are skipped. des2 was judged before slash commands counted as
loads; its four `/adk-system-designer` runs did follow the skill (each opened
`references/checkpoint.md` or `assets/ticket-template.md`, which only SKILL.md names).

| Scenario | A# | Votes | Class | Evidence | Proposed action |
| --- | --- | --- | --- | --- | --- |
| system-design-review-existing-proposal | A1 | FPP (pass) | c | Split vote on "asking only questions that affect decisions"; assumptions recorded with dependent decisions. | none |
| system-design-review-existing-proposal | A6 | PFF | c | Planned checks for all four cases written; separation from executed evidence implied, not stated. Skill asks for it (evidence labels brief). | none |
| system-design-runtime-and-release-review | A1 | FFF | c | runtime-and-delivery.md:17 "Bound query work and data before materialisation"; agent read that file and still omitted it. | none |
| system-design-runtime-and-release-review | A3 | FFF | c | runtime-and-delivery.md:72 "define slow-consumer/backpressure behavior"; agent only said limits are to be decided. | none |
| system-design-practical-handoff | A5 | FFF | c | implementation-handoff.md:316,340 cover Wayfinder with a source link; agent read the file but gave no source-checked suggestion. | none |
| designer-phase-gate-plan-versus-code | A2 | FFF | c | assets/code-review-prompt.md:30 "CRITICAL (a contract ... is broken)"; agent graded C2 "WARNING (CRITICAL if the cache is live)" after citing the live call site. | none |
| designer-phase-gate-plan-versus-code | A5 | FPP (pass) | c | Split; owed manual item flagged with named-person request. | none |
| designer-production-cost-contract | A4 | FFF | b | Runner evidence limit: the plan the agent wrote is 35,090 chars, FILE_LIMIT is 30,000, so the judge never saw the Later table; it holds "Recurring cost review ... first monthly bill" (line 479) and "Decommission ... dependants and backups included" (486). Judge reason: "the plan is truncated". | Runner: raise FILE_LIMIT or show head and tail of long files; re-judge. Trigger is a bill, not a date: may still fail on "date trigger". |
| designer-checkpoint-settles-the-agenda | A1 | FPF | b | "settling each with the user" needs a person to answer; headless run has none (agent recorded questions and assumptions). plan_status.py also needs a shell; agent named it as not run. | Flag assertion as interactive; grade "settles" as "puts each to the user with a proposed resolution". |
| designer-checkpoint-settles-the-agenda | A2, A4 | FPP, PPF (pass) | c | Split votes on completeness of citing-ticket updates and re-estimates. | none |
| designer-tickets-get-journey-goal-and-lint | A1-A3 | FFF ×3 | b | Prompt says "Turn the ready goals ... into ticket files"; the fixture plan (evals/fixtures/designer-tickets-get-journey-goal-and-lint/docs/plans/claims.md, goals table) marks only G01 and G03 ready (G02 blocked: W1, G04/G05 proposed) and has goal entries only for G01 and G03. Agent wrote exactly those two. The skill (SKILL.md:419-421 "one file per goal of the phase") and the journey-goal rule (implementation-plan-template.md) would apply, but the fixture steers away. check_tickets.py needs a shell (A2, A3). | Fixture: mark G01-G05 ready (or the phase "ready for tickets"), add goal entries for G02, G04, G05, drop W1 as a blocker. Flag the "runs check_tickets.py" parts as shell-dependent. |
| designer-weekly-status-from-plan-evidence | A3 | FFF | b | A1's command (`plan_status.py --weekly`) cannot run without a shell, so the agent computed remaining/projected hours by hand (5-9 h, 13.5-17.5 h vs 6-11, 12-17) and the judge counted them as invented figures. Partly c: the agent should have quoted the tickets' figures or labelled its own as estimates. | Flag A1/A3 as shell-dependent; keep the assertion. Also note this run loaded the built-in `update-config` skill (agent.json), an unrelated catalogue entry. |
| designer-sow-from-plan | A3 | PFP (pass) | c | Split on criteria wording. | none |
| designer-sow-from-plan | A4 | FFF | b | Waits listed with owners and dates; fails only on "runs check_sow.py to exit 0", which needs a shell. | Flag as shell-dependent. |
| observability-agent-runtime-latency-and-alerts | A1 | FFP | c | Precedence is in references/signals-and-schema.md:5-7, which the agent read; it omitted it and set telemetry true in an env file. | none |
| observability-agent-runtime-latency-and-alerts | A2 | FFF | c | Tail-loss caveat is in references/compatibility.md:17 ("documented tail-loss case"); agent did not open compatibility.md. SKILL.md:68 names the request-driven reader only in passing. | none (borderline a: SKILL.md could point to the caveat) |
| observability-agent-runtime-latency-and-alerts | A3 | FFF | b | "runs the offline invocation summary" needs a shell; agent hand-computed it. SLO from a placeholder rather than the saved session's measured baseline is c. | Flag the run step as shell-dependent. |
| observability-agent-runtime-latency-and-alerts | A4 | FFF | c | SKILL.md:13 description and sources.md:65 name both owners; no hand-off written. | none |
| release-coding-agent-capability-diff-gate | A1 | FFF | c | references/ci-eval-gates.md:29 "parse `comparison_status` and `rows`"; agent read it, did not wire shipgate. | none |
| release-coding-agent-capability-diff-gate | A2 | PFP (pass) | c | Split. | none |
| release-coding-agent-capability-diff-gate | A3 | FFF | b | Assertion defect: it says the inspector "exits 3 and lists capability_changes". The script (`inspect_security_surface.py:19` "1 with --compare when any capability changed"; line 1046 `return 3 if ... partial`) and adk-agent-security/references/validation.md:25-31 ("It exits 1 ... Exit 3 means no listed change but an area the inspector could not read") say exit 1. The agent mapped exit 1 to capability change and 3 to partial, which is correct, and was failed for it. | Fix the assertion text to "exits 1 and lists capability_changes (3 means partial)"; re-judge. |
| release-coding-agent-capability-diff-gate | A4 | PFF | c | security validation.md:33 "a `Workflow` graph, whose function nodes it names but does not read, is always unread"; agent noted the Workflow is unread but not the hand review. | none |
| release-coding-agent-capability-diff-gate | A5 | FFF | a | adk-release-engineering never mentions the MCP definition pin: grep for `mcp_tool_inventory`/`fail-on-diff` in skills/adk-release-engineering finds nothing; ci-eval-gates.md:29 describes the capability gate without saying the definition pin stays a separate check. It lives in adk-agent-interoperability/SKILL.md:79 and references/evaluation-across-boundaries.md:21. | Owner: add one line to ci-eval-gates.md:29 keeping `mcp_tool_inventory.py --diff --fail-on-diff` as a separate check. |
| release-model-retirement-and-ci-gate | A1 | FFF | b+c | "Runs the release inventory" needs a shell (b). Judge pin is in SKILL.md:29 and model-migration.md:21; agent read both and did not pin the judge or write a manifest (c). | Flag the run step. |
| release-model-retirement-and-ci-gate | A2 | FFF | c | ci-eval-gates.md:17 "In 2.8.0 and every release through 2.12.0, `adk eval` ... exits 0"; agent read it and said 2.8.0 only. | none |
| release-model-retirement-and-ci-gate | A3 | FFF | c | model-migration.md:3 names both hand-offs; agent read it. | none |
| observability-semconv-drift-and-evaluation-events | A1 | PPF (pass) | c | Split on gcp.vertex.agent.* joins. | none |
| observability-semconv-drift-and-evaluation-events | A2 | FFF | c | references/validation.md:23-28 (Weaver live-check, expected_violations) not opened; agent read the asset and wrote its own script. | none |
| observability-semconv-drift-and-evaluation-events | A3 | FFF | c | Recommended attributes incomplete. | none |
| observability-semconv-drift-and-evaluation-events | A4 | FFF | c | compatibility.md:47 "Status: Development"; not carried into the answer. | none |
| interoperability-consume-enterprise-mcp-server-registration-and-sso | A1 | FFF | c | references/mcp-consumption.md:162-170 gives the priority and DCR "only as a fallback, deprecated in 2026-07-28"; agent read it but only forbade DCR. | none |
| interoperability-consume-enterprise-mcp-server-registration-and-sso | A2 | FFF | c | mcp-consumption.md:176 "the credential index that `adk-tool-auth-and-secrets` keeps"; agent read it, did not load tool-auth. | none |
| interoperability-consume-enterprise-mcp-server-registration-and-sso | A4 | FFF | a | Dropped schema keywords are covered only in adk-tool-interface-design/references/results-and-errors.md:155-161 ("the recorded-definition test"); grep of skills/adk-agent-interoperability for a schema-keyword rule or a link to that file finds nothing. The agent loaded interop only. | Owner: in mcp-consumption.md (2026-07-28 revision notes), say that schema keywords ADK's conversion drops must be checked in the recorded-definition test, linking the tool-interface reference. |
| release-promptfoo-gate-exit-codes-and-trajectory-assertions | A2 | FFF | c | ci-eval-gates.md:37 gives 100 block, 0 pass, 1 NOT RUN and the threshold placeholder; agent read it and invented its own codes. | none |
| release-promptfoo-gate-exit-codes-and-trajectory-assertions | A3 | FFF | c | Same paragraph: repeat-min-pass as at-least-m-of-n, share key. | none |
| release-promptfoo-gate-exit-codes-and-trajectory-assertions | A4 | FFF | c | Primary evidence rule in the same paragraph and provider-compatibility.md:59; not stated. | none |
| interoperability-expose-a2a-with-tck-acceptance | A1 | FFF | b | Judge failed protocolVersion because it sits in `supportedInterfaces`, but that is where the skill's own 1.x example puts it (assets/agent-card-1.0.example.json:4-8) and a2a-contracts.md:20 says 1.x cards have no top-level url. Running agent_card_check.py needs a shell. The manual-check list (a2a-contracts.md:307, 410) is c. | Flag the assertion: say "protocolVersion (top level for 0.3, per interface for 1.x)"; mark the helper run as shell-dependent. |
| interoperability-expose-a2a-with-tck-acceptance | A4 | FFF | c | a2a-contracts.md:247-251 has the origin-pinning rule; agent read the file, omitted it. | none |

## Suspected skill defects

1. **adk-release-engineering**, `references/ci-eval-gates.md:29`: the coding-agent capability gate
   says nothing about keeping the MCP definition pin (`mcp_tool_inventory.py --diff --fail-on-diff`)
   as a separate check; it is only in adk-agent-interoperability (SKILL.md:79,
   evaluation-across-boundaries.md:21) and adk-agent-security validation.md:72.
2. **adk-agent-interoperability**, `references/mcp-consumption.md`: no rule that JSON Schema
   keywords ADK's conversion drops must be checked in the recorded-definition test, and no link to
   adk-tool-interface-design `references/results-and-errors.md:155-161`, where it lives.
3. Borderline: **adk-agent-observability** SKILL.md:68 mentions the Agent Runtime request-driven
   metric reader but not its tail-loss caveat, which sits only in a compatibility table row
   (`references/compatibility.md:17`).

## Fixture or assertion defects

- **Runner evidence truncation** (designer-production-cost-contract A4): FILE_LIMIT 30,000 hides
  the end of long plans; the judge failed content that exists. Raise the limit or give head and
  tail, and re-judge.
- **Assertion contradicts the helper** (release-coding-agent-capability-diff-gate A3): "exits 3"
  should be "exits 1" for capability_changes (3 = partial). Fix the assertion text and re-judge.
- **Fixture steers away from the asserted behaviour** (designer-tickets-get-journey-goal-and-lint):
  only G01 and G03 are ready and only they have goal entries, while the prompt asks for tickets
  for the ready goals and A1-A2 expect a journey goal and one ticket per goal. Make G01-G05 ready
  with full entries and no W1 blocker.
- **Assertion ambiguity** (interoperability-expose-a2a-with-tck-acceptance A1): protocolVersion's
  place differs between 0.3 and 1.x cards; the skill's 1.x example puts it per interface.
- **Interactive** (designer-checkpoint-settles-the-agenda A1): settling items with the user cannot
  happen headless.
- **Shell-dependent parts** (flag, don't loosen): plan_status.py (checkpoint A1, weekly A1/A3),
  check_tickets.py (tickets A2/A3), check_sow.py (sow A4), invocation_summary.py (latency A3),
  inventory_release_refs.py (model retirement A1), agent_card_check.py (TCK A1).

No fixture files were changed.
