# New Zealand

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `nz` in
scope. New Zealand has no AI Act and no AI bill, so the New Zealand sections
of the regulatory memo assign no risk tier. They screen which existing laws
and government policies the agent falls under, from facts the design
records, and leave every legal conclusion to counsel. This reference is at
screen depth: the triggers, the key duties, the pack section each lands in
and the questions for counsel. It is not a full statement of New Zealand
law.

## Sources and their status

Read at the primary source on 26 October 2026 unless a line says
"reported; not confirmed at the source on 2026-10-26". Copy `checked
2026-10-26` into a draft only while this file is the newest check.

- Privacy Act 2020, 2020 No 31, latest version as at 8 October 2026
  (<https://www.legislation.govt.nz/act/public/2020/31/en/latest/>): ss 4,
  7 to 12, 22 (the IPPs), 23 to 28, 44, 63, 69, 112 to 128, 193, 201 and 212
  to 214. Privacy Amendment Act 2025, 2025 No 53, read in full. Privacy
  Regulations 2020, SL 2020/194.
- Office of the Privacy Commissioner (OPC,
  <https://www.privacy.org.nz>): "Artificial intelligence and the
  Information Privacy Principles", September 2023, pages 1 to 11; the AI
  topic page; the IPP 3A pages; "Working with third-party providers", 26
  November 2024; the NotifyUs page; the privacy impact assessment page; the
  Biometric Processing Privacy Code pages and the August 2025 summary (the
  code's own text was not read); the Commissioner's submission to the
  Petitions Committee, signed 28 April 2026.
- Google Cloud, Vertex AI generative AI data residency, last updated 22
  October 2026
  (<https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency>).
- MBIE: New Zealand's Strategy for Artificial Intelligence, July 2025, and
  Responsible AI Guidance for Businesses, July 2025.
- Public sector guidance, read on standards.digital.govt.nz, the
  Government Chief Digital Officer's operational copy (its disclaimer says
  digital.govt.nz is authoritative, and that site refused automated reads):
  the Public Service AI Framework (last updated 29 January 2025), the
  Responsible AI Guidance for the Public Service: GenAI (sub-pages last
  updated 3 February 2025) and the Cloud Jurisdictional Risk Guidance (last
  updated 14 August 2024). The July 2023 interim GenAI advice and the
  Algorithm Charter (July 2020) were read as PDFs. Ministry for Regulation,
  "Responsible AI in action", v1.1 updated 25 August 2026. NCSC-NZ pages.
- Fair Trading Act 1986 (as at 1 July 2026); Fair Trading Amendment Bill
  299-1; Human Rights Act 1993; New Zealand Bill of Rights Act 1990;
  Unsolicited Electronic Messages Act 2007; Harmful Digital Communications
  Act 2015; the Health Information, Credit Reporting and Telecommunications
  Information Privacy Codes (consolidated 1 May 2026); Customer and Product
  Data Act 2025; Employment Relations Act 2000; Health and Safety at Work Act
  2015; Financial Markets Conduct Act 2013 (all at legislation.govt.nz or
  privacy.org.nz).

The full research note, with every secondary item marked, is
`docs/research/nz-ai-privacy-law-2026-10-26.md` in the skills repository.

## No AI Act

MBIE's AI Strategy of July 2025 says "New Zealand is taking a light-touch
and principles-based approach to AI policy" and "The adoption of these
principles does not require additional regulatory overlay beyond existing
law". No AI bill was found (search, 26 October 2026; reported; not
confirmed at the source on 2026-10-26). The memo says "No AI-specific
statute applies in New Zealand; the July 2025 AI Strategy relies on
existing law" with `checked 2026-10-26`, and the rest of the New Zealand
sections screen the laws below.

## Roles under the Privacy Act 2020

Record these facts in the memo's Roles section, each conclusion as
`counsel:`. Use the Act's own words: agency, agent, personal information.

- **Agency.** The Act binds every agency, public or private, of any size,
  and the Crown (s 6). There is **no small business exemption and no
  employee records exemption**: employees and job applicants have full IPP
  rights, including access to what the agent holds about them.
- **Overseas agency (s 4(1)(b), (3)).** The Act reaches an overseas agency
  "in the course of carrying on business in New Zealand", without a place of
  business, payment or profit motive. Whether the Sydney consultancy is
  caught in its own right is `counsel:`.
- **Agents (s 11).** Information an agent holds "for or on behalf of" the
  client is treated as held by the client, wherever the agent is (s 11(4)),
  and passing it to the agent and back "is not a use or disclosure"
  (s 11(5)). The agent holds it in its own right as well "if A uses or
  discloses the information for its own purposes" (s 11(3)). The OPC says a
  provider that uses information for AI training is using it for its own
  purposes (third-party providers guidance, 26 November 2024).
- **The client stays responsible.** The OPC's recommended contract terms:
  security proportionate to sensitivity; quick retrieval for access and
  correction; "the contract requires the third-party provider to notify
  you of all breaches"; retention limits and deletion including backups;
  use only to deliver the services; subcontractors held to the same
  standard.
- **Privacy officer (s 201).** Every agency appoints at least one.

This is New Zealand's version of Australia's "use, not disclosure" test,
but it is in the statute: write the s 11 facts, not "effective control".

## The IPPs an agent engages

| IPP | What it requires (text as at 8 October 2026) | Agent facts to record |
| --- | --- | --- |
| IPP 1 | Collect only for a lawful purpose connected with the agency's functions, where "necessary for that purpose"; do not require identity the purpose does not need (1(2)) | One purpose per data item; whether identity is needed |
| IPP 2, 3 | Collect from the person unless an exception applies; tell them the matters in 3(1) before or as soon as practicable after collection | Chat and voice collection notices |
| IPP 3A | Indirect collection notice; see below | One row per indirect source |
| IPP 4 | Lawful, fair means that do not intrude unreasonably, "particularly" for children and young persons | Children likely to use it; covert capture |
| IPP 5 | "Reasonable" safeguards against loss, unauthorised access, use, disclosure and misuse; for service providers, everything reasonably within the agency's power (5(b)). The OPC: keep "prompts and training data" secure | SB and C IDs; provider contract |
| IPP 6, 7 | Access and correction, within 20 working days (s 44(1) and s 63(1), as amended from 24 September 2025, checked 2026-10-26) | Memory, session, vector and trace stores searchable by person; statement of correction |
| IPP 8 | No use or disclosure "without taking any steps that are, in the circumstances, reasonable to ensure that the information is accurate, up to date, complete, relevant, and not misleading" | Evaluation on New Zealand data (M IDs); the review step |
| IPP 9 | Keep no longer than required for a lawful purpose | Retention per store |
| IPP 10, 11 | Use for another purpose, or disclose, only on a listed ground (directly related purpose, authorisation and the rest); IPP 11 is subject to IPP 12 | Re-used datasets; outbound messages and tool calls |
| IPP 12 | Cross-border disclosure; see below | Offshore parties |
| IPP 13 | Assign a unique identifier only if necessary; do not reuse another agency's | National, tax or customer numbers echoed in outputs |

**What the OPC says about AI (September 2023).** Its expectations: senior
leadership approval "based on full consideration of risks and
mitigations"; a necessity and proportionality review; "Conduct a privacy
impact assessment before using these tools"; transparency about "how, when,
and why the tool is being used"; engagement with Māori "about potential
risks and impacts to the taonga of their information"; procedures for
accuracy and access; human review before acting on outputs; and "Ensure
that personal information is not retained or disclosed by the AI tool".
Asking an AI system a question that generates information about a person,
even false information, is collection. Write each expectation as a row of
the input pack's IPP check with its evidence or `gap:`.

**No automated-decision rule.** New Zealand has no counterpart to APP 1.7,
GDPR Article 22 or UK Articles 22A to 22D. IPP 8 is the hook: the OPC says
"Simply having a 'human in the loop' may not be enough to uphold the
accuracy principle, given the well-known problem of automation blindness",
and higher-risk uses "may require independent testing and auditing". Write
the review facts (contract ID, reviewer's authority and training, share
reviewed) and never write that a reviewer satisfies IPP 8.

## Indirect collection (IPP 3A)

IPP 3A applies from 1 May 2026, checked 2026-10-26 (Privacy Amendment Act
2025, Part 1), and not to information collected before that day (s 25A).
When an agency collects personal information "other than from the
individual concerned", it takes reasonable steps so the person is aware of
the fact of collection, the purpose, the intended recipients, the
collecting and holding agencies' names and addresses, any law authorising
it, and the access and correction rights, "as soon as is reasonably
practicable after the information has been collected". Exceptions include
no prejudice, publicly available information, prejudice to the purpose and
"not reasonably practicable". The OPC: "Having incompatible systems or
processes is not a valid reason" to rely on that last one; "Documenting
your rationale and decision-making will be important"; and where a hosting
provider does not use data for its own purposes, the client, not the
provider, is "responsible for meeting any IPP3A requirements".

Triggers: the agent pulls information about people from a CRM, partner API,
web search or grounding service; reads uploads, emails or tickets that name
other people; enriches a record from another source. Whether generated or
inferred statements about a person are an indirect collection is
`counsel:`. Paperwork: the input pack's "New Zealand: Collection and notice
inputs" table, one row per source, with who notifies and any exception's
documented rationale.

## Cross-border: s 11 and IPP 12

- An agency may disclose personal information to a "foreign person or
  entity" (an Australian company is one) only on one of six grounds (IPP
  12(1)): the person's authorisation after being told the recipient may not
  give comparable safeguards; the recipient is carrying on business in New
  Zealand and subject to the Act; comparable laws; a prescribed binding
  scheme; a prescribed country; or reasonable grounds to believe the
  recipient must protect it comparably, "for example, pursuant to an
  agreement". IPP 12(1)(e) was replaced from 27 November 2025, checked
  2026-10-26.
- **No country or binding scheme is prescribed** (Privacy Regulations 2020,
  checked 2026-10-26).
- **Agents are outside IPP 12.** The OPC: "Using offshore technology
  providers to store or process your data is not treated as a disclosure
  under IPP12, so long as they are not using that information for their own
  purposes". IPP 12 bites when a party uses information for its own
  purposes (s 11(3)); IPP 5(b) applies either way.
- **Gemini processes offshore.** The Vertex AI data residency page (updated
  22 October 2026) lists no New Zealand region for machine-learning
  processing; the nearest listed is australia-southeast1. Whether an
  Auckland Google Cloud region is open is reported; not confirmed at the
  source on 2026-10-26. Read the model page for each project.
- The OPC's model contract clauses for IPP 12(1)(f) are reported; not
  confirmed at the source on 2026-10-26.

Paperwork: a New Zealand row in the transfer assessment annex for each
offshore party (consultancy, model endpoint, log sink), with the s 11 facts,
any own-purpose use in the provider's terms (abuse monitoring, service
improvement, training), and the IPP 12 ground only where a party uses
information for its own purposes.

## Notifiable privacy breaches

A privacy breach includes loss of access, such as ransomware (s 112). A
notifiable breach is one "it is reasonable to believe has caused serious
harm ... or is likely to do so". The agency notifies the Commissioner "as
soon as practicable after becoming aware" (s 114), and the OPC says
"Ideally you'll do that within 72 hours", expecting the same of service
providers. Affected people are notified as soon as practicable, or the
public where that is not practicable (s 115). Failing to notify the
Commissioner without reasonable excuse is an offence with a fine not
exceeding $10,000 (s 118). An agent's acts count as the principal's
(s 120). **There is no civil penalty regime**: the Commissioner told
Parliament so on 28 April 2026 and asked for penalties, audit powers and a
right to erasure; no bill was found (reported; not confirmed at the source
on 2026-10-26). Do not import Australian penalty language.

Paperwork: the questionnaire's incident row with the New Zealand clock, who
notifies (the client as agency) and the consultancy's contract duty to tell
the client of all breaches.

## Privacy impact assessment

The Act does not require a PIA; the OPC "expect[s] organisations to do a
privacy impact assessment (PIA) before using AI tools". Its toolkit has a
threshold template, a PIA report template and a risk and mitigation table.
Public service agencies are asked for a PIA "for any testing or use of
GenAI", with senior approval, and the July 2023 advice says to "copy your
PIA to the GCPO". Whether a full PIA is warranted is the privacy officer's
decision (`counsel:`). New Zealand has no Article 30 register; the input
pack's New Zealand sections replace it.

## Biometric Processing Privacy Code 2025

In force for new biometric processing from 3 November 2025, and for
processing that began earlier from 3 August 2026, both checked 2026-10-26
(OPC pages; the code's own text was not read). Its 13 rules replace the IPPs
for biometric information collected "in an automated process to verify,
identify or categorise" people, including voices. Rule 1 requires a
proportionality judgement that weighs "cultural impacts on Māori"; rule 3
requires clear notice and whether a non-biometric option exists; rule 10
bars inferring health, "emotion, mood, personality, mental state, or
intention", "attention, state of fatigue, or alertness", or categorising
by a Human Rights Act ground, with narrow exceptions. Triggers: voiceprint
verification, face or liveness checks, sentiment or emotion detection from
voice or video, staff alertness monitoring. Any of these sets
`counsel_required: yes`. Counsel: is the function "biometric processing";
does a rule 10 exception apply; is speech-to-text alone outside the code?

## Government clients

Government clients bring policy, not statute. There is no counterpart to
the DTA's mandatory AI impact assessment or transparency statement.

- **Public Service AI Framework** (29 January 2025): "Agencies are
  encouraged to align ... however it's not binding."
- **Responsible AI Guidance for the Public Service: GenAI** (3 February
  2025): keep "a register of AI use"; classify uses as low or high risk;
  PIAs "for any testing or use of GenAI"; tell the public when and how AI is
  used and how to challenge outcomes; systems "certified and accredited
  before they're made available to users" (NZISM); vendor advance notice of
  material changes; an exit strategy.
- **Cloud Jurisdictional Risk Guidance** (14 August 2024): "Agencies must
  carry out jurisdictional risk assessments" for cloud services and "only
  store data classified as RESTRICTED or below in a public cloud service".
  Data above RESTRICTED blocks a public cloud design.
- **Algorithm Charter** (July 2020): binds signatory agencies by
  commitment; its risk matrix says the Charter "must be applied" for high
  risk, and its commitments include a public point of contact, "a channel
  for challenging or appealing of decisions informed by algorithms" and
  explaining the role of humans. The signatory list (29 as of 31 July 2023)
  is reported; not confirmed at the source on 2026-10-26: check it per
  client.
- **Te Tiriti and Māori data** appear in guidance, not statute: the Charter
  commits signatories to "Embedding a Te Ao Māori perspective"; the GenAI
  guidance recommends the Māori Data Governance Model; MBIE's guidance says
  New Zealand storage "may better support data sovereignty than offshore
  storage". Record Māori impact and engagement in the impact assessment,
  always for a public sector client.
- NZISM's mandatory incident reporting for agencies is reported; not
  confirmed at the source on 2026-10-26.

For a public sector client, set `counsel_required: yes`. The pack names,
without drafting, the agency's PIA (copied to the GCPO), its AI register
entry and risk class, NZISM certification and accreditation, the
jurisdictional risk assessment and, for signatories, the Charter
assessment.

## Screen when the trigger fires

| Law | Trigger | What the pack records |
| --- | --- | --- |
| Fair Trading Act 1986 ss 9, 12A, 13 | Consumer-facing agent; answers on price, refunds or Consumer Guarantees Act rights; claims about the agent | s 12A forbids an "unsubstantiated representation" made without reasonable grounds: capability claims cite M records; AI disclosure. The Commerce Commission assesses AI harms "through the lens of the Fair Trading Act" and cites *Moffatt v Air Canada*. Bill 299 (reported back 25 September 2026) would add civil pecuniary penalties; not law (checked 2026-10-26) |
| Human Rights Act 1993 ss 21, 22, 44, 65; NZBORA | The agent screens, ranks or decides about candidates, staff, customers, credit or services; a public body exercising statutory functions | s 65 indirect discrimination unless "good reason"; Part 1A and NZBORA s 5 justification and s 27 natural justice for public bodies; impact assessment adverse-impact section; `counsel_required: yes` |
| Health Information Privacy Code 2020 | Health or disability client, or occupational health unit | Rules replace the IPPs; rule 3A from 1 May 2026 (checked 2026-10-26); counsel: is the client a health agency |
| Credit Reporting and Telecommunications codes | Credit reporter or subscriber; telco, ISP or contracted contact centre | Code applicability as `counsel:` |
| Employment Relations Act s 4; Health and Safety at Work Act s 58 | Agent monitors staff, processes HR files or supports restructuring | Good-faith consultation as a calendar wait; no statutory workplace surveillance notice period like NSW |
| Unsolicited Electronic Messages Act 2007 | Outbound commercial email, SMS or instant messages | Consent, sender identification, unsubscribe effective within 5 working days; voice calls, including synthetic voice, are outside it; no statutory Do Not Call register |
| RBNZ and FMA 72-hour incident clocks; CoFI | Bank, insurer, deposit taker or FMA licensee | The 72-hour clocks are reported; not confirmed at the source on 2026-10-26. CoFI's duty to "treat consumers fairly" (in force since 31 March 2025, checked 2026-10-26) |
| Harmful Digital Communications Act 2015 | Public agent generating text or images about real people | Content safety mapped to the s 6 principles |
| Customer and Product Data Act 2025 | The agent requests data through the consumer data right | Role and s 47 records |

## Mention only

One line each in the memo, with `checked 2026-10-26`: no AI Act; no civil
penalty regime and the Commissioner's call for one; Fair Trading Amendment
Bill 299, not law; the Online Safety (Minimum Age and Child Safety Risk
Assessment) Bill (reported; not confirmed at the source on 2026-10-26); the
NCSC-NZ joint guidance "Careful Adoption of Agentic AI Services" (1 May
2026) as a security baseline, not law; Copyright Act s 5(2)(a) on
computer-generated works.

## Screening checklist

| Trigger fact (with its ID) | Law | Document and section |
| --- | --- | --- |
| Personal information about anyone in New Zealand in prompts, tools, memory, logs or evaluation sets | Privacy Act 2020, IPPs | Memo "New Zealand: Privacy Act and IPPs"; input pack flows and "New Zealand: IPP compliance check" |
| Client established or carrying on business in New Zealand | ss 4, 8 | Memo screen and Roles |
| Consultancy staff in Australia hold or access New Zealand data | s 11; s 4(1)(b); IPP 5(b) | Memo Roles (`counsel:`); transfer annex New Zealand row |
| Model, logs, grounding or abuse review outside New Zealand (always true for Gemini today) | s 11; IPP 12 if any party uses information for its own purposes | Input pack recipients; transfer annex |
| The agent pulls information about people from other sources, from 1 May 2026 | IPP 3A | Input pack "New Zealand: Collection and notice inputs" |
| Output about a person is used, sent or acted on | IPP 8 | Impact assessment evaluation; system card limits and oversight |
| Sessions, memory or traces hold information about people | IPPs 6, 7, 9; 20 working days | Input pack data flows and retention |
| Any personal information held | Part 6 notifiable privacy breaches | Questionnaire incident row |
| Voice or face verification; emotion, mood or attention inference | Biometric Processing Privacy Code | Input pack proportionality; `counsel_required: yes` |
| Consumer-facing agent or capability claims | Fair Trading Act | System card claims with M records |
| Decisions about people | Human Rights Act; IPP 8 | Impact assessment adverse impact; `counsel_required: yes` |
| Public Service department, Crown entity or other public body | GenAI guidance; Cloud First jurisdictional risk; Algorithm Charter for signatories; HRA Part 1A | Input pack PIA; transfer annex jurisdictional risk inputs; impact assessment Charter and Māori rows; `counsel_required: yes` |
| Data about Māori, services to Māori, te reo Māori | OPC expectations; Charter; GenAI guidance | Impact assessment Māori impact and engagement |

## Questions counsel usually gets

- Is the consultancy an agent under s 11 only, or an agency in its own right
  (s 4(1)(b), s 11(3))?
- Does Google's abuse monitoring or any retention of flagged prompts count
  as use "for its own purposes"?
- Is AI-generated or inferred information about a person an indirect
  collection under IPP 3A?
- Are the steps taken before using an output "reasonable in the
  circumstances" under IPP 8, given automation blindness?
- If any offshore party is a recipient, which IPP 12(1) ground applies?
- Is a given incident likely to cause "serious harm"?
- For a public body: what Te Tiriti obligations pass to the supplier by
  contract, and is Gemini processing in Australia "offshore" for the
  jurisdictional risk assessment?

## Words to use

Agency (not APP entity or controller), agent (s 11), personal information,
IPP, notifiable privacy breach, serious harm, Privacy Commissioner or OPC,
foreign person or entity, privacy officer. New Zealand has no statutory
"sensitive information" category; write information "sensitive in nature".
Writing "APP", "DTA" or "lawful basis" in a New Zealand section is wrong.
