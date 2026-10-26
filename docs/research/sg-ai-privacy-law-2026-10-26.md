# Singapore: privacy and AI law for the governance pack

*Read 26 October 2026. Research for adding Singapore to
`skills/adk-governance-pack` at screen depth. Drafts, not legal advice.*

## Conclusion

Singapore has no AI Act. It regulates personal data through the Personal
Data Protection Act 2012 (PDPA), as amended in 2020, and governs AI through
voluntary frameworks from IMDA and the PDPC, sector regulators (MAS, MOH and
HSA) and a few targeted statutes (online safety, elections deepfakes). A
Singapore memo is therefore a **regime screen**, like the Australian one, and
assigns no risk tier.

For "an Australian consultancy builds AI agents that process personal data
of Singapore users and employees for Singapore clients", seven things change
the pack.

1. **The consultancy is almost always a data intermediary.** The PDPA has a
   controller and processor split, under its own names: the client is the
   "organisation" and a service provider that processes personal data "on
   behalf of and for the purposes of" the client "pursuant to a contract
   which is evidenced or made in writing" is a **data intermediary**. A data
   intermediary carries only three obligations: protection (s 24),
   retention limitation (s 25) and notifying the client of a breach
   "without undue delay" (s 26C(3)). The PDPC's AI guidance names the role
   directly: "Third-party developers of bespoke AI Systems ('Service
   Providers') are data intermediaries" (1 March 2024), and system
   providers who customise generative AI systems for deployers "are data
   intermediaries" (20 July 2026). The client keeps every other obligation
   "as if the personal data were processed by the organisation itself"
   (s 4(3)). The role is lost for any use beyond the contract: reusing
   client data for another client or for the consultancy's own evaluation
   sets makes the consultancy an organisation with all the obligations.
   This is closer to GDPR than to Australia, where the consultancy is an
   APP entity in its own right.
2. **Consent is the default basis, but the 2020 exceptions fit AI work.**
   There is no lawful-basis menu. The client needs consent, deemed consent
   (by conduct, contractual necessity or notification with an opt-out
   period) or an exception in the First or Second Schedule. The **business
   improvement exception** covers using data already collected to develop,
   test, monitor and debias an AI system for the client's own goods and
   services; the **legitimate interests exception** needs a documented
   adverse-effect assessment and public disclosure of reliance; deemed
   consent by notification needs an assessment and a reasonable opt-out
   period. Each assessment must be kept for as long as the data is used on
   that basis (Personal Data Protection Regulations 2021). The PDPC's new
   generative AI guidelines (20 July 2026) say "General Notifications are
   an insufficient means of obtaining consent" for large-scale model
   training or fine-tuning; that needs an "AI-Specific Notification".
3. **Every flow out of Singapore is a Transfer Limitation Obligation fact,
   and it is the client's.** Section 26 and the Personal Data Protection
   Regulations 2021 require the transferring organisation to ensure the
   recipient is bound by "legally enforceable obligations" (law, a contract
   that imposes a comparable standard **and specifies the countries**,
   binding corporate rules, or another binding instrument) or holds a
   specified certification (Global or APEC CBPR; for a data intermediary
   recipient, also Global or APEC PRP). Singapore keeps no adequacy list.
   The duty sits with the client even when its Singapore data intermediary
   moves the data offshore. Consultancy staff in Sydney reading traces,
   logs or evaluation sets, and any model endpoint outside Singapore, are
   transfers. The pack should write a transfer assessment annex row for
   Singapore, not just an input-pack line as for Australia's APP 8.
4. **Breach notification has a hard three-day clock.** Once the client
   determines that a breach is notifiable (likely significant harm, using
   the prescribed data classes, or 500 or more people), it notifies the
   PDPC "as soon as practicable, but in any case, no later than three (3)
   calendar days", and affected individuals at the same time or after. The
   assessment should generally take no more than 30 calendar days. The
   consultancy's duty is to tell the client without undue delay from when
   it has credible grounds to believe a breach occurred. Australia allows
   30 days to assess and then "as soon as practicable".
5. **No DPIA duty, no automated-decision rule, no Article 30 register.**
   The PDPA has no automated-decision provision like APP 1.7, GDPR Article
   22 or UK Articles 22A to 22D, and no data portability duty in force.
   DPIAs are encouraged, not required; the PDPC's generative AI guidelines
   do expect a DPIA "or other written record(s)" where an organisation
   relies on the publicly available exception for data behind a digital
   barrier. The accountability obligation (ss 11 and 12) requires a
   designated data protection officer with published business contact
   details, written policies and practices, and a complaints process. The
   PDPC's AI guidelines ask for written policies on fairness, safeguards and
   human oversight "proportionate to the risks", and suggest system cards
   form part of them.
6. **The voluntary AI frameworks are the reviewer's vocabulary.** IMDA's
   Model AI Governance Framework for Agentic AI (launched at Davos on 22
   January 2026; Version 1.5 published 20 May 2026, updated 5 June 2026) is
   the crosswalk a Singapore reviewer will expect for an ADK agent: bound
   risks up front, meaningful human accountability (including override-rate
   and review-time monitoring), technical controls and end-user
   responsibility. IMDA's Starter Kit for Testing Agentic Systems
   (October 2026) and the Transparency Guidelines for Generative AI
   Chatbots (20 July 2026, a "chatbot info card" for external chatbots)
   complete the set. All are voluntary.
7. **Sector rules carry the hard paperwork.**
   - **MAS.** Final Guidelines on Artificial Intelligence Risk Management
     were issued on 7 October 2026 and take effect on 7 October 2027, with
     lifecycle controls expected by 7 October 2028. They cover generative
     AI and "AI agents (including multi-agent systems)", including
     inventory attributes for agents. TRM Notices impose a 1-hour incident
     notice to MAS; Notice 658 governs outsourcing by banks (register,
     audit access, offshore customer information).
   - **MOH and HSA.** AIHGle 2.0 (10 March 2026) and the software medical
     device guidelines; the Health Information Act 2026 is expected to
     take effect in early 2027.
   - **Employment.** The Workplace Fairness Act 2025 is the key statute for
     hiring agents; see section 13 for its commencement.

Recommended shape, if Singapore is added as `sg`:
- **Regulatory memo.** "Singapore: PDPA and roles" (organisation and data
  intermediary, public-agency carve-out, DPO); "Singapore: AI governance
  frameworks" (voluntary, with versions); "Singapore: Sector and
  employment".
- **Privacy impact input pack.**
  - "Singapore: PDPA obligations check": consent or exception per purpose,
    with the assessments kept; notification; purpose; access and
    correction; accuracy; protection; retention; transfer.
  - "Singapore: Notification and policy inputs": notification text,
    AI-Specific Notification for any training, legitimate-interest
    disclosure, written-policy content.
- **Transfer assessment annex.** Written when Singapore personal data
  leaves Singapore, including consultancy access from Australia.
- **System card.** PDPC-recommended disclosures (function, data types,
  relevance, influential features) and, for external chatbots, chatbot
  info card inputs.
- **Security questionnaire.** The data intermediary's breach notice to the
  client, the client's 3-day PDPC clock, MAS 1-hour clock for financial
  clients, and PDPC ICT practices for AI systems.
- **Impact assessment.** An agentic MGF mapping; a MAS materiality and FEAT
  section for financial clients; adverse impact on the Workplace Fairness
  Act characteristics for employment uses.
- **Records of processing.** None: Singapore has no Article 30 register. The
  input pack's Singapore sections replace it, as for Australia.

## Sources

"P" means read at the primary source on 26 October 2026 (for PDFs, text
extracted locally from the file the regulator serves). "S" means secondary
reporting or a search-result summary only; re-read before relying on it.
Four research forks read the AI governance frameworks, the legislation
status and the sector rules under the same rules on the same day. Their
notes are `sg-fork-b.md`, `sg-fork-b2.md`, `sg-fork-c.md` and
`sg-fork-c2.md` in the scratchpad. A WebSearch and WebFetch usage limit
stopped every reader between about 17:05 and 17:40 Sydney time. The items
left unread then were re-read after it (forks B2 and C2), or are listed
under "Not verified at a primary source".

### PDPA and PDPC (read by the coordinator)

| Source | Status | Used for |
| --- | --- | --- |
| Personal Data Protection Act 2012, Singapore Statutes Online, "Current version as at 26 Oct 2026" (<https://sso.agc.gov.sg/Act/PDPA2012>) | P for the table of contents and the version timeline only (the section bodies lazy-load and the site then blocked automated requests) | Parts and section titles in force; no data portability Part; amendments by Act 40 of 2020 (versions of 1 February 2021 and 1 October 2022 in the timeline), Act 19 of 2025 (5 December 2025) and Act 2 of 2026 (16 October 2026) |
| Statutes (Miscellaneous Amendments) Act 2025, No. 19 of 2025 (<https://sso.agc.gov.sg/Acts-Supp/19-2025/>) and Public Sector (Governance) (Amendment) Act 2026, No. 2 of 2026 (<https://sso.agc.gov.sg/Acts-Supp/2-2026/>) | P, titles; content per fork B2 | What the 2025 and 2026 PDPA amendments changed |
| PDPC, Advisory Guidelines on Key Concepts in the PDPA, "Revised 29 April 2026" (<https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/ag-on-key-concepts/advisory-guidelines-on-key-concepts-in-the-pdpa-17-may-2022.pdf>; the file name still says 17 May 2022) | P, chapters 6 to 7, 12, 14 to 21 read | Organisation and data intermediary; public agencies; inbound data; consent, deemed consent, legitimate interests, business improvement and research exceptions; notification; access timeframes; retention; transfer conditions and contract clauses; breach notification; DPO |
| PDPC, Advisory Guidelines on Use of Personal Data in AI Recommendation and Decision Systems, "Issued 1 Mar 2024" (<https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/advisory-guidelines-on-the-use-of-personal-data-in-ai-recommendation-and-decision-systems.pdf>) | P, read in full | Business improvement and research exceptions for AI; notification content; written policies; service providers as data intermediaries |
| PDPC, Advisory Guidelines on Use of Personal Data in Generative AI, "Issued 20 July 2026" (<https://www.pdpc.gov.sg/assets/143cb9d4-532e-4cca-9a77-bcc0415ca294>; landing page "Published on 20 Jul 2026", <https://www.pdpc.gov.sg/organisations/regulations-decisions/regulatory-guidance/advisory-guidelines-on-use-of-personal-data-in-generative-ai>) | P, read in full | Model provider, system provider and deployer roles; AI-Specific Notifications; digital barriers; agentic safeguards; access and correction for RAG and models |
| PDPC, public consultation page for those guidelines (<https://www.pdpc.gov.sg/organisations/regulations-decisions/public-consultations/public-consultation-on-the-proposed-advisory-guidelines-on-use-of-personal-data-in-generative-ai>) | P (page body shows only its title and "Published on 20 Jul 2026"); consultation launch on 2 June 2026 is S | History |
| PDPC, Advisory Guidelines on Enforcement of the Data Protection Provisions, "Revised 1 October 2022" (<https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/advisory-guidelines-on-enforcement-of-dp-provisions_1oct2022.pdf>) | P, para 27 read | Financial penalty caps |
| PDPC, Advisory Guidelines on the Do Not Call Provisions, "Revised 1 February 2021" (<https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Advisory-Guidelines/Advisory-Guidelines-on-the-DNC-Provisions-1-Feb-2021.pdf>) | P, overview, checking duty, 21-day validity and voice-call definition read | DNC duties for outbound agents |
| PDPC, Guide to Data Protection Impact Assessments, 14 September 2021 (<https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Other-Guides/DPIA/Guide-to-Data-Protection-Impact-Assessments-14-Sep-2021.pdf>) | P, introduction and phase 1 read | DPIA triggers and phases |
| PDPC, Guide to Data Protection Practices for ICT Systems, "Issued 14 September 2021, Revised 20 July 2026" (<https://www.pdpc.gov.sg/assets/c752cf2b-844b-4163-82a5-ae5a9eb5c982>) | P, introduction and the "When Adopting AI Systems" practices searched | AI inventory; least-privilege and time-bound access for agentic systems; input and output logging |
| PDPC, Guide to Basic Anonymisation, updated 24 July 2024 (<https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/advisory-guidelines/guide-to-basic-anonymisation-(updated-24-july-2024).pdf>) | P, contents and k-anonymity passage read | Five steps; k-anonymity threshold "at 3 or 5" |
| PDPC, NRIC Advisory Guidelines (effective 1 September 2019) and NRIC FAQs (<https://www.pdpc.gov.sg/nric-faqs>) | S (search extract of the PDPC FAQ) | Limits on collecting NRIC and other national identification numbers |
| PDPC decision, Marina Bay Sands Pte Ltd, [2025] SGPDPC 6, 28 October 2025 (<https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/commissions-decisions/gd_mbs_28102025-(final)-v3.pdf>) | S (search summary) | Penalty of S$315,000 under the amended s 48J |
| Personal Data Protection (Amendment) Regulations 2026, reported adopted 26 February 2026 and in force 2 March 2026, amending regulation 12(2) on specified certifications (<https://digitalpolicyalert.org/change/18570-cross-border-data-transfer-regulations-in-personal-data-protection-amendment-regulations-2026>) | S | Consistent with the Key Concepts guidelines (April 2026), which list Global CBPR and Global PRP as specified certifications (P) |
| Data portability status: Allen & Gledhill, 17 November 2020 (<https://www.allenandgledhill.com/sg/publication/articles/17205/expected-date-of-commencement-of-personal-data-protection-amendment-bill-and-preparatory-steps-for-organisations>) | S | Portability was to be phased in later; the SSO table of contents (P) shows no portability Part in force |

### AI governance frameworks (fork B and fork B2)

| Source | Status | Used for |
| --- | --- | --- |
| IMDA, Model AI Governance Framework for Agentic AI, "Version 1.5, Published 20 May 2026 (Updated 5 June 2026)" (<https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf>) | P | Four dimensions; value chain; checkpoints; override rate; end-user disclosures |
| IMDA press release, "Singapore Launches New Model AI Governance Framework for Agentic AI", Davos, 22 January 2026 (<https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/new-model-ai-governance-framework-for-agentic-ai>) | P, title and dateline | Launch date |
| IMDA factsheet, "Updated Model AI Governance Framework for Agentic AI", 20 May 2026 (<https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/factsheets/2026/updated-model-ai-governance-framework-for-agentic-ai>) | P, title and date | Update |
| AI Verify Foundation, MGF for Generative AI page (<https://aiverifyfoundation.sg/resources/mgf-gen-ai/>) | P | GenAI framework of 30 May 2024 and its nine dimensions; MGF 2nd edition of 21 January 2020 |
| AI Verify Foundation, "What is AI Verify" (<https://aiverifyfoundation.sg/what-is-ai-verify/>) and resource library (<https://aiverifyfoundation.sg/resources/>) | P | AI Verify dates, 11 principles, crosswalks; Moonshot; starter kits; assurance sandbox |
| IMDA, Starter Kit for Testing Agentic Systems for Safety and Reliability, Version 1.0, October 2026 (<https://www.imda.gov.sg/assets/603572eb-724a-46cf-ac12-14fe38e1558c.pdf>) | P | Four testing steps |
| IMDA, Starter Kit for Testing LLM-Based Applications for Safety and Reliability (<https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/starter-kit-for-testing-llm-based-applications-for-safety-and-reliability.pdf>) | P that it exists and is voluntary; version and date S (image-only PDF) | Five risks |
| IMDA, Transparency Guidelines for Generative AI Chatbots, "Published 20 July 2026" (<https://www.imda.gov.sg/-/media/imda/file/emerging-technologies-and-research/artificial-intelligence/transparency-guidelines-for-generative-ai-chatbots.pdf>) | P | Chatbot info card; scope; deployer responsibility |
| MDDI, written answer to a parliamentary question on regulating high-risk AI, 7 July 2026 (<https://www.mddi.gov.sg/newsroom/mddi-s-response-to-pq-on-key-risk-thresholds-to-regulate-high-risk-ai-deployments-and-implementing-mandatory-human-oversight-for-fully-automated-decisions-materially-affecting-individuals/>) | P (fork B2) | No AI Act; Government stance |
| MinLaw and MDDI, "Online Safety Commission and Online Safety (Relief and Accountability) Act 2025 to Start on 29 June 2026", 14 May 2026 (<https://www.mlaw.gov.sg/online-safety-commission-and-online-safety-relief-and-accountability-act-2025-to-start-on-29-june-2026/>) | P (fork B2) | OSRAA commencement and first-phase harms |
| MDDI, "New Legal Measures to Uphold Integrity of Online Advertising During Elections", 9 September 2024 (<https://www.mddi.gov.sg/newsroom/new-legal-measures-uphold-integrity-online-advertising-elections/>) | P (fork B2); passage 15 October 2024 and commencement 22 January 2025 S | Elections deepfake prohibition |
| PDPC, *Iapps Pte Ltd*, 10 February 2021 (<https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Commissions-Decisions/Decision---Iapps-Pte-Ltd---10022021.pdf>) | S (fork B2) | Public-agency exclusion narrowed from 1 February 2021 |
| CSA, "Provisions in the Cybersecurity (Amendment) Act to Come Into Force on 31 October 2025" (<https://www.csa.gov.sg/news-events/press-releases/provisions-in-the-cybersecurity--amendment--act-to-come-into-force-on-31-october-2025/>) | P (fork B2) | Commencement; 2-hour CII clock |
| CSA, Guidelines and Companion Guide on Securing AI Systems (<https://www.csa.gov.sg/resources/publications/guidelines-and-companion-guide-on-securing-ai-systems/>) and Securing Agentic AI addendum (<https://www.csa.gov.sg/resources/publications/addendum-on-securing-ai-systems/>, page dated 17 June 2026) | P (fork B2) | AI security baseline; addendum still consultation version |
| IMDA, Model AI Governance Framework, Second Edition (<https://www.imda.gov.sg/-/media/imda/files/infocomm-media-landscape/sg-digital/tech-pillars/artificial-intelligence/second-edition-of-the-model-ai-governance-framework-22jan.pdf>) | P (fork B2) | Principles, four areas, human-involvement models |

### Sector rules (fork C and fork C2)

| Source | Status | Used for |
| --- | --- | --- |
| MAS, Guidelines on Artificial Intelligence Risk Management, 7 October 2026 (<https://www.mas.gov.sg/-/media/mas-media-library/regulation/guidelines/bd/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions/guidelines-on-artificial-intelligence-risk-management.pdf>) | P, sections 1 to 5 read | Scope, dates, inventory, materiality, lifecycle, third-party AI, agents |
| MAS media release, 7 October 2026 (<https://www.mas.gov.sg/news/media-releases/2026/mas-sets-out-supervisory-expectations-on-responsible-ai-adoption-by-financial-institutions>) | P | Dates; 2027 agentic consultation |
| MAS Consultation Paper P017-2025 (13 November 2025 to 31 January 2026) | S | History |
| MAS, FEAT Principles, 12 November 2018, para 1.4 updated 7 February 2019 (<https://www.mas.gov.sg/publications/monographs-or-information-paper/2018/feat>) | P | FEAT status |
| MAS media release, Veritas Toolkit version 2.0, 26 June 2023 (<https://www.mas.gov.sg/news/media-releases/2023/toolkit-for-responsible-use-of-ai-in-the-financial-sector>) | P | Veritas |
| MAS Information Paper on AI Model Risk Management, 5 December 2024 (<https://www.mas.gov.sg/publications/monographs-or-information-paper/2024/artificial-intelligence-model-risk-management>) | S | Precursor |
| MAS, Guidelines on Risk Management Practices – Technology Risk, 18 January 2021 (<https://www.mas.gov.sg/regulation/guidelines/technology-risk-management-guidelines>) | P, landing page | TRM Guidelines |
| MAS Notice FSM-N05 on Technology Risk Management, issued 9 May 2024, effective 10 May 2024 (<https://www.mas.gov.sg/-/media/mas-media-library/regulation/notices/trpd/notice-fsm-n05/mas-notice-fsm-n05.pdf>) | P, read in full | 1-hour notice; 14-day root cause report; 4-hour recovery |
| MAS Consultation Paper P012-2026 on TRM Notices, June 2026 (<https://www.mas.gov.sg/-/media/mas-media-library/publications/consultations/trpd/2026/consultation-paper-on-proposed-amendments-to-notices-on-technology-risk-management.pdf>) | P, preface | Pending AI-related risk register |
| MAS Notice 658, 11 December 2023, effective 11 December 2024 (<https://www.mas.gov.sg/-/media/mas-media-library/regulation/notices/bd/notice-658/mas-notice-658---4.pdf>) and MAS Third-Party Risk Management page (<https://www.mas.gov.sg/regulation/third-party-risk-management>) | P | Outsourcing register, contract terms, audit, offshore customer information |
| MAS SAFR white paper v1.1, 9 October 2026 (<https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf>) | P | Not regulatory guidance; mention only |
| MOH circular MOH-MHC-0024-2026, 13 March 2026, AIHGle 2.0 (<https://isomer-user-content.by.gov.sg/7/f5b5f08c-4c34-499c-89d4-3368b5d93088/MOH%20MHC%20Cir%200024_2026%20Updated%20MOH%20Artificial%20Intelligence%20in%20Healthcare%20Guidelines%20(AIHGle%202.0).pdf>) and MOH AI in healthcare page (<https://moh.gov.sg/licensing-and-regulation/artificial-intelligence-in-healthcare>) | P | AIHGle 2.0 |
| HSA digital health and guidance documents pages (<https://www.hsa.gov.sg/medical-devices/digital-health>; <https://www.hsa.gov.sg/medical-devices/guidance-documents>) | P | Software medical device guidance versions |
| MOH press release on the Health Information Bill, 12 January 2026 (<https://www.moh.gov.sg/newsroom/health-information-bill-to-support-coordinated-care-across-singapore-s-healthcare-ecosystem/>) | P | Content; "early 2027" |
| Government Gazette, Acts Supplement No. 6, 14 February 2025, Workplace Fairness Act 2025, No. 8 of 2025 (<https://assets.egazette.gov.sg/2025/Legislative%20Supplements/Acts%20Supplement/06.pdf>) | P (fork C2) | Passage, assent, commencement by notification, threshold, ss 5, 17 to 19, 27, 28, 34 |
| MOM, Second Reading speech on the Workplace Fairness (Dispute Resolution) Bill, 4 November 2025 (<https://www.mom.gov.sg/newsroom/speeches/2025/1104-second-reading-of-workplace-fairness-dispute-resolution-bill>) and factsheet, 14 October 2025 (<https://www.mom.gov.sg/newsroom/press-releases/2025/1014-workplace-fairness-dispute-resolution-bill-factsheet>) | P (fork C2) | "end-2027" target; claims route |
| TAFEP, Workplace Fairness page (<https://www.tal.sg/tafep/workplace-fairness>), Tripartite Guidelines page (<https://www.tal.sg/tafep/getting-started/fair/tripartite-guidelines>), "Fair Hiring First, AI Second", 20 October 2025 (<https://www.tal.sg/tafep/resources/articles/2025/fair-hiring-first-ai-second>) | P (fork C2) | TGFEP status and sanction; AI hiring good practice |
| MOM, oral answer on employer use of AI in hiring, 13 November 2024 (<https://www.mom.gov.sg/newsroom/parliament-questions-and-replies/2024/1113-oral-answer-to-pq-on-guidelines-on-employer-use-of-artificial-intelligence-in-hiring>) | P (fork C2) | Tools do not change the employer's duty |
| HSA, GL-07 update announcement (<https://www.hsa.gov.sg/announcements/update-for-guidelines-on-risk-classification-of-samd-and-qualification-of-clinical-decision-support-software--cdss-/>) | S (fork C2) | CDSS criterion from 21 July 2025 |
| MAS, Guidelines on Third-Party Risk Management consultation paper P004-2026 (<https://www.mas.gov.sg/-/media/mas-media-library/publications/consultations/bd/2026/consultation-paper---tprmg.pdf>) | S (fork C2) | Not final |


## 1. PDPA scope and roles: organisation, data intermediary, public agency

**(a) Status and dates.** Personal Data Protection Act 2012, current
version as at 26 October 2026 (P, SSO). The data protection provisions
are Parts 3 to 6A; the Do Not Call provisions are Parts 9 and 9A (P, Key
Concepts para "Overview of the PDPA"). The 2020 amendments (Act 40 of 2020)
took effect in stages on 1 February 2021 and 1 October 2022, checked
2026-10-26 (P, SSO timeline; which provision commenced on which date is S).

- **Organisation.** "any individual, company, association or body of
  persons, corporate or unincorporated whether or not formed or recognised
  under the law of Singapore; or resident, or having an office or a place
  of business, in Singapore" (P, Key Concepts). Every organisation must
  comply "in respect of activities relating to the collection, use and
  disclosure of personal data in Singapore" (P). Data collected overseas
  and brought into Singapore is covered from the time it is in Singapore
  (P, "Applicability to Inbound Data Transfers").
- **Data intermediary.** "an organisation that processes personal data on
  behalf of another organisation but does not include an employee of that
  other organisation" (P). When it processes "on behalf of and for the
  purposes of another organisation pursuant to a contract which is
  evidenced or made in writing", it is subject only to the protection,
  retention limitation and breach-notification-to-the-organisation
  obligations (P). The contract need not label it a data intermediary;
  the function decides (P). If it "uses or discloses personal data in a
  manner which goes beyond the processing required ... under the contract,
  then B will not be considered a data intermediary in respect of such use
  or disclosure" and all obligations apply (P). An organisation can be a
  data intermediary for one data set and an organisation for another (P).
- **The client's liability.** Section 4(3): the organisation has the same
  obligations for data processed by its data intermediary "as if the
  personal data were processed by the organisation itself" (P, quoted in
  Key Concepts). The PDPC says due diligence and a clear written scope are
  good practice, including who handles access and correction requests (P).
- **The AI guidance applies the role to AI vendors.**
  - AI recommendation and decision systems guidelines (1 March 2024):
    "Third-party developers of bespoke AI Systems ('Service Providers')
    are data intermediaries who have obligations under the PDPA i.e.,
    Protection and Retention Obligations" (para 1.4, P). Part V does not
    apply to developers of off-the-shelf products (para 11.1, P).
  - Generative AI guidelines (20 July 2026): "Model Providers", "System
    Providers" and "System Deployers" (para 6.2, P). A model provider that
    runs inference or hosts data for downstream users is a data
    intermediary (para 7.4, P); a model provider that uses end-user prompts
    for its own model development is an organisation with all obligations
    (para 7.1, P). A system provider is an organisation for its own data
    sets and a data intermediary "on behalf of downstream deployers (e.g.
    to customise systems for specific use cases ...)" (para 8.1, P). The
    deployer "bear[s] primary responsibility for ensuring that the
    Generative AI Systems they have chosen to use can meet their
    obligations under the PDPA" (para 9.1, P).
- **Public agencies are excluded** from the data protection provisions:
  the Government, ministries, departments, agencies, organs of State,
  tribunals, and statutory bodies the Minister gazettes (P, Key Concepts).
  "Organisations that provide services to public agencies may either have
  obligations under the PDPA as data controllers or as data
  intermediaries" (P). A data intermediary of a public agency must notify
  the agency of a breach without undue delay (s 26E; P, Key Concepts fn
  57). See section 15.
- **Business contact information** is outside the data protection
  provisions (P, Key Concepts).
- **Accountability (ss 11 and 12).** The organisation must designate one or
  more individuals (the DPO) to be responsible for compliance (s 11(3)),
  make the business contact information of at least one available
  (s 11(5)), develop and implement policies and practices, including a
  complaints process, and make information about them available on request
  (s 12) (P, Key Concepts ch 21). Contact details should be "readily
  accessible from Singapore, operational during Singapore business hours
  and in the case of telephone numbers, be Singapore telephone numbers",
  especially if the person "is not physically based in Singapore" (P, para
  21.7).

**(b) Triggers.**
- The client is a Singapore company, or a foreign one that collects, uses
  or discloses personal data in Singapore.
- Data subjects in Singapore: customers, users, employees, applicants.
- The consultancy builds, tests, supports or monitors the system with
  access to the client's personal data.
- The consultancy reuses client data for anything outside the contract
  (cross-client evaluation sets, its own fine-tuning, product analytics).
- Google (or another model provider) runs inference on the data.
- The client is a ministry, statutory board or organ of state.

**(c) Paperwork.**
- **Regulatory memo, Roles.**
  - Client as organisation; consultancy as data intermediary under a
    written contract (contract reference or `gap:`); Google as model
    provider and data intermediary for inference, in the GenAI guidelines'
    terms.
  - Supply-chain roles in the GenAI guidelines' words: consultancy as
    system provider, client as system deployer.
  - Uses that would take the consultancy outside the intermediary role,
    each as `counsel:`.
  - Client's DPO and published contact details (`gap:` until named).
- **Privacy impact input pack.** A "Singapore: PDPA obligations check"
  table that shows which obligations sit with the client and which with
  each data intermediary.
- **Security questionnaire.** The data intermediary's own obligations:
  protection, retention and breach notice to the client.

**(d) Counsel questions.**
- Is the consultancy a data intermediary for every processing step, and
  does the contract record the scope in writing?
- Does any planned reuse (evaluation sets, prompt libraries, telemetry)
  make the consultancy an organisation for that data?
- Does the PDPA reach the consultancy directly for its handling in
  Australia, or only through the client's contract? (The PDPA binds
  organisations wherever formed, for activities in Singapore.)
- Is Google a data intermediary of the client or a sub-intermediary of the
  consultancy, and who holds the contract?

## 2. Consent, deemed consent, notification and the legitimate interests exception

**(a) Status and dates.** Sections 13 to 17 and the First and Second
Schedules; deemed consent by notification (s 15A) and the legitimate
interests exception (First Schedule Part 3 para 1) came with the 2020
amendments; in force since 1 February 2021, checked 2026-10-26 (P for the
provisions in the current Act; the commencement date per the SSO timeline,
provision mapping S).

- **Consent (ss 13, 14).** No collection, use or disclosure without
  consent unless deemed consent or an exception applies. Consent obtained
  by "false or misleading information or using misleading and deceptive
  practices" is not valid, including purposes "stated in vague or
  inaccurate terms" (s 14(2)(b), P). An organisation may not require
  consent beyond what is reasonable to provide the product or service
  (P; repeated for AI training in the GenAI guidelines para 4.8).
- **Deemed consent (s 15).** By conduct: the individual voluntarily
  provides data for purposes "objectively obvious and reasonably
  appropriate from the surrounding circumstances" (P). By contractual
  necessity: disclosure by A to B, and onward to C, where "reasonably
  necessary for the conclusion or performance of the transaction" with the
  individual (s 15(3), P).
- **Deemed consent by notification (s 15A).** For new or secondary
  purposes where no exception fits. Before relying on it the organisation
  must (P, Key Concepts):
  - conduct an assessment that the use "is not likely to have an adverse
    effect on the individual", identifying measures to eliminate or
    mitigate adverse effects (s 15A(4)(a));
  - take reasonable steps to tell the individual its intention, the
    purpose and "a reasonable period within which, and a reasonable manner
    by which" to opt out (s 15A(4)(b));
  - wait until the opt-out period lapses. It "should not be relied on
    where individuals would not have a reasonable opportunity and period
    to opt out". PDPC examples use 10 and 14 days and say a monthly
    interaction implies no less than one month (P).
  - Keep the assessment for as long as the data is used on this basis and
    produce it to the PDPC on request (Personal Data Protection
    Regulations 2021; P, Key Concepts).
- **Legitimate interests (First Schedule Part 3 para 1).** The organisation
  must identify and articulate the legitimate interest, conduct an
  assessment of adverse effects and mitigations with a balancing test for
  any residual effect, and "take reasonable steps to provide the
  individual with reasonable access to information that they are relying
  on the exception", for example in its public data protection policy,
  with the business contact information of a person who can answer
  questions (P). The assessment is kept and produced on request (P). It
  cannot be used "to send direct marketing messages" (P). Examples include
  fraud and money-laundering detection, "IT and network security" and
  "preventing misuse of services" (P).
- **Adverse effect** generally means "physical harm, harassment, serious
  alarm or distress"; differential treatment is not automatically adverse
  (P, Key Concepts).
- **Notification (s 20).** Inform the individual of the purposes on or
  before collection, and of any new purpose before use or disclosure for
  it; on request, give the business contact information of a person who
  can answer questions (P). For employment, the organisation informs the
  individual of the purpose of "entering into an employment relationship
  ... or managing or terminating the employment relationship" (s 20(4)
  and (5), P, Key Concepts fn 14).
- **Evaluative purpose.** Defined in s 2(1) to include determining
  suitability, eligibility or qualifications for employment, promotion,
  continuance or removal; admission to an education institution; awarding
  contracts, scholarships and benefits; and deciding whether to insure a
  person (P, Key Concepts fn 48). Data collected for an evaluative purpose
  is covered by specific consent exceptions and by an exception to the
  access obligation for opinion data kept solely for that purpose (P).
- **Withdrawal (s 16).** Organisations must allow and facilitate withdrawal
  and tell the individual its likely consequences (P).
- **Publicly available data.** Collectable without consent, subject to the
  reasonable-person test (s 18). For generative AI, data behind a "digital
  barrier" (paywall, registration, authentication, geo-blocks or age gates,
  bot blockers) must be assessed before relying on the exception, with
  the reasoning in "a Data Protection Impact Assessment or other written
  record(s)" (GenAI guidelines paras 3.4 to 3.7, P).

**(b) Triggers.**
- A chat or voice agent collects personal data from Singapore users.
- The agent uses existing customer or staff data for a purpose not
  notified at collection (summaries, scoring, grounding, memory).
- A purpose for which consent is impractical: fraud, security monitoring,
  misuse detection (legitimate interests).
- Outputs about a person are generated or inferred (the PDPC treats
  insights about an identifiable person as personal data; Key Concepts on
  business insights, P).
- Recruitment, performance or other evaluative uses.
- Web or forum data used for grounding or training.

**(c) Paperwork.**
- **Privacy impact input pack, "Singapore: PDPA obligations check".** One
  row per purpose: consent, deemed consent (which kind) or the exception
  relied on (Schedule and paragraph), with `counsel:`. Link each deemed
  consent by notification or legitimate interests row to its assessment
  record and owner; a missing assessment is a `gap:`.
- **Input pack, "Singapore: Notification and policy inputs".** Proposed
  notification text; the opt-out period and channel; the public
  legitimate-interest statement and contact.
- **System card.** The data section restates no notice; it points to the
  client's data protection notice and lists the data kinds the agent
  handles.

**(d) Counsel questions.**
- Is each purpose within the original notified purposes, deemed consent,
  or an exception?
- Is the adverse-effect assessment adequate, and is the opt-out period
  reasonable for this channel?
- Does a free-text agent collect data beyond what the notified purpose
  covers, and is that collection "reasonable" under s 18?
- For employees: which purposes fall within the employment exceptions and
  s 20(4), and which need consent?

## 3. Business improvement and research exceptions (the AI development route)

**(a) Status and dates.** First Schedule Part 5 and Second Schedule Part 2
Division 2 (business improvement); Second Schedule Part 2 Division 3
(research); in force since 1 February 2021, checked 2026-10-26 (P for the
text in the guidance; date as in section 2). The PDPC's AI guidelines of 1
March 2024 apply them to AI.

- **Business improvement (use without consent of data already lawfully
  collected).** Purposes: improving or developing goods or services;
  improving or developing methods or processes for business operations;
  "learning or understanding behaviour and preferences of individuals";
  identifying suitable goods or services or personalising them (P). Two
  conditions: the purpose "cannot reasonably be achieved without using the
  personal data in an individually identifiable form", and a reasonable
  person would consider the use appropriate (P). Sharing within a group of
  companies is also covered, with a binding contract or BCRs requiring
  safeguards (P). It cannot be used to send direct marketing (P).
- **For AI systems (AI RDS guidelines, P).** Relevant to development,
  testing and monitoring "when an AI System is intended to improve
  operational efficiency by supporting decision-making, or to offer more or
  new personalised products" (para 4.2(a)). Considerations: whether
  personal data improves the system's effectiveness; whether other means
  are technically possible or cost-effective; industry practice (para 5.3).
  Examples include "Internal HR systems used to recommend potential job
  candidates" and "Job assignment systems" (para 5.4). It can cover
  testing with live personal data and bias assessment, and "generally,
  industry best practice is to use personal data to debias datasets"
  (paras 5.6 to 5.10).
- **Limit for generative AI (GenAI guidelines, P).** The PDPC's example of
  a company that rebrands as a model developer: using customer data for
  generative AI development is "so significant a departure from past
  commercial activities that a reasonable person would not consider the
  use to be appropriate", so "the appropriate course of action is to
  obtain fresh consent" (para 4.2 example).
- **Research.** Broader R&D without a product roadmap. Conditions: the
  purpose cannot be accomplished without identifiable data; "a clear public
  benefit"; results "will not be used to make any decision that affects
  the individual"; published results do not identify the individual. For
  disclosure, it must also be impracticable to seek consent (P).
- **Data protection while using them.** Data minimisation;
  pseudonymisation "as a basic control" where possible; development
  environments protected to production standard; a DPIA encouraged where
  raw personal data is used (AI RDS paras 7.1 to 7.4, P).

**(b) Triggers.**
- Production conversations, tickets or HR records used to build or
  evaluate the agent, or as evaluation sets.
- Live-data testing or bias measurement with protected characteristics.
- Fine-tuning a model on client data.
- Joint research with a university or another company.

**(c) Paperwork.**
- **Input pack, "Singapore: PDPA obligations check".** The exception
  relied on for each development, evaluation and monitoring data set,
  with the two conditions written as facts (why identifiable data is
  needed; why a reasonable person would expect it) and `counsel:`.
- **Input pack, Necessity and proportionality.** Pseudonymisation of
  evaluation sets (C or SB ID, or `gap:`); environment controls.
- **Impact assessment, adverse impact.** Where personal data is used for
  bias assessment, the business improvement basis and the safeguards.
- **Records of the data intermediary (the consultancy).** Data mapping,
  labelling and a provenance record of training and evaluation data, which
  the AI RDS guidelines list as good practice for service providers (para
  11.2, P).

**(d) Counsel questions.**
- Does evaluation or fine-tuning on production data fall within business
  improvement, or is it a "significant departure" needing fresh consent?
- Is identifiable data necessary, or must the sets be pseudonymised or
  anonymised?
- Does the research exception's "no decision that affects the individual"
  condition hold where research outputs feed a later product?

## 4. Purpose, notification, access and correction, accuracy, protection and retention

**(a) Status and dates.** All in force; the access-related preservation
duty (s 22A) and the Personal Data Protection Regulations 2021 since 1
February 2021, checked 2026-10-26 (P for text in the Key Concepts
guidelines; date per the SSO timeline).

| Obligation | What it requires (P, Key Concepts unless marked) | Agent facts to record |
| --- | --- | --- |
| Purpose limitation, s 18 | Only for purposes "a reasonable person would consider appropriate in the circumstances" and that have been notified. Deployers "should be disciplined about specifying the intended purpose of processing and amount of personal data required" (GenAI para 9.2) | The agent's stated purpose; tools and data stores it can reach; whether retrieval is scoped to the purpose |
| Notification, s 20 | Purposes on or before collection and before any new use; contact person on request | Proposed notice text; in-chat notice at first use |
| Access, s 21 | Respond "as soon as reasonably possible"; if not within 30 days, tell the individual in writing within 30 days when it will respond. Covers data held by data intermediaries. Information on use and disclosure in the past year | Which stores (sessions, memory, RAG, logs, evaluation sets) can be searched by person; the GenAI guidelines expect organisations to accede "where the request refers to personal data stored in a Retrieval-Augmented Generation database" (para 10.5(b)) |
| Correction, s 22 | Correct as soon as practicable; if not within 30 days, tell the individual when | Correction path for memory and RAG; removing inaccurate data "from training datasets before they undertake future AI training runs" (GenAI para 10.5(b)) |
| Preservation, s 22A | Keep a copy of data subject to a rejected access request for at least 30 calendar days | Retention rules must not purge it early |
| Accuracy, s 23 | Reasonable effort to ensure accuracy and completeness where data is likely to be used to make a decision affecting the individual or disclosed | Evaluation results; output labelling; the decision the output feeds |
| Protection, s 24 | "Reasonable security arrangements" against unauthorised access, collection, use, disclosure, copying, modification, disposal and loss, including of storage media. Deployers must safeguard "new categories of data sources ... (e.g. end-user prompts, inputs and generated outputs, agent or tool activity data, internal enterprise data)" (GenAI para 9.3). System providers must review security for risks such as "prompt injection attacks" (para 8.2) | SB and C IDs; prompt-injection controls; access controls on prompt logs |
| Retention limitation, s 25 | Cease to retain, or anonymise, as soon as the purpose is no longer served and retention is not needed for legal or business purposes; no "just in case" retention; no fixed period | Retention contract per store; deletion of memory, traces and evaluation sets; the GenAI guidelines recommend a retention policy with a rationale where training data is kept (para 7.3) |

**Anonymisation.** Anonymised data is not personal data (GenAI guidelines
fn 14, P). Ceasing to retain includes removing "the means by which the
personal data can be associated with particular individuals" (s 25, P).
The PDPC's Guide to Basic Anonymisation (updated 24 July 2024, P) sets five
steps (know your data, de-identify, apply techniques, compute risk, manage
re-identification and disclosure risks) and says "Generally the industry
threshold for k-anonymity value is at 3 or 5". Knowing or reckless
unauthorised re-identification of anonymised information is an offence for
individuals (s 48F, P, Key Concepts Part IV).

**(b) Triggers.** Any personal data in prompts, tools, memory, logs, traces,
evaluation sets or backups; a public chat channel; outputs that feed a
decision about a person.

**(c) Paperwork.**
- **Input pack.** The table above as "Singapore: PDPA obligations check",
  one row per obligation with the client and data intermediary split;
  data flows marked searchable by person; retention per store with the
  retention contract ID.
- **Security questionnaire.** Protection answers cite the PDPC's Guide to
  Data Protection Practices for ICT Systems (revised 20 July 2026, P),
  whose "When Adopting AI Systems" practices include an AI system
  inventory "capturing its purpose, data flow information and intended
  users", least-privilege access, and, for systems "with agentic
  capabilities", access limited to the intended data and time window, and
  logging of inputs and outputs. "The responsibility for protecting
  personal data remains with the organisation deploying the AI system" (P).
- **System card.** Limits and accuracy facts tied to M records.

**(d) Counsel questions.**
- Is a 30-day access response achievable for memory and vector stores, and
  does an exception (unreasonable burden) apply to model weights?
- Are evaluation sets anonymised to the PDPC's standard or only
  pseudonymised (and so still personal data)?
- Is the retention of traces and evaluation sets justified by a "legal or
  business purpose"?

## 5. Transfer Limitation Obligation and the transfer conditions in the Regulations

**(a) Status and dates.** Section 26 and Part 3 of the Personal Data
Protection Regulations 2021 (in force since 1 February 2021, checked
2026-10-26; P for content in Key Concepts ch 19, date per the SSO timeline).
The Personal Data Protection (Amendment) Regulations 2026, reported in force
2 March 2026, amended regulation 12(2) on specified certifications (S); the
Key Concepts guidelines revised on 29 April 2026 already list Global CBPR
and Global PRP (P).

- **When it applies.** A transfer to an organisation outside Singapore
  "where it relinquishes possession or direct control", including to a
  data intermediary or a group company (para 19.1, P). Where data overseas
  stays in the organisation's own possession or control (its own staff,
  servers it owns and maintains), all obligations apply directly instead
  (P).
- **Who is responsible.** With a data intermediary, the organisation "is
  responsible for complying with the Transfer Limitation Obligation ...
  regardless of whether the personal data is transferred by the
  organisation to an overseas data intermediary or transferred overseas by
  the data intermediary in Singapore" (P, Key Concepts, data intermediary
  section). The PDPC's example: a Singapore cloud provider moving data to
  London and Hong Kong for its client is a transfer the client must cover
  (P).
- **The standard.** The organisation must "ensure that personal data
  transferred overseas is protected to a standard comparable with the Data
  Protection Provisions" (P).
- **Ways to comply** (Regulations 2021; P, paras 19.4 to 19.7).
  - Legally enforceable obligations on the recipient, under:
    - any law;
    - a contract that imposes a comparable standard and "specifies the
      countries and territories to which the personal data may be
      transferred";
    - binding corporate rules for related recipients;
    - any other legally binding instrument.
  - A "specified certification": Global CBPR or APEC CBPR for a recipient
    organisation; for a recipient data intermediary, also Global PRP or
    APEC PRP.
  - Deemed satisfaction (to use only when the above are not available):
    consent after a written summary of the protection in the destination;
    contractual necessity; vital or national interest; data in transit;
    data publicly available in Singapore.
- **Minimum contract clauses** (para 19.9, P). For a data intermediary
  recipient: protection, retention limitation, and notifying the
  organisation of breaches "without undue delay". For an organisation
  recipient: purpose, accuracy, protection, retention, policies, access,
  correction and breach notification to the PDPC and individuals. The PDPC
  "recognises and encourages the use of the ASEAN Model Contract Clauses"
  (para 19.10, P).
- **Due diligence.** The transferring organisation may rely on a data
  intermediary's "extant protection policies and practices, including
  their assurances of compliance with relevant industry standards or
  certification" (P).
- **No adequacy list.** The guidance names no countries; Australia is not
  whitelisted (P, by absence in ch 19).

**(b) Triggers.**
- Consultancy staff in Australia build, test, read traces or logs, review
  evaluation sets or support the system with access to Singapore personal
  data.
- The model endpoint, the model's machine-learning processing, grounding,
  abuse monitoring or telemetry sit outside Singapore (for Google, check
  the model page for asia-southeast1 processing and the data residency
  exclusions; not read for Singapore today).
- Sub-processors outside Singapore.
- A group client centralises data with an overseas parent.

**(c) Paperwork.**
- **Transfer assessment annex.** Write it for Singapore, with one row per
  transfer: exporter (the client), recipient and country, data categories,
  access mode, the mechanism (contract clause reference specifying
  Australia, certification checked with its date, or deemed satisfaction
  relied on), and supplementary measures. The current annex template says
  `jurisdictions` "must include eu or uk"; that rule would need `sg`.
- **Input pack, Recipients and regions.** The client's transfer
  responsibility for transfers its data intermediaries make.
- **Security questionnaire, Overseas access.** "Singapore Transfer
  Limitation Obligation: contract clauses per Key Concepts para 19.9" with
  the contract reference.

**(d) Counsel questions.**
- Is consultancy access from Australia a transfer for which the client is
  responsible, and does the services contract impose a comparable standard
  and name Australia?
- Can the Privacy Act 1988 count as "any law" binding the consultancy to a
  comparable standard, or is a contract still needed? (Treat the contract
  as required until counsel says otherwise.)
- Does Google hold a specified certification for the data it processes, or
  does the Cloud Data Processing Addendum serve as the contract?
- Where data passes through a Singapore region in transit only, does the
  data-in-transit rule apply?

## 6. Mandatory data breach notification (Part 6A)

**(a) Status and dates.** Part 6A (ss 26A to 26E) and the Personal Data
Protection (Notification of Data Breaches) Regulations 2021, in force since
1 February 2021, checked 2026-10-26 (P for content in Key Concepts ch 20;
date per the SSO timeline).

- **Assessment.** On "credible grounds to believe that a data breach has
  occurred", the organisation takes "reasonable and expeditious steps to
  assess whether the data breach is notifiable"; it "should generally do so
  within 30 calendar days" and document every step (paras 20.2 to 20.5, P).
- **Data intermediary.** Must notify the organisation (or public agency)
  "without undue delay from the time it has credible grounds to believe
  that the data breach has occurred"; it has no duty to assess or to
  notify the PDPC or individuals (paras 20.7 to 20.8, P). Contracts should
  set the procedure (para 20.9, P).
- **Notifiable** if it is likely to result in "significant harm" (deemed
  where prescribed data classes are involved: full name, alias or full
  national identification number combined with financial, health, adoption
  and other listed data, or account identifiers with passwords, security
  codes or "biometric data or other data that is used or required to allow
  access to or use of the individual's account"), or is of "significant
  scale": "500 or more individuals" (paras 20.13 to 20.21, P).
- **Clock.** Notify the PDPC "as soon as practicable, but in any case, no
  later than three (3) calendar days" from determining the breach is
  notifiable; the first day is the day after the determination ("if an
  organisation determines on 1st January that a data breach is notifiable,
  it must notify the Commission by 4th January"). Notify affected
  individuals as soon as practicable, at the same time or after (paras
  20.22 to 20.25, P).
- **Exceptions** from notifying individuals (not the PDPC): remedial action
  making significant harm unlikely; technological protection such as
  encryption before the breach; and a law-enforcement prohibition or PDPC
  waiver (paras 20.26 to 20.30, P).
- **Several organisations.** Each is individually responsible; one may lead
  the assessment; each notifies the PDPC (paras 20.10 to 20.12, P).
- **Breaches within one organisation** (for example a misdirected internal
  email) are not notifiable (para 20.6, P).

**(b) Triggers.** Any personal data held; agent breach paths: prompt
injection that exfiltrates data, cross-user session or memory leakage, logs
sent to the wrong sink, data disclosed to a model provider outside the
contract, an agent sending a message with another person's data.

**(c) Paperwork.**
- **Security questionnaire, Incident response.** The consultancy's notice
  to the client "without undue delay" (contract term, with an hours figure
  if the client wants one); the client's assessment (within 30 days as a
  general rule) and its 3-calendar-day PDPC deadline; the significant-harm
  data classes the agent handles; the 500-person scale threshold.
- **Input pack, Risks and measures.** The agent breach paths above with C
  and SB IDs.
- **System card.** No breach facts; cites the questionnaire.

**(d) Counsel questions.**
- What notice period does the services contract set for the consultancy to
  tell the client?
- Do the data classes the agent handles (NRIC, salary, account
  credentials, health) make most breaches deemed significant harm?
- Who leads the assessment where the client, the consultancy and Google
  all hold the data?

## 7. Financial penalties, offences, private action and data portability

**(a) Status and dates.**
- **Financial penalties (s 48J).** "up to S$1 million or 10% of the
  organisation's annual turnover in Singapore, whichever is higher, for any
  intentional or negligent contravention of the Data Protection
  Provisions", the 10% limb applying where Singapore turnover exceeds S$10
  million; turnover taken from the most recent audited accounts (P,
  Enforcement guidelines para 27, revised 1 October 2022). The higher cap
  has applied since 1 October 2022, checked 2026-10-26 (P, guidelines'
  revision date and SSO timeline; S, PDPC announcement). Penalties weigh
  harm and culpability (P). Data intermediaries can be penalised for their
  own protection and retention failures (P, Key Concepts example: XYZ "may
  be liable under the Protection Obligation"). A recent penalty: Marina Bay
  Sands, S$315,000 for a protection breach, [2025] SGPDPC 6 (S).
- **Do Not Call penalties.** Up to S$200,000 for an individual and S$1
  million otherwise; for dictionary attacks and address harvesting, up to
  S$1 million or 5% of Singapore turnover above S$20 million (P,
  Enforcement guidelines para 27.2).
- **Offences for individuals (Part 9B).** Knowing or reckless unauthorised
  disclosure, improper use for wrongful gain or loss, and unauthorised
  re-identification of anonymised data (P, Key Concepts Part IV).
- **Other enforcement (Part 9C).** Directions, voluntary undertakings,
  alternative dispute resolution and a right of private action (s 48O)
  (P, SSO table of contents).
- **Data portability.** Not in force. The current SSO version (26 October
  2026) has no data portability Part, and the Key Concepts guidelines
  (29 April 2026) have no portability chapter (P, by absence). The 2020
  amendment proposed it with phased implementation (S, Allen & Gledhill,
  17 November 2020). Checked 2026-10-26.

**(b) Triggers.** Any personal data held; a client with Singapore turnover
above S$10 million (the 10% cap); outbound messaging (DNC caps).

**(c) Paperwork.** Regulatory memo: one line on the penalty cap with its
date and `checked 2026-10-26`; one line that data portability is not in
force. No other document needs it.

**(d) Counsel questions.** Exposure of the consultancy as a data
intermediary for protection failures, and the contract's indemnities.

## 8. Do Not Call provisions for outbound agents

**(a) Status and dates.** Parts 9 and 9A of the PDPA; Advisory Guidelines
on the Do Not Call Provisions revised 1 February 2021, checked 2026-10-26
(P).

- Three registers: No Voice Call, No Text Message and No Fax Message (P).
- Before sending a "specified message" (marketing) to a Singapore telephone
  number, check the register, unless the user or subscriber gave "clear and
  unambiguous consent in written or other accessible form", or an ongoing
  relationship exemption applies (P).
- Check results are valid for 21 days; the withdrawal-of-consent period is
  21 days (P).
- Identify the sender and how to contact them (s 44); do not conceal the
  calling line identity on voice calls (s 45) (P).
- "Voice call" includes "a call that involves a recorded or synthetic
  voice" (s 36(1), P, DNC guidelines fn 24). An AI voice agent making
  marketing calls is covered.
- No messages to numbers generated by address-harvesting software or by
  dictionary attacks (s 48B, P).
- Third-party checkers have their own duties (s 43A, P).
- Marketing messages through apps that do not use a Singapore telephone
  number fall outside the DNC provisions but the data protection
  provisions may still apply (P).
- Neither the legitimate interests nor the business improvement exception
  covers sending direct marketing (P, Key Concepts).

**(b) Triggers.** An outbound voice, SMS or messaging agent; marketing or
promotional content; synthetic voice; lead lists.

**(c) Paperwork.** System card, AI disclosure and outbound channel: register
check before each campaign (validity 21 days), sender identification,
calling line identity, consent records. Security questionnaire: consent and
register-check records retained. Regulatory memo: DNC line in the Singapore
section.

**(d) Counsel questions.** Is each message a "specified message" or an
exempt ongoing-relationship message? Does the consent wording meet "clear
and unambiguous"?

## 9. PDPC AI guidance: recommendation and decision systems, generative AI, DPIA, anonymisation, ICT practices

**(a) Status and dates.** All advisory: "not legally binding on the
Commission or on any other party" (GenAI guidelines para 1.5, P), but they
state how the PDPC reads the Act.

- **Advisory Guidelines on Use of Personal Data in AI Recommendation and
  Decision Systems**, issued 1 March 2024, checked 2026-10-26 (P).
  - Business improvement and research exceptions for AI development,
    testing and monitoring (section 3 above).
  - **Notification content** (para 9.5, P), "to the extent practicable":
    the product function that needs personal data; "a general description
    of types of personal data"; how the processing is relevant to the
    feature; "specific features of personal data that are more likely to
    influence the product feature". Detail is "proportionate to the risks
    of each use-case, e.g., taking into account potential harm to the
    individual and the level of autonomy of the AI System" (para 9.4).
    Layering is encouraged (para 9.7).
  - **Written policies** (paras 10.3 to 10.8, P): measures for "fairness
    and reasonableness" (bias assessment, training data quality,
    reproducibility); safeguards (pseudonymisation, minimisation,
    security); for higher-impact outcomes, "accountability mechanisms and
    human agency and oversight" and robustness. "model cards and system
    cards, can also form part of an organisation's written policies"
    (para 10.5). AI Verify test results can support these statements
    (para 10.10). The HSBC decision ([2021] SGPDPC 3) is cited as meeting
    the obligations by explaining AI credit assessments (fn 18).
  - **Service providers** (Part V, P): data mapping and labelling;
    "a provenance record to document the lineage of the training data"
    (para 11.2); supporting clients' notification, consent and
    accountability, including plain-language explanations of how outcomes
    are reached and training for human decision-makers (paras 11.4 to
    11.7). "organisations bear the primary responsibility" (para 11.8).
- **Advisory Guidelines on Use of Personal Data in Generative AI**, issued
  20 July 2026, checked 2026-10-26 (P). They "build on" the 2024
  guidelines (para 1.4).
  - Publicly available exception and digital barriers (section 2).
  - **AI-Specific Notifications** for using "User Data" to train or
    fine-tune: "General Notifications are an insufficient means of
    obtaining consent ... specifically, for large-scale Generative AI Model
    training and/or fine-tuning" (para 4.4). Fn 11 limits this to
    "activities that develop or modify a model's parameters or underlying
    capabilities", so retrieval and prompting are not training. Encouraged
    contents: the model's functions, the data types, how the data trains
    the model, and how to decline or withdraw (para 4.6).
  - **Roles** (paras 6 to 9): model provider, system provider, system
    deployer (section 1 above). Model and system providers are encouraged
    to document and share data access controls, residency, retention,
    input and output filters, testing metrics such as "likelihood of data
    leakage", and incident and breach procedures "(e.g. notification
    timelines)" (paras 7.5 and 8.3). System providers may refer to IMDA's
    chatbot transparency guidelines (para 8.3).
  - **Deployers** must safeguard "end-user prompts, inputs and generated
    outputs, agent or tool activity data, internal enterprise data",
    designate responsibility for each new data source, tell users what
    personal data may be input, and publish written policies (paras 9.3
    to 9.4). For "agentic functionalities" ("independent planning and
    action taking across multiple steps, often involving access to external
    tools and systems"), deployers "should carefully consider and be
    transparent about the privacy-utility trade-offs when scoping their
    agentic use cases" and may refer to IMDA's agentic framework (para
    9.5). The PDPC's agentic example: role-based data controls restricting
    file and network access, data classification for sensitive data, and
    "escalating protocols to humans for complex or high-risk tasks".
  - **Access and correction** (Part IV): obligations reach data used for
    development and deployment; accede "where the request refers to
    personal data stored in a Retrieval-Augmented Generation database";
    remove inaccurate data before future training runs; output filters in
    the interim (para 10.5).
- **Guide to Data Protection Impact Assessments**, 14 September 2021 (P).
  DPIAs are encouraged, not required (Key Concepts para 21.15, P: failing
  to do one "is not itself a breach of the PDPA" but can lead to a s 24
  breach). Conduct one when creating a new system or process that handles
  personal data, changing how existing ones handle it, restructuring, or
  collecting new types of data (P). Six phases: assess need; plan;
  identify personal data and flows; identify and assess risks; create an
  action plan; implement and monitor (P). The 2024 AI guidelines encourage
  a DPIA where raw personal data is used in development (para 7.3, P).
- **Guide to Basic Anonymisation**, updated 24 July 2024 (P): section 4.
- **Guide to Data Protection Practices for ICT Systems**, revised 20 July
  2026 (P): AI practices in section 4.
- **NRIC Advisory Guidelines**, effective 1 September 2019 (S): private
  organisations may collect NRIC numbers or copies only where required by
  law or needed to verify identity "to a high degree of accuracy"; the same
  applies to birth certificate, FIN and work permit numbers (S, PDPC FAQ
  search extract).

**(b) Triggers.** Any AI system using Singapore personal data; training or
fine-tuning on user data; a RAG store with personal data; an agent with
tool access; an agent that asks for or receives NRIC numbers.

**(c) Paperwork.**
- **Input pack, "Singapore: Notification and policy inputs".** The four
  AI RDS notification items per feature; AI-Specific Notification text
  where any model is fine-tuned; the written-policy content (fairness,
  safeguards, oversight) proportionate to impact and autonomy.
- **Input pack, Screening.** Whether a DPIA is advisable under the PDPC
  guide (`counsel:`; the DPO decides), and the written record for any
  publicly available data behind a digital barrier.
- **System card.** It doubles as the "system card" the PDPC names as part
  of written policies: data kinds, influential features, limits,
  oversight, robustness facts with M records.
- **Security questionnaire.** The GenAI guidelines' list of what a system
  provider shares: access controls, residency, retention, filters, data
  leakage test metrics, incident procedures and notification timelines.
- **Records (consultancy's own).** Data map and provenance record for any
  training or evaluation data.
- **NRIC.** Input pack necessity line; a masking contract for NRIC numbers
  in prompts and logs.

**(d) Counsel questions.**
- Is a DPIA expected for this system, given the PDPC encourages one for
  raw personal data in development?
- Does any fine-tuning or adapter training count as "large-scale" training
  needing AI-Specific Notification?
- Is collecting an NRIC number through the agent justified under the NRIC
  guidelines?

## 10. Voluntary AI governance frameworks (IMDA, AI Verify Foundation, CSA)

**(a) Status and dates.** All voluntary, checked 2026-10-26.

| Framework | Status (source) | What the pack takes from it |
| --- | --- | --- |
| Model AI Governance Framework, 2nd edition | Released 21 January 2020 (P, AI Verify Foundation; content P, IMDA PDF via fork B2). Principles: decisions "explainable, transparent and fair"; AI "should be human-centric". Four areas: internal governance; level of human involvement; operations management; stakeholder interaction. Human-in, over and out of the loop chosen on a severity and probability of harm matrix. ISAGO and the Compendium of Use Cases accompanied it (S) | The human-involvement label and its reasoning in the system card |
| Model AI Governance Framework for Generative AI | Released 30 May 2024 (P). Nine dimensions: accountability; data; trusted development and deployment; incident reporting; testing and assurance; security; content provenance; safety and alignment R&D; AI for public good | Mention only; dimensions 1 to 7 map onto existing pack sections |
| Model AI Governance Framework for Agentic AI | Launched at Davos on 22 January 2026 (P); Version 1.5 "Published 20 May 2026 (Updated 5 June 2026)" (P); "a living document" (P) | The Singapore crosswalk for an agent (below) |
| Starter Kit for Testing Agentic Systems for Safety and Reliability | Version 1.0, October 2026 (P); launched 14 October 2026 (S) | Frame agent tests in its four steps |
| Starter Kit for Testing LLM-Based Applications for Safety and Reliability | Voluntary (P); Version 1.0 dated January 2026 (S) | Five risks: hallucination and inaccuracy, bias in decision making, undesirable content, data leakage, adversarial prompts |
| Transparency Guidelines for Generative AI Chatbots | Published 20 July 2026 (P); voluntary but "we strongly encourage chatbot deployers to adopt at least a minimum" (P) | Chatbot info card inputs for external chatbots |
| AI Verify and Project Moonshot | AI Verify launched 25 May 2022, open-sourced 7 June 2023, generative AI extension 29 May 2025; 11 principles; crosswalks to ISO/IEC 42001 (21 July 2025) and NIST AI RMF (P) | Only when the client asks for AI Verify results or a Moonshot red-team |
| Global AI Assurance Sandbox and AI Tester Accreditation | Pilot 2025; first accredited testers October 2026 (P resource page; S for the list) | Security questionnaire "Certifications" row |
| CSA Guidelines and Companion Guide on Securing AI Systems | October 2024 (P); launched 15 October 2024 (S) | AI security baseline row |
| CSA, Securing Agentic AI – An Addendum | Consultation 22 October to 31 December 2025; page dated 17 June 2026 still the consultation version (P) | Cite as "addendum, consultation version" |

**Agentic MGF v1.5, the four dimensions (P, fork B):**
1. **Assess and bound the risks up front.** Impact factors: domain error
   tolerance, access to sensitive data ("the risk increases if the agent
   has persistent memory"), access to external systems, scope of actions
   (read versus write), reversibility; likelihood factors: autonomy,
   system complexity and "usage of third-party solutions". Bound risks by
   limiting tools and systems and giving agents identities and
   permissions so actions are "traceable and controllable".
2. **Make humans meaningfully accountable.** "chains of accountability
   across the agent value chain": model developers, platform providers,
   system providers or app developers, tooling providers (MCP, APIs),
   deployers, end users. Human approval at "significant checkpoints":
   high-stakes, irreversible ("permanently deleting data, sending
   communications, making payments"), outlier and user-defined. Audit
   oversight with the "Human override rate ... A low rate may signal
   rubber-stamping behaviours" and review time.
3. **Technical controls and processes.** Planning, tool and protocol
   controls; change management where "material changes such as model
   updates or autonomy adjustments may require a full governance review";
   pre-deployment testing of "overall execution accuracy, policy
   adherence, and tool use"; gradual roll-out and monitoring.
4. **End-user responsibility.** "Declare upfront in the user interface
   that the users are interacting with agents at the point of interaction,
   rather than writing it only in separate documentation"; the agent's
   range of actions; data handling; escalation contacts; training for
   internal users.

**Chatbot info card (P, fork B).** Deployers are "primarily responsible";
scope is external chatbots, with internal tools "outside the scope"; agents
judged by risk and context, including "taking actions on the user's
behalf" and access by minors. The card answers four questions with at least
one substantive disclosure each: what the chatbot can and cannot do; how
reliable and safe it is; how user data is handled; how to report issues. A
safety statement with a link to the card "at first use"; the card carries
its last-updated date and chatbot version; update triggers include
switching models and guardrail changes.

**(b) Triggers.** Every ADK agent for a Singapore client (agentic MGF);
an external chat agent (chatbot guidelines); a client or procurement asking
for AI Verify, Moonshot, ISO/IEC 42001 or accredited testing; a CISO asking
for an AI security baseline.

**(c) Paperwork.**
- **Regulatory memo, "Singapore: AI governance frameworks".** One line per
  framework: voluntary, version and date, `checked 2026-10-26`.
- **Impact assessment, "Singapore: Agentic MGF mapping".** The §2.1.1 risk
  factors with D and C IDs; value-chain roles (consultancy as system
  provider, Google as model developer and platform provider, client as
  deployer); approval checkpoints with C IDs; change-management triggers.
- **System card.** Human oversight: checkpoints, override rate and review
  time as M records, and the MGF 2020 human-involvement label. AI
  disclosure: "at the point of interaction". For external chatbots, a
  "Singapore: chatbot info card inputs" block (four questions, first-use
  statement, version and date).
- **System card, Evaluation results.** Which starter-kit risks were tested,
  with M records.
- **Security questionnaire.** Agent identity and permissions; CSA
  guidelines and agentic addendum mapped to SB and C IDs when asked.

**(d) Counsel questions.** Usually none. Ask whether the client has adopted
any framework as policy and whether MAS or MOH expects it for this use.

## 11. No AI Act; online safety, elections deepfakes and online harms

**(a) Status and dates.**
- **No AI Act.** "the need for regulation depends on how it is deployed,
  the nature of harm that may be caused"; the Government "will continue to
  study the appropriate regulatory stance for AI" (P, MDDI written answer
  to a parliamentary question, 7 July 2026, via fork B2). No AI bill found
  (S; the Parliament bills list was not searched directly). Checked
  2026-10-26.
- **Online Safety (Relief and Accountability) Act 2025.** Passed 5
  November 2025 (S). The Online Safety Commission began operating, and the
  specified statutory torts commenced, on 29 June 2026, checked 2026-10-26
  (P, MinLaw and MDDI release of 14 May 2026). First phase: intimate image
  abuse, image-based child abuse, doxxing, online harassment and online
  stalking (P); later phases include "inauthentic material abuse"
  (deepfakes) and online impersonation (S). Duties fall on communicators,
  administrators of online locations and platforms (P).
- **Elections (Integrity of Online Advertising) (Amendment) Act 2024.**
  Passed 15 October 2024 (S; confirmed as passed by MDDI, P). From the
  issue of the writ to the close of polling, it prohibits online election
  advertising that is "digitally generated or manipulated" and
  realistically shows a candidate saying or doing something they did not
  (P, MDDI, as introduced). Commencement on 22 January 2025 is S.
- **Online Criminal Harms Act 2023.** Used against AI-enabled scams (P,
  MDDI answer). Mention only.

**(b) Triggers.** A public agent whose outputs other users can see, that
hosts user content or generates content about real people; generated
images, audio or video of real people; political content.

**(c) Paperwork.** Regulatory memo: "No AI-specific statute applies in
Singapore (MDDI, 7 July 2026, checked 2026-10-26)" and mention-only lines.
Impact assessment: synthetic-media, doxxing and harassment risk rows when
the trigger fires.

**(d) Counsel questions.** Is the client an "administrator" or "platform"
for an agent surface? Could an output be election advertising during an
election period?

## 12. MAS: FEAT, Veritas, AI risk management guidelines, TRM and outsourcing

**(a) Status and dates (fork C, P unless marked).**
- **FEAT Principles**, 12 November 2018 (para 1.4 updated 7 February
  2019): principles, not a Notice; they "continue to apply" under the new
  AI guidelines (para 1.2).
- **Veritas Toolkit 2.0**, announced 26 June 2023, open source.
- **Guidelines on Artificial Intelligence Risk Management**, issued 7
  October 2026: "These Guidelines take effect on 7 October 2027. FIs may
  meet the expectations set out in Sections 3 to 4 from 7 October 2027,
  and Section 5 and 6 of the Guidelines by 7 October 2028" (para 1.8),
  checked 2026-10-26. Apply to "all FIs in a proportionate manner" (para
  2.1). AI includes "generative AI (including large language models), and
  AI agents (including multi-agent systems)" (fn 6).
  - Low-risk uses (internal drafting, summaries, staff chatbots locating
    internal resources) need basic governance only (paras 2.3 to 2.5).
  - Board-approved governance and risk appetite; senior management
    escalation for "AI incidents" (paras 3.4 to 3.6).
  - Identification must cover AI "in services provided by material
    third-party service providers" (para 4.2).
  - Inventory attributes; "For AI agents, relevant attributes may include
    agent-specific identifiers, information on the tools and systems the
    agent can access, its components, and the guardrails imposed" (fn 25).
  - Risk materiality by impact, complexity and reliance ("extent of
    autonomy granted ... and the degree of human involvement") (para
    4.12).
  - Lifecycle (section 5): kill-switch protocols for high-risk uses;
    explainability scaled to impact; fairness assessments with protected
    attributes and proxies; human oversight addressing automation bias;
    third-party AI where the FI "retains primary accountability", tests it
    "using the FI's own data" and contracts for "performance guarantees,
    data protection, the right to audit, notification when AI is
    introduced and updated"; evaluation citing IMDA's LLM starter kit;
    reproducibility documentation (para 5.17); independent review before
    deployment; red teaming (para 5.22).
  - MAS will consult in 2027 on further agentic AI guidance (media
    release).
- **TRM Guidelines**, 18 January 2021. **TRM Notice FSM-N05** (banks),
  effective 10 May 2024: "notify the Authority as soon as possible, but not
  later than 1 hour, upon the discovery of a relevant incident"; root cause
  and impact report within 14 days; critical systems' unscheduled downtime
  at most 4 hours in 12 months and recovery time at most 4 hours; IT
  controls to protect customer information. Sister notices cover other FI
  types. Proposed amendments (P012-2026, June 2026) would add an IT risk
  register covering risks of "the use of artificial intelligence"; not in
  force.
- **Outsourcing.** MAS Notice 658 (banks) and 1121 (merchant banks), and
  the Guidelines on Outsourcing for banks and for other FIs, effective 11
  December 2024: a register of outsourced relevant services and of those
  involving customer information; due diligence before material
  outsourcing, including the confidentiality-law risk where customer
  information is handled outside Singapore; contract terms on
  confidentiality, MAS audit access, sub-contracting, termination and
  deletion or return. Guidelines on Third-Party Risk Management are still
  a consultation (P004-2026, 6 March 2026) (S, fork C2).

**(b) Triggers.** The client is MAS-regulated; the agent informs credit,
underwriting, pricing, advice, claims, fraud or collections decisions; it
runs on or connects to a critical system; the consultancy builds or
supports it on an ongoing basis or handles customer information, especially
from Australia.

**(c) Paperwork.**
- **Regulatory memo, "Singapore: Sector and employment".** MAS guidelines
  with both dates; FEAT; whether the engagement is a material outsourced
  relevant service (`counsel:`); the register entry owner.
- **System card.** The fn 25 inventory attributes for agents; explanation
  and redress text.
- **Impact assessment.** MAS materiality inputs (impact, complexity,
  reliance); FEAT fairness definition and metrics; kill switch;
  independent reviewer.
- **Security questionnaire.** MAS 1-hour and 14-day clocks with the
  consultancy's notice to the client sized to them; recovery time; audit
  access; sub-contractor list including Google; third-party AI contract
  terms.
- **Transfer assessment annex.** Customer information accessed from
  Australia, with the Notice 658 para 5.1(c) facts.

**(d) Counsel questions.** Is the use case low-risk under para 2.3? Is the
consultancy a material third-party service provider? Is the engagement a
material outsourced relevant service, and is Google a sub-contractor needing
consent? Does banking secrecy (Banking Act s 47) add duties beyond the
PDPA?

## 13. Employment: Workplace Fairness Act 2025 and the Tripartite Guidelines

**(a) Status and dates (fork C2).**
- **Workplace Fairness Act 2025 (No. 8 of 2025).** Passed 8 January 2025,
  assent 3 February 2025 (P, Gazette). **Not in force**: it commences on a
  date the Minister appoints by Gazette notification, and none was found.
  MOM's target is "end-2027" and may move (P, MOM speech of 4 November
  2025; TAFEP). Write "expected end-2027 (MOM target, not gazetted),
  checked 2026-10-26".
  - Does not apply to employers with fewer than 25 employees, except s 26
    (s 4, P).
  - "Hiring" includes "inviting the individual to an interview, test or
    examination" and "asking for information or documents" (s 5(2)(b), P),
    so a screening agent that invites candidates performs hiring steps.
    Performance appraisal, promotion, training, demotion and dismissal
    are employment decisions (ss 6 and 7, P).
  - Protected characteristics: age; nationality; sex, marital status,
    pregnancy and caregiving responsibilities; race, religion and language
    ability; disability and mental health condition (P). A characteristic
    "suspected, assumed or believed" counts (s 17(4), P).
  - A written "direction, instruction or policy" that influences an
    "agent of the employer" to decide on a protected ground is itself
    discrimination, whether or not a decision follows (s 18, P).
  - Discriminatory job advertisements (s 19), a written grievance process
    with records (s 27) and no retaliation (s 28) (P).
  - Court civil penalties for a body corporate up to $50,000 for a first
    order and $250,000 otherwise (s 34, P).
  - No express provision on AI, algorithms or automated tools (P, text
    searched).
- **Workplace Fairness (Dispute Resolution) Act.** Passed 4 November 2025
  (P, MOM); mediation first, then the Employment Claims Tribunals up to
  $250,000 and the High Court above; time bars of one to 12 months (P).
  Commences with the main Act; number and assent date not confirmed.
- **Tripartite Guidelines on Fair Employment Practices.** Apply now; "All
  employers in Singapore are expected to adhere"; non-compliance brings MOM
  scrutiny and curtailed work pass privileges (P, TAFEP). They continue
  after the Act commences (P). Recruitment records kept "for at least one
  year" (P). MOM: "Regardless of the technological tools used to aid
  employment decisions ... employers must comply" (P, 13 November 2024).
  TAFEP's AI article (20 October 2025, good practice): job-related inputs
  only, "Let AI inform decisions, not make them", tell candidates how
  tools are used, give an appeal contact (P).
- **PDPA overlap.** Evaluative purpose and employment notification
  (section 2); the business improvement exception expressly covers
  "Internal HR systems used to recommend potential job candidates" (AI RDS
  para 5.4, P).

**(b) Triggers.** The agent screens CVs, ranks or shortlists, invites to
interviews or tests, drafts job ads, appraises performance, feeds
promotion, pay or dismissal decisions, or triages grievances, for a client
with Singapore staff or applicants; employer size 25 or more.

**(c) Paperwork.**
- **Regulatory memo.** Employment line: WFA passed, not in force, MOM
  target end-2027, checked 2026-10-26; TGFEP applies now; size threshold
  as a sourced fact.
- **Impact assessment, adverse impact.** Results by protected
  characteristic and by proxy (language ability, graduation year or NRIC
  prefix as age signals, nationality, caregiving gaps), with M records;
  excluded TGFEP fields filtered (C ID).
- **System card.** The person who makes the final decision and the review
  share (M record); candidate disclosure and appeal contact.
- **Input pack.** One-year recruitment record retention squared with the
  PDPA retention limitation.

**(d) Counsel questions.** Has a commencement notice been gazetted? Is the
client under 25 employees? Is a screening prompt or ranking rubric a
"policy ... in writing" under s 18, and is the agent or the consultancy an
"agent of the employer"? Does shortlisting for a client make the
consultancy an employment agency needing a licence?

## 14. Health: MOH AIHGle 2.0, HSA software medical devices, Health Information Act 2026

**(a) Status and dates (fork C and C2).**
- **AIHGle 2.0**, launched 10 March 2026 by MOH and HSA (P, MOH circular
  MOH-MHC-0024-2026 of 13 March 2026, addressed to all HCSA licensees and
  healthcare professionals). Covers generative AI; sets responsibilities
  of "developers, deployers, and users"; adds transparency and deployment
  risk guidance and a deployers' toolkit; replaces the 2021 guidelines
  (P). Guidelines; legal effect through licensing is `counsel:`.
- **HSA.** Software "intended for medical purposes such as investigation,
  detection, diagnosis, monitoring, treatment or management" is a medical
  device (P). Current guidance: GL-04-R4 software medical devices life
  cycle (December 2025); GL-07-R2 risk classification and clinical decision
  support software (July 2025); GN-37-R1 change management for
  machine-learning SaMD; GL-10-R1 cybersecurity (August 2026) (P, titles).
  GL-07-R2, in effect from 21 July 2025, treats CDSS as a non-device only
  if its output is "solely based on established clinical guidelines" (S).
- **Health Information Act 2026.** Passed 12 January 2026 (P, MOH); to
  "take effect from early 2027" (P); uncommenced on SSO (S). NEHR
  contribution, cybersecurity and data security requirements, incident
  notification to MOH, and "Access for employment or insurance purposes is
  prohibited" (P, MOH release).

**(b) Triggers.** An HCSA licensee client; clinical summarising, triage or
decision support; NEHR access or health information sharing; an insurer or
employer seeking health records.

**(c) Paperwork.** Regulatory memo: medical device screen (`counsel:`);
AIHGle roles (consultancy as developer, client as deployer, clinicians as
users); HIA as pending. Impact assessment: clinical validation inputs.
System card: intended setting, limits, transparency to clinicians.
Security questionnaire: HIA requirements once in force.

**(d) Counsel questions.** Is any function a medical device and of which
class? Does AIHGle 2.0 bind through licence conditions? Will HIA data
security requirements reach the consultancy?

## 15. Government clients: outside the PDPA, under the Public Sector (Governance) Act

**(a) Status and dates.**
- Public agencies (the Government, ministries, departments, organs of
  State, tribunals, gazetted statutory bodies) are excluded from the data
  protection provisions (P, Key Concepts). Since 1 February 2021 the
  exclusion covers public agencies only, not organisations acting on their
  behalf (S, *Iapps* decision summary via fork B2). Their service
  providers are organisations or data intermediaries (P), and a data
  intermediary of a public agency must notify it of a breach without
  undue delay (s 26E; P via Key Concepts fn 57).
- Public Sector (Governance) Act 2018 governs data sharing among agencies;
  the Public Sector (Governance) (Amendment) Act 2026 (No. 2 of 2026,
  passed 12 January 2026, assent 3 February 2026) adds data sharing and
  use directions and amends PDPA s 48C; in effect by 16 October 2026 per
  the SSO timeline (P, fork B2). Government ICT rules (IM8) and data
  classification flow down by contract (not read; `gap:`).
- Government AI guidance is mainly internal; GovTech's Agentic Risk &
  Capability Framework is cited in the agentic MGF (P, as a citation).

**(b) Triggers.** The client is a ministry, organ of state or gazetted
statutory board; the agent receives data shared under a public-sector
direction.

**(c) Paperwork.** Memo Roles: client outside the PDPA; consultancy's PDPA
status `counsel:`. Security questionnaire: s 26E breach notice; IM8 terms
`gap:`. `counsel_required: yes`.

**(d) Counsel questions.** Is the client a gazetted public agency? Is the
consultancy an organisation or data intermediary for each data set? Which
government data security terms apply?

## 16. Cybersecurity Act 2018 as amended in 2024

**(a) Status and dates (fork B2).** Key provisions of the Cybersecurity
(Amendment) Act 2024 commenced on 31 October 2025, checked 2026-10-26 (P,
CSA release): CII owners report qualifying incidents "within 2 hours of
becoming aware", now including suspected APT incidents; provider-owned
systems can be designated CII; systems of temporary cybersecurity concern.
Parts 3C (entities of special cybersecurity interest) and 3D (foundational
digital infrastructure) had not commenced (S).

**Reach to an agent vendor.** Only through a CII-owner client: contract
flow-down, and the owner's reporting of incidents on interconnected
supplier systems (S). The consultancy is not itself designated.

**(b) Triggers.** The client owns CII (energy, water, banking and finance,
healthcare, transport, infocomm, media, security and emergency services,
government) and the agent connects to a CII system.

**(c) Paperwork.** Security questionnaire: the owner's 2-hour clock and the
consultancy's notice sized to it (`counsel:`). Memo line only when the
trigger fires.

**(d) Counsel questions.** Is any connected system designated CII, and is
the consultancy's system "interconnected" with it? What do the client's CII
contract terms require?

## Not verified at a primary source

Re-read these before a reference file relies on them.

**PDPA text.** The consolidated SSO section bodies did not load; the
statutory wording here is as the PDPC quotes it in its guidelines. Not
read directly: s 4 (including the 2021 narrowing of the public-agency
exclusion, S), s 26D's own text, s 26E, s 48J and the Personal Data
Protection Regulations 2021. Provision-by-provision commencement dates of
the 2020 amendments (the SSO timeline shows only the dates). The
Personal Data Protection (Amendment) Regulations 2026 (S). The Second
Schedule sub-paragraph deleted by Act 19 of 2025. Data portability status
rests on the absence of a Part in the current SSO contents and the Key
Concepts guidelines, not on a statement.

**PDPC.** The NRIC guidelines (S); the Marina Bay Sands penalty (S); the
generative AI consultation launch date of 2 June 2026 (S); the Guide to
Managing Data Intermediaries (not read).

**Google Cloud.** Whether the pinned Gemini model's machine-learning
processing is listed in asia-southeast1 and which services are excluded
from data residency for Singapore. Read the model page and
<https://cloud.google.com/terms/data-residency> per project.

**Frameworks.** The LLM starter kit's version and date (image-only PDF);
the agentic testing kit's launch date and accredited testers; whether a
final CSA agentic addendum exists; ISAGO and Compendium dates.

**Legislation.** OSRAA's Act number and assent date and the full list of
13 harms; the elections amendment's commencement (22 January 2025, S);
Cybersecurity Act Parts 3C and 3D commencement; whether any AI bill was
introduced (the Parliament bills list was not searched).

**Sector.** Workplace Fairness (Dispute Resolution) Act number and assent;
any WFA commencement notification or subsidiary legislation; the TGFEP's
issue date; HSA GL-07-R2 full criteria; AIHGle 2.0 body text; the Health
Information Act's number, assent and penalties; MAS TPRM guidelines'
finalisation; the MAS Information Paper of December 2024 text.

## Must cover, should cover, mention only

**Must cover.** Every Singapore pack screens for these.

1. PDPA roles: client as organisation, consultancy as data intermediary
   under a written contract, Google as model provider; uses that break the
   intermediary role; the client's DPO and contact.
2. Consent, deemed consent (including by notification) and the exceptions
   per purpose, with the assessments the Regulations require kept.
3. Business improvement and research exceptions for development,
   evaluation and bias testing; AI-Specific Notification for any training
   or fine-tuning.
4. Notification, purpose, access and correction (30 days; RAG stores),
   accuracy, protection (prompts, outputs, agent activity data) and
   retention.
5. Transfer Limitation Obligation for consultancy access from Australia and
   any processing outside Singapore: contract specifying countries or a
   specified certification; written as a transfer annex row.
6. Data breach notification: data intermediary to client without undue
   delay; client assessment (30 days as a rule); PDPC within 3 calendar
   days; significant harm classes and the 500-person threshold.
7. PDPC AI guidelines (1 March 2024 and 20 July 2026) as the standard the
   input pack is measured against, including written policies and system
   cards.
8. No AI Act line (MDDI, 7 July 2026), and the penalty cap (10% of
   Singapore turnover above S$10 million).

**Should cover.** Screen when the trigger fires.

1. Agentic MGF v1.5 mapping in the impact assessment (any agent; promote to
   must if the client's reviewers ask for it).
2. Transparency Guidelines for Generative AI Chatbots (external chat
   agents).
3. MAS AI risk management guidelines, FEAT, TRM Notice clocks and
   outsourcing (financial clients).
4. Tripartite Guidelines now and the Workplace Fairness Act from its
   commencement (hiring and HR agents).
5. Do Not Call provisions (outbound voice, SMS or messaging marketing;
   synthetic voice included).
6. AIHGle 2.0, HSA SaMD guidance and the Health Information Act (health
   clients).
7. Public-agency status and s 26E (government clients; becomes must).
8. NRIC guidelines (agents that collect identity numbers).
9. IMDA starter kits for evaluation evidence; CSA AI security guidelines
   when the CISO asks.
10. Cybersecurity Act (CII-owner clients).

**Mention only.** One line in the memo, with `checked 2026-10-26`.

1. Data portability: not in force.
2. MGF 2020 and ISAGO; MGF for Generative AI 2024.
3. AI Verify, Project Moonshot and the assurance sandbox (unless asked).
4. Online Safety (Relief and Accountability) Act and the Online Safety
   Commission (public agents with user-visible outputs).
5. Elections deepfake prohibition (agents generating media of real people).
6. Online Criminal Harms Act.
7. MAS SAFR white paper and Project MindForge (not regulatory guidance).
8. PDPA amendments of 2025 and 2026 (narrow; no change for agent projects).
9. MAS TPRM guidelines and TRM Notice amendments (consultations).

## Screening checklist

Each trigger is a fact the brief or design records. A "yes" adds the law to
the regime screen and a section to the named document; where a legal
judgement is needed the line is `counsel:`.

| # | Trigger (fact with its ID) | Law | Document → section |
| --- | --- | --- | --- |
| 1 | Personal data of people in Singapore in prompts, tools, memory, logs or evaluation sets | PDPA Parts 3 to 6A | Memo → Singapore: PDPA and roles; input pack → Singapore: PDPA obligations check, data flows |
| 2 | Consultancy processes the client's data under a written contract | Data intermediary (s 4(2), (3)); AI RDS para 1.4; GenAI paras 8.1 and 7.4 | Memo → Roles; questionnaire → protection, retention, breach notice |
| 3 | Consultancy reuses client data outside the contract (cross-client evaluation, own tuning, analytics) | Loses intermediary status; all obligations | Memo → Roles (`counsel:`); input pack → purpose rows |
| 4 | A new or secondary purpose for existing data | s 15A deemed consent by notification; legitimate interests; business improvement | Input pack → PDPA obligations check with assessment IDs |
| 5 | Production data used to build, test, evaluate or debias | Business improvement or research exception | Input pack → exception rows; necessity (pseudonymisation) |
| 6 | Any training or fine-tuning on user data | GenAI guidelines para 4.4 (AI-Specific Notification) | Input pack → Notification and policy inputs |
| 7 | Web or forum data used, including behind a digital barrier | Publicly available exception; GenAI paras 3.4 to 3.7 | Input pack → written record or DPIA |
| 8 | Consultancy staff in Australia can see data, traces, logs or evaluation sets | Transfer Limitation Obligation (s 26; Regulations 2021) | Transfer annex → Singapore row; questionnaire → overseas access |
| 9 | Model processing, endpoint, grounding, abuse monitoring or telemetry outside Singapore | s 26; contract specifying countries or certification | Transfer annex; input pack → recipients and regions |
| 10 | Any personal data held | Part 6A breach notification (3 calendar days) | Questionnaire → incident response |
| 11 | NRIC, salary, account credentials or health data in scope | Significant-harm data classes; NRIC guidelines | Questionnaire → incident; input pack → necessity, masking contract |
| 12 | RAG store, memory or session history holding personal data | Access and correction (ss 21, 22); GenAI para 10.5 | Input pack → data flows (searchable by person) |
| 13 | Output feeds a decision about a person (credit, insurance, hiring, admission, benefits) | Accuracy (s 23); AI RDS notification and written policies; sector rules | System card → data, oversight; impact assessment; `counsel_required: yes` |
| 14 | Agent has write tools, payments, outbound messages, deletion or persistent memory | Agentic MGF dimensions 1 and 2 | Impact assessment → Agentic MGF mapping; system card → oversight |
| 15 | External, customer-facing chat agent | Chatbot transparency guidelines; agentic MGF §2.4 | System card → chatbot info card inputs, AI disclosure |
| 16 | Outbound marketing by voice (including synthetic voice), SMS or messaging to Singapore numbers | Do Not Call provisions (Parts 9, 9A) | System card → outbound channel; questionnaire → consent and register records |
| 17 | Client is MAS-regulated | MAS AI guidelines (from 7 October 2027 and 7 October 2028), FEAT, TRM Notice, Notice 658 | Memo → sector; impact assessment → materiality and FEAT; questionnaire → 1-hour clock, audit access; `counsel_required: yes` for customer decisions |
| 18 | Agent screens candidates, invites to interviews, appraises or feeds dismissal | TGFEP now; Workplace Fairness Act (expected end-2027); PDPA evaluative purpose | Impact assessment → adverse impact; system card → final decision owner; `counsel_required: yes` |
| 19 | Clinical summarising, triage or decision support; NEHR | HSA SaMD; AIHGle 2.0; Health Information Act (early 2027) | Memo → medical device screen; `counsel_required: yes` |
| 20 | Client is a ministry, organ of state or statutory board | Public-agency exclusion; s 26E; Public Sector (Governance) Act | Memo → Roles; questionnaire → breach notice to agency; `counsel_required: yes` |
| 21 | Client owns CII and the agent connects to it | Cybersecurity Act (2-hour clock) | Questionnaire → incident response |
| 22 | Public agent with user-visible or generated content about real people | OSRAA; elections deepfake rules | Memo → mention; impact assessment → synthetic media rows |

## Checker patterns

**Date check (law references the `LEGAL_REF` pattern should recognise).**
The current pattern already catches "Act 2012" through `Act\s(?:19|20)\d\d`,
"Schedule", "Code", "Standard" and section references like "s 26D". Add:

- `PDPA`, `PDPC`, `Personal Data Protection Act`, `Personal Data Protection
  (?:\(Amendment\) )?Regulations`, `Notification of Data Breaches`,
  `Do Not Call`, `DNC`;
- `MAS`, `FEAT`, `TRM`, `FSM-N\d+`, `Notice \d{3,4}` (658, 1121),
  `Guidelines on Artificial Intelligence Risk Management`;
- `AIHGle`, `HSA`, `GL-0\d`, `Health Information Act`;
- `Workplace Fairness`, `WFA`, `TGFEP`, `Tripartite Guidelines`;
- `Cybersecurity Act`, `OSRAA`, `Online Safety \(Relief and Accountability\)`,
  `Online Criminal Harms Act`, `Elections \(Integrity of Online Advertising\)`,
  `Public Sector \(Governance\)`;
- `MGF`, `Model AI Governance Framework`, `Starter Kit`, `Transparency
  Guidelines for Generative AI Chatbots`.

Dates the checker will meet in Singapore drafts, all to carry `checked
2026-10-26`: "1 February 2021" and "1 October 2022" (PDPA amendments), "7
October 2027" and "7 October 2028" (MAS AI guidelines), "10 May 2024"
(FSM-N05), "11 December 2024" (outsourcing), "29 June 2026" (Online Safety
Commission), "31 October 2025" (Cybersecurity amendments), "10 March 2026"
(AIHGle 2.0). Two expected dates are not applicability dates and should be
written without a day so the checker does not demand a check: "end-2027"
(Workplace Fairness Act, MOM target) and "early 2027" (Health Information
Act).

**Phrases that should force `counsel_required: yes`** (in addition to the
existing employment, credit, insurance, health and biometric patterns,
which already fire on Singapore facts):

- public-body clients: `statutory board`, `public agency` (with
  Singapore), `organ of state`, `ministry` (with Singapore);
- financial: `MAS-regulated`, `material outsourc(?:ing|ed)`,
  `outsourced relevant service`, `underwriting`;
- health: `NEHR`, `HCSA licensee`, `clinical decision support` (exists);
- employment: `work pass`, `job advertisement`, `evaluative purpose`;
- identity: `NRIC`, `FIN number`;
- infrastructure: `critical information infrastructure` (exists), `CII
  owner`;
- online harms: `election advertising`, `inauthentic material`.

Negation handling stays as is: a screening-table row that says "n/a:
not MAS-regulated" must not fire.

## How Singapore differs from Australia in ways that change a draft

| Topic | Australia | Singapore | What changes in the draft |
| --- | --- | --- | --- |
| Roles | No controller or processor; the consultancy is an APP entity in its own right unless exempt | Organisation and data intermediary; the consultancy is usually a data intermediary with three obligations, and the client is liable for its processing (s 4(3)) | Singapore Roles section uses "organisation" and "data intermediary", names the written contract, and lists uses that break the role. Never write "APP entity" or "controller" in Singapore sections |
| Basis for processing | No lawful-basis test; APP 3, 5, 6 | Consent by default; deemed consent (conduct, contractual necessity, notification) and Schedule exceptions, each with kept assessments | A per-purpose consent-or-exception table with assessment IDs; no GDPR lawful basis, no APP analysis |
| AI development on held data | APP 6 secondary use; the OAIC recommends consent or opt-out | Statutory business improvement and research exceptions, which the PDPC applies to AI testing and debiasing; fresh consent for generative AI training that is a "significant departure" | Exception rows with their two conditions as facts; AI-Specific Notification for fine-tuning |
| Automated decisions | APP 1.7 to 1.9 from 10 December 2026: privacy-policy entries, human review no exemption | No automated-decision provision; the PDPC recommends notification of influential features and written policies on oversight, proportionate to impact and autonomy | No APP 1.7 table; the system card's disclosure becomes "PDPC recommended disclosures" and is advice, not a duty. Sector rules (MAS, WFA) carry the decision duties |
| Assessment | PIA mandatory only for Commonwealth agencies; OAIC ten steps | DPIA encouraged (PDPC six phases), never mandatory; mandatory written assessments for deemed consent by notification and legitimate interests | Input pack screening says "DPIA encouraged"; the required assessments are the s 15A and legitimate interests ones |
| Overseas | APP 8 and s 16C; use or disclosure test; facts in the input pack | Transfer Limitation Obligation on the client even for its intermediary's transfers; contract must specify countries; Global or APEC CBPR/PRP certifications count; no adequacy list | Write a transfer annex row for Singapore, including consultancy access from Australia; template's "must include eu or uk" needs `sg` |
| Breach clock | Assess within 30 days; notify "as soon as practicable" | Data intermediary to client without undue delay; assess (30 days as a rule); PDPC within 3 calendar days; 500-person threshold | Questionnaire shows both clocks and the consultancy's notice term |
| Penalties | Greater of $50 million, three times benefit or 30% of adjusted turnover | Greater of S$1 million or 10% of Singapore turnover (above S$10 million) | One memo line |
| Access | APP 12 | 30 days to respond or say when; RAG stores in scope; preserve rejected-request data 30 days | Store-by-store access path with the 30-day figure |
| DPO and contact | No statutory privacy officer for organisations | Mandatory DPO with published business contact details, ideally a Singapore number during Singapore business hours | Memo Roles and system card Contact name the client's DPO |
| Marketing calls | Do Not Call Register Act; Spam Act | PDPA Do Not Call provisions; synthetic voice expressly a "voice call"; 21-day check validity | Outbound channel row cites PDPA Parts 9 and 9A |
| Sensitive data | Statutory "sensitive information" with consent under APP 3.3 | No statutory special category; NRIC restrictions and breach "significant harm" data classes do similar work | Write "data classes deemed significant harm" and NRIC handling, not "sensitive information" |
| AI governance | Guidance for AI Adoption (AI6); DTA policy for Commonwealth clients | IMDA agentic MGF v1.5, chatbot transparency guidelines, starter kits, all voluntary | Impact assessment "Singapore: Agentic MGF mapping" instead of the AI6 mapping |
| Government clients | Agencies bound by the Privacy Act and APP Code; DTA assessment | Public agencies outside the PDPA; contractors still under it; s 26E breach notice to the agency | Roles say the client is outside the PDPA and the consultancy is not |
| Employment data | Employee records exemption for the client (not the consultancy) | No employee exemption; employment purposes handled by notification (s 20(4)) and exceptions; TGFEP and WFA for decisions | No exemption line; an employment notification row; adverse-impact section on WFA characteristics |
| Terms | Personal information, sensitive information, APP entity, eligible data breach, PIA, overseas recipient | Personal data, organisation, data intermediary, notifiable data breach, DPIA, transfer, deemed consent, business improvement exception | Singapore sections use Singapore terms |
