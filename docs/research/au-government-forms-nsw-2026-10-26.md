# Australian government AI forms and NSW law: crosswalks for the governance pack

*Read 26 October 2026. Research for `skills/adk-governance-pack`: crosswalks
from the official Commonwealth (DTA) and NSW AI forms to the project's
records, plus the NSW state law that applies to an agent built for a NSW
agency. Drafts, not legal advice.*

Marks: **P** means read at the official source on 2026-10-26. **S** means
secondary: a commentary, a summary, or a copy of an official document hosted
somewhere else. **U** means not verified. Every date below was checked on
2026-10-26 unless a line says otherwise.

## Conclusion

1. **Commonwealth.** The DTA Policy for the responsible use of AI in
   government is at **v2.1**. v2.0 took effect on 15 December 2025, and the
   v2.1 minor updates were published on 21 October 2026 (P).
   - The **AI impact assessment tool is v1.0, published 1 December 2025**.
     It is a fillable Word template in 12 sections. Sections 1 to 4 are the
     threshold assessment and sections 5 to 12 the full assessment (P).
   - The tool's usage-pattern list (question 1.7) has four options. Appendix D
     of policy v2.1 has seven (P). The official form and the policy already
     disagree, which is exactly why the pack should not copy forms. The
     crosswalk records the v2.1 list and flags the drift.
   - Agencies must start assessments within 12 months of the policy taking
     effect: the impact assessment requirement applies to in-scope use cases
     by **15 December 2026**, and existing use cases are due by **30 April
     2027** (P).
   - The Agentic AI addendum (AGT.1 to AGT.8, updated 4 June 2026) is best
     practice, not a mandatory requirement (P).
   - Since v2.0 the Commonwealth also has an **AI Review Committee**. It gives
     non-binding advice on use cases with a *residual* high-risk rating, or
     that agencies deem highly sensitive, novel or complex (P).
2. **NSW.** The NSW AI Ethics Policy is gone.
   - **Circular DCS-2026-02** was issued on 30 July 2026, updated on
     1 September 2026, and replaces DCS-2024-04 (P). It mandates the **NSW AI
     Operational Policy, Final v1.1** (cover date 30 July 2026, P). That
     policy adopts **Australia's eight AI Ethics Principles** in place of the
     five NSW principles (community benefit, fairness, privacy and security,
     transparency, accountability).
   - The **AIAF Platform** has been the mandatory channel for registering and
     assessing AI use cases since **30 September 2026** (P).
   - Registration is a short rules-based questionnaire that decides whether a
     full AIAF assessment is needed (P).
   - Risk bands are low, medium, high and critical (Operational Policy). Uses
     rated **high or critical** must be referred to the NSW AI Review
     Committee within **five business days** of completing the AIAF (P).
   - The platform's question set is not public: it sits behind SectorLink.
     The agency's officers fill it in.
   - The public structure is the **2024 AIAF** (32 numbered questions in five
     sections). Agencies without platform access, and the circular's
     transition rule ("continue to apply the existing AIAF Excel-based
     assessment process ... until the platform is fully adopted"), still use
     it. The official PDF is no longer linked from digital.nsw.gov.au. The
     copy read here is a mirror (S for provenance; the content is the Digital
     NSW 2024 document).
   - **$5 million is not an AI Review Committee trigger on its own.** Projects
     above $5 million, or funded by the Digital Restart Fund, get extra
     central oversight through the Digital Assurance Framework (P). Referral
     is triggered by the risk band.
3. **NSW contracts already carry AI clauses.** ICTA clause 6.11 and the Core&
   Core Terms (August 2025) require the following (P, from the fork):
   - notice and approval before a supplier uses an AI system;
   - records of each AI system;
   - an AI incident programme;
   - by default, six months' notice of a change to the underlying model;
   - Customer Data kept in NSW (ICTA) or personal information kept in
     Australia (Core&), unless the Order Form permits otherwise.

   For an ADK agent, the Gemini model and its version policy must be listed
   in the Order Form.
4. **The vendor is not the form-filler.** The DTA tool's roles (assessing
   officer, approving officer, accountable use case owner) are agency
   officers. The NSW Operational Policy is "not mandatory for ... third-party
   suppliers". Its registration rule "does not apply to third-party
   suppliers" who use AI in their own services; supplier AI is managed
   through procurement and contracts (P).
   - What the agency expects from the vendor is evidence, delivered through
     contract clauses: the DTA AI model clauses, ICTA 6.11 and the Core&
     terms. That evidence covers intended use, testing and monitoring, bias
     and drift detection, records of AI use, human oversight design, no
     ingestion of buyer data, a risk management system (ISO/IEC 42001 or
     NIST AI RMF) and incident notification.
   - The crosswalks therefore produce **draft answers for the agency's
     officers**, each citing project evidence, with `agency:` where only the
     agency can answer.
5. **NSW state law** (summarised from a fork's primary reads; see Part C):
   - The PPIP Act IPPs and s 19(2) on cross-border disclosure.
   - The Mandatory Notification of Data Breach scheme (Part 6A), in force
     since 28 November 2023.
   - The HRIP Act HPPs for health information.
   - The GIPA Act: the contracts register at $150,000 or more, and AI as
     government information.
   - The State Records Act **1998** (there is no 2024 Act; the State Records
     Regulation 2024 commenced on 1 September 2024): AI outputs and metadata are State records,
     and the Operational Policy says so expressly.
   - The NSW Cyber Security Policy 2026–2027: Essential Eight **Maturity
     Level One** is the mandatory baseline, not Level Two; cyber incidents
     are reported within 24 hours.
   - The Workplace Surveillance Act 2005: 14 days' notice.

   Commonwealth Privacy Act s 7B(5) takes the consultancy's acts under a
   State contract out of the APPs. The consultancy is still an APP entity for
   its other acts.

## Sources

### Commonwealth (read by the coordinator)

| Source | Mark | Used for |
| --- | --- | --- |
| DTA, Policy for the responsible use of AI in government, landing and Implementation pages (<https://www.digital.gov.au/ai/ai-in-government-policy>, <https://www.digital.gov.au/ai/ai-in-government-policy/implementation>) | P | v2.0 effective 15 Dec 2025, v2.1 published 21 Oct 2026; NCEs; carve-outs; list of mandatory requirements |
| DTA, policy PDF "Policy for the responsible use of AI in government 2_1_1.pdf", last updated 22 Oct 2026 (<https://www.digital.gov.au/sites/default/files/documents/2026-10/Policy%20for%20the%20responsible%20use%20of%20AI%20in%20government%202_1_1.pdf>) | P (text-extracted) | Version 2.1 cover; vendor-change monitoring sentence |
| DTA, Strategy and oversight (<https://www.digital.gov.au/ai/ai-in-government-policy/strategy-and-oversight>) | P | Transparency statement, strategic position (6 months), accountable officials, use case owners and register (12 months), register shared every 6 months |
| DTA, Preparedness and operations (<https://www.digital.gov.au/ai/ai-in-government-policy/preparedness-and-operations>) | P | Operationalise responsible AI; staff training (12 months); technical standard and AI procurement guidance "strongly recommended" |
| DTA, AI use case impact assessment (<https://www.digital.gov.au/ai/ai-in-government-policy/ai-use-case-impact-assessment>) | P | In-scope test at design; assessment before deployment; tool or equivalent internal process; medium-risk and high-risk actions; vendor change monitoring; 30 April 2027 |
| DTA, Appendix C (<https://www.digital.gov.au/ai/ai-in-government-policy/policy-responsible-use-ai-government-version-20-appendix-c-scope-ai-use-cases>) | P | Five in-scope criteria; seven areas to consider; experimentation carve-out |
| DTA, Appendix D v2.1 (<https://www.digital.gov.au/ai/ai-in-government-policy/policy-responsible-use-ai-government-version-21-appendix-d-classification-system-ai-use>) | P | Seven usage patterns, six domains |
| DTA, Appendix A related frameworks (<https://www.digital.gov.au/ai/ai-in-government-policy/policy-responsible-use-ai-government-version-21-appendices>) | P | Lists "Information management for records created using AI technologies", ADM Better Practice Guide |
| DTA, Standard for AI transparency statements v2.1, updated 20 Oct 2026 (<https://www.digital.gov.au/ai/ai-in-government-policy/standard-ai-transparency-statements>) | P | Minimum contents; review triggers; notify DTA |
| DTA, Standard for accountability v2.1, updated 20 Oct 2026 (<https://www.digital.gov.au/ai/ai-in-government-policy/accountability>) | P | Accountable official duties; use case owner duties; register minimum fields; high-risk notification contents |
| DTA, AI impact assessment tool page (<https://www.digital.gov.au/ai/impact-assessment-tool>) and introduction (<https://www.digital.gov.au/ai/impact-assessment-tool/introduction>) | P | Word template and guidance PDF, both last updated 1 Dec 2025 |
| DTA, "AI impact assessment tool.docx", document control v1.0, published 01/12/2025 (<https://www.digital.gov.au/sites/default/files/documents/2025-12/AI%20impact%20assessment%20tool_1.docx>) | P (read in full) | Every section and question below |
| DTA, Guidance for the AI impact assessment tool, web pages for sections 1 to 12 (<https://www.digital.gov.au/ai/impact-assessment-tool/guidance>) | P | Question numbering 1.1 to 12.5; 4.1 options; 6.3 supplier considerations; 8.3 documentation types |
| DTA, Agentic AI addendum, PDF last updated 4 Jun 2026, and statement pages (<https://www.digital.gov.au/policy/ai/agentic-ai-addendum>) | P | AGT.1 to AGT.8 and their criteria |
| DTA, AI Review Committee and terms of reference (<https://www.digital.gov.au/policy/ai/ai-review-committee>, <https://www.digital.gov.au/policy/ai/ai-review-committee/terms-of-reference>) | P | Residual high-risk or highly sensitive, novel or complex use cases; non-binding; up to PROTECTED |
| Australian Government Solicitor, Legal update no. 327, 4 April 2025 (<https://www.ags.gov.au/publications/express-law/el327>) | P (AGS description); clause text itself S (BuyICT not read) | DTA AI model clauses, published 17 March 2025: what the seller must do |

### NSW AI policy and assessment (read by the coordinator unless marked "fork")

| Source | Mark | Used for |
| --- | --- | --- |
| DCS-2026-02 Use of Artificial Intelligence by NSW Government Agencies, issued 30 Jul 2026, updated 1 Sep 2026 (<https://arp.nsw.gov.au/dcs-2026-02-use-of-artificial-intelligence-by-nsw-government-agencies>) | P | Mandatory; entity types; eight mandatory agency requirements; attestation 31 October from 2027; Excel process during transition; AIRC within 5 business days; replaces DCS-2024-04 |
| NSW AI Operational Policy page (<https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-strategy-and-operational-policy/nsw-ai-operational-policy>) and PDF Final v1.1 (<https://www.digital.nsw.gov.au/sites/default/files/2026-09/nsw-ai-operational-policy-01092026.pdf>) | P (PDF text-extracted by the fork) | Replaces the AI Ethics Policy; risk-band definitions; Attachment A registration questions; supplier exclusion; standards A and B |
| NSW AI Assessment Framework page (<https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/nsw-ai-assessment-framework>) | P | Platform mandatory from 30 Sep 2026; offline pathway only for SectorLink gaps; high or critical go to AIRC; $5m and DRF central oversight |
| NSW AI Review Committee page (<https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/ai-review-committee>) | P | Advisory; chair Prof. Ed Santow; referrals via AISecretariat |
| Identifying AI guidance (<https://www.digital.nsw.gov.au/policy/artificial-intelligence/nsw-artificial-intelligence-assessment-framework/identifying-ai>) | P | Non-AI and AI questionnaires; "conversational assistant" is AI |
| Responsible AI guidance, roles and RACI (<https://www.digital.nsw.gov.au/policy/artificial-intelligence/nsw-artificial-intelligence-assessment-framework/responsibilities>) | P | "Evaluate vendors and third-party AI solutions for compliance with the NSW AI Operational Policy, AIAF ..."; transparency reports for high-risk or customer-facing AI |
| The NSW AI Assessment Framework, Digital NSW 2024 (88 pages), mirror copy at <https://www.aigl.blog/content/files/2026/02/The-NSW-AI-Assessment-Framework.pdf> | S (provenance); content is the official 2024 document; text-extracted; questions 14 and 30 not fully recovered | The 32 questions, risk factor matrices, risk levels, procurement questions |
| AI agent usage and deployment guidance, Oct 2025 (<https://www.digital.nsw.gov.au/sites/default/files/2025-10/ai-agent-usage-and-deployment-guidance.pdf>) | P (fork) | Guideline only, not mandatory; 15 agent-owner responsibilities |
| Generative AI: basic guidance (<https://www.digital.nsw.gov.au/policy/artificial-intelligence/generative-ai-basic-guidance>) | P (fork) | Staff use rules |
| Digital Assurance Framework v3.1, 2024 (<https://www.digital.nsw.gov.au/sites/default/files/2024-05/Digital-Assurance-Framework-2024.pdf>) | P (fork) | $5m registration; tiers; AI risk scores |
| NSW Cyber Security Policy 2026–2027 (<https://www.digital.nsw.gov.au/sites/default/files/2026-06/nsw-cyber-security-policy-2026-2027.pdf>); DCS-2026-03 | P (fork) | Requirements 1.1 to 3.15; ML1; 24-hour reporting; supplier clauses |
| PBD-2025-03; ICTA August 2025; Core& One Core Terms August 2025; AI Procurement Essentials, 6 May 2026 (<https://www.info.buy.nsw.gov.au>) | P (fork) | AI clauses, data location, model-change notice |

### NSW law (read by a fork on 2026-10-26; IPC AI PIA guide and s 19(2) fact sheet also read by the coordinator)

| Source | Mark | Used for |
| --- | --- | --- |
| IPC, PPIP Act page and IPP fact sheet, August 2026 (<https://www.ipc.nsw.gov.au/privacy/nsw-privacy-laws/ppip>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-information-protection-principles-ipps>) | P | The 12 IPPs |
| IPC, Fact Sheet: Transborder Disclosure Principle, s 19(2), November 2019 (<https://www.ipc.nsw.gov.au/resources/fact-sheet-transborder-disclosure-principle-section-192>) | P | s 19(2) grounds; the "reasonable steps" contract minimum |
| PPIP Act 1998, 2016 compilation, council-hosted copy (<https://www.campbelltown.nsw.gov.au/files/sharedassets/public/v/1/information-pages/documents/privacyandpersonalinformationprotectionact1998.pdf>) | S (superseded) | Section headings; s 4(4); s 12(d); s 19(3) to (5) repealed; s 33 |
| IPC, Guide to making privacy management plans, May 2026 (<https://www.ipc.nsw.gov.au/resources/guide-guide-making-privacy-management-plans>) | P | s 33(2)(c1); AI and ADM content |
| IPC, MNDB guide, July 2024; Data breaches and contracted service providers, January 2023; Part 6A assessment guidelines, September 2023 (<https://www.ipc.nsw.gov.au/resources/guide-mandatory-notification-data-breach-scheme-guide-managing-data-breaches-accordance-ppip-act>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-data-breaches-and-contracted-service-providers>, <https://www.ipc.nsw.gov.au/resources/guideline-guidelines-assessment-data-breaches-under-part-6a-ppip-act>) | P | Commencement 28 November 2023; ss 59C, 59E, 59M, 59N, 59O, 59P, 59ZD, 59ZE |
| IPC, Guide to undertaking PIAs on AI systems and projects, December 2024 (<https://www.ipc.nsw.gov.au/resources/guide-guide-undertaking-privacy-impact-assessments-ai-systems-and-projects>) | P | B5 crosswalk |
| IPC, Guide to PIAs in NSW, May 2020; Privacy by design fact sheet; Guide: privacy risks of generative AI tools, May 2026 (<https://www.ipc.nsw.gov.au/resources/guide-guide-privacy-impact-assessments-nsw>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-privacy-design>, <https://www.ipc.nsw.gov.au/resources/guide-privacy-risks-associated-use-generative-ai-tools>) | P | PIA steps; PIA expected, not statutory; vendor terms |
| IPC, AI and ADM desktop review release, 17 November 2025 (<https://www.ipc.nsw.gov.au/news-events/media-releases/new-review-considers-how-agencies-are-incorporating-aiadm-their-transparency-and-accountability-policies>) | P | AI disclosure in agency information guides and PMPs |
| IPC, HRIP Act page; HPP fact sheet, May 2026 (<https://www.ipc.nsw.gov.au/privacy/nsw-privacy-laws/hrip>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-health-privacy-principles-hpps-agencies>) | P | The 15 HPPs; who is bound; HPP 14 |
| IPC, ADM and GIPA fact sheet, August 2024; Government contractors and GIPA; contract register checklist; s 121 fact sheet; open access fact sheet; digital records and GIPA (<https://www.ipc.nsw.gov.au/resources/fact-sheet-automated-decision-making-digital-government-and-preserving-information-access-rights-agencies>, <https://www.ipc.nsw.gov.au/information-access/agencies/government-contractors-and-gipa-act>, <https://www.ipc.nsw.gov.au/media/726>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-guide-section-121-gipa-act-agencies>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-open-access-information-agencies>, <https://www.ipc.nsw.gov.au/resources/fact-sheet-digital-records-and-gipa-act>) | P | Contracts register of $150,000 or more; ss 29 to 35; s 121; AI and government information |
| State Records NSW, legislation and compliance; AI and recordkeeping, last updated 9 February 2024; For the Record, October 2026 (<https://www.nsw.gov.au/nsw-government/recordkeeping/legislation-and-compliance>, <https://www.nsw.gov.au/nsw-government/recordkeeping/create-and-capture/ai-and-recordkeeping>, <https://www.nsw.gov.au/departments-and-agencies/dciths/state-records-nsw/news-and-updates/for-record-october-2026>) | P | State Records Act 1998 still governs; AI records are State records |
| State Records Regulation 2024 as made (<https://legislation.nsw.gov.au/view/pdf/asmade/sl-2024-419>) | S (search result only; site returned 403) | Commencement 1 September 2024 |
| DPC circular C2005-37, Workplace Surveillance Act 2005 (<https://arp.nsw.gov.au/c2005-37-workplace-surveillance-act-2005>) | P | Commencement; s 10 notice contents |
| NSW Law Reform Commission, Anti-Discrimination Act review, last updated 26 October 2026 (<https://lawreform.nsw.gov.au/content/dcj/law-reform-commission/law-reform-commission-home/projects/anti-discrimination-act-review.html>); ADNSW religious vilification news and types of discrimination (<https://antidiscrimination.nsw.gov.au>) | P | Reform status; attributes |
| Privacy Act 1988, Compilation No. 104, 4 June 2026 (<https://www.legislation.gov.au/C2004A03712/latest/text>) | P | s 6(1) "State contract"; s 7B(5); s 95C; Schedule 2 |
| legislation.nsw.gov.au, AustLII, parliament.nsw.gov.au | U (HTTP 403 on 2026-10-26) | Current NSW statute text not read |

---

# Part A. Commonwealth: DTA Policy for the responsible use of AI in government

## A1. Status and mandatory requirements

**Version and application (P).** "This version of the policy came into effect
15 December 2025 (v2.0), with minor updates published on 21 October 2026
(v2.1). It replaces version 1.1 of the policy, which came into effect
1 September 2024."
- All non-corporate Commonwealth entities (NCEs) "must apply this policy".
- Corporate Commonwealth entities are encouraged to.
- Excluded: the defence portfolio, and the national intelligence community
  as defined in s 4 of the Office of National Intelligence Act 2018. That
  covers ONI, ASD, ASIO, ASIS, AGO, DIO and ACIC, plus the intelligence roles
  of AUSTRAC, the AFP, Home Affairs and Defence.

**Mandatory requirements and their dates.** Time limits run from 15 December
2025, the date v2.0 took effect.

| Requirement | What it says (P) | Deadline in words |
| --- | --- | --- |
| Accountable official(s) | Designate them under the Standard for accountability; notify the DTA at ai@dta.gov.au; they notify the DTA of any new high-risk use case | Carried over from v1.1, which first applied on 30 November 2024 |
| AI transparency statement | Public statement per the Standard; reviewed "annually or sooner"; notify the DTA of each publication and change | In force since 28 February 2025 (v1.x); current Standard v2.1 updated 20 October 2026 |
| Strategic position on AI adoption | Develop and communicate it to staff | Within 6 months: by 15 June 2026 |
| Operationalise responsible use | A process for adopting use cases; staff informed of the AI Ethics Principles; staff and public pathways to report AI safety concerns and incidents; AI incident processes aligned to ICT incident management | Within 12 months: by 15 December 2026 |
| Accountable use case owners | One per in-scope use case; the accountable official keeps a register of them | Within 12 months: by 15 December 2026 |
| Internal AI use case register | Minimum fields set by the Standard for accountability (A5); shared with the DTA every 6 months | Created within 12 months: by 15 December 2026; then every 6 months |
| Staff training | Mandatory training for all staff (the AI fundamentals module may be used) | Within 12 months: by 15 December 2026 |
| AI use case impact assessment | Assess every new use case against Appendix C at design. For in-scope use cases, conduct the impact assessment with the DTA tool, or an internal process that "integrates all provisions" and gives "the same (or a higher) risk outcome". Start at design and finalise, with agreed treatments applied, before deployment | Assessments begin within 12 months: in-scope use cases by 15 December 2026. Existing use cases not yet assessed by 30 April 2027 |
| Medium risk (inherent) | "Should consider" governing through a designated board or senior executive | Not applicable |
| High risk (inherent) | Report to the accountable official with the reasons, mitigations and residual risks; govern through a board or senior executive; once deployment is decided, report to the DTA through the accountable official; review at least every 12 months | At the deployment decision, then every 12 months |
| Re-validation | Monitor and evaluate. Re-validate on a "material change in the use case scope, usage or operation". Agencies "should also monitor changes that are not initiated by the agency. For example, vendor changes ... Agencies could also ask vendors to provide information on updates through contractual mechanisms" | Ongoing |

**Strongly recommended, not mandatory (P):**
- The AI technical standard (42 statements).
- The Guidance on AI procurement in government.
- The **Agentic AI addendum**: "Agencies exploring, developing or using
  agentic AI are expected to apply this addendum in conjunction with the AI
  technical standard." The addendum's own wording is "expected" but the
  policy does not make it mandatory. Record it as strongly recommended.

**AI Review Committee (Commonwealth, P).** It sits under the AI Plan for the
APS.
- It gives "expert and non-binding advice" on use cases, before deployment,
  that an agency "assessed as having a residual high-risk rating" or
  "identified as highly sensitive, novel or complex" (ToR 2.2).
- It may also review serious AI incidents after the agency has concluded its
  response (ToR 2.5, 2.6).
- It considers information classified up to PROTECTED only (ToR 2.7).
- Its advice is not endorsement or compliance advice (ToR 2.9).
- The committee is chaired by the DTA CEO, and its members include the
  Privacy Commissioner.
- The pack names a possible referral as a calendar wait `W`.

## A2. The AI impact assessment tool v1.0 (1 December 2025): structure

Read in full from the Word template (P). The tool's "Document control"
table shows a single row: v1.0, published 01/12/2025. The template says to
check <https://digital.gov.au/ai/ai-in-government-policy> for the latest
version. **The crosswalk records "tool v1.0, 1 December 2025, checked
2026-10-26".**

Roles (P):
- The **assessing officer** completes the assessment and determines the risk
  ratings.
- The **approving officer** approves it, including the inherent risk
  ratings.
- The **accountable use case owner** is a separate policy role.
- **Expert contributors** are recorded at 1.10.

Flow (P):
- Complete sections 1 to 4.
- "If all inherent risks are rated low", the approving officer can endorse
  concluding at section 4.
- "If any of the inherent risks at section 3 are rated medium or high,
  proceed to the full assessment and complete sections 5 to 12."
- Section 3 rates **inherent** risk, "before it is treated with controls".
  The overall rating at 3.9 is the highest of 3.1 to 3.8.

Risk scales (P):
- Likelihood: almost certain (91% and above), likely (61–90%), possible
  (31–60%), unlikely (5–30%), rare (under 5%).
- Consequence: insignificant, minor, moderate, major, severe.
- The 5×5 matrix gives Low, Medium or High.
- "If you are unsure, take a precautionary approach and rate the
  consequence as at least 'possible'." The template applies "possible" to
  consequence, although "possible" is a likelihood level. Quote it as
  written and do not repair it.

Form quirks to note (P):
- Question 3.7's consequence descriptors for "Major" and "Moderate" are
  identical in the template ("System feature causes data leak or access
  issue. Contained but serious.").
- Question 7.3 ("What measures are in place ...") offers Yes/No/Not
  applicable boxes.
- Question 1.7's four usage patterns (decision-making and administrative
  action; analytics for insights; workplace productivity; image processing)
  predate the seven patterns of Appendix D v2.1: decision-making and
  administrative action; analytics; strategic support; workplace
  productivity; workflow automation; image processing; coding.
- The draft answers in the form's order but uses the Appendix D v2.1 names,
  with `agency:` to confirm which list the agency's copy of the form uses.

## A3. Crosswalk: DTA AI impact assessment tool v1.0

Columns:
- **Form** quotes or closely paraphrases the official question, with its
  number.
- **Answer needs** is what the answer must contain.
- **From our records** is where the answer usually comes from.
- `agency:` marks a question only the agency can answer; `counsel:` marks a
  legal question.

Record sources:
- discovery brief: `docs/discovery/<topic>.md`;
- design: R, C, D and SB IDs, accepted risks, deferred controls;
- plan: G and A goals, M, I and W records;
- evaluation reports;
- pack documents: `regulatory-memo.md`, `impact-assessment.md` (H and B
  rows), `privacy-impact-input-pack.md`, `system-card.md`,
  `security-questionnaire.md`.

### Section 1. Basic information (threshold)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 1.1 | AI use case profile: name of AI use case; internal reference number or identifier; lead agency | Name, agency reference, lead agency | Name: design title. Reference and lead agency: `agency:` |
| 1.2 | Establishing impact assessment responsibilities: assessing officer (name, position/team, email); accountable use case owner(s); approving officer | Three agency officers | `agency:` for all three. The pack writes `gap: assessing officer, approving officer, use case owner` until named, sourced as `source: <role>, <date>` |
| 1.3 | Additional roles and responsibilities: "people at your agency or third parties with responsibilities related to this AI use case. For example, responsibilities for developing the system, including external suppliers, monitoring ... or data governance" | Rows for the consultancy (developer), Google (model and cloud provider), operators | Memo Roles section; design operations and access decisions (D); SOW support terms. Consultancy rows from the brief's stakeholders |
| 1.4 | AI use case description: "In plain language, briefly explain how you are using or intend to use AI" | Two or three plain sentences | System card "Intended use"; memo "System and intended purpose" (R and C IDs) |
| 1.5 | In-scope use case: select any of five criteria (more than insignificant harm; materially influence administrative decisions; public interaction or significant impact without human review; personal or sensitive data or security classified information; elevated risk as directed by the DTA) or "Not applicable" | Ticked criteria, each with its fact | Harm: brief harms and cost of a wrong answer. Administrative decisions: design contracts on decisions (C), memo APP 1.7 table. Public interaction: design channels and review contracts (C, M share reviewed). Personal data: brief §4 data register, input pack. DTA direction: `agency:`. Whether it is in scope: `counsel:` / `agency:` |
| 1.6 | Type of AI technology: "Briefly explain the types of AI technology" | For example: generative AI (LLM), agentic orchestration with tool calls, retrieval | Design model decision (D: pinned model ID), agent topology (D), tools table |
| 1.7 | Usage pattern: select all that apply ("Source: Classification system for AI use") | Patterns from Appendix D v2.1 | Design contracts and channels. An ADK agent typically ticks workflow automation and/or decision-making and administrative action, plus strategic support or workplace productivity. `agency:` confirm which list their form uses (A2) |
| 1.8 | Administrative decisions: only if 1.7 is decision-making and administrative action **and** "AI automated decision-making is used for an administrative decision under an Act": "Provide the legislative authority for automating such a decision". Advisory note: "Express legislative authority is generally required" | The statute and section, or `n/a:` | `counsel:` always. Facts: design decision contracts (C) showing whether the agent decides or drafts, M record of the share reviewed |
| 1.9 | Domain: select all that apply (service delivery; compliance and fraud detection; law enforcement, intelligence and security; policy and legal; scientific; corporate and enabling) | Domain(s) | Brief context; `agency:` confirm |
| 1.10 | Expert contributions: name, role and expertise, date last consulted, input and resulting changes | Rows per expert | Consultancy experts from the plan (reviewers named on G goals), security review (SB evidence), evaluation lead (M). Agency experts: `agency:` |
| 1.11 | Impact assessment review log: review type (pre-deployment / re-validation), reasons, date, post-review changes | Log rows | Plan goal history: design revisions, pilot goals, release records. Re-validation triggers from impact-assessment.md "Monitoring and review" |

### Section 2. Purpose and expected benefits (threshold)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 2.1 | Problem definition: "Identify the problem you are trying to solve" | Problem statement | Discovery brief §1 (problem, current process, cost of the status quo) |
| 2.2 | AI use case purpose: "Describe the purpose of your use of AI, focusing on how it will address the problem" | Purpose and mechanism | Design purpose and R IDs; system card Intended use |
| 2.3 | Non-AI alternatives: "Outline non-AI alternatives that could address this problem" | Alternatives and why rejected | Brief options considered; design decisions recording rejected alternatives (D). `gap:` if none recorded |
| 2.4 | Identifying stakeholders (Attachment A stakeholder mapping aid): stakeholder group and how affected | Groups from Attachment A: end users; evaluation or decision subjects; oversight team; system owner or deployer; AI model or system engineers; rights holders; malicious actors; bystanders; regulators; other government agencies; civil society organisations; communities or groups; associated parties; staff and other personnel (including unions); intermediaries | impact-assessment.md "Interested parties"; brief stakeholders and harms. Malicious actors: adk-agent-security threat model (SB17, SB18). Unions and staff: `agency:` |
| 2.5 | Expected benefits: "What are the expected benefits"; advisory note: supported by "quantitative and/or qualitative analysis" | Benefits with evidence | impact-assessment.md B rows; brief KPIs; plan M records (measured) or `hypothesis:` |

### Section 3. Inherent risk assessment (threshold)

Each of 3.1 to 3.8 asks for a consequence (insignificant to severe), a
likelihood (rare to almost certain), a risk rating (low, medium or high) and
a "Rationale for risk rating including any existing controls". The rating is
**inherent**, before treatment. The pack proposes ratings marked
`assumption:` with their basis. The assessing officer sets them and the
approving officer approves them (`agency:`).

| # | Form (the risk asked about) | Prompts in the form, abridged (P) | From our records |
| --- | --- | --- | --- |
| 3.1 | Risk of reducing service accessibility and inclusion | Fundamental or critical services? New barriers? Low digital literacy? Language or culture? Answers the public would misinterpret? Can users get human verification or review? | Brief users and channels; design accessibility and hand-off contracts (C); system card "AI disclosure and hand-off"; M records on hand-off time; languages not evaluated (system card Limits) |
| 3.2 | Risk of unfair discrimination | Replicate or amplify bias? Proxies (postcode, education, country of birth)? Used in assessment, eligibility, employment or resource allocation? Can users identify bias? | impact-assessment.md "Adverse impact and equality" (M IDs or `gap:`); design decision contracts; proxies removed (C) |
| 3.3 | Risk of perpetuating stereotyping or demeaning representations | Generalising individuals to groups? Outputs reinforcing stereotypes? Misrepresenting marginalised communities? Tested with diverse demographics? Defamation risk from false statements about an individual | Evaluation reports (adversarial and fairness sets); grounding and citation contracts (C); system card Limits |
| 3.4 | Risk of harm | Physical, psychological, social, economic, reputational or environmental harm? Deprioritise or misclassify? Physical environments or machinery? Critical infrastructure? | Brief harms and cost of a wrong answer; impact-assessment.md H rows; tool-tier and confirmation contracts (C, SB18) |
| 3.5 | Risk of AI use raising privacy concerns | Collection, storage or disclosure of personal information, including sensitive? New or changed handling? Significant privacy impact? A privacy threshold assessment, and a PIA for "high privacy risk" projects under the Agencies Privacy Code | privacy-impact-input-pack.md (Screening, Data flows, People and data categories); `counsel:` high privacy risk |
| 3.6 | Risk raising security concerns – data aspects | Breach harm? Data under legislative, classification, contractual or equitable confidentiality (protected, security classified, commercial, law enforcement, national security, confidential, personal information)? External data sources governed? Do inputs and outputs leave agency systems? Third-party access and secondary use (ingestion, data mining)? Access records? Breach response plan? | Design data register and classification (brief §4, D); input pack "Model provider data use" and "Recipients and regions"; security questionnaire answers on logging (SB14), sub-processors and incident response; security classification: `agency:` |
| 3.7 | Risk of raising security concerns – system aspects | Externally developed, open source or pretrained model? Explainable, testable, auditable? Safeguards, circuit-breaker or shutdown? Anomaly monitoring? Known vulnerabilities and dependencies? On premises or cloud, and are the servers in Australia? Novel algorithms? | Pinned model and lifecycle (D); evaluation and adversarial suite (M, SB17); kill switch and rollback (D, G); observability alerts; dependency audits (SB15, SB21, SB24); hosting region and model processing region (D, model page `source:`) |
| 3.8 | Risk to reputation or public confidence | Fails public expectations of government as an exemplar? Outcomes that appear unfair or insensitive? | Brief harms; impact-assessment.md H rows; `agency:` (the agency's own appetite) |
| 3.9 | Overall inherent risk rating: "Use the highest risk rating identified" in 3.1 to 3.8, plus a rationale | Highest of 3.1 to 3.8 | Computed from the rows above; `agency:` approval |

### Section 4. Threshold assessment outcome

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 4.1 | Assessing officer recommendation: "A full assessment is necessary / is not necessary"; comments; name, position, date. Guidance: if any risk is medium or higher, the officer must complete a full assessment, amend the scope until the threshold rating is low, or not proceed | Recommendation | `agency:` The pack proposes, for example: "Full assessment necessary: 3.5 rated medium (assumption: personal information in prompts, privacy-impact-input-pack.md)" |
| 4.2 | Approving officer review: agrees a full assessment is or is not necessary; comments; name, position, date | Decision | `agency:` only. A calendar wait `W` in the plan |

### Section 5. Fairness (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 5.1 | Defining fairness: "Do you have a clear definition of what constitutes a fair process and/or outcome in the context of your use of AI?" Yes / No / N/A; explain | Operational fairness definition | impact-assessment.md "Adverse impact and equality"; design acceptance criteria (R, C); `agency:` for the policy definition of fairness in their service |
| 5.2 | Measuring fairness: "Do you have a way of measuring the fairness of system outcomes quantitatively or qualitatively?" | Metric, test, sample | M records on outcome rates by group; evaluation reports; `gap:` with a goal for adk-agent-evaluation if unmeasured |

### Section 6. Reliability and safety (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 6.1 | Data suitability: "can you explain why the chosen data is suitable?" (accuracy, timeliness, completeness, consistency, lineage, provenance, volume; permissions and rights) | Data sources, quality, rights | Brief §4 data register; RAG and memory design (D); evaluation set provenance; `agency:` data permissions |
| 6.2 | Indigenous data: "If your AI system uses Indigenous data, including where any outputs relate to Indigenous people, have you ensured ... consistent with the Framework for Governance of Indigenous Data?" | Yes / No / N/A with reason | Brief data register; `agency:` (data custodians); usually `n/a:` with reason or `gap:` |
| 6.3 | Suitability of procured AI system: "If you are procuring an AI model, can you explain its suitability?" Contract terms on testing, support, data governance, privacy, security, intellectual property and warranties. Guidance lists further supplier considerations: overseas hosting and FOCI, supply chain, model evaluation, versioning, liability, data handover or destruction, controls on malfunction, hallucination, bias and drift measures, records the supplier provides, IP in inputs and outputs | Model choice rationale and contract terms | Design model decision (D) with the model page and lifecycle row; input pack "Model provider data use"; security questionnaire "Sub-processors"; contract terms: `agency:` / `counsel:` |
| 6.4 | Testing: "Has the AI system been tested sufficiently and are you satisfied with its reliability and safety?"; concerns from testing, or the elements of a test plan | Results and gaps | Evaluation reports; plan M records; system card "Evaluation results" and "Not yet measured" |
| 6.5 | Pilot: "Have you conducted, or will you conduct, a pilot of your use case before deploying?" | Pilot plan or results | Plan pilot goal (G), its acceptance cases (A), M records from the pilot |
| 6.6 | Monitoring: "Have you established a plan to monitor and evaluate the performance of your AI system?" | SLIs, alerts, owners | Observability design (adk-agent-observability); impact-assessment.md "Monitoring and review"; release triggers |
| 6.7 | Preparedness to intervene or disengage: "clear processes for human intervention or safely disengaging the AI system" | Override, stop, rollback | System card "Human oversight" (stop and rollback); approval contracts (SB18); kill switch decision (D); operational guardrails |
| 6.8 | Training of AI system operators: "a process ... to ensure operators ... are sufficiently skilled and trained" | Training plan | Plan handover goal; `agency:` (agency training programme) |

### Section 7. Privacy protection and security (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 7.1 | Minimise and protect personal information: "Are you satisfied that any collection, use or disclosure of personal information complies with the APPs?" | APP analysis | privacy-impact-input-pack.md "Australia: APP compliance check"; `counsel:` |
| 7.2 | Privacy threshold and/or impact assessment: "Record where you have stored your privacy threshold assessment and, if applicable, your privacy impact assessment" | Repository location | `agency:` (their records system). The pack supplies the input pack as the PIA input |
| 7.3 | Security risks: engage the agency's IT Security Adviser (ITSA); consider the PSPF, ISM and ASD advice on Engaging with AI. "What measures are in place to address security risks arising from the operation of the AI?" | Controls with status | security-questionnaire.md answer bank; design SB table; adk-agent-security findings; ITSA review: `agency:` and a calendar wait `W` |

### Section 8. Transparency and explainability (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 8.1 | Consultation: "Have you consulted stakeholders identified in section 2.4?" | Who, when, outcome | Brief stakeholder interviews (dated sources); `agency:` for community and union consultation |
| 8.2 | Public visibility: "Will appropriate information be made publicly available, such as the scope and goals related to the use of AI?" | Publication plan | System card (public version); agency transparency statement (A4); `agency:` |
| 8.3 | Maintain appropriate documentation and records: "processes to maintain appropriate documentation and records throughout the lifecycle". Guidance names system factsheet or model card, datasheets, system decision registries, and reliability and safety documentation | Records kept and where | System card (the factsheet); data register (the datasheet); decision lineage logging (C, observability); design and plan as lifecycle records; records retention: `agency:` (Archives Act or agency records authority) |
| 8.4 | Disclosing AI interactions and outputs: "Will people be informed when they interact with the AI system or receive outputs generated by AI?" and "Will members of the public interacting with the system be provided with the ability to request a non-AI alternative?" | Disclosure mechanism; non-AI route | System card "AI disclosure and hand-off"; disclosure contract (C with its test); hand-off route and M time to connect |
| 8.5 | Offer appropriate explanations: "Will your AI system allow for appropriate explanation of the factors leading to AI-generated decisions, recommendations or insights?" | Explanation design | System card "Automated-decision disclosure: meaningful information about the logic"; grounding and citation contracts (C); trace retention (SB14) |

### Section 9. Contestability (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 9.1 | Notification of AI affecting rights: "Will individuals ... be notified if an administrative action with a legal or significant effect on them was materially influenced by the AI system?" | Notification design | System card automated-decision disclosure; memo APP 1.7 table; `counsel:` (administrative law; "materially influenced") |
| 9.2 | Challenging administrative actions influenced by AI: "Is there a timely and accessible process to challenge the administrative actions discussed at section 9.1?" | Review route | System card "Human review, representations and contest"; `agency:` (the agency's internal review and external merits review route) |

### Section 10. Human-centred values (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 10.1 | Incorporating diversity: "satisfied that you have incorporated diversity and people with appropriately diverse skills, experiences and backgrounds throughout the lifecycle?" | Team, data and consultation diversity | Evaluation set composition (M); brief stakeholders consulted; `agency:` |
| 10.2 | Human rights obligations (complete last): "Have you consulted an appropriate source of advice or otherwise ensured that your AI use case and the use of data align with human rights obligations?" | Advice and outcome | `counsel:` always. The pack lists the facts: decisions affecting people, data categories, contest route |

### Section 11. Accountability (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 11.1 | Ensuring accountability during the lifecycle: "Are there mechanisms in place to ensure responsibility and accountability by the agency and relevant individuals for AI systems and their outcomes?" | Owners, RACI, governance | Memo Roles; design owners; residual risk acceptance (impact-assessment.md); agency governance board: `agency:` |

### Section 12. Use case review and next steps (full assessment)

| # | Form | Answer needs | From our records |
| --- | --- | --- | --- |
| 12.1 | Alignment with relevant legal frameworks: "Have you identified and documented all agency specific legislation, or regulatory instruments that are relevant?" | Agency's enabling Act and others | Memo jurisdiction screen and Australian sections; agency-specific statutes: `agency:` / `counsel:` |
| 12.2 | Legal advice: identified the need? where is it stored? ("should not be disclosed to anyone other than those who need to know") | Yes or no; repository | `agency:` only. The pack lists its `counsel:` questions without the advice |
| 12.3 | Risk summary table: each inherent risk rated medium or high in section 3, with risk treatments and residual risk (low, medium or high) | Treatments per risk | impact-assessment.md "Measures" and "Residual risk and decision" (H → C, SB with status); planned treatments as `planned G<n>`, never "in place" |
| 12.4 | Overall residual risk rating and rationale | Low, medium or high | Proposed from 12.3, marked `assumption:`; `agency:` sets it |
| 12.5 | Internal governance body review: required if inherent risk is high; recommendation and agreed next steps | Board outcome | `agency:`; calendar wait `W` |
| Att. A | Stakeholder mapping aid | Supports 2.4 | As 2.4 |

## A4. Crosswalk: AI transparency statement (Standard v2.1, 20 October 2026)

The statement is **agency-level** and need not list use cases (P). The
pack supplies the facts for this use case. The agency writes and publishes
the statement.

| Required content (P) | Answer needs | From our records |
| --- | --- | --- |
| "the intentions behind why the agency uses AI or is considering its adoption" | The agency's rationale | `agency:` (the use case's purpose feeds it: system card Intended use) |
| "classification of AI use according to usage patterns and domains, as listed at Appendix D" | Pattern and domain for this use case | As DTA tool 1.7 and 1.9 |
| "classification of use where the public may directly interact with, or be significantly impacted by, AI or its outputs without human review" | Yes or no, and where | Design channels and review contracts (C); M share reviewed |
| "measures to monitor the effectiveness of deployed AI systems and protect the public against negative impacts" | Monitoring and safeguards | impact-assessment.md "Monitoring and review"; system card Human oversight |
| "overview of compliance with the requirements under the Policy" | Agency compliance | `agency:` |
| "compliance with applicable legislation and regulation" | Laws | Memo screen; `counsel:` / `agency:` |
| "when the statement was most recently updated" | Date | `agency:` |
| Plain language, Style Manual, contact email; published on the agency website; reviewed yearly, on a significant change, or when a new factor affects accuracy; DTA notified | Form rules | `agency:`. The pack flags "new factor materially impacts accuracy" when this use case changes the agency's AI profile |

## A5. Crosswalk: internal AI use case register (Standard for accountability v2.1)

| Minimum field (P) | From our records |
| --- | --- |
| Use case name | Design title |
| Agency identifier (reference number) | `agency:` |
| Description (what the AI does, business objective, underpinning product's name) | System card Intended use; model and product names (D) |
| AI technology type (generative AI, machine learning, natural language processing and/or computer vision) | Design model decision (D) |
| Lifecycle stage (Discover, Operate or Retire) | Plan status |
| Use of the Technical standard (not applied, partially applied or fully applied) | Pack conformance table against the technical standard and AGT (A6); `agency:` confirms |
| Domain (Appendix D) | As 1.9 |
| Usage pattern (Appendix D) | As 1.7 |
| Accountable use case owner (name and email address) | `agency:` |
| In-scope criteria met (Appendix C) | As 1.5 |
| Inherent risk rating | DTA tool 3.9 (`agency:` approved) |
| Residual risk rating | DTA tool 12.4 |
| Date the impact assessment was last updated | `agency:` |
| High-risk only: last review date; next review date | `agency:`; plan wait `W` |

High-risk notification to the DTA (accountable official): type of AI,
intended application, how the agency arrived at "high-risk", any
sensitivities (P). The pack supplies the first three from the system card
and the impact assessment.

## A6. Agentic AI addendum (updated 4 June 2026): conformance list

Strongly recommended, not mandatory. The statement and criterion titles are
quoted from the DTA pages (P). Map each to the toolkit's evidence.

| Statement / criterion (P) | Toolkit evidence |
| --- | --- |
| AGT.1 Establish governance and safeguards ... agentic AI systems | Memo Roles; design owners |
| AGT.1.1 Identify and assign responsibilities for agents and human accountability for decisions | Agent and tool ownership table (D); human approver contracts (SB18) |
| AGT.1.2 Identify effective human oversight and intervene when necessary | Approval and confirmation contracts (adk-operational-guardrails); system card Human oversight |
| AGT.1.3 Explain agentic system decision-making processes | Trace and decision lineage (observability); system card logic |
| AGT.1.4 Establish an orchestration layer | Workflow design (adk-workflow-design) D IDs |
| AGT.2 / AGT.2.1 Establish (robust) memory management mechanisms | Memory scope, retention and erasure contracts (adk-memory-architecture) |
| AGT.3 Design for agentic workflow; AGT.3.1 business needs and goals; 3.2 sequence and logical order of tasks and agents; 3.3 guardrails and constraints; 3.4 self-correction, fail-safes, feedback loops; 3.5 choose the tools; 3.6 conditional branches and decision points; 3.7 scalability and complexity | Design R, D, C; tool interface design; invocation limits and budgets (SB19, SB25); repair loops (adk-model-and-output-contracts) |
| AGT.4 Orchestrate routing and data flow management; 4.1 secure, efficient, reliable data exchange between agents; 4.2 dynamic routing to appropriate agents | Session-state handoff contracts; A2A or MCP interoperability decisions |
| AGT.5 Select appropriate agent, model and AI technology; 5.1 aligns with use case; 5.2 trade-offs selecting LLMs or pre-trained models; 5.3 prompt engineering technique | Model decision (D) with lifecycle; instruction design records |
| AGT.6 Continuous evaluation; 6.1 robustness to unexpected inputs; 6.2 agent–tool interaction; 6.3 agent–environment interaction; 6.4 agent–memory interaction | Evaluation reports, adversarial suite (M, SB17), memory replay tests |
| AGT.7 Select tools and protocols; 7.1 tools that let agents communicate, interact and expand capabilities; 7.2 standard protocols | MCP allowlist and pinning (SB), A2A cards |
| AGT.8 Ongoing monitoring; 8.1 individual agents and their environment; 8.2 "Establish a control tower to provide system oversight" | Observability dashboards, alerts, SLOs; the kill switch |
| Decommission (existing statement 41, criterion 147: securely decommission or repurpose computing resources) | Cleanup and teardown goals (deploy-adk-on-google-cloud) |

## A7. Contractors: what applies and what the agency expects

- **The policy binds the agency, not the vendor (P).** It applies to NCEs.
  The tool says it is "designed for Australian Government staff". Section
  1.3 records "external suppliers" among the people with responsibilities.
- **What agencies are told to ask vendors for (P):**
  - Under the policy, information on vendor-initiated changes "through
    contractual mechanisms".
  - The procurement considerations in the tool guidance at 6.3 (A3 above):
    contractual compliance with privacy and discrimination law, the AI
    Ethics Principles, the AI policy and the PSPF; training, monitoring and
    validation duties; records "of how agency data is used"; versioning;
    measures against hallucination, bias and drift; and data handover or
    destruction.
- **DTA AI model clauses (published 17 March 2025; AGS description P, clause
  text S).**
  - Seller using AI in services: the buyer's approval, quality assurance of
    outputs, detailed records of AI use, banned AI systems.
  - Bespoke AI systems:
    - cl 2: intended use and statement of requirement;
    - cl 2.6: fairness, no discrimination on protected characteristics, no
      reputational risk;
    - cl 3: compliance with laws and policies, including new ones;
    - cl 4: Privacy Act, including eligible data breaches;
    - cl 5.1: human oversight, designed so that humans can effectively
      oversee and monitor it, with information for the buyer's oversight
      personnel;
    - cl 6.2.4: training, testing and monitoring that identify protected-
      characteristic disparity, bias, hallucination and drift;
    - cl 11: no data mining and no ingestion of buyer data into an LLM;
    - cl 13: comply with the buyer's AI policy, or ISO/IEC 42001:2023, or a
      specified AI risk management system.
- **Commonwealth contracts and the Privacy Act.** Under s 95B an agency must
  put terms in place so that the contracted service provider does not breach
  the APPs. Already in `australia.md`.
- **Pack consequence.** Write the DTA crosswalk draft as "Draft answers for
  the agency's assessing officer". The vendor-evidence pack is the system
  card, impact assessment, input pack and questionnaire, plus an
  "AI model clauses evidence" table: cl 5.1 → human oversight; cl 6.2.4 → M
  records and evaluation reports; cl 11 → input pack "Model provider data
  use"; cl 13 → the NIST AI RMF mapping in the impact assessment.

---

# Part B. NSW: AI Operational Policy and AI Assessment Framework

## B1. Status (all P unless marked)

- **DCS-2026-02 "Use of Artificial Intelligence by NSW Government
  Agencies".**
  - Issued 30 July 2026 by the Secretary, Department of Customer Service;
    updated 1 September 2026. Status: Active. Compliance: Mandatory.
  - Replaces DCS-2024-04.
  - Who must comply: advisory entities, departments, executive agencies
    related to departments, public financial corporations, public
    non-financial corporations, separate agencies, state owned
    corporations, statutory authorities and bodies, and NSW Government
    subsidiaries under the Corporations Act.
  - The Operational Policy itself excludes local government, universities
    and third-party suppliers (s 1.3, from the fork). The Cyber Security
    Policy is not mandatory for SOCs (fork). Note the difference.
- **NSW AI Operational Policy, Final v1.1.**
  - Cover date 30 July 2026. The fork read a version table showing v1.0
    approved by the Secretaries Board on 11 June 2026 and v1.1 approved on
    31 August 2026; the cover and the table disagree.
  - It "replaces the NSW AI Ethics Policy". The eight Australian AI Ethics
    Principles are now "the mandatory NSW Government AI ethical principles".
- **Mandatory agency requirements** (circular and policy page):
  1. adhere to Australia's AI Ethics Principles;
  2. appoint an Accountable Official as the point of coordination with NSW
     GovAI (within three months of issue, per the fork's read of the
     policy);
  3. establish governance and assurance of AI;
  4. register all AI use cases in the AIAF Platform and keep complete
     records across the lifecycle;
  5. apply the AIAF where registration requires it;
  6. refer high-risk and critical-risk use cases to the AI Review Committee;
  7. align ICT acceptable use policies;
  8. make AI literacy and policy training available.
- **Attestation:** a signed annual attestation to NSW GovAI "by 31 October
  each year, with the first attestation due by 31 October 2027".
- **AIAF Platform:** "From 30 September 2026, the AIAF Platform is the
  mandatory platform for registering and assessing AI use cases across the
  NSW Government". Offline numbered assessment only where SectorLink
  onboarding is outstanding; "It is not a general alternative to the
  platform".
- **Transition:** "agencies must continue to apply the existing AIAF
  Excel-based assessment process to all AI use cases until the platform is
  fully adopted".
- **AI Review Committee:** agencies "must refer critical and high-risk AI
  use cases"; NSW GovAI "may also refer medium-risk AI use cases ... where
  higher risk characteristics are present". Engage by emailing the AI
  Secretariat "within 5 business days of completing the AIAF". The advice is
  advisory and the agency keeps decision-making authority. Chair: Professor
  Ed Santow.
- **Digital Assurance Framework:** "Projects with a budget exceeding
  $5 million, or those funded through the Digital Restart Fund, receive
  additional central oversight to confirm AIAF compliance" (AIAF page). The
  DAF v3.1 requires ICT and digital projects with an estimated total cost of
  $5 million or more to register via the Assurance Portal (fork). **The
  answer to the brief's question:** the AI Review Committee trigger is the
  risk band (high or critical), not cost. Cost brings DAF gateway oversight,
  which then checks AIAF compliance.
- **NSW AI Ethics Policy and its five principles** (community benefit,
  fairness, privacy and security, transparency, accountability): superseded.
  They survive only as the section headings of the 2024 AIAF, which is still
  the Excel and offline process. The superseded policy page was not re-read
  (U, fork).
- **NSW AI Strategy:** the circular names "The AI Strategy" ("No changes
  were made to the AI Strategy"). It is the 2020 strategy as far as is known
  (U, page not read).
- **Generative AI: basic guidance** (P, fork, undated). No sensitive or
  personal data in web-based gen AI tools; cite or watermark gen AI use;
  fact-check; "You are responsible for the content you use". Per the fork,
  gen AI must not be used in administrative decision-making until the AIAF
  has been applied.
- **AI agent usage and deployment guidance** (October 2025, P, fork):
  "This is a guideline only. It is not mandatory." It lists 15 agent-owner
  responsibilities, including "Set and lock authority limits", "Disclose and
  label", "Maintain fail-safe plans" and "Manage upgrade dependencies".
  - Pilot checklist: exportable decision lineage (inputs → actions →
    outputs + timestamps); pre-approved LLMs.
  - Production checklist: update the AIAF assessment; register the agent in
    the asset register; "Limit agents per owner (default 3–5)".

**Risk bands (Operational Policy, P):**
- Low-risk: "can be easily reversed or corrected without causing any harm or
  damage".
- Medium-risk: "noticeable but ... generally limited and manageable".
- High-Risk: "substantial risk profile ... significant, affect trust or
  operations".
- Critical-risk: "the highest level of risk ... severe, widespread, or
  irreversible".

The 2024 AIAF used five levels: none, negligible or N/A; low; mid-range;
high; very high. It referred residual **high and very high** risk.

The Operational Policy says the AIAF applies an **intrinsic** risk approach:
"the risk of an AI use case as a function of what the use case involves and
how it is intended to be used, rather than how it may later be managed or
mitigated". The 2024 AIAF referred on **residual** risk. The NSW and DTA
regimes therefore point opposite ways: the DTA tool is inherent-then-residual
and the Commonwealth committee looks at residual high risk. The pack must say
which rating it proposes, and the agency sets it.

## B2. Crosswalk: AIAF Platform registration (Operational Policy Attachment A)

The platform's exact wording is behind SectorLink (`agency:`). The
Operational Policy publishes the baseline questions ("These will be tested
and implemented within the AIAF platform and will evolve"):

| # | Baseline question (P) | Answer needs | From our records |
| --- | --- | --- | --- |
| R1 | "Approved Tool – Are you using an agency-approved AI system, platform or product?" | Whether Gemini on Vertex AI and ADK on Cloud Run or Agent Runtime are on the agency's approved list | `agency:` (approved products list); design model and hosting decisions (D) |
| R2 | "Consequential Decision-Making – Is the AI being used to automate or materially influence decisions that affect a person's rights, entitlements, access to services, compliance outcomes, or other consequential decisions?" | Yes or no with facts | Design decision contracts (C), memo APP 1.7 table (the same facts), M share reviewed |
| R3 | "Elevated-Risk Use – Is the AI being used in a way that introduces elevated risk beyond routine productivity or analytical assistance?" | Yes or no | Agent autonomy and tools (C, SB18); public channel; personal data. Attachment A's registration triggers include "Autonomous or semi-autonomous AI interactions" and AI "embedded into operational workflows, systems, or public-facing services": an ADK agent with tools is normally "yes" |
| R4 | "Experimental Use – ... only for experimentation with synthetic, publicly available or non-sensitive information in an isolated environment, without informing real decisions, services or operational processes?" | Yes only for a POC on synthetic data | Design profile (proof of concept) and data floor; POC note |
| Reg | Registration details: "agency, responsible officer and use case details"; an Accountable Owner registers at agency, team or individual level | Owner, agency, description | `agency:` owner; description from the system card |

## B3. Crosswalk: 2024 AIAF self-assessment (the Excel and offline process)

The structure is from the Digital NSW 2024 document (88 pages; mirror copy,
S provenance):
1. Scope of applying the framework.
2. Self-assessment readiness.
3. Self-assessment and risk summary: basic information, then five principle
   sections.
4. Mitigation and next steps, with procurement considerations.
5. End of self-assessment.

Most questions branch on Yes / Partially / No / Unclear / N/A, with
"controls" such as "Pause the project". Every answer requires "You must
explain your answer". Risk factor matrices are rated very low or N/A, low,
mid-range, high or very high.

### Part 1. Scope: is the use potentially elevated risk? (unnumbered)

| Item (P content) | From our records |
| --- | --- |
| Operational impact: produces or directly influences an administrative decision (legal or similar significant effect) | Decision contracts (C); memo APP 1.7 table |
| Operational impact: triggers a real-world action with more than negligible effect | Tool tiers and write actions (C, SB18) |
| Autonomous: operates autonomously, or can produce harmful outputs without manual initiation | Workflow design (D); triggers and schedules |
| Automating decisions: automates at least one critical step in decision-making | Decision contracts (C) |
| Data sensitivity: trained on, or can output, sensitive information | Brief §4 data register; screening contracts (protect-adk-sensitive-data) |
| Unintended harms: failure, misuse or inappropriate deployment that could harm | Brief harms; H rows |
| Explainability and transparency: fails to provide explainability | Citation and grounding contracts; trace design |
| "All Generative AI solutions should be classified elevated risk" | An ADK agent on Gemini is elevated risk by definition |
| Do I need to use the framework? Buy AI and use / Embed AI and/or co-train / Develop AI and/or train / Automating decisions | A consultancy-built ADK agent is "Develop AI" or "Embed AI" (design decisions) |

### Part 2. Readiness (unnumbered)

| Item | From our records |
| --- | --- |
| Human rights prompts: restricts human rights, and is that publicly justifiable? Trade-offs between principles documented? Does the system suggest decisions to users? Should users be informed that outputs are algorithmic? HRIA recommended where rights are at risk | `counsel:` (human rights); facts from the system card disclosure and decision contracts |
| Responsible officers: Project Sponsor; Executive Business Sponsor; Technical System Owner; Data Governance owner ("must not all be held by the same person") | `agency:`; the consultancy's delivery lead is not a responsible officer. The technical owner may be shared, so record it as `agency:` |

### Part 3. Self-assessment

| # | Form (2024 AIAF, P content) | Answer needs | From our records |
| --- | --- | --- | --- |
| Info | Project or system name; how delivered (buy and use, embed AI or co-train, develop AI or co-train); phase (design and develop, verify and validate through pilot, deploy and evaluate, operate/monitor/maintain, re-evaluate); responsible officers defined?; contributors; next review date or milestone; business goals; problem; what the system is trying to achieve; "Why is an AI system the better way?" | Profile facts | Design profile and plan phase; brief §1; contributors from the plan; next review: plan wait `W` |
| CB benefits (optional) | Confidence in: better quality existing service; reduced processing times; financial savings; capability reusable by other agencies; new service; future innovation | Ratings with evidence | impact-assessment.md B rows; M records or `hypothesis:` |
| 1 | "Will the AI system improve on existing approaches to deliver the outcomes described in" the Human Services Outcomes Framework, Smart Places Outcomes Framework, NSW Treasury Budget Outcomes, agency strategic plans or another NSW outcomes framework? (controls: Partially → formal benefits review after pilot; Not sure → pause and prepare a Benefits Realisation Management Plan; No → do not proceed) | Which outcomes | `agency:` (strategic outcomes); brief KPIs |
| CB risk factors | Initial risk: new or existing service; discrimination from unintended bias; single point of failure; sufficient experienced human oversight; over-reliance, or ignoring the system because of high false-alert rates; clear link between operation and policy outcome; explainability of generated content and decisions | Ratings | H rows; design availability and fallback (D); review contracts and M share reviewed; evaluation false-positive rates (M) |
| 2 | "Were other, non-AI systems considered?" | Alternatives | As DTA 2.3 |
| 3 | "Does this system and the use of data align with relevant legislation?": PPIP Act; Anti-Discrimination Act 1977; GIPA Act 2009; State Records Act 1998; public interest directions under the PPIP and HRIP Acts; HRIP Act 2002; Public Health Act 2010; agency Acts (control: Unclear → pause and seek NSW legal advice or the Privacy Commissioner) | Each Act engaged | Memo NSW section (Part C of this note); `counsel:` |
| CB harms | Physical; psychological; environmental or community; unauthorised use of health or sensitive personal information; impact on a right, privilege or entitlement; unintended identification or misidentification; misapplication of a fine or penalty; other financial; incorrect advice or guidance; inconvenience or delay; erosion of trust; ethical implications; economic disruption; social equality; other | Ratings | Brief harms and cost of a wrong answer; H rows |
| 4 | "Could the AI system cause harms that are reversible?" (Yes and mid-range or higher → do not proceed until legal advice; consider ethics approval and an HRIA) | Reversibility facts | Correction and override paths (C); `counsel:` when mid-range or higher |
| 5 | "Could the AI system cause significant or irreversible harms?" (Yes → do not proceed until clear legal advice; ethics committee; HRIA) | Facts | H rows; `counsel:` |
| 6 | "Could the AI System result in secondary harms, or result in a cumulative harm from repeated application?" | Facts | Memory and accumulation design (adk-memory-architecture); H rows |
| Fairness risk factors | Incomplete or inaccurate data; excluding outlier data; informal data cleansing; informal bias detection (best practice is automated testing); reproducibility of re-runs; new associations when linking data; differences between training data and intended-use data | Ratings | Data register; evaluation repeat policy and variance (adk-release-engineering); grounding data quality |
| 7 | "Can you explain why you selected the data you're using in your system?" | Data rationale | As DTA 6.1 |
| 8 | "Is the data that you need for your system available and of appropriate quality given the potential harms identified?" | Availability and quality | Data register; RAG corpus decisions (D) |
| 9 | "Does your data reflect the population that will be impacted by your system?" | Representativeness | Evaluation set composition (M); `gap:` |
| 10 | "Have you considered how your AI system will address issues of diversity and inclusion (including geographic diversity)?" | Approach | Evaluation coverage; accessibility (C) |
| 11 | "Have you considered the impact with regard to gender and on minority groups ..." (disability, LGBTQIA+, CALD, Aboriginal and Torres Strait Islander people, children and young people, socio-economic) | Approach and tests | Adverse-impact section; languages and populations not evaluated (system card Limits) |
| 12 | "Do you have appropriate performance measures and targets (including fairness ones) for your AI system, given the potential harms?" (No and elevated risk → pause until established) | Metrics and targets | Design acceptance thresholds; release gate thresholds (adk-release-engineering) |
| 13 | "Do you have a way to monitor and calibrate the performance (including fairness) of your AI system?" (weekly calibration recommended for continuously training elevated-risk systems; monthly for low risk; custom for high or very high) | Monitoring cadence | Observability SLIs; online monitors; scheduled evaluation |
| P&S risk factors | Sensitive data by identifiable cohort size (>50 to <5): children; religious individuals; racially or ethnically diverse individuals; political opinions; trade union membership; gender or sexually diverse individuals; criminal record; specific health or genetic information; biometric information; other sensitive person-centred data | Ratings per category | Brief §4 data register; screening contracts; usually "not trained on agency data" for a Gemini agent, but outputs and memory can contain it |
| 14 | Privacy by design and security by design. The question text was not recovered from the extraction; the guidance applies the IPC's 7 Privacy by Design principles and the NSW Security Principles (Partially or No → pause; consider the Information and Privacy Commission or Cyber Security NSW) | Application of PbD and SbD | Input pack measures; SB table; `agency:` |
| 15 | "Have you completed a privacy impact assessment (either third party or self-assessed)?" (No → pause until completed) | PIA status | privacy-impact-input-pack.md (the input); `agency:` (the agency's PIA under the IPC guide) |
| 16 | "If you are using information about individuals who are reasonably identifiable, have you sought consent from citizens about using their data for this particular purpose?" (authorised use under legislation → clear legal or independent privacy advice; a public interest direction is possible) | Consent or authority | Input pack; `counsel:` (IPP 10 and 11 exceptions, legislative authority) |
| 17 | "Does your system adhere to the mandatory requirements in the NSW Cyber Security Policy? Have you considered end-to-end Security Principles for your system?" (No or partially → pause) | Policy mapping | Security questionnaire mapped to the NSW Cyber Security Policy (Part C); SB table |
| 18 | "Does your dataset include using sensitive data subjects as described by section 19 of the NSW Privacy and Personal Information Protection Act 1998?" (Yes → seek NSW legal advice or the Privacy Commissioner; consider ethics approval; use privacy-enhancing technology) | s 19(1) categories | Data register; screening; `counsel:` |
| T risk factors | Incomplete documentation; unable to explain a complex model's output; public unaware they interact with AI; low ability to incorporate user feedback; inability to audit past decisions that used AI input | Ratings | System card; disclosure contract; feedback capture (observability); trace retention |
| 19 | "Have you consulted with the relevant community that will benefit from (or be impacted by) the system?" (No → pause and develop a Community Engagement Plan) | Consultation | `agency:`; brief interviews |
| 20 | "Are the scope and goals of the project publicly available, and have you communicated how safeguards have been put in place to mitigate any potential harms?" | Publication | `agency:`; public system card |
| 21 | "Is there an easy and cost-effective way for people to appeal a decision that has been informed by your system?" (No → pause and establish an appeals process) | Appeal route | System card contest route; `agency:` |
| 22 | "Does the AI system allow for transparent explanation of the factors leading to a decision or insight?" (No, but a person decides → a process to readily reverse; No → pause) | Explanation, or a reversal process | System card logic; override and reversal (C) |
| A risk factors | Insufficient operator training; insufficient awareness of limitations among responsible officers; no or limited record of insight or decision history; third parties unable to audit insights or decisions | Ratings | Handover training (G); decision lineage logs; audit access (contract) |
| 23 | "Have you established who is responsible for: use of the AI outputs, insights and decisions? policy/outcomes ...? monitoring the performance ...? data governance? technical solution governance? appeal and redress processes?" | Named owners | Memo Roles; `agency:` |
| 24 | "Have you established a clear processes to: intervene if a relevant stakeholder finds concerns ... (appeal and redress)? ensure you do not get overconfident or over reliant on the AI system?" | Intervention and over-reliance controls | Human oversight design; reviewer sampling; automation-bias measures (M override rate) |
| Summary | Highest risk per principle (N/A, low, mid-range, high, very high) | Five ratings | Proposed as `assumption:`; `agency:` |

### Part 4. Mitigation, residual risk, procurement

| # | Form (P content) | Answer needs | From our records |
| --- | --- | --- | --- |
| 25 | "Review your self-assessment, list here the mitigations to be applied and the high-level steps ..." High and very high operational risks need "regular external independent risk audits" | Mitigation list | impact-assessment.md Measures (C and SB with status) |
| 26 | "Is your project / system an elevated risk?" (high or very high residual → pilot, formal review after pilot, independent risk audit and AI Review Committee review; mid-range → pilot and consider the committee; low → proceed with controls) | Residual band | impact-assessment.md "Residual risk and decision"; `agency:` |
| 27 | "When considering risks, did you identify treatments ... that were system requirements or contractual controls?" (control split: buy and use = high supplier control; embed = shared; develop = full agency control) | Treatments by type | Design C and SB (system requirements); contract terms: `agency:` / `counsel:` |
| 28 | "Are the contractual clauses in your contract sufficient for the identified contractual controls?" (No → Core& must move to the ICTA; under the ICTA, add Order Form additional conditions, items 11 and 66) | Contract sufficiency | `counsel:` / `agency:`. The pack lists the ICTA 6.11 items the design relies on (Part C, C12) |
| 29 | "... any questions that you could not answer or could only partially answer due to supplier provided products or services?" | Questions for suppliers | Pack `gap:` and `counsel:` lists; Google model page facts with `source:` |
| 30 | Question text not recovered from the extraction; the options read "Yes: You must use the ICTA contract if you proceed. No: You may use Core& or ICTA". Paraphrase: is the procurement high risk under the ICT Purchasing Framework (Core& for low risk up to $1 million ex GST; MICTA/ICTA for high risk or over $1 million)? | Contract framework | `agency:` |
| 31 | "Did you identify any treatments that are system requirements?" (→ Statement of Requirements and evaluation criteria) | Requirements | Design R and C IDs |
| 32 | "Do all risks have appropriate treatments, including the order in which the treatments are applied?" | Treatment order | impact-assessment.md Measures |
| End | Residual high or greater → AI Review Committee; mid-range or above → pilot before scaling; record in the records management system; all responsible officers approve | Next steps | Plan waits `W` (AIRC referral within 5 business days; pilot goal) |

## B4. What a NSW agency expects from the vendor

- **Not registration or the assessment itself** (Operational Policy
  Attachment A exclusion, P). The agency's Accountable Owner registers. The
  vendor supplies evidence for:
  - the AIAF answers (B2, B3);
  - the "supplier solution assessment" and "AIAF self-assessment" stages in
    AI Procurement Essentials (fork, P);
  - the ICTA 6.11 records and incident programme (Part C, C12).
- **The Responsible AI guidance RACI** makes product owners and management
  responsible for "Evaluate vendors and third-party AI solutions for
  compliance with the NSW AI Operational Policy, AIAF, and AI procurement
  guidance" (P).
- **The Operational Policy's assurance function** (fork, P): "Contractual
  arrangements must support transparency, including mechanisms for
  suppliers to disclose AI use and notify the agency of material changes".
  It also requires "Continuity and sovereign capability": the ability to
  operate or transition if a model changes or becomes unavailable.

---
## B5. Crosswalk: IPC "Guide to undertaking Privacy Impact Assessments on AI systems and projects" (December 2024)

Source: IPC NSW (<https://www.ipc.nsw.gov.au>, guide page, "December 2024";
P, read 2026-10-26). The guide sits beside the general Guide to Privacy
Impact Assessments in NSW. It supports privacy assessments under the AIAF
and the national assurance framework. Its framing points:
- "If an AI system or project involves handling personal information, a PIA
  will typically be required".
- "The cost or size of a project or system is not a reliable indicator".
- PIAs are refreshed "before a purchase, before a system is launched, when a
  system is being reconfigured, when a new use case is being considered, or
  when a vendor contract is due for renewal".
- "AI-generated inferences about individuals are also considered personal
  information, even if they are incorrect".
- The IPC cannot endorse a project, write a PIA, or comment on policy
  objectives.

This is the NSW PIA form the pack's input pack must serve when the client is
a NSW agency. It replaces the APP compliance check, which does not apply to
the agency (Part C, C1).

| IPP / HPP (guide's heading) | Guide's questions (abridged, P) | From our records |
| --- | --- | --- |
| IPP/HPP 1 Lawful | Collection directly related to a function and necessary? Beyond what is reasonably necessary? Review each input; outputs as "collection through creation"; legislative compliance; do not rely on unexplainable AI for automated decisions about individuals | Input pack data flows and people and data categories; design data register (brief §4); generated outputs and memory (C); `counsel:` legal basis for any automated decision |
| IPP 2 / HPP 3 Direct | Collected from the individual or authorised? Created information; collection from other sources, public or third party; hidden AI features in software | Data flows (sources column); grounding sources (D); `counsel:` |
| IPP 3 / HPP 4 Open | Notice of collection, purposes and recipients; third-party providers as recipients; notice of created information; is personal information used for training, and does it benefit the provider? Required or voluntary? Chatbot notice "at the time the conversation is occurring" | System card AI disclosure; proposed notice text (input pack inventory, adapted to the NSW s 10 notice); model provider data use (no training); disclosure contract (C) |
| IPP 4 / HPP 2 Relevant | Each input relevant? Accurate, complete, up to date, not excessive? Source reliable? Prompting for complete information in the right format? Old information? Free-text fields raise unsolicited-collection risk | Data register; screening contracts for free text (protect-adk-sensitive-data); structured-input design (C) |
| IPP/HPP 5 Secure | Stored securely? Who has access? Can one individual see another's information? Retention periods and disposal (State Records Act minimums)? Third-party due diligence; contracts binding the PPIP and HRIP Acts and the MNDB scheme; caution with standard terms | SB table and security questionnaire; per-user scope contracts (SB03, SB04); retention table (input pack); cross-user leak tests (M); contract: `agency:` / `counsel:` |
| IPP/HPP 6 Transparent | How the agency explains what is stored, why, and access rights; update the Privacy Management Plan to include AI use | System card; `agency:` (PMP update, s 33) |
| IPP/HPP 7 Accessible | Ready for access requests, including inferences? Extract from vendor platforms? | Memory, session and log stores reachable by a request (input pack retention and erasure); export path (C or `gap:`) |
| IPP/HPP 8 Correct | Correction path; decisions use the corrected information | Correction and re-index path for memory and RAG (C); `gap:` |
| IPP/HPP 9 Accurate | Checks before use; extra checks on AI outputs; limit outputs to low-risk use; explainability; "human validation of any AI process that uses personal information" | Evaluation reports (M); human review contracts and share reviewed; grounding and citation (C) |
| IPP/HPP 10 Limited | Used only for the collection purpose (or consent, a directly related purpose, or a serious threat)? Third party not using it for its own purposes? Training without personal information? | Input pack necessity and proportionality (re-used datasets); model provider data use (training off, abuse-monitoring logging); `counsel:` |
| IPP 11 Restricted / HPP 11 Limited | Disclosure to another person or body? Vendor access may be a disclosure; access "for the sole purpose of carrying out a contracted service" is "likely to be a 'use'"; staff seeing other individuals' data; document intended disclosures and the IPP 11 rationale | Recipients and regions (Google, consultancy support access); consultancy access decision (D); `counsel:` use or disclosure |
| IPP 12 Safeguarded | Sensitive categories (ethnic or racial origin, political opinions, religious or philosophical beliefs, trade union membership, sexual activities) not disclosed? **Disclosure to a Commonwealth agency or a person or body outside NSW?** Location of third-party providers; remove sensitive information from chatbot free text | Screening contracts; processing region (D, model page `source:`); abuse-monitoring and support locations; `counsel:` s 19(2) (Part C, C1) |
| HPP 12 Not identified | Unique identifiers needed? | Data register; `n/a:` unless health |
| HPP 14 Controlled | Health information transferred outside NSW: recipient bound by equivalent standards, consent, or a contract benefiting the individual | Processing region; `counsel:` |
| Risks and mitigations table | Inaccurate information; bias and discrimination; lack of transparency; secondary use; unauthorised disclosure; retention and disposal; re-identification; third-party risk; data breaches; plus mitigations (data minimisation, due diligence, contractual controls, human validation, synthetic data, automated destruction, access restrictions) | Input pack "Risks and measures" rows, one per guide risk, each citing C and SB IDs with status |

---
# Part C. NSW state law and policy for an agent built for a NSW agency

**Access limit, read first.** legislation.nsw.gov.au, AustLII and
parliament.nsw.gov.au returned HTTP 403 to automated fetches on 2026-10-26.
NSW statutory wording below therefore comes from:
- regulator pages that quote the Acts (IPC, State Records NSW,
  arp.nsw.gov.au), marked P for what the regulator says;
- a superseded 2016 compilation of the PPIP Act hosted by a council, marked
  S;
- recollection, marked U.

**Before a reference relies on these sections, re-read the current text at
legislation.nsw.gov.au from a browser:**
- PPIP ss 4(4), 19 and 33;
- the Part 6A section on extending the 30 days;
- GIPA ss 27 to 35;
- the State Records Act section numbers;
- Workplace Surveillance Act ss 10 to 22;
- HPP 14.

**Corrections to the brief:**
1. There is **no State Records Act 2024**. The State Records Act 1998 still
   governs, as amended by the Museums of History NSW Act 2022. The 2024
   instrument is the **State Records Regulation 2024**, from 1 September
   2024 (S, search result for sl-2024-419).
2. PPIP **ss 19(3) to (5)**, including the s 19(4) code power, show as
   "(Repealed)" in the 2016 compilation (S). No transborder code applies;
   s 19(2) applies directly.
3. Privacy Act **s 95C concerns Commonwealth contracts**, not State
   contracts (P).
4. The MNDB scheme has its own "held" test in **s 59C** (P via IPC).
5. Section 59ZE is the internal breach register. The public notification
   register is s 59P (P via IPC).

## C1. PPIP Act 1998: IPPs, s 19(2), contractors, privacy management plan

**Status.** In force. IPC IPP fact sheet August 2026; PMP guide May 2026
(P).

**The 12 IPPs** (headings from the 2016 compilation, S; numbering per IPC,
P). The IPC's "plain" names, used in the AI PIA guide, come after the
heading:

| IPP | Section | Heading (IPC short name) |
| --- | --- | --- |
| 1 | s 8 | Collection for lawful purposes (Lawful) |
| 2 | s 9 | Collection directly from the individual (Direct) |
| 3 | s 10 | Requirements when collecting (Open) |
| 4 | s 11 | Other requirements relating to collection (Relevant) |
| 5 | s 12 | Retention and security (Secure) |
| 6 | s 13 | Information about personal information held (Transparent) |
| 7 | s 14 | Access (Accessible) |
| 8 | s 15 | Alteration (Correct) |
| 9 | s 16 | Check accuracy before use (Accurate) |
| 10 | s 17 | Limits on use (Limited) |
| 11 | s 18 | Limits on disclosure (Restricted) |
| 12 | s 19 | Special restrictions on disclosure (Safeguarded) |

**Section 19(2), transborder disclosure** (2016 text S; the IPC fact sheet
of November 2019 matches, P).
- The rule: an agency "must not disclose the information to any person or
  body who is in a jurisdiction outside New South Wales or to a Commonwealth
  agency unless" one of these grounds applies:
  - (a) a reasonable belief that the recipient is subject to "a law, binding
    scheme or contract that effectively upholds principles ... substantially
    similar" to the IPPs;
  - (b) express consent;
  - (c) and (d) contract necessity;
  - (e) the individual's benefit where consent is impracticable;
  - (f) a serious and imminent threat;
  - (g) "reasonable steps" to ensure that the recipient will not handle the
    information inconsistently with the IPPs;
  - (h) authorised or required by law.
- The IPC on (a): the Commissioner names no jurisdictions and "urges
  caution".
- The IPC on (g): at a minimum, "an enforceable contract" that requires
  IPP-compliant handling, with enforcement rights, a complaints mechanism,
  breach notification to the agency and flow-down to subcontractors.
- Sensitive information (s 19(1): ethnic or racial origin, political
  opinions, religious or philosophical beliefs, trade union membership,
  sexual activities) must first pass s 19(1), then s 19(2). Health
  information goes through HPP 11 and HPP 14 instead (P, IPC table).
- **Use or disclosure.** The AI PIA guide says vendor access "for the sole
  purpose of carrying out a contracted service ... is likely to be a 'use'"
  (P). The fork read the transborder fact sheet as saying the same where a
  provider "simply holds the data and acts according to the instructions of
  the agency".

**Contractors.**
- s 4(4) (S): information is "held" by the agency if it is in the
  possession or control of "a person employed or engaged by the agency in
  the course of such employment or engagement". Information a contractor
  holds for the engagement is therefore held by the agency.
- s 12(d) (S): the agency does everything reasonably within its power to
  prevent unauthorised use or disclosure when information goes to a person
  "in connection with the provision of a service to the agency".
- **The PPIP Act does not bind the contractor directly.** "The service
  provider will only be subject to NSW privacy law if specifically required
  under the contract" (P, IPC).
- Contractor staff engaged by an agency can be "public sector officials" for
  the s 62 corrupt use and disclosure offence (S, s 3 definition; U whether
  it reaches a consultancy's staff).

**Section 33, privacy management plan.**
- Contents (S plus P):
  - policies and practices for compliance with the PPIP and HRIP Acts;
  - dissemination of those policies to staff;
  - internal review under Part 5;
  - **(c1)**, Part 6A procedures (P, quoted in the IPC PMP guide, May 2026);
  - other matters.
- A copy goes to the Commissioner when prepared and when amended (s 33(5)).
- The May 2026 guide: where AI involves personal information, "the plan
  should include information about the use of AI and ADM" (P).

**Triggers for an agent.**
- Any personal information in prompts, retrieval, tools, logs, memory or
  evaluation sets.
- Inferences: the IPC calls these "collection through creation" (P).
- Model endpoints, abuse monitoring, telemetry or consultancy support
  outside NSW. Note that this includes other Australian states, not only
  overseas. **This is stricter than APP 8:** a Melbourne support engineer or
  a non-NSW Google region is "outside NSW".
- Chatbot collection notices (s 10). The IPC prefers notice "communicated by
  the chatbot at the time the conversation is occurring".

**Paperwork mapped to the pack:**
- Input pack: a new section "NSW: IPP and HPP check", from the B5
  crosswalk, replacing the APP check for the agency's own handling.
- The data-flow table gains an "outside NSW?" column.
- The memo's NSW section records the s 19(2) ground as `counsel:`.
- Proposed s 10 notice text (replacing APP 5).
- PMP update (`agency:`).
- A contract privacy schedule as `counsel:`: IPP flow-down, breach
  reporting and sub-processors.

**Questions for counsel:**
- Is the model provider, logging or support access a use or a disclosure?
  If a disclosure, which s 19(2) ground applies?
- Does the Google Cloud contract, flowed down, meet the IPC's (g) minimum?
- Are named consultancy staff "public sector officials" for s 62?
- Does any public interest direction or code apply to the agency?

## C2. HRIP Act 2002: Health Privacy Principles

**Status.** In force; IPC HPP fact sheet May 2026 (P).

**The 15 HPPs** (Schedule 1, IPC titles, P):
1. Lawful
2. Relevant
3. Direct
4. Open
5. Secure
6. Transparent
7. Accessible
8. Correct
9. Accurate
10. Limited use
11. Limited disclosure
12. Not identified (unique identifiers)
13. Anonymous
14. Controlled transfer outside NSW
15. Authorised (health records linkage)

**HPP 14.** "An organisation must only transfer health information about an
individual outside New South Wales in accordance with HPP 14" (P). The AI
PIA guide lists the main grounds: the recipient bound by standards
equivalent to the HPPs; consent; or a contract benefiting the individual
where consent is impracticable and the individual would likely consent (P).
The full verbatim grounds were not read (U).

**Who is bound (P).** Public sector agencies, and private sector persons
that provide a health service or collect, hold or use health information.
**Unlike the PPIP Act, the HRIP Act can bind the consultancy directly.** The
fork reported a $3 million turnover qualifier for some businesses; check it
against the Act before relying on it (S/U).

**Triggers.** Health or disability information in agency records,
retrieval or free-text chat. This includes services that are not health
services: for example, a citizen mentions a condition to a transport agent.

**Paperwork.** Input pack HPP rows; HPP 14 analysis beside s 19(2); a
`counsel:` question on whether the consultancy is an "organisation" bound in
its own right. A health client adds the existing `australia.md` health rows.

## C3. Mandatory Notification of Data Breach scheme (PPIP Act Part 6A)

**Status.** "From 28 November 2023, every NSW public sector agency bound by
the PPIP Act must notify the Privacy Commissioner and affected individuals
of eligible data breaches" (P, IPC guide, July 2024). The research note's
earlier "U" on this date is now resolved, checked 2026-10-26.

**Steps** (section numbers from IPC footnotes, P):
- Contain "immediately" (s 59E(2)(a)).
- Assess, and the assessment "must be completed within 30 days"
  (s 59E(2)(b)). The extension power exists, but its section number was not
  verified (U).
- Mitigate (s 59F).
- Notify the Commissioner "immediately" on the approved form (s 59M).
- Notify individuals "as soon as reasonably practicable" with the s 59O
  contents. Public notification where direct notice is impracticable
  (s 59N(2)), kept on the public register for at least 12 months (s 59P).
- **Published data breach policy** (s 59ZD).
- **Internal register of eligible data breaches** (s 59ZE).
- Exemptions (ss 59S to 59X); assessment guidelines under s 59ZI (September
  2023).

**Contractors (P).**
- The scheme "does not generally apply to contracted service providers".
- Under s 59C, the agency holds information it possesses or controls,
  including through a contractual right of access. In SaaS or IaaS hosting,
  "in most cases the agency will be considered to hold" it.
- Contracts should require the provider to "promptly report data breaches to
  the agency, take mitigating actions and assist the agency in undertaking
  assessments", and should say who notifies individuals.
- Multi-agency breach: each agency assesses and notifies the Commissioner;
  one notifies individuals, usually the one with the most direct
  relationship.

**Agent breach paths.** Prompt injection exfiltration; cross-user session or
memory leakage; logs sent to the wrong sink; disclosure to a provider
outside the contract. The IPC's generative AI guide (May 2026) notes that
leakage "may constitute a notifiable data breach" (P).

**Paperwork.**
- Security questionnaire incident row: the NSW clocks are agency-side
  (contain immediately, assess within 30 days, Commissioner immediately).
  The contractor clock is set by contract: ICTA "immediately", then details
  within 48 hours (fork, P); Core& "within 48 hours" (fork, P).
- Cyber incidents go to Cyber Security NSW within 24 hours (C10).
- `agency:` the data breach policy entry.
- `counsel:` whether the agency "holds" data in the consultancy's dev, test
  and log environments.

## C4. IPC guidance on AI and PIAs

- **Guide to undertaking PIAs on AI systems and projects** (December 2024,
  P). Crosswalk in B5.
- **Guide to Privacy Impact Assessments in NSW** (May 2020, P).
  - "While there are no strict legal requirements in NSW around undertaking
    a PIA": a PIA is **expected, not statutory**.
  - Steps: documented threshold assessment; plan; consult stakeholders; map
    information flows; identify risks and remedies; recommendations;
    report, with publication as "best practice"; the agency's response
    (adopt, partially adopt or not adopt); review.
  - Appendix A gives a report format. The input pack's common sections
    supply the flows and risks.
- **Guide: Privacy risks associated with the use of generative AI tools**
  (May 2026, P).
  - "If a generative AI system will be used within the agency to handle
    personal information, a privacy impact assessment (PIA) should be
    undertaken."
  - Vendor terms should: prohibit training on customer data; bind the vendor
    to PPIP-equivalent protection and breach notice aligned with Part 6A;
    set retention and deletion; give audit and termination rights. Australian
    residency "where possible".
- **Privacy by design** fact sheet (May 2020, P): seven principles. AIAF
  question 14 refers to it.
- **Consulting the Commissioner is optional.** The IPC cannot endorse a
  project, write a PIA or comment on policy objectives (P).
- **IPC desktop review of AI and ADM disclosure** (17 November 2025, P). Of
  119 agencies, few documented AI use in their agency information guides or
  PMPs. Six recommendations.

## C5. GIPA Act 2009

**Status.** In force. Statute text not read (403). Provisions below are from
IPC pages (P).

- **Open access information (s 18):** agency information guide (s 20),
  policy documents (s 23), disclosure log (ss 25 and 26), **government
  contracts register (s 27)**. The IPC's AI and ADM fact sheet (August 2024)
  says agency information guides should list "machine-enhanced
  decision-making systems". Its 2025 review calls failure to document AI
  use "a potential compliance risk".
- **Contracts register (Part 3 Division 5).**
  - Covers contracts with private sector entities "valued at $150,000
    (including GST) or more".
  - Class 1 particulars (s 29): contractor, effective date, duration,
    services, estimated amount, variation and renegotiation provisions,
    tender method and criteria.
  - Class 2 (s 30): adds risk apportionment, guarantees and other key
    elements.
  - Class 3 (s 31): a copy of the contract. The IPC says copies are
    included for contracts "more than, or expected to reach the value of
    $5 million".
  - Exclusions (s 32): commercial-in-confidence provisions, with reasons.
  - Also published on tenders.nsw.gov.au (s 35).
  - The 45-working-day entry time and the class 2 triggers: U.
- **Section 121.** A contract for **services to the public on behalf of** an
  agency must give the agency an "immediate right of access" to information
  about the contractor's performance, information collected from the
  public, and information received from the agency. That information
  becomes government information. The IPC publishes template clauses (P).
  This applies when the agent serves the public and the consultancy operates
  it.
- **AI outputs as government information.** The IPC says access rights
  "remain applicable" to technology-assisted decisions, and responses
  should consider "algorithms, source codes, test suites, data sets and
  variables". It cites *O'Brien v Secretary, DCJ* [2022] NSWCATAD 100 on a
  contractor-built algorithm (P). Its digital records fact sheet treats
  databases, SaaS content and "audit and access logs" as records, so
  prompts, outputs and traces the agency holds are government information.
  No IPC page names "prompts" expressly (U).
- **Paperwork.**
  - Memo NSW section: the GIPA register entry (`agency:`), commercial-in-
    confidence claims (`counsel:`), whether s 121 applies (`counsel:`), and
    the agency information guide entry listing the agent (`agency:`).
  - Design: log export and search, so the agency can answer access
    applications (`gap:` if absent).

## C6. State records: State Records Act 1998 and Regulation 2024

**Status (P, State Records NSW).**
- Act commenced 1 January 1999.
- Amended by the Museums of History NSW Act 2022, with Part 4 archive
  changes from 1 January 2024.
- Regulated by State Records NSW, now in the Department of Creative
  Industries, Tourism, Hospitality and Sport.
- State Records Regulation 2024 from 1 September 2024 (S).

**Duties (P).** "make and keep full and accurate records"; a records
management program; disposal only as authorised (State Records NSW approval,
other legislation, or normal administrative practice). Section numbers U;
s 12 is believed to be the main duty.

**AI guidance (P, State Records NSW "AI and recordkeeping", last updated
9 February 2024).**
- "any record created during government business – whether by AI, a
  computer system, or a person – is a State record".
- AI records need metadata: AI-generated status, "the software used", "the
  prompts, inputs or algorithms used".
- "It is not enough to leave them in the AI tool"; they must be saved in
  official recordkeeping systems.
- The **NSW AI Operational Policy** says "AI outputs and metadata are State
  records" (fork, P), and requires records "through the AI system
  lifecycle".
- The 2024 AIAF says results must be stored in the agency records system
  "Refer NSW State Records Act" (S provenance).

**Paperwork.**
- Design: an export to the agency's recordkeeping system for outputs used in
  government business, with metadata (model ID and version, prompt or input
  reference, timestamps). This is a goal for adk-agent-observability and
  adk-memory-architecture.
- Retention contracts aligned to disposal authorities (`agency:` which
  authority, for example general authorities for administrative records).
- Return-or-destroy at contract end.
- System card Data section.

## C7. NSW Cyber Security Policy 2026–2027 (from the fork, P)

- **Version.** "NSW Cyber Security Policy 2026–2027", July 2026, Cyber
  Security NSW (DCS).
  - Mandatory for departments, public service agencies and statutory
    authorities.
  - Not mandatory for SOCs, local government or universities (2.2, 2.3).
  - Covers "third-party and shared services".
- **31 mandatory requirements** (verified ML1 sentence and 24-hour wording
  in the extracted text):
  - Domain 1, Govern and identify (1.1 to 1.12), including 1.10 third-party
    risk.
  - Domain 2, Detect, respond and recover (2.1 to 2.4).
  - Domain 3, Protect (3.1 to 3.15), where 3.3 to 3.10 are the Essential
    Eight.
- **Essential Eight.** "Mandatory requirements 3.3 to 3.10 embed the
  Maturity Level One Essential Eight controls". Higher maturity is risk-
  based. **There is no Maturity Level Two mandate**, contrary to the
  brief's assumption.
- **Reporting.** Annual assurance and attestation by 31 October. Cyber
  incidents reported via the Cyber Portal "within 24 hours of detection and
  classification".
- **Suppliers.**
  - 1.10.2: a contractually supported process for providers to notify
    incidents and data breaches.
  - 1.10.4: contract clauses on cyber requirements, plus break clauses.
  - 9.4: consider data sovereignty "where data is hosted and supported".
  - 9.1.1 (advisory): agencies "may apply" the mandatory requirements to AI
    systems, including vendor risk, data leakage, logging of AI use and
    outputs, and change management.
- **Other directives:**
  - DCS-2026-03: crown jewels inventory by 31 October 2026, third-party
    inventory and annual penetration tests of crown jewels by 30 June 2027.
  - DCS-2025-01: restricted applications list (content U).
- **Paperwork.**
  - Security questionnaire: map SB rules to requirements 1.10, 2.1 to 2.3,
    3.2, 3.5 and 3.12 (encryption with ASD-approved algorithms).
  - ML1 evidence for the delivered environment.
  - Incident notification procedure that fits inside the agency's 24-hour
    window.
  - Data location statement.
  - `agency:` crown jewel status.

## C8. Workplace Surveillance Act 2005

**Status.** Commenced 7 October 2005 (P, DPC circular C2005-37). Current
text not read (403).

- **s 10 notice** (P, circular): written notice "at least 14 days" before
  surveillance starts, or less by agreement. It states the type, how it is
  done, the start date, whether continuous or intermittent, and whether for
  a limited period or ongoing.
- **Computer surveillance** (s 12, S): only under a notified policy.
- **Blocking email or websites** (s 17, S): only under policy, with a
  prevented-delivery notice.
- **Covert surveillance** (Part 4): an offence without a magistrate's
  authority (P, circular; section numbers U).
- The circular also tells agencies to make contractors and labour hire staff
  aware.
- Related: the WHS Amendment (Digital Work Systems) Act 2026, assent 18
  February 2026. Its main duties await proclamation (`australia.md`,
  checked 2026-10-26). The fork could not confirm commencement status (U).
- **Pack.** Already in `australia.md`. For a NSW agency client, the notice
  is the agency's: a wait `W` of at least 14 days before production, if
  identity-linked logs of staff prompts count as computer surveillance
  (`counsel:`). Add whether consultancy staff on agency systems receive
  notice from the agency, the consultancy, or both (`counsel:`).

## C9. Anti-Discrimination Act 1977 (NSW)

**Status at 26 October 2026 (P, NSW Law Reform Commission page "last updated
26 October 2026").**
- **The review is still in progress. No new Act and no final report.**
- Consultation Paper 24 (unlawful conduct) was released 20 May 2025.
- Consultation Paper 25 (procedures and compliance) was released 24 July
  2026; submissions closed 2 October 2026.
- The religious vilification amendment commenced 12 November 2023 (P,
  ADNSW).
- Reports of a 2025 religious belief discrimination amendment are U.

**Attributes (P, ADNSW):**
- race; sex; pregnancy and breastfeeding; disability; age; carer's
  responsibilities; homosexuality; transgender status; marital or domestic
  status; infectious disease;
- vilification grounds: race, homosexuality, transgender status, HIV/AIDS,
  religion.

No positive duty on public authorities was found (U).

**Pack.** For "the NSW Anti-Discrimination Act as reformed", write that the
reform is pending, with `checked 2026-10-26`. Show bias measurement in the
impact assessment's adverse-impact section, and in AIAF questions 9 to 13 and
DTA 5.1 and 5.2. Add `counsel:` on indirect discrimination and on who is
liable for system outputs.

## C10. NSW procurement for ICT and AI (from the fork, P; ICTA 6.11 re-checked by the coordinator)

**PBD-2025-03** (28 October 2025, updated 13 November 2025): agencies must
use the ICT Purchasing Framework.
- **Core&**: low-risk procurements up to $1 million ex GST.
- **MICTA/ICTA**: high-risk procurements or $1 million or more. It "replaces
  Procure IT 3.2".

**ICTA (August 2025) clause 6.11, AI Systems** (P, text re-read):
- Other than for AI Systems set out in the Order Form, no use or deployment
  of an AI System without written notice, a 3-month wait (or another period
  set by a Module or the Order Form), and the Customer's prior written
  approval.
- The supplier must "maintain detailed records of any AI System ...
  (including records of the design (including functions, features and
  interconnected systems), performance, governance and intended and actual
  use)" and provide them promptly.
- A warranty of risk-managed design, training and testing, "including
  ensuring accuracy and reliability".
- An optional Order Form item bars EU AI Act Article 5 practices.
- Per the fork:
  - an AI incident programme with quarterly reporting by default;
  - suspension and termination rights;
  - **6 months' notice of "a change to the underlying model"** by default;
  - Customer Data used to train only the customer's own instance;
  - Customer Data kept in NSW unless the Order Form permits otherwise
    (cl 19.3);
  - security incident notice "immediately", then details within 48 hours.

**Core& One Core Terms (August 2025)** (fork, P):
- 3 months' notice and consent before using AI.
- AI logs are Buyer Data.
- No personal information outside Australia, or accessed from outside
  Australia.
- Breach notice within 48 hours.

**AI Procurement Essentials** (6 May 2026) (fork, P): plan with AIAF triage
and self-assessment; source with "AIAF self-assessment and supplier
solution assessment". The page still links the superseded Ethics Policy.

**ICT Services Scheme (SCM0020)** (S): a supplier-side arrangement.

**Pack.** A new memo row, "NSW contract AI clauses", with these items:
- The models listed in the Order Form (Gemini model IDs; whether coding
  assistants count).
- **A model-change notice period that matches the provider's lifecycle**: a
  6-month default notice against Gemini retirement dates is a real
  conflict. Give it to adk-model-and-output-contracts and
  adk-release-engineering as a gap.
- The data location: NSW. Google Cloud australia-southeast1 is Sydney, but
  check model processing and support access.
- The ICTA 6.11 records as a deliverable the system card and design
  already produce.

## C11. Commonwealth Privacy Act and a contractor to a NSW agency

**Sources:** Privacy Act 1988, Compilation No. 104, 4 June 2026 (P,
verbatim from the fork).
- **s 6(1) "State contract":** "a contract, to which a State or Territory or
  State or Territory authority is or was a party, under which services are
  to be, or were to be, provided to a State or Territory authority."
- **s 7B(5):** an act or practice of an organisation is exempt if "(a) the
  organisation is a contracted service provider for a State contract
  (whether or not the organisation is a party to the contract); and (b) the
  act is done, or the practice is engaged in for the purposes of meeting
  (directly or indirectly) an obligation under the contract."
- **s 95C** is about Commonwealth contracts only.
- Statutory tort, Schedule 2: "staff member" of a State authority includes
  "a consultant or contractor to the agency or authority" for the
  good-faith exemption. Whether this covers a corporate contractor is
  `counsel:`.

**Meaning.**
- The consultancy's acts done to meet obligations under the NSW contract
  fall outside the APPs, and the IPC says outside the Commonwealth
  notifiable data breach scheme as well (fork, P).
- NSW privacy law reaches the consultancy only through the contract (PPIP)
  or directly (HRIP).
- For everything else, the consultancy remains an APP entity unless s 6D
  exempts it: its own HR, other clients, reuse of agency data for its own
  purposes (which the contract should forbid anyway), and its own privacy
  policy.
- APP 1.7, from 10 December 2026, binds its own automated decisions, not
  the agency's.

**Questions for counsel.**
- Is each processing activity "for the purposes of meeting" a contract
  obligation? Examples: evaluation sets reused across clients, trace review
  for the consultancy's own tooling.
- Does the small business exemption apply to the consultancy?
- Which regime governs a breach in the consultancy's own environment?

## C12. Paperwork summary: what the pack produces for a NSW agency

| Item | Owner | Pack document |
| --- | --- | --- |
| AIAF Platform registration and assessment; AIRC referral within 5 business days if high or critical | Agency (Accountable Owner) | government-form-answers.md, AIAF sections (B2, B3); impact assessment |
| Agency PIA under the IPC guides | Agency | Input pack with "NSW: IPP and HPP check" (B5) |
| s 19(2) and HPP 14 analysis | Agency, `counsel:` | Input pack recipients and regions, with an "outside NSW?" column |
| PMP update (s 33, AI and ADM) | Agency | `agency:` line in the memo |
| MNDB policy (s 59ZD) and contract breach clause | Agency; contract | Security questionnaire incident row; memo |
| GIPA contract register entry (contracts of $150,000 or more); agency information guide entry; s 121 access clause if the agent serves the public | Agency | Memo NSW section |
| State records capture of AI outputs and metadata | Agency; design | Design goal; system card Data |
| NSW Cyber Security Policy mapping; ML1 evidence; 24-hour incident path | Agency; consultancy evidence | Security questionnaire |
| ICTA 6.11 AI system records, Order Form AI list, model-change notice | Contract | Memo NSW contract row; system card; design model decision |
| Workplace surveillance notice (14 days) | Agency | Wait `W` |
| DAF gateway (estimated total cost of $5 million or more, or DRF funded) | Agency | Wait `W`; plan |

## C13. Counsel and agency questions (NSW)

1. Is the Gemini endpoint, abuse-monitoring storage, telemetry or consultancy
   support access a "use" or a "disclosure" to a recipient outside NSW? If
   a disclosure, which s 19(2) ground applies, and does the contract meet
   the IPC's (g) minimum?
2. Is any health information handled? Is the consultancy bound by the HRIP
   Act in its own right? Is HPP 14 met?
3. Does the agency "hold" (s 59C) data in the consultancy's development,
   test and log environments? Who notifies, and by when?
4. Does the agent provide "services to the public on behalf of" the agency
   (GIPA s 121)? Which contract provisions are commercial-in-confidence?
5. Which disposal authority applies to agent outputs and traces? Are traces
   State records or ephemeral?
6. Is identity-linked prompt logging "computer surveillance" of employees?
7. Does any output feed an "administrative decision under an Act"? If so,
   is express legislative authority needed? This appears in AIAF Part 1 and
   DTA 1.8 as well.
8. Is everything the consultancy does "for the purposes of meeting" the
   State contract (s 7B(5))?
9. Which AIAF risk band applies (intrinsic), and is AIRC referral needed?
10. Which contract applies (Core& or ICTA)? What notice period applies to
    model changes, and which AI systems are listed in the Order Form?


---

# Part D. What to build in the pack

## D1. Proposed reference: `references/au-government-crosswalks.md`

One reference file. Read it when the jurisdiction screen finds a Commonwealth
or NSW government client. It ships the maps, never the forms. Proposed
outline (about 350 lines):

1. **When to read and what it produces.**
   - Trigger: client type "Australian Commonwealth agency" (NCE) or "NSW
     agency" (DCS-2026-02 entity list).
   - Output: one new pack document, `government-form-answers.md`, holding
     draft answers in the official form's own order for the agency's
     officers to paste into the official tool. Each form gets its own
     section headed with:
     - the form's name and version;
     - its URL;
     - "version checked <ISO date>";
     - "the agency completes and approves this in the official tool".
   - Every answer cites an evidence ID or carries `agency:` or `counsel:`.
     `agency:` is a new marker meaning "only the agency can answer". The
     checker must accept it the way it accepts `counsel:` (D2).
2. **Rules.**
   - Never reproduce the form. Quote at most the question number and a short
     paraphrase.
   - Re-read the form's page before drafting. If the version differs from
     the one in the reference, say so and stop at a `gap:` until the
     crosswalk is updated.
   - The pack never fills the officer, approval, risk-rating decision or
     legal-advice fields. It proposes ratings as `assumption:` with their
     basis.
   - Say which rating is proposed: DTA inherent then residual; NSW intrinsic
     band (Operational Policy) or residual (2024 AIAF).
   - Planned treatments stay "planned G<n>".
3. **Commonwealth.** The policy facts table (A1); DTA tool v1.0 (1 December
   2025) crosswalk (A3, compressed to one table per section); the
   transparency statement inputs (A4); the register fields (A5); the AGT.1
   to AGT.8 conformance table (A6); the AI model clauses evidence table
   (A7); the Commonwealth AI Review Committee trigger (residual high, or
   highly sensitive, novel or complex) as a wait `W`.
4. **NSW.** The status table (B1): DCS-2026-02, Operational Policy v1.1,
   AIAF Platform from 30 September 2026, risk bands, AIRC within 5 business
   days, attestation from 31 October 2027. Then the registration crosswalk
   (B2), the 2024 AIAF crosswalk (B3) marked "the platform's own wording is
   not public: confirm with the agency (`agency:`)", the IPC AI PIA crosswalk
   (B5) and the vendor-evidence list (B4 and C12).
5. **NSW law screen.** A compressed Part C table: law, status and date,
   trigger, pack document. Plus the s 7B(5) roles rule.
6. **Documents the pack names but the agency produces.** DTA assessment,
   transparency statement and register entry; AIAF registration and
   assessment; AIRC referral; the agency PIA (IPC guide); the GIPA contract
   register entry; the PMP update; the MNDB policy entry; the DAF gateway
   (projects of $5 million or more, or DRF funded).
7. **Re-check list** with dates: the DTA tool version; Appendix D drift; the
   AIAF Platform question set; the Operational Policy version-table
   discrepancy; AIAF 2024 questions 14 and 30; Anti-Discrimination reform
   status.

Template change: add `assets/government-form-answers-template.md`. It has
front matter (`document: government-form-answers`, `form:`,
`form_version:`, `form_url:`, `form_checked:`), then one section per form:
DTA tool, DTA transparency inputs, DTA register row, AIAF registration,
AIAF assessment, IPC AI PIA. Each section is a table with the columns "#",
"Question (paraphrase)", "Draft answer", "Evidence", "Who decides".

## D2. Checker patterns

### New counsel triggers (add to `COUNSEL_TRIGGERS["public-body clients"]`)

```python
r"\bNSW (?:Government )?(?:agenc(?:y|ies)|department|public sector agency)",
r"\bstate (?:government )?agenc(?:y|ies)",
r"\bnon-corporate Commonwealth entit",            # NCE
r"\bAIAF\b",                                       # case-sensitive acronym
r"AI Assessment Framework",
r"AI Review Committee",
r"DCS-2026-02",
r"NSW AI Operational Policy",
r"\bAI impact assessment tool\b",
r"administrative decisions? under an Act",
r"\bState contract\b",
```

- Add `r"\bAIAF"` to `CASE_SENSITIVE`.
- New area `"workplace surveillance"`: `r"Workplace Surveillance Act"`,
  `r"computer surveillance"`, `r"staff prompts? (?:are )?logged"`.
- Extend `"health care"` with `r"\bHRIP Act\b"` and `r"health information"`.
- Extend `"law enforcement"` with `r"\bfines? administration\b"` and
  `r"infringement notices?"`.

### New legal references (extend `LEGAL_REF`)

The checker then requires `checked <date>` beside their applicability dates:

```
|PPIP Act|PPIPA|HRIP Act|HRIPA|IPPs?\s?\d+|HPPs?\s?\d+|Part 6A|MNDB
|GIPA Act|State Records Act|Workplace Surveillance Act|Anti-Discrimination Act
|DCS-20\d\d-\d\d|PBD-20\d\d-\d\d|ICTA|Core&|AIAF|Operational Policy
|Cyber Security Policy|Essential Eight|Appendix [A-D]\b|AGT\.\d
```

Also accept `cl\.?\s?\d+(\.\d+)*` for contract clauses such as ICTA 6.11.

### New marker

Add `agency` to `MARKER` and `GAP_LINE`. `agency:` means only the agency
can answer: a form field for agency officers, or an agency decision. It
counts as "cite or flag", like `counsel:`, and the closing summary counts it
separately. A `government-form-answers.md` must list every question of the
form version it names. A missing number is an error, which catches
forgotten rows; the check needs the crosswalk's question list in the
reference or the script.

### Version-drift warning

When `government-form-answers.md` names `form_version` and `form_checked`,
warn when `form_checked` is more than 90 days old. That is shorter than the
180 days used for laws, because forms move faster.

### Jurisdiction rule

A `government-form-answers.md` requires `au` in `jurisdictions`.

## D3. Additions to `australia.md`

Replace the "Commonwealth and state government clients" section with
corrected facts and pointers (all checked 2026-10-26):

- **DTA policy** (wording correction):
  - v2.0 took effect on 15 December 2025; v2.1 minor updates were published
    on 21 October 2026.
  - "The AI impact assessment tool v1.0 was published on 1 December 2025."
  - "Agencies must begin assessments within 12 months": in-scope use cases
    by 15 December 2026, existing use cases by 30 April 2027.
  - The tool rates **inherent** risk at section 3; sections 5 to 12 follow
    if any risk is medium or high.
  - Inherent high risk: report to the accountable official, a board or SES
    governance, report to the DTA at deployment, review every 12 months.
  - Add **the Commonwealth AI Review Committee**: non-binding advice for
    residual high-risk, or highly sensitive, novel or complex use cases;
    PROTECTED and below.
  - Add the usage-pattern drift (tool v1.0 lists four; Appendix D v2.1
    lists seven).
  - Add the AI model clauses (17 March 2025) as the vendor's contract
    duties.
  - Pointer: crosswalks in `au-government-crosswalks.md`.
- **NSW** (replace the current two lines):
  - **DCS-2026-02** (30 July 2026, updated 1 September 2026) mandates the
    **NSW AI Operational Policy v1.1**, which replaces the NSW AI Ethics
    Policy and adopts Australia's eight AI Ethics Principles.
  - Agencies must register **every** AI use case on the AIAF Platform
    (mandatory from 30 September 2026). Registration decides whether an
    AIAF assessment is needed.
  - **High or critical** intrinsic risk goes to the AI Review Committee
    within five business days.
  - The first annual attestation is due 31 October 2027.
  - Projects of $5 million or more, or funded by the Digital Restart Fund,
    get Digital Assurance Framework gateway oversight. **Cost alone does not
    trigger AIRC referral.**
  - The Operational Policy does not bind suppliers. Supplier AI is governed
    by ICTA clause 6.11 and the Core& terms.
- **NSW state privacy** (new subsection; facts from Part C):
  - PPIP Act IPPs, with s 19(2) transborder disclosure and the
    Commissioner's "reasonable steps" contract expectations.
  - The MNDB scheme (Part 6A) from 28 November 2023, with its 30-day
    assessment.
  - HRIP Act HPPs for health information (HPP 14 transborder).
  - The IPC AI PIA guide (December 2024).
  - GIPA contracts register for contracts of $150,000 or more.
  - State Records Act 1998 and Regulation 2024: AI outputs and metadata are
    State records.
  - NSW Cyber Security Policy 2026–2027: ML1 baseline, 24-hour reporting,
    supplier contract clauses.
- **Roles:**
  - Under a NSW State contract, s 7B(5) takes the consultancy's acts under
    that contract out of the Privacy Act. The PPIP Act binds the **agency**,
    and the contract must carry the IPPs to the contractor.
  - The consultancy stays an APP entity for its other handling, and its
    staff access from outside NSW is an s 19(2) question for the agency.
  - Write NSW sections in NSW terms: personal information, health
    information, IPP, HPP, public sector agency, privacy management plan,
    eligible data breach under Part 6A. Never use APP terms for the agency's
    duties.
- **Screening checklist rows to add:**
  - NSW agency client → AIAF, PPIP and HRIP, MNDB, GIPA, State Records, NSW
    Cyber Security Policy, ICTA 6.11.
  - Staff in NSW and prompt logging → Workplace Surveillance Act notice (14
    days, wait `W`).
  - Health information → HRIP Act.
  - Contract of $150,000 or more → GIPA register entry (the agency's).
- **Counsel questions to add:**
  - Is the model endpoint, logging or support access a "disclosure" to a
    recipient outside NSW (s 19(2)), or a "use" (IPC: contractor access for
    the contracted service is "likely to be a 'use'")?
  - Which s 19(2) ground is relied on?
  - Does s 7B(5) cover all of the consultancy's acts?
  - Is prompt logging "computer surveillance"?
  - Is any AI-informed action an "administrative decision under an Act"
    needing express authority?

## D4. Additions to the jurisdiction screen

**Facts to establish.** Split the client-type row: "state or local
government" becomes "NSW public sector agency (DCS-2026-02 entity types:
departments, executive agencies, separate agencies, statutory bodies, SOCs,
public financial and non-financial corporations, advisory entities); other
state; local council". Add a fact row:

| Fact | Why it matters | Usual home in the record |
| --- | --- | --- |
| Contract vehicle and value: ICTA or Core&, value against $150,000 and $1 million (ex GST), DAF registration at $5 million | GIPA register; ICTA 6.11 AI clauses; DAF gateway | SOW; brief stakeholders; `agency:` |

**New row in "When each regime is in scope"** (the regime code stays `au`;
this adds a state-government sub-screen, not a fifth code):

| Regime | In scope when any of these holds | Notes |
| --- | --- | --- |
| `au` — NSW government client | The client is a NSW public sector agency or SOC, or the consultancy works under a NSW State contract | Add the NSW sections: AIAF registration and assessment (agency), PPIP and HRIP Acts (s 19(2)), MNDB Part 6A, GIPA, State Records Act 1998, NSW Cyber Security Policy, Workplace Surveillance Act when staff prompts are logged. Commonwealth Privacy Act: the consultancy's acts under the State contract fall under s 7B(5); its other acts stay under the APPs (`counsel:`). Always `counsel_required: yes` |
| `au` — Commonwealth client | The client is a non-corporate Commonwealth entity (corporate entities opt in) | DTA policy v2.1; DTA tool v1.0; Agencies Privacy Code PIA; s 95B contract terms. Always `counsel_required: yes` |

**"What each regime adds to each document"** gains a column note for `au`
government clients:
- Regulatory memo: new section "Australia: NSW government" or "Australia:
  Commonwealth government".
- Privacy impact input pack: "NSW: IPP and HPP check (IPC AI PIA guide)"
  replaces the APP check for the agency's handling.
- Security questionnaire: NSW Cyber Security Policy mapping; incident
  clocks (24 hours to Cyber Security NSW; MNDB; ICTA immediate notice, then
  details within 48 hours).
- System card: AIAF transparency, appeal and non-AI alternative facts.
- New `government-form-answers.md`.

**"Documents the pack names but the client's process produces"**: replace
the NSW row with:

| Document | Regime and trigger | Inputs come from |
| --- | --- | --- |
| AIAF Platform registration and, where required, AIAF assessment; AIRC referral for high or critical | Australia: NSW agency; platform mandatory since 30 September 2026; AIRC within 5 business days of completing the AIAF (checked 2026-10-26) | government-form-answers.md AIAF sections; impact assessment; input pack |
| Agency PIA (IPC Guide to PIAs in NSW and the AI PIA guide) | Australia: NSW agency handling personal or health information | Input pack "NSW: IPP and HPP check" |
| Privacy management plan update; MNDB data breach policy and register entry | Australia: NSW agency | Input pack; security questionnaire |
| GIPA contract register entry | Australia: NSW agency, contract of $150,000 or more (incl. GST) | SOW facts |
| DAF gateway review | Australia: NSW project with estimated total cost of $5 million or more, or DRF funded | Design, plan, evaluation reports |
| Commonwealth AI Review Committee advice | Australia: NCE use case with residual high risk, or highly sensitive, novel or complex | government-form-answers.md DTA section |

