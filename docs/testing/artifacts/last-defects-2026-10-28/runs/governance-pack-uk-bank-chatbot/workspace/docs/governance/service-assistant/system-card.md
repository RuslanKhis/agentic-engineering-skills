---
document: system-card
system: Thamesbridge customer service assistant
version: build v0.8.0
status: draft
jurisdictions: [au, eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: UK DPO (Oliver Grant), Ireland DPO (Siobhán Kelly) and group CISO (Rachel Adeyemi)
sources: docs/discovery/service-assistant.md, docs/architecture/service-assistant.md, docs/plans/service-assistant.md
---

# System card: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Thamesbridge reviewers. It describes build v0.8.0 and nothing later. Not legal advice. Every statement cites a design, plan or evidence ID, a dated source, or is marked `assumption:` or `counsel:`. Controls evidenced only in local tests are "in place, tested locally", not "in production".

## Intended use

- **Purpose:** in-app chat that answers balance and transaction questions, freezes a card after the customer confirms, and explains a declined overdraft from the decision engine's reason codes (R1, R2, R3).
- **Users:** opted-in retail customers, 5,000 in the UK and 1,000 in Ireland, for an 8-week pilot; external users (docs/discovery/service-assistant.md §6).
- **Deployer and provider:** Thamesbridge Bank plc for UK customers and Thamesbridge Bank Ireland DAC for Irish and EU customers; built and supported by Southgate Labs (regulatory-memo.md Roles; D4; counsel: confirm).
- **Decisions it informs:** none; the CreditLens decision engine makes every credit decision and the assistant may not decide, promise or change one; it can freeze a card only after confirmation (D3, R4, C2).

## Out-of-scope use

- Making or changing credit decisions, payments and unfreezing cards (docs/architecture/service-assistant.md Scope gate, D5).
- Promising that a decision will change or inviting a reapplication outcome; limited by an output check (C4).
- Reading another customer's accounts; limited by the verified customer ID scope (C1).
- Advice on credit, debt or financial difficulty: assumption: out of scope; gap: no control or refusal test is recorded.
- Use by customers under 18 or outside the UK and the EU countries served: gap: not recorded (docs/discovery/service-assistant.md §6).

## Limits

- Explanations matched the decision engine's reason codes in 99.2 % of 500 synthetic declined applications; the other 0.8 % did not match and real customer traffic is untested (M1).
- Freezes needed confirmation in all 300 scripted conversations, with 0 executed without it; missed freezes and wrong-card freezes were not measured (M2, C2).
- The 41 % resolved without transfer comes from 120 staff test chats and is not comparable with the 22 % baseline from the existing menu bot on customer traffic (M3, docs/discovery/service-assistant.md §2).
- Not evaluated: languages other than English, accessibility needs, customers in vulnerable circumstances, groups (gap: no goal; proposed for adk-agent-evaluation).
- **Model:** gemini-3.5-flash-001 pinned (D1); gap: retirement date and processing region not read, no network access and the lifecycle table is not installed; proposed goal for adk-model-and-output-contracts.

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Overdraft explanations matching the decision engine's reason codes | 99.2 % | gap: no threshold recorded | 500 synthetic declined applications, 2026-10-05 to 2026-10-16 | v0.8.0 | M1 |
| Freezes executed without confirmation | 0 | 0 | 300 scripted conversations, 2026-10-05 to 2026-10-16 | v0.8.0 | M2 |
| Resolved without transfer on the test journey | 41 % | 22 % (July 2026, existing menu bot) | 120 staff test chats, 2026-10-12 to 2026-10-16 | v0.8.0 | M3 |

Not yet measured: complaints mentioning the chat per 10,000 chats (baseline 3.1, docs/discovery/service-assistant.md §2), cross-customer isolation on real traffic, hand-off time, pseudonymisation coverage; measured by a goal for adk-agent-evaluation and protect-adk-sensitive-data (gap:).

## Human oversight

- A person confirms every card freeze (C2); the assistant hands over to an agent when an explanation fails validation (C3). gap: the share of chats handed over, the override rate and the hand-off time are not measured.
- A customer can contest a decision or an explanation only through the bank's own routes; gap: no route is recorded and the assistant cannot promise a change (R4, C4).
- Stopping or rolling back the pilot, and who can do it: gap: no rollback or kill-switch owner is recorded; proposed goal for adk-release-engineering (docs/plans/service-assistant.md).

## Automated-decision disclosure

- **Kinds of personal information used:** account balances, transactions including merchant names, card status, overdraft decision and reason codes, chat text (docs/discovery/service-assistant.md §3).
- **Decisions made solely by the system:** none by the assistant; the decision engine, run by Thamesbridge, makes overdraft decisions (D3, R4; counsel: whether the engine's declines are solely automated significant decisions under GDPR Article 22 and UK Articles 22A to 22D).
- **Decisions where the system does something substantially and directly related:** it explains a decline from reason codes and does not rank, score or recommend (C3, R3).
- **Meaningful information about the logic:** the explanation is the engine's reason codes for that application, worded by the model; no counterfactual is produced (C3; gap: counterfactual not offered).
- **Human review, representations and contest:** gap: the route and its owner are not recorded (C3, R4).
- **Opt-out or appeal, where offered:** the pilot is opt-in (docs/discovery/service-assistant.md §6); gap: the opt-out route and an appeal route for declines; counsel: required by the regimes in scope.
- **Australia, APP 1.8:** n/a: no Australian customers and no decision by the consultancy (D4).
- **Quebec s 12.1, government client facts:** n/a: no Canadian or government client (docs/discovery/service-assistant.md §1).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** the chat header says the customer is talking to the bank's assistant (D6); gap: the wording does not say AI, there is no contract or test, and the reply to "are you a human?" is not recorded; EU Article 50(1) applies from 2 August 2026 (checked 2026-10-26).
- **Hand-off to a person:** handover on a failed explanation (C3), and a transfer to an agent exists as the baseline measure (docs/discovery/service-assistant.md §2); gap: route, hours and connection time are not recorded or measured.
- **Persona, memory of the user or relationship features:** none recorded (D2; assumption: none; gap: confirm no cross-session memory).
- **Public claims about the system:** the client has made none in the record; any claim about resolution or accuracy must cite M1, M2 or M3 and not the 41 % as customer performance (gap: no claims register).
- **Singapore chatbot info card, Ontario job-posting disclosure:** n/a: neither regime is in scope (docs/discovery/service-assistant.md §1).

## Data

- Reads balances, transactions, card status and decision reason codes for the signed-in customer; stores transcripts, logs and traces; pseudonymised transcript copies are kept for support (docs/discovery/service-assistant.md §3, D2, C5; privacy-impact-input-pack.md).
- Own-account scope and transcript pseudonymisation are in place, tested locally; gap: log and trace content, retention and erasure, and merchant-name masking (C1, C5).
- Personal data is processed in London and Belgium, with Southgate Labs access from Sydney (D2, D4; transfer-assessment.md).

## Contact

- **Owner:** Laura Whitfield, Director of Customer Operations, is sponsor and decider (docs/discovery/service-assistant.md §5); gap: the operational contact is not confirmed by the client.
- **Report a problem or make a privacy complaint:** gap: the channel and the data protection complaint route (DPA 2018 s 164A, in force from 19 June 2026, checked 2026-10-26) are not confirmed by the client; the DPOs are Oliver Grant (UK) and Siobhán Kelly (Ireland) (docs/discovery/service-assistant.md §5).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| UK DPO (Oliver Grant) | this document | pending | pending |
| Ireland DPO (Siobhán Kelly) | this document | pending | pending |
| Group CISO (Rachel Adeyemi) | Limits, Human oversight and Data | pending | pending |
