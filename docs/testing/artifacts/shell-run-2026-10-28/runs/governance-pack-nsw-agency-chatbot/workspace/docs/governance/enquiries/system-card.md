---
document: system-card
system: Public enquiries assistant
version: build v0.7.0
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Accountable Official for AI (Ruth Abbott)
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md
---

# System card: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for the NSW Trades Licensing Office's reviewers. It describes build v0.7.0 and nothing later. Not legal advice. Every statement cites a design, plan or evidence ID, a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** answer licensing questions from the Office's published guidance with a link, and report a caller's application status when they give the application number and the applicant's date of birth; hand over to the contact centre (R1, R2, R3).
- **Users:** members of the public on the "Apply for a licence" pages during a six-week pilot (docs/discovery/enquiries.md §6); gap: expected number of users.
- **Deployer and provider:** the Office puts it into service; Southgate Labs built it and supports it (D6, docs/discovery/enquiries.md §5); counsel: roles in regulatory-memo.md.
- **Decisions it informs:** none; it cannot decide or change applications (docs/architecture/enquiries.md Scope gate).

## Out-of-scope use

- Deciding or changing applications, and payments (docs/architecture/enquiries.md Scope gate).
- Guessing others' applications, limited by matching and a three-failure block (C2, C3).
- Questions the guidance does not answer: it hands over instead (C1, C4).

## Limits

- On 400 historical enquiries, 94% of answers cited a correct guidance page, so about 6% did not (M1); offline only, not measured on live callers.
- Scripted attempts: 0 status lookups returned for a mismatched date of birth in 250 attempts (M2); not tested with real callers.
- Languages, accessibility needs and non-English callers have not been evaluated (gap: owner adk-agent-evaluation).
- **Model:** `gemini-3.5-flash-001`, retirement 2027-02-26 (D1, model page read 2026-10-20; not re-read on 2026-10-28). The contract's default six-month model-change notice cannot be met for that date; see regulatory-memo.md (D1, `docs/contract/order-form-summary.md`).

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Answers citing a correct guidance page | 94% | no threshold recorded: gap | 400 historical enquiries, 2026-10-13 to 2026-10-24, offline evaluation | v0.7.0 | M1 |
| Status lookups returned for a mismatched date of birth | 0 | 0 expected | 250 scripted attempts, 2026-10-13 to 2026-10-24, scripted tests | v0.7.0 | M2 |

Not yet measured: complaints about wrong or misleading information (baseline 14 a month), calls about application status (baseline 17,500 a month), handover time, bias and accessibility, screening of free-text disclosures (gap: owners adk-agent-evaluation and protect-adk-sensitive-data; docs/discovery/enquiries.md §2).

## Human oversight

- No person reviews answers before they are shown; the assistant makes no decision about a person (C1, C2). Share reviewed: n/a: no review step is in the design.
- A caller contests or corrects an answer by asking for a person: the handover reaches the contact-centre queue or a callback form (C4); gap: who owns corrections and the measured handover time.
- Stopping or rolling back the service: gap: no stop or rollback owner is recorded; the Office controls the website widget window (W1) and the pilot decision (docs/discovery/enquiries.md §6).

## Automated-decision disclosure

- **Kinds of personal information used:** application number, date of birth, application stage and missing documents; free text in chat (docs/discovery/enquiries.md §3, C2).
- **Decisions made solely by the system:** none (docs/architecture/enquiries.md Scope gate).
- **Decisions where the system does something substantially and directly related:** n/a: no decision about a person; it reads a status (C2); counsel: confirm.
- **Meaningful information about the logic:** guidance answers cite their source page (C1); a status is returned only when number and date of birth match, otherwise "we couldn't find that application" (C2).
- **Human review, representations and contest:** handover to the contact centre on request or when it cannot answer (C4).
- **Opt-out or appeal, where offered:** n/a: none required for a lookup; the contact centre remains available (C4); counsel: confirm.
- **Government client facts:** AIAF registration and the Office's transparency obligations are the agency's (W5); agency: the non-AI alternative is the contact centre (docs/discovery/enquiries.md §1, C4).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** gap: no contract covers an AI disclosure or its answer to "are you a human?"; proposed notice text is in privacy-impact-input-pack.md; goal for adk-agent-evaluation to test it.
- **Hand-off to a person:** the contact-centre queue or callback form (C4); gap: hours and measured connect time.
- **Persona, memory of the user or relationship features:** none recorded; no memory beyond the 90-day transcript (D3).
- **Public claims about the system:** the only recorded figures are M1 (94%) and M2 (0 of 250), offline and scripted; no accuracy claim should go beyond them (M1, M2).

## Data

- Reads published guidance and the licensing system's status API; stores transcripts for 90 days in Firestore in australia-southeast1 (D2, D3); transcripts may hold health and criminal-history disclosures (docs/discovery/enquiries.md §3).
- Screening of free text and log retention: gap; abuse-monitoring location and Brisbane support access are described in privacy-impact-input-pack.md (D4, D5).

## Contact

- **Owner:** Ruth Abbott, Deputy Commissioner and Accountable Official (docs/discovery/enquiries.md §5); agency: confirm the public contact.
- **Report a problem or make a privacy complaint:** agency: the Office's channel and its privacy officer, Sam Taylor (docs/discovery/enquiries.md §5); gap: no channel recorded.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Accountable Official for AI (Ruth Abbott) | this document | pending | pending |
| Privacy officer (Sam Taylor) | Automated-decision disclosure, AI disclosure and Data | pending | pending |
