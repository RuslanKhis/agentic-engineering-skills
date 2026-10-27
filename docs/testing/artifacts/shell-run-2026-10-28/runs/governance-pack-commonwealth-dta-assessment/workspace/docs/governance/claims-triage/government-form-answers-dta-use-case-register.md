---
document: government-form-answers
system: Claims triage assistant (Compensation Claims Office)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO officer who completes the form (assessing officer or accountable use case owner; agency: to be named)
form: Internal AI use case register row (Standard for accountability)
form_version: v2.1, updated 20 October 2026
form_url: https://www.digital.gov.au/ai/ai-in-government-policy/accountability
form_checked: 2026-10-26
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md
---

# Draft answers for Internal AI use case register row (Standard for accountability): Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own order, for the Compensation Claims Office's officers to check and paste into the official tool, where they complete, rate and approve the assessment. Each answer cites the project record, or says who must answer it: `agency:` for what only the agency can answer, `counsel:` for a legal question. Not legal advice.

## Form and version

- **Form:** Standard for accountability v2.1, https://www.digital.gov.au/ai/ai-in-government-policy/accountability (checked 2026-10-26).
- **Crosswalk used:** references/au-government-crosswalks.md, verified 2026-10-26 (source: adk-governance-pack reference, read 2026-10-28).
- **Version match:** gap: official page not re-read in this session (no network); version and date are the crosswalk's.
- **Rating basis the form uses:** inherent and residual ratings come from the impact assessment tool (assumption: proposals only; agency: sets).

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Accountable use case owner | agency: name and position | gap: not named |
| Register keeper | agency: | gap: not named |
| External suppliers | Southgate Labs; Google | D1, D4 |

## Draft answers

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| Field 1 | Use case name; agency reference | Claims triage assistant; reference agency: | README.md | agency: |
| Field 2 | Description, business objective, product name | Drafts triage recommendations for officers to accept or change; objective to cut time to triage from a 6-working-day median; model Gemini 3.5 Flash | R1, docs/discovery/claims-triage.md §2, D1 | the record |
| Field 3 | AI technology type | Generative language model | D1 | the record |
| Field 4 | Lifecycle stage | Pilot design; pilot decision 2026-12-08; offline evaluation verified locally | docs/discovery/claims-triage.md §6, G04 | agency: |
| Field 5 | Use of the technical standard | See the agentic addendum answers | government-form-answers-dta-agentic-addendum.md | agency: confirms |
| Field 6 | Domain and usage pattern | Compensation claims; decision-making and administrative action, workflow automation (assumption: agency: confirm the list) | government-form-answers-dta-impact-assessment.md | agency: |
| Field 7 | Accountable use case owner | agency: | gap: not named | agency: |
| Field 8 | In-scope criteria met | As the impact assessment tool item 1.5 | government-form-answers-dta-impact-assessment.md | counsel: and agency: |
| Field 9 | Inherent and residual ratings; date last updated | Proposed inherent high and residual high (assumption: basis in impact-assessment.md); set by the agency | impact-assessment.md | agency: |
| Field 10 | High risk only: last and next review dates | agency: next review within 12 months of deployment (checked 2026-10-26); W3 | W3 | agency: |

## Questions for the agency

- agency: reference number, owner and register location; needed by W3.

## Questions for counsel

- counsel: none specific to the register beyond those in government-form-answers-dta-impact-assessment.md; needed by W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO officer completing the form (agency: to be named) | this document | pending | pending |
