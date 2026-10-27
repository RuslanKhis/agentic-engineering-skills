---
document: system-card
system: Claims triage assistant (Compensation Claims Office)
version: build v0.6.3
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO Privacy Officer (James Whitlam)
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md
---

# System card: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for CCO reviewers. It describes build v0.6.3 and nothing later. Not legal advice. Every statement cites a design, plan or evidence ID, a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** drafts a triage recommendation (category, priority, missing evidence) for a new claim, citing the claim passages relied on (R1, R2).
- **Users:** claims officers, internal; 20 in the Canberra pilot for 8 weeks (docs/discovery/claims-triage.md §6).
- **Deployer and provider:** the CCO deploys; Southgate Labs develops; Google provides the model and cloud (regulatory-memo.md Roles; D1).
- **Decisions it informs:** the officer's triage decision; the assistant writes nothing to the case system (R4, C3).

## Out-of-scope use

- Determining liability or payment, and contacting claimants (docs/architecture/claims-triage.md Scope gate).
- Reading claims outside the officer's team queue, limited by team-scoped access (R3, C1).
- Relying on the draft without reading the claim notes, a foreseeable misuse; the control is that passages are cited (docs/discovery/claims-triage.md §4, C2); review depth is not measured (gap).

## Limits

- On 900 past claims, the draft category matched the officer's decision 88% of the time and the priority 79% (M1, M2). A wrong low priority delays payment (docs/discovery/claims-triage.md §4).
- Not evaluated: groups of claimants, languages, claim types by volume, unreadable or very long attachments (gap: no breakdown reported).
- **Model:** `gemini-3.5-flash-001` (D1); retirement date: gap: not read from the provider's lifecycle page (no network); propose a check by adk-model-and-output-contracts.

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Draft category matching officer decision | 88% | gap: no threshold set | 900 past claims, 2026-10-06 to 2026-10-17 | v0.6.3 | M1 |
| Draft priority matching officer decision | 79% | gap: no threshold set | 900 past claims, 2026-10-06 to 2026-10-17 | v0.6.3 | M2 |

Not yet measured: share of triage decisions changed by officers in the pilot (baseline 11%, docs/discovery/claims-triage.md §2); time from lodgement to triage decision (baseline 6 working days); group-level results; review depth (gap: needs a pilot measurement goal). Missing: a written evaluation report path (gap: the plan cites M records only).

## Human oversight

- The officer accepts or changes every draft and the decision is recorded with the draft (R4, C4); share of drafts changed: gap: not measured.
- How a claimant contests a triage outcome, and who owns corrections: agency: not recorded; the assistant does not decide liability or payment (docs/architecture/claims-triage.md Scope gate).
- How the system is stopped or rolled back, and by whom: gap: no kill switch is recorded (DTA tool 6.7; goal for adk-release-engineering).

## Automated-decision disclosure

- **Kinds of personal information used:** claim form and notes, including injury and medical details, mental-health history, employment history and sometimes family violence disclosures, and attached medical reports (docs/discovery/claims-triage.md §3).
- **Decisions made solely by the system:** none recorded; the officer accepts or changes every draft (R4, C4).
- **Decisions where the system does something substantially and directly related:** drafts a category, priority and list of missing evidence for the triage of a claim (R1; counsel: APP 1.7, from 10 December 2026, checked 2026-10-26).
- **Meaningful information about the logic:** a generative model reads the claim and drafts the three outputs; each field cites claim passages and a draft without citations is withheld (R2, C2). No scores or weights are published.
- **Human review, representations and contest:** officer review is built (C4); route for a claimant to contest: agency: not recorded.
- **Opt-out or appeal, where offered:** agency: not recorded; counsel: whether any is required.
- **Government client facts:** DTA transparency statement entry, non-AI alternative and contest route are the agency's (government-form-answers-dta-transparency-statement.md; agency: owner).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** n/a: officers use a drafting tool; no conversation with claimants (R4, docs/architecture/claims-triage.md Scope gate). Disclosure to claimants that AI informs triage: agency: not recorded (privacy-impact-input-pack.md).
- **Hand-off to a person:** n/a: the officer is the person.
- **Persona, memory of the user or relationship features:** none recorded (docs/architecture/claims-triage.md Contracts).
- **Public claims about the system:** none recorded; any figure quoted publicly cites M1 and M2 (gap: no claims approved).

## Data

- Reads claims in the officer's team queue; stores the draft and the officer's decision in the decisions table; logs prompts and drafts for 30 days; hosts in australia-southeast1 (C1, C4, D2, D3; privacy-impact-input-pack.md).
- Screening of sensitive information before the model or logs: gap: no evidence recorded; goal for protect-adk-sensitive-data.

## Contact

- **Owner:** CCO Assistant Secretary, Claims Operations (source: discovery brief, Helen Park, 2026-09-02).
- **Report a problem or make a privacy complaint:** agency: CCO channel not recorded; gap.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO Privacy Officer (James Whitlam) | this document | pending | pending |
