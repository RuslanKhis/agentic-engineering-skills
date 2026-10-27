Activation run: backend claude-cli, model claude-sonnet-5-5, 114 cases x 2 repeat(s)
catalogue 0d93b63db2ea4b1a  corpus f51ed02934672ec3

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 111 | 2 | 1 | 0 |
| repeat 2 | 111 | 2 | 1 | 0 |
| all | 222 | 4 | 2 | 0 |

Cases not passing in every repeat:
- designer-checkpoint-positive [adk-system-designer, positive] PASS PARTIAL: primary adk-engineer; supporting adk-system-designer. Checkpointing an in-flight build plan after a design-meaning change and hour overrun spans several ADK concerns, with replanning and scope trade-offs from the system designer.
- memory-ingestion-positive [adk-memory-architecture, positive] PASS FAIL: primary none; supporting -. Classifying document pages as scans, tables or drawings and routing to OCR/vision for an ingestion report is document-ingestion work that no catalogue skill covers.
- observability-eval-handoff-positive [adk-agent-observability, positive] PARTIAL PARTIAL: primary adk-agent-evaluation; supporting adk-agent-observability,protect-adk-sensitive-data. Building a regression eval set is evaluation work, fed by production traces from Agent Analytics (observability) and requiring PII removal (sensitive-data protection).
- portability-migration-build-near-miss [adk-portability-planning, near-miss] FAIL PASS: primary adk-portability-planning; supporting -. Moving off ADK/GCP to LangGraph on AWS is a portability matter, though this skill only writes a plan and the actual migration is outside the catalogue.
- presenter-rollout-ui-near-miss [adk-presenter, near-miss] PARTIAL PASS: primary adk-frontend-integration; supporting adk-presenter. Adding agent UI elements to the chat interface is frontend integration work, and the AI disclosure wording relates to rollout pack content from the presenter skill.
