# System design: claims triage assistant

Status: user-reviewed decisions recorded below

## Purpose and constraints

Claims handlers at a mid-sized general insurer receive first-notice-of-loss
reports by web form and email. The assistant classifies each new claim by
type and urgency, checks the policy wording for the coverage question,
drafts a triage note, and, after the handler approves, writes the type,
urgency and note to the claims platform. The handler decides coverage; the
model drafts and code controls every write.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | End of phase 1; continued into a pilot with one claims team |
| People and hours | One developer, one claims lead reviewing |
| Data touched and effects allowed | Personal claim data; writes to the claims platform only after handler approval |
| Delivery profile | MVP or pilot: one team, real claims, handler approval on every write |
| Portability concern | yes: raised by the insurer's CTO (source: CTO, 2026-10-20); group IT may standardise on Azure, and the board asked what AWS would involve. Exit plan wanted, not a second platform. |

## Requirements and contracts

| ID | Requirement | Need it serves | Status (confirmed / assumed) |
| --- | --- | --- | --- |
| R1 | Classify each new claim by type and urgency for the handler queue | Faster first contact on urgent claims | confirmed |
| R2 | Cite the policy clause behind each coverage note | Handlers trust and check the note | confirmed |
| R3 | Nothing is written to the claims platform without the handler's approval | Handler stays accountable | confirmed |
| R4 | Only the insurer's claims staff can use it | Claim data stays internal | confirmed |

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R2 | Every coverage note cites at least one clause retrieved from the policy corpus, or says no clause was found | Per note | Code | Output check after the draft step | Note withheld | planned: offline eval, G02 |
| C2 | R3 | No claims-platform write without an approval bound to the claim ID and note version | Per write | Code | Tool confirmation; recheck in the write tool | Write refused | planned: local Runner test, G03 |
| C3 | R4 | A handler sees only claims in their team queue | Per request | Code | Ownership check from the IAP identity | 403 | planned: local test, G03 |
| C4 | R1 | Triage output validates against the TriageResult schema | Per claim | Code | `output_schema` plus validation | Retry once, then manual triage | planned: offline eval, G01 |

## Architecture and decisions

| ID | Enforces | Design choice | Reason | Tradeoff / alternative | Verification and expected result |
| --- | --- | --- | --- | --- | --- |
| D1 | C4 | ADK 2.x: a `SequentialAgent` of classify, retrieve and draft steps, served by FastAPI on Cloud Run in australia-southeast1 | Simple ordered flow; one container | Agent Runtime rejected: no need for managed memory | Runner tests per step |
| D2 | C4 | Pinned Gemini Flash model on Agent Platform, `output_schema` TriageResult, thinking off | Cheap, fast, structured output | Larger model only if M1 falls short | Eval set accuracy (M1) |
| D3 | C2 | `DatabaseSessionService` on Cloud SQL for PostgreSQL, IAM database authentication | Approval state survives restarts; standard Postgres | `VertexAiSessionService` rejected: needs Agent Runtime | Restart test |
| D4 | C1 | Policy wording corpus in RAG Engine with Gemini embeddings, queried by `VertexAiRagRetrieval` | Managed chunking and ranking | Own pgvector index: more work now | Retrieval eval in G02 |
| D5 | C2 | Claims platform REST API called by one `FunctionTool` with `require_confirmation`; the client is passed in | Approval in code, idempotent write key | MCP server not available from the vendor | Confirmation test |
| D6 | C3 | Claim attachments in Cloud Storage through `GcsArtifactService` | Native ADK artifact service | — | Artifact read test |
| D7 | C3 | IAP with Google Workspace accounts in front of Cloud Run; service account for Cloud SQL; claims API key in Secret Manager | Keyless workload identity; staff already on Workspace | Identity Platform: not needed for staff | Ownership test |
| D8 | C1 | OpenTelemetry spans exported to Cloud Trace; logs to Cloud Logging; evaluation with `adk eval` and a Gemini judge | Toolkit defaults | Third-party APM: not requested | Trace present per turn |
| D9 | C1 | Model Armor screens claim free text before the model call | Prompt injection in emailed claims | Own regex screen: weaker | Adversarial cases |

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Pilot volume | Sizing of Cloud SQL | Claims lead | Nothing in phase 1 |
