# Implementation plan: public enquiries assistant pilot

Status: in progress
Architecture: [docs/architecture/enquiries.md](../architecture/enquiries.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Answers from published guidance | 1 | implementation | 5-7 | none | adk-memory-architecture | verified_local |
| G02 Verified application status lookup | 1 | implementation | 4-6 | none | adk-tool-auth-and-secrets | verified_local |
| G03 Handover to the contact centre | 1 | implementation | 2-3 | G01 | adk-workflow-design | verified_local |
| G04 Pilot journey | 1 | journey | 3-4 | G02, G03 | adk-agent-evaluation | verified_local |
| G05 Governance papers | 1 | governance | 5-8 | G04 | adk-governance-pack | ready |

## Calendar waits

- W1: website change window for the chat widget, 2026-11-25.
- W2: CISO security assessment before the pilot.
- W3: Agency counsel review of the governance pack, including the ICTA clause 6.11 model-change position, needed before the 2026-12-10 pilot decision; requested the day the drafts go out.
- W4: Privacy officer's PIA under the IPC AI PIA guide, privacy management plan and s 10 notice update, and records disposal authority advice from the records manager, needed before the 2026-12-10 pilot decision.
- W5: AIAF Platform registration and assessment by the agency's Accountable Owner, needed before the 2026-12-10 pilot decision.
- W6: NSW AI Review Committee referral, within 5 business days of completing the AIAF; applies only if the agency sets the band at high or critical.
- W7: Customer's written approval or Order Form variation for the replacement of the pinned model and for any processing or support access outside NSW, needed before the pilot starts.

## Measurement records

- M1: metric answers citing a correct guidance page; value 94%; window 2026-10-13 to 2026-10-24; sample 400 historical enquiries; method offline evaluation; owner Southgate Labs; build v0.7.0
- M2: metric status lookups returned for a mismatched date of birth; value 0; window 2026-10-13 to 2026-10-24; sample 250 scripted attempts; method scripted tests; owner Southgate Labs; build v0.7.0

## Evidence

- G05: drafted, not sent. Documents in `docs/governance/enquiries/`; waits W3 to W7 added by the pack. No production or pilot-approval goal exists in this plan: W3 to W7 should block one (proposed G06 Pilot approval, decider Ruth Abbott, 2026-12-10).

## Resume here

Next: G05 Governance papers.
