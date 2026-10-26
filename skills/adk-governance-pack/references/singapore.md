# Singapore

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `sg` in
scope. Singapore has no AI Act. It regulates personal data through the
Personal Data Protection Act 2012 (PDPA) and governs AI through voluntary
frameworks from IMDA and the PDPC, sector regulators and a few targeted
statutes. The Singapore sections of the regulatory memo therefore assign no
risk tier: they screen which laws and frameworks apply, from facts the
design records, and leave every legal conclusion to counsel. This reference
is at screen depth: the triggers, the key duties, the pack section each
lands in and the questions for counsel.

## Sources and their status

Read at the primary source on 26 October 2026 unless a line says
"reported; not confirmed at the source on 2026-10-26". Copy `checked
2026-10-26` into a draft only while this file is the newest check.

- PDPA, Singapore Statutes Online, "Current version as at 26 Oct 2026"
  (<https://sso.agc.gov.sg/Act/PDPA2012>): the table of contents and the
  version timeline only. **The section bodies did not load**, so statutory
  wording here is as the PDPC quotes it in its guidelines; re-read the
  sections at the source before relying on their exact words.
- PDPC (<https://www.pdpc.gov.sg>): Advisory Guidelines on Key Concepts in
  the PDPA, revised 29 April 2026 (chapters 6, 7, 12 and 14 to 21); Advisory
  Guidelines on Use of Personal Data in AI Recommendation and Decision
  Systems, issued 1 March 2024, read in full; Advisory Guidelines on Use of
  Personal Data in Generative AI, issued 20 July 2026, read in full;
  Advisory Guidelines on Enforcement of the Data Protection Provisions,
  revised 1 October 2022 (para 27); Advisory Guidelines on the Do Not Call
  Provisions, revised 1 February 2021; Guide to Data Protection Impact
  Assessments, 14 September 2021; Guide to Data Protection Practices for ICT
  Systems, revised 20 July 2026; Guide to Basic Anonymisation, updated 24
  July 2024.
- IMDA and the AI Verify Foundation: Model AI Governance Framework for
  Agentic AI, Version 1.5, published 20 May 2026, updated 5 June 2026;
  Transparency Guidelines for Generative AI Chatbots, published 20 July
  2026; Starter Kit for Testing Agentic Systems, Version 1.0, October 2026;
  the Model AI Governance Framework, second edition, and the framework for
  generative AI (30 May 2024).
- MDDI written answer to a parliamentary question, 7 July 2026; MinLaw and
  MDDI release on the Online Safety Commission, 14 May 2026; CSA releases.
- MAS: Guidelines on Artificial Intelligence Risk Management, 7 October 2026
  (sections 1 to 5); Notice FSM-N05 on Technology Risk Management, read in
  full; Notice 658; FEAT Principles.
- MOH circular MOH-MHC-0024-2026 (AIHGle 2.0); HSA guidance pages; MOH
  release on the Health Information Bill, 12 January 2026; Government
  Gazette, Workplace Fairness Act 2025; MOM and TAFEP pages.

The full research note, with every secondary item marked, is
`docs/research/sg-ai-privacy-law-2026-10-26.md` in the skills repository.

## No AI Act

MDDI's written answer of 7 July 2026 says "the need for regulation depends
on how it is deployed, the nature of harm that may be caused" and that the
Government "will continue to study the appropriate regulatory stance for
AI". No AI bill was found (reported; not confirmed at the source on
2026-10-26). The memo says "No AI-specific statute applies in Singapore
(MDDI, 7 July 2026)" with `checked 2026-10-26`.

## Roles: organisation, data intermediary, public agency

Record these facts in the memo's Roles section, each conclusion as
`counsel:`. Use the PDPA's own words.

- **Organisation.** Any person or body, whether or not formed under
  Singapore law, for activities relating to the collection, use and
  disclosure of personal data in Singapore (Key Concepts).
- **Data intermediary.** An organisation that processes personal data on
  behalf of another "pursuant to a contract which is evidenced or made in
  writing" carries only the protection, retention limitation and breach
  notification to the organisation obligations (Key Concepts). The function
  decides, not the label. A use beyond the contract ends the role for that
  use: reusing client data for another client or for the consultancy's own
  evaluation sets makes the consultancy an organisation for it, with every
  obligation.
- **The client keeps the rest.** It has the same obligations for data its
  intermediary processes "as if the personal data were processed by the
  organisation itself" (s 4(3), as the PDPC quotes it).
- **The PDPC applies these roles to AI vendors.** "Third-party developers
  of bespoke AI Systems ('Service Providers') are data intermediaries" (1
  March 2024, para 1.4). The 20 July 2026 guidelines name model providers,
  system providers and system deployers: a model provider running inference
  for downstream users is a data intermediary, one that uses prompts for its
  own model development is an organisation, and the deployer bears "primary
  responsibility".
- **Public agencies** (the Government, ministries, departments, organs of
  State, tribunals and gazetted statutory bodies) are outside the data
  protection provisions. Their service providers are organisations or data
  intermediaries; a data intermediary of a public agency must notify it of a
  breach without undue delay (s 26E, as the PDPC cites it). Government ICT
  and data classification terms flow down by contract (not read; a `gap:`
  until the client supplies them). A public agency client sets
  `counsel_required: yes`.
- **Accountability (ss 11, 12).** A designated data protection officer with
  published business contact details, readily accessible from Singapore
  during Singapore business hours (Key Concepts para 21.7), written policies
  and a complaints process.

This is closer to GDPR than to Australia, where the consultancy is an APP
entity in its own right. Never write "APP entity" or "controller" in a
Singapore section.

## Consent, deemed consent and the exceptions

There is no lawful-basis menu. Each purpose needs consent, deemed consent or
an exception, with the assessments the Personal Data Protection
Regulations 2021 require kept for as long as the data is used on that basis.

- **Consent and withdrawal (ss 13 to 16).** Consent obtained through vague
  or misleading purposes is not valid.
- **Deemed consent** by conduct, by contractual necessity, or by
  notification (s 15A): an assessment that the use "is not likely to have an
  adverse effect", notice of the purpose and "a reasonable period" to opt
  out, then waiting until it lapses.
- **Legitimate interests** (First Schedule Part 3): an assessment with a
  balancing test, and public disclosure that the organisation relies on
  it. It cannot be used for direct marketing.
- **Business improvement** (use of data already collected): improving
  goods, services or operations, understanding behaviour, personalising,
  where identifiable data is needed and a reasonable person would consider
  the use appropriate. The PDPC applies it to developing, testing,
  monitoring and debiasing AI systems (1 March 2024, paras 4.2 and 5.3 to
  5.10), but not to a "significant departure" such as a company turning its
  customer data to generative AI development, where "the appropriate course
  of action is to obtain fresh consent" (20 July 2026, para 4.2).
- **AI-Specific Notification.** "General Notifications are an insufficient
  means of obtaining consent" for large-scale generative AI model training
  or fine-tuning (para 4.4); retrieval and prompting are not training (fn
  11).
- **Publicly available data behind a digital barrier** (paywall,
  registration, age gate) needs a written record or DPIA before the
  exception is relied on (paras 3.4 to 3.7).
- The 2020 amendments that brought deemed consent by notification and the
  new exceptions took effect in stages on 1 February 2021 and 1 October
  2022 (checked 2026-10-26); which provision commenced on which date is
  reported; not confirmed at the source on 2026-10-26.

Paperwork: the input pack's "Singapore: PDPA obligations check", one row
per purpose with the basis and the assessment's ID and owner, a missing
assessment as `gap:`; the notification text in "Singapore: Notification and
policy inputs".

## The obligations an agent engages

| Obligation | What it requires (PDPC guidance) | Agent facts to record |
| --- | --- | --- |
| Purpose (s 18) and notification (s 20) | Purposes a reasonable person would consider appropriate, notified on or before collection | Stated purpose; tools and stores the agent can reach |
| Access (s 21) and correction (s 22) | Respond as soon as reasonably possible; if not within 30 days, say in writing when. Accede to requests about data "stored in a Retrieval-Augmented Generation database" (20 July 2026, para 10.5) | Stores searchable by person |
| Preservation (s 22A) | Keep data subject to a rejected access request for at least 30 calendar days | Retention must not purge it early |
| Accuracy (s 23) | Reasonable effort where data is likely to be used to decide about the person | Evaluation results (M IDs) |
| Protection (s 24) | "Reasonable security arrangements", including for "end-user prompts, inputs and generated outputs, agent or tool activity data" (para 9.3) | SB and C IDs; prompt-injection controls |
| Retention (s 25) | Cease to retain or anonymise when the purpose is no longer served; no "just in case" retention | Retention per store |

For agents, the PDPC's ICT practices (revised 20 July 2026) ask for an AI
system inventory, least-privilege access limited for agentic systems to the
intended data and time window, and logging of inputs and outputs. The PDPC
recommends notifying people of the product function, the data types, how
the processing is relevant and the features most likely to influence it,
proportionate to impact and autonomy (1 March 2024, paras 9.4 and 9.5), and
written policies on fairness, safeguards and human oversight, which may
include "model cards and system cards" (para 10.5). Singapore has **no
automated-decision provision and no DPIA duty**: a DPIA is encouraged, and
failing to do one "is not itself a breach of the PDPA" (Key Concepts para
21.15). Data portability is not in force (by absence in the current SSO
contents and the guidelines, checked 2026-10-26).

## Transfer Limitation Obligation

- A transfer happens when the organisation "relinquishes possession or
  direct control" of data to a recipient outside Singapore, including its
  own data intermediary (Key Concepts para 19.1).
- **It is the client's duty**, "regardless of whether the personal data is
  transferred by the organisation to an overseas data intermediary or
  transferred overseas by the data intermediary in Singapore".
- The client ensures a "standard comparable" to the PDPA through legally
  enforceable obligations on the recipient (a law; a contract that imposes a
  comparable standard and "specifies the countries and territories to which
  the personal data may be transferred"; binding corporate rules; another
  binding instrument) or a specified certification (Global or APEC CBPR;
  for a data intermediary recipient, also Global or APEC PRP). The Personal
  Data Protection (Amendment) Regulations 2026 on certifications are
  reported; not confirmed at the source on 2026-10-26.
- Minimum clauses for a data intermediary recipient: protection, retention
  limitation and breach notice to the organisation "without undue delay"
  (para 19.9). The PDPC encourages the ASEAN Model Contract Clauses.
- **There is no adequacy list**; Australia is not whitelisted.
- Whether Gemini's machine-learning processing is listed in asia-southeast1
  for the pinned model was not read; read the model page for each project.

Consultancy staff in Sydney reading traces, logs or evaluation sets, and any
model endpoint outside Singapore, are transfers. Write a Singapore row in
the transfer assessment annex for each, not just an input-pack line as for
Australia's APP 8. Treat the contract as required until counsel says
whether the Privacy Act 1988 counts as "any law" binding the consultancy.

## Data breach notification

On credible grounds to believe a breach occurred, the client assesses
whether it is notifiable, generally within 30 calendar days. It is
notifiable if it is likely to cause "significant harm" (deemed for the
prescribed data classes, such as a full name or national identification
number with financial or health data, or account credentials) or affects
"500 or more individuals". The client notifies the PDPC "as soon as
practicable, but in any case, no later than three (3) calendar days" after
determining that, and affected individuals at the same time or after. The
data intermediary only tells the client "without undue delay" (Key Concepts
chapter 20; in force since 1 February 2021, checked 2026-10-26). Paperwork:
the questionnaire's incident row with both clocks and the consultancy's
contractual notice term.

## Penalties

Financial penalties up to S$1 million or 10% of annual turnover in
Singapore, whichever is higher, the 10% limb where that turnover exceeds
S$10 million (Enforcement guidelines para 27; the higher cap has applied
since 1 October 2022, checked 2026-10-26). A data intermediary can be
penalised for its own protection and retention failures. One memo line.

## Voluntary AI frameworks

| Framework | Status (checked 2026-10-26) | What the pack takes from it |
| --- | --- | --- |
| Model AI Governance Framework for Agentic AI | Launched 22 January 2026; Version 1.5 published 20 May 2026, updated 5 June 2026; voluntary | Impact assessment "Singapore: Agentic MGF mapping": bound risks up front (error tolerance, sensitive data and persistent memory, external systems, write actions, reversibility, autonomy); meaningful human accountability, including the "Human override rate ... A low rate may signal rubber-stamping behaviours"; technical controls and change management on model updates; end-user disclosure "at the point of interaction" |
| Transparency Guidelines for Generative AI Chatbots | Published 20 July 2026; voluntary, external chatbots only | System card chatbot info card inputs: what it can and cannot do; how reliable and safe; how user data is handled; how to report issues; a first-use statement; version and date |
| Starter Kit for Testing Agentic Systems | Version 1.0, October 2026 | Frame evaluation evidence in its steps |
| Model AI Governance Framework, second edition; framework for generative AI | 21 January 2020; 30 May 2024 | The human-involvement label; mention only |
| CSA Guidelines on Securing AI Systems; agentic addendum | October 2024; addendum still a consultation version (page dated 17 June 2026) | AI security baseline row when the CISO asks |

## Screen when the trigger fires

| Law | Trigger | What the pack records |
| --- | --- | --- |
| MAS Guidelines on AI Risk Management; FEAT; TRM Notice; Notice 658 | MAS-regulated client | The guidelines take effect on 7 October 2027, with sections 5 and 6 expected by 7 October 2028 (checked 2026-10-26); inventory attributes for agents (tools, components, guardrails); materiality; third-party AI contract terms. FSM-N05: notify MAS within 1 hour of discovering a relevant incident, root cause report within 14 days. Notice 658 outsourcing register and audit access. `counsel_required: yes` for customer decisions |
| Workplace Fairness Act 2025; Tripartite Guidelines | The agent screens CVs, invites to interviews, appraises or feeds dismissal for an employer of 25 or more | The Act passed and received assent but is not in force: expected end-2027 (MOM target, not gazetted), checked 2026-10-26. The Tripartite Guidelines apply now, with recruitment records kept at least one year. A written direction that influences an agent of the employer to decide on a protected ground is itself discrimination (s 18). `counsel_required: yes` |
| AIHGle 2.0; HSA software medical devices; Health Information Act 2026 | Clinical summarising, triage or decision support; NEHR | AIHGle 2.0 launched 10 March 2026 (checked 2026-10-26); medical device screen as `counsel:`; the Health Information Act is expected to take effect early 2027; `counsel_required: yes` |
| PDPA Do Not Call provisions | Outbound marketing by voice (synthetic voice included), SMS or messaging to Singapore numbers | Register check valid 21 days; sender identification; calling line identity |
| Cybersecurity Act 2018 as amended | The client owns critical information infrastructure the agent connects to | CII owners report within 2 hours of becoming aware, from 31 October 2025 (checked 2026-10-26); the consultancy's notice sized to it (`counsel:`) |
| Online Safety (Relief and Accountability) Act 2025 | Public agent with user-visible content about real people | Online Safety Commission operating since 29 June 2026 (checked 2026-10-26); mention only |
| NRIC Advisory Guidelines | The agent asks for or receives NRIC or other national identification numbers | Limits on collection are reported; not confirmed at the source on 2026-10-26; masking contract |

## Screening checklist

| Trigger fact (with its ID) | Law | Document and section |
| --- | --- | --- |
| Personal data of people in Singapore in prompts, tools, memory, logs or evaluation sets | PDPA Parts 3 to 6A | Memo "Singapore: PDPA and roles"; input pack "Singapore: PDPA obligations check" |
| Consultancy processes the client's data under a written contract | Data intermediary | Memo Roles; questionnaire protection, retention and breach notice |
| Consultancy reuses client data outside the contract | Loses intermediary status | Memo Roles (`counsel:`) |
| A new purpose for existing data; production data used to build, test or debias | s 15A; legitimate interests; business improvement or research | Input pack rows with assessment IDs |
| Training or fine-tuning on user data | AI-Specific Notification | Input pack notification inputs |
| Consultancy access from Australia; processing outside Singapore | Transfer Limitation Obligation | Transfer annex Singapore rows |
| Any personal data held | Part 6A, 3 calendar days | Questionnaire incident row |
| RAG store, memory or history with personal data | ss 21, 22 | Input pack data flows |
| Output feeds a decision about a person | s 23; PDPC recommended disclosures; sector rules | System card; impact assessment; `counsel_required: yes` |
| Agent with write tools, payments, outbound messages or persistent memory | Agentic MGF dimensions 1 and 2 | Impact assessment mapping |
| External customer chat agent | Chatbot transparency guidelines | System card chatbot info card inputs |
| Ministry, organ of state or statutory board client | Public agency exclusion; s 26E | Memo Roles; questionnaire; `counsel_required: yes` |

## Questions counsel usually gets

- Is the consultancy a data intermediary for every step, and does the
  written contract record the scope? Does any reuse make it an organisation?
- Is each purpose within consent, deemed consent or an exception, and are
  the required assessments adequate?
- Is consultancy access from Australia a transfer the client must cover, and
  does the contract impose a comparable standard and name Australia?
- Does evaluation or fine-tuning on production data fall within business
  improvement, or is it a significant departure needing fresh consent?
- Who leads the breach assessment where the client, the consultancy and
  Google all hold the data?
- For a public agency client: is the client gazetted, and which government
  data security terms apply to the consultancy?

## Words to use

Personal data, organisation, data intermediary, notifiable data breach,
DPIA, transfer, deemed consent, business improvement exception, data
protection officer. Singapore has no statutory "sensitive information"
category: write "data classes deemed significant harm". Never use APP or
GDPR terms in a Singapore section.
