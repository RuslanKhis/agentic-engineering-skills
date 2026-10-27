# Triage: security (sec1, sec2) and memory (mem1, mem2)

All 22 scenarios were graded with three judge repeats. 50 rows: assertions that failed by majority, plus passes with split votes. Classes: (a) skill defect, (b) fixture or assertion defect, (c) run variance. Paths are under `skills/` unless stated. "Read" means the agent opened the file (agent.json `skill_files_read`).

| Scenario | A# | Votes | Class | Evidence | Proposed action |
| --- | --- | --- | --- | --- | --- |
| security-review-untrusted-content-with-write-tools | A2 | FFF | c | SKILL.md:98, mode (f): "Use all references". The agent read only adversarial-testing.md and operating-rules.md. The 2.8.0 fencing fact is in compatibility.md (SKILL.md:47). | none |
| security-review-untrusted-content-with-write-tools | A3 | FFF | c | Mode (e), SKILL.md:97, asks for "deterministic scripted-model Runner assertions". The agent wrote direct tool calls. The fixture has no Runner harness, and the context promises none. | none |
| security-review-untrusted-content-with-write-tools | A4 | FFF | c | SKILL.md:98 asks for "the OWASP LLM or ASI identifier ... and the owning skill". The agent named no owner per finding. | none |
| security-code-execution-environment-selection | A2 | FFF | c | agency-and-output.md:193 (read) covers it: "Beside the code executors, which run one code string ... Tier an environment like a write tool". | none |
| security-code-execution-environment-selection | A3 | FFF | c | 169.254.169.254 egress tests are covered in agency-and-output.md (read). The agent wrote a domain allow-list test instead. | none |
| security-refund-agent-build-time-controls-vs-screening | A1 | FFF | a | Preview status and "Verdicts may not be accurate" are in agency-and-output.md:322-331 ("Screening is a layer"). The SKILL.md:96 row (d) never names that section. The agent read no reference. | Add screening, aggregate bounds and signed writes to row (d) and link SKILL.md:130 to it |
| security-refund-agent-build-time-controls-vs-screening | A3 | FFF | a | Signed writes ("writes signed by a key the model never holds", agency-and-output.md:341-343) are reachable only through the same unlinked section. | Same |
| security-refund-agent-build-time-controls-vs-screening | A4 | FFF | a | The simulated anomaly detection and the aggregate bound appear in agency-and-output.md:332-338 only. The deterministic A2A policy service appears in threat-model.md only. No route from SKILL.md. | Same |
| security-adversarial-suite-ported-goal-classes | A1 | FPF | c | Split votes. adversarial-testing.md and the asset (both read) name all four classes. Two classes and the origin attribution were missed. | none |
| security-adversarial-suite-ported-goal-classes | A2 | FFF | c | situation.md plants the gate gaps (delete_mail, create_event, aggregate). The agent saw them and skipped those cases. The skill's gate guidance was available. | none (watch: the prompt asks only to extend tests) |
| security-adversarial-suite-ported-goal-classes | A3 | FFF | c | adversarial-testing.md (read) has the "pipeline element" and attack-success-rate route. It was mentioned only in passing. | none |
| security-red-team-a2a-exposed-agent-with-pyrit | A2 | FFF | c | protocol_version, agent_card_path and A2ATarget are in adversarial-testing.md (read). The agent described a plan but wrote no config. | none |
| security-red-team-a2a-exposed-agent-with-pyrit | A4 | FFF | c | ASI07 fake-peer is in adversarial-testing.md (read). The agent chose not to write it and mislabelled the evidence tier. | none |
| security-garak-ci-gate-on-adk-runner | A3 | FFF | c | agent_breaker and the toolkit-table mapping are in adversarial-testing.md (read). | none |
| security-garak-ci-gate-on-adk-runner | A4 | FFF | c | The sentry-sdk gap, telemetry opt-out and ASI_0n normalisation are in adversarial-testing.md (read). deepteam was not implemented. | none |
| sensitive-data-local-tool-result-screen-llamafirewall | A1 | FFF | a | Primary protect-adk-sensitive-data has nothing on PromptGuard (grep "Prompt Guard\|PromptGuard\|512" over the package: none). The 512-token chunking is only in adk-agent-security/references/agency-and-output.md:287-293, and the primary has no pointer to it. | Add a PromptGuard paragraph or cross-link in protect-adk-sensitive-data/references/boundaries.md beside the AlignmentCheck text (:108-125) |
| sensitive-data-local-tool-result-screen-llamafirewall | A2 | FFF | a | "scan_async() returns a successful ALLOW ..." is only in adk-agent-security agency-and-output.md:296-298, which was not read. | Same |
| sensitive-data-local-tool-result-screen-llamafirewall | A3 | FPP | c | Passed 2/3. boundaries.md:110-113 (read) covers Together AI and the static key. One vote failed on the key detail. | none |
| sensitive-data-local-tool-result-screen-llamafirewall | A4 | FFF | c | The tests cover screening on only. The on/off contrast is an agent omission, not a missing fact. | none |
| sensitive-data-local-tool-result-screen-llamafirewall | A5 | FFF | a | The Llama 4 Community License note is only in adk-agent-security agency-and-output.md:315-318, and the primary does not mention it. | Same |
| security-gate-default-deny-and-call-provenance | A1 | FFF | c | injection-patterns.md:93-107 and :156 (read) say "Deny by default. Keep an explicit read-only set and one policy per write". | none |
| security-gate-default-deny-and-call-provenance | A2 | FFF | c | injection-patterns.md:134-140 (read) say "an approximation of CaMeL ... steered by a document". | none |
| security-gate-default-deny-and-call-provenance | A3 | FFF | c | Readers rule at :161 and CaMeL arXiv 2503.18813 at :5 are in the read file. | none |
| security-gate-default-deny-and-call-provenance | A4 | FFF | c | Mode (e) requires scripted-model Runner tests. The agent wrote stdlib unit tests and reported them not run. | none |
| security-adopt-third-party-mcp-server-with-scan | A1 | FFF | c | tool-supply-chain.md:82,106 (read): "uvx snyk-agent-scan@0.6.9 scan --ci". | none |
| security-adopt-third-party-mcp-server-with-scan | A3 | FFF | c | tool-supply-chain.md:86 (read) covers inspect: "lists tools, prompts, resources and skills locally". | none |
| security-adopt-third-party-mcp-server-with-scan | A4 | PFF | c | Split votes. "Not run" is stated in the answer but not in the checklist. | none |
| mcp-rug-pull-runtime-pin-and-mcp-ids | A1 | FFF | a | The security reference (tool-supply-chain.md:41-44) never says ADK does not subscribe to `notifications/tools/list_changed`, or what ttl=None does. That is only in adk-agent-interoperability/references/mcp-consumption.md:134-140. The agent said "TTL unknown". | Add one sentence plus a cross-link in tool-supply-chain.md "Pin by hash" (low severity) |
| mcp-rug-pull-runtime-pin-and-mcp-ids | A3 | FFF | c | threat-model.md:162-174 (read) cover the link rule, MCP06 drift and the MCP03 mapping. | none |
| security-review-with-atlas-and-cosai-ids | A1 | FFF | c | threat-model.md:130 (read): "put that identifier beside the OWASP one rather than translating". The agent dropped OWASP because of the user's "not OWASP". | none |
| security-review-with-atlas-and-cosai-ids | A3 | PFP | c | Split votes, passed. | none |
| security-review-with-atlas-and-cosai-ids | A4 | FPP | c | Split votes, passed. | none |
| memory-local-document-completeness | A3 | FFF | c | local-document-coverage.md:78-90 (read), "Govern the visual branch", gives the path. The agent emitted only a generic label. | none |
| memory-third-party-service-silent-empty-and-supersede | A4 | FPF | c | Split votes, a judgement call on the telemetry setdefault and "live calls not run" wording. | none |
| engineer-agents-cli-focused-memory-1-11 | A1 | FFF | b | Requires consulting google-agents-cli-adk-code, which is not in this repository, so the run cannot install it. There is no "or says it is unavailable" escape, and the agent did not say so either. | Flag: the assertion needs an uninstallable skill; accept "reports it unavailable" or mark the scenario partial |
| engineer-agents-cli-focused-memory-1-11 | A3 | FFF | a | Memory SKILL.md:146-152 asks for tests after "a real invocation" but never says what to do when the SDK is absent: write scripted-model Runner tests and report them not run. That rule is only in adk-engineer SKILL.md. The agent used SimpleNamespace stubs. | Add the SDK-absent rule to memory SKILL.md "Validate and report" |
| engineer-agents-cli-focused-memory-1-11 | A4 | FFF | c | The agent edited the accepted spec. adk-engineer composition.md says to preserve it, but the agent did not load adk-engineer (the prompt has no slash command). | none |
| engineer-ticket-creates-cloud-sql | A1 | FFF | b | "tests it at least by a dry run" needs a shell. There is no "or reports it not run" escape. The script itself was written correctly. | Flag the assertion for shell-less runs |
| engineer-ticket-creates-cloud-sql | A3 | FFF | a | Backups and PITR outliving the instance are only in adk-system-designer/references/resource-costs.md:42-45, which is not installed for this scenario. adk-engineer ticket-lifecycle.md:34-50 ("Resources that charge") and memory sessions-state.md:119 (AlloyDB only) are silent. | Add the backup and retention line to ticket-lifecycle.md "Resources that charge" |
| engineer-ticket-creates-cloud-sql | A4 | FFF | c | ticket-lifecycle.md:46-49 (read): "the billing report show the resources gone". The agent named only the instance-list check. No SKILL.md was loaded (skills_loaded []). | none |
| memory-write-back-loop-from-horizon | A1 | FFF | c | memory-bank.md:73 (read): "throttled per session (120 s cooldown". The flush was not throttled. | none |
| memory-write-back-loop-from-horizon | A3 | FFF | c | The skill routes exact settings to a profile record (SKILL.md, D1-style guidance). The agent stored units and language in semantic memory. | none |
| memory-write-back-loop-from-horizon | A4 | FFF | a | Same gap as 1-11 A3: there is no SDK-absent scripted-model Runner instruction in the memory skill. | Same as 1-11 A3 |
| memory-poisoned-fact-rollback-and-update-cases | A1 | FPF | c | memory-bank.md:93-96 (read) covers consolidation, "duplicative...". Split votes. | none |
| memory-poisoned-fact-rollback-and-update-cases | A3 | FFF | b | "measured before and after" needs running the gold set, which needs a shell, and there is no escape. The cases were added. | Flag the assertion for shell-less runs |
| memory-document-shape-and-source-coordinates | A1 | FFP | b | The prompt asks only to "work out whether we're cutting up or losing parts". Memory SKILL.md:35-36 says "implementation waits for its own request", and the agent diagnosed correctly (final.md). The assertion demands the identities be kept, i.e. code changed. | Flag: the prompt is diagnosis-only while A1/A2/A4/A5 need a fix; reword the prompt to ask for the fix, or accept a diagnosis with remedies |
| memory-document-shape-and-source-coordinates | A2 | FFP | b | Same mismatch. The adjacency versus pack-order diagnosis was made. | Same |
| memory-document-shape-and-source-coordinates | A3 | PFF | c | Split votes. local-document-coverage.md:74 covers the reviewer point, but the agent read no reference (SKILL.md:87-89 routes local PDFs there). | none |
| memory-document-shape-and-source-coordinates | A4 | FFF | b | An actual-sized storage and reopen test needs execution (a shell), and the prompt does not ask for a fix. | Same flag |
| memory-document-shape-and-source-coordinates | A5 | FFF | b | "Changes the earliest affected producer" contradicts the diagnosis-only prompt and SKILL.md:35-36. | Same flag |

Counts: (a) 10, (b) 7, (c) 33.

## Suspected skill defects

- **adk-agent-security, SKILL.md:96 (mode d) and :130.** The "Screening is a layer" section (references/agency-and-output.md:250-345) is not routed from SKILL.md. It holds the Semantic Governance Preview caveat, the aggregate bound keyed on the order, signed writes and the simulated anomaly detection. An agent hardening a refund agent against screening read no reference at all. Affects security-refund A1, A3, A4.
- **protect-adk-sensitive-data, references/boundaries.md:108-125.** It covers AlignmentCheck but nothing on PromptGuard: 512-token chunking, `scan_async` returning ALLOW on error, the Llama 4 Community License on the weights. Those facts live only in adk-agent-security/references/agency-and-output.md:287-318, with no cross-link from the primary. Affects llamafirewall A1, A2, A5.
- **adk-memory-architecture, SKILL.md:146-152.** There is no rule for the SDK-absent case: write scripted-model Runner tests of stored effects and report them not run. Agents fell back to SimpleNamespace stubs. Affects 1-11 A3 and horizon A4.
- **adk-engineer, references/ticket-lifecycle.md:34-50 ("Resources that charge").** It does not say that Cloud SQL backups and PITR retention outlive the instance and must be checked at teardown. That fact sits only in the designer's resource-costs.md:42-45, which is not installed in this scenario. Affects cloud-sql A3.
- **adk-agent-security, references/tool-supply-chain.md:41-44 (low severity).** It does not state that `McpToolset` never subscribes to `notifications/tools/list_changed` or that ttl=None re-lists on every call. That is only in adk-agent-interoperability/references/mcp-consumption.md:134-140. Affects rug-pull A1.

## Fixture or assertion defects

- **memory-document-shape-and-source-coordinates A1, A2, A4, A5.** The prompt asks for a diagnosis, while the assertions require code changes and an executed storage round trip. The skill (SKILL.md:35-36) rightly stops at gaps with remedies. Fix: reword the prompt to ask for the repair ("...and fix it") or flag these assertions. Do not loosen them.
- **engineer-agents-cli-focused-memory-1-11 A1.** It requires consulting google-agents-cli-adk-code, which is not in this repository. Fix: flag it. The fair version credits "names it as unavailable and proceeds"; alternatively mark the scenario as needing external skills.
- **engineer-ticket-creates-cloud-sql A1 and memory-poisoned-fact-rollback-and-update-cases A3.** "tests it by a dry run" and "measured before and after" need a shell, which default confinement removes. Fix: flag them as shell-dependent, so a Bash-enabled run grades them and a shell-less run records them as not gradeable.
- **No fixture files were changed.** security-review-untrusted-content-with-write-tools has no Runner harness, but its context does not promise one; it is noted, not changed.
