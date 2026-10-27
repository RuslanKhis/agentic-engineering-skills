---
document: system-card
system: Staff HR assistant (Wattle & Co)
version: build v0.4.1 (M1 to M3)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Privacy Officer (Grace Nguyen)
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# System card: Staff HR assistant (Wattle & Co)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Wattle & Co reviewers. It describes the build named above and nothing
later. Not legal advice. Every statement cites a design, plan or evidence ID,
a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** staff ask about their own leave balance, roster and HR policy; managers ask about leave and attendance of people who report to them (R1, R2).
- **Users:** pilot of 300 staff and 25 managers in NSW stores; 4,800 staff in the design; internal only (docs/discovery/hr-assistant.md §1 and §6).
- **Deployer and provider:** Wattle & Co deploys; Southgate Labs builds (regulatory memo, Roles; counsel: confirm).
- **Decisions it informs:** a manager's performance conversation can be informed by an attendance summary (D6); it cannot approve or change leave or rosters (R4, C3).

## Out-of-scope use

- Approving or changing leave, and any write to Workday (docs/architecture/hr-assistant.md, Scope gate; C3).
- Viewing another person's records unless the user manages them (R3, C1, C2).
- Treating an attendance summary as a finding or a reason for a decision without checking the listed records and the person's context (docs/discovery/hr-assistant.md §4, C5); assumption: this wording is proposed, the manager guide's wording is not in the record.
- Typing health, family or union information into prompts: masking of these is incomplete (C4, M2).

## Limits

- Masking caught 82% of synthetic prompts with union and medical phrases; it missed "my delegate", "SDA meeting", "physio" and "IVF appointment" and similar (M2).
- 3% of 240 leave-balance test questions were wrong (M1); 5% of 60 attendance summaries did not match Workday (M3).
- Error reports with request and response bodies go to a Sentry project in the US region (D4); this is not a Sydney-only system.
- Not evaluated: policy answers, bias, Victoria and Queensland data, real manager use (gap: no recorded measure).
- **Model:** `gemini-3.5-flash-001` in australia-southeast1 (D1); gap: retirement date and processing region not read in this session.

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Correct leave balances | 97% | none recorded | 240 questions, 2026-10-12 to 2026-10-16 | v0.4.1 | M1 |
| Sensitive phrases masked in logged prompts | 82% | none recorded | 150 synthetic prompts, 2026-10-12 to 2026-10-16 | v0.4.1 | M2 |
| Attendance summaries matching Workday | 95% | none recorded | 60 summaries, 2026-10-12 to 2026-10-16 | v0.4.1 | M3 |

Not yet measured: answers staff mark wrong (target under 5%), measured by G05 (docs/discovery/hr-assistant.md §2; gap: unmeasured).

## Human oversight

- A manager reads the summary and its source records and decides what to do (C5, D6); gap: share checked and override rate unmeasured.
- Contest or correction: gap: a team member has no route to contest a summary; staff errors are corrected in Workday (R4, C3); owner not named.
- Stop or roll back: gap: no kill switch or rollback owner recorded; ADK runtime baseline is deferred (SB05, deferred: production).

## Automated-decision disclosure

- **Kinds of personal information used:** leave balances and history, rosters, clock-in, lateness and absences, plus anything typed into prompts (docs/discovery/hr-assistant.md §3).
- **Decisions made solely by the system:** none (R4, C3).
- **Decisions where the system does something substantially and directly related:** a summary of a team member's attendance prepared before a performance conversation (D6, C5); counsel: APP 1.7 from 10 December 2026 (checked 2026-10-26).
- **Meaningful information about the logic:** the model summarises Workday attendance records the manager is entitled to see and lists them (C2, C5).
- **Human review, representations and contest:** manager review (C5); gap: no representation route for the team member.
- **Opt-out or appeal, where offered:** gap: none designed; counsel: whether required.
- **Government client facts:** n/a: private client.

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** gap: no disclosure contract exists in C1 to C5.
- **Hand-off to a person:** gap: route to the HR service centre not recorded.
- **Persona, memory of the user or relationship features:** gap: session memory design is not in the record; goal G01 is verified_local.
- **Public claims about the system:** accuracy claims limited to M1 (97% of 240 balances) and M3 (95% of 60 summaries); no other claim is supported.

## Data

- Reads Workday leave, roster and time data; logs masked prompts and answers for 30 days; sends error bodies to Sentry in the US; engineers in Sydney read logs and Sentry (D3, D4, D5; privacy-impact-input-pack.md).
- Screening: phrase-list masking before logging (C4, M2); gap: not recorded as applying to Sentry.

## Contact

- **Owner:** Marcus Bell, Chief People Officer (source: docs/discovery/hr-assistant.md §5, accepted 2026-09-10).
- **Report a problem or make a privacy complaint:** gap: no channel confirmed; proposed: Privacy Officer (Grace Nguyen) (source: docs/discovery/hr-assistant.md §5).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy Officer (Grace Nguyen) | this document | pending | pending |
