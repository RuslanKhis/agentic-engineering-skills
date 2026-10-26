# Jurisdiction screen

Read before drafting anything. The screen decides which regimes' sections
each draft carries. It is the first step of every pack, including a
proof-of-concept note and a single requested document.

Sources: the four research notes this skill was built from, each read on 26
October 2026 (`docs/research/au-ai-privacy-law-2026-10-26.md`,
`us-ai-privacy-law-2026-10-26.md`, `eu-ai-privacy-law-2026-10-26.md` and
`uk-ai-privacy-law-2026-10-26.md` in the skills repository), and the
regime references they produced: [Australia](australia.md),
[United States](united-states.md), [EU AI Act](eu-ai-act.md),
[privacy and records](privacy-and-records.md) and
[United Kingdom](united-kingdom.md).

## The order never changes

Australia, United States, EU, United Kingdom. The consultancy is in
Australia, so Australia is screened first even when the client is not. Every
list, table and front-matter value keeps this order: `jurisdictions: [au,
us, eu, uk]`, with the codes that are in scope only.

## Facts to establish

Take each fact from the record with its ID, or from the user with
`source: <role>, <date>`. A fact you cannot find is a `gap:` line, and every
regime it could trigger stays in scope until it is resolved, because writing
a section counsel strikes out costs less than missing one.

| Fact | Why it matters | Usual home in the record |
| --- | --- | --- |
| Where the client is established and carries on business | Establishment brings a regime's privacy law in on its own | Brief stakeholders; SOW parties |
| Where the data subjects are: users, employees, applicants, customers, people named in records | Most regimes follow the people, not the servers | Brief §4 data register; design users |
| Where processing happens: hosting region, the model's processing region (from the model page, which can differ from where the endpoint is offered), logs, grounding, abuse monitoring, telemetry sinks, backups | Transfers and overseas disclosure | Design hosting and model decisions (D IDs) |
| Who at the consultancy can see personal data, and from where: build, test, evaluation sets, log and trace review, support, incidents | Australian staff access is a restricted transfer for EU and UK data, and brings the consultancy's own Privacy Act position into scope | Design operations and access decisions; SOW support terms |
| Client type: private company; Australian Commonwealth agency; state or local government; UK central government department or arm's-length body; US federal agency or contractor | Government clients carry mandatory assessments (DTA, ATRS) and public-law duties | Brief stakeholders |
| Sector: finance, health, insurance, credit, employment, education, telecommunications marketing | Sector statutes and regulators | Brief context |
| Decision effects: does an output decide, or feed a decision about, a person's job, money, credit, housing, insurance, health, education, a benefit or access to a service? Is a person's review measured? | Automated-decision rules in all four regimes; counsel triggers | Design contracts (C IDs), plan M records |
| Channel: consumer-facing chat, voice, outbound messages, public web | Chatbot disclosure, consumer law, marketing rules | Design channels |
| Children likely to use it; biometrics; health or other sensitive data in free text | Counsel triggers and stricter consent | Brief §4; design screening contracts |

## When each regime is in scope

| Regime | In scope when any of these holds | Notes |
| --- | --- | --- |
| `au` Australia | The client is established or carries on business in Australia; data subjects are in Australia; or the consultancy's staff or systems handle personal information for the project | When only the consultancy's own handling brings it in, the Australian sections cover that handling (the consultancy's APP entity status, APP 8 and 11, notifiable data breaches) and say so; whether the Privacy Act reaches it is `counsel:` |
| `us` United States | The client is established or does business in the US; the data subjects include US residents (consumers, employees or applicants); the client is a US federal agency or contractor | Data merely stored or routed in the US does not bring state privacy laws in; it is a transfer question for the other regimes |
| `eu` EU | The client is established in the EU; the system offers goods or services to, or monitors, people in the EU; the system is placed on the EU market or its output is used in the EU (AI Act) | GDPR territorial scope (Article 3) and AI Act scope (Article 2) are `counsel:` conclusions; record the facts |
| `uk` United Kingdom | The client is established in the UK; the system offers goods or services to, or monitors, people in the UK; the client is a UK central government department or in-scope arm's-length body | UK GDPR territorial scope is a `counsel:` conclusion; a UK pack with EU users keeps the EU sections as well |

## Record the result

- **Front matter.** Every draft carries `jurisdictions: [<codes>]` in the
  order above. The checker fails a draft whose list is missing, empty,
  out of order or holds an unknown code, and fails a regime section whose
  code is not listed.
- **Screen table.** The regulatory memo (and the proof-of-concept note's
  Classification section) has one row for each of the four regimes,
  including the ones not in scope:

  | Regime | In scope | Trigger facts | Reason |
  | --- | --- | --- | --- |
  | Australia | yes | Consultancy staff in Sydney review traces (D7) | The consultancy's own handling; counsel: whether the Privacy Act reaches it |
  | United States | no | Customers in the UK and EU only (docs/discovery/x.md §4) | n/a: no US data subjects, client or processing purpose |
  | EU | yes | EU customers (R3) | Offers services to people in the EU |
  | United Kingdom | yes | Client established in London (source: client counsel, 2026-10-20) | Establishment |

  A `gap:` row reads "yes (gap: <fact missing>)", stays in scope and
  becomes a question for counsel or the client.
- **Practice profile facts** (see SKILL.md) can add a regime, never remove
  one the project record implies.

## What each regime adds to each document

| Document | `au` | `us` | `eu` | `uk` |
| --- | --- | --- | --- | --- |
| Regulatory memo | Australia: Privacy Act and roles; Automated decisions (APP 1.7); Sector, state and government AI policy | United States: Preemption, FTC and roles; Automated decisions and state AI laws; Privacy, sector and employment laws | EU: Prohibited practices; High-risk classification; Transparency obligations; General-purpose AI model | United Kingdom: UK GDPR and automated decisions; Equality, consumer, online safety and sector |
| Privacy impact input pack (PIA, DPIA, data protection and risk assessment) | Australia: APP compliance check; Australia: Inventory and notice inputs | United States: Notice, consent and opt-out; United States: Assessment approval | EU: Legal basis | United Kingdom: Lawful basis and ADM safeguards |
| Records of processing | Not written for `au` alone: Australia has no Article 30 register; the inventory section of the input pack replaces it | Not written for `us` alone | Written | Written |
| Transfer assessment annex | APP 8 facts live in the input pack | n/a | Written when EU personal data leaves the EEA, including Australian staff access | Written when UK personal data leaves the UK, including Australian staff access |
| System card | APP 1.8 block in the automated-decision disclosure | ADMT and chatbot disclosure facts | GDPR Articles 13 to 15 and 22 facts; Article 50(1) | Article 22C facts; complaint route |
| Security questionnaire | Notifiable data breach clocks and sector clocks | Breach and Safeguards clocks | GDPR, NIS2, CRA clocks | UK GDPR clocks |
| Impact assessment | Guidance for AI Adoption mapping; DTA AI impact assessment inputs for Commonwealth clients | Adverse impact (employment, credit); NIST AI 600-1 actions with red-team results for Texas | FRIA crosswalk where Article 27 applies | Equality and Consumer Duty rows |

## Documents the pack names but the client's process produces

These are named in the memo with their owner and wait; the pack supplies
inputs from its own sections and does not draft the document:

| Document | Regime and trigger | Inputs come from |
| --- | --- | --- |
| DTA AI impact assessment and the agency's AI transparency statement | Australia: a non-corporate Commonwealth entity client with an in-scope use case; the assessment is due for in-scope use cases by 15 December 2026 (checked 2026-10-26) | Impact assessment section "Australia: DTA AI impact assessment inputs"; system card |
| NSW AI Assessment Framework entry | Australia: NSW agency client; the platform has been mandatory since 30 September 2026 (checked 2026-10-26) | Impact assessment; privacy impact input pack |
| Bias audit by an independent auditor | United States: NYC Local Law 144 (automated employment decision tool used on NYC candidates or employees) | Impact assessment section "Adverse impact and equality" |
| Consumer notices (pre-use ADMT notice, adverse-outcome explanation, opt-out or appeal) | United States: CPPA ADMT and Colorado SB 26-189 | System card section "Automated-decision disclosure" |
| ATRS record | United Kingdom: central government department or in-scope arm's-length body, tool in Beta, Pilot or Production with public effect or public interaction | System card, privacy impact input pack, impact assessment |
| Online Safety Act risk assessments | United Kingdom: users can share outputs, the agent searches several sites or databases, or it can generate pornography | Memo `gap:` with its owner |
| Fundamental rights impact assessment | EU: Article 27 deployer of an Annex III system | Impact assessment section "FRIA crosswalk" |
