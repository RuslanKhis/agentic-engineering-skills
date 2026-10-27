### Re-run of scenarios with (a) rows

| Primary skill | Scenarios run | Assertions passed (majority) | Split votes | Primary SKILL.md loaded |
| --- | --- | --- | --- | --- |
| adk-agent-evaluation | 3 | 2/14 | 2 | 2/3 |
| adk-agent-interoperability | 1 | 3/4 | 1 | 1/1 |
| adk-agent-security | 3 | 8/13 | 0 | 2/3 |
| adk-memory-architecture | 3 | 5/12 | 1 | 3/3 |
| adk-operational-guardrails | 3 | 5/13 | 1 | 3/3 |
| adk-release-engineering | 1 | 2/5 | 1 | 1/1 |
| deploy-adk-on-google-cloud | 1 | 4/4 | 0 | 1/1 |
| protect-adk-sensitive-data | 1 | 4/6 | 0 | 1/1 |
| **All** | 16 | 33/71 (46 %) | 6 | 14/16 |

### Scenarios not run in Phase 9

| Primary skill | Scenarios run | Assertions passed (majority) | Split votes | Primary SKILL.md loaded |
| --- | --- | --- | --- | --- |
| (no primary) | 1 | 2/3 | 0 | 0/1 |
| adk-agent-interoperability | 5 | 6/20 | 3 | 5/5 |
| adk-agent-observability | 1 | 1/4 | 1 | 1/1 |
| adk-engineer | 2 | 3/7 | 1 | 2/2 |
| adk-frontend-integration | 4 | 7/15 | 2 | 4/4 |
| adk-model-and-output-contracts | 1 | 1/4 | 0 | 1/1 |
| adk-portability-planning | 1 | 6/8 | 2 | 1/1 |
| adk-presenter | 2 | 7/9 | 1 | 2/2 |
| adk-release-engineering | 2 | 2/8 | 1 | 1/2 |
| adk-sql-agent-engineering | 3 | 6/12 | 3 | 3/3 |
| adk-workflow-design | 7 | 8/33 | 4 | 2/7 |
| deploy-adk-on-google-cloud | 2 | 3/10 | 4 | 2/2 |
| protect-adk-sensitive-data | 2 | 4/10 | 2 | 2/2 |
| **All** | 33 | 56/143 (39 %) | 24 | 26/33 |

| Scenario | Batch | Primary | Passed | Votes | Split | Primary loaded | Skills loaded | Agent $ | Judge $ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| guardrails-continuation-accounting-and-duplicates | a1 | adk-operational-guardrails | 3/5 | A1:PPP A2:FFF A3:PPP A4:FFF A5:PPP | none | yes | adk-operational-guardrails | 0.35 | 0.18 |
| guardrails-escalation-two-sided-calibration | a1 | adk-operational-guardrails | 1/4 | A1:FFF A2:FFF A3:FFF A4:PPF | A4 | yes | adk-operational-guardrails | 0.22 | 0.08 |
| guardrails-unanswered-approval-and-screening-placement | a1 | adk-operational-guardrails | 1/4 | A1:FFF A2:FFF A3:FFF A4:PPP | none | yes | adk-operational-guardrails | 0.26 | 0.11 |
| privacy-with-observability | a1 | protect-adk-sensitive-data | 4/6 | A1:PPP A2:PPP A3:PPP A4:FFF A5:PPP A6:FFF | none | yes | protect-adk-sensitive-data | 0.20 | 0.10 |
| sensitive-data-local-tool-result-screen-llamafirewall | a1 | adk-agent-security | 4/5 | A1:PPP A2:PPP A3:PPP A4:FFF A5:PPP | none | no | protect-adk-sensitive-data | 0.36 | 0.16 |
| security-refund-agent-build-time-controls-vs-screening | a1 | adk-agent-security | 2/4 | A1:PPP A2:PPP A3:FFF A4:FFF | none | yes | adk-agent-security | 0.40 | 0.16 |
| evaluation-bound-spans-versus-model-paraphrase | a2 | adk-agent-evaluation | 0/5 | A1:FFF A2:FFF A3:FFF A4:FFF A5:FFF | none | no | - | 0.19 | 0.08 |
| evaluation-progressive-downstream-repair | a2 | adk-agent-evaluation | 1/5 | A1:FFF A2:FFF A3:FFF A4:FPF A5:PPP | A4 | yes | adk-agent-evaluation | 0.28 | 0.08 |
| evaluation-collateral-damage-no-op-control | a2 | adk-agent-evaluation | 1/4 | A1:FFP A2:PPP A3:FFF A4:FFF | A1 | yes | adk-agent-evaluation | 0.42 | 0.25 |
| release-coding-agent-capability-diff-gate | a2 | adk-release-engineering | 2/5 | A1:FFF A2:PFF A3:PPP A4:PPP A5:FFF | A2 | yes | adk-release-engineering | 0.28 | 0.09 |
| interoperability-consume-enterprise-mcp-server-registration-and-sso | a2 | adk-agent-interoperability | 3/4 | A1:PPP A2:PPF A3:PPP A4:FFF | A2 | yes | adk-agent-interoperability, adk-tool-auth-and-secrets | 0.34 | 0.11 |
| mcp-rug-pull-runtime-pin-and-mcp-ids | a3 | adk-agent-security | 2/4 | A1:FFF A2:PPP A3:FFF A4:PPP | none | yes | adk-agent-security | 0.36 | 0.13 |
| engineer-agents-cli-focused-memory-1-11 | a3 | adk-memory-architecture | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes | adk-memory-architecture | 0.25 | 0.08 |
| engineer-ticket-creates-cloud-sql | a3 | adk-memory-architecture | 2/4 | A1:FFF A2:PPP A3:PPF A4:FFF | A3 | yes | adk-engineer, adk-memory-architecture | 0.49 | 0.17 |
| memory-write-back-loop-from-horizon | a3 | adk-memory-architecture | 2/4 | A1:FFF A2:PPP A3:FFF A4:PPP | none | yes | adk-memory-architecture | 0.84 | 0.32 |
| web-backend-deploy-routes-to-deploy | a3 | deploy-adk-on-google-cloud | 4/4 | A1:PPP A2:PPP A3:PPP A4:PPP | none | yes | deploy-adk-on-google-cloud | 0.27 | 0.09 |
| interoperability-expose-and-register-a2a | b1 | adk-agent-interoperability | 0/4 | A1:FFF A2:FFF A3:FFF A4:FFF | none | yes | adk-agent-interoperability | 0.34 | 0.13 |
| interoperability-expose-mcp-server-with-conformance-baseline | b1 | adk-agent-interoperability | 0/4 | A1:FFF A2:FFF A3:FFF A4:FFF | none | yes | adk-agent-interoperability | 0.37 | 0.13 |
| interoperability-exposed-agent-forgets-on-modern-clients | b1 | adk-agent-interoperability | 3/4 | A1:PPP A2:PPP A3:PPP A4:FFF | none | yes | adk-agent-interoperability | 0.20 | 0.09 |
| interoperability-mcp-app-widget-to-custom-frontend | b1 | adk-agent-interoperability | 2/4 | A1:PPP A2:FFF A3:FPP A4:PFF | A3, A4 | yes | adk-agent-interoperability | 0.34 | 0.11 |
| interoperability-verify-signed-agent-card | b1 | adk-agent-interoperability | 1/4 | A1:FFP A2:PPP A3:FFF A4:FFF | A1 | yes | adk-agent-interoperability | 0.33 | 0.12 |
| observability-handover-and-postmortem | b1 | adk-agent-observability | 1/4 | A1:FPF A2:PPP A3:FFF A4:FFF | A1 | yes | adk-agent-observability | 0.30 | 0.16 |
| release-bigquery-analytics-score-gate-and-drift | b1 | adk-release-engineering | 1/4 | A1:PPP A2:FFF A3:FFF A4:FFF | none | yes | adk-release-engineering | 0.47 | 0.12 |
| release-post-launch-quality-loop-aqua | b1 | adk-release-engineering | 1/4 | A1:FFF A2:FFF A3:FFF A4:FPP | A4 | no | - | 0.17 | 0.07 |
| engineer-resumes-from-progress-block | b2 | adk-engineer | 2/3 | A1:PPP A2:FFF A3:PFP | A3 | yes | adk-engineer | 0.21 | 0.07 |
| engineer-ticket-with-missing-companion | b2 | adk-engineer | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes | adk-engineer, adk-frontend-integration | 0.40 | 0.05 |
| engineer-agents-cli-deploy-ticket | b2 | deploy-adk-on-google-cloud | 1/5 | A1:PFP A2:FFF A3:FFF A4:FFF A5:FFF | A1 | yes | deploy-adk-on-google-cloud | 0.23 | 0.10 |
| engineer-google-skills-supporting-missing | b2 | deploy-adk-on-google-cloud | 2/5 | A1:PFF A2:FFF A3:PFF A4:PPP A5:FPP | A1, A3, A5 | yes | deploy-adk-on-google-cloud | 0.25 | 0.11 |
| frontend-a2ui-route-and-validation-declared | b2 | adk-frontend-integration | 0/4 | A1:FFF A2:FFF A3:PFF A4:FFF | A3 | yes | adk-frontend-integration | 0.27 | 0.12 |
| frontend-assistant-ui-adk-python-gateway | b2 | adk-frontend-integration | 3/4 | A1:PPP A2:PFP A3:PPP A4:FFF | A2 | yes | adk-frontend-integration | 0.62 | 0.24 |
| frontend-tool-widgets-staged-emission | b2 | adk-frontend-integration | 1/4 | A1:PPP A2:FFF A3:FFF A4:FFF | none | yes | adk-frontend-integration, adk-workflow-design | 0.25 | 0.11 |
| web-backend-stream-progress-routes-to-frontend | b2 | adk-frontend-integration | 3/3 | A1:PPP A2:PPP A3:PPP | none | yes | adk-frontend-integration | 0.27 | 0.13 |
| model-output-schema-with-tools-hardening | b3 | adk-model-and-output-contracts | 1/4 | A1:PPP A2:FFF A3:FFF A4:FFF | none | yes | adk-model-and-output-contracts | 0.25 | 0.12 |
| sensitive-data-model-armor-file-attachments-and-template-update | b3 | protect-adk-sensitive-data | 3/5 | A1:PPP A2:PPP A3:PPP A4:FFF A5:FFF | none | yes | protect-adk-sensitive-data | 0.54 | 0.23 |
| sensitive-data-offline-pii-oracle-in-ci | b3 | protect-adk-sensitive-data | 1/5 | A1:FFF A2:FFF A3:PFF A4:PFF A5:PPP | A3, A4 | yes | protect-adk-sensitive-data | 0.31 | 0.13 |
| sql-acceptance-metric-names-and-spider2-bigquery-probe | b3 | adk-sql-agent-engineering | 3/4 | A1:PPP A2:FFF A3:PPP A4:PFP | A4 | yes | adk-sql-agent-engineering | 0.23 | 0.10 |
| sql-managed-bigquery-mcp-read-only-by-platform | b3 | adk-sql-agent-engineering | 2/4 | A1:PPP A2:PPP A3:FFF A4:FFF | none | yes | adk-sql-agent-engineering, adk-agent-interoperability | 0.38 | 0.10 |
| sql-semantic-map-reviewed-files | b3 | adk-sql-agent-engineering | 1/4 | A1:FFP A2:FFF A3:FFP A4:PPP | A1, A3 | yes | adk-sql-agent-engineering | 0.56 | 0.22 |
| out-of-scope-marketing-edit | b3 | None | 2/3 | A1:PPP A2:PPP A3:FFF | none | no | - | 0.03 | 0.03 |
| plain-adk-no-scaffold | b4 | adk-workflow-design | 3/5 | A1:PPP A2:PPP A3:PPP A4:FFF A5:FFF | none | yes | adk-workflow-design | 0.09 | 0.05 |
| workflow-checkpoint-dependency-invalidation | b4 | adk-workflow-design | 1/5 | A1:FFF A2:FFF A3:FFP A4:PPP A5:FFF | A3 | no | - | 0.61 | 0.16 |
| workflow-content-safeguards-in-code | b6 | adk-workflow-design | 3/5 | A1:PPP A2:PPP A3:FFF A4:FFF A5:PPP | none | no | - | 0.44 | 0.16 |
| workflow-durable-refund-resume-or-engine | b6 | adk-workflow-design | 0/4 | A1:FFF A2:PFF A3:FFF A4:FFF | A2 | no | - | 0.22 | 0.12 |
| workflow-engine-restate-or-dapr-keeps-adk-contract | b6 | adk-workflow-design | 0/5 | A1:FFF A2:FFF A3:FFF A4:FFF A5:FFF | none | yes | adk-workflow-design | 0.75 | 0.28 |
| workflow-realistic-checkpoint-storage-preflight | b6 | adk-workflow-design | 0/5 | A1:FFF A2:FFF A3:FFP A4:FFF A5:FFF | A3 | no | - | 0.22 | 0.12 |
| workflow-warning-only-correction-preservation | b6 | adk-workflow-design | 1/4 | A1:PPP A2:FFF A3:FFP A4:FFF | A3 | no | - | 0.22 | 0.09 |
| portability-ticket-carried-out | b7 | adk-portability-planning | 6/8 | A1:PPP A2:FFF A3:PPP A4:PPP A5:PPP A6:PPP A7:FPF A8:PFP | A7, A8 | yes | adk-portability-planning | 0.58 | 0.21 |
| presenter-poc-review-evidence-only | b7 | adk-presenter | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP | none | yes | adk-presenter | 0.40 | 0.18 |
| presenter-monthly-value-report | b7 | adk-presenter | 2/4 | A1:PPP A2:FFF A3:PFF A4:PPP | A3 | yes | adk-presenter | 0.16 | 0.07 |

Recorded cost: agent $16.51, judge $6.42, total $22.93
