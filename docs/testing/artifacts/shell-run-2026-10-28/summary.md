# Scenario results, Phase 13 shell run · 28 October 2026

Unconfined run: the agent had Bash. Batches s1, s2, r3, r4 the four governance packs never run before
(r3 and r4 re-run Auckland-Singapore and Quebec-Ontario after s3 and s4 were spoiled by refused writes);
s5, s6 the eight scenarios whose assertion text carries a no-shell escape; t1 three helper scenarios;
rj1 a re-judge of `engineer-ticket-with-missing-companion` on unchanged evidence after the shell-read
parser fix. Votes are the three judge verdicts per assertion, in order; "last no-shell" is the latest
earlier graded run of the scenario (phases 9-11). "Skills loaded" counts the Skill tool, a Read of a
SKILL.md, a shell read of it (parser at `05fd0e5` for rj1, `1795c5c` for the others) or a slash command.

| Scenario | Batch | Passed | Votes | Last no-shell | Primary loaded | Skills loaded | Bash calls | Agent $ | Judge $ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| governance-pack-nsw-agency-chatbot | s1 | 6/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:PPP | never run | yes | adk-governance-pack | 15 | 0.94 | 0.53 |
| governance-pack-commonwealth-dta-assessment | s2 | 5/5 | A1:PPP A2:PPP A3:PPP A4:FPP A5:PPP | never run | yes | adk-governance-pack | 16 | 1.12 | 0.60 |
| governance-pack-auckland-singapore-retailer | r3 | 5/6 | A1:PPP A2:PPP A3:PPP A4:FFF A5:PPP A6:PPP | never run | yes | adk-governance-pack | 22 | 1.29 | 0.61 |
| governance-pack-quebec-ontario-hr-assistant | r4 | 6/6 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:PPP | never run | yes | adk-governance-pack | 16 | 0.96 | 0.53 |
| presenter-monthly-value-report | s5 | 4/4 | A1:PPP A2:PPP A3:FPP A4:PPP | 2/4 (phase10): A1:PPP A2:FFF A3:PFF A4:PPP | yes | adk-presenter | 9 | 0.20 | 0.19 |
| engineer-resumes-from-progress-block | s5 | 3/3 | A1:PPP A2:PPP A3:FPP | 2/3 (phase10): A1:PPP A2:FFF A3:PFP | yes | adk-engineer | 12 | 0.25 | 0.22 |
| engineer-google-skills-supporting-missing | s5 | 5/5 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP | 2/5 (phase10): A1:PFF A2:FFF A3:PFF A4:PPP A5:FPP | yes | deploy-adk-on-google-cloud, adk-tool-auth-and-secrets | 10 | 0.22 | 0.21 |
| portability-ticket-carried-out | s5 | 7/8 | A1:PPP A2:PPP A3:PPP A4:PPP A5:PPP A6:PPP A7:PPP A8:FFP | 6/8 (phase10): A1:PPP A2:FFF A3:PPP A4:PPP A5:PPP A6:PPP A7:FPF A8:PFP | yes | adk-portability-planning | 11 | 0.50 | 0.35 |
| interoperability-verify-signed-agent-card | s6 | 3/4 | A1:FPP A2:PPP A3:PPP A4:FFF | 1/4 (phase10): A1:FFP A2:PPP A3:FFF A4:FFF | yes | adk-agent-interoperability | 8 | 0.26 | 0.22 |
| interoperability-expose-mcp-server-with-conformance-baseline | s6 | 1/4 | A1:FFF A2:FFF A3:FPP A4:FFF | 0/4 (phase10): A1:FFF A2:FFF A3:FFF A4:FFF | yes | adk-agent-interoperability | 5 | 0.24 | 0.19 |
| engineer-ticket-with-missing-companion | s6 | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | 1/4 (phase10): A1:FFF A2:PPP A3:FFF A4:FFF | yes | adk-engineer | 13 | 0.35 | 0.30 |
| workflow-checkpoint-dependency-invalidation | s6 | 3/5 | A1:FFF A2:FFF A3:FPP A4:PPP A5:PFP | 1/5 (phase11): A1:FFF A2:FFF A3:FFF A4:FPP A5:PFF | yes | adk-workflow-design | 13 | 0.61 | 0.37 |
| designer-tickets-get-journey-goal-and-lint | t1 | 0/3 | A1:FFF A2:FFF A3:FFF | 0/3 (phase9): A1:FFF A2:FFF A3:FFF | yes | adk-system-designer | 5 | 0.19 | 0.15 |
| evaluation-underwriter-labelling-session | t1 | 3/4 | A1:FFF A2:PPP A3:PPP A4:PPP | 2/4 (phase9): A1:FFF A2:FFF A3:PPP A4:PPP | yes | adk-agent-evaluation | 5 | 0.18 | 0.15 |
| tool-interface-wrong-tool-diagnosis | t1 | 1/4 | A1:FFF A2:PPP A3:FFF A4:FFF | 1/4 (phase9): A1:FFF A2:PPP A3:FFF A4:FFF | yes | adk-tool-interface-design | 5 | 0.11 | 0.13 |
| engineer-ticket-with-missing-companion | rj1 re-judge, same evidence | 2/4 | A1:PPP A2:PPP A3:FFF A4:FFF | 1/4 (phase10): A1:FFF A2:PPP A3:FFF A4:FFF | yes | adk-engineer, adk-frontend-integration | 13 | 0.00 | 0.29 |
| governance-pack-auckland-singapore-retailer | s3 spoiled (writes refused after cd) | 0/6 | A1:FFF A2:FFF A3:FFF A4:FFF A5:FFF A6:FFF | never run | yes | adk-governance-pack | 16 | 0.70 | 0.20 |
| governance-pack-quebec-ontario-hr-assistant | s4 spoiled (writes refused after cd) | 3/6 | A1:PPP A2:FFF A3:FFP A4:FFF A5:PPP A6:PPP | never run | yes | adk-governance-pack | 14 | 0.86 | 0.24 |

Recorded cost of the rows above: agent $8.99, judge $5.49, total
$14.48. Not in the table: the smoke test ($0.06), the working-directory
probe ($0.03) and the two authentication probes (under $0.01).
