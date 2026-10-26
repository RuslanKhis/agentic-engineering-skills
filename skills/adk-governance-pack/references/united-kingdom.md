# United Kingdom

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `uk` in
scope. The UK has no AI Act, so the UK sections of the regulatory memo assign
no risk tier. They screen UK GDPR as amended by the Data (Use and Access) Act
2025 and the other laws and regulator expectations the agent falls under. If
the system also has EU users or its output is used in the EU, the EU sections
apply as well; the UK sections do not replace them.

## Sources and their status

Read at the primary source on 26 October 2026 unless a line says
"reported; not confirmed at the source on 2026-10-26". Copy `checked
2026-10-26` into a draft only while this file is the newest check.

- legislation.gov.uk: the Data (Use and Access) Act 2025 (DUAA) ss 70, 71,
  76, 78, 80, 81, 103 and Schedules 4, 7, 12 and 13; the commencement
  regulations SI 2026/82 (main commencement 5 February 2026; s 103 on 19
  June 2026) and SI 2026/1015 (the Information Commission from 30 September
  2026); SI 2026/386; SI 2026/425; UK GDPR Articles 30, 35 and 37; DPA 2018
  s 157; PECR Schedule 1; Equality Act 2010 ss 19 and 149.
- ico.org.uk: "DUAA: what does it mean for organisations?" (updated 19 June
  2026); the draft automated decision-making guidance (31 March 2026) and its
  consultation page; the AI and data protection guidance (updated 15 March
  2023, "under review"); the DPIA list; the monitoring workers guidance;
  the generative AI consultation response; the agentic AI Tech Futures
  report and the agentic AI call for evidence; the complaints guidance; the
  adequacy page; the plans for new guidance.
- gov.uk: the King's Speech 2026; the DUAA commencement plan (updated 12
  October 2026); the Code of Practice for the Cyber Security of AI (31
  January 2025); the ATRS mandatory scope and exemptions policy (17 December
  2024); the CMA's guidance on complying with consumer law when using AI
  agents (9 March 2026); the AI Management Essentials government response;
  the Employment Rights Act timeline.
- fca.org.uk: the FCA's AI approach blog (8 June 2026).

The full research note, with every secondary item marked, is
`docs/research/uk-ai-privacy-law-2026-10-26.md` in the skills repository.

## No AI statute; the regulator's new name

The King's Speech of 13 May 2026 announced no AI bill (checked 2026-10-26).
The memo says "No AI-specific statute applies in the UK" with that date. The
office of Information Commissioner was abolished on 30 September 2026
(checked 2026-10-26, SI 2026/1015); drafts name the Information Commission,
adding "(formerly the ICO)", and cite "UK GDPR", never the EU text. The ICO
says all data protection provisions of the DUAA are in force (page updated
19 June 2026).

## Automated decisions: Articles 22A to 22D

In force since 5 February 2026 (checked 2026-10-26, DUAA s 80).

- **Article 22A.** A decision is based solely on automated processing if
  there is "no meaningful human involvement in the taking of the decision",
  considering how far it is reached by profiling. It is significant if it
  produces a legal or similarly significant effect.
- **Article 22B.** A significant decision based wholly or partly on special
  category data may not be solely automated unless the person gave explicit
  consent, or it is necessary for a contract or required or authorised by
  law and Article 9(2)(g) applies. No solely automated significant decision
  may rest on the recognised legitimate interest basis, Article 6(1)(ea).
- **Article 22C.** Every solely automated significant decision needs
  safeguards: information about such decisions, the chance to make
  representations, human intervention by the controller, and the right to
  contest.
- **Article 22D.** Regulations may define meaningful involvement or add
  safeguards; none were found on 2026-10-26.

The ICO's draft guidance (31 March 2026; consultation closed 29 May 2026,
final due "Winter 2026"): the reviewer acts where they can change the
outcome, with authority and discretion, "suitably trained and qualified to
understand the system's logic, outputs, limitations, and risks"; "Using ad
hoc spot-checking isn't sufficient"; building the system does not count as
involvement. You "should do a DPIA for any ADM". Keep the existing rule that
"a human is in the loop" without a measured review share is not a fact; the
ICO's draft makes it sharper.

**Paperwork.** Input pack "United Kingdom: Lawful basis and ADM safeguards":
where a person decides (contract ID), who they are, their training and
authority, the share they review (M record), special category data used or
inferable with the masking contract and its coverage, and how each Article
22C safeguard is delivered. System card: the automated-decision disclosure
and the review route. Records: a "solely automated significant decision"
column.

## Lawful bases and re-use

In force since 5 February 2026 (checked 2026-10-26):

- **Article 6(1)(ea), recognised legitimate interest**: processing necessary
  for a purpose in Annex 1 (disclosure for a requester's public task,
  national and public security, emergencies, crime, safeguarding a
  vulnerable individual), with no balancing test.
- **Article 6(11)** gives examples that may be legitimate interests under
  6(1)(f): direct marketing, intra-group transmission for internal
  administration, and "ensuring the security of network and information
  systems". The balancing test still applies.
- **Article 8A** sets the compatibility test for further processing; data
  collected on consent can be re-used only within the consent or narrow
  limbs. Write one line per re-used dataset (HR, CRM, tickets, production
  traffic for evaluation sets) with its original purpose and basis.
- For employees, consent is rarely appropriate; the ICO says the same.

## DPIAs, records and the ICO list

Articles 30, 35 and 37 carry no substantive DUAA amendment; only
"Commissioner" became "Commission" on 30 September 2026. The EU-shaped DPIA
and Article 30 templates still fit; name the Information Commission and use
the ICO's list. The ICO's AI guidance says "In the vast majority of cases,
the use of AI will involve a type of processing likely to result in a high
risk", and an AI DPIA records variation and margins of error, the degree of
human involvement and the trade-offs.

The ICO list (pages "under review"), screened beside the WP248 criteria:
innovative technology including AI (with another criterion); denial of
service by ADM, profiling or special category data; large-scale profiling,
including applying AI to an existing process; biometric data (with another
criterion); genetic data (with another); data matching; invisible
processing (with another); tracking, including workplace monitoring;
targeting children or other vulnerable people; risk of physical harm. A
generative agent meets "innovative technology", so one more criterion
(employees, evaluation, data matching across tools) makes a DPIA required.
The DPO decides.

## Subject access, complaints and children

- **Access.** A person is entitled only to what a "reasonable and
  proportionate search" finds (Article 15(1A)); time limits run under
  Article 12A from 5 February 2026, with a pause while clarification is
  awaited (checked 2026-10-26). The input pack records per store whether
  it is searchable by person and how.
- **Complaints.** Since 19 June 2026 (checked 2026-10-26), controllers
  facilitate complaints, acknowledge within 30 days and report the outcome
  without undue delay (DPA 2018 s 164A). The system card names the route;
  an agent that receives complaints routes data protection complaints to
  it.
- **Children.** Services likely to be accessed by children take into account
  the "children's higher protection matters" in data protection by design
  (Article 25(1A), from 5 February 2026, checked 2026-10-26).

## International transfers: the data protection test

In force since 5 February 2026 (checked 2026-10-26, DUAA Schedule 7). A
transfer needs adequacy regulations, appropriate safeguards or a derogation
(Article 44A). Relying on safeguards, the controller must consider, "acting
reasonably and proportionately", that the protection is "not materially
lower" than under UK law. The ICO says a TRA completed under its earlier
guidance that found protection sufficient meets the test, and plans to
update the IDTA and Addendum during 2026; keep using the current versions.

**There are no UK adequacy regulations for Australia** (ICO adequacy page).
The UK list covers the EEA and a short list of countries, with partial
adequacy for the US through the UK Extension to the Data Privacy Framework.
So whenever the consultancy's staff or systems access UK personal data from
Australia, that is a restricted transfer needing the IDTA or the Addendum
and a documented data protection test: write a
[transfer assessment annex](../assets/transfer-assessment-annex-template.md)
row for it, `n/a:` only when the design shows no access. The Commission
renewed the UK's EU adequacy on 19 December 2025 (read via a search extract
of the Commission page), so EU clients can keep sending data to UK-hosted
systems.

## PECR

Since 5 February 2026 (checked 2026-10-26), analytics and appearance or
functionality cookies may be set without consent if users get clear
information and a simple, free way to object; advertising still needs
consent. The input pack records each front-end storage item and the
exception or consent; the questionnaire keeps the cookie inventory. PECR
breaches of regulations 5 to 8, 14 and 19 to 24 now sit under DPA 2018 s
157(2)(a) as modified, which reads as the higher maximum of £17.5 million
or 4% of turnover; the ICO's own summary says only "aligned ... in most
cases", so write the amount as `counsel:`.

## ICO positions on AI and agents

- The 2023 AI and data protection guidance is "under review" but remains the
  ICO's published view. Roles follow function: in the cloud ML example,
  "The clients will be controllers, and the provider is likely to be a
  processor". The December 2024 generative AI response says "A contract
  does not necessarily determine" roles: whether Google is a controller for
  any part (for example abuse monitoring) is `counsel:`.
- A statutory code of practice on AI and automated decision-making is
  required by SI 2026/425 (in force 12 May 2026); no draft is published.
- The agentic AI call for evidence runs from 8 October to 20 November 2026;
  agentic guidance is planned for Spring 2027. The ICO's Tech Futures
  report names ten agentic risks, which the input pack uses as UK risk rows:
  controllership across the supply chain; ADM; purpose creep; data
  minimisation; special category inference; accuracy and cascading
  hallucinations; transparency, including "invisible processing";
  individual rights; security (goal manipulation, poisoned memory); memory.
- Cite drafts as drafts with their status and date.

## Employment

The monitoring workers guidance ("under review"; update planned Winter
2026/2027) says a DPIA is required before processing likely to cause high
risk, workers must be told except in very exceptional circumstances,
"Consent is not usually appropriate in the employment context", and
employers should seek and document workers' views. The ICO's 31 March 2026
report on automated hiring asks employers to monitor for bias, tell
candidates, and explain how to challenge and get human review. Record
employees as vulnerable data subjects, monitoring as tracking, and worker
consultation (Article 35(9)) as a calendar wait.

## Equality Act 2010

- **Indirect discrimination (s 19):** a provision, criterion or practice
  that puts people sharing a protected characteristic at a particular
  disadvantage is unlawful unless it is "a proportionate means of achieving
  a legitimate aim". Postcode, names, age signals and language are
  proxies to record.
- **Public sector equality duty (s 149):** public authorities and anyone
  exercising public functions have due regard to eliminating prohibited
  conduct and advancing equality. The EHRC's guidance (1 September 2022)
  says it applies "from the very start" and covers AI others develop for
  them. A PSED trigger sets `counsel_required: yes`; the impact assessment's
  adverse impact and equality section is the due-regard record input.

## Consumer law, online safety, finance and government

| Regime | Trigger | What the pack records |
| --- | --- | --- |
| CMA, Complying with consumer law when using AI agents (9 March 2026) | The agent deals with UK consumers: prices, offers, reviews, purchases | The business is accountable "even if a third party designed or supplies it"; tell people they are dealing with AI where it could change their decision; "Do not overstate the role or AI involved"; test before deployment; a human actively checking decisions. System card disclosure and claims; questionnaire confirmation before high-risk actions and audit logs |
| Online Safety Act 2023 | Users can share outputs with each other, the agent searches several sites or databases, or it can generate pornography | Ofcom's November 2024 position on chatbots is reported; not confirmed at the source on 2026-10-26 (the page refused reads). A power to extend the Act to AI services was inserted by the Crime and Policing Act 2026 s 248 (Royal Assent 29 April 2026); no regulations found. Memo line and, if in scope, the Ofcom-format risk assessments named as `gap:` with an owner |
| FCA | FCA-authorised client; retail customers | "We are not going to introduce new regulations for AI" (8 June 2026); the Consumer Duty and SM&CR apply. Impact assessment Consumer Duty rows; memo names the accountable senior manager |
| ATRS | Central government department or in-scope arm's-length body; tool in Beta, Pilot or Production that significantly influences decisions with public effect or interacts with the public | An ATRS record is mandatory; suppliers are not bound directly but buyers should require it. The pack names the record and supplies inputs from the system card |
| DSIT Code of Practice for the Cyber Security of AI (31 January 2025, voluntary) | The CISO asks for a baseline, or procurement cites it | Questionnaire mapping of its 13 principles to SB and C IDs; the agency is usually "Developer" and the client "System Operator" and "Data Custodian". Its publication as ETSI EN 304 223 is from ETSI search extracts; cite it as such |

**Mention only**, with `checked 2026-10-26`: the AI Management Essentials
tool was not published and is not a procurement requirement (government
response updated 6 February 2026); the copyright report of 18 March 2026
says a broad text and data mining exception with opt-out is no longer the
preferred way forward and no reform is pending; the Employment Rights Act
2025 bans blacklists drafted using AI from April 2027; the Cyber Security
and Resilience Bill is not law.

## Screening checklist

| Trigger fact (with its ID) | Law or guidance | Document and section |
| --- | --- | --- |
| UK users', employees' or candidates' personal data | UK GDPR, DPA 2018 | Input pack UK section; records rows |
| Employees, workers or candidates | ICO monitoring workers; WP248 criterion 7; Article 35(9) | Input pack screening; worker consultation wait |
| Output decides, or a person only spot-checks, with effect on job, money, service, housing, health, education or reputation | Articles 22A and 22C; ICO draft ADM guidance | Input pack ADM safeguards; system card disclosure; `counsel_required: yes` |
| Special category data used or inferable in such a decision | Article 22B; Article 9 | Input pack; masking contract and coverage |
| Consultancy staff or systems in Australia access UK data, logs or evaluation sets | Articles 44A and 46(1A); no Australia adequacy | Transfer assessment annex; records transfers column |
| Endpoint, cache, grounding or abuse logs outside the UK or EEA | Articles 44A to 46 | Input pack recipients and model provider data use |
| Personal data in sessions, memory, traces, evaluation sets or vector stores | Articles 15(1A), 12A, 17 | Input pack flows (searchable by person) and erasure |
| Public-facing or employee-facing channel | DPA 2018 s 164A | System card contact; input pack measures |
| Likely to be accessed by under-18s | Article 25(1A) | Input pack necessity and proportionality; `counsel_required: yes` |
| Web front end sets cookies or local storage; the agent sends marketing | PECR | Input pack flows; questionnaire cookie inventory |
| Decisions about people; protected characteristics or proxies | Equality Act s 19 | Impact assessment adverse impact and equality |
| Public authority or public functions | Equality Act s 149 | Impact assessment; `counsel_required: yes` |
| Central government client | ATRS | Memo names the record; `counsel_required: yes` |
| UK consumers | CMA AI-agent guidance | System card; questionnaire |
| FCA-authorised client | Consumer Duty; SM&CR | Impact assessment; memo owner |
