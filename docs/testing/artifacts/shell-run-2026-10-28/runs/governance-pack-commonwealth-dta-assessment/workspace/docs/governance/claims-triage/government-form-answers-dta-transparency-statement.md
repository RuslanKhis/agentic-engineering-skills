---
document: government-form-answers
system: Claims triage assistant (Compensation Claims Office)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO officer who completes the form (assessing officer or accountable use case owner; agency: to be named)
form: AI transparency statement inputs (Standard for AI transparency statements)
form_version: v2.1, updated 20 October 2026
form_url: https://www.digital.gov.au/ai/ai-in-government-policy/standard-ai-transparency-statements
form_checked: 2026-10-26
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md
---

# Draft answers for AI transparency statement inputs (Standard for AI transparency statements): Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own order, for the Compensation Claims Office's officers to check and paste into the official tool, where they complete, rate and approve the assessment. Each answer cites the project record, or says who must answer it: `agency:` for what only the agency can answer, `counsel:` for a legal question. Not legal advice.

## Form and version

- **Form:** Standard for AI transparency statements v2.1, https://www.digital.gov.au/ai/ai-in-government-policy/standard-ai-transparency-statements (checked 2026-10-26).
- **Crosswalk used:** references/au-government-crosswalks.md, verified 2026-10-26 (source: adk-governance-pack reference, read 2026-10-28).
- **Version match:** gap: official page not re-read in this session (no network); version and date are the crosswalk's.
- **Rating basis the form uses:** n/a: the statement is agency-level and rates nothing.

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Author and publisher of the statement | agency: the CCO, through the accountable official or delegate | gap: not named |
| External suppliers | Southgate Labs (developer); Google (model and cloud) | D1, D4 |

## Draft answers

The statement is agency-level and need not list use cases (source: adk-governance-pack reference, read 2026-10-28). The inputs below are this use case's facts for the agency to fold in.

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| Content 1 | Why the agency uses AI | agency: ; this use case drafts claim triage recommendations to shorten time to triage while officers decide | system-card.md, R1 | agency: |
| Content 2 | Usage patterns and domains | Proposed: decision-making and administrative action, with workflow automation; domain compensation claims | government-form-answers-dta-impact-assessment.md items 1.7 and 1.9 | agency: |
| Content 3 | Where the public may interact with or be significantly affected by AI without human review | The public does not interact with it; claimants are affected only through an officer who reviews every draft (R4, C4); share of drafts changed in the pilot not yet measured | R4, C4; gap: pilot measure | agency: |
| Content 4 | Monitoring and protection against negative impacts | Offline evaluation M1 and M2; pilot measures planned: gap: no goal; officer review of every draft | impact-assessment.md Monitoring and review; M1, M2 | agency: |
| Content 5 | Compliance with the policy | agency: | regulatory-memo.md | agency: |
| Content 6 | Compliance with legislation | Privacy Act and APPs, APP 1.7 from 10 December 2026 (checked 2026-10-26) | regulatory-memo.md | counsel: and agency: |
| Content 7 | When last updated; contact; plain language | agency: | system-card.md Contact | agency: |

- Flag for the agency: if this is the first use case that uses personal and sensitive health information with a generative model, it changes the agency's AI profile and the statement needs review (agency: confirm).

## Questions for the agency

- agency: whether the statement exists, when it was last updated, and whether it must change before the pilot; needed by W3.

## Questions for counsel

- counsel: statement wording on legislation compliance; needed by W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO officer completing the form (agency: to be named) | this document | pending | pending |
