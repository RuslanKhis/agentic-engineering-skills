# United States: AI and privacy law for the governance pack

*Read 26 October 2026. Research for adding the United States to
`skills/adk-governance-pack`, for clients that are US companies or that
serve US residents. Drafts, not legal advice.*

## Conclusion

The United States has no AI Act and no federal privacy statute, and no
federal law preempts state AI laws as of today. A US "classification memo"
is therefore not a risk-tier classification. It is a **regime screen**, as
for Australia: which federal and state laws the agent falls under,
triggered by facts the design already records (where the client is, which
states' residents it serves, its revenue and data volumes, the data
categories, whether an output feeds a consequential decision, whether the
agent is used on employees or applicants, and whether it chats with
consumers).

What changes the pack, in order of weight:

1. **Federal preemption is a campaign, not a law.** EO 14365 (11 December
   2025) set up a DOJ AI Litigation Task Force, a Commerce list of
   "onerous" state laws (not published as far as can be found), funding
   conditions (not issued) and an FTC policy statement (only proposed, 7
   July 2026). The White House's legislative recommendations (20 March
   2026) are non-binding, and no preemption bill has left committee. State
   laws apply unless a court rules otherwise. Every US memo must say so
   with the date, because this can change quickly.
2. **California's CPPA (now "CalPrivacy") regulations are the heaviest
   paperwork.** In force from 1 January 2026, checked 2026-10-26. A
   *risk assessment* is required before processing sensitive personal
   information, using automated decisionmaking technology (ADMT) for a
   significant decision, or inferring traits of employees or applicants
   by systematic observation. The ADMT duties (pre-use notice, opt-out or
   human appeal, access) apply from 1 January 2027. Risk-assessment
   attestations are due to the agency by 1 April 2028. California is the
   only state whose privacy law covers employee data. Its §7152 content
   list is close to the DPIA input pack and adds a named approver and a
   go/no-go decision.
3. **Nineteen state privacy laws in force (twenty-three signed) mostly
   require a "data protection assessment"** for profiling with a risk of harm and for sensitive data,
   and give an opt-out from profiling for decisions with legal or
   similarly significant effects. The DPIA input pack can serve as that
   assessment if it carries a US variant of the screening and legal-basis
   sections (there is no lawful-basis test; sensitive data needs opt-in
   consent).
4. **Employment uses carry the most specific duties.** NYC Local Law 144
   (independent bias audit, published summary, 10 business days' notice),
   Illinois HB 3773 (in force 1 January 2026: no discriminatory effect,
   no zip-code proxies, notice to employees), California's FEHA
   automated-decision system regulations (in force 1 October 2025: vendors
   can be the employer's "agent", four-year retention of ADS data,
   anti-bias testing as evidence), California SB 947 (discipline and
   termination, 1 July 2027) and Connecticut PA 26-15 (pre-decision notice,
   1 October 2027). Federal Title VII disparate impact is still statute,
   even though federal agencies have stopped enforcing it.
5. **Colorado's AI Act never took effect.** SB 24-205 was repealed and
   re-enacted on 14 May 2026 as SB 26-189 (automated decision-making
   technology). Its main duties apply from 1 January 2027: notice before
   a consequential decision, an explanation within 30 days of an adverse
   outcome, correction and human review, three-year records. It has **no
   impact assessment, no risk-management programme and no NIST AI RMF
   affirmative defence**. A federal court has stopped the Attorney
   General enforcing it until rulemaking finishes and the xAI case is
   decided.
6. **Chatbot laws multiplied.** A plain customer-service agent meets
   disclosure duties (Utah on request, Maine, California's bot law when
   selling, California AB 1609 for businesses over $500 million from 1
   January 2027 with a human hand-off within 15 minutes). Companion-chatbot
   laws (California SB 243, New York, Washington, Connecticut, Colorado
   HB 26-1263 and about six more) almost all exclude customer-service
   bots. A persona that remembers the user and sustains a relationship
   brings them in.
7. **NIST AI RMF is a legal shield in one state only.** Texas TRAIGA gives
   no liability when a violation is found through an internal review that
   substantially complies with the NIST AI RMF Generative AI Profile, or
   through red-teaming. Elsewhere it is a reference, not a defence. The
   impact assessment's existing NIST mapping therefore does real work for
   Texas and is good evidence elsewhere.

Federal law that binds a private deployer today is FTC Act Section 5 (no
deceptive claims about what the agent can do; the Rite Aid order is the
template for "reasonable safeguards"), the amended COPPA Rule (compliance
from 22 April 2026), and sector statutes: HIPAA (a business associate
agreement when the agent touches PHI), GLBA (vendor contract terms; FTC
breach notice in 30 days), FCRA (adverse action; avoid becoming a consumer
reporting agency), ECOA Regulation B (specific principal reasons for
adverse credit action, unchanged even though the CFPB's AI circulars were
withdrawn), Title VII and ADA, and the TCPA when the agent places calls.

For the pack: the classification memo gets a US regime screen (or a
sibling `us-applicability-memo.md`); the DPIA input pack gets a US
screening table and CPPA §7152 fields; the records rows gain retention
periods from CPPA (five years), FEHA (four) and Colorado (three); the
system card carries chatbot and ADMT disclosure facts; and two new
documents are worth adding: a **consumer notice pack** (pre-use ADMT
notice, adverse-outcome explanation, opt-out or appeal path, chatbot
disclosure text) and, for employment, a **bias audit input pack** for
NYC Local Law 144 and FEHA anti-bias testing.

## Sources

Five research subagents read these on 26 October 2026; the coordinator
re-read the items marked "coordinator". PRIMARY means the government's
own site, the Federal Register, eCFR, govinfo, api.congress.gov, a
legislature's site, or an agency PDF. SECONDARY means law-firm, tracker or
news pages. Blocked sites: leginfo.legislature.ca.gov (Cloudflare 403),
ilga.gov (SSL error), hhs.gov, dol.gov, reginfo.gov and congress.gov web
pages (403; the congress.gov API worked). Anything resting on those is
marked "not verified at a primary source" in its section.

### Primary

| Source | What it supports |
| --- | --- |
| EO 14179, 90 FR 8741, <https://www.federalregister.gov/documents/2025/01/31/2025-02172/removing-barriers-to-american-leadership-in-artificial-intelligence> | Revocation of EO 14110; Action Plan ordered |
| EO 14365, 90 FR 58499, <https://www.govinfo.gov/content/pkg/FR-2025-12-16/pdf/2025-23092.pdf>; <https://www.whitehouse.gov/presidential-actions/2025/12/eliminating-state-law-obstruction-of-national-artificial-intelligence-policy/> | Task Force, Commerce list, BEAD, FCC, FTC, legislative recommendation |
| AG memo creating the AI Litigation Task Force, 9 January 2026, <https://www.justice.gov/ag/media/1422986/dl?inline=> | Task Force exists (date from file metadata) |
| DOJ intervention in *X.AI LLC v. Weiser*, <https://www.justice.gov/opa/pr/justice-department-intervenes-xai-lawsuit-challenging-colorados-algorithmic-discrimination> | Colorado challenge |
| White House legislative recommendations, 20 March 2026, <https://www.whitehouse.gov/wp-content/uploads/2026/03/03.20.26-National-Policy-Framework-for-Artificial-Intelligence-Legislative-Recommendations.pdf> | Proposed preemption scope and carve-outs |
| America's AI Action Plan, July 2025, <https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf> | Opened, text not extractable; content from secondary summaries |
| "Inaugurating the Era of Super Intelligence" fact sheet, 29 September 2026, <https://www.whitehouse.gov/fact-sheets/2026/09/fact-sheet-president-donald-j-trump-inaugurates-the-era-of-super-intelligence/> (coordinator) | Federal documents now say "SI" for AI |
| api.congress.gov: S.2750, H.R.5388, H.R.9925 | No preemption statute |
| FTC proposed policy statement on suppression of accuracy, 91 FR 41638, <https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-seeks-public-comment-policy-statement-addressing-ai-accuracy> | Proposed preemption theory |
| FTC "Ditches Disparate Impact", 7 August 2026, <https://www.ftc.gov/news-events/news/press-releases/2026/08/ftc-ditches-disparate-impact> (coordinator) | FTC drops disparate-impact claims |
| FTC Operation AI Comply, Rytr set-aside, Workado, Air AI, Rite Aid, 6(b) chatbot orders (URLs in §1.2) | Section 5 enforcement |
| Amended COPPA Rule, 90 FR 16918, <https://www.govinfo.gov/content/pkg/FR-2025-04-22/html/2025-05904.htm> | Dates and duties |
| FTC TAKE IT DOWN Act pages, <https://www.ftc.gov/news-events/news/press-releases/2026/05/ftc-begins-enforcing-take-it-down-act> | Platform duties |
| eCFR: 45 CFR 160.103, 92.210; 12 CFR 1016; 16 CFR 314; 12 CFR 1002.9; 29 CFR 1607.4 | Sector rule text (current to 22 October 2026) |
| Federal Register: HIPAA Security NPRM 2024-30983; Section 1557 notice 2026-11015; CFPB withdrawals 2025-08286, 2025-08644; Reg B final rule 2026-07804; EO 14281 2025-07378 | Sector rule status |
| <https://www.consumerfinance.gov/compliance/guidance/withdrawn-guidance/> | Circulars 2022-03, 2023-03, 2024-06 withdrawn |
| FCC Declaratory Ruling FCC 24-17, <https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf> | AI voices under the TCPA |
| Colorado SB 26-189, <https://leg.colorado.gov/bills/sb26-189> (coordinator) and fiscal note <https://leg.colorado.gov/bill_files/117715/download>; HB 26-1263, <https://leg.colorado.gov/bills/hb26-1263> | Colorado replacement law and chatbot law |
| Texas HB 149 enrolled, <https://capitol.texas.gov/tlodocs/89R/billtext/html/HB00149F.htm> | TRAIGA text |
| Utah SB 226 (2025) and HB 320 (2026) enrolled, <https://le.utah.gov/Session/2025/bills/enrolled/SB0226.pdf>, <https://le.utah.gov/Session/2026/bills/enrolled/HB0320.pdf> | Utah disclosure rules |
| NYC DCWP AEDT page, <https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page> | Local Law 144 |
| Connecticut PA 26-15 summary, <https://www.cga.ct.gov/2026/SUM/PDF/2026SUM00015-R02SB-00005-SUM.PDF> | Companion and employment provisions |
| New York GBL §§1700, 1703, <https://www.nysenate.gov/legislation/laws/GBS/1700> | AI companion models |
| CPPA regulations text, <https://cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_appr_text.pdf>; <https://cppa.ca.gov/regulations/ccpa_updates.html>; <https://www.cppa.ca.gov/regulations/cpi_adjustment.html> | ADMT, risk assessment, audits, thresholds |
| Civil Rights Council ADS final text, <https://calcivilrights.ca.gov/wp-content/uploads/sites/32/2025/06/Final-Text-regulations-automated-employment-decision-systems.pdf> | FEHA ADS rules |
| SB 243 chaptered text (Sidley mirror of Ch. 677), <https://www.sidley.com/en/-/media/resource-pages/ai-monitor/laws-and-regulations/cal-sb243-companion-chatbots.pdf?la=en> | Companion chatbots |
| CDT SB 53 page, <https://www.cdt.ca.gov/technology-innovation/transparency-in-frontier-ai-act/> | Frontier thresholds |
| Governor's releases of 10, 16 and 30 September 2026, gov.ca.gov (coordinator read 30 September) | 2026 signings |
| Assemblymember Zbur release on AB 1609, <https://zbur.asmdc.org/press-releases/20260929-californians-gain-right-human-customer-service-under-new-zbur-law> (coordinator) | Right to Human Customer Service Act |
| NAIC model bulletin, <https://content.naic.org/sites/default/files/cmte-h-big-data-artificial-intelligence-wg-ai-model-bulletin.pdf.pdf> | Insurers' AI programme |

| NIST AI RMF page, <https://www.nist.gov/itl/ai-risk-management-framework> (coordinator) | 1.0 "being revised"; AI 600-1 current; critical-infrastructure profile concept note |
| NIST IR 8596 initial preliminary draft, <https://csrc.nist.gov/pubs/ir/8596/iprd>; COSAiS/COSIS, <https://csrc.nist.gov/projects/cosais>; AI Agent Standards Initiative, <https://www.nist.gov/caisi/ai-agent-standards-initiative>; Zero Drafts, <https://www.nist.gov/artificial-intelligence/ai-research/nists-ai-standards-zero-drafts-pilot-project-accelerate>; <https://www.nist.gov/caisi> | New NIST work relevant to agents |
| Minnesota Stat. 325M.14 and 325M.18, <https://www.revisor.mn.gov/statutes/cite/325M.14> | Right to question profiling; assessments and inventory |
| Maryland SB 541 (MODPA) bill page, <https://mgaleg.maryland.gov/mgawebsite/Legislation/Details/sb0541?ys=2024RS> | Effective date |
| Washington RCW 19.375 and 19.373, <https://app.leg.wa.gov/RCW/default.aspx?cite=19.375&full=true>, <https://app.leg.wa.gov/RCW/default.aspx?cite=19.373&full=true> | Biometrics; My Health My Data |
| Colorado HB 24-1130, <https://leg.colorado.gov/bills/hb24-1130> | Biometric amendment |
| CPPA announcement of approval, <https://www.cppa.ca.gov/announcements/2025/20250923.html> | Dates |

### Secondary (used where primary was blocked or silent)

Arnold & Porter, Taft, Akin and Jenner on Colorado SB 26-189 and the xAI
case; Norton Rose Fulbright and McDermott on the enforcement stay;
K&L Gates and Benton on the unpublished Commerce list; Roll Call on BEAD;
MoFo, WSGR, Holland & Knight, Morgan Lewis, CHCF, Inside Privacy and
NatLawReview on California's 2026 session; CAIDP and AGORA on AB 2013;
Seyfarth and Ogletree on the Illinois rules; DLA Piper on the NYC audit;
Hunton on Washington HB 2225; privacyworld.blog for the 2026 chatbot-law
roundup; Goodwin on the CFPB funding case; Ogletree and DirectEmployers on
the Uniform Guidelines rescission; Cooley on removed EEOC guidance;
clearinghouse.net on *Mobley v. Workday*. URLs are given where each is
used.


For the state privacy table: the IAPP tracker (updated 8 September 2026,
<https://iapp.org/resources/article/us-state-privacy-legislation-tracker/>)
and its signed-laws chart (dated 29 June 2026); Hunton on Oklahoma and
Alabama; Troutman on Louisiana; Mayer Brown on Vermont; OneTrust and FPF
on Connecticut's 2025 and 2026 changes; Sidley on *Clay v. Union Pacific*
(BIPA); National Law Review and Holland & Knight on SB 26-189 removing the
framework safe harbour.

## How to read each entry

Each law has four parts: **(a) status and dates**, **(b) triggers** a
screening step can test, **(c) paperwork** mapped to the pack's documents
(memo = classification memo or US regime screen; IA = impact assessment;
DPA = DPIA input pack used as a data protection assessment; records;
card = system card; questionnaire), and **(d) counsel** questions. Dates
are in words with "checked 2026-10-26" as the checker expects.

## 1. Federal

### 1.1 Executive orders and preemption

**(a) Status.**

- EO 14179, *Removing Barriers to American Leadership in AI*, signed 23
  January 2025, 90 FR 8741, checked 2026-10-26. Revoked EO 14110 and
  ordered an AI Action Plan. No duties on private companies.
- EO 14365, *Ensuring a National Policy Framework for Artificial
  Intelligence*, signed 11 December 2025, 90 FR 58499, checked
  2026-10-26. It preempts nothing by itself. Its parts:
  - AI Litigation Task Force: created by an Attorney General memo of 9
    January 2026. No DOJ lawsuit against a state found. DOJ intervened on
    24 April 2026 in *X.AI LLC v. Weiser* (D. Colo., No. 1:26-cv-01515),
    which challenges Colorado's law on equal-protection grounds (PRIMARY,
    DOJ release above). No DOJ action against California found.
  - Commerce evaluation of "onerous" state laws, due about 11 March 2026:
    not published as far as can be found (SECONDARY:
    <https://www.klgates.com/thought-leadership/How-AI-Governance-Is-Being-Built-in-Real-Time-and-What-Comes-Next-5-26-2026>).
  - BEAD non-deployment funding condition: NTIA notice not issued; FAQ v18
    of 2 March 2026 says guidance is pending (PRIMARY,
    <https://broadbandusa.ntia.gov/sites/default/files/2026-03/BEAD_FAQs_v18_03_02_26.pdf>).
  - FCC proceeding on a preemptive disclosure standard: waits for the
    Commerce list; none found.
  - FTC policy statement: issued only as a *proposed* statement on 7 July
    2026 (91 FR 41638, docket FTC-2026-0859), saying covert steering of
    outputs may be deceptive and that state laws requiring it (Colorado
    named) are impliedly preempted to the extent they conflict. Not final.
  - Legislative recommendations delivered 20 March 2026: preempt state AI
    laws that "impose undue burdens", with carve-outs for generally
    applicable consumer protection, child safety, AI infrastructure zoning
    and state procurement. Non-binding.
- America's AI Action Plan, released 23 July 2025, checked 2026-10-26.
  Not self-executing. Relevant parts (SECONDARY summaries; PDF text not
  extractable): FTC to revisit orders that "unduly burden AI innovation"
  (it set aside the Rytr order on 22 December 2025 citing the plan,
  PRIMARY); funding to weigh state AI climates; NIST to revise the AI RMF
  to remove misinformation, DEI and climate references.
- Federal legislation: no preemption statute. S.2750 (SANDBOX Act,
  referred 10 September 2025), H.R.5388 (American AI Leadership and
  Uniformity Act, in subcommittee since 19 December 2025) and H.R.9925
  (FRONTIER Act, introduced 23 July 2026, frontier developers only, keeps
  state rules on deployers) have not left committee (PRIMARY,
  api.congress.gov). The ten-year moratorium was struck 99–1 on 1 July
  2025 and preemption was dropped from the FY2026 NDAA (SECONDARY).
- EO 14434, *Inaugurating the Era of Super Intelligence*, 29 September
  2026: agencies must say "Super Intelligence" and "SI" instead of "AI"
  in non-statutory documents (PRIMARY, fact sheet, coordinator). It
  imposes nothing on private companies, but new federal guidance will be
  indexed under "SI" (the FTC's AI hub already is).
- OMB M-25-21, M-25-22 and M-26-04 bind federal agencies and their
  contractors only (PRIMARY,
  <https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/>).

**(b) Triggers.** None for a private client. A federal-agency client or
subcontract brings in the OMB memos (M-26-04 asks LLM vendors for model,
system or data cards and acceptable-use policies).

**(c) Paperwork.** Memo: a "Federal preemption status" line with the date,
saying no statute preempts the state laws screened and naming any court
order that stays one (today: Colorado). Card or IA: if system prompts or
guardrails steer substantive outputs, record why, and do not market the
agent as "objective" (FTC proposed statement).

**(d) Counsel.** Does any court order or final FTC statement affect a
state law the memo relies on? Is the client a federal contractor?

### 1.2 FTC Act Section 5, COPPA and the TAKE IT DOWN Act

**(a) Status.**

- Section 5 enforcement on AI focuses on deceptive capability claims
  ("AI-washing") and fraud. Operation AI Comply was announced 25
  September 2024 (PRIMARY,
  <https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes>).
  Later orders: DoNotPay (final 11 February 2025; no unsupported "robot
  lawyer" claims); Workado (final 28 August 2025; accuracy claims about
  AI detection need competent and reliable evidence, PRIMARY,
  <https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-approves-final-order-against-workado-llc-which-misrepresented-accuracy-its-artificial>);
  Air AI (settlement announced 24 March 2026); IntelliVision (13 January
  2025, unsupported "bias-free" facial-recognition claims). The Rytr
  order was set aside on 22 December 2025 (PRIMARY,
  <https://www.ftc.gov/news-events/news/press-releases/2025/12/ftc-reopens-sets-aside-rytr-final-order-response-trump-administrations-ai-action-plan>).
- On 7 August 2026 the FTC said it will not bring disparate-impact or
  "unfair discrimination" claims under Section 5 or ECOA (PRIMARY,
  coordinator). Disparate treatment stays in scope.
- Rite Aid (complaint 19 December 2023; stipulated order filed 8 March
  2024): five-year ban on facial recognition for surveillance, deletion
  of images and derived models, and for any future biometric system a
  monitoring programme with a risk assessment, pre-deployment and ongoing
  accuracy and bias testing, consumer notice, complaints, retention limits
  and shutdown if risks cannot be controlled (PRIMARY,
  <https://www.ftc.gov/legal-library/browse/cases-proceedings/2023190-rite-aid-corporation-ftc-v>).
  It remains the clearest federal statement of what "reasonable" AI
  safeguards look like.
- 6(b) inquiry into AI companion chatbots (orders 11 September 2025 to
  seven firms, PRIMARY,
  <https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions>):
  no report found.
- Amended COPPA Rule: published 22 April 2025 (90 FR 16918), effective 23
  June 2025, compliance from 22 April 2026, checked 2026-10-26, except
  the safe-harbour provisions. Separate verifiable parental consent before
  disclosing children's data to third parties (including for AI training
  or targeted advertising), a written retention policy and a written
  security programme. An age-verification enforcement policy statement
  followed on 25 February 2026.
- TAKE IT DOWN Act, Public Law 119-12, signed 19 May 2025: covered
  platforms must remove reported non-consensual intimate images,
  including AI forgeries, within 48 hours; FTC enforcement from 19 May
  2026, checked 2026-10-26.

**(b) Triggers.** Any marketing or sales claim about the agent's accuracy,
autonomy, "bias-free" operation or savings (Section 5). Any biometric
identification (Rite Aid). A service directed to children under 13 or
actual knowledge of their data (COPPA). An agent that hosts or publishes
user-generated images or video (TAKE IT DOWN).

**(c) Paperwork.** Card: every capability or accuracy claim the client
will make publicly cites an M record; the card's "Limits" section is what
substantiates marketing. IA: for biometric features, the Rite Aid
programme elements as measures. DPA: COPPA consent and retention policy
when children are in scope. Questionnaire: written security programme
(COPPA) cites the security baseline.

**(d) Counsel.** Are the client's public claims about the agent
substantiated by the evidence cited? Is the service directed to children
or likely to have actual knowledge of under-13 users?

### 1.3 Sector statutes

**HIPAA.** (a) Business associate definition at 45 CFR 160.103 (PRIMARY,
<https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-160/subpart-A/section-160.103>).
The Security Rule overhaul proposed on 6 January 2025 (90 FR 898) is
neither final nor withdrawn; secondary sources put the final rule in
July 2027. Section 1557's rule on patient care decision support tools
(45 CFR 92.210) is in force: non-discrimination from 5 July 2024 and the
duties to identify and mitigate risk from 1 May 2025, checked 2026-10-26;
the October 2025 vacatur in *Tennessee v. Kennedy* touched only gender
identity provisions (PRIMARY, 91 FR 32887,
<https://www.federalregister.gov/documents/2026/06/02/2026-11015>).
(b) The agent creates, receives, stores, logs or transmits PHI for a
health plan, provider or clearinghouse (the consultancy becomes a
business associate and Google Cloud a subcontractor); for 92.210, the
client receives HHS funding and the agent supports care decisions.
(c) DPA: a BAA chain (client, consultancy, Google Cloud) as a processor
row; records: PHI flows including logs; IA: for 92.210, an inventory of
input variables that measure race, colour, national origin, sex, age or
disability, and a mitigation record. Questionnaire: Security Rule risk
analysis. (d) Is the client a covered entity? Is the data PHI or
de-identified? Does Google's BAA cover every service in the design?

**GLBA.** (a) Regulation P (12 CFR 1016.13) lets a financial institution
share data with a vendor under a contract limiting use to the contracted
purpose. The FTC Safeguards Rule (16 CFR 314) requires vendor oversight
(314.4(f)) and, from 13 May 2024, notice to the FTC within 30 days of an
unencrypted-data breach affecting 500 or more consumers (314.4(j)),
checked 2026-10-26 (PRIMARY, eCFR). (b) The client is a bank, lender,
broker, insurer, tax preparer, auto dealer or other financial
institution and the agent handles customer information. (c) DPA: purpose
limit (no training or reuse); questionnaire: vendor safeguards and an
incident-reporting clock short enough for the 30-day notice. (d) Which
regulator's Safeguards Rule applies (FTC or a banking agency)?

**FCRA.** (a) Statute unchanged; the CFPB withdrew its proposed data
broker rule on 15 May 2025 (90 FR 20568) and Circular 2024-06 on worker
dossiers and algorithmic scores on 12 May 2025, checked 2026-10-26
(PRIMARY). (b) The agent assembles or evaluates information about people
from sources other than the client and returns it for credit, insurance,
employment or tenancy decisions (risk that the consultancy or client
becomes a consumer reporting agency); or the client uses consumer reports
in a decision the agent supports. (c) Memo: a CRA-risk line; card:
adverse action and pre-adverse-action (employment) notices where reports
are used; DPA: data sources. (d) Is any output a "consumer report"?

**ECOA and Regulation B.** (a) 12 CFR 1002.9(b)(2) still requires
specific principal reasons in adverse action notices; "failed to reach a
qualifying score" is insufficient (PRIMARY, eCFR). CFPB Circulars 2022-03
and 2023-03 on complex algorithms were withdrawn on 12 May 2025 (90 FR
20084), but the rule they explained is unchanged. A final Regulation B
rule (published 22 April 2026, effective 21 July 2026, checked
2026-10-26) removes the disparate-impact "effects test" from the CFPB's
reading of ECOA (PRIMARY,
<https://www.federalregister.gov/documents/2026/04/22/2026-07804/equal-credit-opportunity-act-regulation-b>).
EO 14281 (23 April 2025, 90 FR 17537) tells agencies to deprioritise
disparate-impact enforcement; private plaintiffs and states are
unaffected. The CFPB's funding is in litigation (SECONDARY, Goodwin,
<https://www.goodwinlaw.com/en/insights/blogs/2026/10/court-vacates-cfpb-directors-bid-to-zero-out-funds>).
(b) The agent scores, ranks or recommends in a credit decision.
(c) IA and card: the system must be able to produce principal reasons
per decision (an evaluation case shows it); records: reason codes per
decision. (d) Does the creditor rely on the output, and do the reasons
reflect the model's actual drivers?

**Title VII, ADA and the EEOC.** (a) The EEOC's 2022 and 2023 AI
technical-assistance documents now return 404 (PRIMARY, checked by HTTP
status). The four-fifths rule (29 CFR 1607.4(D)) is still codified; a
final rule rescinding the interpretive Uniform Guidelines went to OIRA on
16 October 2026 (SECONDARY only, not verified). Title VII §703(k)
disparate impact and the ADA's accommodation duty (42 USC 12112(b)(5))
are statute. *Mobley v. Workday* (N.D. Cal.; ADEA collective
conditionally certified 16 May 2025) tests vendor liability as the
employer's agent (SECONDARY, <https://clearinghouse.net/case/44074/>).
(b) Any employment use: screening, ranking, scheduling, performance,
discipline. (c) IA: adverse-impact analysis by group (selection rates,
four-fifths ratio, statistical tests), validation and less-discriminatory
alternatives; card: notice of AI use and an accommodation or alternative
assessment route; memo: vendor-as-agent exposure for the consultancy.
(d) Is the consultancy an "agent" of the employer? Will the client keep
the adverse-impact file after the Uniform Guidelines change?

**TCPA.** (a) FCC 24-17 (released 8 February 2024): AI-generated voices
are "artificial" voices; calls need prior express consent, written for
telemarketing (PRIMARY,
<https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf>). (b) The agent
places outbound calls or voicemails to US numbers. (c) Card: caller
identification and opt-out script; records: consent records; DPA:
Do Not Call checks. (d) Is the consent captured sufficient for the call
type?

## 2. State AI laws (outside California)

### 2.1 Colorado: SB 26-189 (replacing SB 24-205) and HB 26-1263

**(a) Status.** SB 24-205 was delayed to 30 June 2026 by SB25B-004 and
then repealed and re-enacted by SB 26-189, *Automated Decision-Making
Technology*, signed 14 May 2026, Session Law Chapter 131 (PRIMARY,
coordinator, <https://leg.colorado.gov/bills/sb26-189>). Disclosure,
consumer-rights and enforcement sections took effect 14 May 2026; the
rest applies to consequential decisions made on or after 1 January 2027,
checked 2026-10-26. On 27 April 2026 the federal court ordered the
Attorney General not to enforce SB 24-205 "or any legislation amending"
it until rulemaking finishes and the court rules in *X.AI v. Weiser*
(fiscal note; SECONDARY,
<https://www.mcdermottlaw.com/insights/colorado-ai-law-in-flux-comprehensive-replacement-bill-signed-after-federal-court-blocks-predecessors-enforcement/>).
The Attorney General's rules (4 CCR 904-6) had a revised draft on 6
October 2026 and a hearing today; rules are due by 1 January 2027
(SECONDARY, Akin). The enacted text could not be loaded (over 10 MB);
the dropped duties come from the bill page, fiscal note and four law
firms.

HB 26-1263, the Chatbot Safety Act, signed 29 May 2026, operator duties
from 1 January 2027, checked 2026-10-26 (PRIMARY,
<https://leg.colorado.gov/bills/hb26-1263>).

**(b) Triggers.** SB 26-189: the system processes personal data and its
output "materially influences" a consequential decision about a Colorado
consumer in education, employment, housing, financial or lending
services, insurance, health care or essential government services.
Chatbots that only communicate or summarise for later human review, and
customer-service triage, are excluded. HB 26-1263: a publicly available
conversational AI service offered to consumers; excludes tools primarily
for "commerce-related or transactional assistance" (whether a support
agent fits is open).

**(c) Paperwork.**

- Developer (often the consultancy, or the client under contract) to
  deployer: intended and known harmful uses, training-data categories,
  limits, instructions for monitoring and meaningful human review,
  material-change notices. The system card is the natural vehicle.
- Deployer: notice before use in a consequential decision; within 30
  days of an adverse outcome, a plain-language description of the
  decision and the ADMT's role and the consumer's rights; access,
  correction, and human review where commercially reasonable. New
  consumer notice pack.
- Records: three years for both roles.
- HB 26-1263: AI disclosure, age estimation, self-harm protocol with an
  annual report to the Attorney General, minor protections, no claim to
  be a licensed professional. Card and consumer notice pack.
- Gone with SB 24-205: impact assessments, a risk-management programme,
  the duty of reasonable care, 90-day Attorney General notice of
  discrimination, the small-deployer exemption and the NIST/ISO
  affirmative defence.

**(d) Counsel.** Is the client a developer, deployer or both? Does the
output "materially influence" the decision under the final rules' de
minimis presumption? Is enforcement still stayed? Does the
commerce/transactional carve-out cover the chatbot?

### 2.2 Texas: TRAIGA (HB 149)

**(a) Status.** In force 1 January 2026, checked 2026-10-26 (PRIMARY,
enrolled text). No 2026 regular session; no amendment found.

**(b) Triggers.** Doing business or advertising in Texas, or offering a
product used by Texas residents. Private-sector prohibitions turn on
*intent*: AI intended to incite self-harm, harm or crime (§552.052), to
infringe constitutional rights (§552.055), or to discriminate unlawfully
(§552.056; disparate impact alone is not intent); sexual deepfakes and
child-imitating sexual chat (§552.057). Disclosure (§552.051) binds
government agencies and health care providers using AI in treatment
(disclose no later than the date care begins). No general chatbot
disclosure for private businesses.

**(c) Paperwork.** The Attorney General's civil investigative demand
(§552.103) can ask for the system's purpose and use, training-data
types, inputs and outputs, performance metrics and limits, post-
deployment monitoring and safeguards: the system card and impact
assessment answer it. The safe harbour (§552.105(e)) needs evidence that
a violation was found through testing including red-teaming, or through
an internal review substantially complying with the NIST AI RMF
Generative AI Profile or another recognised framework: the IA's NIST
mapping plus the adversarial-suite results. The 60-day cure (§552.104)
requires a written statement and updated internal policies. Texas CUBI
(biometrics) was narrowed for AI training and security uses.

**(d) Counsel.** Does the IA's NIST mapping amount to "substantial
compliance" with the Generative AI Profile? Is the client a health care
provider using AI in treatment?

### 2.3 Utah: Artificial Intelligence Policy Act as amended

**(a) Status.** SB 226 (in force 7 May 2025) narrowed the consumer
disclosure to a clear and unambiguous request; regulated occupations
must disclose "high-risk" AI interactions up front (PRIMARY, enrolled
text). HB 320 (in force 6 May 2026) reworks the AI office and sandbox
but leaves the disclosure chapter alone. SB 226 and SB 332 moved the
sunset to 1 July 2027 for chapter 72 (the office); a sunset on chapter
75 (disclosure) was not seen. HB 452 (2025) regulates mental-health
chatbots (SECONDARY, FPF).
**(b) Triggers.** A generative AI agent interacting with Utah consumers;
a licensed occupation (for example health, finance, legal) collecting
health, financial or biometric data or giving personalised advice.
**(c) Paperwork.** Card: disclosure behaviour (answers truthfully when
asked; discloses at the outset for regulated occupations). Disclosing
clearly at the outset and throughout is a safe harbour (§13-75-104).
"The AI did it" is no defence. **(d) Counsel.** Does chapter 75 sunset?
Is the client a regulated occupation?

### 2.4 Illinois: HB 3773, AI Video Interview Act, WOPR Act

**(a) Status.** HB 3773 (Public Act 103-0804) amends the Human Rights Act
§2-102(L), in force 1 January 2026, checked 2026-10-26. IDHR's notice
rules were proposed 15 May 2026 and withdrawn 2 June 2026; no final
rules (SECONDARY,
<https://www.seyfarth.com/news-insights/illinois-department-of-human-rights-temporarily-withdraws-proposed-rules-on-use-of-artificial-intelligence-in-employment.html>).
AI Video Interview Act (820 ILCS 42) since 2020; the Wellness and
Oversight for Psychological Resources Act (HB 1806, August 2025) bans
AI therapy without a licensed professional. SB 315 (frontier, 1 January
2027) is not ours. ilga.gov was unreachable: not verified at a primary
source.
**(b) Triggers.** AI used on Illinois employees or applicants in
recruitment, hiring, promotion, discipline, discharge or terms of
employment; AI analysis of video interviews; any therapy-like chatbot.
**(c) Paperwork.** IA: discriminatory-effect analysis and a list of
proxies removed (zip code named in the statute); card and notice pack:
notice to employees that AI is used; video interviews: explanation,
consent, deletion within 30 days of request, annual demographic report.
**(d) Counsel.** What notice suffices without IDHR rules?

### 2.5 New York City Local Law 144

**(a) Status.** Enforced since 5 July 2023 under 6 RCNY ch. 5 subch. T
(PRIMARY, DCWP page). The State Comptroller's audit of 2 December 2025
called enforcement ineffective (SECONDARY, DLA Piper,
<https://www.dlapiper.com/en-au/insights/publications/2026/01/critical-audit-of-nyc-ai-hiring-law-signals-increased-risk-for-employers>).
No 2026 amendment found.
**(b) Triggers.** An employer or employment agency uses an automated
employment decision tool to screen NYC candidates or employees for hiring
or promotion.
**(c) Paperwork.** New bias audit input pack: an independent auditor's
bias audit within a year before use and yearly; a public summary with
selection or scoring rates and impact ratios by sex, race/ethnicity and
intersections; notice 10 business days before use naming the
qualifications assessed and the alternative-process route; data-source
and retention information on request (records).
**(d) Counsel.** Does the tool "substantially assist or replace"
discretionary decisions under the DCWP definition? Who is the
independent auditor?

### 2.6 Other states: chatbots, employment and insurance

- **Connecticut PA 26-15** (SB 5, signed 27 May 2026; PRIMARY, OLR
  summary). AI companions from 1 January 2027 (customer service,
  business operations, financial services and education bots excluded).
  Automated employment decision technology from 1 October 2027: written
  notice before the decision naming the tool, its purpose, data
  categories and sources and a contact; from 1 October 2026, using such
  a tool is no defence to discrimination and anti-bias testing may be
  weighed. Trigger: Connecticut employees or applicants. Paperwork:
  notice pack; IA bias evidence.
- **New York GBL Article 47** (AI companion models), in force 5 November
  2025 (PRIMARY, nysenate.gov §§1700, 1703): crisis protocol and a
  recurring not-a-human notice; customer-service and internal tools
  excluded. RAISE Act: frontier developers only.
- **Maine LD 1727** (2025): disclose a chatbot used in trade where a
  reasonable consumer could think it human (SECONDARY only,
  <https://www.compliancepoint.com/marketing-compliance/maines-new-ai-transparency-law/>).
- **2026 companion or conversational chatbot laws** (SECONDARY roundup,
  <https://www.privacyworld.blog/2026/09/u-s-ai-law-2026-midyear-state-update/>,
  not verified at a primary source): Washington HB 2225 (1 January 2027;
  private right of action; Hunton,
  <https://www.hunton.com/privacy-and-cybersecurity-law-blog/washington-state-enacts-law-regulating-ai-companion-chatbots-with-private-right-of-action>),
  Oregon SB 1546 (1 January 2027), Idaho S1297, Nebraska, Iowa SF2417
  (1 July 2027), Georgia and Hawaii SB3001 (dates conflict). Treat as a
  family: trigger is a persona that sustains a relationship; paperwork
  is a disclosure cadence, a self-harm protocol and minor protections.
- **Virginia** HB 2094 vetoed in 2025; no 2026 automated-decision law
  found. **New Jersey**: Division on Civil Rights guidance (January
  2025) that the Law Against Discrimination reaches algorithmic
  discrimination (not re-verified).
- **Insurance**: the NAIC model bulletin (adopted 4 December 2023;
  PRIMARY) expects a written AI Systems programme, vendor due diligence
  with audit clauses and consumer notice, and names the NIST AI RMF as an
  acceptable basis. Adoption list not verified. Colorado's SB 21-169
  governance regulation for insurers not verified (page blocked).
  Trigger: an insurer client. Paperwork: IA and questionnaire (vendor
  cooperation and audit rights).

## 3. California

### 3.1 CPPA (CalPrivacy) regulations: risk assessments, ADMT, audits

**(a) Status.** Adopted 24 July 2025, approved by OAL 22 September 2025,
in force 1 January 2026, checked 2026-10-26 (PRIMARY,
<https://cppa.ca.gov/regulations/ccpa_updates.html>). Key dates:

| Duty | Date (checked 2026-10-26) |
| --- | --- |
| Risk assessment before new in-scope processing | from 1 January 2026 |
| Risk assessment for processing begun before 2026 and continuing | by 31 December 2027 |
| ADMT duties for existing significant-decision use | by 1 January 2027 |
| Risk-assessment submission and executive attestation for 2026–2027 | by 1 April 2028, then each 1 April |
| First cybersecurity audit certification | 1 April 2028 (revenue over $100M), 1 April 2029 ($50–100M), 1 April 2030 (under $50M) |

Pre-rulemaking on **employee data** closed 20 May 2026; no formal package
yet. No ADMT enforcement yet.

**(b) Triggers.** The client is a "business": doing business in California
and over $26,625,000 gross revenue (2025 figure), or buying, selling or
sharing personal information of 100,000 or more consumers or households,
or 50% of revenue from selling or sharing (Civ. Code §1798.140(d)). Then:

- Risk assessment (§7150(b)) before: selling or sharing; processing
  sensitive personal information (employee data for payroll, benefits and
  similar is exempt); ADMT for a significant decision; automated
  inference of intelligence, aptitude, performance, health, behaviour and
  similar from systematic observation of applicants, students, employees
  or contractors, or from presence at a sensitive location; processing
  personal information intended to train ADMT for significant decisions
  or facial, emotion or other biometric identification.
- ADMT (§7001(e)): technology that processes personal information and
  replaces or substantially replaces human decisionmaking. A human
  reviewer who can interpret the output, reviews it with other
  information and has authority to change the decision takes it out.
- Significant decision (§7001(ddd)): financial or lending, housing,
  education, employment or contracting (hiring, work allocation, pay,
  promotion, discipline, termination), healthcare. Advertising is not.
- Cybersecurity audit: 50% revenue test, or the revenue test plus
  personal information of 250,000+ consumers or sensitive information of
  50,000+.

**(c) Paperwork.**

- DPA as CPPA risk assessment (§7152): specific purpose; categories and
  minimum necessary; collection, use, retention per category, approximate
  number of consumers, disclosures, and each service provider and why;
  for ADMT, logic with assumptions and limits and how the output is used;
  benefits; negative impacts (discrimination, loss of control, dark
  patterns, economic, physical, psychological, reputational); safeguards;
  **whether the business will proceed**; contributors; **approval date and
  approver name and position**. Review every three years, update within
  45 days of a material change, keep five years or for the life of the
  processing. A single assessment can cover comparable processing and an
  assessment for another state can be reused if supplemented (§7156).
- Consumer notice pack (ADMT): pre-use notice (§7220) at or before
  collection: purpose, opt-out or the exception relied on, access right,
  plain-language logic and output use, alternative process; opt-out with
  two methods, stop within 15 business days (§7221), or a human appeal
  exception; access responses explaining purpose, logic, outcome
  (§7222).
- Records: five-year retention of the assessment; the opt-out log.
- Questionnaire and memo: as service provider the consultancy must
  cooperate with the client's risk assessment and audit (§7050(h)), honour
  forwarded opt-outs, and, if it supplies ADMT trained on personal
  information, give the client the facts for its assessment (§7153).

**(d) Counsel.** Is the client a "business"? Does a human reviewer meet the
three-part test, so the system is not ADMT? Which §7221(b) exception
applies? Who is the approver with go/no-go authority?

### 3.2 Civil Rights Council FEHA regulations on automated-decision systems

**(a) Status.** Filed 27 June 2025, in force 1 October 2025, checked
2026-10-26, 2 CCR §11008 et seq. (PRIMARY, final text). **(b) Triggers.**
A "computational process that makes a decision or facilitates human
decision making regarding an employment benefit" (§11008.1(a)) used on
California applicants or employees: resume screening, ranking, games,
interview analysis, targeted job adverts. An "agent" acting for the
employer, including through an ADS, is itself an employer (§11008(a)).
**(c) Paperwork.** IA: anti-bias testing, with quality, recency, scope,
results and the response to them, which is relevant evidence for any
claim or defence (§11009(f)); records: four-year retention of selection
criteria and ADS data (§11013(c)); card: accommodation route and a check
that assessments do not elicit disability information. **(d) Counsel.**
Is the consultancy the employer's agent? Is the anti-bias testing
adequate?

### 3.3 SB 947 (No Robo Bosses Act) and other 2026 employment laws

**(a) Status.** Signed 30 September 2026 (PRIMARY, Governor's list);
operative 1 July 2027, checked 2026-10-26 (SECONDARY, Morgan Lewis,
<https://www.morganlewis.com/pubs/2026/10/california-enacts-new-laws-governing-employer-use-of-ai>).
Text not verified (leginfo blocked). AB 1883 (no emotion recognition in
workplace surveillance) and SB 951 (AI layoff notice) from 1 January
2027. **(b) Triggers.** An ADS used in discipline or termination of
California workers (not hiring). **(c) Paperwork.** Card and notice pack:
no sole reliance; human corroboration where primarily relied on; a
post-use notice when the decision is communicated. **(d) Counsel.** Is
reliance "primary"?

### 3.4 Chatbot and disclosure laws

- **AB 1609, Right to Human Customer Service Act.** Signed (PRIMARY,
  Zbur release, coordinator); in force 1 January 2027, checked
  2026-10-26. Large businesses serving Californians must offer human
  service in business hours, try in good faith to connect within 15
  minutes of a request or schedule an appointment, disclose when the
  representative is a chatbot and post contact details. The $500 million
  revenue threshold is SECONDARY (WSGR,
  <https://www.wsgr.com/en/insights/california-enacts-over-two-dozen-key-privacy-and-ai-bills-into-law-in-2026-legislative-session.html>).
  Trigger: a consumer customer-service agent for a large business.
  Paperwork: card (disclosure, hand-off path and its measured time);
  design contract for escalation.
- **Bot disclosure law** (B&P §§17940–17943, operative 1 July 2019): a
  bot that interacts online with a Californian to incentivise a sale or
  influence a vote, with intent to mislead about being a bot, is
  unlawful; clear disclosure is the safe harbour (SECONDARY code
  reproduction). The 10 million visitor figure defines platforms, not
  bot users.
- **SB 243, companion chatbots** (Ch. 677, in force 1 January 2026,
  checked 2026-10-26; PRIMARY chaptered text). Excludes bots used only
  for customer service, operations, productivity, internal research or
  technical help. Duties: AI notice if a person could be misled, a
  published suicide and self-harm protocol, protections for known minors,
  annual reports from 1 July 2027, private right of action. **SB 1119**
  (signed 10 September 2026; core duties 1 July 2027, SECONDARY) adds
  child-user duties including pre-launch risk assessments.
- **SB 942 AI Transparency Act** as amended by AB 853 and **SB 1000**
  (signed 30 September 2026): covered-provider duties operative 2 August
  2026; SB 1000 removed the one-million-user threshold so any publicly
  accessible generative system producing image, video or audio in
  California is covered (latent disclosures, a free verification tool);
  platform duties from 1 January 2027 (amended by AB 2713) and capture
  devices from 1 January 2028 (SECONDARY, MoFo,
  <https://www.mofo.com/resources/insights/261001-california-revamps-ai-transparency-requirements>).
  A text-only agent is likely out of scope.
- **Health care**: AB 3030 (from 1 January 2025): generative AI patient
  communications need a disclaimer and a route to a human unless a
  licensed provider reviewed them. AB 489 (from 1 January 2026): no
  implying a licensed professional. AB 1979 and SB 503 (signed 30
  September 2026, from 1 January 2027, SECONDARY): clinician judgment
  preserved; consumer health chatbots treated as providers under CMIA;
  clinical decision support developers document intended use, training
  data, evaluation and bias.

### 3.5 Not ours, but to rule out

- **SB 53** (in force 1 January 2026): frontier developers training above
  10^26 operations; large developers above $500 million revenue (PRIMARY,
  CDT). An ADK build on Gemini is not a frontier developer. Write it as
  `n/a:` in the memo.
- **AB 2013** (training-data summaries, Civ. Code §3110, from 1 January
  2026): applies to whoever "substantially modifies" a generative system,
  including by fine-tuning, for public use in California. Relevant only
  when the project fine-tunes and the result is public. *xAI v. Bonta*:
  preliminary injunction denied 4 March 2026; Ninth Circuit appeal
  pending (SECONDARY, CAIDP). Not verified at a primary source.

## 4. State comprehensive privacy laws

**(a) Status.** Twenty-three states have signed comprehensive consumer
privacy laws (IAPP chart, SECONDARY); 19 are in force today and four
start between 1 January 2027 and 1 January 2028, checked 2026-10-26.
Four were signed in 2026: Oklahoma, Alabama, Louisiana and Vermont. No
enactment after Vermont (16 June 2026) was found; Massachusetts H.5479
was in conference in August and Pennsylvania HB 78 has not passed.
Effective dates are from the IAPP chart unless marked; thresholds marked
† are from memory of the statutes and need checking at the source before
a memo relies on them.

| State (law) | In force (checked 2026-10-26) | Applies when (per year, state residents) |
| --- | --- | --- |
| California (CCPA as amended by CPRA) | 1 January 2020; CPRA 1 January 2023 | Over $26,625,000 revenue, or 100k consumers or households bought, sold or shared, or 50% revenue from selling or sharing (PRIMARY, CPPA). **Covers employees and B2B contacts** |
| Virginia (VCDPA) | 1 January 2023 | 100k; or 25k and over 50% revenue from sales† |
| Colorado (CPA) | 1 July 2023 | 100k; or 25k and any revenue or discount from sales† |
| Connecticut (CTDPA) | 1 July 2023; SB 1295 changes 1 July 2026 | Since 1 July 2026: 35k, or any sensitive data, or any sale (SECONDARY, OneTrust) |
| Utah (UCPA) | 31 December 2023 | $25M revenue and (100k, or 25k and over 50%)† |
| Texas (TDPSA) | 1 July 2024 | Any business that is not an SBA small business† |
| Oregon (OCPA) | 1 July 2024 | 100k; or 25k and 25%†; B2B data covered† |
| Montana (MCDPA) | 1 October 2024 | Lowered from 1 October 2025 to 25k, or 15k and over 25%† |
| Iowa (ICDPA) | 1 January 2025 | 100k; or 25k and over 50%† |
| Delaware (DPDPA) | 1 January 2025 | 35k; or 10k and over 20%† |
| Nebraska (NDPA) | 1 January 2025 | Texas-style small-business test† |
| New Hampshire | 1 January 2025 | 35k; or 10k and over 25%† |
| New Jersey | 15 January 2025 | 100k; or 25k and any revenue from sales† |
| Tennessee (TIPA) | 1 July 2025 | Over $25M revenue and (175k, or 25k and over 50%)† |
| Minnesota (MCDPA) | 31 July 2025 (PRIMARY, revisor) | 100k; or 25k and over 25%† |
| Maryland (MODPA) | 1 October 2025 (PRIMARY, bill page); processing from 1 April 2026† | 35k; or 10k and over 20%† |
| Indiana (ICDPA) | 1 January 2026 | 100k; or 25k and over 50%† |
| Kentucky (KCDPA) | 1 January 2026 | 100k; or 25k and over 50%† |
| Rhode Island (RIDTPPA) | 1 January 2026 | 35k; or 10k and over 20%† |
| Oklahoma (SB 546) | 1 January 2027 | 100k; or 25k and over 50% (SECONDARY, Hunton) |
| Louisiana (SB 386) | 1 January 2027 | Over $25M revenue, or 75k, or 50% revenue from sales (SECONDARY, Troutman) |
| Alabama (HB 351) | 1 May 2027 | Over 25k, or over 25% revenue from sales; under 500 employees exempt unless selling; **no assessments, no appeal** (SECONDARY, Hunton) |
| Vermont (S.71) | 1 January 2028 | 35k; or 3k sensitive-data subjects; health provisions with no threshold (SECONDARY, Mayer Brown) |

Florida's narrow law (very large controllers) is counted by some firms
as a 24th; it is unlikely to reach a consultancy's clients.

**(b) Triggers.** The client meets a state's threshold for that state's
residents' data, counted as *consumers*: every law except California's
excludes people acting in an employment or B2B context. Then:

- **Profiling opt-out.** Every law except Utah's (and arguably Iowa's)
  lets consumers opt out of "profiling in furtherance of decisions that
  produce legal or similarly significant effects": financial or lending,
  housing, insurance, education, criminal justice, employment, health
  care, essential goods. Minnesota (325M.14 subd. 1(g), PRIMARY) adds a
  right to question the result, learn the reason, review the data and
  have the decision re-evaluated; Connecticut from 1 July 2026 and
  Vermont from 2028 are similar (SECONDARY).
- **Data protection assessment.** Every law except Utah, Iowa and Alabama
  requires one before targeted advertising, sale, sensitive-data
  processing, or profiling with a foreseeable risk of unfair or deceptive
  treatment, disparate impact, financial, physical or reputational
  injury, or intrusion on seclusion. Produced to the Attorney General on
  demand, confidential, no privilege waiver; one assessment can cover
  comparable operations and assessments made for other laws count.
  Connecticut adds an impact assessment for significant-effect profiling
  (activities from 1 August 2026, SECONDARY). Colorado's rules (4 CCR
  904-3, Rules 8.04 and 9.06; not verified at the source) list the
  contents, including the level of human involvement ("solely
  automated", "human reviewed", "human involved"), accuracy and
  disparate-impact testing.
- **Sensitive data.** Opt-in consent everywhere except California (right
  to limit) and Utah and Iowa (notice and opt-out). Maryland limits
  sensitive-data processing to what is strictly necessary for a
  requested service and bans its sale (wording not verified).
  Connecticut now asks whether personal data trains large language
  models in the privacy notice (SECONDARY).
- **Processor terms.** A written contract with instructions, purpose,
  data types, duration, confidentiality, deletion or return, flow-down to
  sub-processors, audits, and **assistance with the controller's
  assessments** (statutory pattern; Oklahoma confirmed, SECONDARY).

**(c) Paperwork.**

- DPA used as the data protection assessment: add a US screening table
  (sale, targeted ads, sensitive data, significant-effect profiling, per
  state); replace "legal basis" with notice, consent (sensitive data) and
  opt-out facts; add the level of human involvement in Colorado's terms;
  add disparate-impact testing (an M record) and the benefit-risk weighing
  with safeguards.
- Consumer notice pack: privacy-notice text on profiling, the opt-out
  route and appeal; Minnesota's question-the-result path.
- Records: there is no Article 30 register in US law, but Minnesota
  requires a data inventory and named privacy lead (325M.18, PRIMARY);
  the processing-records rows serve it.
- Questionnaire: processor-contract terms and assessment assistance; the
  Google Cloud flow-down.

**(d) Counsel.** Which states' thresholds does the client meet? Is the
decision "legal or similarly significant"? Is free-text chat collecting
sensitive data, and does consent cover it? Does Maryland's strict
necessity test hold? Can one assessment serve California's §7152 and the
other states?

## 5. Biometric laws

**(a) Status.** Illinois BIPA (740 ILCS 14): written policy, notice and a
written release before collection, consent before disclosure, private
right of action at $1,000 or $5,000 per violation. The 2 August 2024
amendment (SB 2979) makes repeated collection one violation per person
and allows electronic signatures; the Seventh Circuit held it
retroactive on 1 April 2026 (*Clay v. Union Pacific*, SECONDARY,
<https://datamatters.sidley.com/2026/04/08/seventh-circuit-limits-potential-damages-under-bipa-holds-2024-amendment-applies-retroactively/>).
ilga.gov was unreachable: BIPA text not verified at a primary source.
Texas CUBI as amended by TRAIGA (1 January 2026, PRIMARY): consent before
capture; AI training exempt unless the system identifies individuals.
Washington RCW 19.375 (PRIMARY): notice and consent or opt-out before
enrolment. Colorado HB 24-1130 (C.R.S. 6-1-1314, in force 1 July 2025,
PRIMARY): public biometric policy with retention and incident response,
consent, limits on employers. Washington My Health My Data Act (RCW
19.373, in force 31 March 2024, PRIMARY): consumer health data includes
voice and face biometrics and health inferences; separate consent to
collect and to share, signed authorisation to sell, homepage policy, no
threshold; employment context excluded.
**(b) Triggers.** Voiceprints (speaker verification in a voice agent),
face geometry, keystroke or gait; health inferences from chat for
Washington consumers. Biometric laws reach employees (Illinois, Colorado,
Texas, Washington RCW 19.375).
**(c) Paperwork.** DPA: biometric data flow, written release or consent
records, retention schedule and destruction; records: retention policy;
card: notice text; IA: Rite Aid-style accuracy and bias testing.
**(d) Counsel.** Is a voice feature a "voiceprint"? Has every Illinois
data subject signed a release? Is chat content "consumer health data"
under Washington law?

## 6. Standards: NIST, ISO/IEC 42001 and where the law rewards them

**(a) Status.**

- **NIST AI RMF 1.0** (NIST AI 100-1, 26 January 2023) is still current.
  NIST says it "is being revised as part of the White House AI Action
  Plan"; no draft has been published (PRIMARY, coordinator). The Action
  Plan asks NIST to remove references to misinformation, DEI and climate
  change. A concept note for an AI RMF Profile on Trustworthy AI in
  Critical Infrastructure was released on 7 April 2026.
- **NIST AI 600-1**, Generative AI Profile (26 July 2024), is current.
- **Cyber AI Profile** (NIST IR 8596), initial preliminary draft 16
  December 2025, built on CSF 2.0; no public draft yet (PRIMARY).
- **SP 800-53 control overlays** (COSAiS, renamed COSIS on 20 October
  2026) plan single-agent and multi-agent use cases; outlines only
  (PRIMARY).
- **AI Agent Standards Initiative** (February 2026): an RFI on agent
  security and an NCCoE concept paper on software and AI agent identity
  and authorisation (PRIMARY). The closest federal work to ADK agents.
- **Zero Drafts**: July 2026 public draft *Guidance and Templates for
  Public-Facing AI Documentation* (PRIMARY), a likely future reference
  for the system card.
- CAISI's page is now titled "Center for Advancing Innovation and
  Standards for Super Intelligence (CAISSI)" under EO 14434.

**Where state law rewards a framework (checked 2026-10-26):**

| Law | Framework | Effect |
| --- | --- | --- |
| Texas TRAIGA §552.105(e)(2)(D) | "Most recent version" of NIST AI RMF Generative AI Profile, or another recognised framework | No liability for a violation found through internal review while substantially complying (PRIMARY) |
| Texas TRAIGA §552.105(c) | none named | Rebuttable presumption of reasonable care |
| Colorado SB 24-205 §§6-1-1703, 6-1-1706(3) | NIST AI RMF, ISO/IEC 42001 | **Repealed** by SB 26-189; no successor defence (SECONDARY, NatLawReview, <https://natlawreview.com/article/colorados-sb-26-189-understanding-new-automated-decision-making-technology-law>) |
| Tennessee TIPA §47-18-3213 | NIST Privacy Framework (not the AI RMF) | Affirmative defence for a conforming written privacy programme (from memory; not verified) |
| California FEHA ADS rules §11009(f); Connecticut PA 26-15 | anti-bias testing (no framework) | Evidence for or against a claim, not a defence |
| NAIC model bulletin | NIST AI RMF | Acceptable basis for an insurer's AI programme; guidance |
| CPPA regulations | none | No NIST or ISO reference found in the text |

**(b) Triggers.** Texas residents served (TRAIGA reach is wide);
Tennessee consumers above its threshold; insurer clients.
**(c) Paperwork.** IA: keep the NIST mapping and add the GenAI Profile
action IDs actually performed, with the red-team results, so the Texas
defence has evidence. Cite AI 600-1 as "the most recent version" with its
date. Questionnaire: note the agent-security work (IR 8596, COSIS) as
watch items, not as controls claimed.
**(d) Counsel.** Does the client's practice amount to "substantial
compliance"? Is ISO/IEC 42001 certification worth it for US clients now
that no surviving statute names it?

## Must cover, should cover, mention only

**Must cover** (most US agent projects meet at least one):

1. California CPPA risk assessment and ADMT rules (any client that is a
   CCPA "business" with Californian consumers or staff).
2. State privacy laws' data protection assessments, profiling opt-out and
   sensitive-data consent (consumer data across nineteen states in force, twenty-three signed).
3. Employment AI rules: NYC Local Law 144, Illinois HB 3773, California
   FEHA ADS regulations, Title VII and ADA adverse impact and
   accommodation.
4. Colorado SB 26-189 (consequential decisions from 1 January 2027).
5. Chatbot disclosure: Utah, Maine, California bot law and AB 1609; the
   companion-chatbot exclusion test.
6. FTC Section 5 substantiation of claims about the agent.
7. Federal preemption status line.

**Should cover** (when the trigger is present):

8. HIPAA business associate chain and Section 1557 §92.210.
9. ECOA Regulation B principal reasons; FCRA adverse action and CRA risk.
10. GLBA vendor terms and Safeguards breach notice.
11. Texas TRAIGA (intent prohibitions, investigative demand, NIST safe
    harbour).
12. Biometric laws (BIPA and others) when voice or face features exist.
13. COPPA when children may use the service.
14. California SB 947, Connecticut PA 26-15 employment notices, Colorado
    HB 26-1263 and the 2026 companion-chatbot family.
15. TCPA for outbound voice.

**Mention only**: EO 14179, the AI Action Plan, OMB memos, SB 53, the New
York RAISE Act, Illinois SB 315, the FRONTIER Act and other pending
bills, AB 2013 (unless fine-tuning for public use), SB 942 (unless the
agent generates media), the TAKE IT DOWN Act (unless hosting user
content), the NAIC bulletin (insurers), EO 14434's "SI" terminology.

## Screening checklist

Each row is a fact the discovery brief or design can answer, the law it
brings in, and where the draft records it. "Memo" means the US regime
screen section (or `us-applicability-memo.md`); "notice pack" and "bias
audit pack" are the proposed new documents.

| Trigger (fact with an ID) | Law | Document section |
| --- | --- | --- |
| Any US client or US residents served | Federal preemption status; FTC Section 5 | Memo: preemption line; card: Limits back every public claim |
| Client meets CCPA "business" test and has Californian consumers **or staff** | CPPA regulations | DPA: §7150 screening and §7152 content; records: five-year retention |
| Output replaces or substantially replaces a human in a financial, housing, education, employment or healthcare decision about a Californian | CPPA ADMT (1 January 2027) | Notice pack: pre-use notice, opt-out or appeal, access; card: human involvement test |
| Automated inference about employees or applicants from systematic observation | CPPA risk assessment §7150(b)(4) | DPA |
| Client meets a state privacy threshold for that state's consumers | State privacy laws (table §4) | DPA as data protection assessment; questionnaire: processor terms |
| Profiling feeds a decision with legal or similarly significant effect | Profiling opt-out; Minnesota question right; Connecticut impact assessment | Notice pack: opt-out and appeal; DPA: human involvement level |
| Sensitive data (health, biometrics, race, religion, sexuality, precise location, children's, neural, financial in Connecticut), including in free-text chat | State opt-in consent; Maryland strict necessity; CPPA | DPA: consent and masking evidence |
| Output "materially influences" a consequential decision about a Colorado consumer | Colorado SB 26-189 (1 January 2027; enforcement stayed) | Notice pack: pre-use notice, 30-day adverse explanation; card: developer documentation; records: three years |
| Use on job applicants or employees in hiring or promotion in NYC | NYC Local Law 144 | Bias audit pack; notice pack: 10 business days |
| Use on Illinois employees or applicants | Illinois HB 3773; AI Video Interview Act | IA: discriminatory-effect and proxy analysis; notice pack |
| Use on California applicants or employees | FEHA ADS regulations; SB 947 for discipline and termination (1 July 2027) | IA: anti-bias testing; records: four years; notice pack: post-use notice |
| Use on Connecticut employees or applicants | Connecticut PA 26-15 (1 October 2027) | Notice pack: pre-decision notice |
| Any employment use anywhere in the US | Title VII disparate impact; ADA accommodation | IA: adverse-impact analysis; card: accommodation route |
| Consumer-facing chatbot | Utah (on request), Maine, California bot law (sales) | Card: disclosure behaviour; design contract for "are you human?" |
| Consumer customer-service agent for a business over $500 million serving Californians | California AB 1609 (1 January 2027) | Card: disclosure and 15-minute human hand-off; M record for hand-off time |
| Persona, memory of the user, or relationship features | Companion-chatbot laws (CA SB 243 and SB 1119, NY, WA, CT, CO HB 26-1263, others) | Card: disclosure cadence, self-harm protocol, minor protections; memo: exclusion analysis |
| Users may be under 13, or minors likely | COPPA; companion laws' minor duties | DPA: parental consent, retention policy |
| Agent touches PHI for a covered entity or business associate | HIPAA | DPA: BAA chain; questionnaire: Security Rule risk analysis |
| Client receives HHS funding and agent supports care decisions | Section 1557 §92.210 | IA: input-variable inventory and mitigation |
| California health facility sends AI-written patient messages | AB 3030; AB 489; AB 1979 and SB 503 (1 January 2027) | Card: disclaimer and human route |
| Agent scores or recommends in a credit decision | ECOA Regulation B | IA and card: principal reasons per decision |
| Agent compiles third-party data about people for eligibility decisions | FCRA | Memo: consumer reporting agency risk; notice pack: adverse action |
| Client is a financial institution | GLBA Privacy and Safeguards Rules | Questionnaire: vendor safeguards, 30-day breach notice support |
| Client is an insurer | NAIC bulletin; state insurance rules | IA: AI programme; questionnaire: audit cooperation |
| Voiceprint, face geometry or other biometric | BIPA, CUBI, RCW 19.375, Colorado 6-1-1314; FTC Rite Aid | DPA: release, retention, destruction; IA: accuracy and bias tests |
| Health inferences about Washington consumers | My Health My Data Act | DPA: separate consents; homepage policy |
| Outbound calls or voicemails | TCPA | Card: caller ID and opt-out; records: consent |
| Texas residents served | TRAIGA | IA: NIST GenAI Profile mapping and red-team results (safe harbour); card: answers to a civil investigative demand |
| Generates images, video or audio for the California public | SB 942 as amended by SB 1000 | Card: latent disclosure and provenance |
| Project fine-tunes a generative model offered to the public in California | AB 2013 | Card: training-data summary |
| Hosts user-generated images or video | TAKE IT DOWN Act | Card: notice-and-removal process |
| Federal agency client or subcontract | OMB M-25-21, M-25-22, M-26-04 | Card and questionnaire: model, system and data cards; acceptable use |

## What to change in the current skill

1. **SKILL.md description and "Size the pack".** The description and the
   first drafting step assume the EU AI Act. Add a jurisdiction step
   before drafting: list where the client is established and whose
   residents and staff the system serves (a fact with an ID), then pick
   the screens. For the US, the classification memo becomes a regime
   screen; size it like the EU memo (always written when any other
   document is).
2. **New reference `references/us-law.md`** with the screening checklist
   above, the dates table and the counsel questions. Keep the state
   privacy table there, with its † thresholds marked as needing a check.
   It needs a shorter re-check interval than the EU file (the checker's
   180-day warning is too long for Colorado, the companion-chatbot laws
   and federal preemption; 90 days is safer for US rows).
3. **Classification memo template.** Make the EU sections conditional
   and add a US section set: Federal preemption status; Consequential or
   significant decisions (CPPA ADMT, Colorado SB 26-189, state profiling
   opt-outs); Employment AI rules; Chatbot and companion disclosure;
   Sector statutes (HIPAA, GLBA, FCRA, ECOA, TCPA); Not applicable (SB
   53, RAISE, AB 2013 unless fine-tuning), each with `checked` dates.
4. **DPIA input pack template.** Add a US screening table alongside
   WP248 (sale, targeted ads, sensitive data, significant-effect
   profiling, CPPA §7150(b) triggers), replace "Legal basis" with
   "Notice, consent and opt-out" for US-only packs, and add the CPPA
   §7152 fields the GDPR pack lacks: approximate number of consumers,
   **whether the business will proceed**, contributors, and the
   **approver's name, position and approval date**. Add the level of
   human involvement in Colorado's and CPPA's terms (the CPPA three-part
   human-involvement test decides whether the system is ADMT at all).
5. **Processing-records template.** Add a retention-of-governance-records
   column: CPPA assessments five years, FEHA ADS data four years,
   Colorado SB 26-189 records three years. Note that US law has no
   Article 30 register but Minnesota requires a data inventory.
6. **System card reference.** Add chatbot disclosure behaviour (when it
   says it is an AI, how it answers "are you human?", cadence for
   companion features), the human hand-off path and its measured time
   (AB 1609), and a "public claims" check: every capability claim the
   client will market cites an M record (FTC Section 5).
7. **Impact assessment reference.** Its NIST mapping is right and now
   has legal weight in Texas: ask for the AI 600-1 action IDs actually
   performed and the red-team results, and cite AI 600-1 as "the most
   recent version" with its date. Add an adverse-impact section for
   employment and credit uses (selection rates by group, four-fifths
   ratio, statistical test, less-discriminatory alternatives, proxies
   removed) because NYC, Illinois, California FEHA, Connecticut and
   Title VII all turn on it. Note that NIST documents may now say "SI"
   (EO 14434) and the framework may be revised.
8. **New templates** (proposed): `consumer-notice-pack.md` (pre-use
   ADMT notice, adverse-outcome explanation within 30 days, opt-out or
   human appeal, access response, chatbot disclosure text) and
   `bias-audit-input-pack.md` (NYC Local Law 144 fields: data source,
   counts, selection or scoring rates and impact ratios by sex,
   race/ethnicity and intersections, auditor independence; FEHA testing
   quality, recency, scope, results and response).
9. **Checker.** Add a US trigger list parallel to `ANNEX_III` that forces
   `counsel_required: yes`: hiring, promotion, termination, credit,
   housing, insurance, health care decisions, biometrics, voiceprint,
   children, PHI. Most already overlap the Annex III phrases; add
   *tenant screening*, *adverse action*, *voiceprint*, *PHI*,
   *companion*. Accept "January 1, 2027" (already matched by
   `LEGAL_DATE`) so US-style dates pass.
10. **Roles.** The EU provider/deployer split maps poorly. Add the US
    roles: CCPA business and service provider or contractor, state
    privacy controller and processor, Colorado developer and deployer,
    FEHA "agent" of the employer, HIPAA business associate. The
    consultancy's exposure as the employer's agent (FEHA, *Mobley*) and
    as a CPPA service provider who must cooperate with assessments
    belongs in the memo.
11. **Dated facts in references.** `privacy-and-records.md` mentions only
    GDPR for automated decisions; add a pointer to the US reference for
    CPPA ADMT and state profiling rights.

## Not verified at a primary source

- California statute text for SB 947, SB 1000, AB 853, AB 2713, SB 1119,
  AB 1609 thresholds and penalties, AB 1979, SB 503, AB 2013, AB 3030,
  AB 489 and B&P §§17940–17943 (leginfo blocked); chapter numbers;
  operative dates of SB 947 and SB 1119 (1 July 2027).
- Colorado SB 26-189 enacted text (over 10 MB); the list of duties it
  dropped rests on the bill page, fiscal note and law-firm summaries.
  Colorado's privacy rules 4 CCR 904-3 rule numbers.
- Illinois statutes (BIPA, HB 3773, Video Interview Act, HB 1806).
- Maine LD 1727; the 2026 chatbot laws of Washington, Oregon, Idaho,
  Nebraska, Iowa, Georgia and Hawaii; Virginia 2026; New Jersey guidance.
- Thresholds marked † in the privacy table; Maryland MODPA wording;
  Connecticut PA 25-113 text and a possible 2026 SB 4.
- Tennessee's NIST Privacy Framework defence; Montana SB 212.
- HHS guidance (cloud, OCR AI letter), DOL AI principles, Unified Agenda
  dates, the Uniform Guidelines rescission at OIRA, CFPB leadership.
- The Commerce "onerous laws" list and BEAD notice (not found; absence
  cannot be proved).
- The Action Plan's exact wording (PDF not extractable).
- Connecticut PA 26-15 employment notice date: the OLR summary (PRIMARY)
  says 1 October 2027; FPF (SECONDARY) says 1 October 2026. This note
  uses the OLR date.
