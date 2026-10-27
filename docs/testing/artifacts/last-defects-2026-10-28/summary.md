# Scenario results, Phase 11 · 28 October 2026

Batches: c1 the seven adk-workflow-design scenarios; c2 the guardrails
placement scenario; c3 four of the eight governance packs (the batch was
stopped after its fourth agent for the cost cap, its manifest cut to those
four and they were judged with `judge --run-dir`; `c3-manifest.json` is the
cut manifest); c4 presenter-rollout-pack-go-live. Votes are the three judge
verdicts per assertion, in order. "Skills loaded" lists the skills whose
SKILL.md was loaded (Skill tool, a read of the file or a leading slash
command).

| Scenario | Batch | Primary | Passed | Votes | Split | Primary loaded | Skills loaded | Agent $ | Judge $ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| workflow-checkpoint-dependency-invalidation | c1 | adk-workflow-design | 1/5 | A1:FFF A2:FFF A3:FFF A4:FPP A5:PFF | A4, A5 | yes | adk-workflow-design | 0.72 | 0.16 |
| workflow-engine-restate-or-dapr-keeps-adk-contract | c1 | adk-workflow-design | 0/5 | A1:FFF A2:FFF A3:FFF A4:FPF A5:FFF | A4 | yes | adk-workflow-design | 0.94 | 0.32 |
| workflow-realistic-checkpoint-storage-preflight | c1 | adk-workflow-design | 1/5 | A1:FFF A2:FFF A3:FFF A4:FFF A5:PFP | A5 | yes | adk-workflow-design | 0.26 | 0.15 |
| workflow-warning-only-correction-preservation | c1 | adk-workflow-design | 1/4 | A1:PPP A2:FFF A3:FFP A4:FFF | A3 | yes | adk-workflow-design | 0.28 | 0.10 |
| plain-adk-no-scaffold | c1 | adk-workflow-design | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP | none | yes | adk-workflow-design | 0.16 | 0.08 |
| workflow-content-safeguards-in-code | c1 | adk-workflow-design | 3/5 | A1:PPP A2:PPP A3:FFF A4:FFF A5:PPP | none | yes | adk-workflow-design | 0.49 | 0.19 |
| workflow-durable-refund-resume-or-engine | c1 | adk-workflow-design | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes | adk-workflow-design | 0.60 | 0.05 |
| guardrails-unanswered-approval-and-screening-placement | c2 | adk-operational-guardrails | 1/4 | A1:FFF A2:FFF A3:FFF A4:PPP | none | yes | adk-operational-guardrails, protect-adk-sensitive-data | 0.33 | 0.11 |
| governance-pack-annex-iii-pilot | c3 | adk-governance-pack | 4/6 | A1:PPP A2:FFP A3:PPP A4:PPP A5:PPP A6:FFF | A2 | yes | adk-governance-pack | 1.23 | 0.46 |
| governance-pack-au-hr-internal | c3 | adk-governance-pack | 5/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:FFF | none | yes | adk-governance-pack | 0.80 | 0.32 |
| governance-pack-uk-bank-chatbot | c3 | adk-governance-pack | 3/5 | A1:PPP A2:PPP A3:PFF A4:PPF A5:FFF | A3, A4 | yes | adk-governance-pack | 1.57 | 0.48 |
| governance-pack-us-hiring-screener | c3 | adk-governance-pack | 5/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:FFF | none | yes | adk-governance-pack | 1.15 | 0.38 |
| presenter-rollout-pack-go-live | c4 | adk-presenter | 2/4 | A1:PPP A2:FFF A3:FFF A4:PPF | A4 | yes | adk-presenter | 0.24 | 0.14 |

| Primary skill | Scenarios run | Assertions passed (majority) | Split votes | Primary SKILL.md loaded |
| --- | --- | --- | --- | --- |
| adk-governance-pack | 4 | 17/23 | 3 | 4/4 |
| adk-operational-guardrails | 1 | 1/4 | 0 | 1/1 |
| adk-presenter | 1 | 2/4 | 1 | 1/1 |
| adk-workflow-design | 7 | 12/33 | 5 | 7/7 |
| **All** | 13 | 32/64 (50 %) | 9 | 13/13 |

Recorded cost: agent $8.77, judge $2.94, total $11.70.
