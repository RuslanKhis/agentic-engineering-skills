# United Kingdom: privacy and AI law for the governance pack

*Read 26 October 2026. Research for adding the UK to
`skills/adk-governance-pack`. Drafts, not legal advice.*

Every source below was read on 26 October 2026 unless a row says otherwise.
(P) marks a primary source (legislation.gov.uk, ico.org.uk, gov.uk,
fca.org.uk, Parliament, the European Commission, ETSI). (S) marks a
secondary source (law-firm notes, trade press), used only where no primary
page could be read, and said so.

## Conclusion

The UK has no AI Act and, as of today, no AI bill. The King's Speech of
13 May 2026 announced none, checked 2026-10-26 (P). AI is governed
through existing law and sector regulators. A UK "classification memo" is
therefore a **regime screen**, like the Australian one: which laws and
regulator expectations the agent falls under, triggered by facts the
design already records.

UK data protection law now differs from the EU GDPR in ways that change the
pack's templates. The Data (Use and Access) Act 2025 (DUAA) made the
changes. The ICO says "all data protection provisions" of the DUAA are in
force as of 19 June 2026 (P). What changes the pack:

1. **Article 22 is replaced by Articles 22A to 22D, in force since
   5 February 2026, checked 2026-10-26** (P). A significant decision based
   solely on automated processing is now allowed on any lawful basis,
   provided the Article 22C safeguards are in place: information about the
   decision, the chance to make representations, human intervention, and
   the right to contest. The old prohibition survives only where special
   category data is used (Article 22B), and where the basis is a
   recognised legitimate interest. "Solely automated" means "no meaningful
   human involvement" (Article 22A). The DPIA pack therefore needs an
   **ADM safeguards** section, not just an Article 22 yes or no.
2. **DPIAs, records of processing and DPOs are unchanged in substance.**
   The DPIA, records and DPO changes in the old Data Protection and Digital
   Information Bill were not carried into the DUAA. Articles 30, 35 and 37
   carry only a word change ("Commissioner" became "Commission") on
   30 September 2026 (P). The EU-shaped DPIA and Article 30 templates still
   fit. What changes is the content: lawful bases, ADM, transfers, the
   regulator's name and the ICO's own DPIA list.
3. **The regulator is now the Information Commission.** The office of
   Information Commissioner was abolished on 30 September 2026, checked
   2026-10-26 (SI 2026/1015, P). UK GDPR references now read
   "Commission". Drafts should name the Information Commission, adding
   "(formerly the ICO)". The ico.org.uk site and guidance continue.
4. **Transfers use the "data protection test".** The protection must be
   "not materially lower" than UK law, assessed "acting reasonably and
   proportionately" (Articles 44A to 47A, in force 5 February 2026, P).
   **Australia has no UK adequacy regulations** (ICO, P). So whenever the
   Australian consultancy's staff or systems access UK personal data from
   Australia, that is a restricted transfer. It needs the IDTA or the
   Addendum plus a documented data protection test (the ICO still calls
   this a TRA). For an Australian-based agency this is the most common
   UK trigger.
5. **New controller duties a DPIA should point to.** These are:
   - a complaints process (acknowledge within 30 days), in force
     19 June 2026 (P);
   - subject access limited to a "reasonable and proportionate search",
     treated as in force from 1 January 2024 (P);
   - a new Article 12A time-limit regime with a clarification pause, from
     5 February 2026 (P);
   - "children's higher protection matters" in data protection by design
     for services likely to be accessed by children, from 5 February 2026
     (P).
6. **PECR cookie exceptions widened, and fines raised to UK GDPR levels.**
   Analytics and appearance or functionality cookies may be set without
   consent if users get clear information and a simple, free way to
   object. Breaches of regulations 5 to 8, 14 and 19 to 24 now fall under
   the DPA 2018 higher maximum: £17.5 million or 4% of worldwide turnover.
   Both changes are in force from 5 February 2026 (P). This matters when
   the agent's web front end sets cookies or the agent sends marketing.
7. **The ICO's AI rulebook is in motion, not settled.** As of today:
   - the draft ADM and profiling guidance was consulted on from
     31 March 2026 to 29 May 2026, with the final due "Winter 2026" (P);
   - a statutory AI and ADM code of practice is required by SI 2026/425,
     in force 12 May 2026 (P);
   - an agentic AI call for evidence is open from 8 October 2026 to
     20 November 2026 (P);
   - the 2023 AI and data protection guidance, the DPIA guidance and the
     worker-monitoring guidance all carry "under review" banners because
     of the DUAA (P).

   Drafts should cite these with their status and date, and treat the
   older guidance as still the ICO's published view.
8. **Equality Act 2010, Online Safety Act 2023, consumer law and the FCA
   are conditional add-ons:**
   - **Equality Act:** always relevant to employment or service decisions.
     The public sector equality duty applies for public-sector clients.
   - **Online Safety Act:** applies only if users can share agent outputs
     with each other, or the agent searches multiple sites or databases.
   - **Consumer law:** the DMCC Act and the CMA's guidance of 9 March 2026
     on AI agents apply to consumer-facing agents.
   - **FCA:** applies to regulated financial firms. There are no
     AI-specific rules; the Consumer Duty and the Senior Managers and
     Certification Regime (SM&CR) apply.
9. **Public-sector clients:** for central government departments and
   in-scope arm's-length bodies, an **Algorithmic Transparency Recording
   Standard (ATRS) record** is mandatory for tools in Beta, Pilot or
   Production that significantly influence decisions with public effect
   or interact with the public (P). This is a new document the pack can
   draft from the system card.
10. **Voluntary security baseline.** The DSIT Code of Practice for the
    Cyber Security of AI (31 January 2025) is now a European Standard,
    ETSI EN 304 223 V2.1.1 (2025-12) (P). Its 13 principles map well onto
    the security questionnaire. The AI Management Essentials tool was
    **not** published: DSIT decided against it (P).

## Sources

### Primary: legislation (legislation.gov.uk)

| Source | Status on 26 Oct 2026 | Used for |
| --- | --- | --- |
| Data (Use and Access) Act 2025 c. 18, s. 70 <https://www.legislation.gov.uk/ukpga/2025/18/section/70> | Fully in force 5 Feb 2026 (SI 2026/82 reg. 2(c)) | Art. 6(1)(ea) recognised legitimate interest; Art. 6(11) legitimate-interest examples |
| DUAA Sch. 4 <https://www.legislation.gov.uk/ukpga/2025/18/schedule/4> | In force 5 Feb 2026 | Annex 1 recognised legitimate interests |
| DUAA s. 71 <https://www.legislation.gov.uk/ukpga/2025/18/section/71> | In force 5 Feb 2026 | Art. 8A compatible further processing |
| DUAA s. 74 <https://www.legislation.gov.uk/ukpga/2025/18/section/74> | In force 20 Aug 2025 (SI 2025/904) | Art. 11A power to add special categories (no regulations seen) |
| DUAA s. 76 <https://www.legislation.gov.uk/ukpga/2025/18/section/76> | In force 5 Feb 2026 (reg. 2(h)) | Art. 12A time limits; clarification pause |
| DUAA s. 78 <https://www.legislation.gov.uk/ukpga/2025/18/section/78> | In force at Royal Assent; treated as in force from 1 Jan 2024 | Art. 15(1A) reasonable and proportionate search |
| DUAA s. 80 <https://www.legislation.gov.uk/ukpga/2025/18/section/80> | In force 5 Feb 2026 (reg. 2(j)) | Arts. 22A to 22D |
| DUAA s. 81 <https://www.legislation.gov.uk/ukpga/2025/18/section/81> | In force 5 Feb 2026 (reg. 2(k)) | Art. 25(1A), (1B) children's higher protection matters |
| DUAA s. 103 <https://www.legislation.gov.uk/ukpga/2025/18/section/103> | In force 19 Jun 2026 (SI 2026/82 reg. 3(a)) | DPA 2018 ss. 164A, 164B complaints; UK GDPR Art. 77 omitted |
| DUAA Sch. 7 <https://www.legislation.gov.uk/ukpga/2025/18/schedule/7> | In force 5 Feb 2026 (reg. 2(z9)) | Arts. 44A, 45A to 45C, 46(1A), 47A |
| DUAA Sch. 12 <https://www.legislation.gov.uk/ukpga/2025/18/schedule/12> | In force 5 Feb 2026 (reg. 2(z13)) | PECR Sch. A1 cookie exceptions |
| DUAA Sch. 13 <https://www.legislation.gov.uk/ukpga/2025/18/schedule/13> | In force 5 Feb 2026 (reg. 2(z14)) | PECR enforcement through DPA 2018 s. 157 |
| PECR 2003 Sch. 1 para. 18 as amended <https://www.legislation.gov.uk/uksi/2003/2426/schedule/1> | Current | Modified s. 157(2)(a) listing regs. 5 to 8, 14, 19 to 24 |
| DPA 2018 s. 157 <https://www.legislation.gov.uk/ukpga/2018/12/section/157> | Current | Higher maximum £17.5m or 4%; standard maximum £8.7m or 2% |
| SI 2026/82, DUAA (Commencement No. 6 and Transitional and Saving Provisions) Regulations 2026, reg. 2 <https://www.legislation.gov.uk/uksi/2026/82/regulation/2/made> and reg. 3 <https://www.legislation.gov.uk/uksi/2026/82/regulation/3/made> | Made 29 Jan 2026 | Main Part 5 commencement 5 Feb 2026; s. 103 on 19 Jun 2026 |
| SI 2026/1015, DUAA (Commencement No. 9 ...) Regulations 2026 <https://www.legislation.gov.uk/uksi/2026/1015/made> | Made 10 Sep 2026 | Information Commission from 30 Sep 2026 |
| SI 2026/386, DUAA (Consequential Amendments and Transitional Provision) Regulations 2026 <https://www.legislation.gov.uk/uksi/2026/386/body/made> | Made 26 Mar 2026 | "Commissioner" to "Commission" throughout |
| SI 2026/425, DPA 2018 (Code of Practice on AI and ADM) Regulations 2026 <https://www.legislation.gov.uk/uksi/2026/425/made> | In force 12 May 2026 | Duty to prepare a statutory AI and ADM code |
| UK GDPR Art. 30 <https://www.legislation.gov.uk/eur/2016/679/article/30>, Art. 35 <https://www.legislation.gov.uk/eur/2016/679/article/35>, Art. 37 <https://www.legislation.gov.uk/eur/2016/679/article/37> | Current revised text | No substantive DUAA change, only "Commission" from 30 Sep 2026 (Art. 37(1)(a) adds "and tribunals") |
| Equality Act 2010 s. 19 <https://www.legislation.gov.uk/ukpga/2010/15/section/19>, s. 149 <https://www.legislation.gov.uk/ukpga/2010/15/section/149> | Current | Indirect discrimination; public sector equality duty |
| Crime and Policing Act 2026 c. 20, s. 248 <https://www.legislation.gov.uk/ukpga/2026/20/section/248> | In force at Royal Assent (29 Apr 2026) | New OSA s. 216A power over AI services |

### Primary: ICO (ico.org.uk)

| Source | Date shown | Used for |
| --- | --- | --- |
| DUAA: what does it mean for organisations? <https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-what-does-it-mean-for-organisations/> | Updated 19 Jun 2026 | "All data protection provisions ... now in force"; summary of changes |
| DUAA summary: data protection <https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/data-protection/> and PECR <https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/privacy-and-electronic-communications/> | 19 Jun 2025 to 19 Jun 2026 | Change summaries |
| Draft ADM guidance <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/automated-decision-making/> and subpages "What does the UK GDPR say about ADM?" and "What else do we need to consider?" | Draft, 31 Mar 2026 | Meaningful human involvement; DPIA "should" for any ADM |
| ADM consultation page <https://ico.org.uk/about-the-ico/ico-and-stakeholder-consultations/2026/03/ico-consultation-on-the-draft-guidance-about-automated-decision-making-including-profiling/> | 31 Mar to 29 May 2026, closed | Status |
| Guidance on AI and data protection <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/> and accountability chapter <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/what-are-the-accountability-and-governance-implications-of-ai/> | Updated 15 Mar 2023; "under review" | AI DPIA contents; roles |
| Generative AI consultation response: controllership <https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/allocating-controllership-across-the-generative-ai-supply-chain/>; accuracy <https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/accuracy-of-training-data-and-model-outputs/>; web scraping <https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/the-lawful-basis-for-web-scraping-to-train-generative-ai-models/> | Dec 2024 (index page undated) | Deployer positions |
| AI and biometrics strategy news <https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2025/06/information-commissioner-people-must-trust-their-data-is-protected-in-the-age-of-ai/>; update March 2026 <https://ico.org.uk/about-the-ico/our-information/our-strategies-and-plans/artificial-intelligence-and-biometrics-strategy/ai-and-biometrics-strategy-update-march-2026/> | 5 Jun 2025; Mar 2026 | Strategy and progress |
| ICO Tech Futures: agentic AI, risks page <https://ico.org.uk/about-the-ico/research-reports-impact-and-evaluation/research-and-reports/technology-and-innovation/tech-horizons-and-ico-tech-futures/ico-tech-futures-agentic-ai/data-protection-and-privacy-risks> | Jan 2026 (per strategy update) | Ten agentic risks for the DPIA risk table |
| Agentic AI call for evidence <https://ico.org.uk/about-the-ico/ico-and-stakeholder-consultations/2026/10/agentic-ai-call-for-evidence/>; news <https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2026/10/ico-secures-changes-from-leading-ai-developers-as-scrutiny-extends-to-ai-agents/> | 8 Oct to 20 Nov 2026, open | Agentic AI status |
| Plans for guidance: general <https://ico.org.uk/about-the-ico/what-we-do/our-plans-for-new-and-updated-guidance/general-data-protection/>; technology <https://ico.org.uk/about-the-ico/what-we-do/our-plans-for-new-and-updated-guidance/technology/> | Undated | Agentic AI guidance due Spring 2027; foundation models Autumn 2026; monitoring workers Winter 2026/2027; SARs generated by AI Winter 2026 |
| DPIA: examples of processing likely to result in high risk <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/examples-of-processing-likely-to-result-in-high-risk/>; when do we need a DPIA <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/when-do-we-need-to-do-a-dpia/> | "Under review" | ICO DPIA list |
| Monitoring workers <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/monitoring-workers/> and "Data protection and monitoring workers" subpage | "Under review" | DPIA, transparency, consultation of workers |
| AI tools in recruitment audit outcomes <https://ico.org.uk/action-weve-taken/audits-and-overview-reports/2024/11/ai-tools-used-in-recruitment/> | 6 Nov 2024 | Recruitment expectations (search extract only) |
| Automated hiring decisions news <https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2026/03/automated-decisions-can-streamline-the-hiring-process-with-the-right-safeguards-in-place/> | 31 Mar 2026 | Recruitment ADM expectations |
| Recognised legitimate interest guidance <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/recognised-legitimate-interest/> | 23 Mar 2026 (search extract) | Status |
| How to deal with data protection complaints <https://ico.org.uk/for-organisations/how-to-deal-with-data-protection-complaints/> | Published 12 Feb 2026, updated 8 May 2026 | Complaints duties |
| Adequacy regulations: is the restricted transfer covered? <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/adequacy-regulations/is-the-restricted-transfer-covered-by-adequacy-regulations/> | Undated | Adequacy list; no Australia |
| Final storage and access technologies guidance news <https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2026/04/final-storage-and-access-technologies-guidance-published/> | 29 Apr 2026 (search extract) | Cookie guidance status |

### Primary: government, regulators, Parliament, EU, ETSI

| Source | Date shown | Used for |
| --- | --- | --- |
| DUAA plans for commencement <https://www.gov.uk/guidance/data-use-and-access-act-2025-plans-for-commencement> | Updated 12 Oct 2026 | Stage table |
| The King's Speech 2026 <https://www.gov.uk/government/speeches/the-kings-speech-2026> | 13 May 2026 | No AI bill |
| AI Opportunities Action Plan <https://www.gov.uk/government/publications/ai-opportunities-action-plan/ai-opportunities-action-plan> | 13 Jan 2025 | Regulation recommendations 23 to 29 |
| AI Opportunities Action Plan: One Year On <https://www.gov.uk/government/publications/ai-opportunities-action-plan-one-year-on/ai-opportunities-action-plan-one-year-on> | Jan 2026 (search extract) | 38 of 50 actions met |
| Tackling AI security risks (AISI rename) <https://www.gov.uk/government/news/tackling-ai-security-risks-to-unleash-growth-and-deliver-plan-for-change> | 14 Feb 2025 (search extract) | AI Security Institute name |
| Code of Practice for the Cyber Security of AI <https://www.gov.uk/government/publications/ai-cyber-security-code-of-practice/code-of-practice-for-the-cyber-security-of-ai> | 31 Jan 2025 | 13 principles; roles |
| ETSI press release <https://www.etsi.org/newsroom/press-releases/2627-etsi-releases-world-leading-standard-for-securing-ai/>; EN 304 223 V2.1.1 (2025-12) <https://www.etsi.org/deliver/etsi_en/304200_304299/304223/02.01.01_60/en_304223v020101p.pdf> | Jan 2026; Dec 2025 (search extracts, PDF not opened) | Standard status |
| AIME government response <https://www.gov.uk/government/consultations/ai-management-essentials-tool/outcome/guidance-for-using-the-ai-management-essentials-tool-government-response> | Updated 6 Feb 2026 | AIME not published |
| ATRS mandatory scope and exemptions policy <https://www.gov.uk/government/publications/algorithmic-transparency-recording-standard-mandatory-scope-and-exemptions-policy/algorithmic-transparency-recording-standard-atrs-mandatory-scope-and-exemptions-policy> | 17 Dec 2024 | Who, which tools, when |
| DSIT data regulation in the age of AI call for evidence <https://www.gov.uk/government/calls-for-evidence/data-regulation-in-the-age-of-ai-and-other-data-intensive-technologies/data-regulation-in-the-age-of-ai-and-other-data-intensive-technologies> | 15 Jul to 9 Sep 2026 | Possible further UK GDPR reform |
| Responsible AI in Recruitment (DSIT) <https://www.gov.uk/government/publications/responsible-ai-in-recruitment-guide/responsible-ai-in-recruitment> | 25 Mar 2024 | Recruitment assurance mechanisms |
| EHRC, AI: meeting the PSED <https://www.equalityhumanrights.com/guidance/artificial-intelligence-meeting-public-sector-equality-duty-psed> | 1 Sep 2022 | PSED expectations |
| PM news on AI chatbots and the OSA <https://www.gov.uk/government/news/pm-no-platform-gets-a-free-pass-government-takes-action-to-keep-children-safe-online> | 15 Feb 2026 | Chatbot loophole policy |
| Online Safety Act explainer <https://www.gov.uk/government/publications/online-safety-act-explainer/online-safety-act-explainer> | Updated 24 Apr 2025 | OSA duties and dates |
| Ofcom open letter on generative AI and chatbots <https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/open-letter-to-uk-online-service-providers-regarding-generative-ai-and-chatbots> | Nov 2024 | **Returned HTTP 403**; content from search extracts only |
| CMA, Complying with consumer law when using AI agents <https://www.gov.uk/government/publications/complying-with-consumer-law-when-using-ai-agents/complying-with-consumer-law-when-using-ai-agents> | 9 Mar 2026 | Deployer expectations |
| CMA, Agentic AI and consumers <https://www.gov.uk/government/publications/agentic-ai-and-consumers/agentic-ai-and-consumers> | 9 Mar 2026 | Risks; foundation-model principles still relevant |
| CMA, new consumer protection regime news <https://www.gov.uk/government/news/cma-to-boost-consumer-and-business-confidence-as-new-consumer-protection-regime-comes-into-force> | Apr 2025 (search extract) | DMCC direct enforcement, 10% fines |
| CMA AI Foundation Models update paper <https://assets.publishing.service.gov.uk/media/661941a6c1d297c6ad1dfeed/Update_Paper__1_.pdf> | 11 Apr 2024 (not opened) | Principles named in the CMA's 2026 paper |
| Report on Copyright and AI <https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence> | 18 Mar 2026 (first 100k characters read) | TDM exception position |
| Employment Rights Act timeline <https://www.gov.uk/government/publications/implementing-the-plan-to-make-work-pay-and-employment-rights-act/plan-to-make-work-pay-and-employment-rights-act-timeline-update> | Updated 22 Oct 2026 | Dates; AI blacklist ban |
| FCA blog, AI in financial services <https://www.fca.org.uk/news/blogs/ai-financial-services-approach> | 8 Jun 2026 | No AI-specific rules |
| FCA, Mills Review press release <https://www.fca.org.uk/news/press-releases/fca-publishes-landmark-review-impact-ai-retail-financial-services> | 6 Jul 2026 | Seven recommendations |
| European Commission adequacy page <https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en>; Implementing Decision (EU) 2025/2574 <https://eur-lex.europa.eu/eli/dec_impl/2025/2574/oj/eng> | 19 Dec 2025 (search extracts) | EU-to-UK adequacy renewed |
| Cyber Security and Resilience (NIS) Bill, Lords second reading Hansard <https://hansard.parliament.uk/Lords/2026-07-14/debates/29073BC1-AD49-48CF-A269-8E83A76AFE90/details> | 14 Jul 2026 (search extract) | MSP scope, still a bill |

### Secondary (used only where noted)

| Source | Used for |
| --- | --- |
| Bratby Law, SI 2026/425 note <https://bratby.law/ico-ai-biometrics-code-of-practice/> | Code timeline estimate (2027 earliest); SI facts re-checked at legislation.gov.uk |
| IAPP, King's Speech, no AI bill <https://iapp.org/news/a/king-s-speech-signals-diffuse-uk-digital-policy-agenda-but-no-ai-bill>; Bird & Bird <https://www.twobirds.com/en/insights/2026/ai-in-the-kings-speech-2026-regulating-for-growth-bill-announced> | Context only; the speech text is primary |
| The Register on the "ICO" name continuing <https://www.theregister.com/a/5300439> | Branding only |
| Mishcon de Reya, cookie fines <https://www.mishcon.com/news/fines-for-cookie-contraventions-more-likely-as-a-result-of-law-change> | Removal of the "serious contravention" threshold (not checked against PECR reg. 31 text) |
| Freeths, EU renewal to 27 Dec 2031 <https://www.freeths.co.uk/insights-events/legal-articles/2026/european-commission-renews-uk-adequacy-decisions-until-27-december-2031/> | Expiry date (the Commission draft decision says six years) |
| Digital Policy Alert, s. 103 commencement <https://digitalpolicyalert.org/event/40956-data-use-and-access-act-2025-commencement-no-6-and-transitional-and-saving-provisions-regulations-2026-section-103-data-protection-complaints-including-data-protection-regulation-enter-into-force> | Corroboration only |

## 1. UK GDPR and the DPA 2018 as amended by the DUAA

### 1.0 Commencement: what is in force today

The DUAA received Royal Assent on 19 June 2025 (P, ICO summary
"originally published 19 June 2025"; gov.uk plan). Data protection
provisions came in four stages (P, gov.uk commencement plan, updated
12 October 2026; SIs as listed):

| Date (checked 2026-10-26) | Instrument | What commenced |
| --- | --- | --- |
| 19 June 2025 (Royal Assent) | DUAA s. 142 | s. 78 (subject access search, treated as in force from 1 January 2024); some sections for regulation-making purposes |
| 20 August 2025 | SI 2025/904 (Commencement No. 1) | s. 74 (power to add special categories); parts of ss. 72 and 110; ICO objectives; copyright report duties |
| 5 February 2026 | SI 2026/82 reg. 2 (Commencement No. 6) | Most of Part 5: ss. 67, 68, 70, 71, 72, 73, 75, 76, 77, 80, 81, 83, 85 to 87, 94, 98 to 101, 105, 110, 112, 114 to 116, 120, 121, 130, 132, 133(4); Schs. 4 to 9, 11 (except para. 32), 12, 13, 15. This includes ADM, recognised legitimate interests, transfers, the PECR cookie and fine changes, and children's higher protection matters |
| 31 March 2026 | SI (Commencement No. 8) | Sch. 11 para. 32: new erasure ground, Art. 17(1)(g), for data processed because of a malicious unfounded allegation (gov.uk plan) |
| 19 June 2026 | SI 2026/82 reg. 3 | s. 103 and Sch. 10: complaints to controllers |
| 30 September 2026 | SI 2026/1015 (Commencement No. 9) and SI 2026/386 | ss. 117(4)(a), 118, 119: Information Commissioner abolished, functions move to the Information Commission; "Commission" substituted throughout UK GDPR |

Not yet commenced, or with no date found: the ICO governance changes beyond
the Commission itself (P, gov.uk plan) and the National Underground Asset
Register. Neither affects the pack.

### 1.1 Automated decision-making: Articles 22A to 22D

**(a) Status.** In force since 5 February 2026, checked 2026-10-26 (P,
s. 80; SI 2026/82 reg. 2(j)). The ICO's ADM guidance is still a draft.
It was consulted on from 31 March 2026 to 29 May 2026, and the final is
due "Winter 2026" (P). The pre-DUAA guidance stays available as a PDF
until then (P).

What the law says (P, s. 80):

- **Article 22A.** A decision is "based solely on automated processing"
  if there is "no meaningful human involvement in the taking of the
  decision". When judging that, the controller must consider how far the
  decision is reached by means of profiling. A decision is "significant"
  if it produces a legal effect or a similarly significant effect.
- **Article 22B.** A significant decision based wholly or partly on
  special category data may not be solely automated unless one of two
  conditions holds:
  - the person gave explicit consent; or
  - the decision is necessary for a contract or required or authorised by
    law, and Article 9(2)(g) applies.

  Separately, no solely automated significant decision may rest on
  Article 6(1)(ea), the recognised legitimate interest basis.
- **Article 22C.** Safeguards are required for every solely automated
  significant decision. They must:
  - give the person information about such decisions;
  - let them make representations;
  - let them obtain human intervention by the controller;
  - let them contest the decision.
- **Article 22D.** The Secretary of State may, by affirmative regulations,
  say what is or is not meaningful human involvement or a similarly
  significant effect, and add safeguards. No regulations were found.

The ICO's draft guidance (P, 31 March 2026):

- **Meaningful human involvement.** The reviewer must act at a point where
  they can change the outcome and must have the authority and discretion
  to do so. They must be "suitably trained and qualified to understand the
  system's logic, outputs, limitations, and risks". "Using ad hoc
  spot-checking isn't sufficient." Building or designing the system does
  not count as involvement. Organisations should record how the human was
  involved.
- **Significant effects** include effects on finances, employment, health,
  education, housing, essential services, reputation, behaviour or
  choices. When unsure, "apply the safeguards to all decisions".
- **DPIA.** You "must" do one for systematic and extensive profiling with
  significant effects. You "should do a DPIA for any ADM as this is very
  likely to be a type of processing that can result in high risk".
- **Testing.** You "should" check systems are working as intended and
  find inaccuracies or bias, for example by manually reviewing a sample of
  decisions. Monitoring statistical accuracy is not human intervention.

**(b) Triggers.**

- The agent's output alone decides, or the human reviewer only spot-checks
  or rubber-stamps, and the decision affects someone's job, money, access
  to a service, housing, education, health or reputation.
- Agent output is used in a decision about a UK employee or candidate:
  shortlisting, performance, scheduling, discipline.
- The decision uses special category data, or the agent may infer it from
  free text. This engages Article 22B.
- The lawful basis proposed for the decision is a recognised legitimate
  interest. This is barred for solely automated significant decisions.

**(c) Paperwork.**

- **DPIA input pack, new "ADM and safeguards (UK GDPR Articles 22A to
  22D)" section.** It records:
  - where a person decides, citing the contract ID;
  - who that person is, their training, their authority to change the
    outcome, and what information they see;
  - what share of decisions they review (an M record), noting that
    sampling alone fails the ICO test;
  - whether special category data is used or could be inferred, and the
    masking contract with its measured coverage;
  - how each of the four Article 22C safeguards is delivered: the notice
    text, the representation channel, the human-review route and the
    contest route.
- **System card.** It holds the person-facing ADM information (the
  Article 22C(2)(a) notice) and the human-review route.
- **Records of processing.** A column, or a note, records "solely
  automated significant decision: yes or no, safeguards reference".

**(d) Counsel only.**

- Is the decision "significant"?
- Is human involvement "meaningful" on these facts?
- Which Article 6 basis applies?
- If special category data is involved, does explicit consent or the
  Article 22B(3)(b) condition hold?
- Should the client adopt the ICO draft's expectations before the final
  guidance?

### 1.2 Recognised legitimate interests and legitimate-interest examples

**(a) Status.** In force since 5 February 2026, checked 2026-10-26 (P,
s. 70, Sch. 4). ICO guidance was published on 23 March 2026 (P, search
extract).

- **The new basis.** Article 6(1)(ea) applies where processing is
  necessary for a purpose in Annex 1. There is no balancing test, but the
  processing must still be necessary. Annex 1 lists:
  - disclosure to a requester who states it needs the data for an
    Article 6(1)(e) public task;
  - national security, public security and defence;
  - emergencies;
  - crime;
  - safeguarding a vulnerable individual (a person under 18, or an adult
    "at risk").
- **Legitimate-interest examples.** New Article 6(11) gives examples of
  processing that may be necessary for an Article 6(1)(f) legitimate
  interest: direct marketing; intra-group transmission for internal
  administrative purposes; and "ensuring the security of network and
  information systems" (P). These are examples only; the balancing test
  still applies.

**(b) Triggers.**

- The agent supports safeguarding, crime or fraud detection, or
  disclosures to police or public bodies.
- The design relies on legitimate interests for security logging,
  intra-group sharing or marketing.

**(c) Paperwork.** The DPIA "Legal basis" section and the records' "Legal
basis" column gain the UK options: 6(1)(ea) with its Annex 1 condition,
and 6(1)(f) with the Article 6(11) example if one applies. Security
logging and abuse-monitoring flows can cite the network-security example
in a `counsel:` prompt.

**(d) Counsel only.**

- Does an Annex 1 condition truly apply?
- Is the processing necessary for it?
- Is a public-authority client barred from relying on (ea) or (f) for its
  own tasks?

### 1.3 Purpose limitation: compatible further processing

**(a) Status.** In force since 5 February 2026 (P, s. 71).

- New Article 8A sets out the compatibility factors and lists cases
  deemed compatible, including Annex 2 purposes.
- Data collected on consent can be re-used only within the consent, or
  under narrow limbs.
- Article 6(4) is omitted, and new Article 5(3) says compatibility does
  not by itself make processing lawful.

**(b) Triggers.**

- Re-using existing HR, CRM or ticket data to ground, evaluate or tune the
  agent.
- Building evaluation sets from production traffic.

**(c) Paperwork.** In the DPIA "Necessity and proportionality" section,
write one line per re-used dataset: its original purpose and basis,
whether it was consent-based, and the Article 8A factors.

**(d) Counsel only.** Is the re-use compatible under Article 8A?

### 1.4 DPIAs, records of processing and DPOs: unchanged in substance

**(a) Status, checked 2026-10-26.** Articles 30, 35 and 37 carry no
substantive DUAA amendment. Each changed only "Commissioner" to
"Commission" on 30 September 2026 (SI 2026/386 and SI 2026/1015), and
Article 37(1)(a) now reads "courts and tribunals" (P). The
under-250-employee exemption in Article 30(5) and its three exceptions are
unchanged (P). The DPDI Bill's proposals for a "senior responsible
individual" and a lighter "assessment of high risk processing" did not
pass. That was the earlier, lapsed bill; this note did not re-read it.

Article 35 still requires the following (P):

- (4) the Commission publishes a list of processing needing a DPIA (the
  ICO list, §2.5);
- (7) the four minimum contents;
- (9) data subjects' views where appropriate;
- (11) review when the risk changes.

Article 36 prior consultation is unchanged: the regulator has up to eight
weeks, extendable by six. This is UK GDPR text this note did not re-read;
the article does not appear in the DUAA's commencement lists.

**(b) Triggers.** As in the EU reference, with the ICO list (§2.5)
replacing the national-list placeholder.

**(c) Paperwork.**

- The existing DPIA template (Article 35(7) mapping) and the Article 30(1)
  records template carry over.
- The regulator becomes the Information Commission.
- The national list becomes the ICO's ten-item list.
- Article 30(1)(g) refers to "security measures referred to in Article 32
  or section 28(3) of the 2018 Act" (P, Art. 30 amendment note F1).

**(d) Counsel only.**

- Is a DPIA required on the ICO list plus WP248 criteria?
- Is prior consultation needed?

### 1.5 Subject access: reasonable and proportionate searches; time limits

**(a) Status.**

- **The search limit.** New Article 15(1A) entitles the person only to
  what the controller can provide after "a reasonable and proportionate
  search". It has been in force since Royal Assent and is treated as in
  force from 1 January 2024, checked 2026-10-26 (P, s. 78(5)).
- **The time limits.** New Article 12A has been in force since
  5 February 2026 (P, s. 76):
  - the clock starts at the latest of receipt of the request, receipt of
    any identity information, or payment of any fee;
  - the period is one month, extendable by two months for complexity or
    number of requests;
  - time spent waiting for requested clarification does not count.
- **ICO guidance.** Guidance on "Handling subject access requests
  generated by AI" is in drafting, due Winter 2026 (P, plans page).

**(b) Triggers.**

- Personal data sits in agent session state, memory banks, traces, logs,
  evaluation sets or vector stores.
- The agent itself may draft SAR responses.
- The client expects AI-generated SARs at volume.

**(c) Paperwork.** The DPIA "Data flows" and "Retention and erasure"
sections gain, per store: whether it is searchable by data subject, the
search method, and the erasure path. This evidences the "reasonable and
proportionate search". The security questionnaire answer on "data subject
rights" cites the same rows.

**(d) Counsel only.** Is a search confined to the stores listed
"reasonable and proportionate", given the agent's memory design?

### 1.6 Complaints to controllers

**(a) Status.** In force since 19 June 2026, checked 2026-10-26 (P,
s. 103; SI 2026/82 reg. 3).

- **New s. 164A DPA 2018.** Controllers must facilitate complaints, for
  example with "a complaint form which can be completed electronically".
  They must acknowledge within 30 days and inform the complainant of the
  outcome without undue delay.
- **New s. 164B.** The Secretary of State may require controllers to
  report complaint numbers. No regulations were found.
- **UK GDPR Article 77 is omitted**; complaints to the regulator now run
  through s. 165 DPA 2018 (P).
- **ICO guidance.** Final guidance was published on 12 February 2026 and
  updated on 8 May 2026 (P). It says there are no exemptions from the duty
  to have a process.

**(b) Triggers.** Any UK controller client. The trigger is sharper when
the agent faces the public or employees, or is itself a complaint channel.

**(c) Paperwork.**

- The system card "Contact" section names the complaint route.
- The DPIA "Risks and measures" section cites the client's s. 164A
  process, or records a `gap:`.
- If the agent handles complaints, the design must route data protection
  complaints to that process.

**(d) Counsel only.** Does the agent's channel count as receiving a data
protection complaint, so that the 30-day acknowledgement clock starts?

### 1.7 Children's higher protection matters

**(a) Status.** In force since 5 February 2026 (P, s. 81). New Article
25(1A) and (1B) apply to information society services "likely to be
accessed by children". When designing technical and organisational
measures, the controller "must take into account the children's higher
protection matters". The ICO says conformity with the Age Appropriate
Design Code should already satisfy this (P, ICO summary).

**(b) Triggers.** A consumer-facing agent that under-18s are likely to
use: education, gaming, retail, health.

**(c) Paperwork.** The DPIA gains a "Children" subsection under
"Necessity and proportionality", and the system card's out-of-scope use
records the position.

**(d) Counsel only.**

- Is the service "likely to be accessed by children"?
- Is conformity with the Age Appropriate Design Code needed?

### 1.8 International transfers: the "data protection test"

**(a) Status.** In force since 5 February 2026, checked 2026-10-26 (P,
Sch. 7).

- **Article 44A.** A transfer must be approved by regulations (Article
  45A), subject to appropriate safeguards (Article 46), or within a
  derogation (Article 49).
- **The test (Article 45B and 46(1A), (6), (7)).** The standard of
  protection must be "not materially lower" than under the UK GDPR and the
  DPA 2018. A controller relying on safeguards must consider, "acting
  reasonably and proportionately", that the test is met, judged by "all
  the circumstances" including the nature and volume of data.
- **ICO guidance.**
  - The ICO glossary says "data protection test" replaces the TRA wording
    in law. A TRA completed under earlier ICO guidance that concluded
    protection was sufficient meets the test (P, ICO search extracts).
  - The transfer guides were restructured on 15 January 2026.
  - The ICO plans to update the IDTA and the Addendum "in the course of
    2026"; until then, keep using the current versions. No revised IDTA
    was found as of today.
- **UK adequacy list** (P, ICO page): the EEA; Andorra, Argentina, Faroe
  Islands, Gibraltar, Guernsey, Isle of Man, Israel, Jersey, New Zealand,
  Switzerland, Uruguay, South Korea; partial adequacy for Canada (PIPEDA),
  Japan (APPI) and the US (the UK Extension to the Data Privacy Framework
  only). **No UK adequacy regulations exist for Australia.**
- **EU to UK.** The Commission renewed the UK's adequacy on
  19 December 2025 by Implementing Decision (EU) 2025/2574 (P, Commission
  page, search extract), to 27 December 2031 (S, Freeths). EU clients can
  keep sending data to UK-hosted systems.

**(b) Triggers.**

- Australian (or other non-adequate) staff of the consultancy access UK
  production data, logs, traces, evaluation sets or support tickets.
- The model endpoint, cache, grounding logs or abuse-monitoring storage
  sit outside the UK or EEA. The global endpoint gives no location
  guarantee, per the existing Google reference.
- US sub-processors: does the UK Extension apply, or are safeguards
  needed?

**(c) Paperwork.**

- **Records.** The "Third-country transfers and safeguard" column names,
  per row, the country, the mechanism (adequacy regulation, IDTA,
  Addendum, derogation) and the reference to a data protection test
  record.
- **DPIA.** The "Recipients, processors and regions" section lists the
  same facts.
- **New annex: "Transfer data protection test inputs".** Per restricted
  transfer, it records: data categories and volume; the access mode
  (remote access from Australia counts); the recipient's safeguards
  (SB IDs); the laws of the destination country; and onward transfers.
  These are the facts the client's or agency's TRA needs. The conclusion
  is counsel's.

**(d) Counsel only.**

- Is remote access by the consultancy a restricted transfer, and who is
  the exporter?
- Is the IDTA or the Addendum the right tool?
- Is the test met for Australia?
- Does the client's contract with Google already cover transfers (the
  Cloud DPA)?
- Does the consultancy need a UK Article 27 representative? Article 27
  was not re-read for this note.

### 1.9 Cookies and PECR: exceptions and fines

**(a) Status.** In force since 5 February 2026, checked 2026-10-26 (P,
Schs. 12 and 13).

New PECR Schedule A1 allows storage or access without consent for:

- transmission of a communication;
- what is strictly necessary for a requested service (security, fraud
  prevention, authentication, remembering selections);
- statistical purposes to improve one's own service or website;
- website appearance or functionality;
- locating a user who asks for emergency help.

The statistics and appearance exceptions need "clear and comprehensive
information" and a "simple" free means to object. Advertising still needs
consent (S, Blake Morgan via search).

Fines:

- PECR regulations 5, 6, 7, 8, 14 and 19 to 24 now sit under DPA 2018
  s. 157(2)(a) as modified by PECR Schedule 1 para. 18 (P). That carries
  the higher maximum of £17.5 million or 4% of worldwide turnover (P,
  s. 157). This is the reading of the modified section; the ICO summary
  says only "aligned with UK GDPR ... in most cases".
- Communications providers' breach notification moves to 72 hours (P, ICO
  summary).
- Final ICO storage and access technologies guidance was published on
  29 April 2026 (P, search extract).

**(b) Triggers.**

- The agent's web front end sets cookies or local storage: analytics,
  session, A/B testing, chat-widget persistence.
- The agent sends marketing emails or texts.

**(c) Paperwork.**

- The DPIA "Data flows" section adds a front-end storage row: the purpose,
  and the exception relied on or consent.
- The security questionnaire records the cookie inventory.
- The system card or privacy notice gives the objection route for the
  analytics exception.

**(d) Counsel only.**

- Does each cookie fall within an exception, or does it need consent?
- Is any agent-sent message "direct marketing"?

### 1.10 The regulator and fines

**(a) Status.**

- The Information Commission replaced the Information Commissioner on
  30 September 2026, checked 2026-10-26 (P, SI 2026/1015).
- UK GDPR fines are unchanged: Article 83 tiers through DPA 2018 s. 157
  (P).
- Infringement of s. 164A (complaints) attracts the standard maximum of
  £8.7 million or 2% (P, s. 157(4A)).
- The ICO has new powers, including compelled interviews (P, ICO
  "organisations" page).

**(c) Paperwork.** Every draft names "the Information Commission" and
cites UK GDPR as "UK GDPR" (retained Regulation (EU) 2016/679 as amended),
never the EU text.

### 1.11 Where the UK now differs from the EU GDPR (template impact)

| Topic | EU GDPR (current reference) | UK GDPR today | Template change |
| --- | --- | --- | --- |
| Automated decisions | Art. 22 prohibition with three exceptions | Arts. 22A to 22D: permitted on any basis with Art. 22C safeguards; prohibition kept for special category data and for basis (ea) | New DPIA ADM section; system card ADM notice |
| Lawful bases | Art. 6(1)(a) to (f) | Adds (ea) recognised legitimate interest (Annex 1); Art. 6(11) examples | Legal-basis prompts list (ea) |
| Further processing | Art. 6(4) | Art. 8A and Annex 2; stricter for consent-based data | Re-use line per dataset |
| Special categories | Art. 9 | Art. 9 plus Art. 11A power to add categories (none made) | Note the power; no change yet |
| Subject access | One month; full search | Reasonable and proportionate search; Art. 12A clock and pause | Searchability per store |
| Complaints | Complaint to supervisory authority (Art. 77) | Controllers must run a s. 164A complaints process with 30-day acknowledgement; Art. 77 omitted, regulator complaints under DPA 2018 s. 165 (whether the regulator may require a prior complaint to the controller was not verified) | System card contact; DPIA measure |
| Children | Recital 38; Art. 8 | Art. 25(1A) "children's higher protection matters" | DPIA children subsection |
| Transfers | Chapter V "essentially equivalent"; adequacy; SCCs; TIA | "Not materially lower" data protection test; Art. 45A regulations; IDTA or Addendum; no Australia adequacy | Transfer annex; records column |
| DPIA, records, DPO | Arts. 30, 35, 37 | Same substance; "Commission"; ICO DPIA list | National list becomes the ICO list |
| Regulator | Lead supervisory authority | Information Commission (from 30 Sep 2026) | Name |
| Cookies | ePrivacy consent with narrow exemptions | PECR Sch. A1 adds analytics and functionality exceptions with an opt-out | Front-end storage row |
| AI-specific law | EU AI Act | None; regulator guidance only | Regime screen replaces Art. 6 and Annex III memo |

## 2. ICO guidance

### 2.1 Guidance on AI and data protection

**(a) Status.** Last updated 15 March 2023. It carries a banner: "this
guidance is under review and may be subject to change" because of the
DUAA, checked 2026-10-26 (P). It remains the ICO's published view.

The accountability chapter (P) says:

- "In the vast majority of cases, the use of AI will involve a type of
  processing likely to result in a high risk."
- An AI DPIA should give "an explanation of any relevant variation or
  margins of error", "identify and record the degree of any human
  involvement", and "describe any trade-offs", such as statistical
  accuracy against data minimisation.
- Roles follow function, not contract labels. In the cloud ML service
  example, "The clients will be controllers, and the provider is likely to
  be a processor."

**(b) Triggers.** Every UK agent that processes personal data.

**(c) Paperwork.** The DPIA "Risks and measures" section adds three
fields: performance variance from evaluation reports (M IDs), the degree
of human involvement (from §1.1), and trade-offs (D IDs).

**(d) Counsel only.** Whether the client needs to read the 2023 guidance
against the DUAA changes.

### 2.2 ADM and profiling guidance, and the statutory AI and ADM code

**(a) Status.**

- The draft ADM guidance is covered in §1.1.
- **SI 2026/425**, in force 12 May 2026, checked 2026-10-26 (P), requires
  the Commissioner (now the Commission) to prepare a code of practice on
  "the processing of personal data in connection with the development and
  use of artificial intelligence" and on ADM, including children's data.
  No draft code is published. A secondary source estimates 2027 at the
  earliest (S, Bratby).
- The ICO says the agentic AI call for evidence and the ADM guidance will
  inform the code (P).

**(c) Paperwork.** In the impact assessment, "Monitoring and review" names
the code as a re-review trigger.

### 2.3 Generative AI consultation outcomes (December 2024)

**(a) Status.** The response to the 2024 consultation series was
published in December 2024 (P, search extract and chapter pages; index
undated). The ICO says the DUAA "may have an impact on the positions".
Positions relevant to a deployer (P):

- **Controllership.** "A contract does not necessarily determine" roles.
  "Joint controllership is more likely where both parties retain shared
  objectives or influence during the deployment stage." A developer using
  deployer data to improve its own models is a controller for that
  processing.
- **Accuracy.** The level of accuracy needed is "linked to the specific
  purpose". Outputs that users rely on as fact need more. Labelling
  outputs as AI-generated is a possible measure.
- **Purpose limitation.** Developing a model and developing an
  application on it are separate purposes.

**(b) Triggers.**

- The client uses a third-party model through an API. This is the normal
  ADK case.
- The client fine-tunes the model.
- Users rely on the agent's outputs as fact.

**(c) Paperwork.**

- The DPIA's "Model provider data use" section gains the controllership
  question for the provider. The existing Google facts (no training
  without permission, abuse monitoring) feed it.
- The system card's "Limits" section states the accuracy position and any
  output labelling.

**(d) Counsel only.** Is Google a processor only, or a controller for any
part, for example abuse monitoring?

### 2.4 AI and biometrics strategy, foundation models and agentic AI

**(a) Status, checked 2026-10-26.**

- **The strategy** launched on 5 June 2025 (P). The March 2026 update
  lists progress (P):
  - research on ADM in recruitment;
  - police facial recognition audits;
  - the Tech Futures report on agentic AI (January 2026);
  - engagement with foundation model developers.
- **Foundation models.** On 8 October 2026 the ICO said ten developers,
  including Google, made or committed to data protection changes (P).
  Foundation model guidance is due Autumn 2026 (P, plans page).
- **Agentic AI.** A call for evidence runs from 8 October 2026 to
  20 November 2026 (P). Its sections are data security, transparency,
  accountability, ADM, fairness and purpose limitation, and lawfulness.
  Agentic AI guidance is due Spring 2027 (P, plans page). The ICO says
  agent autonomy does not excuse poor compliance (P).
- **The ten agentic risks** in the Tech Futures report (P):
  1. controllership across the supply chain;
  2. ADM;
  3. purpose creep;
  4. data minimisation;
  5. special category inference;
  6. accuracy and cascading hallucinations;
  7. transparency, including "invisible processing";
  8. individual rights;
  9. security (goal manipulation, poisoned memory);
  10. memory.

**(b) Triggers.**

- Multi-agent or tool-using agents.
- Agents with persistent memory.
- Agents acting on a person's behalf.

**(c) Paperwork.** The DPIA "Risks and measures" table uses these ten
risks as its UK row headings, each citing C, SB and M IDs.
`adk-agent-security` and `protect-adk-sensitive-data` evidence fills the
security, minimisation and inference rows.

**(d) Counsel only.** Should the client respond to the call for evidence,
or wait for the final guidance?

### 2.5 DPIA guidance and the ICO list

**(a) Status.** The DPIA guidance pages carry the DUAA "under review"
banner, checked 2026-10-26 (P). The ICO list (P) has ten entries. Some
need a DPIA on their own; others only when combined with a WP248
criterion:

- **Innovative technology,** "including AI". Combined with another
  criterion.
- **Denial of service.** Access to a product, service, opportunity or
  benefit decided by ADM, profiling or special category data.
- **Large-scale profiling.** Includes "Application of AI to existing
  process".
- **Biometric data** for unique identification. Combined.
- **Genetic data.** Combined.
- **Data matching.**
- **Invisible processing.** Combined.
- **Tracking.** Includes workplace monitoring; geolocation when combined.
- **Targeting of children or other vulnerable individuals.**
- **Risk of physical harm.**

The ICO keeps WP248's "two criteria usually" rule of thumb and adds that
one factor can be enough (P).

**(b) Triggers.** A generative-AI agent meets "innovative technology", so
one more criterion makes a DPIA required, for example employees (a
vulnerable data subject), evaluation, or data matching across tools.

**(c) Paperwork.** The DPIA "Screening" section gains a UK table: ICO list
item, met or not, cited fact. It sits beside the existing WP248 nine.

**(d) Counsel only.** Is a DPIA required? The DPO decides.

### 2.6 Employment: monitoring workers and recruitment

**(a) Status, checked 2026-10-26.**

- **Monitoring workers guidance** (published October 2023; date not shown
  on the page) carries the DUAA "under review" banner (P). An update is in
  drafting, due Winter 2026/2027 (P, plans page). Its content (P):
  - "You must carry out a DPIA before undertaking any processing likely
    to cause high risk."
  - Workers must be told, apart from "very exceptional circumstances";
    covert monitoring needs senior sign-off.
  - "Consent is not usually appropriate in the employment context."
  - Employers "should seek and document the views of your workers or
    their representatives".
- **Recruitment.** Guidance is in drafting, due Winter 2026 (P).
  - The November 2024 audit of AI recruitment tools made 296
    recommendations. Concerns included filtering by protected
    characteristics, inferring them from names, and providers wrongly
    calling themselves processors (P, search extract).
  - The ICO's 31 March 2026 report asks employers using ADM in hiring to
    monitor for bias (consider monthly reviews), tell candidates, and
    explain how to challenge and get human review (P).

**(b) Triggers.**

- The agent processes data about UK employees, workers, contractors or
  candidates.
- The agent monitors productivity, communications or behaviour.
- The agent screens, ranks or schedules people.

**(c) Paperwork.**

- The DPIA's "Data subjects" and "Screening" sections record employees as
  vulnerable (WP248 criterion 7) and tracking or monitoring (ICO list).
- Article 35(9) consultation with workers or their representatives is a
  calendar wait (W).
- The system card states the worker notice.

**(d) Counsel only.**

- Is this "monitoring"?
- Is any covert element justified?
- Must works councils or unions be consulted under the employment
  contracts or collective agreements?

### 2.7 Storage and access technologies guidance

**(a) Status.** The final guidance was published on 29 April 2026, with a
new chapter on the DUAA exceptions (P, search extract). Mapping as in
§1.9.

## 3. UK AI policy

### 3.1 No AI bill

**(a) Status, checked 2026-10-26.**

- **The King's Speech of 13 May 2026** mentions no AI bill (P). Its
  relevant bills are:
  - the **Regulating for Growth Bill**, with cross-economy sandbox powers
    and a stronger Growth Duty (P, briefing-notes title; S for detail);
  - the **Cyber Security and Resilience (Network and Information Systems)
    Bill**, carried over and in the Lords as HL Bill 32. It had its Lords
    second reading on 14 July 2026 (P, Hansard via search) and is not
    law.
- **The 2024 plan** to legislate for frontier model developers is
  reported as shelved (S, Bird & Bird).
- **The AI Growth Lab.** The call for evidence ran from 21 October 2025
  to 7 January 2026. A legal-services advisory lab was announced on
  8 June 2026; it "does not change legislation" (P, search extracts).
- **DSIT call for evidence** on "Data regulation in the age of AI" ran
  from 15 July 2026 to 9 September 2026 (P). It asks whether "further
  guidance, targeted changes or more fundamental reform" of UK GDPR is
  needed for AI, including agentic AI and the Article 22A test. This is a
  signal of possible further data reform. There is no proposal yet.

**(c) Paperwork.**

- The UK classification memo states: "No AI-specific statute applies in
  the UK on <date>, checked <date>; the regimes below apply."
- If the client also places the system on the EU market, or its output
  is used in the EU, the EU AI Act memo still applies. The UK memo does
  not replace it.

**(d) Counsel only.** Does the EU AI Act apply through EU users or EU
output use?

### 3.2 AI Opportunities Action Plan

**(a) Status.**

- Published on 13 January 2025 (P). It keeps the "pro-innovation approach
  to regulation".
- It recommends:
  - funding regulators' AI capability (rec. 25);
  - sandboxes (rec. 27);
  - that regulators "publish annually how they have enabled innovation"
    (rec. 28);
  - AI assurance tools (rec. 29);
  - a text and data mining reform "at least as competitive as the EU"
    (rec. 24).
- The One Year On report (January 2026) says 38 of 50 actions are met (P,
  search extract).

**(c) Paperwork.** None directly. Mention only, as context in the memo.

### 3.3 AI Security Institute

**(a) Status.** Renamed from the AI Safety Institute on 14 February 2025
(P, gov.uk news via search). It is a research and evaluation body with no
regulatory powers over deployers; none were found. The ICO is making
enquiries of it about agent testing incidents (P, ICO 8 October 2026).

**(c) Paperwork.** Mention only. Its published evaluations can be cited in
the impact assessment's NIST mapping as external evidence.

### 3.4 Code of Practice for the Cyber Security of AI and ETSI EN 304 223

**(a) Status.**

- **The DSIT code.** Published on 31 January 2025; voluntary (P). It has
  13 principles across five phases:
  - **secure design:** 1 awareness, 2 design for security, 3 threats and
    risk, 4 human responsibility;
  - **secure development:** 5 assets, 6 infrastructure, 7 supply chain,
    8 document data, models and prompts, 9 testing;
  - **secure deployment:** 10 communication with end-users and affected
    entities;
  - **secure maintenance:** 11 updates, 12 monitor behaviour;
  - **secure end of life:** 13 data and model disposal.

  It defines five roles: Developers, System Operators, Data Custodians,
  End-users and Affected Entities (P).
- **The ETSI standard.** ETSI EN 304 223 V2.1.1 (2025-12) is the European
  Standard built on the code and TS 104 223. ETSI announced it in January
  2026 as the "first globally applicable European Standard" for AI
  cybersecurity (P, search extracts). Companion TS 104 275 (2026-09)
  covers generative AI (P, search extract). The PDF was not opened.

**(b) Triggers.**

- The client's CISO asks for a baseline.
- A public-sector or regulated client cites the code in procurement.

**(c) Paperwork.**

- **Security questionnaire.** Add a "DSIT Code / EN 304 223" mapping
  column: principle number, then the SB or C ID, then evidence status. The
  agency is usually "Developer" and the client "System Operator" and
  "Data Custodian".
- **System card.** Principle 10 information goes here.

**(d) Counsel only.** Whether contracts should promise conformity with
EN 304 223.

### 3.5 AI Management Essentials (AIME)

**(a) Status.** The consultation ran from 6 November 2024 to 29 January
2025. The government response, updated 6 February 2026, says: "DSIT will
not be publishing AIME and therefore will not be making it a requirement
of the government procurement process." DSIT plans future SME guidance on
"foundational governance measures" (P), checked 2026-10-26.

**(c) Paperwork.** None. Mention only, so drafters do not cite AIME as a
live tool.

### 3.6 Algorithmic Transparency Recording Standard (ATRS)

**(a) Status.** Mandatory for central government since 6 February 2024
(S via search; the policy page of 17 December 2024 is P).

- **Who must publish.** Ministerial and non-ministerial departments, and
  arm's-length bodies that "provide public or frontline services, or
  routinely interact with the general public". Phase 1 covers most
  ministerial departments and HMRC; phase 2 covers the rest (P).
- **Which tools.** Tools that "have a significant influence on a
  decision-making process with public effect" or interact directly with
  the public, once in Beta, Pilot or Production (P).
- **Exemptions.** FOI exemptions apply; a field can be marked "EXEMPT"
  (P).
- **Suppliers.** Suppliers are not bound directly, but buyers "should make
  this expectation clear in their invitation to tender" (P).
- **Wider public sector.** The standard is recommended (S, search extract
  of the hub page).

**(b) Triggers.**

- The client is a UK central government department or an in-scope
  arm's-length body.
- The tool is public-facing or influences decisions with public effect.
- The tool is going to Beta, Pilot or Production.

**(c) Paperwork.** A **new document: an ATRS record draft**, filled from
the system card (purpose, data, human oversight, risks), the DPIA and the
impact assessment. Tier 1 is a summary; Tier 2 holds the detail. The
template fields were not re-read for this note.

**(d) Counsel only.**

- Is the body in scope?
- Which fields are FOI-exempt?

### 3.7 Cyber Security and Resilience Bill (mention only)

**(a) Status.** A bill in the Lords (HL Bill 32), not law, checked
2026-10-26. It would bring medium and large "relevant managed service
providers" into NIS (P, Hansard via search).

**(b) Trigger.** The consultancy provides ongoing managed services with
privileged access to a UK client's systems after handover.

**(d) Counsel only.** Would the consultancy be a relevant managed service
provider if the bill passes?

## 4. Other laws

### 4.1 Equality Act 2010

**(a) Status.** In force. The parts that matter for an agent:

- **Indirect discrimination (s. 19, P).** A provision, criterion or
  practice that puts people sharing a protected characteristic at a
  particular disadvantage is unlawful unless it is "a proportionate means
  of achieving a legitimate aim". The relevant characteristics are age,
  disability, gender reassignment, marriage and civil partnership, race,
  religion or belief, sex and sexual orientation.
- **Public sector equality duty (s. 149, P).**
  - **Who.** It binds public authorities, and anyone exercising public
    functions (s. 149(2)).
  - **What.** They must have "due regard to the need to" eliminate
    prohibited conduct, advance equality of opportunity and foster good
    relations.
  - **EHRC guidance (1 September 2022, P).** The duty applies "from the
    very start" and covers AI that "others may be developing or using on
    their behalf". Its example of a postcode used as a proxy shows
    indirect discrimination.
- **Services and employment.** The prohibitions in services (s. 29) and
  employment (s. 39) and the duty to make reasonable adjustments
  (s. 20) are cited from the Act's structure. These sections were not
  re-read today.
- **DSIT's Responsible AI in Recruitment guide (25 March 2024, P)**
  recommends:
  - impact and equality impact assessments;
  - a DPIA ("required for all development and deployment of AI systems
    that involve personal data");
  - bias audits;
  - performance testing;
  - model cards.
- **Employment Rights Act 2025.** It adds provisions to Equality Act
  ss. 40 and 40B (third-party harassment). These are listed on the s. 149
  page as yet to be applied (P).

**(b) Triggers.**

- The agent informs decisions about employees, candidates, customers or
  service users.
- The agent uses or could infer protected characteristics or proxies:
  postcode, name, age signals, language.
- The client is a public authority, or the agent exercises public
  functions.
- Disabled users interact with the agent: accessibility and reasonable
  adjustments.

**(c) Paperwork.**

- **Impact assessment.** A UK "Equality" subsection under Impacts: the
  protected characteristics at risk, the proxies, the bias test (M ID) or
  a `gap:`, and the accessibility route. For public-sector clients this
  is an **equality impact assessment input**: PSED due regard, recorded
  before the decision.
- **System card.** Limits record bias results by group, or `gap:`.

**(d) Counsel only.**

- Is any disparity objectively justified?
- Does the PSED apply to the client or the function?
- Are the reasonable adjustments enough?

### 4.2 Online Safety Act 2023

**(a) Status.**

- **Duties in force.** Illegal content duties are enforceable from
  17 March 2025; children's risk assessments were due by 24 July 2025 (P,
  gov.uk explainer updated 24 April 2025).
- **Ofcom on chatbots.** The open letter (November 2024; page returned
  403, so content is from search extracts) says:
  - a chatbot whose outputs users can share with other users is a
    user-to-user service;
  - generative AI that searches "more than one website and/or database"
    is a search service;
  - tools that generate pornography are in scope;
  - a chatbot that talks only to the user, does not search multiple
    sources and cannot generate pornography is outside the Act.
- **The loophole closure.**
  - The government announced on 15 February 2026 that it would close the
    "loophole" so all AI chatbot providers meet illegal content duties
    (P).
  - Crime and Policing Act 2026 s. 248 (Royal Assent 29 April 2026)
    inserts OSA s. 216A. It lets the Secretary of State amend the Act by
    regulations as regards "AI services" and illegal AI-generated content
    (P).
  - No regulations under s. 216A were found as of today. A report to
    Parliament by 31 December 2026 is mentioned in secondary sources,
    not seen in the section text.

**(b) Triggers.**

- The agent product lets users share content or outputs with other users:
  group chats, shared threads, user-built agents.
- The agent searches multiple websites or databases for UK users. Ofcom
  calls this a "search service"; a RAG agent over the open web or many
  databases may qualify.
- The agent can generate pornographic content.
- The agent is consumer-facing and likely to be used by children.

**(c) Paperwork.**

- **Classification memo.** A UK "Online Safety Act" section: service type
  (user-to-user, search, Part 5, or none), with the facts.
- **New document if in scope:** an illegal content risk assessment and,
  if children are likely to access the service, a children's access
  assessment and risk assessment. These are Ofcom-format documents the
  pack does not draft today. Flag them as `gap:` with the owner.
- Internal enterprise agents with no sharing are usually out of scope.
  Record why with `n/a:`.

**(d) Counsel only.**

- Does the service type fall in scope?
- Does the "multiple websites or databases" test catch the agent's
  retrieval?
- Will future s. 216A regulations bring a one-to-one chatbot in?

### 4.3 Consumer law: DMCC Act 2024 and the CMA on AI agents

**(a) Status.**

- **DMCC direct enforcement** has applied to conduct from 6 April 2025
  (P, CMA material via search). The CMA can decide infringements itself
  and fine up to 10% of global turnover or £300,000, whichever is higher.
  Fake reviews and drip pricing are banned practices (P, search
  extracts).
- **CMA guidance on AI agents.** "Complying with consumer law when using
  AI agents" (9 March 2026, P) says:
  - the business is accountable "even if a third party designed or
    supplies it";
  - tell people they are dealing with AI where it could change their
    decision;
  - "Do not overstate the role or AI involved";
  - test before deployment;
  - "Make sure there is a human in the loop, actively checking that the
    AI agent is making correct decisions";
  - fix problems quickly, especially at scale or with vulnerable
    customers;
  - prices must include unavoidable charges.
- **CMA paper "Agentic AI and consumers"** (9 March 2026, P) lists
  steering, errors, bias, loss of agency, agentic collusion, lock-in, and
  privacy and security. It recommends disclosure, mandatory confirmation
  for high-risk actions, and audit logs.

**(b) Triggers.**

- The agent deals with UK consumers: sales, pricing, recommendations,
  refunds, comparison.
- The agent writes or solicits reviews.
- The agent takes purchasing or payment actions.

**(c) Paperwork.**

- **System card.** AI disclosure; capabilities stated without
  overstatement.
- **Impact assessment.** A "Consumer" impact row.
- **Security questionnaire.** Confirmation before high-risk actions
  (cite `adk-operational-guardrails` evidence) and audit logs.
- A **consumer-law check** subsection in the UK memo.

**(d) Counsel only.**

- Is any agent behaviour a misleading action or omission, or a banned
  practice?
- Who is liable between the client and the agency?

### 4.4 FCA: Consumer Duty and AI

**(a) Status, checked 2026-10-26.**

- **No AI-specific rules.** "We are not going to introduce new
  regulations for AI" (P, FCA blog, 8 June 2026). The FCA relies on the
  Consumer Duty and SM&CR. It is exploring governance, testing and
  monitoring, fair treatment of customers "with features of
  vulnerability", and explaining AI-driven decisions.
- **Good and poor practice report** due "later this year" (P).
- **The Mills Review** (6 July 2026, P) makes seven recommendations,
  including "Build the foundations for agentic finance". AI Live Testing
  and the AI Lab continue (P).
- The Consumer Duty itself (PRIN 2A) has been in force since 31 July 2023
  for open products. This date is from this note's prior knowledge and was
  not re-read.

**(b) Triggers.**

- The client is FCA-authorised.
- The agent touches retail customers: advice, servicing, complaints,
  collections, credit.

**(c) Paperwork.**

- **Impact assessment.** Consumer Duty outcomes (products and services,
  price and value, consumer understanding, consumer support) as impact
  rows.
- **System card.** Consumer understanding.
- **Classification memo.** The SM&CR accountable senior manager is named
  as an owner.

**(d) Counsel only.**

- Does the agent's output amount to regulated advice?
- Does the deployment meet the Duty's cross-cutting rules?

### 4.5 CMA on foundation models (mention only)

**(a) Status.** The initial review was published in September 2023 and
the update paper on 11 April 2024 (P, search extracts). The CMA's March
2026 agentic paper says its principles of access, diversity, choice, fair
dealing, transparency and accountability "remain directly relevant" (P).
They are aimed at model developers and markets.

**(c) Paperwork.** None for a deployer, beyond the transparency and
accountability points already in §4.3.

### 4.6 Copyright and AI

**(a) Status.**

- **The report.** The report and impact assessment under DUAA ss. 135 and
  136 were published on 18 March 2026 (P). It says:
  - "a broad copyright exception with opt-out is no longer the
    government's preferred way forward";
  - there is no replacement exception;
  - industry work on input transparency and on labelling AI-generated
    content is to come;
  - protection for wholly computer-generated works should be removed;
  - "We will not introduce reforms to copyright law until we are
    confident."
- **No legislation is pending.** The UK text and data mining exception
  (CDPA s. 29A, non-commercial research) is unchanged. That is prior
  knowledge, not re-read today.

**(b) Triggers.**

- The client fine-tunes or trains on third-party content.
- The agent ingests copyrighted corpora for RAG.
- The agent generates published content.

**(c) Paperwork.**

- **System card, "Data" section.** The source and licence of corpora, or
  `gap:`.
- **Impact assessment.** An IP row.
- No new document.

**(d) Counsel only.**

- Is ingestion or retrieval of these works licensed?
- Who owns the outputs?

### 4.7 Employment Rights Act 2025 (mention only)

**(a) Status.** Royal Assent on 18 December 2025 (P, gov.uk via search).
The timeline was updated on 22 October 2026 (P):

- 30 October 2026: new harassment duties, including preventing
  harassment by third parties;
- 1 January 2027: unfair dismissal qualifying period cut to six months;
- April 2027: wider blacklisting protections, including "banning
  blacklists drafted using AI".

There are no worker-surveillance or AI-consultation duties (P).

**(b) Triggers.**

- An employee-facing agent that could be a channel for third-party
  harassment.
- Any agent that compiles lists of union members or activists.

**(c) Paperwork.** An impact-assessment row only.

## 5. Must cover, should cover, mention only

Ranked for "a consultancy builds AI agents that process UK users' and
employees' personal data".

**Must cover** (template changes and the screening step):

1. **UK GDPR Articles 22A to 22D** and the ICO draft ADM guidance (§1.1).
2. **International transfers:** the data protection test; no adequacy for
   Australia; IDTA or Addendum (§1.8).
3. **The ICO DPIA list and AI DPIA contents**, and the regulator name
   (§1.4, §2.1, §2.5).
4. **Lawful bases with (ea) and Article 6(11)**; Article 8A re-use
   (§1.2, §1.3).
5. **Employment:** monitoring-workers guidance, recruitment ADM, and
   worker consultation (§2.6).
6. **Equality Act:** indirect discrimination; PSED for public bodies
   (§4.1).
7. **Subject access search and complaints process** (§1.5, §1.6).
8. **ICO agentic AI positions:** the ten risks; the call for evidence
   status; the statutory code coming (§2.4, §2.2).

**Should cover** (conditional sections):

9. **PECR cookies and marketing**, and the new fines (§1.9).
10. **ATRS record** for central-government clients (§3.6).
11. **Online Safety Act screen:** user-to-user or search service (§4.2).
12. **Consumer law and the CMA AI-agent guidance** for consumer-facing
    agents (§4.3).
13. **FCA Consumer Duty** for regulated financial clients (§4.4).
14. **DSIT Code of Practice and EN 304 223** mapping in the security
    questionnaire (§3.4).
15. **Children's higher protection matters** (§1.7).
16. **Generative AI controllership and accuracy positions** (§2.3).

**Mention only:**

17. No AI bill; the Regulating for Growth Bill; the DSIT data regulation
    call for evidence (§3.1).
18. AI Opportunities Action Plan (§3.2); AI Security Institute (§3.3).
19. AIME, not published (§3.5).
20. Cyber Security and Resilience Bill (§3.7).
21. CMA foundation model principles (§4.5).
22. Copyright and AI (§4.6); Employment Rights Act 2025 (§4.7).
23. EU-to-UK adequacy renewed to 2031 (§1.8).

## 6. Screening checklist: trigger, law, document section

| Trigger (fact in the design or brief) | Law or guidance | Document and section |
| --- | --- | --- |
| UK users, employees or candidates' personal data processed | UK GDPR, DPA 2018 | All: UK variant of DPIA pack and records |
| Data subjects include employees, workers or candidates | ICO monitoring workers; WP248 criterion 7; Art. 35(9) | DPIA Screening, Data subjects; plan W for worker consultation |
| Agent output decides, or a human only spot-checks, with effect on job, money, service, housing, health, education, reputation | UK GDPR Arts. 22A, 22C; ICO draft ADM guidance | DPIA "ADM and safeguards"; system card ADM notice and review route |
| Special category data used, or inferable from free text, in such a decision | UK GDPR Art. 22B; Art. 9 | DPIA ADM section; Legal basis; masking contract and coverage |
| Lawful basis proposed is safeguarding, crime, emergencies, security, or a public-task disclosure | Art. 6(1)(ea), Annex 1 | DPIA Legal basis; records Legal basis |
| Security logging, intra-group sharing or marketing on legitimate interests | Art. 6(1)(f), Art. 6(11) | DPIA Legal basis (counsel prompt) |
| Existing datasets re-used for grounding, evaluation or tuning | Art. 8A, Annex 2 | DPIA Necessity and proportionality |
| Generative model, plus any WP248 criterion or ICO list item | ICO DPIA list (innovative technology including AI) | DPIA Screening: ICO list table |
| Consultancy staff or systems in Australia (or elsewhere non-adequate) access UK data, logs or evaluation sets | Arts. 44A, 46(1A); no Australia adequacy; IDTA or Addendum | Records transfer column; DPIA Recipients and regions; transfer test annex |
| Model endpoint, cache, grounding or abuse logs outside UK or EEA; global endpoint | Arts. 44A to 46 | DPIA Model provider data use; Recipients and regions |
| Personal data in sessions, memory, traces, evaluation sets, vector stores | Art. 15(1A), Art. 12A; Art. 17 | DPIA Data flows, Retention and erasure (searchability per store) |
| Public-facing or employee-facing channel; agent receives complaints | DPA 2018 s. 164A | System card Contact; DPIA Risks and measures |
| Service likely to be accessed by under-18s | Art. 25(1A); Age Appropriate Design Code | DPIA Children subsection; system card out-of-scope |
| Web front end sets cookies or local storage; agent sends marketing | PECR reg. 6 and Sch. A1; regs. 22, 23; s. 157 higher maximum | DPIA Data flows (front-end storage row); questionnaire cookie inventory |
| Multi-agent, tool use, persistent memory, acts on a person's behalf | ICO Tech Futures agentic risks; call for evidence | DPIA Risks and measures (ten agentic rows) |
| Third-party model used through an API | ICO generative AI controllership; AI guidance roles | DPIA Model provider data use (controllership counsel item) |
| Users rely on outputs as fact | ICO accuracy position | System card Limits (accuracy, labelling) |
| Decisions about people; protected characteristics or proxies present | Equality Act s. 19 (and ss. 29, 39) | Impact assessment Equality; system card Limits (bias by group) |
| Client is a public authority or the agent exercises public functions | Equality Act s. 149 PSED; EHRC guidance | Impact assessment Equality (PSED due-regard record) |
| Client is a central government department or in-scope arm's-length body; tool in Beta, Pilot or Production; public effect or public-facing | ATRS mandatory scope policy | **New: ATRS record draft** |
| Users can share outputs with other users; agent searches multiple websites or databases; can generate pornography | Online Safety Act; Ofcom open letter; OSA s. 216A | Classification memo OSA section; **new: OSA risk assessments** if in scope (`gap:`) |
| Agent deals with UK consumers: prices, offers, reviews, purchases | DMCC Act 2024; CMA AI-agent guidance | UK memo consumer-law check; system card AI disclosure; questionnaire confirmation and audit logs |
| Client is FCA-authorised and the agent touches retail customers | FCA Consumer Duty; SM&CR | Impact assessment Consumer Duty rows; memo owner |
| CISO asks for an AI security baseline | DSIT Code; ETSI EN 304 223 | Security questionnaire mapping column |
| Fine-tuning or RAG on third-party works; published outputs | CDPA 1988; copyright report | System card Data; impact assessment IP row |
| Consultancy keeps privileged managed access after handover | Cyber Security and Resilience Bill (not law) | Memo note (mention only) |
| EU users or EU use of outputs as well | EU AI Act; EU GDPR | Keep the EU classification memo and EU DPIA references alongside |

## 7. What in the current skill's GDPR material needs a UK variant

Checked against `skills/adk-governance-pack/references/privacy-and-records.md`,
the DPIA and records templates, and `SKILL.md`, all read on 26 October
2026.

1. **Source line and amendment status.** The reference cites EU Regulation
   2016/679 on EUR-Lex and the EU Digital Omnibus caveat. The UK variant
   must cite:
   - UK GDPR and the DPA 2018 on legislation.gov.uk;
   - the DUAA commencement (SI 2026/82, SI 2026/1015);
   - the line "all data protection provisions in force since 19 June
     2026", with the date checked.

   The Omnibus caveat does not apply to UK law.
2. **Screening.** Keep WP248's nine criteria; the ICO built on them. Add
   the ICO's ten-item list (§2.5). Replace "name the client's lead
   authority and leave the list check to counsel" with "the Information
   Commission's list" and the ICO's "AI ... in the vast majority of cases
   ... high risk" statement.
3. **Article 22 bullet.** Rewrite for Articles 22A to 22D, with these
   elements:
   - "meaningful human involvement" in place of "solely automated";
   - the ICO's reviewer criteria and "spot-checking isn't sufficient";
   - the special category restriction in Article 22B;
   - the bar on basis (ea);
   - the four Article 22C safeguards.

   Keep the existing rule that "a human is in the loop" without a review
   rate is not a fact. The ICO's draft makes it sharper.
4. **Legal basis list.** Add Article 6(1)(ea) with Annex 1, the Article
   6(11) examples and Article 8A re-use. Keep the employee-consent
   warning; the ICO says the same.
5. **Article 9 bullet.** Unchanged list. Add a note on the Article 11A
   power (no regulations), and that the ICO's special category guidance
   is due Autumn 2026.
6. **"AI Act Article 4a" bullet.** It has no UK equivalent. Remove it from
   the UK variant, or mark it "EU only". For bias-monitoring processing in
   the UK, prompt counsel on an Article 9 condition (DPA 2018 Schedule 1).
7. **Article 36.** Same mechanics; name the Information Commission.
8. **Model provider data use.** The Google facts carry over. Add:
   - the UK transfer view: the endpoint region and where caching and
     abuse logs live;
   - the ICO's generative-AI controllership position as a `counsel:`
     prompt;
   - whether the provider is a controller for abuse monitoring.

   The EDPB Opinion 28/2024 paragraph is EU-only. The ICO's equivalent
   positions are the generative AI consultation response and the October
   2026 foundation model report. The latter was not read in full here.
9. **Records of processing.** Article 30(1) fields are unchanged. Change:
   - the "Third-country transfers and safeguard" column to name the UK
     mechanism (adequacy regulation, IDTA, Addendum, Article 49) and a
     data protection test reference;
   - the "Legal basis" column to allow (ea);
   - optionally, add an "ADM (22A) yes or no" column.

   The template's header line "GDPR Article 30(1)" becomes "UK GDPR
   Article 30(1)".
10. **DPIA template sections to add.**
    - "ADM and safeguards (UK GDPR Arts. 22A to 22D)";
    - "Children (Art. 25(1A))", when relevant;
    - "Front-end storage (PECR)";
    - "Subject access searchability" inside Data flows;
    - "Complaints process (s. 164A)" inside Risks and measures;
    - a transfer data protection test annex.
11. **Classification memo.** The EU memo is built around AI Act Articles 5,
    6, 50 and Annex III. The UK needs a **regime screen memo**:
    - no AI statute, with the date;
    - UK GDPR ADM;
    - Equality Act and PSED;
    - Online Safety Act service type;
    - consumer law;
    - FCA;
    - ATRS;
    - EU AI Act if there are EU users.

    The checker's Annex III trigger phrases still help, because UK
    employment and credit uses are the same sensitive areas. But the UK
    memo should set `counsel_required: yes` on any Article 22A significant
    decision or PSED trigger.
12. **Impact assessment.** Add UK rows: Equality (with PSED for public
    bodies), Consumer and Consumer Duty, and the ICO's ten agentic risks.
    The ISO 42005 and NIST mapping is unchanged.
13. **Security questionnaire.** Add the DSIT Code and EN 304 223 mapping
    column, the cookie inventory, and the transfer facts.
14. **New documents for UK clients.**
    - An **ATRS record draft** for central government.
    - A **transfer data protection test inputs** annex.
    - An **OSA applicability note**, and risk assessments flagged as
      `gap:`, for user-to-user or search-type agent products.
15. **Dates and checker.** All UK dates above are in force or past except:
    - final ADM guidance (Winter 2026);
    - agentic AI guidance (Spring 2027);
    - the statutory code (no date);
    - the revised IDTA (2026, not seen);
    - any s. 216A regulations (none).

    Drafts must carry these as status lines with `checked <date>`, not as
    applicability dates.

## Not verified at a primary source

- **Ofcom pages** (the open letter and the chatbots explainer) returned
  HTTP 403. Their positions are taken from search extracts quoting them
  and from the gov.uk OSA explainer, which cites the letter.
- **ETSI EN 304 223 text.** The PDF was not opened. Its status, title and
  13-principle structure come from ETSI search extracts.
- **ATRS mandate start of 6 February 2024** comes from a search extract;
  the scope policy page itself (17 December 2024) was read.
- **PECR higher maximum.** Reading the modified DPA 2018 s. 157(2)(a) as
  carrying the higher maximum is an inference from the PECR Schedule 1
  modification plus s. 157's structure, corroborated by several law-firm
  notes. The ICO summary says only "aligned ... in most cases".
- **Removal of the "serious contravention" PECR threshold**: secondary
  (Mishcon de Reya).
- **The EU renewal expiry of 27 December 2031**: secondary, consistent
  with the Commission draft's six-year term.
- **The ICO generative AI response date** (December 2024) comes from
  search extracts; the chapter pages are undated.
- **Monitoring workers guidance first published October 2023**: not shown
  on the page.
- **Equality Act ss. 20, 29, 39, CDPA s. 29A, the Consumer Duty in force
  date, UK GDPR Arts. 27 and 36**: from prior knowledge, not re-read
  today.
- **Report to Parliament by 31 December 2026 under the chatbot power**:
  secondary only, not in the s. 248 text read.
- **DMCC fines and banned practices**: from gov.uk and CMA search
  extracts; the Act itself was not opened.
- **The Regulating for Growth Bill**: its content is from the
  briefing-notes title and secondary notes. Its text and parliamentary
  stage were not checked.

## Proposed decisions for the UK variant

- **One pack, a jurisdiction switch.** Keep the six documents. Add UK
  reference files (`uk-gdpr-and-ico.md`, `uk-regime-screen.md`) and UK
  template variants only where sections differ: the DPIA ADM section,
  transfers, the records header and columns, and the regime-screen memo.
  The Article 35(7) and Article 30(1) skeletons are shared.
- **Regime screen, not risk tier.** As for Australia: the UK memo lists
  the regimes that apply, with triggers and facts, and leaves conclusions
  as `counsel:`.
- **Australian staff access is a default transfer row.** Every UK pack
  starts with a records row and a transfer-annex entry for consultancy
  access from Australia, marked `n/a:` only when the design shows no
  access.
- **Treat ICO drafts as drafts.** Cite the draft ADM guidance and the
  agentic call for evidence with their status and date, and name the 2023
  AI guidance as the published view. Add a 180-day re-check: the ADM final
  (Winter 2026), the foundation model guidance (Autumn 2026) and the
  agentic guidance (Spring 2027) are all due within the checker's
  warning window.
