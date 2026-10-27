---
document: government-form-answers
system: Claims triage assistant (Compensation Claims Office)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO officer who completes the form (assessing officer or accountable use case owner; agency: to be named)
form: Agentic AI addendum conformance
form_version: PDF last updated 4 June 2026
form_url: https://www.digital.gov.au/policy/ai/agentic-ai-addendum
form_checked: 2026-10-26
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md
---

# Draft answers for Agentic AI addendum conformance: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own order, for the Compensation Claims Office's officers to check and paste into the official tool, where they complete, rate and approve the assessment. Each answer cites the project record, or says who must answer it: `agency:` for what only the agency can answer, `counsel:` for a legal question. Not legal advice.

## Form and version

- **Form:** Agentic AI addendum, PDF last updated 4 June 2026, https://www.digital.gov.au/policy/ai/agentic-ai-addendum (checked 2026-10-26). Strongly recommended, not mandatory.
- **Crosswalk used:** references/au-government-crosswalks.md, verified 2026-10-26 (source: adk-governance-pack reference, read 2026-10-28).
- **Version match:** gap: official page not re-read in this session (no network); version and date are the crosswalk's.
- **Rating basis the form uses:** n/a: conformance statements, no rating.

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Accountable use case owner | agency: | gap: not named |
| External suppliers | Southgate Labs supplies the evidence; Google provides the model | D1, D4 |

## Draft answers

The assistant is a read-only drafting agent, not an autonomous actor: it has no write tools (C3) and an officer decides every output (R4).

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| AGT.1 | Governance and safeguards: responsibilities, human oversight, explanation, orchestration | Accountable official and privacy and security officers named; officer accepts or changes every draft; cited passages; orchestration layer: gap: topology not recorded | docs/discovery/claims-triage.md §5, R2, R4, C4 | agency: |
| AGT.2 | Memory management | gap: memory scope, retention and erasure not recorded; the decisions table holds drafts and decisions | C4 | agency: |
| AGT.3 | Workflow design | Single triage workflow; read-only; invocation limits and budgets: gap: not recorded | R1, C3; SB05 deferred: production | agency: |
| AGT.4 | Routing and data flow between agents | n/a: no multi-agent routing recorded | docs/architecture/claims-triage.md Contracts | agency: |
| AGT.5 | Choice of agent, model and technique | Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`; lifecycle gap: retirement date not read | D1 | agency: |
| AGT.6 | Continuous evaluation | Offline evaluation M1 and M2; adversarial and memory tests: gap | M1, M2 | agency: |
| AGT.7 | Tools and protocols | Read-only case system tool scoped to the officer's team | C1, C3 | agency: |
| AGT.8 | Ongoing monitoring and a control tower | gap: monitoring, alerts and a kill switch are not recorded | docs/architecture/claims-triage.md | agency: |
| Decommissioning | Cleanup and teardown | gap: no decommissioning goal; the pilot lasts 8 weeks and its data needs a disposal plan | docs/discovery/claims-triage.md §6 | agency: |

- **Vendor evidence for the DTA AI model clauses** (clause text reported; not confirmed at the source on 2026-10-26): human oversight (cl 5.1) is in system-card.md Human oversight; testing and monitoring (cl 6.2.4) rests on M1 and M2 with gaps; no ingestion of buyer data into a model (cl 11) is a gap pending the provider's terms (privacy-impact-input-pack.md); risk management (cl 13) is impact-assessment.md.

## Questions for the agency

- agency: whether the CCO adopts the addendum for the pilot; needed by W3.

## Questions for counsel

- counsel: whether the DTA AI model clauses are in the contract with Southgate Labs and Google; needed by W2.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO officer completing the form (agency: to be named) | this document | pending | pending |
