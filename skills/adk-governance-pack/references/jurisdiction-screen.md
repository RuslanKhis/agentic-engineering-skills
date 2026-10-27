# Jurisdiction screen

<!-- verified: 2026-10-26; re-check every 180 days -->

Read before drafting anything. The screen decides which regimes' sections
each draft carries. It is the first step of every pack, including a
proof-of-concept note and a single requested document.

Sources: the research notes this skill was built from, each read on 26
October 2026 (`docs/research/au-ai-privacy-law-2026-10-26.md`,
`us-ai-privacy-law-2026-10-26.md`, `eu-ai-privacy-law-2026-10-26.md`,
`uk-ai-privacy-law-2026-10-26.md`, `nz-ai-privacy-law-2026-10-26.md`,
`sg-ai-privacy-law-2026-10-26.md`, `ca-ai-privacy-law-2026-10-26.md` and
`au-government-forms-nsw-2026-10-26.md` in the skills repository), and the
regime references they produced: [Australia](australia.md),
[United States](united-states.md), [EU AI Act](eu-ai-act.md),
[privacy and records](privacy-and-records.md),
[United Kingdom](united-kingdom.md), [New Zealand](new-zealand.md),
[Singapore](singapore.md), [Canada](canada.md) and
[AU government crosswalks](au-government-crosswalks.md).

## The order never changes

Australia, United States, EU, United Kingdom, New Zealand, Singapore,
Canada. The consultancy is in Australia, so Australia is screened first even
when the client is not. Every list, table and front-matter value keeps this
order: `jurisdictions: [au, us, eu, uk, nz, sg, ca]`, with the codes that are
in scope only. Name Canada as "Canada" or "Quebec", never "CA", which US
sections use for California.

The screen covers seven regimes. A screen written before New Zealand,
Singapore and Canada were added, with four rows, fails the checker until it
gains their three rows, each with the reason it is or is not in scope: a
regime left out without a reason is the failure the screen exists to stop.

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
| Who at the consultancy can see personal data, and from where: build, test, evaluation sets, log and trace review, support, incidents | Australian staff access is a restricted transfer for EU and UK data, an s 11 agent or IPP 12 fact for New Zealand data, a Transfer Limitation Obligation transfer for Singapore data, an s 17 flow for Quebec data and an s 19(2) fact for a NSW agency's data, and brings the consultancy's own Privacy Act position into scope | Design operations and access decisions; SOW support terms |
| Client type: private company; Australian Commonwealth agency (non-corporate Commonwealth entity); NSW public sector agency (DCS-2026-02 entity types: departments, executive agencies, separate agencies, statutory bodies, state owned corporations, public financial and non-financial corporations, advisory entities); other state agency; local council; UK central government department or arm's-length body; US federal agency or contractor; New Zealand public service department, Crown entity or local authority; Singapore ministry, organ of state or statutory board; Canadian federal institution, Ontario ministry or provincial agency | Government clients carry mandatory assessments and forms (DTA, NSW AIAF, ATRS, Canada's AIA) and public-law duties | Brief stakeholders |
| Contract vehicle and value: NSW ICTA or Core&, value against $150,000 (including GST) and $1 million (excluding GST), Digital Assurance Framework above $5 million; Commonwealth contract terms | GIPA contracts register; ICTA clause 6.11 AI clauses and model-change notice; s 7B(5) State contract exemption; s 95B | SOW; brief stakeholders; `agency:` |
| Sector: finance, health, insurance, credit, employment, education, children's services, telecommunications marketing | Sector statutes and regulators | Brief context |
| Decision effects: does an output decide, or feed a decision about, a person's job, money, credit, housing, insurance, health, education, a benefit or access to a service? Is a person's review measured? Is any decision made by the system alone? | Automated-decision rules (APP 1.7, GDPR and UK GDPR, US state laws, Quebec s 12.1) and the accuracy and fairness duties of the others; counsel triggers | Design contracts (C IDs), plan M records |
| Province or state of the people: Quebec, Ontario, Alberta, BC; NSW and other Australian states | Canada chooses the privacy law flow by flow; NSW s 19(2) reaches any recipient outside NSW | Brief §4 data register; design users |
| Channel: consumer-facing chat, voice, outbound messages, public web | Chatbot disclosure, consumer law, marketing rules | Design channels |
| Children likely to use it; biometrics; health or other sensitive data in free text | Counsel triggers and stricter consent | Brief §4; design screening contracts |

## When each regime is in scope

| Regime | In scope when any of these holds | Notes |
| --- | --- | --- |
| `au` Australia | The client is established or carries on business in Australia; data subjects are in Australia; or the consultancy's staff or systems handle personal information for the project | When only the consultancy's own handling brings it in, the Australian sections cover that handling (the consultancy's APP entity status, APP 8 and 11, notifiable data breaches) and say so: the client's own APP 1.7 and sector rows are `n/a:` with the reason, the inventory describes the consultancy's handling for its own privacy policy, and the Guidance for AI Adoption mapping is skipped. Whether the Privacy Act reaches that handling is `counsel:` |
| `us` United States | The client is established or does business in the US; the data subjects include US residents (consumers, employees or applicants); the client is a US federal agency or contractor | Data merely stored or routed in the US does not bring state privacy laws in; it is a transfer question for the other regimes |
| `eu` EU | The client is established in the EU; the system offers goods or services to, or monitors, people in the EU; the system is placed on the EU market or its output is used in the EU (AI Act) | GDPR territorial scope (Article 3) and AI Act scope (Article 2) are `counsel:` conclusions; record the facts |
| `uk` United Kingdom | The client is established in the UK; the system offers goods or services to, or monitors, people in the UK; the client is a UK central government department or in-scope arm's-length body | UK GDPR territorial scope is a `counsel:` conclusion; a UK pack with EU users keeps the EU sections as well |
| `nz` New Zealand | The client is a New Zealand agency (company, public service department, Crown entity, local authority); personal information about people in New Zealand is handled; the consultancy holds or accesses New Zealand data | The Act binds agencies of any size, with no small business or employee records exemption; whether the consultancy is an overseas agency carrying on business in New Zealand is `counsel:`. Gemini processes outside New Zealand in every design today, so the transfer annex has a New Zealand row |
| `sg` Singapore | The client collects, uses or discloses personal data in Singapore; data subjects are in Singapore; the client is a Singapore public agency (outside the PDPA, but its contractors are not) | The consultancy is usually a data intermediary; every flow out of Singapore, including Sydney access, is the client's Transfer Limitation Obligation and a transfer annex row |
| `ca` Canada | The client carries on a commercial activity or an enterprise in Canada; data subjects are in Canada (record the province); the client is a federal institution or an Ontario ministry or agency | Which law governs each flow (PIPEDA, Quebec, Alberta, BC) is `counsel:`. Quebec people or a Quebec enterprise bring the s 3.3 PIA, the s 17 assessment for every flow leaving Quebec (a transfer annex row) and s 12.1 |
| `au` NSW government client | The client is a NSW public sector agency or state owned corporation, or the consultancy works under a NSW State contract | Not a separate code: the `au` sections add the NSW material from [Australia](australia.md) (AIAF registration and assessment, the PPIP and HRIP Acts with s 19(2), Part 6A, GIPA, the State Records Act 1998, the NSW Cyber Security Policy, ICTA clause 6.11), the memo's "Australia: Government client" section and government form answers from [AU government crosswalks](au-government-crosswalks.md). The consultancy's acts under the State contract fall under s 7B(5); its other acts stay under the APPs (`counsel:`). Always `counsel_required: yes` |
| `au` Commonwealth client | The client is a non-corporate Commonwealth entity (corporate entities opt in) | DTA policy v2.1 and tool v1.0; the Agencies Privacy Code PIA; s 95B contract terms; government form answers from the crosswalks. Always `counsel_required: yes` |

**Only the EU has an AI Act.** The other six regimes' sections screen which
existing laws apply and assign no risk tier: the US sections screen state AI
and automated-decision laws, sector laws and FTC claims; the Australian, UK,
New Zealand, Singapore and Canadian sections screen privacy, consumer,
employment, sector and government rules.

**A public website or chat reachable from anywhere** does not by itself put
every country in scope. Record whether the client offers its services to,
or monitors, people there (language, currency, delivery, marketing). Where
it does, or the record does not say, the regime stays in scope; where the
record shows incidental visitors only, write the row as out of scope with
`assumption:` and `counsel:` to confirm.

**A group of companies** (a parent in one country, a subsidiary in another)
may hold two controller or APP entity roles. Name each entity in Roles and
in the input pack's front matter, and write which is the exporter of each
transfer as `counsel:`.

## Record the result

- **Sections.** Write only the sections whose regime is triggered, and
  record a reason for every regime that is not. Over-including is safer:
  counsel can strike a section out, but cannot review one that was never
  written.
- **Front matter.** Every draft carries `jurisdictions: [<codes>]` in the
  order above. The checker fails a draft whose list is missing, empty,
  out of order or holds an unknown code, and fails a regime section whose
  code is not listed.
- **Screen table.** The regulatory memo (and the proof-of-concept note's
  Classification section) has one row for each of the seven regimes,
  including the ones not in scope (the example shows the first four; the
  New Zealand, Singapore and Canada rows follow in the same form):

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

| Document | `nz` | `sg` | `ca` | `au` government client |
| --- | --- | --- | --- | --- |
| Regulatory memo | New Zealand: Privacy Act and IPPs; Sector, consumer and government AI policy | Singapore: PDPA and roles; AI governance frameworks; Sector and employment | Canada: Privacy laws and roles; Automated decisions; Employment, sector and government AI policy | Australia: Government client (Commonwealth or NSW agency) |
| Privacy impact input pack | New Zealand: IPP compliance check; Collection and notice inputs | Singapore: PDPA obligations check; Notification and policy inputs | Canada: Consent and notice inputs; Quebec PIA and s 17 facts | Australia: NSW IPP and HPP check (NSW agency) |
| Records of processing | Not written: no Article 30 register | Not written | Not written | As `au` |
| Transfer assessment annex | New Zealand: s 11 agents and IPP 12 (and jurisdictional risk inputs for public sector clients) | Singapore: Transfer Limitation Obligation | Canada: Quebec s 17 and Alberta service providers | NSW s 19(2) facts stay in the input pack |
| System card | AI disclosure and alternative channel; Algorithm Charter facts for signatories | Chatbot info card inputs for external chatbots | Quebec s 12.1 block; Ontario job-posting disclosure | AIAF or DTA transparency, appeal and non-AI alternative |
| Security questionnaire | Notifiable privacy breach clock; NZISM for public service | 3-day PDPC clock; MAS 1 hour | PIPEDA clock and 24-month record; CAI notice and register; Alberta | NSW Cyber Security Policy (ML1); 24-hour reporting; Part 6A; ICTA notice |
| Impact assessment | New Zealand: Responsible AI Guidance mapping and Māori impact | Singapore: Agentic MGF mapping | Canada: AIA inputs (federal clients) | Government form answers documents |

## Documents the pack names but the client's process produces

These are named in the memo with their owner and wait; the pack supplies
inputs from its own sections and does not draft the document:

| Document | Regime and trigger | Inputs come from |
| --- | --- | --- |
| DTA AI impact assessment and the agency's AI transparency statement | Australia: a non-corporate Commonwealth entity client with an in-scope use case; the assessment is due for in-scope use cases by 15 December 2026 (checked 2026-10-26) | Impact assessment section "Australia: DTA AI impact assessment inputs"; system card |
| NSW AI Assessment Framework entry | Australia: NSW agency client; the platform has been mandatory since 30 September 2026 (checked 2026-10-26) | Impact assessment; privacy impact input pack |
| AIAF Platform registration and, where required, AIAF assessment; NSW AI Review Committee referral for high or critical | Australia: NSW agency; referral within 5 business days of completing the AIAF (checked 2026-10-26) | Government form answers (AIAF registration and assessment); impact assessment; input pack |
| Agency PIA under the IPC guides; privacy management plan update; Part 6A data breach policy and register entry; GIPA contract register entry | Australia: NSW agency | Input pack "Australia: NSW IPP and HPP check"; memo; security questionnaire |
| Digital Assurance Framework gateway review | Australia: NSW project over $5 million or funded by the Digital Restart Fund | Design, plan, evaluation reports |
| DTA transparency statement entry, use case register row, Commonwealth AI Review Committee advice | Australia: non-corporate Commonwealth entity; committee for residual high risk or highly sensitive, novel or complex use cases | Government form answers (DTA tool, transparency, register, agentic addendum) |
| Agency PIA copied to the Government Chief Privacy Officer; AI register entry and risk class; NZISM certification and accreditation; jurisdictional risk assessment; Algorithm Charter assessment | New Zealand: public service or other public sector client (Charter for signatories) | Input pack; transfer annex; impact assessment |
| Quebec EFVP (privacy impact assessment) and s 17 assessment | Canada: Quebec enterprise | Input pack "Canada: Quebec PIA and s 17 facts"; transfer annex |
| Algorithmic Impact Assessment and its publication; GC AI Register entry | Canada: federal institution, output making or informing an administrative decision | Impact assessment "Canada: AIA inputs"; system card |
| Ontario electronic monitoring policy; ministry AI use-case inventory | Canada: Ontario employer of 25 or more; Ontario ministry or provincial agency | Input pack logging flow; system card |
| Bias audit by an independent auditor | United States: NYC Local Law 144 (automated employment decision tool used on NYC candidates or employees) | Impact assessment section "Adverse impact and equality" |
| Consumer notices (pre-use ADMT notice, adverse-outcome explanation, opt-out or appeal) | United States: CPPA ADMT and Colorado SB 26-189 | System card section "Automated-decision disclosure" |
| ATRS record | United Kingdom: central government department or in-scope arm's-length body, tool in Beta, Pilot or Production with public effect or public interaction | System card, privacy impact input pack, impact assessment |
| Online Safety Act risk assessments | United Kingdom: users can share outputs, the agent searches several sites or databases, or it can generate pornography | Memo `gap:` with its owner |
| Fundamental rights impact assessment | EU: Article 27 deployer of an Annex III system | Impact assessment section "FRIA crosswalk" |
