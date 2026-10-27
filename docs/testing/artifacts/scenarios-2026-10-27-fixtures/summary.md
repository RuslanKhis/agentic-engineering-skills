| Primary skill | Scenarios run | Assertions passed (majority) | Unstable | Primary SKILL.md loaded |
| --- | --- | --- | --- | --- |
| adk-agent-evaluation | 16 | 33/72 | 9 | 11/16 |
| adk-agent-instructions | 1 | 1/4 | 0 | 1/1 |
| adk-agent-interoperability | 2 | 3/8 | 0 | 2/2 |
| adk-agent-observability | 3 | 6/13 | 2 | 3/3 |
| adk-agent-security | 11 | 16/45 | 5 | 10/11 |
| adk-engineer | 8 | 20/29 | 5 | 7/8 |
| adk-fastapi-backend | 1 | 1/4 | 0 | 1/1 |
| adk-frontend-integration | 1 | 0/4 | 1 | 1/1 |
| adk-memory-architecture | 11 | 29/47 | 5 | 10/11 |
| adk-operational-guardrails | 3 | 5/13 | 0 | 1/3 |
| adk-release-engineering | 3 | 4/13 | 1 | 3/3 |
| adk-sql-agent-engineering | 1 | 2/4 | 1 | 1/1 |
| adk-system-designer | 11 | 40/53 | 8 | 11/11 |
| adk-tool-interface-design | 1 | 1/4 | 0 | 1/1 |
| deploy-adk-on-google-cloud | 1 | 3/4 | 0 | 1/1 |
| optimise-adk-on-google-cloud | 1 | 2/4 | 0 | 1/1 |
| protect-adk-sensitive-data | 1 | 2/6 | 1 | 0/1 |
| safe-api-tool-calls | 1 | 2/6 | 1 | 0/1 |
| **All** | 77 | 170/333 | 39 | 65/77 |

| Scenario | Primary | Passed | Votes | Unstable | Primary loaded (how) | Agent $ |
| --- | --- | --- | --- | --- | --- | --- |
| evaluation-bound-spans-versus-model-paraphrase | adk-agent-evaluation | 0/5 | A1:FFF A2:FFF A3:FFF A4:FFF A5:FFF | none | no (-) | 0.16 |
| evaluation-collateral-damage-no-op-control | adk-agent-evaluation | 2/4 | A1:PPP A2:PPP A3:PFF A4:FFF | A3 | yes (skill-tool) | 0.43 |
| evaluation-generalization-and-deliverable-budget | adk-agent-evaluation | 3/4 | A1:PPP A2:PPP A3:PPF A4:FFF | A3 | no (-) | 0.19 |
| evaluation-improve-decisions-error-analysis | adk-agent-evaluation | 1/5 | A1:FPF A2:PPP A3:FFF A4:FFF A5:FFP | A1, A5 | yes (skill-tool) | 0.46 |
| evaluation-incident-regression-fail-to-pass | adk-agent-evaluation | 3/4 | A1:PPP A2:PPP A3:PFP A4:FFF | A3 | yes (skill-tool) | 0.21 |
| evaluation-judge-agreement-and-harness-bridge | adk-agent-evaluation | 0/4 | A1:FFF A2:FFP A3:FFF A4:FFF | A2 | yes (skill-tool) | 0.65 |
| evaluation-preinference-contract-qualification | adk-agent-evaluation | 0/6 | A1:FFF A2:FFF A3:FFF A4:FFF A5:FFF A6:FFF | none | yes (skill-tool) | 0.39 |
| evaluation-progressive-downstream-repair | adk-agent-evaluation | 0/5 | A1:FFF A2:FFF A3:FFF A4:FFF A5:FFF | none | no (-) | 0.12 |
| evaluation-recovery-is-not-full-route-acceptance | adk-agent-evaluation | 5/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:FFF | none | yes (skill-tool) | 0.24 |
| evaluation-recurring-failures-reentry | adk-agent-evaluation | 4/4 | A1:PPP A2:PPP A3:PPP A4:PPP | none | no (-) | 0.58 |
| evaluation-repeated-trials-pass-hat-k-and-end-state | adk-agent-evaluation | 2/4 | A1:PPP A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.47 |
| evaluation-reviewer-coverage-versus-uncertainty | adk-agent-evaluation | 3/4 | A1:PPP A2:PPP A3:FFP A4:PPP | A3 | yes (skill-tool) | 0.30 |
| evaluation-selected-source-support | adk-agent-evaluation | 3/5 | A1:PPP A2:PPP A3:FFF A4:PPP A5:FFF | none | no (-) | 0.12 |
| evaluation-self-hosted-harnesses-mlflow-deepeval-opik | adk-agent-evaluation | 2/4 | A1:PFP A2:FFF A3:PPP A4:FFF | A1 | yes (skill-tool) | 0.20 |
| evaluation-tool-fault-matrix-and-resilience | adk-agent-evaluation | 3/4 | A1:PPP A2:FFF A3:PPP A4:PPF | A4 | yes (skill-tool) | 0.62 |
| evaluation-underwriter-labelling-session | adk-agent-evaluation | 2/4 | A1:FFF A2:FFF A3:PPP A4:PPP | none | yes (skill-tool) | 0.27 |
| instructions-routing-and-templating-repair | adk-agent-instructions | 1/4 | A1:PPP A2:FFF A3:FFF A4:FFF | none | yes (skill-tool) | 0.25 |
| interoperability-consume-enterprise-mcp-server-registration-and-sso | adk-agent-interoperability | 1/4 | A1:FFF A2:FFF A3:PPP A4:FFF | none | yes (skill-tool) | 0.25 |
| interoperability-expose-a2a-with-tck-acceptance | adk-agent-interoperability | 2/4 | A1:FFF A2:PPP A3:PPP A4:FFF | none | yes (skill-tool) | 0.35 |
| interoperability-expose-and-register-a2a | adk-agent-interoperability | agent-error | | | | |
| interoperability-expose-mcp-server-with-conformance-baseline | adk-agent-interoperability | agent-error | | | | |
| interoperability-exposed-agent-forgets-on-modern-clients | adk-agent-interoperability | agent-error | | | | |
| interoperability-mcp-app-widget-to-custom-frontend | adk-agent-interoperability | agent-error | | | | |
| interoperability-verify-signed-agent-card | adk-agent-interoperability | agent-error | | | | |
| observability-agent-runtime-latency-and-alerts | adk-agent-observability | 0/4 | A1:FFP A2:FFF A3:FFF A4:FFF | A1 | yes (skill-tool) | 0.34 |
| observability-cost-reconciliation-agenttool-litellm | adk-agent-observability | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP | none | yes (skill-tool) | 0.21 |
| observability-handover-and-postmortem | adk-agent-observability | agent-error | | | | |
| observability-semconv-drift-and-evaluation-events | adk-agent-observability | 1/4 | A1:PPF A2:FFF A3:FFF A4:FFF | A1 | yes (skill-tool) | 0.33 |
| mcp-rug-pull-runtime-pin-and-mcp-ids | adk-agent-security | 2/4 | A1:FFF A2:PPP A3:FFF A4:PPP | none | yes (skill-tool) | 0.29 |
| security-adopt-third-party-mcp-server-with-scan | adk-agent-security | 1/4 | A1:FFF A2:PPP A3:FFF A4:PFF | A4 | yes (skill-tool) | 0.21 |
| security-adversarial-suite-ported-goal-classes | adk-agent-security | 1/4 | A1:FPF A2:FFF A3:FFF A4:PPP | A1 | yes (skill-tool) | 0.47 |
| security-code-execution-environment-selection | adk-agent-security | 2/4 | A1:PPP A2:FFF A3:FFF A4:PPP | none | yes (skill-tool) | 0.46 |
| security-garak-ci-gate-on-adk-runner | adk-agent-security | 2/4 | A1:PPP A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.39 |
| security-gate-default-deny-and-call-provenance | adk-agent-security | 0/4 | A1:FFF A2:FFF A3:FFF A4:FFF | none | yes (skill-tool) | 0.23 |
| security-red-team-a2a-exposed-agent-with-pyrit | adk-agent-security | 2/4 | A1:PPP A2:FFF A3:PPP A4:FFF | none | yes (skill-tool) | 0.26 |
| security-refund-agent-build-time-controls-vs-screening | adk-agent-security | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.30 |
| security-review-untrusted-content-with-write-tools | adk-agent-security | 1/4 | A1:PPP A2:FFF A3:FFF A4:FFF | none | yes (skill-tool) | 0.56 |
| security-review-with-atlas-and-cosai-ids | adk-agent-security | 3/4 | A1:FFF A2:PPP A3:PFP A4:FPP | A3, A4 | yes (skill-tool) | 0.26 |
| sensitive-data-local-tool-result-screen-llamafirewall | adk-agent-security | 1/5 | A1:FFF A2:FFF A3:FPP A4:FFF A5:FFF | A3 | no (-) | 0.37 |
| engineer-ends-with-checkpoint-after-contract-delta | adk-engineer | 1/3 | A1:PFP A2:FFF A3:FFP | A1, A3 | yes (slash-command) | 0.44 |
| engineer-parallel-tickets-with-overlapping-touches | adk-engineer | 2/3 | A1:PPP A2:PPP A3:FFF | none | no (-) | 0.36 |
| engineer-resumes-from-progress-block | adk-engineer | 1/3 | A1:PPP A2:FFP A3:FFF | A2 | yes (slash-command) | 0.12 |
| engineer-ticket-with-missing-companion | adk-engineer | 2/4 | A1:PPP A2:PPP A3:FFF A4:FFF | none | yes (slash-command) | 0.39 |
| engineer-writes-progress-block-when-stopping | adk-engineer | 3/3 | A1:PPP A2:PPP A3:PPP | none | yes (slash-command) | 0.19 |
| router-builds-at-poc-depth | adk-engineer | 4/4 | A1:PPP A2:PPP A3:PFP A4:PFP | A3, A4 | yes (skill-tool) | 0.41 |
| router-flags-underestimated-ticket | adk-engineer | 4/4 | A1:PPP A2:PPP A3:PPP A4:PPP | none | yes (skill-tool) | 0.43 |
| router-missing-specialist | adk-engineer | 3/5 | A1:PPP A2:PPP A3:FFF A4:PPP A5:FFF | none | yes (skill-tool) | 0.19 |
| web-backend-app-migrations-beside-adk-sessions | adk-fastapi-backend | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.18 |
| frontend-agui-approval-contract-declared | adk-frontend-integration | 0/4 | A1:FPF A2:FFF A3:FFF A4:FFF | A1 | yes (skill-tool) | 0.19 |
| engineer-agents-cli-focused-memory-1-11 | adk-memory-architecture | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.20 |
| engineer-gcp-goal-unaffected-by-portability | adk-memory-architecture | 3/3 | A1:PPP A2:PPP A3:PPP | none | yes (read) | 0.25 |
| engineer-ticket-creates-cloud-sql | adk-memory-architecture | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | no (-) | 0.33 |
| existing-agents-cli-focused-memory | adk-memory-architecture | 6/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:PPP | none | yes (skill-tool) | 0.17 |
| memory-document-shape-and-source-coordinates | adk-memory-architecture | 0/5 | A1:FFP A2:FFP A3:PFF A4:FFF A5:FFF | A1, A2, A3 | yes (skill-tool) | 0.30 |
| memory-ingestion-scan-detection | adk-memory-architecture | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP | none | yes (skill-tool) | 0.22 |
| memory-local-document-completeness | adk-memory-architecture | 3/4 | A1:PPP A2:PPP A3:FFF A4:PPP | none | yes (skill-tool) | 0.20 |
| memory-poisoned-fact-rollback-and-update-cases | adk-memory-architecture | 2/4 | A1:FPF A2:PPP A3:FFF A4:PPP | A1 | yes (skill-tool) | 0.48 |
| memory-third-party-service-silent-empty-and-supersede | adk-memory-architecture | 3/4 | A1:PPP A2:PPP A3:PPP A4:FPF | A4 | yes (skill-tool) | 0.30 |
| memory-write-back-loop-from-horizon | adk-memory-architecture | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.88 |
| router-resumes-accepted-goal | adk-memory-architecture | 4/4 | A1:PPP A2:PPP A3:PPP A4:PPP | none | yes (read) | 0.35 |
| guardrails-continuation-accounting-and-duplicates | adk-operational-guardrails | 3/5 | A1:PPP A2:FFF A3:PPP A4:FFF A5:PPP | none | no (-) | 0.28 |
| guardrails-escalation-two-sided-calibration | adk-operational-guardrails | 1/4 | A1:FFF A2:FFF A3:FFF A4:PPP | none | no (-) | 0.16 |
| guardrails-unanswered-approval-and-screening-placement | adk-operational-guardrails | 1/4 | A1:FFF A2:FFF A3:FFF A4:PPP | none | yes (skill-tool) | 0.18 |
| release-bigquery-analytics-score-gate-and-drift | adk-release-engineering | agent-error | | | | |
| release-coding-agent-capability-diff-gate | adk-release-engineering | 2/5 | A1:FFF A2:PFP A3:PPP A4:FFF A5:FFF | A2 | yes (skill-tool) | 0.28 |
| release-model-retirement-and-ci-gate | adk-release-engineering | 1/4 | A1:FFF A2:FFF A3:FFF A4:PPP | none | yes (skill-tool) | 0.50 |
| release-post-launch-quality-loop-aqua | adk-release-engineering | agent-error | | | | |
| release-promptfoo-gate-exit-codes-and-trajectory-assertions | adk-release-engineering | 1/4 | A1:PPP A2:FFF A3:FFF A4:FFF | none | yes (skill-tool) | 0.46 |
| sql-toolbox-read-only-and-secure-tenant | adk-sql-agent-engineering | 2/4 | A1:PPP A2:PPF A3:FFF A4:FFF | A2 | yes (skill-tool) | 0.44 |
| designer-checkpoint-settles-the-agenda | adk-system-designer | 3/4 | A1:FPF A2:FPP A3:PPP A4:PPF | A1, A2, A4 | yes (slash-command) | 0.34 |
| designer-names-google-product-skills | adk-system-designer | 2/4 | A1:PPP A2:FFF A3:PPP A4:FFF | none | yes (skill-tool) | 1.55 |
| designer-phase-gate-plan-versus-code | adk-system-designer | 4/5 | A1:PPP A2:FFF A3:PPP A4:PPP A5:FPP | A5 | yes (slash-command) | 0.27 |
| designer-production-cost-contract | adk-system-designer | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPF A5:PPP | A4 | yes (skill-tool) | 1.67 |
| designer-sow-from-plan | adk-system-designer | 3/4 | A1:PPP A2:PPP A3:PFP A4:FFF | A3 | yes (skill-tool) | 0.27 |
| designer-tickets-get-journey-goal-and-lint | adk-system-designer | 0/3 | A1:FFF A2:FFF A3:FFF | none | yes (slash-command) | 0.18 |
| designer-weekly-status-from-plan-evidence | adk-system-designer | 2/3 | A1:PPP A2:PPP A3:FFF | none | yes (slash-command) | 0.56 |
| system-design-practical-handoff | adk-system-designer | 5/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:FFF A6:PPP | none | yes (skill-tool) | 0.99 |
| system-design-review-existing-proposal | adk-system-designer | 7/8 | A1:FPP A2:PPP A3:PPP A4:PPP A5:PPP A6:PFF A7:PPP A8:PPP | A1, A6 | yes (skill-tool) | 0.25 |
| system-design-runtime-and-release-review | adk-system-designer | 4/6 | A1:FFF A2:PPP A3:FFF A4:PPP A5:PPP A6:PPP | none | yes (skill-tool) | 0.18 |
| system-design-scope-gate-time-boxed | adk-system-designer | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP | none | yes (skill-tool) | 0.34 |
| tool-interface-wrong-tool-diagnosis | adk-tool-interface-design | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | none | yes (skill-tool) | 0.13 |
| web-backend-deploy-routes-to-deploy | deploy-adk-on-google-cloud | 3/4 | A1:PPP A2:PPP A3:FFF A4:PPP | none | yes (skill-tool) | 0.28 |
| optimise-compaction-atomic-groups-three-points | optimise-adk-on-google-cloud | 2/4 | A1:PPP A2:FFF A3:FFF A4:PPP | none | yes (skill-tool) | 0.25 |
| privacy-with-observability | protect-adk-sensitive-data | 2/6 | A1:FFF A2:FFP A3:PPP A4:FFF A5:PPP A6:FFF | A2 | no (-) | 0.13 |
| chosen-test-first-workflow | safe-api-tool-calls | 2/6 | A1:FFF A2:FFF A3:FFF A4:PFF A5:PPP A6:PPP | A4 | no (-) | 0.10 |

Spend: agent $28.77, judge $9.69, total $38.46
