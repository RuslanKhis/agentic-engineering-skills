---
document: system-card
system: Kowhai Retail customer agent
version: build v0.6.1 (M1, M2)
status: draft
jurisdictions: [au, nz, sg]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: privacy officer (Aroha Ngata) and Data Protection Officer (Daniel Tan)
sources: docs/discovery/customer-agent.md, docs/architecture/customer-agent.md, docs/plans/customer-agent.md
---

# System card: Kowhai Retail customer agent

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Kowhai Retail reviewers. It describes the build named above and
nothing later. Not legal advice. Every statement cites a design, plan or
evidence ID, a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** answers "where is my order", returns and refunds-as-store-credit questions for signed-in customers, reads their order history from the CRM and issues store credit for an eligible return up to NZD 150 or SGD 130 per order (R1, R2, docs/discovery/customer-agent.md §2).
- **Users:** signed-in web chat customers of Kowhai Retail in New Zealand and Singapore, external, for a 6-week pilot; number of pilot customers not recorded (gap) (docs/discovery/customer-agent.md §6).
- **Deployer and provider:** Kowhai Retail Limited and Kowhai Retail (Singapore) Pte. Ltd. deploy it under the Kowhai name; Southgate Labs built it (docs/discovery/customer-agent.md §1, §5; regulatory-memo.md Roles).
- **Decisions it informs:** the customer decides whether to return an item; the tool decides eligibility and issues credit within the limit; a person receives the handover on request (C2, C3, C4).

## Out-of-scope use

- Cash refunds, changing orders and marketing messages (docs/architecture/customer-agent.md Scope gate).
- Reading another customer's orders; the tool is scoped to the verified customer ID and refuses otherwise (C1).
- Issuing credit twice for one return or above the limit (C2, C3).
- Use by customers outside New Zealand and Singapore, or by children; assumption: not designed or evaluated for them (docs/discovery/customer-agent.md §3).

## Limits

- Order status answers were correct in 93% of 300 test chats, so about 7% were not (M1).
- 27% of 300 test customers had a CRM address older than 24 months; the agent reads the CRM and cannot tell that an address is outdated (M3, D5).
- Evaluation used test chats and scripted conversations, not live customers (M1, M2).
- Not evaluated: live pilot chats, languages other than the test language, accessibility, adversarial prompts (gap: proposed goals for adk-agent-evaluation).
- **Model:** Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in australia-southeast1; retirement date not read (gap; proposed goal for adk-model-and-output-contracts) (D1).

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Correct order status answers | 93% | no threshold set (gap) | 300 test chats, 2026-10-06 to 2026-10-17 | v0.6.1 | M1 |
| Credits above the limit or for ineligible returns | 0 | 0 | 200 scripted conversations, 2026-10-06 to 2026-10-17 | v0.6.1 | M2 |
| CRM addresses older than 24 months among test customers | 27% | none | 300 customers, 2026-10-06 to 2026-10-17 | n/a | M3 |

Not yet measured: share of enquiries resolved in chat without an agent (baseline 18%) and store credit per 1,000 chats (baseline 31), measured by the pilot (gap: no goal records it; docs/discovery/customer-agent.md §2); handover time to connect (gap).

## Human oversight

- No person reviews or approves a credit before it is issued; a customer can ask for a person at any time (C2, R3, C4). Share of chats handed over and override rate: not measured (gap).
- A customer corrects an output by asking for a person; callback form if the queue is unavailable; owner of corrections not recorded (C4; gap).
- Stopping or rolling back the agent and who may do it are not recorded (D2; gap; proposed goal for adk-release-engineering).

## Automated-decision disclosure

- **Kinds of personal information used:** name, contact details, order history, return records and the customer's ID (D5, C1).
- **Decisions made solely by the system:** whether a return qualifies for store credit and its amount within the limit, with no person involved before issue (C2, C3; counsel: whether this is solely automated in any regime in scope).
- **Decisions where the system does something substantially and directly related:** the answer about order status and returns eligibility (R1, C2).
- **Meaningful information about the logic:** credit is issued only if the return is eligible and the amount is within the per-order limit; the eligibility rule is in code and its text is not recorded here (C2; gap: policy wording).
- **Human review, representations and contest:** a customer can ask for a person, or leave a callback request; no formal contest route is recorded (C4; gap).
- **Opt-out or appeal, where offered:** none recorded; n/a: no regime in scope requires one by statute, counsel to confirm (C4; counsel: New Zealand and Singapore have no automated-decision provision; APP 1.7 for the consultancy only from 10 December 2026, checked 2026-10-26).
- **Quebec s 12.1 notice and review (Canada):** n/a: Canada is not in scope (regulatory-memo.md Jurisdiction screen).
- **Government client facts:** n/a: private client (docs/discovery/customer-agent.md §1).
- **Australia, APP 1.8 block (consultancy's own policy):** kinds of information as above; decisions it does something substantially and directly related to as above; counsel: whether APP 1.8 applies to the consultancy (D4, C2).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** gap: no contract or test records when and how the agent says it is an AI or how it answers "are you a human?"; proposed goal for adk-model-and-output-contracts (R3).
- **Hand-off to a person:** reaches the service queue in the customer's country, with a callback form as fallback; hours and time to connect not recorded (C4; gap).
- **Persona, memory of the user or relationship features:** none recorded beyond kept transcripts of 12 months (D3).
- **Public claims about the system:** none recorded; any claim of accuracy or resolution rate cites M1 or the pilot result (M1; gap: pilot result).
- **Singapore chatbot info card inputs (external chat agents):** can do: answer order and returns questions, issue store credit within the limit, hand over to a person; cannot do: cash refunds, order changes or marketing (docs/architecture/customer-agent.md Scope gate); reliability: M1 and M2; user data: processed by Google Cloud in Sydney, chats kept 12 months and reused for evaluation, engineers in Sydney read traces (D1, D3, D4); how to report issues: gap; first-use statement: gap; card version and date: build v0.6.1, 2026-10-28.
- **Ontario job-posting disclosure:** n/a: no applicant screening (R1, R2).

## Data

- Reads customer profile, order history and the store credit ledger; keeps chat transcripts for 12 months (docs/discovery/customer-agent.md §3, D3, D5; privacy-impact-input-pack.md).
- Per-customer scope and limit checks are in place, tested locally; masking and screening of prompts, logs and traces are not evidenced (C1, C2; gap: proposed goal for protect-adk-sensitive-data); the Salesforce integration user with the credit permission was granted 2026-09-30 (W1).

## Contact

- **Owner:** Mere Walker, General Manager, Customer, Kowhai Retail, as sponsor and decider (source: General Manager, Customer, discovery brief accepted 2026-08-19).
- **Report a problem or make a privacy complaint:** gap: no channel is recorded; Aroha Ngata (New Zealand privacy officer) and Daniel Tan (Singapore DPO) are the privacy contacts named in the record (docs/discovery/customer-agent.md §5).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer, Kowhai Retail Limited (Aroha Ngata) | New Zealand facts and shared sections of this document | pending | pending |
| Data Protection Officer, Kowhai Retail (Singapore) Pte. Ltd. (Daniel Tan) | Singapore facts and shared sections of this document | pending | pending |
