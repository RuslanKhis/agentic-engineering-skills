# Australia: privacy and AI law for the governance pack

*Read 26 October 2026. Research for adding Australia to
`skills/adk-governance-pack`. Drafts, not legal advice.*

## Conclusion

Australia has no AI Act and, as of today, is not going to get one soon.
The September 2024 proposal for mandatory guardrails in high-risk settings
was dropped. The National AI Plan of 2 December 2025 relies on existing
laws, sector regulators and voluntary guidance. An Australian
"classification memo" is therefore not a risk-tier classification. It is a
**regime screen**: which existing laws and government policies the agent
falls under, triggered by facts the design already records (client type,
data subjects, data categories, where data is processed, decision effects,
outbound channels).

The Privacy Act 1988 carries most of the weight. What changes the pack:

1. **Automated-decision transparency starts on 10 December 2026, checked
   2026-10-26** (APP 1.7 to 1.9, inserted by the Privacy and Other
   Legislation Amendment Act 2024). The test is wider than GDPR Article 22.
   A computer program that does "a thing that is substantially and
   directly related to making" a decision is caught, even when a person
   signs off. The OAIC says machine learning or generative AI outputs used
   in such decisions "would generally fall within scope ... unless subject
   to extensive human oversight and control". Its list of in-scope
   decisions is close to Annex III. The OAIC also says vendors should give
   the client "clear, high-level information" for its privacy policy. The
   system card is where that goes.
2. **The DPIA becomes a Privacy Impact Assessment (PIA).** It follows the
   OAIC's 10-step guide. A PIA is mandatory for Australian Government
   agencies on "high privacy risk projects" (Australian Government Agencies
   Privacy Code s 12) and recommended for everyone else. There is no
   lawful-basis test. The analysis runs APP by APP: APP 3 (collection is
   reasonably necessary; consent for sensitive information), APP 5
   (notice), APP 6 (primary purpose and the secondary-use exceptions),
   APP 8 (overseas), APP 10 (quality), APP 11 (security), APP 12 and 13
   (access and correction).
3. **Records of processing have no Australian equivalent.** There is no
   Article 30. The nearest duties are APP 1.2 (practices, procedures and
   systems), the APP 1.4 privacy policy contents, the APP 5 collection
   notice and, from 10 December 2026, the APP 1.8 entries. Replace the
   records document with a **personal information inventory and notice
   inputs** document. Its rows feed the client's privacy policy, its
   collection notice and its automated-decision disclosure.
4. **Australian law has no controller and processor today.** A
   consultancy that handles personal information is an APP entity in its
   own right, unless it is a small business with a turnover of $3 million
   or less and none of the exceptions applies. The client's employee
   records exemption does not cover the consultancy. The OAIC says it does
   not cover contractors handling another organisation's employee records.
   A controller and processor split exists only in the August 2026
   exposure draft bill, which is not law.
5. **Offshore model processing is an APP 8 question.** Sending personal
   information to a model endpoint outside Australia may be a "use" (the
   provider is bound by contract, any subcontractors are bound the same
   way, and the entity keeps effective control) or a "disclosure". If it
   is a disclosure, APP 8.1 applies and s 16C makes the client accountable
   for the recipient's breaches. No country has been prescribed under the
   new APP 8.3. The regional endpoint, the ML processing location and the
   grounding exclusions become facts the PIA must state.
6. **Government clients bring hard paperwork with near deadlines.**
   - **Commonwealth agencies.** DTA policy v2.0 took effect on 15 December
     2025 and v2.1 was published on 21 October 2026. Agencies must
     implement the AI impact assessment for in-scope use cases by
     15 December 2026, checked 2026-10-26, using the DTA tool or an
     equivalent. They also need an owner for each use case, a register
     entry and inputs to the agency's AI transparency statement, plus the
     PIA under the Agencies Privacy Code.
   - **NSW agencies.** Registering and assessing use cases on the NSW AI
     Assessment Framework platform has been mandatory since 30 September
     2026, checked 2026-10-26.
7. **The pending items are not law yet.**
   - The Children's Online Privacy Code must be registered by 10 December
     2026. Consultation on the exposure draft closed on 5 June 2026.
   - The "tranche 2" exposure draft, the Privacy Amendment (Personal Data
     Protection) Bill 2026, was released on 31 August 2026 and
     consultation closed on 18 September 2026. It has not been introduced
     to Parliament. It proposes the fair and reasonable test, an expanded
     definition of sensitive information, inferences treated as
     collection, a controller and processor split, and stronger APP 11
     duties. It does not remove the small business or employee records
     exemptions.
   Mention both as "pending, re-check before relying on them".

Recommended shape: a jurisdiction switch in the pack.
- **Australian classification memo.** A regime screen in place of the
  EU AI Act memo.
- **PIA input pack.** The OAIC's 10 steps with an APP-by-APP compliance
  check. Replaces the DPIA input pack.
- **Personal information inventory and notice inputs.** Replaces the
  records of processing.
- **AI impact assessment.** Keep it, mapped to the Guidance for AI
  Adoption (AI6). For Commonwealth clients also produce a DTA impact
  assessment input pack.
- **System card.** Gains an APP 1.8 disclosure block.
- **Security questionnaire.** Gains Australian incident-notification
  clocks and the Essential Eight, ISM and PSPF frameworks clients ask
  about.

## Sources

"P" means I read it on the primary source on 26 October 2026. "S" means
it came from secondary reporting or search-result summaries only and must
be re-read before anyone relies on it. Two research forks read the
government AI policy and the "other laws" sources on the same day under
the same rules. Their readings are marked the same way.

### Privacy Act and OAIC (read by the coordinator)

| Source | Status | Used for |
| --- | --- | --- |
| Privacy and Other Legislation Amendment Act 2024, No. 128, 2024, as made (<https://www.legislation.gov.au/C2024A00128/asmade/text>, full text via its epub HTML) | P, read in full | Commencement table; APP 1.7–1.9; APP 11.3; APP 8.3; ss 13G, 13H, 13K; s 26GC Children's code; Schedule 2 tort |
| Privacy Act 1988, Compilation No. 104, compilation date 4 June 2026 (<https://www.legislation.gov.au/C2004A03712/latest/text>) | P | APP text; ss 6D, 7B, 13G penalties, 16C, 26WH–26WL, 95B |
| Privacy Regulation 2013, Compilation No. 20, 11 February 2025 (<https://www.legislation.gov.au/F2013L02126/latest/text>) | P | No country or scheme prescribed for APP 8.3 |
| Privacy (Australian Government Agencies — Governance) APP Code 2017, F2017L01396 (<https://www.legislation.gov.au/F2017L01396/latest/text>) | P | s 12 PIA for high privacy risk projects; s 15 PIA register |
| OAIC, APP 1.7–1.9 Transparency Obligation Fact Sheet, September 2026 (<https://www.oaic.gov.au/__data/assets/pdf_file/0021/269013/APP-1.7-1.9-Transparency-Obligation-Fact-Sheet.PDF>) | P, read in full | Scope tests, in-scope decision list, vendor role, commercial-in-confidence carve-out |
| OAIC news, "New resources on transparency for use of AI and automated decision-making", 30 September 2026 (<https://www.oaic.gov.au/news/media-centre/new-resources-on-transparency-for-use-of-ai-and-automated-decision-making>) | P | Release date; APP 1 Guidelines update; agency fact sheet; flowchart |
| OAIC, APP Guidelines Chapter 1 v2 (September 2026 PDF) | S, title and listing only | Chapter 1 v2.0 effective 29 September 2026, per search summary of the OAIC version-history page |
| OAIC, Guidance on privacy and the use of commercially available AI products, 21 October 2024, header shows updated 17 January 2025 (<https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/guidance-on-privacy-and-the-use-of-commercially-available-ai-products>) | P, first 100,000 characters | Deployer duties APP 1, 3, 5, 6, 8, 10, 11 |
| OAIC, Guidance on privacy and developing and training generative AI models, 21 October 2024, updated 23 October 2024 (<https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/guidance-on-privacy-and-developing-and-training-generative-ai-models>) | P, first 100,000 characters | Fine-tuning, secondary use, scraping, notice |
| OAIC, Children's Online Privacy Code page (<https://www.oaic.gov.au/privacy/privacy-registers/privacy-codes/childrens-online-privacy-code>) | P | Exposure draft; consultation 31 March to 5 June 2026; register by 10 December 2026 |
| OAIC, Small business page (<https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business>) | P | $3m threshold and the exceptions |
| OAIC, Employee records exemption, December 2015 (<https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/employee-records-exemption>) | P | Scope; contractors not covered |
| OAIC, APP Guidelines Chapter 8, updated 3 October 2025 (<https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-8-app-8-cross-border-disclosure-of-personal-information>) | P | Use versus disclosure for overseas cloud (para 8.14); reasonable steps (8.16) |
| OAIC, Guide to undertaking privacy impact assessments, 2 September 2021 (<https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/privacy-impact-assessments/guide-to-undertaking-privacy-impact-assessments>) | P, first 100,000 characters | Ten steps; mandatory only for agencies |
| OAIC NDB pages (about the scheme; when to report) | P | Definitions; the 30-day rule read in s 26WH |
| OAIC, Australian Clinical Labs penalties, 9 October 2025 (<https://www.oaic.gov.au/news/media-centre/australian-clinical-labs-ordered-to-pay-penalties-in-relation-to-medlab-pathology-data-breach-in-first-for-privacy-act>) | P | First civil penalties; $5.8m |
| OAIC, Privacy Commissioner statement on the ART's Bunnings decision, 5 March 2026 (<https://www.oaic.gov.au/news/media-centre/privacy-commissioner-statement-on-administrative-review-tribunals-bunnings-decision>) | P | Outcome; no appeal |
| OAIC, updated facial recognition guidance, 29 July 2026 (<https://www.oaic.gov.au/news/media-centre/privacy-commissioner-publishes-updated-guidance-on-facial-recognition-in-retail-spaces>) | P | Kmart under ART review, hearings early 2027 |
| Commissioner Initiated Investigation into Kmart Australia Limited (Privacy) [2025] AICmr 155, 26 August 2025 (OAIC PDF) | S, title and search summary | Breaches of APP 3.3 and 5.1 |
| OAIC, Statement on Clearview AI, 21 August 2024 (<https://www.oaic.gov.au/news/media-centre/statement-on-clearview-ai>) | P | The 2021 determination stands |
| OAIC, I-MED preliminary inquiries report, 31 July 2025 (<https://www.oaic.gov.au/privacy/privacy-assessments-and-decisions/privacy-decisions/Investigation-inquiry-reports/report-into-preliminary-inquiries-of-i-med>) | P | De-identification before disclosure for AI training |
| OAIC, regulatory action priorities 2025–26, 29 July 2025 (<https://www.oaic.gov.au/news/media-centre/oaic-releases-regulatory-action-priorities-for-2025-26>) | P | AI, biometrics, ad tech |
| AGD, Privacy Reform consultation page (<https://consultations.ag.gov.au/rights-and-protections/privacy-reform/>), consultation paper and Exposure Draft Privacy Amendment (Personal Data Protection) Bill 2026 (PDFs on that page) | P; consultation paper read in full, draft bill searched | Tranche 2 contents and status |
| Bunnings Group Limited and Privacy Commissioner [2026] ARTA 130 | S (G+T, ABC, Biometric Update) | Permitted general situation accepted; APP 1.2, 1.3 and 5.1 breaches stand |
| Commonwealth penalty unit $364 from 1 July 2026 | S (ASIC fines page via search) | Converting penalty units |
| Gemini on Google Cloud: ML processing in australia-southeast1, grounding and RAG Engine excluded from data residency | S (search summaries of docs.cloud.google.com and cloud.google.com/terms/data-residency) | APP 8 facts; re-read the model page |

### Government AI policy (fork B)

| Source | Status | Used for |
| --- | --- | --- |
| DISR, Voluntary AI Safety Standard, published 5 September 2024, updated 2 December 2025 (<https://www.industry.gov.au/publications/voluntary-ai-safety-standard>) | P | 10 guardrails; the Guidance for AI Adoption "evolves" it |
| NAIC, Guidance for AI Adoption: Foundations and Implementation guidance, 21 October 2025 (<https://www.ai.gov.au/staying-safe-and-responsible/essential-ai-practices/guidance-ai-adoption-implementation-guidance>) | P for practices 1–3; S for the names of practices 4–6 | Six essential practices |
| NAIC templates: AI policy, AI register, supplier questions, 22 April 2026 (<https://www.ai.gov.au/practical-guides-and-learning/planning-tools-and-templates>) | P | Register row shape |
| Consultation hub, mandatory guardrails proposals paper (<https://consult.industry.gov.au/ai-mandatory-guardrails>) | P | "will not proceed at this time" |
| National AI Plan, 2 December 2025 (<https://www.industry.gov.au/publications/national-ai-plan>, "Keep Australians safe" chapter) | P | Existing laws; AISI; no text-and-data-mining exception; ACL review |
| Australian AI Safety Institute | S (press) | Announced 25 November 2025; not a regulator |
| DTA, Policy for the responsible use of AI in government v2.0/v2.1 and implementation pages (<https://www.digital.gov.au/ai/ai-in-government-policy>) | P | Mandatory requirements and dates |
| DTA, Appendix C scope criteria (<https://www.digital.gov.au/ai/ai-in-government-policy/policy-responsible-use-ai-government-version-20-appendix-c-scope-ai-use-cases>) | P | When a use case is in scope |
| DTA, AI impact assessment tool, updated 1 December 2025 (<https://www.digital.gov.au/ai/impact-assessment-tool/introduction>) | P | 12 sections; threshold and full assessment |
| DTA, Standard for AI transparency statements v2.1, updated 20 October 2026 (<https://www.digital.gov.au/ai/ai-in-government-policy/standard-ai-transparency-statements>) | P | Statement contents |
| DTA, AI technical standard, updated 22 August 2025, and Agentic AI addendum, updated 4 June 2026 (<https://www.digital.gov.au/policy/ai/agentic-ai-addendum>) | P | AGT.1–AGT.8 |
| NSW AI Assessment Framework (<https://www.digital.nsw.gov.au/nsw-artificial-intelligence-assurance-framework>) | P | Mandatory platform from 30 September 2026 |
| Victoria Administrative Guideline 2024/07; Queensland FAIRA | S | Mention only |
| Criminal Code Amendment (Deepfake Sexual Material) Act 2024 | S | Mention only |
| AS ISO/IEC 42001:2023 adopted 16 February 2024 | S | Mention only |

### Other laws (fork C)

Several sites refused automated fetches with 403: aph.gov.au, accc.gov.au,
legislation.nsw.gov.au, austlii, oic.qld.gov.au and humanrights.gov.au.
The search budget also ran out. Items from those sources are S, or U
(unverified).

| Source | Status | Used for |
| --- | --- | --- |
| Treasury, Review of AI and the Australian Consumer Law, final report, 3 October 2025 (<https://treasury.gov.au/publication/p2025-702329>) | P, full text | ACL adequate; deployer liable for chatbot misstatements |
| Competition and Consumer Amendment (Unfair Trading Practices) Act 2026, No. 64, 2026 (<https://www.legislation.gov.au/C2026A00064/asmade>) | P | New ACL s 28B; commences 1 July 2027 |
| ASIC REP 798, 29 October 2024 (<https://asic.gov.au/regulatory-resources/find-a-document/reports/rep-798-beware-the-gap-governance-arrangements-in-the-face-of-ai-innovation/>) | P landing page; findings S | Licensee AI governance |
| ACCC AI snapshot; ASIC frontier-AI cyber letter, 8 May 2026 | S | Mention |
| NSW Workplace Surveillance Act 2005 (Judicial Commission bench book <https://www.judcom.nsw.gov.au/publications/benchbks/local/act-2005-47.html>) | P (bench book), Act text S | 14-day notice; covert surveillance offences |
| NSW Work Health and Safety Amendment (Digital Work Systems) Act 2026 (<https://www.safework.nsw.gov.au/legal-obligations/legislation/accordians/work-health-and-safety-amendment-digital-work-systems-act-2026-amendment-act>) | P | Assent 18 February 2026; main duties uncommenced |
| Victorian Parliament inquiry into workplace surveillance (<https://www.parliament.vic.gov.au/get-involved/inquiries/inquiryintoworkplacesurveillance/reports>) | P (report 13 May 2025, response 18 November 2025); bill S | Pending Victorian law |
| House Standing Committee, The Future of Work, 11 February 2025; ACT Workplace Privacy Act 2011 | S / U | Mention |
| Spam Act 2003 (<https://www.legislation.gov.au/C2004A01214/latest/downloads>) | P | s 5(5) voice calls excluded, including synthetic voice |
| Telecommunications (Telemarketing and Research Calls) Industry Standard 2017, F2017L00323 | P | Call hours; synthetic-voice rules ss 12–13 |
| Do Not Call Register industry overview (<https://www.donotcall.gov.au/industry/industry-overview>) | P | Registered numbers; liability of the business that causes the call |
| eSafety, social media age restrictions (<https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions>) and codes (<https://www.esafety.gov.au/industry/codes>) | P; chatbot code text S | Minimum age since 10 December 2025; age-restricted material codes |
| Attorney-General media release, 26 October 2025 (<https://ministers.ag.gov.au/node/1903>) | P | No text-and-data-mining exception |
| Cyber Security Act 2024, No. 98, 2024 (<https://www.legislation.gov.au/C2024A00098>) | P; threshold S | ss 26–27 ransomware payment reports, 72 hours |
| CISC, SOCI data storage or processing (<https://www.cisc.gov.au/information-for-your-industry/data-storage-and-processing/legislation-regulation-and-compliance/soci-act-2018>) | P; incident timings U | Business critical data |
| APRA CPS 234 (<https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf>); CPS 230 (<https://www.apra.gov.au/operational-risk-management>) | P | Notification clocks; material service providers |
| APRA media release on AI risk, 30 April 2026 (<https://www.apra.gov.au/news-and-publications/apra-calls-step-change-ai-related-risk-management-and-governance>) | P release; letter S | AI expectations under existing standards |
| My Health Records Act 2012, compilation of 1 July 2026 (<https://www.legislation.gov.au/C2012A00063/latest/downloads>) | P | s 77 no offshore holding or processing |
| Vic Health Records Act 2001 (<https://www.legislation.vic.gov.au/in-force/acts/health-records-act-2001>); NSW HRIPA (<https://www.ipc.nsw.gov.au/privacy/nsw-privacy-laws/hrip>) | P headers and landing pages; principle numbers U | State health privacy |
| TGA software and AI pages; digital scribe review outcome, 16 October 2026 (<https://www.tga.gov.au/news/news-articles/outcome-digital-scribe-review>) | P | Medical device screen |
| IPC NSW, Mandatory Notification of Data Breach scheme (<https://www.ipc.nsw.gov.au/privacy/MNDB-scheme>) | P; commencement date U | NSW agency breaches |
| OVIC, public and enterprise generative AI guidance, both updated 26 June 2026 (<https://ovic.vic.gov.au/privacy/resources-for-organisations/use-of-enterprise-generative-ai-tools-in-the-victorian-public-sector/>) | P | PIA per function; contractors bound |
| Queensland Information Privacy Act 2009 as amended by the IPOLA Act 2023 | S / U | QPPs; breach notification |

## 1. Privacy Act 1988 and the APPs

**(a) What and status.** The Act and its 13 Australian Privacy Principles
(Schedule 1) are in force. The current compilation, No. 104, is dated
4 June 2026 (P). The Act binds "APP entities": Australian Government
agencies, and organisations other than small business operators.

- **Small business exemption (s 6D).** Annual turnover of $3 million or
  less. It does not apply to: health service providers; businesses that
  trade in personal information; contracted service providers under a
  Commonwealth contract; credit reporting bodies; AML/CTF reporting
  entities for their AML/CTF activities; Consumer Data Right accredited
  businesses; businesses related to a covered business; prescribed
  businesses; and businesses that opt in. Source: OAIC small business page
  (P), which shows no 2026 change.
- **Employee records exemption (s 7B(3)) (P).** It applies to an
  employer's act or practice "directly related to" a current or former
  employment relationship and an employee record. The OAIC says it does
  not cover:
  - unsuccessful job applicants;
  - contractors and subcontractors handling another organisation's
    employee information;
  - recruitment, HR, medical, training or superannuation providers working
    under contract to an employer;
  - volunteers.
  Source: OAIC employee records page, December 2015 (P).
- **State contracts (s 7B(5)) (P).** An organisation acting as a
  contracted service provider under a State contract, to meet an
  obligation under that contract, is exempt from the Privacy Act for those
  acts. The State's own privacy law and the contract's clauses govern
  instead.
- **Commonwealth contracts (s 95B) (P).** An agency must put contract
  terms in place so the contracted service provider does not breach the
  APPs, and that duty flows down to subcontracts.

The APPs that bite on an agent (P, Privacy Act Schedule 1 and the two OAIC
AI guidance pages):

- **APP 1 (open and transparent management).**
  - APP 1.2: take reasonable steps to implement practices, procedures and
    systems that ensure compliance. The Tribunal upheld breaches of
    APP 1.2 and 1.3 against Bunnings (S), and the OAIC confirmed that the
    governance findings stand (P).
  - APP 1.4: the privacy policy must include, among other things, overseas
    disclosure and the countries involved where practicable.
  - APP 1.7 to 1.9 from 10 December 2026, checked 2026-10-26: see
    section 2.
- **APP 3 (collection).**
  - An organisation must collect personal information only where it is
    reasonably necessary for its functions or activities (3.2).
  - Sensitive information needs consent unless an exception applies (3.3).
  - The OAIC treats information an AI system generates or infers about a
    person as a collection: "If AI systems are used to generate or infer
    personal information, this is a collection" (commercial AI guidance, P).
  - Collection must be by lawful and fair means. The training guidance
    calls scraping "generally a covert method of collection" (P).
- **APP 5 (notice of collection).** The notice must cover the APP 5.2
  matters, including the purposes, usual recipients and whether
  information is likely to go overseas, with the countries if practicable
  (P, Act). The OAIC also recommends telling people when they are
  interacting with an AI system rather than a human (S, the OAIC page as
  summarised). Kmart breached APP 5.1 (S). Bunnings breached APP 5.1 (S)
  and its notification finding stands (P).
- **APP 6 (use and disclosure).**
  - Personal information may be used only for the primary purpose of
    collection, unless a 6.2 exception applies (for example, a related
    secondary purpose within reasonable expectations, or consent).
  - Entering personal information into an AI system may be a use or a
    disclosure.
  - The OAIC says secondary AI uses are hard to fit within reasonable
    expectations, and recommends consent or a meaningful opt-out (P).
  - Updating a privacy policy does not by itself change reasonable
    expectations (training guidance, P).
- **APP 8 and s 16C (cross-border disclosure).**
  - Before disclosing to an overseas recipient, an entity must take
    reasonable steps to ensure the recipient does not breach the APPs
    (8.1). An enforceable contract is generally expected (Chapter 8, para
    8.16, P).
  - Section 16C makes the disclosing entity liable for the overseas
    recipient's acts that would breach the APPs.
  - The exceptions are in 8.2: a substantially similar law with
    enforcement mechanisms, informed consent, required by law, and others.
    The new 8.3 allows regulations to prescribe countries or binding
    schemes, but none is prescribed in Privacy Regulation 2013, Compilation
    No. 20 (P).
  - **Use or disclosure.** Giving personal information to an overseas
    cloud provider is a "use" rather than a disclosure where the entity
    does not release the information from its "effective control". That
    needs a binding contract limiting handling to the stated purposes,
    the same obligations on any subcontractors, and effective control in
    the entity's hands. Security, retrieval and deletion are relevant
    considerations (Chapter 8, para 8.14, P).
  - Google's abuse monitoring can store flagged prompts that people may
    review (see the skill's model-provider section). Whether that, or
    support access from outside Australia, releases effective control is a
    question for counsel.
- **APP 10 (quality).** Take reasonable steps so personal information
  collected, used or disclosed is accurate, up to date, complete and
  relevant. The OAIC links this to testing, labelling outputs as
  probabilistic and taking particular care for high privacy risk uses (P).
- **APP 11 (security, retention, destruction).**
  - Take reasonable steps to protect information from misuse,
    interference, loss and unauthorised access, modification or disclosure
    (11.1).
  - Destroy or de-identify information that is no longer needed (11.2).
  - New 11.3 from 11 December 2024: "such steps include technical and
    organisational measures" (P, the 2024 Act).
- **APP 12 and 13 (access and correction).** Individuals can request
  access and correction. APP 13.5 (dealing with requests) is now an
  infringement-notice provision under s 13K. Memory stores, session
  history and evaluation sets are all "held" information that an access
  request reaches.

**(b) When it applies to an agent project.**
- The client is an APP entity: an agency, an organisation with turnover
  above $3 million, or a small business within an exception, such as a
  health service provider.
- The consultancy is an APP entity when its own turnover is above
  $3 million, or it is a contracted service provider under a Commonwealth
  contract.
- The data the agent handles, stores, logs, remembers or infers includes
  personal information about customers, users or employees.
- Overseas: the model endpoint, logs, grounding, sub-processors or
  support access sit outside Australia.
- Sensitive information can appear: health, biometric, racial or ethnic
  origin, sexual orientation, criminal record, union membership. Free text
  makes this likely.
- An agency handling employee data: the employee records exemption does
  not apply to agencies. That is a reading of s 7B, which covers
  organisations only; the OAIC page covers private employers only.
  Counsel to confirm.

**(c) Paperwork and facts.**
- **PIA input pack.**
  - Threshold assessment.
  - Information flows: one per path, including prompts, tool calls,
    memory, logs, evaluation sets and backups.
  - APP-by-APP compliance check.
  - Overseas recipients, with the use-or-disclosure facts (contract terms,
    effective control, region, endpoint).
  - Sensitive information, with the consent or exception for each kind.
  - Secondary uses, including any fine-tuning or evaluation on production
    data.
  - Retention and destruction.
  - How access and correction requests reach memory and logs.
- **Personal information inventory and notice inputs.** These replace the
  records of processing.
  - Rows: kinds of personal information, purpose, source (collected from
    the person, a third party, or generated or inferred), usual
    recipients, overseas countries, retention.
  - Proposed APP 5 notice text and privacy-policy additions.
- **Security questionnaire.**
  - APP 11 technical and organisational measures.
  - NDB readiness: the 30-day assessment and notifying the OAIC as soon as
    practicable.
- **Classification memo, roles section.**
  - Whether the client and the consultancy are each APP entities.
  - Whether the small business, employee records or State contract
    exemptions apply.

**(d) Counsel questions.**
- Is the consultancy an APP entity for this engagement? Do any exemptions
  apply (small business, employee records, State contract)?
- Is sending prompts to the model endpoint a use or a disclosure under
  APP 8? Does s 16C exposure arise? Is the Google Cloud contract enough
  for "reasonable steps"?
- Is the agent's use of existing customer or employee data a related
  secondary purpose within reasonable expectations (APP 6.2(a)), or does
  it need consent?
- Is any sensitive information collected, including inferred or derived
  sensitive information, and on what APP 3.3 basis?

## 2. Automated-decision transparency (APP 1.7 to 1.9)

**(a) What and status.** Inserted by Schedule 1 Part 15 of the Privacy and
Other Legislation Amendment Act 2024 (assent 10 December 2024). It
commences "the day after the end of the period of 24 months beginning on
the day this Act receives the Royal Assent", which is 10 December 2026,
checked 2026-10-26 (P, commencement table item 7). It applies to decisions
made after commencement, whenever the program was arranged or the data was
collected (item 89, P). APP 1.7 is a civil penalty provision under
s 13K(1)(b)(iia), with a maximum of 200 penalty units, and infringement
notices are available (P).

Exact text of APP 1.7 (P):

> 1.7 Without limiting subclause 1.3, the APP privacy policy of an APP
> entity must contain the information covered by subclause 1.8 if:
> (a) the entity has arranged for a computer program to make, or do a
> thing that is substantially and directly related to making, a
> decision; and
> (b) the decision could reasonably be expected to significantly affect
> the rights or interests of an individual; and
> (c) personal information about the individual is used in the operation
> of the computer program to make the decision or do the thing that is
> substantially and directly related to making the decision.

APP 1.8 requires the policy to state:
- the kinds of personal information used;
- the kinds of decisions made solely by the program;
- the kinds of decisions for which the program does a thing substantially
  and directly related to making them.

APP 1.9 says three things:
- Deciding includes refusing or failing to decide.
- Effects can be adverse or beneficial.
- Examples of decisions affecting rights or interests are benefit grants
  under an Act, decisions affecting rights under a contract, and access to
  "a significant service or support".

OAIC fact sheet, September 2026 (P):
- **"Computer program"** includes rule-based processes, AI and machine
  learning, and "generative AI used to generate text, images, videos, code
  or synthesis, including chatbots".
- **"Substantially"** means "a key factor in facilitating the human's
  decision making". **"Directly"** means "a direct connection with making
  the decision".
- **Human review is not an exemption.** A decision may be in scope "even
  where a computer program output does not replace the entire
  decision-making process or is subject to human review". Machine learning
  or generative AI outputs used in significant decisions "would generally
  fall within scope ... unless subject to extensive human oversight and
  control".
- **"Arranged for"** includes procuring a third-party program,
  configuring off-the-shelf software and "reliance on advisory outputs".
- **"Significantly"** means "more than trivial" with "potential to
  considerably influence" the person's circumstances. Vulnerability raises
  the impact.
- **In-scope examples (Note 1):**
  - facial recognition watchlists;
  - recruitment software that sorts candidates;
  - personalised pricing of significant goods;
  - prioritising health or disability services;
  - government benefit or housing eligibility;
  - education admission;
  - loan or credit approval;
  - programmatic advertising for significant goods;
  - insurance eligibility;
  - "reports created by artificial intelligence used to rank employee
    performance, determine promotions, or decide bonus/remuneration
    outcomes";
  - scholarships and grants;
  - immigration and border processing.
- **Responsibility.** The duty "typically remain[s] with the APP entity"
  making the decision. "Providers of third-party software or enterprise
  solutions ... should provide clear, high-level information about how
  their software can be used to make decisions".
- **Carve-out.** Commercially sensitive information and trade secrets are
  excluded. Embarrassment is not a ground.
- **When in doubt,** the fact sheet tells entities to "take a cautious
  approach" and disclose.

The OAIC released the fact sheet, an agency supplement, a flowchart and an
updated APP 1 Guideline on 30 September 2026 (P).

**(b) When it applies.**
- The client is an APP entity.
- The agent, a tool it calls, or a score it produces feeds a decision
  about a person, including a refusal or a failure to act.
- The decision touches a contract right, a benefit, a significant service,
  employment (performance, promotion, pay, hiring), credit, insurance,
  health or education.
- Personal information about that person is used.

**(c) Paperwork and facts.**
- **Classification memo.** A new "Automated decisions (APP 1.7)" section.
  For each decision the agent touches, record:
  - what the agent does;
  - whether it decides solely or does a substantially and directly related
    thing;
  - the human review step, with its contract ID and the M record of the
    share of outputs reviewed;
  - the effect on the person;
  - the personal information used.
- **System card.** A new "Privacy policy inputs (APP 1.8)" block listing
  the three kinds of information above in plain language. This is the
  vendor information the OAIC expects.
- **Inventory document.** Proposed privacy-policy wording.

**(d) Counsel questions.**
- Does the decision "significantly affect" rights or interests?
- Is the review "extensive human oversight and control"?
- Can any part be withheld as commercial-in-confidence?
- Does the client's current privacy policy need amending before
  10 December 2026?

## 3. Statutory tort for serious invasions of privacy

**(a) What and status.** Schedule 2 of the 2024 Act inserted Schedule 2 of
the Privacy Act. It commenced on 10 June 2025, checked 2026-10-26: the
default date six months after assent (P, commencement table item 8).

A plaintiff must show (cl 7, P):
- an invasion of privacy, either by intruding upon seclusion or by misusing
  information (misuse includes collecting, using or disclosing it);
- a reasonable expectation of privacy;
- that the invasion was intentional or reckless;
- that it was serious;
- that the public interest in privacy outweighed any countervailing public
  interest.

Exemptions cover intelligence and enforcement bodies, people under 18 and
journalists in some circumstances (P, simplified outline). The listed
exemptions do not include small businesses or employee records. That is
my reading of the outline; counsel to confirm.

**(b) When it applies.** The agent intrudes or misuses information
intentionally or recklessly. Examples: covert monitoring of staff or
users, publishing or exposing personal information, or deliberately
re-identifying people. Negligence is not enough. It reaches people and
businesses the APPs do not.

**(c) Paperwork.** PIA risk register: a line on intentional or reckless
intrusion or misuse scenarios, and the controls against them. Impact
assessment: harms to individuals.

**(d) Counsel.** Could any designed behaviour (monitoring, profiling,
disclosure) be "reckless"? Does the consultancy carry exposure as the
builder?

## 4. Children's Online Privacy Code

**(a) What and status.** The Commissioner must develop and register a code
within 24 months of assent, that is by 10 December 2026, checked
2026-10-26 (s 26GC(10), P). The exposure draft and explanatory statement
are published. Phase 3 consultation ran from 31 March to 5 June 2026. The
code is not yet registered (OAIC page, P). In the Act, "child" means
under 18.

**(b) When it applies.** The client provides a social media service, a
relevant electronic service or a designated internet service (Online
Safety Act definitions) that is "likely to be accessed by children" and is
not a health service. Other entities can be named in the code
(s 26GC(5), P). A public-facing chat agent offered to consumers may be a
relevant electronic service; counsel decides.

**(c) Paperwork.** The PIA records whether children are likely users and
any age assurance. The memo carries a "pending code" line until the code
is registered.

**(d) Counsel.** Is the service in a covered class and "likely to be
accessed by children"? What commencement or transition will the final
code set?

## 5. OAIC powers and penalties

**(a) What and status.** Mostly from 11 December 2024 (P, commencement
table):

| Provision | Who | Maximum |
| --- | --- | --- |
| s 13G, serious interference with privacy | Body corporate | Greatest of $50,000,000; 3 times the benefit; or 30% of adjusted turnover in the breach turnover period |
| s 13G | Other persons | $2,500,000 |
| s 13H, interference without the "serious" element | Any | 2,000 penalty units |
| s 13K, specified APP breaches | Any | 200 penalty units |

- **s 13G seriousness factors** include sensitivity, consequences, the
  number of people affected, children or vulnerable people, repetition,
  and a failure to implement privacy practices.
- **s 13K covers** APP 1.3, 1.4, 1.7 from 10 December 2026, 2.1, 6.5,
  7.2(c), 7.3(c) and (d), 7.7, 13.5, and a non-compliant breach statement.
  Infringement notices and compliance notices are available.
- **New OAIC powers:**
  - public inquiries (Part 10);
  - determinations requiring specific steps (Part 11);
  - Regulatory Powers Act monitoring and investigation (Part 14);
  - Federal Court orders (Part 9);
  - eligible data breach declarations by the Minister (s 26X).
- **Penalty unit.** $364 for conduct from 1 July 2026 (S, ASIC table);
  $330 before.
- **Enforcement record.** The first civil penalties were $5.8 million
  against Australian Clinical Labs on 8 October 2025: $4.2 million for
  APP 11.1, $800,000 for a failed s 26WH assessment and $800,000 for late
  notification under s 26WK (P, OAIC release of 9 October 2025).

**(b) When it applies.** Any APP entity.

**(c) Paperwork.** None directly. The memo cites the penalty regime once,
so reviewers see the exposure.

**(d) Counsel.** Exposure assessment.

## 6. Notifiable Data Breaches scheme

**(a) What and status.** Part IIIC of the Privacy Act, in force since
22 February 2018.
- An eligible data breach is unauthorised access, unauthorised disclosure
  or loss that is likely to result in serious harm, where remedial action
  has not removed that likelihood.
- On reasonable grounds to suspect one, the entity must carry out a
  "reasonable and expeditious assessment" and take all reasonable steps to
  complete it "within 30 days" (s 26WH, P).
- On reasonable grounds to believe one occurred, it must give the
  Commissioner a statement "as soon as practicable" (s 26WK, P) and notify
  the affected individuals (s 26WL).
- Where several entities hold the information (client, consultancy, cloud
  provider), one entity's compliant assessment and notification covers the
  others (s 26WJ for the assessment and s 26WM for notification, P).
- The Minister may make an eligible data breach declaration to permit
  information sharing (s 26X, from 11 December 2024, P).

**(b) When it applies.** Any APP entity holding personal information in
the agent's stores, logs, memory or evaluation sets. Agent-specific breach
paths:
- prompt injection that exfiltrates data;
- a cross-user session or memory leak;
- logs sent to the wrong sink;
- data disclosed to a model provider outside the contract.

**(c) Paperwork.**
- Questionnaire: an incident-notification topic giving the 30-day
  assessment, who notifies, and the contractual flow-down between client
  and consultancy.
- PIA: the breach-response measure.
- Plan: the I-record links.

**(d) Counsel.** Which entity notifies, and what does the services
contract say about notice from the consultancy to the client?

## 7. Tranche 2: Privacy Amendment (Personal Data Protection) Bill 2026

**(a) What and status.** Exposure draft and consultation paper published by
the Attorney-General's Department. The consultation opened on 31 August
2026 and closed on 18 September 2026. "The Bill remains subject to further
consideration by government" (P, AGD page). I found no introduction to
Parliament (S, search). The draft's commencement table is blank (P). Not
law.

Contents relevant to agents (P, consultation paper):
- **Fair and reasonable test.** A single "fair and reasonable" test for
  collection, use and disclosure, with legislated factors, including
  children's interests.
- **Collection.** "Collects" covers information "generated or derived
  through means such as data analysis, artificial intelligence". The paper
  says this means "inferences drawn by AI-enabled technology about an
  individual would be considered collection".
- **Sensitive information.** Expanded, adding biometric templates and
  "precise geolocation tracking data" (draft s 6FE, P). There are rules on
  when derived sensitive information is collected.
- **Disclosure.** A definition based on making information accessible.
  "The mere transmission or storage of personal information, including
  overseas, will not constitute a disclosure unless the information is made
  accessible to another person or body." That matters for APP 8 and model
  endpoints.
- **Controllers and processors (Schedule 6).** A processor acting on a
  controller's "documented instructions" would be exempt from all APPs
  except APP 1 and APP 11. Commonwealth contracted service providers are
  excluded from the processor definition.
- **APP 11.** Strengthened: identify the personal information held,
  consider destruction before de-identification, and regularly assess
  effectiveness.
- **Other measures.** A right to erasure against large digital platforms;
  direct marketing that includes group-level targeting; NDB changes.

Not in the draft: I found no removal of the small business exemption or
the employee records exemption in either document (P, text searched). One
draft amendment touches s 6D(8) on trading. The exposure draft does not
deal with ADM beyond APP 1.7, which is already enacted.

**(b) When it applies.** Not yet. Screen for it as "pending".

**(c) Paperwork.** One line in the memo and the PIA: "Tranche 2 exposure
draft of 31 August 2026 not enacted, checked 2026-10-26". In practice,
designing to the fair and reasonable test and the processor instructions
model now is cheap. Recommend documented client instructions to the
consultancy in the statement of work.

**(d) Counsel.** Whether to design to the draft. Whether the consultancy
would be a processor under it.

## 8. OAIC AI guidance and determinations

**Commercially available AI products, 21 October 2024 (P).** For
deployers, including organisations using third-party models inside their
own products.
- Privacy duties apply to inputs and outputs.
- Generated or inferred personal information is collected.
- Update privacy policies and notices.
- Do not put personal or sensitive information into publicly available
  generative AI tools.
- Do due diligence ("not ... set and forget"), privacy by design and a
  PIA.
- Consider server location under APP 8.
- Label outputs as probabilistic under APP 10.
- Keep human oversight.

**Developing and training generative AI models, 21 October 2024 (P).**
Covers fine-tuning.
- Public availability does not make data usable.
- Scraping is generally covert collection.
- Secondary use of data the entity already holds needs reasonable
  expectations or consent, or "a meaningful and informed ability to
  opt-out".
- Delete sensitive information where there is no consent or exception.
- A privacy policy alone does not meet APP 5.
- RAG is not addressed by name (S, my reading of the first 100,000
  characters).

I found no later revision and no OAIC guidance on agentic AI (search,
26 October 2026).

**Determinations and decisions:**

| Matter | Outcome | Lesson for agents |
| --- | --- | --- |
| Clearview AI, 14 October 2021 | Breaches, including sensitive information collected without consent; the determination stands; no further action (statement of 21 August 2024, P) | Scraping images for biometric matching is unlawful collection |
| Bunnings [2024] AICmr 230, 19 November 2024 → ART [2026] ARTA 130, 4 February 2026 | Tribunal accepted FRT for "the limited purpose of combatting very significant retail crime" but left the notice and governance findings standing; Commissioner did not appeal (statement of 5 March 2026, P). Permitted general situation and APP 1.2/1.3/5.1 detail (S) | Proportionality analysis and APP 1/APP 5 paperwork are where cases are lost |
| Kmart [2025] AICmr 155, 26 August 2025 | Breaches of APP 3.3 and 5.1 (S); under ART review, hearings early 2027 (P, OAIC 29 July 2026) | Biometric matching of everyone to catch a few is disproportionate |
| I-MED, 31 July 2025 | No further action: disclosed data was adequately de-identified (P) | Before sharing data with an AI developer: de-identify, test the samples, sign contracts barring re-identification, keep separate environments, treat it as high privacy risk |
| Australian Clinical Labs [2025] FCA 1224 | $5.8m (P) | Security and breach-assessment timing are penalised |

OAIC regulatory priorities 2025–26 include "practices that erode
information access and privacy rights in the application of artificial
intelligence", facial recognition and biometrics, ad tech and excessive
collection (P, 29 July 2025).

**Paperwork mapping.**
- PIA: cite both AI guidance pages. Use the commercial AI products
  checklist questions in the threshold and analysis steps.
- System card "Limits": APP 10 labelling.
- Any fine-tuning or evaluation on production data: a secondary-use
  analysis with consent or opt-out.
- Biometric features: force counsel and a proportionality section.

## 9. Privacy Impact Assessment as the Australian DPIA

**(a) What and status.**
- **Agencies.** The Privacy (Australian Government Agencies — Governance)
  APP Code 2017 (F2017L01396), in force since 1 July 2018:
  - "An agency must conduct a PIA for all high privacy risk projects"
    (s 12(1), P).
  - A project may be high privacy risk where it "involves any new or
    changed ways of handling personal information that are likely to have
    a significant impact on the privacy of individuals" (s 12(2)).
  - Agencies must keep and publish a register of PIAs (s 15).
  - The Commissioner can direct an agency to conduct a PIA (s 33D of the
    Act).
- **Private sector.** PIAs are recommended, not required. The guide says
  "The OAIC encourages organisations to undertake PIAs" (P).
- **The OAIC's suggested ten steps (P, 2 September 2021):**
  1. threshold assessment;
  2. plan;
  3. describe the project;
  4. identify and consult stakeholders;
  5. map information flows;
  6. privacy impact analysis and compliance check;
  7. privacy management (addressing risks);
  8. recommendations;
  9. report;
  10. respond and review.

**(b) When.**
- **Required:** the client is an Australian Government agency and the
  project is high privacy risk. An agent handling personal information in
  a new way almost always is.
- **Recommended:** any APP entity. The OAIC's AI guidance recommends one
  for AI.
- **State agencies:** see the state privacy laws section.

**(c) Paperwork.** Rename the DPIA input pack the **PIA input pack** for
Australian projects and reorder it to the ten steps:
- threshold;
- description;
- stakeholders;
- information flows;
- APP-by-APP analysis (APP 1, 3, 5, 6, 8, 10, 11, 12, 13);
- risks and measures;
- recommendations;
- questions for counsel.

Drop the "Legal basis" section (there is no Article 6 equivalent).
Replace it with the APP 3, 3.3 and 6 analysis. Replace the WP248 screening
with the OAIC threshold assessment. For agencies, add the PIA register
entry and the s 12 high-privacy-risk conclusion as a `counsel:` item.

**(d) Counsel.** Is the project high privacy risk (agency)? Will the PIA be
published?

## 10. Government AI policy

### 10.1 Voluntary AI Safety Standard and Guidance for AI Adoption

**(a)**
- **The Voluntary AI Safety Standard** has 10 guardrails, published
  5 September 2024 and updated 2 December 2025 (P).
- **The Guidance for AI Adoption** ("AI6") was published by the National
  AI Centre on 21 October 2025, in Foundations and Implementation versions
  (P). It "evolves" the Standard.
- Both are voluntary.
- **The six practices:**
  1. decide who is accountable;
  2. understand impacts and plan accordingly;
  3. measure and manage risks;
  4. share essential information;
  5. test and monitor;
  6. maintain human control.
  Practices 1 to 3 are P. The names of practices 4 to 6 are S.
- **Implementation clauses useful to the pack (P):**
  - 1.2: accountability across the supply chain, naming model developer,
    system developer and deployer;
  - 2.1.4: scope, intended use, foreseeable misuse, limits;
  - 2.1.5: stakeholder impacts, including vulnerable groups and use of
    personal information;
  - 2.2: contestability and redress;
  - 3.1.1: an AI impact assessment process and risk tolerance;
  - 3.1.3: "data sheets, model cards, or system cards".
- **NAIC templates (P), published 22 April 2026:**
  - an AI policy template;
  - an AI register template;
  - questions to ask suppliers.

**(b) When.** Any private client. It is the reference baseline boards and
counsel cite.

**(c) Paperwork.**
- **Impact assessment.** Add an "AI6 mapping" table beside the NIST one.
- **Classification memo, roles.** Supply-chain roles in the clause 1.2
  terms (the consultancy as system developer, Google as model developer,
  the client as deployer).
- **AI register row.** A row in the NAIC template shape.
- **System card.** Meets 3.1.3. Add contestability (2.2) to Human
  oversight.

**(d) Counsel.** Has the client adopted AI6 or ISO/IEC 42001 (AS ISO/IEC
42001:2023, adopted by Standards Australia on 16 February 2024, S), or
contracted to either?

### 10.2 Mandatory guardrails, National AI Plan, AI Safety Institute

**(a)**
- **Proposals paper.** Consultation ran from 5 September to 4 October
  2024. The consultation page now says: "The government will not proceed
  at this time with the proposals to introduce mandatory guardrails for AI
  development and deployment. Feedback on the paper informed the National
  AI Plan" (P).
- **What the paper proposed (S):**
  - principles for designating high risk (human rights, health and safety,
    legal effects, groups, society);
  - general-purpose AI treated as high risk;
  - ten mandatory guardrails;
  - three legislative options.
- **The National AI Plan, 2 December 2025 (P):**
  - "established laws remain the foundation for addressing and mitigating
    AI-related risks";
  - regulators act in their own domains;
  - "targeted laws where needed";
  - the Treasury review found the ACL applies, with minor clarifications to
    come;
  - a text-and-data-mining copyright exception is ruled out;
  - reviews of AI in health care and of TGA software regulation.
  The Plan does not use the words "AI Act", "guardrails" or "high-risk"
  (P, fork's reading). The view that Australia chose not to legislate a
  standalone AI Act comes from the consultation notice and press (S).
- **Australian AI Safety Institute (S).** Announced 25 November 2025 with
  $29.9m and operating from early 2026 inside the Department of Industry.
  The Plan describes it as monitoring, testing and sharing information,
  and advising regulators. It is not a regulator (P).

**(b) When.** No direct obligations.

**(c) Paperwork.** One sentence in the Australian memo: no AI-specific
classification regime; obligations come from the laws screened below,
checked 2026-10-26.

**(d) Counsel.** None.

### 10.3 DTA Policy for the responsible use of AI in government (Commonwealth clients)

**(a) Status (P).**
- **Versions.** v2.0 effective 15 December 2025, replacing v1.1 (effective
  1 September 2024). v2.1 published 21 October 2026.
- **Who.** Mandatory for non-corporate Commonwealth entities. Corporate
  entities are encouraged. Defence and the intelligence community are
  excluded.
- **Requirements:**
  - accountable officials;
  - a strategic position on AI within 6 months;
  - an accountable owner for each in-scope use case, an internal use-case
    register shared with the DTA every 6 months, a process for responsible
    AI use with incident and concern reporting, and mandatory staff
    training, each within 12 months;
  - one AI transparency statement per agency, a requirement since
    28 February 2025, with minimum contents under Standard v2.1 (updated
    20 October 2026), refreshed at least yearly or on significant change.
- **AI impact assessment.** Agencies "are required to implement the AI
  impact assessment requirement for in-scope use cases by 15 December
  2026", checked 2026-10-26. Existing use cases are due by 30 April 2027.
  The assessment starts at design and must be complete, with treatments
  applied, before deployment. High inherent risk means board or SES
  governance, reporting to the DTA and review at least every 12 months.
- **The DTA tool (updated 1 December 2025):**
  - Sections 1 to 4 are a threshold assessment. Sections 5 to 12 are the
    full assessment, required if any risk is medium or high.
  - Topics: fairness, reliability and safety, privacy and security,
    transparency and explainability, contestability, accountability,
    human-centred values.
  - Each assessment has an assessing officer and an approving officer.
- **Strongly recommended, not mandatory:** the AI technical standard
  (42 statements, updated 22 August 2025) and the **Agentic AI addendum**
  (AGT.1 to AGT.8, updated 4 June 2026). The addendum covers memory
  scope, retention and deletion, bounded workflows and approvals, typed
  tools and access control, adversarial evaluation, monitoring, kill
  switches and decommissioning.

**(b) When it applies.** The client is a non-corporate Commonwealth entity
(or a corporate one that opts in), outside the carve-outs. Appendix C puts
a use case in scope on any one of:
- more than insignificant harm;
- material influence on administrative decisions;
- public interaction, or significant effect on the public, without human
  review;
- use of personal, sensitive or security-classified data;
- DTA designation.
An ADK agent touching personal data is almost always in scope (P).

**(c) Paperwork.** New document: the **DTA AI impact assessment input
pack**. It follows the tool's 12 sections, threshold first and then full.
It also carries:
- the use-case owner;
- the register fields;
- the agency transparency statement inputs (the Appendix D usage pattern
  and domain, public interaction without human review, monitoring);
- an AGT.1 to AGT.8 conformance table, cross-referenced from the
  questionnaire.
Plus the PIA under the Agencies Privacy Code.

**(d) Counsel and client.**
- Is the use case in scope under Appendix C?
- What is the inherent risk rating?
- Who are the assessing and approving officers?
- Will the agency use the DTA tool or its own equivalent?
- Who owns intellectual property in inputs and outputs?

### 10.4 State government AI frameworks (mention)

- **NSW (P).** Agencies must apply the AI Assessment Framework. The
  online platform has been mandatory for registering and assessing use
  cases since 30 September 2026, checked 2026-10-26. High or critical risk
  cases go to the AI Review Committee. NSW's own example is a public-facing
  government chatbot rated high risk, which triggers a PIA, cyber and legal
  review, and accessibility checks.
- **Victoria (S).** Administrative Guideline 2024/07 on generative AI.
  OVIC resources on enterprise generative AI, 26 June 2026.
- **Queensland (S).** FAIRA v1.0.0, and FAIRA LITE from August 2026.

For a state agency client, fill in the state framework's fields beside the
state PIA.

## 11. Other laws an agent can breach

These are read by fork C. The source marks follow the table above.

### 11.1 Australian Consumer Law

**(a)**
- **Misleading conduct.** ACL s 18 (misleading or deceptive conduct) and
  s 29 (false representations) are in force and technology-neutral.
- **Treasury final report (3 October 2025, P).** The ACL is "generally
  well adapted" to AI, and the ACCC needs no new powers. A business that
  deploys a third-party chatbot "would be liable for the misleading
  conduct" to its customers, with a remedy against its supplier under the
  consumer guarantees.
- **Unfair trading practices.** The Competition and Consumer Amendment
  (Unfair Trading Practices) Act 2026 received assent on 6 July 2026 and
  commences on 1 July 2027, checked 2026-10-26 (P).
  - New s 28B prohibits conduct that "manipulate[s] the consumer" or
    "unreasonably distort[s] the environment" of the consumer's decision,
    causing detriment.
  - Examples include obstruction or pressure "including by using design
    elements in digital interfaces".
  - It protects individual consumers only.
  - The same Act adds drip pricing (s 48A) and subscription rules.
- **ACCC and ASIC.** No ACCC chatbot enforcement case found (S). ASIC
  REP 798, 29 October 2024, reviewed 624 AI use cases at 23 licensees (S
  for findings).

**(b) When.**
- Consumer-facing agents: sales, support, refunds, guarantees, product
  recommendations, price comparison.
- Claims about the agent itself, such as "unbiased" or "human-checked".
- Retention, upsell or cancellation flows (s 28B from 1 July 2027).

**(c) Paperwork.**
- **System card.** Capability claims, substantiated by M records, and
  disclosure that the user is talking to an AI.
- **Impact assessment.** A new "Consumer claims and choice-architecture
  review" section covering refund and guarantee answers and persuasion
  flows.
- **Classification memo.** The liability chain (client, consultancy,
  Google).

**(d) Counsel.**
- Do statements about refunds and guarantees comply?
- Could a retention flow breach s 28B?
- Can the AI claims be substantiated?
- Is liability allocated in the services agreement?

### 11.2 Anti-discrimination

**(a)** The federal Acts are the Racial Discrimination Act 1975, the Sex
Discrimination Act 1984, the Disability Discrimination Act 1992 and the
Age Discrimination Act 2004. State Acts also apply, and so do Fair Work
Act s 351 general protections (U; the AHRC site returned 403). They
cover direct and indirect discrimination in employment and in goods and
services. There is no algorithm carve-out.

**(b) When.** The agent screens, ranks or decides about people
(recruitment, rostering, credit, insurance, tenancy, eligibility), or uses
proxies for protected attributes.

**(c) Paperwork.** Impact assessment: bias measurement (M records),
removed proxies, human review. Memo: a counsel flag.

**(d) Counsel.** Do measured disparities amount to indirect
discrimination, and is the condition reasonable?

### 11.3 Workplace surveillance and AI at work

**(a)**
- **NSW Workplace Surveillance Act 2005 (S for Act text, P bench book).**
  - Written notice at least 14 days before computer, camera or tracking
    surveillance starts, stating its kind, method, start date and
    duration.
  - Computer surveillance must follow a notified policy.
  - Surveillance without proper notice is covert and needs a magistrate's
    authority (s 19 offence).
  - Blocking email or web access other than under policy is restricted
    (s 17).
- **ACT Workplace Privacy Act 2011.** A similar notice regime (U).
- **NSW Work Health and Safety Amendment (Digital Work Systems) Act 2026**
  received assent on 18 February 2026.
  - New duties: workers must not be put at risk by "digital work systems"
    (algorithms, AI, automation), and work allocation by such systems must
    be safe.
  - Union inspection power over digital work systems.
  - The main provisions await proclamation after guidelines (P). Not in
    force, checked 2026-10-26.
- **Victoria.** The inquiry reported on 13 May 2025, and the government
  responded on 18 November 2025 (P). A bill covering notice, biometrics and
  human oversight of AI decisions was announced in July 2026 (S). No bill
  was found.
- **Federal.** The House committee report "The Future of Work"
  (11 February 2025) recommends treating employment AI as high risk (S).
  No government response was found.

**(b) When.**
- The client is an employer and the agent handles staff data.
- Agent logs or telemetry record staff computer use, including staff
  prompts.
- The agent allocates work.
- Staff are in NSW, the ACT or Victoria.

**(c) Paperwork.**
- A new **workplace surveillance check**: states of employment, whether
  agent logging is "computer surveillance", the notice as a calendar wait
  `W` (at least 14 days in NSW), and the policy reference.
- PIA: employees, the employee records exemption reach, and job applicants
  (not exempt).
- Impact assessment: work-health-and-safety and work-allocation risk once
  the NSW duties commence.

**(d) Counsel.**
- Is prompt logging computer surveillance?
- Does the existing policy cover it?
- Do consultation clauses in enterprise agreements apply?

### 11.4 Spam Act, Do Not Call Register, Telemarketing Standard

**(a)**
- **Spam Act 2003 (P).** Covers commercial electronic messages: email,
  SMS, MMS, instant messages. The rules are consent, sender
  identification, and a functional unsubscribe honoured within 5 working
  days (S).
  - Section 5(5) excludes voice calls over a standard telephone service.
  - "Voice call" includes "a call that involves a recorded or synthetic
    voice".
  - So AI voice calls fall outside the Spam Act and under the
    telemarketing regime instead.
- **Telecommunications (Telemarketing and Research Calls) Industry
  Standard 2017 (P).**
  - Call hours: weekdays 9 am to 8 pm, Saturdays 9 am to 5 pm. No Sundays
    or national public holidays.
  - Synthetic-voice calls must provide a way during the call to get the
    caller's information (s 12).
  - End the call immediately on request (s 13).
  - Possible sunset around 1 April 2027 (U).
- **Do Not Call Register Act 2006 (P, donotcall.gov.au).** No telemarketing
  to registered numbers without consent. The business that causes the call
  is liable as well as the caller, including for overseas calls.

**(b) When.** Outbound marketing by email, SMS or chat; outbound voice
agents; transactional messages with promotional content.

**(c) Paperwork.** A new **outbound channel** section in the system card
and questionnaire, recording:
- where consent came from;
- evidence of washing lists against the register;
- call-hours enforcement in code (C ID);
- the synthetic-voice information mechanism;
- unsubscribe handling.

**(d) Counsel.** Is the message commercial? Does inferred consent hold?
Does an exemption apply?

### 11.5 Online Safety Act and the social media minimum age

**(a)**
- **Minimum age.** The social media minimum age has applied since
  10 December 2025, checked 2026-10-26 (P). It applies to services whose
  sole or a significant purpose is social interaction. Messaging and
  gaming are excluded.
- **Age-restricted material codes (P):**
  - three in effect from 27 December 2025 (hosting, carriage, search);
  - six from 9 March 2026, including relevant electronic services and
    designated internet services.
- **Chatbots.** eSafety's fact sheet says the codes reach "AI companions
  and chatbots" that can produce sexual, high-impact violence or self-harm
  material, which need age assurance (S).
- **Children's Code link.** Children's Online Privacy Code scope uses the
  same service categories (section 4).

**(b) When.** A public-facing generative chatbot that Australians can
reach. Internal enterprise agents are usually out of scope.

**(c) Paperwork.**
- Memo: an "Online safety scope" line (service category, what content it
  can produce, age assurance decision).
- System card: out-of-scope uses.

**(d) Counsel.** Which code or standard covers the service, if any?

### 11.6 Copyright

**(a)** "The government is not considering a Text and Data Mining
Exception" (Attorney-General, 26 October 2025, P). The Copyright and AI
Reference Group is looking at paid collective licensing, copyright in AI
outputs and a small-claims forum. An April 2026 response reaffirmed this;
no bill (S). The National AI Plan repeats the position (P).

**(b) When.** Fine-tuning, retrieval corpora built from third-party
content, published outputs.

**(c) Paperwork.** Impact assessment: the intellectual property row and a
content-source and licence register.

**(d) Counsel.** Are there licences for the corpus? Who owns the outputs?

### 11.7 Cyber Security Act 2024 and SOCI Act 2018

**(a)**
- **Cyber Security Act 2024 ransomware reports.** A business must report a
  ransomware payment "within 72 hours of making the ransomware payment or
  becoming aware" of it (ss 26–27, P). Reporting applies from 30 May 2025,
  checked 2026-10-26: the commencement fallback date (P), which matches
  secondary reports. The turnover threshold of more than $3 million is in
  the rules (S). SOCI responsible entities must report regardless of
  turnover.
- **SOCI data storage or processing.** A data storage or processing asset
  is critical when it is used mainly for a commercial data service to
  government or to a responsible entity, relating to "business critical
  data" (P, CISC). Responsible entities must tell their data provider.
- **SOCI duties.** Register, report cyber incidents (12 or 72 hours, U),
  and run a risk management program.

**(b) When.**
- Client turnover above $3 million (ransomware reporting).
- The client is a SOCI responsible entity, or the agent holds business
  critical data for one.
- A government client.

**(c) Paperwork.** Questionnaire incident-notification topic: who reports
within 72 hours. Records: whether the client has notified the consultancy
or Google as a data provider.

**(d) Counsel.** Is the consultancy or the hosting a data storage or
processing provider for a critical asset?

### 11.8 APRA and ASIC for financial clients

**(a)**
- **CPS 234 (P).**
  - Assess third parties' information security capability (para 16).
  - Notify APRA within 72 hours of a material information security
    incident (para 35).
  - Notify within 10 business days of a material control weakness
    (para 36).
- **CPS 230 (P).** Commenced 1 July 2025, checked 2026-10-26. Amendments
  of 30 April 2026 commence 1 July 2026.
  - Notify within 72 hours of a material operational risk incident
    (para 32).
  - Notify within 24 hours of a critical-operation disruption outside
    tolerance (para 41).
  - Keep a register of material service providers (para 48). "Core
    technology services" are presumed material (para 49(d)).
  - Notify within 20 business days of entering or materially changing an
    agreement for a critical operation, and before material offshoring
    (para 60).
- **APRA on AI, 30 April 2026 (P release).** Governance lags adoption,
  board AI literacy is weak, entities concentrate on a single provider, and
  embedded AI is opaque. APRA "not proposing to introduce additional
  requirements at this stage". It expects AI supply-chain mapping and exit
  plans (S).
- **ASIC REP 798** for licensees (S).

**(b) When.** The client is a bank, insurer or super trustee; the agent
supports a critical operation; the consultancy or Google is a material
service provider; data is processed offshore.

**(c) Paperwork.**
- A new **APRA service provider and offshoring facts** sheet: critical
  operation, data location, exit plan, fourth parties (Google
  sub-processors).
- Questionnaire: the CPS 234 and CPS 230 clocks.
- Impact assessment: concentration risk.

**(d) Counsel.** Is the arrangement material? Is APRA notification or
consultation needed for offshoring? Do the post-1 July 2026 exemptions
apply?

### 11.9 Health records

**(a)**
- **My Health Records Act 2012 s 77 (P).** The System Operator,
  registered repository operators, portal operators and registered
  contracted service providers "must not ... hold the records, or take the
  records, outside Australia" or "process or handle the information ...
  outside Australia". They also must not cause or permit others to.
  Penalties: up to 5 years' imprisonment, 300 penalty units, or a civil
  penalty of 1,500 penalty units.
- **Victoria.** The Health Records Act 2001 binds public and private
  organisations (P header). It includes HPP 9 on transborder flows (U).
- **NSW.** HRIPA covers agencies and private health service providers and
  holders (P). HPP 14 on transborder flows (U).
- **ACT.** Health Records (Privacy and Access) Act 1997 (U).
- **TGA.**
  - Digital scribe review outcome on 16 October 2026.
  - Changes to the clinical decision support exemption take effect
    1 November 2026, checked 2026-10-26 (P).
  - The exclusion for digital mental health tools is under review.

**(b) When.**
- Health information in prompts, retrieval or memory.
- Clinical summarising, triage or decision support.
- Any My Health Record integration: then **no offshore processing**. A
  model endpoint or log sink outside Australia blocks the design.

**(c) Paperwork.**
- PIA: the regions section, with evidence of the ML processing region.
- Memo: a medical device screen and the applicable state Health Privacy
  Principles.

**(d) Counsel.** Is any function a medical device? Does s 77 reach the
consultancy or Google? Which state's principles apply?

### 11.10 State public sector privacy

**(a)**
- **NSW PPIP Act 1998.** The Mandatory Notification of Data Breach scheme
  in Part 6A covers agencies and state-owned corporations: notification,
  an internal breach register and a published policy (P). The
  commencement date of 28 November 2023 was not confirmed on the page (U).
- **Victoria PDP Act 2014.** OVIC's guidance (both pages updated 26 June
  2026, P):
  - Do not put personal information into public generative AI tools; it
    likely breaches the IPPs, including IPP 9 on transborder flows.
  - Outputs containing personal information are a new collection.
  - For enterprise generative AI, PIAs are needed "per function";
    one overarching PIA "likely will not be sufficient".
  - Care with automated decisions, including steps that "significantly
    influence" them.
  - IPP 5 policy updates.
  - The Victorian Protective Data Security Standards bind contracted
    service providers.
- **Queensland.** The Information Privacy Act 2009 as amended by the IPOLA
  Act 2023 brings the QPPs and mandatory breach notification from 1 July
  2025, with local government from 1 July 2026, and bound contracted
  service providers (S/U).
- **Privacy Act link.** The consultancy acting under a State contract is
  exempt from the federal Privacy Act for those acts (s 7B(5), P), so the
  state Act and the contract clauses govern.

**(b) When.** The client is a state agency, council or state-owned
corporation, or the consultancy is bound by contract to a state Act.

**(c) Paperwork.**
- PIA in the state's own template (OVIC template; NSW AI Assessment
  Framework).
- Breach-scheme roles.
- The Victorian Protective Data Security Standards or the state ISMS in the
  questionnaire.
- The contracted service provider clauses in the memo's roles section.

**(d) Counsel.** Which Act binds the consultancy? Does the Google region
satisfy the state transborder rule?

## Not verified at a primary source

Re-read these before a reference file relies on them.

**Privacy and the OAIC**
- The full text of the ART Bunnings decision [2026] ARTA 130, including
  the permitted general situation reasoning and the APP 1.2, 1.3 and 5.1
  findings.
- The text of the Kmart determination.
- The date of APP Guidelines Chapter 1 v2.0.
- The last 25 to 35% of each OAIC AI guidance page (not read).
- Whether the tranche 2 bill has been introduced since 18 September 2026.
  Search found nothing; the parliamentary site refused automated fetches.
- The $364 penalty unit.

**Google Cloud.** Gemini ML processing in australia-southeast1 for the
pinned model, and the data-residency exclusions. Read the model page and
<https://cloud.google.com/terms/data-residency> per project; the terms page
did not render for the fetch tool.

**Government AI policy.** The names of AI6 practices 4 to 6, and the AISI
details.

**Other laws**
- Queensland IPOLA commencement dates.
- The NSW data breach scheme commencement (28 November 2023).
- AHRC guidance.
- The federal discrimination Acts' text.
- The ACT Workplace Privacy Act.
- CPG 235.
- The full APRA AI letter.
- The Telemarketing Standard sunset.
- The eSafety chatbot code text.
- The $3 million ransomware threshold in the rules.
- The SOCI incident-reporting hours.
- The 2024 SOCI data storage amendment.
- The Victorian workplace surveillance bill.

## Must cover, should cover, mention only

**Must cover.** Every Australian pack screens for these.

1. Privacy Act and the APPs (1, 3, 5, 6, 8, 10, 11, 12, 13). Include the
   APP entity status of client and consultancy and the small business,
   employee records and State contract exemptions.
2. APP 1.7 to 1.9 automated-decision transparency, from 10 December 2026,
   checked 2026-10-26.
3. PIA (OAIC 10 steps). Mandatory for Commonwealth agencies on high
   privacy risk projects.
4. APP 8 and s 16C for model endpoints, logs, grounding and support access
   outside Australia.
5. Notifiable Data Breaches (30-day assessment), with the incident clocks
   of the sector regimes beside it.
6. OAIC AI guidance (both October 2024 pages) as the standard the PIA is
   measured against.
7. DTA policy, the AI impact assessment (by 15 December 2026) and the
   transparency statement inputs, for Commonwealth clients.
8. Australian Consumer Law ss 18 and 29 for consumer-facing agents, plus
   s 28B from 1 July 2027.

**Should cover.** Screen for these when the trigger fires.

1. Workplace surveillance (NSW, ACT) and employee consultation, for agents
   touching staff.
2. APRA CPS 234 and CPS 230 and the April 2026 AI letter, for finance
   clients.
3. My Health Records s 77 and the state health records Acts, for health
   clients.
4. State public sector privacy (NSW PPIP, Vic PDP with OVIC guidance, Qld
   IP Act) and the NSW AI Assessment Framework, for state clients.
5. Guidance for AI Adoption (AI6) mapping in the impact assessment.
6. Statutory privacy tort, for monitoring, profiling or disclosure
   designs.
7. Spam Act, Do Not Call Register and Telemarketing Standard, for outbound
   agents.
8. Anti-discrimination, for agents that decide about people.
9. Cyber Security Act ransomware reporting and SOCI.

**Mention only.** One line in the memo, with the date checked.

1. Tranche 2 exposure draft (not law).
2. Children's Online Privacy Code (to be registered by 10 December 2026).
3. National AI Plan, mandatory guardrails dropped, and the AI Safety
   Institute.
4. OAIC biometric determinations (Clearview, Bunnings, Kmart). Promote
   them to "must" if the agent touches biometrics.
5. Online Safety codes and the social media minimum age (public chatbots
   only).
6. Copyright: no text-and-data-mining exception.
7. TGA medical device rules.
8. NSW digital work systems duties (not commenced).
9. The Victorian workplace surveillance bill (not introduced).
10. Deepfake sexual material offences.
11. AS ISO/IEC 42001.

## Screening checklist

Each trigger is a fact the brief or design already records. A "yes" adds
the law to the regime screen and a section to the named document. Where a
trigger needs a legal judgement, the line is a `counsel:` item, not a
conclusion.

| # | Trigger (fact with its ID) | Law | Document → section |
| --- | --- | --- | --- |
| 1 | Personal information about anyone in prompts, tools, memory, logs or evaluation sets | Privacy Act, APPs | Memo → Regime screen; PIA input pack → Information flows, APP compliance check |
| 2 | Client turnover ≤ $3m, and not a health provider, Commonwealth contractor or other exception | s 6D small business exemption | Memo → Roles under the Privacy Act (`counsel:`) |
| 3 | Consultancy itself handles personal information (build, test, support) | Consultancy as APP entity; s 6D, s 7B(2), s 95B | Memo → Roles; Inventory → Consultancy rows |
| 4 | Client is a Commonwealth agency | Agencies Privacy Code s 12 PIA; s 95B contract terms; DTA policy | PIA input pack (mandatory); DTA AI impact assessment input pack; System card → Transparency statement inputs |
| 5 | Client is a non-corporate Commonwealth entity and the use case meets any DTA Appendix C criterion | DTA AI impact assessment by 15 December 2026, checked 2026-10-26 | DTA input pack → Threshold (sections 1–4), full (sections 5–12) |
| 6 | Client is a state agency, council or state-owned corporation; or the consultancy works under a State contract | s 7B(5); NSW PPIP and HRIPA, Vic PDP, Qld IP Act; NSW AI Assessment Framework | Memo → Roles, Sector and state laws; state PIA template |
| 7 | Data subjects are the client's employees | Employee records exemption s 7B(3) (client only, not the consultancy, not job applicants); NSW and ACT workplace surveillance | Memo → Roles; Workplace surveillance check; Plan → W wait for the notice |
| 8 | Agent logs, monitors or analyses staff computer use or prompts | NSW Workplace Surveillance Act; ACT Workplace Privacy Act; tort | Workplace surveillance check; PIA → Risks |
| 9 | Agent output feeds a decision about a person: contract right, benefit, significant service, employment, credit, insurance, health, education, pricing | APP 1.7–1.9 from 10 December 2026, checked 2026-10-26; anti-discrimination | Memo → Automated decisions (APP 1.7); System card → Privacy policy inputs (APP 1.8); Impact assessment → Bias; `counsel_required: yes` |
| 10 | Model endpoint is global or outside Australia, or the model page does not list Australian ML processing; grounding with Google Search or Maps; RAG Engine; offshore support or abuse review | APP 8.1, s 16C; APP 5.2(i)–(j) | PIA → Overseas recipients (use or disclosure facts); Inventory → Overseas countries |
| 11 | Sensitive information is collected, inferred or likely in free text (health, biometric, racial or ethnic origin, sexuality, criminal record, union membership) | APP 3.3 consent; APP 6.2(b) | PIA → Sensitive information; OAIC AI guidance |
| 12 | Health information; client is a health service provider | Privacy Act (no small business exemption); Vic HRA and NSW HRIPA | PIA → Health; Memo → Sector and state laws |
| 13 | Integration with My Health Record | My Health Records Act s 77: nothing held or processed offshore | Memo → Blocker unless every flow is in Australia |
| 14 | Clinical summarising, triage or decision support | TGA software as a medical device | Memo → Medical device screen (`counsel:`) |
| 15 | Biometric features: face, voice or fingerprint matching | APP 3.3; Bunnings and Kmart; OAIC facial recognition guide, July 2026 | PIA → Proportionality; `counsel_required: yes` |
| 16 | Reuse of existing customer or staff data for fine-tuning, evaluation or new purposes | APP 6; OAIC training guidance; I-MED lessons | PIA → Secondary use (consent or opt-out) |
| 17 | Agent talks to consumers, or makes claims about products, refunds or guarantees | ACL ss 18 and 29; s 28B from 1 July 2027 | Impact assessment → Consumer claims and choice-architecture review; System card → AI disclosure |
| 18 | Outbound email, SMS or chat marketing | Spam Act | System card and questionnaire → Outbound channel |
| 19 | Outbound voice calls (synthetic voice) | Do Not Call Register Act; Telemarketing Standard | Outbound channel → Register check, hours, s 12 information |
| 20 | Public chatbot reachable by Australians; service likely to be used by under-18s | Online Safety codes; Children's Online Privacy Code (pending) | Memo → Online safety scope; PIA → Children |
| 21 | Client is APRA-regulated, or the agent supports a critical operation | CPS 234, CPS 230; APRA AI letter of 30 April 2026 | APRA service provider and offshoring facts; Questionnaire → Incident notification |
| 22 | Client is a SOCI responsible entity or government; turnover above $3m | SOCI; Cyber Security Act ransomware reporting | Questionnaire → Incident notification |
| 23 | Any personal information held | Notifiable Data Breaches ss 26WH–26WM | Questionnaire → Incident notification (30-day assessment; who notifies) |
| 24 | Third-party content used for fine-tuning or retrieval, or outputs published | Copyright (no text-and-data-mining exception) | Impact assessment → Intellectual property; Content licence register |
| 25 | Agent decides or acts without human review | AI6 practice 6; DTA AGT addendum; APP 1.7 | System card → Human oversight and contestability |
| 26 | Design intentionally monitors, profiles or exposes people | Statutory tort (Schedule 2) | PIA → Risks |

## What the current skill gets wrong or misses for Australia

Read against `SKILL.md`, the four references, the seven templates and
`scripts/check_governance.py` at commit 6139498.

1. **The classification memo is EU-only and the checker enforces that.**
   `REQUIRED` hard-codes the memo sections "Roles (provider and
   deployer)", "Prohibited practices (Article 5)", "High-risk
   classification (Article 6 and Annex III)" and "Transparency obligations
   (Article 50)". An Australian memo would have to fill them with `n/a:`
   lines or fail. The pack needs a jurisdiction field in the front matter
   (`jurisdictions: [AU]`) and per-jurisdiction required sections. The
   Australian memo has these sections:
   - Regime screen;
   - Roles under the Privacy Act;
   - Automated decisions (APP 1.7);
   - Sector and state laws;
   - Government AI policy;
   - Applicable dates;
   - Questions for counsel.
2. **"DPIA" and its screening are GDPR-specific.**
   - The template screens against the nine WP248 criteria and has a
     "Legal basis" section built on Article 6 and Article 9.
   - Australia has no lawful-basis test. Writing "legal basis: legitimate
     interests" in an Australian pack would be wrong.
   - The Australian equivalent is the OAIC PIA: a threshold assessment,
     then an APP-by-APP compliance check, with the s 12 Agencies Code
     trigger for Commonwealth clients.
   - Article 36 prior consultation has no equivalent.
   - "Works council" has no Australian equivalent. The nearest are
     consultation terms in modern awards and enterprise agreements, and
     the NSW and ACT workplace surveillance notice rules.
3. **Records of processing (Article 30) do not exist in Australia.**
   Replace them with the personal information inventory and notice inputs
   (APP 1.4 policy contents, APP 5.2 notice matters, APP 1.8 entries,
   overseas countries). The checker's `processing-records` section name
   would need a jurisdiction variant.
4. **The roles text is wrong for Australia.** The skill says that under
   GDPR the client is usually controller and the agency processor. In
   Australia today:
   - There is no processor category.
   - The consultancy is an APP entity in its own right unless it is a
     small business. A small business is still covered as a Commonwealth
     contracted service provider (s 6D), or when it is exempt only for
     acts under a State contract (s 7B(5)), where state law and contract
     clauses apply instead.
   - Section 95B makes Commonwealth agencies flow the APPs down by
     contract.
   - The client's employee records exemption does not cover the
     consultancy.
   - A controller and processor model exists only in the tranche 2 draft.
5. **"Human in the loop" is treated as the escape from automated-decision
   rules.** The privacy reference frames automated decisions through
   GDPR Article 22 ("based solely on automated processing").
   - APP 1.7 is wider: it covers a program that does a thing
     "substantially and directly related to making" a decision.
   - The OAIC says human review does not take generative AI outputs out
     of scope unless oversight is "extensive".
   - The draft must not imply that recording a reviewer takes a system out
     of scope in Australia.
6. **No breach-notification facts.** The pack has no section on incident
   notification. Australian clients will ask for these clocks:
   - Privacy Act: assess within 30 days and notify "as soon as
     practicable" (ss 26WH and 26WK);
   - ransomware payment report: 72 hours, Cyber Security Act;
   - SOCI cyber incidents: 12 or 72 hours (unverified);
   - CPS 234: 72 hours to APRA.
   Add an "Incident notification" topic to the questionnaire answer bank,
   and contract flow-down from consultancy to client.
7. **The model-provider section has no cross-border analysis.** It
   describes Google's retention and abuse monitoring but not whether
   prompts leave Australia.
   - For Australian clients, the PIA needs the APP 8 facts: the regional
     endpoint (australia-southeast1 or 2, never global), whether the
     pinned model has ML processing listed in Australia, the grounding and
     RAG Engine exclusions from data residency (S), offshore abuse-review
     and support access, and the "effective control" contract facts.
   - Under the My Health Records Act, holding or processing those records
     outside Australia is a hard stop (see the health records section).
8. **The impact assessment maps to ISO/IEC 42005 and NIST only.**
   - Add an AI6 (Guidance for AI Adoption) mapping, which Australian
     reviewers recognise.
   - For Commonwealth clients, add the DTA AI impact assessment input
     pack, due for in-scope use cases by 15 December 2026, checked
     2026-10-26.
   - For NSW agencies, add the NSW AI Assessment Framework fields.
9. **The system card misses the APP 1.8 block and transparency statement
   inputs.**
   - The OAIC expects vendors to give the client "clear, high-level
     information" for its privacy policy.
   - Commonwealth agencies need transparency statement inputs.
   - The card's Human oversight section should also cover contestability
     (AI6 clause 2.2) and the DTA contestability section.
10. **Article 50 transparency has no Australian statute, but the duty
    reappears elsewhere.**
    - The OAIC recommends telling people they are dealing with AI.
    - The ACL prohibits misleading conduct, such as an agent presenting as
      human or making false claims.
    - For outbound messages, the Spam Act's identification rules apply.
    - The memo should screen these, not say "no transparency duty".
11. **The checker's applicability-date rule does not fire on Australian
    references.** `LEGAL_REF` matches only "Art.", "Article", "Annex",
    "Regulation", "Directive", "AI Act", "GDPR", "Omnibus" and "Chapter".
    - A line such as "APP 1.7 applies from 10 December 2026" or "s 26WH
      ... Privacy Act" carries no matched term, so a missing `checked`
      date is not caught.
    - Add `APP\s?\d`, `Privacy Act`, `\bs{1,2}\s?\d+[A-Z]*`, `Schedule`,
      `Code`, `Standard` (CPS) and `Act \d{4}`.
12. **The Annex III trigger list is EU-shaped, though largely reusable.**
    - The OAIC's list of in-scope APP 1.7 decisions overlaps Annex III
      (recruitment, credit, insurance, education admission, benefits,
      biometrics, immigration). It adds personalised pricing, programmatic
      advertising for significant goods, health and disability service
      prioritisation, and employee bonus and remuneration.
    - For Australian packs, a match should also force `counsel_required:
      yes` with the area named "APP 1.7 significant decision".
    - Add Australian triggers: "My Health Record", "health information",
      "tax file number", "outbound call", "SMS campaign", "under 18",
      "Commonwealth entity", "APRA-regulated".
13. **Dates and sources.** Every Australian date in this note carries
    "checked 2026-10-26".
    - The checker's 180-day staleness warning is right for Australia: the
      tranche 2 bill, the Children's Code and the Kmart review may all
      move within six months.
    - Like the EU sources, the Australian sources cannot go in the GitHub
      source register; date them in the reference files.
14. **Australian terms to adopt.**
    - "personal information" (not "personal data");
    - "sensitive information" (not "special category");
    - "APP entity";
    - "contracted service provider";
    - "eligible data breach";
    - "PIA";
    - "overseas recipient".
    Using GDPR terms in an Australian pack signals to an Australian
    reviewer that it was not written for them.
