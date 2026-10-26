# Australia

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `au` in
scope. Australia has no AI Act, so the Australian sections of the regulatory
memo assign no risk tier. They screen which existing laws and government
policies the agent falls under, from facts the design records, and leave
every legal conclusion to counsel.

## Sources and their status

Read at the primary source on 26 October 2026 unless a line says
"reported; not confirmed at the source on 2026-10-26". Copy `checked
2026-10-26` into a draft only while this file is the newest check.

- Privacy Act 1988, Compilation No. 104, 4 June 2026
  (<https://www.legislation.gov.au/C2004A03712/latest/text>), and the
  Privacy and Other Legislation Amendment Act 2024, No. 128, as made
  (<https://www.legislation.gov.au/C2024A00128/asmade/text>), read in full.
- Privacy Regulation 2013, Compilation No. 20
  (<https://www.legislation.gov.au/F2013L02126/latest/text>); Privacy
  (Australian Government Agencies — Governance) APP Code 2017
  (<https://www.legislation.gov.au/F2017L01396/latest/text>).
- OAIC: APP 1.7 to 1.9 Transparency Obligation Fact Sheet, September 2026
  (<https://www.oaic.gov.au/__data/assets/pdf_file/0021/269013/APP-1.7-1.9-Transparency-Obligation-Fact-Sheet.PDF>),
  read in full; APP Guidelines Chapter 8, updated 3 October 2025; Guide to
  undertaking privacy impact assessments, 2 September 2021; guidance on
  commercially available AI products and on developing and training
  generative AI models, both 21 October 2024 (first 100,000 characters of
  each); small business and employee records exemption pages; the
  notifiable data breach pages (<https://www.oaic.gov.au>).
- Department of Industry, Science and Resources: mandatory guardrails
  consultation page (<https://consult.industry.gov.au/ai-mandatory-guardrails>);
  National AI Plan, 2 December 2025
  (<https://www.industry.gov.au/publications/national-ai-plan>); Guidance
  for AI Adoption, 21 October 2025
  (<https://www.ai.gov.au/staying-safe-and-responsible/essential-ai-practices/guidance-ai-adoption-implementation-guidance>).
- Digital Transformation Agency: Policy for the responsible use of AI in
  government v2.0 and v2.1, Appendix C, the AI impact assessment tool, the
  Standard for AI transparency statements v2.1 and the Agentic AI addendum
  (<https://www.digital.gov.au/ai/ai-in-government-policy>).
- Treasury, Review of AI and the Australian Consumer Law, final report, 3
  October 2025 (<https://treasury.gov.au/publication/p2025-702329>);
  Competition and Consumer Amendment (Unfair Trading Practices) Act 2026
  (<https://www.legislation.gov.au/C2026A00064/asmade>).
- Sector sources named in their sections below.

The full research note, with every secondary item marked, is
`docs/research/au-ai-privacy-law-2026-10-26.md` in the skills repository.

## No AI Act

The government will not proceed with the September 2024 proposals for
mandatory guardrails; the consultation page says feedback informed the
National AI Plan (read 2026-10-26). The Plan of 2 December 2025 says
"established laws remain the foundation for addressing and mitigating
AI-related risks", with regulators acting in their own domains. The memo
says so in one line with `checked 2026-10-26`, and the rest of the
Australian sections screen the laws below.

## Roles under the Privacy Act

Australian privacy law has no controller and processor today. Record these
facts in the memo's Roles section, each conclusion as `counsel:`:

- **APP entities.** The Act binds Australian Government agencies and
  organisations other than small business operators.
- **Small business exemption (s 6D).** Annual turnover of $3 million or
  less, except health service providers, businesses that trade in personal
  information, contracted service providers under a Commonwealth contract,
  credit reporting bodies and the other listed exceptions. Both the client
  and the consultancy are screened: the consultancy is an APP entity in its
  own right when its turnover is above $3 million, or it works under a
  Commonwealth contract.
- **Employee records exemption (s 7B(3)).** Covers an employer's act
  directly related to a current or former employment relationship and an
  employee record. The OAIC says it does not cover unsuccessful job
  applicants, contractors handling another organisation's employee
  information, or recruitment and HR providers working under contract to an
  employer. So the client's exemption does not cover the consultancy. Whether
  it applies to an agency client is `counsel:`; s 7B covers organisations.
- **State contracts (s 7B(5)).** A contracted service provider acting under
  a State contract is exempt from the Act for those acts; the State's own
  privacy law and the contract govern instead.
- **Commonwealth contracts (s 95B).** An agency must put contract terms in
  place so the contracted service provider does not breach the APPs, flowed
  down to subcontracts.
- **Supply-chain roles in Guidance for AI Adoption terms** (clause 1.2): the
  consultancy as system developer, Google as model developer, the client as
  deployer.

A controller and processor split exists only in the tranche 2 exposure
draft (see Mention only). Do not use GDPR roles for Australian law.

## The APPs an agent engages

| APP | What it requires | Agent facts to record |
| --- | --- | --- |
| APP 1.2 | Reasonable steps to implement practices, procedures and systems that ensure compliance | Governance owners; the PIA itself |
| APP 1.4 | The privacy policy covers, among other things, overseas disclosure and the countries where practicable | Inventory rows with countries |
| APP 3 | Collect only what is reasonably necessary; consent for sensitive information unless an exception applies (3.3); collection by lawful and fair means. The OAIC: "If AI systems are used to generate or infer personal information, this is a collection" | Inferred and generated personal information; free text that carries sensitive information |
| APP 5 | A collection notice covering the APP 5.2 matters, including purposes, usual recipients and likely overseas disclosure with the countries | Proposed notice text |
| APP 6 | Use or disclose only for the primary purpose unless a 6.2 exception applies. The OAIC says secondary AI uses are hard to fit within reasonable expectations and recommends consent or a meaningful opt-out; updating a privacy policy does not by itself change reasonable expectations | Re-use of existing customer or staff data for grounding, evaluation or fine-tuning |
| APP 8, s 16C | See Overseas processing below | Endpoint and processing region, logs, support access |
| APP 10 | Reasonable steps so personal information is accurate, up to date, complete and relevant; the OAIC links this to testing and labelling outputs as probabilistic | Evaluation results; output labelling |
| APP 11 | Protect from misuse, interference, loss and unauthorised access (11.1); destroy or de-identify when no longer needed (11.2); since 11 December 2024, "such steps include technical and organisational measures" (11.3, checked 2026-10-26) | SB and C IDs; retention contracts |
| APP 12, 13 | Access and correction; APP 13.5 is an infringement-notice provision | Memory stores, session history and evaluation sets are held information an access request reaches |

Use Australian terms in Australian sections: personal information,
sensitive information, APP entity, contracted service provider, eligible
data breach, PIA, overseas recipient. GDPR terms tell an Australian reviewer
the draft was not written for them.

## Automated-decision transparency (APP 1.7 to 1.9)

**Status.** Inserted by the Privacy and Other Legislation Amendment Act 2024;
commences on 10 December 2026, checked 2026-10-26, and applies to decisions
made after that day whenever the program was arranged or the data
collected. APP 1.7 is a civil penalty provision (s 13K, up to 200 penalty
units) with infringement notices available.

**The test (APP 1.7).** The APP privacy policy must contain the APP 1.8
information if the entity has arranged for a computer program to make, or
do a thing that is substantially and directly related to making, a
decision; the decision could reasonably be expected to significantly affect
the rights or interests of an individual; and personal information about
the individual is used in the operation of the program.

**APP 1.8 contents.** The kinds of personal information used; the kinds of
decisions made solely by the program; the kinds of decisions for which the
program does a thing substantially and directly related to making them.
APP 1.9: deciding includes refusing or failing to decide; effects can be
adverse or beneficial; examples include decisions under an Act, decisions
affecting rights under a contract, and access to "a significant service or
support".

**What the OAIC fact sheet (September 2026) adds.**

- "Computer program" includes rule-based processes, machine learning and
  "generative AI used to generate text, images, videos, code or synthesis,
  including chatbots".
- "Substantially" means "a key factor in facilitating the human's decision
  making"; "directly" means "a direct connection with making the decision".
- Human review is not an exemption: a decision may be in scope "even where
  a computer program output does not replace the entire decision-making
  process or is subject to human review". Machine learning or generative AI
  outputs used in significant decisions "would generally fall within scope
  ... unless subject to extensive human oversight and control".
- "Arranged for" includes procuring a third-party program, configuring
  off-the-shelf software and "reliance on advisory outputs".
- In-scope examples include recruitment software that sorts candidates,
  personalised pricing of significant goods, prioritising health or
  disability services, government benefit or housing eligibility,
  education admission, loan or credit approval, insurance eligibility,
  programmatic advertising for significant goods, facial recognition
  watchlists, AI reports used to rank employee performance or decide
  promotions or pay, scholarships and grants, and immigration processing.
- The duty typically remains with the APP entity making the decision.
  Providers of third-party software "should provide clear, high-level
  information about how their software can be used to make decisions":
  the system card's automated-decision disclosure is that information.
- Commercially sensitive information and trade secrets may be withheld;
  embarrassment is not a ground. When in doubt, the fact sheet says to take
  a cautious approach and disclose.

**Do not imply that recording a reviewer takes the system out of scope.**
APP 1.7 is wider than GDPR Article 22. Write the review step with its
contract ID and the M record of the share reviewed, and leave "significantly
affect" and "extensive human oversight" to counsel.

**Paperwork.** Memo "Australia: Automated decisions (APP 1.7)" table, one
row per decision; system card automated-decision disclosure (APP 1.8 kinds
in plain language); proposed privacy-policy wording in the input pack's
inventory section; `counsel_required: yes` when a decision is in an area the
fact sheet lists.

## Privacy impact assessment

- **Agencies.** The Australian Government Agencies Privacy Code requires a
  PIA "for all high privacy risk projects" (s 12(1)): new or changed ways of
  handling personal information likely to have a significant impact on
  privacy (s 12(2)). Agencies keep and publish a PIA register (s 15).
- **Everyone else.** Recommended, not required: "The OAIC encourages
  organisations to undertake PIAs". The OAIC's AI guidance recommends one.
- **The OAIC's ten steps:** threshold assessment; plan; describe the
  project; identify and consult stakeholders; map information flows;
  privacy impact analysis and compliance check; privacy management; 
  recommendations; report; respond and review. The input pack's common
  sections supply steps 3 to 7 and its "Australia: APP compliance check"
  section supplies step 6.
- **No lawful-basis test.** Australia has no Article 6 equivalent. Never
  write "legal basis: legitimate interests" in an Australian section; the
  analysis runs APP 3, 3.3 and 6.
- **No Article 30 register.** Write the input pack's "Australia: Inventory
  and notice inputs" section instead (APP 1.4 policy contents, APP 5.2
  notice matters, APP 1.8 entries, overseas countries).
- **No works council, no Article 36 prior consultation.** The nearest
  consultation duties are award and enterprise agreement terms and the
  workplace surveillance notice rules below.

## Overseas processing (APP 8 and s 16C)

- Before disclosing to an overseas recipient, an entity takes reasonable
  steps to ensure the recipient does not breach the APPs (APP 8.1); an
  enforceable contract is generally expected (Chapter 8, para 8.16).
  Section 16C makes the disclosing entity liable for the recipient's acts
  that would breach the APPs.
- **Use or disclosure.** Giving personal information to an overseas cloud
  provider is a "use", not a disclosure, where the entity keeps "effective
  control": a binding contract limiting handling to the stated purposes,
  the same obligations on any subcontractors, and control in the entity's
  hands, with security, retrieval and deletion relevant (Chapter 8, para
  8.14). Whether abuse-monitoring storage of flagged prompts, or support
  access from outside Australia, releases effective control is `counsel:`.
- The exceptions in APP 8.2 include a substantially similar law with
  enforcement mechanisms and informed consent. APP 8.3 lets regulations
  prescribe countries or binding schemes; none is prescribed (Privacy
  Regulation 2013, Compilation No. 20).
- **Facts the input pack states:** the regional endpoint; whether the
  pinned model's machine-learning processing is listed in an Australian
  region on the model page; grounding and other services excluded from data
  residency; abuse review and support access; the contract terms. That
  Gemini machine-learning processing is offered in australia-southeast1 and
  that grounding and RAG Engine are excluded from data residency are
  reported; not confirmed at the source on 2026-10-26. Read the model page
  and <https://cloud.google.com/terms/data-residency> for each project.

## Notifiable data breaches and penalties

- On reasonable grounds to suspect an eligible data breach, the entity
  carries out a "reasonable and expeditious assessment", taking all
  reasonable steps to complete it "within 30 days" (s 26WH). On reasonable
  grounds to believe one occurred, it gives the Commissioner a statement "as
  soon as practicable" (s 26WK) and notifies affected individuals (s 26WL).
  Where several entities hold the information (client, consultancy, cloud
  provider), one compliant assessment and notification covers the others
  (ss 26WJ, 26WM). Which entity notifies is `counsel:` and a contract term.
- Agent breach paths to name: prompt injection that exfiltrates data; a
  cross-user session or memory leak; logs sent to the wrong sink; data
  disclosed to a model provider outside the contract.
- **Penalties.** Serious interference with privacy (s 13G): for a body
  corporate the greatest of $50 million, three times the benefit, or 30% of
  adjusted turnover in the breach period; s 13H: 2,000 penalty units;
  s 13K, specified APP breaches including APP 1.7 from 10 December 2026: 200
  penalty units (checked 2026-10-26). The first civil penalties were $5.8
  million against Australian Clinical Labs (OAIC release of 9 October 2025).
  A penalty unit of $364 from 1 July 2026 is reported; not confirmed at the
  source on 2026-10-26.

## OAIC AI guidance and determinations

Measure the PIA against the two OAIC guidance pages of 21 October 2024:

- **Commercially available AI products** (deployers): privacy duties apply
  to inputs and outputs; generated or inferred personal information is
  collected; update policies and notices; do not put personal information
  into public generative AI tools; due diligence, privacy by design and a
  PIA; server location under APP 8; probabilistic labelling under APP 10;
  human oversight.
- **Developing and training generative AI models** (including fine-tuning):
  public availability does not make data usable; scraping is generally a
  covert method of collection; secondary use of held data needs reasonable
  expectations, consent or "a meaningful and informed ability to opt-out";
  a privacy policy alone does not meet APP 5.

Determinations to cite where the facts are close: Clearview AI (biometric
scraping; the 2021 determination stands, statement of 21 August 2024);
Bunnings (the Administrative Review Tribunal accepted facial recognition for
"the limited purpose of combatting very significant retail crime" but the
notice and governance findings stand, and the Commissioner did not appeal,
statement of 5 March 2026); I-MED (no further action because the data
disclosed for AI training was adequately de-identified, 31 July 2025). Any
biometric feature forces counsel and a proportionality section.

## Commonwealth and state government clients

- **DTA Policy for the responsible use of AI in government.** v2.0 took
  effect on 15 December 2025 and v2.1 was published on 21 October 2026
  (checked 2026-10-26). Mandatory for non-corporate Commonwealth entities;
  corporate entities are encouraged; Defence and the intelligence community
  are excluded. Agencies must implement the AI impact assessment for
  in-scope use cases by 15 December 2026, and for existing use cases by 30
  April 2027 (checked 2026-10-26). The assessment starts at design and is
  complete, with treatments applied, before deployment. A use case is in
  scope (Appendix C) on any of: more than insignificant harm; material
  influence on administrative decisions; public interaction or significant
  public effect without human review; use of personal, sensitive or
  security-classified data; DTA designation. An agent touching personal
  data is almost always in scope.
- **The DTA tool:** sections 1 to 4 are a threshold assessment and 5 to 12
  the full assessment, required if any risk is medium or high; each
  assessment has an assessing officer and an approving officer. Each
  agency also publishes an AI transparency statement under the Standard
  v2.1 and keeps a use-case owner and register entry. The Agentic AI
  addendum (AGT.1 to AGT.8, updated 4 June 2026) is strongly recommended,
  not mandatory: memory scope and deletion, bounded workflows and approvals,
  typed tools and access control, adversarial evaluation, monitoring, kill
  switches and decommissioning.
- The pack names the DTA assessment and transparency statement in the memo
  and fills the impact assessment's "Australia: DTA AI impact assessment
  inputs" section; the agency's officers complete the assessment. The PIA
  under the Agencies Privacy Code is required as well.
- **NSW agencies.** Registering and assessing use cases on the NSW AI
  Assessment Framework platform has been mandatory since 30 September 2026
  (checked 2026-10-26); high or critical risk cases go to the AI Review
  Committee.
- **State public sector privacy.** NSW agencies run the Mandatory
  Notification of Data Breach scheme (PPIP Act Part 6A). In Victoria, OVIC's
  generative AI guidance (both pages updated 26 June 2026) says personal
  information should not go into public generative AI tools, outputs
  containing personal information are a new collection, enterprise tools
  need a PIA "per function", and the Victorian Protective Data Security
  Standards bind contracted service providers. Queensland's amended
  Information Privacy Act is reported; not confirmed at the source on
  2026-10-26. Use the state's own PIA template.

## Australian Consumer Law

Sections 18 (misleading or deceptive conduct) and 29 (false representations)
are in force and technology-neutral. Treasury's final report (3 October
2025) found the ACL "generally well adapted" to AI and said a business that
deploys a third-party chatbot "would be liable for the misleading conduct"
to its customers, with a remedy against its supplier. New s 28B, against
conduct that manipulates consumers or unreasonably distorts their decision
environment, including through digital interface design, commences on 1
July 2027 (checked 2026-10-26). For a consumer-facing agent: the system
card's capability claims cite M records, the card records AI disclosure,
and refund, guarantee and retention flows are reviewed in the impact
assessment.

## Screen when the trigger fires

| Law | Trigger | What the pack records |
| --- | --- | --- |
| NSW Workplace Surveillance Act 2005 | Staff in NSW and agent logs or telemetry record their computer use, including prompts | Written notice at least 14 days before computer surveillance starts, under a notified policy (Judicial Commission bench book); the notice is a calendar wait `W`; counsel: is prompt logging computer surveillance? ACT and Victorian rules: counsel |
| NSW Work Health and Safety Amendment (Digital Work Systems) Act 2026 | The agent allocates work | Assent 18 February 2026; main duties await proclamation, not in force (checked 2026-10-26) |
| APRA CPS 234 and CPS 230 | Bank, insurer or super trustee client; agent supports a critical operation | CPS 234: notify APRA within 72 hours of a material information security incident (para 35). CPS 230 (from 1 July 2025, checked 2026-10-26): 72 hours for a material operational risk incident; a register of material service providers, with core technology services presumed material; notice before material offshoring. APRA's 30 April 2026 release adds no requirements and expects AI governance under existing standards |
| My Health Records Act 2012 s 77 | Any My Health Record integration | Nothing held, taken, processed or handled outside Australia: an offshore endpoint or log sink blocks the design |
| Victorian Health Records Act 2001; NSW HRIPA | Health information; health service provider client | State health privacy principles; counsel: which apply |
| TGA software as a medical device | Clinical summarising, triage or decision support | Changes to the clinical decision support exemption take effect 1 November 2026 (checked 2026-10-26); counsel: is any function a medical device? |
| Statutory tort for serious invasions of privacy (Privacy Act Schedule 2) | The design intentionally monitors, profiles or exposes people | Commenced 10 June 2025 (checked 2026-10-26); intentional or reckless invasion only; a PIA risk line |
| Spam Act 2003 | Outbound commercial email, SMS or instant messages | Consent, sender identification, unsubscribe; system card outbound channel |
| Do Not Call Register Act 2006; Telemarketing and Research Calls Industry Standard 2017 | Outbound voice, including synthetic voice (voice calls are outside the Spam Act, s 5(5)) | Register washing, call hours (weekdays 9 am to 8 pm, Saturdays 9 am to 5 pm), a way to get the caller's details during the call, end on request |
| Federal and state anti-discrimination Acts; Fair Work Act general protections | The agent screens, ranks or decides about people | Bias measurement in the impact assessment; counsel: indirect discrimination |
| Cyber Security Act 2024 ss 26 and 27 | Ransomware payment | Report within 72 hours of payment or becoming aware, applying from 30 May 2025 (checked 2026-10-26); the $3 million turnover threshold is reported; not confirmed at the source on 2026-10-26 |
| SOCI Act 2018 | Client is a responsible entity, or the agent holds business critical data for one | Data storage or processing asset facts; counsel |
| Guidance for AI Adoption (voluntary) | Any private client | Impact assessment "Australia: Guidance for AI Adoption mapping" for practices 1 to 3 (decide who is accountable; understand impacts and plan accordingly; measure and manage risks); the names of practices 4 to 6 are reported; not confirmed at the source on 2026-10-26 |

## Mention only

One line each in the memo, with `checked 2026-10-26`:

- **Tranche 2 exposure draft** (Privacy Amendment (Personal Data Protection)
  Bill 2026): consultation 31 August to 18 September 2026; "subject to
  further consideration by government"; not law. It proposes a fair and
  reasonable test, inferences treated as collection, a controller and
  processor split and stronger APP 11 duties; it does not remove the small
  business or employee records exemptions.
- **Children's Online Privacy Code:** must be registered by 10 December
  2026; consultation on the exposure draft closed 5 June 2026; not yet
  registered. Screen public chat agents likely to be used by under-18s.
- **Social media minimum age and online safety codes:** public chatbots
  only; the minimum age has applied since 10 December 2025.
- **Copyright:** the government is not considering a text and data mining
  exception (Attorney-General, 26 October 2025).

## Screening checklist

| Trigger fact (with its ID) | Law | Document and section |
| --- | --- | --- |
| Personal information in prompts, tools, memory, logs or evaluation sets | Privacy Act and APPs | Memo "Australia: Privacy Act and APPs"; input pack flows and APP compliance check |
| Client or consultancy turnover at or below $3 million | s 6D small business exemption and its exceptions | Memo Roles (`counsel:`) |
| The consultancy handles personal information (build, test, support) | Consultancy as APP entity; s 6D, s 7B, s 95B | Memo Roles; inventory consultancy rows |
| Client is a Commonwealth agency | Agencies Privacy Code s 12 PIA; s 95B; DTA policy | Input pack (PIA required); impact assessment DTA inputs; `counsel_required: yes` |
| Client is a state agency, council or state-owned corporation | s 7B(5); state privacy Acts; NSW AI Assessment Framework | Memo Roles and sector section; state PIA template |
| Data subjects are the client's employees | Employee records exemption (client only); workplace surveillance | Memo Roles; workplace surveillance notice wait |
| Output feeds a decision about a person: contract right, benefit, significant service, employment, credit, insurance, health, education, pricing | APP 1.7 to 1.9; anti-discrimination | Memo APP 1.7 table; system card disclosure; impact assessment bias; `counsel_required: yes` |
| Endpoint, processing, logs, grounding, abuse review or support outside Australia, or not listed in Australia | APP 8.1, s 16C; APP 5.2 | Input pack recipients and inventory countries |
| Sensitive information collected, inferred or likely in free text | APP 3.3; APP 6.2 | Input pack data subjects and APP check |
| Biometric features | APP 3.3; Bunnings and Clearview determinations | Input pack proportionality; `counsel_required: yes` |
| Re-use of existing customer or staff data | APP 6; OAIC training guidance | Input pack necessity and proportionality |
| Consumers, or claims about products, refunds or guarantees | ACL ss 18 and 29; s 28B from 1 July 2027 | System card claims and disclosure; impact assessment |
| Any personal information held | Notifiable data breaches | Questionnaire incident response |

## Questions counsel usually gets

- Is the consultancy an APP entity for this engagement, and does any
  exemption apply?
- Is sending prompts to the model endpoint a use or a disclosure under APP
  8, and is the Google Cloud contract enough for reasonable steps?
- Is the agent's use of existing data a related secondary purpose within
  reasonable expectations, or does it need consent?
- Does a decision "significantly affect" rights or interests, and is the
  review "extensive human oversight and control"?
- Does the client's privacy policy need amending before 10 December 2026?
- Which entity notifies an eligible data breach?
