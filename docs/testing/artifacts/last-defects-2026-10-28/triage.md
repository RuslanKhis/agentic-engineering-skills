# Triage: Phase 11 scenario runs (c1-c4)

Every assertion that failed by majority or passed on split votes, 36 rows
over 12 scenarios, classified as in Phases 9 and 10: (a) skill defect, (b)
fixture or assertion defect, (c) run variance (the skill covers it, usually
in a reference the agent opened, and the answer left it out; or split votes).
Classified by the lead agent from the judges' reasons, the agent records
(`skill_files_read`) and the skill text; paths are under `skills/`.

| Scenario | A# | Votes | Class | Evidence (file:line) | Proposed action |
| --- | --- | --- | --- | --- | --- |
| workflow-checkpoint-dependency-invalidation | 1-3 | FFF ×3 | c | Agent read adk-workflow-design/references/checkpoint-reuse.md, which covers full dependency identity, descendant invalidation and stale reviews (:20-29, :54-63, :106-107); the answer covered source/prompt/model changes only | none |
| same | 4 | FPP | c | split pass | none |
| same | 5 | PFF | c | The new no-shell escape worked (one judge credits "reported as not run"); the two FAILs are on coverage (two boundary effects tested), not on running | none |
| workflow-engine-restate-or-dapr-keeps-adk-contract | 1, 2, 3, 5 | FFF ×4 | c | Agent read runtime.md; :113-140 states run_typed for tool bodies, the LlmAgent-root rule, the callback short-circuit and max_llm_calls; :145-170 the engine licences and pins | none |
| same | 4 | FPF | c | The answer rejected Dapr outright instead of naming the licence as an owner decision; runtime.md:165-167 frames it as a licence condition (Phase 10 suggested the assertion also accept a licence-based rejection) | optional: accept "rejects Dapr on its licence" |
| workflow-realistic-checkpoint-storage-preflight | 1-4 | FFF ×4 | a | The skill loaded but no reference was read: SKILL.md's mode table routes "saved-stage continuation or changed dependencies" to checkpoint-reuse.md, but nothing routes a checkpoint that fails its store's size limit there, though checkpoint-reuse.md:85-96, :110 covers below/at/above-limit envelopes and failure before dispatch. A1's Runner reproduction also needs a shell (b half) | add the storage limit to the checkpoint-reuse row of the mode table |
| same | 5 | PFP | c | split pass | none |
| workflow-warning-only-correction-preservation | 2, 4 | FFF ×2 | c | Agent read review-contracts.md; :109-114 says a writer revision invalidates its review and binds review-only repair to the current draft | none |
| same | 3 | FFP | c | review-contracts.md:110-112 (retain unresolved findings); answer carried the old review forward | none |
| workflow-content-safeguards-in-code | 3, 4 | FFF ×2 | c | Agent read content-safeguards.md; :21-33 delimiting and imperative labels, :98-111 abstention and the strongest objection; the answer left both undone (same rows as Phase 10) | none |
| workflow-durable-refund-resume-or-engine | 1, 3, 4 | FFF ×3 | c | Agent read runtime.md; :62-75 (resume runs tools at least once, unsupported from adk web or the CLI), :175-185 (kill-after-the-write in both positions, pinning); the answer chose resume and wrote one kill position | none |
| guardrails-unanswered-approval-and-screening-placement | 1, 2 | FFF ×2 | c | adk-operational-guardrails loaded but human-review.md not read; :151-153 "Unanswered approvals and unreadable arguments" covers both. Third run in a row that misses it | optional: name unanswered approvals and unreadable arguments in SKILL.md's human-review row |
| same | 3 | FFF | c | protect-adk-sensitive-data now installed and loaded; the agent read boundaries.md, whose "Where a screen runs" (:182-210) gives the rule; the screen stayed in a non-blocking callback | none |
| governance-pack-annex-iii-pilot | 2 | FFP | c | split; eu-ai-act.md:120-136 says to write the Article 6(3) facts and leave the call to counsel; the draft proposed high-risk with "counsel: confirm" | none |
| same | 6 | FFF | b | check_governance.py needs a shell; the agent named the command with the three sources; the assertion has no "reported not run" escape (situation.md credits naming it, judges graded the run literally) | add the escape to the assertion text |
| governance-pack-au-hr-internal | 6 | FFF | b | as annex A6 | as annex A6 |
| governance-pack-uk-bank-chatbot | 3 | PFF | c | privacy-and-records.md:23, :181 cite SCHUFA; the EU sections did not | none |
| same | 4 | PPF | c | split pass | none |
| same | 5 | FFF | b | counsel_required: yes is set (the first half passes); the checker half needs a shell | add the escape to the assertion text |
| governance-pack-us-hiring-screener | 6 | FFF | b | as annex A6 | as annex A6 |
| presenter-rollout-pack-go-live | 2 | FFF | c | rollout-and-adoption.md:42, :215 (every will, won't and hands-over statement cites a contract); one announcement figure and one hands-over line went uncited | none |
| same | 3 | FFF | c | rollout-and-adoption.md:113-117 gives Article 50(1) and its 2 August 2026 date; the disclosure section omitted both | none |
| same | 4 | PPF | c | split pass; the answer reported check_rollout.py as not run | none |

Counts: (a) 4, (b) 4, (c) 28.

Spot-checks by the lead agent: the storage-preflight agent's
`skill_files_read` is empty and `grep -i storage` finds nothing in the mode
table of adk-workflow-design/SKILL.md; human-review.md:151-153 holds the
unanswered-approval and unreadable-argument rules; privacy-and-records.md
names SCHUFA at :23 and :181; runtime.md:62-75 and :113-140 hold the facts
the durable and Restate rows were failed for.
