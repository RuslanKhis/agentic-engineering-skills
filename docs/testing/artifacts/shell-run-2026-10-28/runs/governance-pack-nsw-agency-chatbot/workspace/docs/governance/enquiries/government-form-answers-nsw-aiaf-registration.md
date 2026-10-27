---
document: government-form-answers
system: Public enquiries assistant
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: AIAF Accountable Owner at the NSW Trades Licensing Office (agency: to be named)
form: NSW AIAF Platform registration
form_version: baseline registration questions in the NSW AI Operational Policy, Final v1.1, Attachment A
form_url: https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-strategy-and-operational-policy/nsw-ai-operational-policy
form_checked: 2026-10-26
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md
---

# Draft answers for NSW AIAF Platform registration: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own order, for the NSW Trades Licensing Office's officers to check and paste into the official tool, where they complete, rate and approve the registration. Each answer cites the project record, or says who must answer it: `agency:` for what only the agency can answer, `counsel:` for a legal question. Not legal advice.

## Form and version

- **Form:** NSW AIAF Platform registration, baseline questions in the NSW AI Operational Policy Final v1.1 Attachment A, https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-strategy-and-operational-policy/nsw-ai-operational-policy (checked 2026-10-26).
- **Crosswalk used:** references/au-government-crosswalks.md, verified 2026-10-26 (source: adk-governance-pack reference, read 2026-10-28).
- **Version match:** gap: official page not re-read on 2026-10-28 (no web access); the platform's own wording is behind SectorLink and not public; agency: confirm the live questions.
- **Rating basis the form uses:** the Operational Policy's intrinsic band, set by the agency (assumption: any proposal here is intrinsic, not residual).

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Accountable Owner | agency: name and position once the agency names them; the Accountable Official is Ruth Abbott (docs/discovery/enquiries.md §5) | gap: whether the Accountable Owner is the same person |
| Approving officer | agency: name and position | gap |
| External suppliers | Southgate Labs as developer; Google as model and cloud provider | regulatory-memo.md Roles, D1, D6 |

## Draft answers

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| Reg 1 | Is an agency-approved AI system, platform or product used? | The agent is custom-built on google-adk with Gemini on Vertex AI (docs/architecture/enquiries.md Scope gate, D1); whether Gemini and Vertex AI are on the agency's approved list is unknown | D1, D6 | agency: approved list |
| Reg 2 | Does it automate or materially influence consequential decisions about a person? | Proposed no: it decides nothing and cannot change applications (docs/architecture/enquiries.md Scope gate); it reports a status and answers from guidance | C1, C2, M2 | agency: answers; counsel: confirm |
| Reg 3 | Is it elevated risk beyond routine productivity or analytical assistance? | Proposed yes: a public-facing agent with a tool that reads applicants' personal information (R2, C2, docs/discovery/enquiries.md §3) | R2, C2 | agency: answers |
| Reg 4 | Is it experimental use only, on synthetic, public or non-sensitive data in an isolated environment? | Proposed no: the pilot uses real application status data and real public transcripts (docs/architecture/enquiries.md Scope gate) | docs/architecture/enquiries.md Scope gate | agency: answers |
| Registration | Agency, responsible officer and use case details | Agency: NSW Trades Licensing Office. Use case: a public web chat assistant on the "Apply for a licence" pages that answers licensing questions from published guidance and checks application status; six-week pilot; decision 2026-12-10; contract TLO-2026-031, 2026-09-15 to 2027-09-14 | docs/discovery/enquiries.md §1, §6, `docs/contract/order-form-summary.md` | agency: officer and use case owner |

## Questions for the agency

- agency: is Gemini on Vertex AI on the approved list; needed by W5.
- agency: who is the Accountable Owner who registers (the vendor does not register); needed by W5.
- agency: which version of the platform questions applies now; needed by W5.

## Questions for counsel

- counsel: is a guidance answer or status read-out ever a decision that materially influences a person for Reg 2; needed by W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| AIAF Accountable Owner (agency: to be named) | this document | pending | pending |
