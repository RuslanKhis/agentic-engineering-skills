---
document: impact-assessment
system: Kowhai Retail customer agent
version: design accepted 2026-09-09; build v0.6.1 (M1, M2)
status: draft
jurisdictions: [au, nz, sg]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: privacy officer (Aroha Ngata) and Data Protection Officer (Daniel Tan), for Mere Walker as risk owner
trigger: pilot decision of 2026-11-26 (docs/discovery/customer-agent.md §6)
sources: docs/discovery/customer-agent.md, docs/architecture/customer-agent.md, docs/plans/customer-agent.md, regulatory-memo.md
---

# AI system impact assessment: Kowhai Retail customer agent

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF
1.0 and NIST AI 600-1. Draft for Kowhai Retail's risk owner; scores are
provisional until they set them. Conformity to ISO/IEC 42005 needs the
client's own copy of the standard (source: adk-governance-pack reference impact-assessment.md, read 2026-10-25). Not legal advice.

## Scope and intended use

- **System and functions:** web chat agent that answers order and returns questions from CRM data and issues store credit; code decides eligibility and limit, the model composes the answer (R1, R2, C1, C2).
- **Intended use:** "where is my order", returns and refunds-as-store-credit enquiries for signed-in customers in New Zealand and Singapore (docs/discovery/customer-agent.md §2, R1, R2); **unintended or foreseeable misuse:** a customer or attacker tries to obtain credit for another person or above the limit, or to read another customer's order (C1, C2, C3; assumption: no adversarial test result is recorded, so prompt-injection resistance is a gap).
- **Organisation's role:** Kowhai Retail is deployer and Southgate Labs developer; Google is model provider (regulatory memo Roles; D1, D4; counsel).
- **Lifecycle stage and trigger:** pilot, 6 weeks, decision 2026-11-26 (G05, docs/discovery/customer-agent.md §6).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Signed-in customers in New Zealand and Singapore | Direct users; their order data is read and credit is written | assumption: no; children and customers in distress are not recorded either way (gap) | docs/discovery/customer-agent.md §3, R1 |
| Customers whose CRM data is outdated | Answers about orders are wrong | assumption: not vulnerable | M3 |
| Māori customers in New Zealand | Personal information and service impacts; engagement not recorded | gap | docs/discovery/customer-agent.md §3 |
| Service staff in each country | Receive handovers and callbacks | assumption: no | C4 |
| Southgate Labs engineers | Read traces with customer data | n/a: staff of the supplier | D4 |

## System information

- **Data:** CRM profile and order history read at the time of the question, store credit ledger written, chat transcripts kept (docs/discovery/customer-agent.md §3, D3, D5); 27% of test customers have an address older than 24 months (M3).
- **Model and logic:** Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`; gap: retirement date not read from the model page; deterministic code for eligibility, limit and idempotency (D1, C2, C3).
- **Deployment environment:** Cloud Run and Firestore in australia-southeast1, operated by Southgate Labs engineers during the pilot (D2, D4).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Customers and Kowhai | harm | Credit issued to the wrong customer or above policy; may disclose an order | assumption: low; M2 shows 0 in 200 scripted conversations | assumption: high for disclosure, medium for money | docs/discovery/customer-agent.md §4, C1, C2, M2 |
| H2 | Customers | harm | A wrong delivery or returns answer misleads a customer | assumption: medium; 93% correct on 300 test chats | assumption: medium | docs/discovery/customer-agent.md §4, M1 |
| H3 | Customers | harm | Old or wrong CRM data (an outdated address) leads to a wrong answer | assumption: medium; 27% of test customers affected | assumption: medium | docs/discovery/customer-agent.md §4, M3 |
| H4 | Customers | harm | Transcripts and traces retain personal data and are reused and read by Sydney engineers without a notice | assumption: medium | assumption: medium | D3, D4 |
| H5 | Customers | harm | Customer steered to store credit when a refund right exists | assumption: low; hypothesis: the policy offers store credit only | assumption: medium | R2; counsel |
| B1 | Kowhai and customers | benefit | More enquiries resolved in chat without an agent, from an 18% baseline (July 2026, FAQ bot) | hypothesis: no pilot result yet | n/a: | hypothesis: docs/discovery/customer-agent.md §2 |
| B2 | Kowhai | benefit | Counter-metric: store credit issued per 1,000 chats against a baseline of 31 (agents only) | hypothesis: no pilot result yet | n/a: | hypothesis: docs/discovery/customer-agent.md §2 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | Tool scoped to verified customer ID; eligibility and limit in code; idempotency key | in place, tested locally | C1, C2, C3, M2 |
| H1 | Adversarial test for prompt injection that forces credits | gap: proposed goal for adk-agent-evaluation | C2 |
| H2 | Answer from the CRM at question time; handover on request | in place, tested locally | M1, C4, D5 |
| H3 | Address freshness check or caveat in answers | gap: proposed goal for adk-workflow-design | M3 |
| H4 | Retention, masking and notice | gap: retention and masking not recorded; no notice text; proposed goals for protect-adk-sensitive-data | D3, D4 |
| H5 | Wording that states refund rights | gap: proposed goal for adk-model-and-output-contracts; counsel | R2 |

## Residual risk and decision

- After the measures, H1 is bounded by code and tested locally only, while H2, H3, H4 and H5 remain open (H1, H2, H3, H4, H5; C1, C2, M1, M3).
- **Accepted by:** gap: acceptance by Mere Walker as sponsor and decider; the privacy officer and DPO advise (docs/discovery/customer-agent.md §5).
- **Conditions that end acceptance:** a credit above limit or to a wrong customer in the pilot; a breach notifiable in either country; a change of the pinned model (C2, D1).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | Sponsor and decider named; the privacy officer, DPO and consultancy lead named; acceptance, policies and AI literacy for service staff not recorded (gap) | docs/discovery/customer-agent.md §5 |
| Map | Scope, parties and the regimes screened in regulatory-memo.md (Australia consultancy only, New Zealand, Singapore) | docs/discovery/customer-agent.md §1, §3 |
| Measure | M1 93% correct order status, M2 0 credit errors, M3 27% outdated addresses, all on test data; not measured: pilot resolution rate, handover time, adversarial resistance, bias (gap) | M1, M2, M3 |
| Manage | Contracts C1 to C4, security baseline SB01, SB03; runtime hardening deferred to production; no incident record | C1, C2, C3, C4, SB05 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| CBRN information or capabilities | n/a: narrow retail tool | none needed | R1, R2 |
| Confabulation | yes | CRM-grounded answers; 93% correct; suggested action IDs not recorded (gap) | M1, D5 |
| Dangerous, violent or hateful content | yes, low | no content screening evidence (gap) | R1 |
| Data privacy | yes | Per-customer scope; retention and masking gap | C1, D3, D4 |
| Environmental impacts | n/a: noted only, not measured | none | D1 |
| Harmful bias or homogenisation | yes, low | rule-based eligibility; no group measurement (gap) | C2 |
| Human-AI configuration | yes | handover on request; no review before credit; AI disclosure gap | C4, R3 |
| Information integrity | yes, low | answers are order facts; no marking decision | R1 |
| Information security | yes | route scoping, credential handling; runtime deferred; no red-team result (gap) | SB01, SB03, SB05 |
| Intellectual property | n/a: no third-party content generated or retrieved | none | R1 |
| Obscene, degrading or abusive content | yes, low | no screening evidence (gap) | R1 |
| Value chain and component integration | yes | model pinned; retirement date and Salesforce role gaps | D1, D5 |

## Monitoring and review

- Watch credits above limit or for ineligible returns (threshold 0, M2), correct order status answers (M1, no threshold set; gap), store credit per 1,000 chats against the baseline of 31, and handover share (gap) (docs/discovery/customer-agent.md §2, M2, M1).
- **Review triggers:** model change or retirement, a new country or customer group, an incident, a change in law (APP 1.7 from 10 December 2026, checked 2026-10-26), a change to the credit limit (D1, R2).

## Adverse impact and equality (if the system ranks, scores or decides about people)

Kept because code decides credit eligibility for customers (C2); no ranking or scoring exists.

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| Customers by country | gap: not measured | gap | gap | gap | M2 |

- **Less discriminatory alternatives considered and accessibility route:** handover to a person on request is the alternative route (C4); accessibility of the web chat is not recorded (gap; counsel: Human Rights Act s 65 good-reason facts, regime New Zealand).
- **Regime checklists:** New Zealand Human Rights Act s 65 good-reason facts: gap (M2).

## New Zealand: Responsible AI Guidance mapping and Māori impact

| Item | Content in this assessment | Evidence |
| --- | --- | --- |
| MBIE Responsible AI Guidance (private clients): inventory, PIA at design, security and jurisdictional risk, transparency | Inventory: this document; PIA: W2; security: SB01, SB03; jurisdictional risk: Sydney hosting (D2); transparency: notice text gap | D2, SB01, SB03, W2 |
| Algorithm Charter (signatory agencies) | n/a: private client, not a signatory on the record | docs/discovery/customer-agent.md §1 |
| Māori impact and engagement: data about Māori, noa or tapu classification, offshore storage rationale, engagement owner | gap: not recorded; Sydney hosting rationale for New Zealand data not recorded | D2; gap |
| Senior leadership approval (OPC expectation) | Mere Walker accepted the brief and design; approval of the pilot is the 2026-11-26 decision | docs/discovery/customer-agent.md §6 |

## Singapore: Agentic MGF mapping

| Dimension (Model AI Governance Framework for Agentic AI v1.5) | Content in this assessment | Evidence |
| --- | --- | --- |
| 1 Assess and bound the risks up front (error tolerance, sensitive data and memory, external systems, write actions, reversibility, autonomy) | Write action: store credit capped at NZD 150 or SGD 130 per order, once per return; external system: Salesforce; reversibility of a wrongly issued credit not recorded (gap); no persistent agent memory recorded beyond transcripts | R2, C2, C3, D3 |
| 2 Make humans meaningfully accountable (value-chain roles, approval checkpoints, override rate and review time) | Value-chain roles in regulatory-memo.md; no approval checkpoint before credit; override rate n/a: no review step; handover share gap | C2, C4 |
| 3 Technical controls and processes (change management on model updates, pre-deployment testing, gradual roll-out) | Model pinned; tests M1, M2; 6-week pilot as gradual roll-out; change management on model update not recorded (gap) | D1, M1, M2, docs/discovery/customer-agent.md §6 |
| 4 End-user responsibility (disclosure at the point of interaction, range of actions, escalation contacts) | Handover to a person on request; AI disclosure gap | R3, C4 |

- **Financial clients:** n/a: not MAS-regulated (assumption: docs/discovery/customer-agent.md §1).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer, Kowhai Retail Limited (Aroha Ngata) | New Zealand sections and shared sections of this document | pending | pending |
| Data Protection Officer, Kowhai Retail (Singapore) Pte. Ltd. (Daniel Tan) | Singapore sections and shared sections of this document | pending | pending |
