---
document: system-card
system: HR assistant (Érable Logistics)
version: build v0.5.0
status: draft
jurisdictions: [au, ca]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Me Geneviève Roy, counsel, Érable Logistics Inc.
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# System card: HR assistant (Érable Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Érable Logistics reviewers. It describes build v0.5.0 and nothing later. Not legal advice. Every statement cites a design, plan or evidence ID, a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** answers HR policy questions in French or English, takes leave requests and approves routine ones (R1, R2, R3).
- **Users:** distribution-centre staff in Montréal (1,150) and Toronto (640); the pilot is one shift per centre for 6 weeks; internal (docs/discovery/hr-assistant.md §1, §6).
- **Deployer and provider:** Érable deploys it under its own name; Southgate Labs built it (regulatory-memo.md Roles; counsel: confirm).
- **Decisions it informs:** it approves leave requests under two days by itself when the balance covers them and no blackout date applies; all other requests go to the employee's manager (C3, C5).

## Out-of-scope use

- Pay, discipline and leave of two days or more (docs/architecture/hr-assistant.md Scope gate).
- An employee reading or requesting leave for another employee, limited by a tool scoped to the verified employee ID (C2).
- Refusing a request: the assistant never refuses; a request failing the rule goes to the manager (C3).

## Limits

- Policy answers cited the right section in 92% of 300 questions (M1); the other 8% did not.
- Dates and leave type were extracted correctly in 98.4% of 500 replayed requests (M3), so some requests may be mis-extracted and then decided by the rule.
- Not evaluated: employee confirmation of extracted dates, performance by language or site on extraction (M3 gives no split), and behaviour on live pilot traffic (gap: proposed goal for adk-agent-evaluation).
- **Model:** `gemini-3.5-flash-001` (D1); gap: retirement date not read (no network), proposed goal for adk-model-and-output-contracts.

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Policy answers citing the right section | 92% | threshold not set (gap) | 300 questions (150 French, 150 English), 2026-10-05 to 2026-10-16 | v0.5.0 | M1 |
| Share of pilot-shape leave requests the rule approves without review | 64% | n/a: descriptive | 500 requests replayed from July 2026, 2026-10-05 to 2026-10-16 | v0.5.0 | M2 |
| Dates and leave type extracted correctly | 98.4% | threshold not set (gap) | 500 requests, 2026-10-05 to 2026-10-16 | v0.5.0 | M3 |

Not yet measured: leave decisions reversed after complaint with the assistant (baseline 1.2% before it, docs/discovery/hr-assistant.md §2); median hours from request to decision with the assistant (baseline 31 hours, docs/discovery/hr-assistant.md §2); bias by group (gap).

## Human oversight

- No person reviews an auto-approved request (C4); the manager sees every other request in the UKG queue (C5). The measured share approved without review in replay is 64% (M2). gap: pilot review share and override rate.
- Contest or correction route for an auto-approved decision: gap: none designed; a manager or HR route is proposed for the s 12.1 review (counsel: what Quebec requires).
- Stop or roll back: gap: no kill switch, owner or rollback unit recorded in the plan; proposed goal for adk-release-engineering.

## Automated-decision disclosure

- **Kinds of personal information used:** employee ID, site, role, manager and leave balances from UKG; requested dates and leave type; the leave reason text may reach the model (C2, C3, docs/discovery/hr-assistant.md §3).
- **Decisions made solely by the system:** approval of leave under two days (C3, C4).
- **Decisions where the system does something substantially and directly related:** n/a: the assistant only routes other requests to a person, who decides (C5).
- **Meaningful information about the logic:** a rule checks that the leave is under two days, the balance covers it and no blackout date applies; the model only extracts dates and leave type (C3, D5).
- **Human review, representations and contest:** gap: no route for an employee to submit observations to a staff member, or to have the personal information used corrected, after an automated approval (C4; counsel: s 12.1).
- **Opt-out or appeal, where offered:** gap: none designed; employees could submit to the manager instead (assumption: the manager route is available on request; counsel: whether an alternative must be offered).
- **Quebec s 12.1 notice and review (Canada):** the person must be told no later than when the decision is communicated; on request they get the personal information used, the reasons and principal factors, and may have it corrected and submit observations to a staff member who can review the decision (checked 2026-10-26; wording reported; not confirmed at the source on 2026-10-26). Not built (gap: proposed goal for adk-operational-guardrails; counsel: applies to a favourable decision?).
- **Government client facts:** n/a: private client (docs/discovery/hr-assistant.md §1).
- **Australian APP 1.8 entries:** n/a: no Australian individuals' decisions (regulatory-memo.md Australia: Automated decisions).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** gap: no contract records an AI disclosure; proposed text for the first message, in French and English, for counsel to settle (counsel: Charter of the French Language and s 12.1 wording).
- **Hand-off to a person:** policy answers without a citation go to HR (C1); non-routine leave goes to the manager (C5). gap: no measured time to connect.
- **Persona, memory of the user or relationship features:** none designed; the only retained history is the 60-day log (R1 to R4, D3).
- **Public claims about the system:** none made; any claim such as "92% accurate" must cite M1 and its sample (M1).
- **Ontario job-posting disclosure:** n/a: the assistant does not screen, assess or select applicants (R1 to R4).

## Data

- Reads UKG profile and leave balances; writes leave requests and decisions to UKG; logs prompts and answers with employee ID for 60 days (C2, C4, D3; privacy-impact-input-pack.md).
- Hosted in Toronto; the model processes in the United States; Sydney engineers read logs (D1, D2, D4). Screening and pseudonymisation: gap: none recorded.

## Contact

- **Owner:** Luc Tremblay, Vice-President, People, as sponsor and decider (docs/discovery/hr-assistant.md §5); gap: owner contact details not confirmed.
- **Report a problem or make a privacy complaint:** Marie-Claude Gagnon, person in charge of the protection of personal information (docs/discovery/hr-assistant.md §5); gap: channel and published contact not confirmed by Érable.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Me Geneviève Roy, counsel, Érable Logistics Inc. | this document | pending | pending |
