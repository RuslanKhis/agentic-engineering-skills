# Australia

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `au` in
scope. Australia has no AI Act, so the Australian sections of the regulatory
memo assign no risk tier. They screen which existing laws and government
policies the agent falls under, from facts the design records, and leave
every legal conclusion to counsel.

**Which sections to read.** Every Australian pack: Roles, the APPs,
automated-decision transparency, privacy impact assessment, overseas
processing, notifiable data breaches, the screen and the checklist. When
Australia is in scope only through the consultancy's own handling, those
are enough. Add "Commonwealth and state government clients" for any
government client, "NSW government clients" for a NSW agency or State
contract, and the Consumer Law and sector rows when their trigger fires.
Whether the Privacy Act reaches a foreign client's data merely hosted or
read in Australia is not covered here: write it as `counsel:`.

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
- NSW government (read 26 October 2026 for the NSW sections below):
  DCS-2026-02 (<https://arp.nsw.gov.au/dcs-2026-02-use-of-artificial-intelligence-by-nsw-government-agencies>);
  the NSW AI Operational Policy, Final v1.1, and the AIAF and AI Review
  Committee pages (<https://www.digital.nsw.gov.au>); the NSW Cyber
  Security Policy 2026–2027; ICTA (August 2025) and the Core& One Core Terms
  (<https://www.info.buy.nsw.gov.au>); the Information and Privacy
  Commission's PPIP Act, IPP, s 19(2), HRIP Act, HPP, mandatory data breach,
  privacy management plan, AI PIA, generative AI and GIPA pages
  (<https://www.ipc.nsw.gov.au>); State Records NSW's legislation and AI
  recordkeeping pages; DPC circular C2005-37 on the Workplace Surveillance
  Act; the NSW Law Reform Commission's Anti-Discrimination Act review page.
  **legislation.nsw.gov.au, AustLII and parliament.nsw.gov.au refused
  automated reads that day**, so NSW statutory wording comes from the
  regulators' pages that quote it, or from a superseded 2016 compilation of
  the PPIP Act; each such point says "re-read the section at the source".

The full research notes, with every secondary item marked, are
`docs/research/au-ai-privacy-law-2026-10-26.md` and
`docs/research/au-government-forms-nsw-2026-10-26.md` in the skills
repository.

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
- **More on the DTA forms** (checked 2026-10-26). The AI impact assessment
  tool v1.0 was published on 1 December 2025. Section 3 rates **inherent**
  risk, before controls; an inherent high risk is reported to the
  accountable official, governed through a board or senior executive,
  reported to the DTA once deployment is decided and reviewed at least every
  12 months. Since v2.0 a **Commonwealth AI Review Committee** gives
  non-binding advice on use cases with a residual high-risk rating, or that
  agencies deem highly sensitive, novel or complex, up to PROTECTED. The
  tool's question 1.7 lists four usage patterns while Appendix D of policy
  v2.1 lists seven. The DTA AI model clauses (17 March 2025) are the
  vendor's contract duties; their text is reported; not confirmed at the
  source on 2026-10-26. The form crosswalks, and the
  `government-form-answers` document they produce, are in
  [AU government crosswalks](au-government-crosswalks.md).
- **NSW agencies.** Registering and assessing use cases on the NSW AI
  Assessment Framework platform has been mandatory since 30 September 2026
  (checked 2026-10-26); high or critical risk cases go to the AI Review
  Committee. See "NSW government clients" below for the policy, the state
  law and the contract terms.
- **State public sector privacy.** NSW agencies run the Mandatory
  Notification of Data Breach scheme (PPIP Act Part 6A). In Victoria, OVIC's
  generative AI guidance (both pages updated 26 June 2026) says personal
  information should not go into public generative AI tools, outputs
  containing personal information are a new collection, enterprise tools
  need a PIA "per function", and the Victorian Protective Data Security
  Standards bind contracted service providers. Queensland's amended
  Information Privacy Act is reported; not confirmed at the source on
  2026-10-26. Use the state's own PIA template.

## NSW government clients

Read when the client is a NSW public sector agency or state owned
corporation, or the consultancy works under a NSW State contract. A NSW
agency client always sets `counsel_required: yes`. Write NSW sections in
NSW terms: personal information, health information, IPP, HPP, public
sector agency, privacy management plan, eligible data breach under Part
6A. Never use APP terms for the agency's own duties. Each point below was
checked 2026-10-26; NSW statute wording the research could not read at
legislation.nsw.gov.au is marked "re-read the section at the source".

### Policy: DCS-2026-02, the Operational Policy and the AIAF

- **DCS-2026-02**, "Use of Artificial Intelligence by NSW Government
  Agencies", was issued on 30 July 2026 and updated on 1 September 2026. It
  is mandatory for departments, executive agencies, separate agencies,
  statutory bodies, state owned corporations, public financial and
  non-financial corporations, advisory entities and NSW Government
  subsidiaries, and replaces DCS-2024-04.
- It mandates the **NSW AI Operational Policy, Final v1.1**, which replaces
  the NSW AI Ethics Policy and makes Australia's eight AI Ethics Principles
  "the mandatory NSW Government AI ethical principles". The policy's cover
  says 30 July 2026 while its version table reads v1.1 approved on 31
  August 2026; quote the cover and note the table.
- Agencies must adhere to the principles, appoint an Accountable Official,
  establish governance and assurance, register **all** AI use cases on the
  AIAF Platform with lifecycle records, apply the AIAF where registration
  requires it, refer high and critical risk use cases to the AI Review
  Committee, align acceptable use policies and offer AI training. The first
  annual attestation is due by 31 October 2027.
- **AIAF risk bands** (Operational Policy): low ("can be easily reversed or
  corrected without causing any harm or damage"), medium ("noticeable but
  ... generally limited and manageable"), high ("substantial risk profile
  ... significant, affect trust or operations") and critical ("the highest
  level of risk ... severe, widespread, or irreversible"). The band is
  **intrinsic**: what the use case involves and how it is intended to be
  used, not how it may later be mitigated. The 2024 AIAF, still used in the
  Excel transition process, referred residual high and very high risk.
- **AI Review Committee.** Agencies "must refer critical and high-risk AI use
  cases", by email to the AI Secretariat "within 5 business days of
  completing the AIAF"; NSW GovAI may also refer medium-risk cases with
  higher-risk characteristics. The committee advises; the agency keeps the
  decision. Write the referral as a calendar wait `W` that the production
  goal depends on.
- **Cost is not the trigger.** Projects over $5 million, or funded by the
  Digital Restart Fund, get Digital Assurance Framework oversight, which
  then checks AIAF compliance; AI Review Committee referral follows the
  band.
- **The vendor does not register.** The Operational Policy is not mandatory
  for third-party suppliers, and its registration rule "does not apply to
  third-party suppliers"; the agency's Accountable Owner registers. The
  consultancy supplies evidence, and the pack drafts answers in
  `government-form-answers-<form>.md` from
  [AU government crosswalks](au-government-crosswalks.md).
- The AI agent usage and deployment guidance (October 2025) is "a guideline
  only. It is not mandatory"; its production checklist asks to update the
  AIAF assessment and register the agent in the asset register.

### Roles: the s 7B(5) State contract rule

The Privacy Act 1988 defines a "State contract" as one "under which services
are to be, or were to be, provided to a State or Territory authority"
(s 6(1)). An organisation's act is exempt if it is "a contracted service
provider for a State contract" and the act is done "for the purposes of
meeting (directly or indirectly) an obligation under the contract" (s
7B(5)). So the consultancy's acts for the NSW contract fall outside the
APPs, and the IPC says outside the Commonwealth notifiable data breach
scheme too. For everything else (its own staff, other clients, any reuse of
agency data for its own purposes, which the contract should forbid) the
consultancy stays an APP entity unless s 6D exempts it. The PPIP Act binds
the **agency**, not the contractor: "The service provider will only be
subject to NSW privacy law if specifically required under the contract"
(IPC). The HRIP Act can bind the consultancy directly (below). Whether every
act is "for the purposes of meeting" the contract is `counsel:`.

### PPIP Act 1998: the IPPs and s 19(2)

- The 12 IPPs (ss 8 to 19, IPC fact sheet, August 2026): lawful, direct,
  open, relevant collection; secure; transparent; accessible; correct;
  accurate before use; limited use; restricted disclosure; and special
  restrictions on disclosure (s 19).
- **Section 19(2) reaches any recipient outside NSW**, including other
  Australian states and a Commonwealth agency: an agency "must not disclose
  the information to any person or body who is in a jurisdiction outside New
  South Wales or to a Commonwealth agency unless" a ground applies, among
  them a reasonable belief that the recipient is bound by substantially
  similar principles, express consent, and "reasonable steps" to ensure the
  recipient will not handle it inconsistently with the IPPs (IPC fact
  sheet, November 2019; re-read the section at the source). The IPC names no
  jurisdictions and "urges caution"; for reasonable steps it expects at
  least an enforceable contract requiring IPP-compliant handling, with
  enforcement rights, complaints, breach notice to the agency and flow-down
  to subcontractors. **This is stricter than APP 8**: a Melbourne support
  engineer, a non-NSW region or abuse-monitoring storage elsewhere is
  "outside NSW".
- **Use or disclosure.** The IPC's AI PIA guide says vendor access "for the
  sole purpose of carrying out a contracted service ... is likely to be a
  'use'". Whether a given flow is a use or a disclosure, and which s 19(2)
  ground applies to a disclosure, is `counsel:`.
- Information a contractor holds for the engagement is "held" by the
  agency (s 4(4)), and the agency does everything reasonably within its
  power to prevent unauthorised use or disclosure by service providers
  (s 12(d)); both are from the superseded 2016 compilation: re-read the
  sections at the source. Sensitive information under s 19(1) must pass
  s 19(1) first.
- **Privacy management plan (s 33).** It covers compliance with the PPIP
  and HRIP Acts and, under s 33(2)(c1), the Part 6A procedures (IPC guide,
  May 2026); "the plan should include information about the use of AI and
  ADM". Re-read s 33 at the source. The update is the agency's
  (`agency:`).
- Paperwork: the input pack's "Australia: NSW IPP and HPP check" replaces
  the APP check for the agency's handling, with an "outside NSW?" column per
  flow; proposed s 10 notice text (the IPC prefers a chatbot's notice "at
  the time the conversation is occurring"); a contract privacy schedule as
  `counsel:`.

### HRIP Act 2002: health information

The 15 HPPs apply to public sector agencies and to private sector persons
that provide a health service or collect, hold or use health information,
so **the HRIP Act can bind the consultancy directly** (IPC). HPP 14 controls
transfer of health information outside NSW; the AI PIA guide lists the main
grounds (equivalent standards, consent, or a contract benefiting the person
where consent is impracticable); re-read HPP 14 at the source. A citizen
mentioning a condition to a transport agent is health information in free
text. A turnover qualifier for some businesses is reported; not confirmed
at the source on 2026-10-26. Counsel: is the consultancy an "organisation"
bound in its own right; is HPP 14 met?

### Mandatory Notification of Data Breach scheme (PPIP Act Part 6A)

From 28 November 2023, every NSW public sector agency bound by the PPIP Act
must notify the Privacy Commissioner and affected individuals of eligible
data breaches (IPC guide, July 2024). The agency contains the breach
immediately, completes the assessment within 30 days (s 59E(2)(b)),
notifies the Commissioner immediately on the approved form (s 59M) and
individuals as soon as reasonably practicable, keeps a published data
breach policy (s 59ZD) and an internal register (s 59ZE). The section that
lets the agency extend the 30 days was not verified: re-read Part 6A at the
source. The scheme "does not generally apply to contracted service
providers", but in hosted services "in most cases the agency will be
considered to hold" the information (s 59C), so the contract should require
the provider to report promptly, mitigate and assist. Whether the agency
holds data in the consultancy's development, test and log environments is
`counsel:`.

### GIPA Act 2009

- Agencies keep a **government contracts register** of contracts with
  private sector entities valued at $150,000 (including GST) or more, with
  more particulars for larger contracts and a copy where the contract is
  more than, or expected to reach, $5 million (IPC); commercial-in-confidence
  provisions may be excluded with reasons. Re-read GIPA ss 27 to 35 at the
  source.
- **Section 121.** A contract for **services to the public on behalf of** an
  agency must give the agency an "immediate right of access" to information
  about the contractor's performance, information collected from the
  public and information received from the agency (IPC). A public-facing
  agent the consultancy operates is the case to screen; whether s 121
  applies is `counsel:`.
- Access rights "remain applicable" to technology-assisted decisions, and
  databases, SaaS content and audit logs are records (IPC), so prompts,
  outputs and traces the agency holds are government information; the
  design needs log export and search, or a `gap:`. Agency information
  guides should list "machine-enhanced decision-making systems" (IPC fact
  sheet, August 2024).

### State Records Act 1998

There is no State Records Act 2024: the State Records Act 1998 still
governs (State Records NSW), and the State Records Regulation 2024
commencing on 1 September 2024 is reported; not confirmed at the source on
2026-10-26. State Records NSW: "any record created during government
business – whether by AI, a computer system, or a person – is a State
record", with metadata on AI-generated status, "the software used" and "the
prompts, inputs or algorithms used", and "It is not enough to leave them in
the AI tool". The Operational Policy says AI outputs and metadata are State
records. **Prompts and outputs used in government business are State
records**: the design exports them, with model ID and version and
timestamps, to the agency's recordkeeping system (a goal for
adk-agent-observability and adk-memory-architecture), retention follows the
agency's disposal authority (`agency:`), and the contract provides for
return or destruction at its end. The Act's section numbers were not read:
re-read them at the source before citing one.

### NSW Cyber Security Policy 2026–2027

Mandatory for departments, public service agencies and statutory
authorities (not state owned corporations, councils or universities), and it
covers third-party and shared services. Requirements 3.3 to 3.10 "embed the
Maturity Level One Essential Eight controls": **Maturity Level One is the
mandatory baseline**, and higher maturity is risk-based. Cyber incidents are
reported through the Cyber Portal "within 24 hours of detection and
classification". Suppliers: a contractually supported process to notify
incidents and data breaches (1.10.2) and contract cyber clauses with break
clauses (1.10.4). Paperwork: the questionnaire's Government security policy
row, ML1 evidence for the delivered environment, and an incident procedure
that fits inside the agency's 24 hours.

### NSW contract AI clauses: ICTA clause 6.11 and Core&

- Procurement uses the ICT Purchasing Framework (PBD-2025-03): Core& for
  low-risk buys up to $1 million excluding GST, MICTA and ICTA for high-risk
  buys or $1 million or more.
- **ICTA (August 2025) clause 6.11, AI Systems.** Other than AI systems set
  out in the Order Form, no use of an AI system without written notice, a
  three-month wait (or another period set by a Module or the Order Form)
  and the customer's prior written approval; "detailed records of any AI
  System ... (including records of the design (including functions, features
  and interconnected systems), performance, governance and intended and
  actual use)"; a warranty of risk-managed design, training and testing. By
  default it also requires an AI incident programme, **six months' notice of
  "a change to the underlying model"**, Customer Data kept in NSW unless the
  Order Form permits otherwise, and security incident notice "immediately",
  then details within 48 hours.
- **Core& One Core Terms (August 2025):** three months' notice and consent
  before using AI; AI logs are Buyer Data; no personal information outside
  Australia, or accessed from outside it; breach notice within 48 hours.
- **The model-change notice meets the model lifecycle check.** List the
  Gemini model IDs in the Order Form. Compare the notice period with the
  pinned model's retirement date (SKILL.md, "Read the record first"): **a
  retirement date inside the notice window**, or a forced migration the
  supplier cannot announce six months ahead, **is a gap** for
  adk-model-and-output-contracts and adk-release-engineering **and a
  counsel question** on the notice period and the Order Form terms. When the
  retirement date cannot be read, the conflict stays a `gap:` until it is.
- Customer Data in NSW: Google Cloud australia-southeast1 is in Sydney, but
  check the model's processing region and support access on the model page.

### NSW Workplace Surveillance Act and anti-discrimination

- The Workplace Surveillance Act 2005 notice (at least 14 days, s 10, per
  DPC circular C2005-37) is in "Screen when the trigger fires" below; for a
  NSW agency client the notice is the agency's, a wait of at least 14 days
  before production if identity-linked logs of staff prompts count as
  computer surveillance (`counsel:`), and whether consultancy staff on
  agency systems receive notice from the agency, the consultancy or both is
  `counsel:`. Re-read ss 10 to 22 at the source.
- The NSW Anti-Discrimination Act 1977 review is still in progress, with no
  new Act and no final report (NSW Law Reform Commission page, last updated
  26 October 2026). Show bias measurement in the impact assessment and leave
  indirect discrimination to `counsel:`.

### What a NSW agency produces, and what the pack supplies

| Item | Owner | Pack document |
| --- | --- | --- |
| AIAF Platform registration and assessment; review committee referral within 5 business days for high or critical | Agency (Accountable Owner) | government-form-answers documents; impact assessment |
| Agency PIA under the IPC guides | Agency | Input pack with "Australia: NSW IPP and HPP check" |
| s 19(2) and HPP 14 analysis | Agency, `counsel:` | Input pack recipients and the "outside NSW?" flow table |
| Privacy management plan update; Part 6A policy and register entry | Agency | Memo; security questionnaire |
| GIPA contract register entry; s 121 access clause | Agency | Memo "Australia: Government client" |
| State records capture of outputs and metadata | Agency; design | Design goal; system card Data |
| Cyber Security Policy mapping, ML1 evidence, 24-hour incident path | Agency; consultancy evidence | Security questionnaire |
| ICTA 6.11 Order Form AI list, records, model-change notice | Contract | Memo "Australia: Government client"; design model decision |
| Workplace surveillance notice | Agency | Wait `W` |
| Digital Assurance Framework gateway (over $5 million or DRF funded) | Agency | Wait `W` |

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
| NSW Workplace Surveillance Act 2005 | Staff in NSW and agent logs or telemetry record their computer use, including prompts | Written notice at least 14 days before computer surveillance starts, under a notified policy (Judicial Commission bench book); the notice is a calendar wait `W`; counsel: is prompt logging computer surveillance? Staff in other states, including the ACT, Victoria and Queensland: counsel, because this reference does not cover their rules |
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
| The people affected are the client's employees | Employee records exemption (client only); workplace surveillance | Memo Roles; workplace surveillance notice wait |
| Output feeds a decision about a person: contract right, benefit, significant service, employment, credit, insurance, health, education, pricing | APP 1.7 to 1.9; anti-discrimination | Memo APP 1.7 table; system card disclosure; impact assessment bias; `counsel_required: yes` |
| Endpoint, processing, logs, grounding, abuse review or support outside Australia, or not listed in Australia | APP 8.1, s 16C; APP 5.2 | Input pack recipients and inventory countries |
| Sensitive information collected, inferred or likely in free text | APP 3.3; APP 6.2 | Input pack data subjects and APP check |
| Biometric features | APP 3.3; Bunnings and Clearview determinations | Input pack proportionality; `counsel_required: yes` |
| Re-use of existing customer or staff data | APP 6; OAIC training guidance | Input pack necessity and proportionality |
| Consumers, or claims about products, refunds or guarantees | ACL ss 18 and 29; s 28B from 1 July 2027 | System card claims and disclosure; impact assessment |
| Any personal information held | Notifiable data breaches | Questionnaire incident response |
| Client is a NSW agency, or the consultancy works under a NSW State contract | DCS-2026-02 and the AIAF; s 7B(5); PPIP and HRIP Acts; Part 6A; GIPA; State Records Act 1998; NSW Cyber Security Policy; ICTA 6.11 | Memo "Australia: Government client"; input pack NSW IPP and HPP check; government form answers; `counsel_required: yes` |
| Any flow to a recipient outside NSW (another state, an overseas region, support staff elsewhere) for a NSW agency | PPIP Act s 19(2); HPP 14 for health information | Input pack "outside NSW?" flow table (`counsel:`) |
| NSW contract lists a model-change notice period | ICTA clause 6.11 | Memo government row; model retirement date against the notice window (`gap:` and `counsel:` if inside it) |
| Contract of $150,000 (including GST) or more with a NSW agency; the agent serves the public for the agency | GIPA contracts register; s 121 | Memo government row (`agency:`, `counsel:`) |
| Client is a non-corporate Commonwealth entity | DTA policy and tool; Commonwealth AI Review Committee | Government form answers from [AU government crosswalks](au-government-crosswalks.md) |

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
- For a NSW agency: is the model endpoint, logging or support access a use
  or a disclosure to a recipient outside NSW, and which s 19(2) ground
  applies to a disclosure? Does the contract meet the IPC's reasonable-steps
  minimum?
- Is everything the consultancy does "for the purposes of meeting" the State
  contract (s 7B(5))?
- Does the agency hold, under s 59C, data in the consultancy's environments,
  and who notifies a Part 6A breach?
- Does the agent provide services to the public on behalf of the agency
  (GIPA s 121)?
- Does any output feed an administrative decision under an Act, needing
  express legislative authority?
- Which AIAF band applies, and is review committee referral needed?
- Does the ICTA model-change notice period fit the pinned model's
  retirement date, and which AI systems does the Order Form list?
