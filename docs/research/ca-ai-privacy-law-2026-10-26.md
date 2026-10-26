# Canada: privacy and AI law for the governance pack

*Read 26 October 2026. Research for adding Canada to
`skills/adk-governance-pack` at screen depth. Drafts, not legal advice.*

## Conclusion

Canada has no AI Act and no AI bill. The Artificial Intelligence and Data
Act died with Bill C-27 in January 2025. The successor privacy bill, Bill
C-36 (Protecting Privacy and Consumer Data Act), was introduced on 15 June
2026 and has had only a first reading. It contains no AI statute. A
Canadian memo is therefore a **regime screen**, like the Australian one.
The facts that drive it differ from Australia's: which province the
people and the client are in, whether the client is federally regulated,
and whether any data leaves Quebec or Canada.

What changes the pack:

1. **Two layers of privacy law, chosen flow by flow.** PIPEDA covers
   commercial activity across Canada and every cross-border flow. Quebec,
   Alberta and BC have their own private sector laws for flows inside
   those provinces. PIPEDA reaches employees only at federal works (banks,
   airlines, telecoms). Outside Quebec, Alberta and BC, a provincially
   regulated employer's staff data has no general private sector privacy
   statute.
2. **Quebec is the strictest regime and is in force.** Under Law 25:
   - every agent project for a Quebec enterprise needs a privacy impact
     assessment (s 3.3), and the CAI lists AI systems by name;
   - every flow out of Quebec needs a PIA and a written agreement before
     it starts (s 17). That covers the US, Australia and other provinces,
     including a Toronto region;
   - a decision "based exclusively on automated processing" needs notice,
     an explanation on request and a human reviewer (s 12.1), in force
     since 22 September 2023, checked 2026-10-26;
   - public-facing products default to the highest privacy settings
     (s 9.1);
   - administrative penalties reach the greater of $10 million or 2% of
     worldwide turnover (S).
3. **Cross-border processing runs on accountability, not adequacy.**
   PIPEDA treats a transfer for processing as a "use". It needs a contract
   giving "a comparable level of protection" and a notice that foreign
   authorities may access the data. Alberta also makes the organisation
   list the countries where service providers handle the data, and tell
   people who can answer their questions. No SCCs, no country list.
4. **Consent is the default basis.** Consent must be meaningful (s 6.1 and
   the OPC's guidelines). An overriding test says purposes must be ones "a
   reasonable person would consider ... appropriate" (s 5(3)). The memo
   never writes "lawful basis" or "legitimate interests" for Canada.
5. **Breach paperwork differs in each regime:**
   - PIPEDA: report and notify "as soon as feasible" on a real risk of
     significant harm, and keep a record of *every* breach for 24 months;
   - Quebec: notify the CAI on a risk of serious injury, and keep an
     incident register;
   - Alberta: notify the Commissioner "without unreasonable delay";
   - BC: no statutory duty.
6. **The OPC sets the AI standard through guidance and findings.**
   - The December 2023 generative AI principles (joint with the provinces)
     ask organisations for PIAs and AIAs, notice when generative AI is part
     of a decision, and an opportunity for human review.
   - The 2026 ChatGPT finding (6 May) and the Grok finding (11 June) make
     launch-time risk assessment the expectation.
   - The OPC's work on agentic AI is "ongoing", with no guidance yet.
7. **Government clients bring hard paperwork.**
   - Federal institutions run the Algorithmic Impact Assessment (levels I
     to IV) under the Directive on Automated Decision-Making, current
     version dated 24 June 2025 (S), and follow the generative AI guide.
     They list systems in the GC AI Register, launched 28 November 2025.
   - Ontario ministries follow the Responsible Use of AI Directive
     (1 December 2024).
   - The EDSTA's AI duties for the Ontario public sector still await
     regulations.
8. **Employment.**
   - Ontario: from January 1, 2026, checked 2026-10-26, employers with 25
     or more employees disclose AI used to "screen, assess or select
     applicants" in public job postings. Ontario employers of that size
     must also keep an electronic monitoring policy.
   - Human rights codes apply to any screening or ranking.

## Sources

"P" means read at the primary source on 26 October 2026. "S" means it came
from secondary reporting or search-result summaries only, and must be
re-read before anyone relies on it. Several primary sites refused automated
reads today: parl.ca (LEGISinfo and bill text), LégisQuébec, CanLII, the TBS
policy site, the CRTC FAQ and, late in the session, Justice Laws. Claims
resting on those sites are marked S.

### Federal privacy

| Source | Status | Used for |
| --- | --- | --- |
| PIPEDA, S.C. 2000, c. 5, current to 2026-09-30, pages 1, 3, 5, 7 (<https://laws-lois.justice.gc.ca/eng/acts/P-8.6/page-1.html>) | P | ss 4, 5(3), 6.1, 10.1–10.3, 26(2)(b), 28, 30; Schedule 1 principles |
| Breach of Security Safeguards Regulations, SOR/2018-64, current to 2026-09-30 (<https://laws-lois.justice.gc.ca/eng/regulations/SOR-2018-64/FullText.html>) | P | Report and notice contents; 24-month record |
| OPC, Guidelines for obtaining meaningful consent, modified 2025-08-11 (<https://www.priv.gc.ca/en/privacy-topics/collecting-personal-information/consent/gl_omc_201805/>) | P | Seven principles; four key elements; express consent cases |
| OPC, Guidelines for processing personal data across borders, 2009-01-27 (<https://www.priv.gc.ca/en/privacy-topics/airports-and-borders/gl_dab_090127/>) | P | Transfer is a use; contract; foreign-access notice |
| OPC and provincial commissioners, Principles for responsible, trustworthy and privacy-protective generative AI technologies, 7 December 2023, modified 2025-05-06 (<https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/gd_principles_ai/>) | P | Nine principles; deployer and developer duties; no-go zones |
| OPC statement on ChatGPT joint investigation, 6 May 2026 (<https://www.priv.gc.ca/en/opc-news/speeches-and-statements/2026/s-d_260506/>) | P | PIPEDA Findings #2026-002 |
| OPC news release on Grok, 11 June 2026 (<https://www.priv.gc.ca/en/opc-news/news-and-announcements/2026/nr-c_260611/>) | P | PIPEDA Findings #2026-004; launch-time assessment |
| OPC statement on Bill C-36, 15 June 2026 (<https://www.priv.gc.ca/en/opc-news/speeches-and-statements/2026/s-d_260615/>) | P | C-36 tabled; PIAs; Commission |
| OPC remarks to the OBA Privacy Law Summit, 8 October 2026 (<https://www.priv.gc.ca/en/opc-news/speeches-and-statements/2026/sp-d_20261008/>) | P | C-36 still a proposal; age assurance; children's code |
| OPC submission on ISED AI transparency, 23 September 2026 (<https://www.priv.gc.ca/en/opc-actions-and-decisions/submissions-to-consultations/sub_ised_20260923/>) | P | AI interaction notice; agentic AI work ongoing |
| ISED backgrounder on Bill C-36, 15 June 2026 (<https://www.canada.ca/en/innovation-science-economic-development/news/2026/06/government-of-canada-introduces-legislation-to-protect-canadians-privacy-in-the-digital-age.html>) | P | C-36 content; penalties; no AI statute |
| LEGISinfo C-36 (<https://www.parl.ca/legisinfo/en/bill/45-1/c-36>) and C-34 | S, refused (403); search summaries only | Stage: awaiting second reading |
| Gowling WLG, Understanding Bill C-36, 24 June 2026, and timeline (<https://gowlingwlg.com/en/insights-resources/articles/2026/understanding-bill-c36>) | S | C-36 section numbers |
| Norton Rose Fulbright on C-36, June 2026 (<https://www.nortonrosefulbright.com/en-ca/knowledge/publications/375addc0/bill-c-36-the-government-of-canadas-latest-attempt-at-private-sector-privacy-reform>) | S | ADS disclosure; de-identification; private right of action |
| ISED, Enhancing trust in AI through increased transparency (<https://ised-isde.canada.ca/site/ised/en/enhancing-trust-artificial-intelligence-through-increased-transparency>) | P (first 100,000 characters) | Five areas incl. AI agents; AI for All; bills C-34, C-36, C-8 |

### Quebec

| Source | Status | Used for |
| --- | --- | --- |
| CQLR c P-39.1 at LégisQuébec (<https://www.legisquebec.gouv.qc.ca/en/document/cs/P-39.1>) | S, refused (403 and 502); search summaries | Wording of ss 12.1, 14, 18.3, 90.12, 91, 93.1 |
| CAI, aide-mémoire *Vers la conformité à la Loi sur le privé*, 8 February 2023 (<https://www.cai.gouv.qc.ca/uploads/pdfs/CAI_GU_Responsabilites_Entreprises.pdf>) | P, read in full | Phased dates; ss 3.1, 3.2, 3.5–3.8, 8.1, 9.1, 12.1, 23, 27 obligations |
| CAI, *Réaliser une évaluation des facteurs relatifs à la vie privée*, v3.1, April 2024 (<https://www.cai.gouv.qc.ca/uploads/pdfs/CAI_GU_EFVP.pdf>) | P, sections 1 and 7 read | Five mandatory PIA situations; s 17 factors, adequate protection, written agreement; s 3.3 projects incl. AI systems |
| CAI release on the 2026 five-year report, 11 June 2026 (<https://www.cai.gouv.qc.ca/uploads/pdfs/CAI_Communique_RQ_2026.pdf>) | P | 74 recommendations incl. inferences, scraping, dark patterns |
| quebec.ca, Décision fondée exclusivement sur un traitement automatisé, updated 20 October 2025 (<https://www.quebec.ca/gouvernement/travailler-gouvernement/normes-gouvernance-pratiques-internes/protection-des-renseignements-personnels/technologie-et-droit-a-la-protection-des-renseignements-personnels/decision-traitement-automatise>) | P | Public sector twin (Access Act s 65.2); "contrôle important" test |
| CAI brief on AI at work; CAI generative AI principles; CAI ChatGPT report | S, search summaries | Recommendations; Quebec ChatGPT finding |
| Firm summaries of Quebec penalties (Clyde & Co, McCarthy) | S | 2% and 4% caps |

### Provinces

| Source | Status | Used for |
| --- | --- | --- |
| Alberta PIPA, SA 2003, c P-6.5, consolidation current as of 1 September 2025 (<https://kings-printer.alberta.ca/documents/Acts/P06P5.pdf>) | P | ss 6(2), 13.1, 34, 34.1, 59 |
| alberta.ca PIPA engagement, updated 3 March 2026 (<https://www.alberta.ca/personal-information-protection-act-engagement>) | P | No bill; committee review February 2025, 12 recommendations; survey 2–17 February 2026 |
| Alberta OIPC, PIPA Privacy Breach Process, April 2024 | S, search summary | Regulation s 19; s 37.1 |
| BC PIPA, SBC 2003, c 63, current to 20 October 2026 (<https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/03063_01>) | P | ss 1, 6, 8, 10, 13, 16, 19, 34, 35, 56; no breach or offshore provision |
| Ontario ESA guide, publicly advertised job postings, updated 24 February 2026 (<https://www.ontario.ca/document/your-guide-employment-standards-act-0/requirements-related-publicly-advertised-job>) | P | AI disclosure from January 1, 2026; exemptions; records |
| Ontario ESA guide, written policy on electronic monitoring, updated 8 July 2024 (<https://www.ontario.ca/document/your-guide-employment-standards-act-0/written-policy-electronic-monitoring-employees>) | P | 25-employee threshold; contents; deadlines |
| Ontario Responsible Use of AI Directive, updated 7 January 2026 (<https://www.ontario.ca/page/responsible-use-artificial-intelligence-directive>) | P | Ministries and agencies; disclosure; inventory |
| IPC Ontario, *AI Scribes: Key Considerations for the Health Sector*, January 2026 (<https://www.ipc.on.ca/en/media/6177/download>) | P, partly read | PHIPA roles; EDSTA AI provisions awaiting regulations |
| OHRC and LCO, Human Rights AI Impact Assessment release, 6 November 2024 (<https://www.ohrc.on.ca/en/news-center/AI-ohrc-and-lco-release-new-tool>) | P | HRIA structure and users |
| IPC and OHRC, Principles for the Responsible Use of AI (<https://www.ohrc.on.ca/en/principles-responsible-use-artificial-intelligence>) | P (content); S (21 January 2026 date) | Six principles; adverse-impact discrimination |
| Hicks Morley (March 2026), Lerners, Dentons on EDSTA and FIPPA | S | EDSTA commencement; no AI regulation; FIPPA 1 July 2025 |

### Federal government AI policy

| Source | Status | Used for |
| --- | --- | --- |
| TBS Directive on Automated Decision-Making (<https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32592>) | S, refused; search summaries | 24 June 2025 version; transition to 24 June 2026; Appendix C |
| TBS, 4th review overview and proposed modifications, Fall 2024 (<https://wiki.gccollab.ca/images/f/f1/Overview_4th_review_of_the_Directive_on_Automated_Decision-Making.pdf>) | P (proposals, not final text) | Proposed changes and unacceptable uses |
| canada.ca, Algorithmic Impact Assessment tool, modified 2026-09-15 (<https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html>) | P | 65 risk and 41 mitigation questions; levels I–IV bands; publication |
| canada.ca, Guide on the use of generative AI, modified 2026-09-24 (<https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/guide-use-generative-ai.html>) | P | FASTER; DADM applies; notify users |
| AI Strategy for the Federal Public Service 2025–2027, full text, page dated 2026-10-02 (<https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/gc-ai-strategy-full-text.html>) | P | Priorities; expectations; fourth review complete; register consultation |
| TBS release, first AI Register, 28 November 2025 (<https://www.canada.ca/en/treasury-board-secretariat/news/2025/11/canada-launches-first-register-of-ai-uses-in-federal-government.html>) | P | Register contents |

### Marketing, competition and context

| Source | Status | Used for |
| --- | --- | --- |
| ISED, CASL: getting consent to send email, modified 2019-04-01 (<https://ised-isde.canada.ca/site/canada-anti-spam-legislation/en/getting-consent-send-email>) | P | Consent durations; identification; 10 business days |
| CRTC CASL FAQ and guidance (<https://crtc.gc.ca/eng/com500/faq500.htm>) | S, refused; search summaries | Three requirements; onus of proof |
| CASL and Competition Act text at Justice Laws | S, unreachable (TLS errors) | Penalty caps |
| BLG, AI transparency: the Competition Bureau weighs in, 15 October 2026 (<https://www.blg.com/en/insights/2026/10/ai-transparency-the-competition-bureau-weighs-in>) | S | Bureau submission of 23 September 2026 |
| ISED releases on the voluntary code (December 2023, May 2024, November 2024) | S, search summaries | Signatory counts |
| Digital Policy Alert, BLG, Jurist on Bill C-8 | S | Royal Assent 15 June 2026 |

## 1. PIPEDA (federal private sector)

**(a) What and status.** The Personal Information Protection and Electronic
Documents Act, S.C. 2000, c. 5, Part 1, is in force. The Justice Laws
consolidation is "current to 2026-09-30"; the last amendment listed is
4 March 2025 (P, page read 2026-10-26). No AI-specific amendment has been
made. Bill C-36 would replace Part 1 (section 2), but it is at first
reading only.

**Who it binds (P, ss 4, 26(2)(b), 30).**

- Every organisation that collects, uses or discloses personal information
  "in the course of commercial activities" (s 4(1)(a)), across Canada,
  except where a province has a law declared substantially similar under
  s 26(2)(b) and the information stays within that province. Quebec, Alberta
  and British Columbia have general private sector laws declared
  substantially similar; Ontario, New Brunswick, Nova Scotia and
  Newfoundland and Labrador have health-information laws so declared
  (S, the exemption orders were not re-read today).
- **Employees: only federal works.** Part 1 reaches employee and job
  applicant information only "in connection with the operation of a federal
  work, undertaking or business" (s 4(1)(b)): banks, airlines, interprovincial
  transport, telecommunications, broadcasting. **A provincially regulated
  employer's staff data has no general private sector privacy statute
  outside Quebec, Alberta and BC.** That gap is a screening fact, not an
  invitation to ignore employee privacy: collective agreements, common law
  torts (intrusion upon seclusion in Ontario) and the Ontario electronic
  monitoring policy (section 6) still apply.
- Interprovincial and international flows. PIPEDA applies to personal
  information that crosses a provincial or national border in the course of
  commercial activity, even for organisations in Alberta, BC or Quebec
  (S, OPC summary of the substantially similar regime; not re-read today).
  An Australian consultancy that receives Canadian personal information in
  Sydney is a cross-border flow.

**The principles as they bite on an agent (Schedule 1, P).**

| Principle | Text (Schedule 1) | Agent facts to record |
| --- | --- | --- |
| 4.1 Accountability; 4.1.3 transfers for processing | The organisation "is responsible for personal information under its control", including information transferred to a third party for processing, and "shall use contractual or other means to provide a comparable level of protection" | Contract with Google Cloud and with the consultancy; sub-processors; where the consultancy's staff access data from |
| 4.1.4 Policies | Procedures to protect information, handle complaints, train staff, explain policies | Governance owners; the PIA itself |
| 4.2 Identifying purposes | Purposes identified at or before collection; a new purpose is identified before use | Every purpose in the client's words, including evaluation sets and re-use of existing data |
| 4.3 Consent; s 6.1 valid consent | "To make the consent meaningful, the purposes must be stated" (4.3.2); express consent generally where information is sensitive (4.3.6); consent "is only valid if it is reasonable to expect" the target audience to understand "the nature, purpose and consequences" (s 6.1) | Proposed notice and consent text; whether prompts are likely to carry health or financial information |
| s 5(3) Appropriate purposes | Purposes "a reasonable person would consider are appropriate in the circumstances" | The no-go-zone check (section 3) |
| 4.4 Limiting collection | "limited to that which is necessary for the purposes identified" | Data minimisation in prompts and tool results |
| 4.5 Limiting use, disclosure, retention | Minimum and maximum retention periods; destroy, erase or make anonymous when no longer needed (4.5.2, 4.5.3) | Session, memory, log and evaluation-set retention |
| 4.6 Accuracy | "as accurate, complete, and up-to-date as is necessary" | Evaluation results; output labelling; inferences written back to records |
| 4.7 Safeguards | Proportionate to sensitivity; physical, organisational, technological measures | SB and C IDs |
| 4.8 Openness | Policies and practices readily available, including the accountable person's name or title and address | Privacy policy inputs; the system card |
| 4.9 Access; 4.10 Challenging compliance | Access and an account of use and disclosure on request (4.9.1); complaints to the accountable person | Memory stores, session history and evaluation sets are information an access request reaches |

**Meaningful consent (OPC Guidelines for obtaining meaningful consent, page
modified 11 August 2025, P).** Seven principles: emphasise key elements;
let people control detail and timing; give clear yes or no options;
be innovative; take the consumer's perspective; make consent ongoing;
be accountable. The four key elements to put up front: what personal
information, with which parties, for what purposes, and the risk of harm.
Express consent is generally required where the information is sensitive,
the use is outside reasonable expectations, or it creates a "meaningful
residual risk of significant harm". A practice with a probable risk of
significant harm "would generally be considered inappropriate under
subsection 5(3)" and "should not be the subject of consent". For an agent:
a chat UI that collects free text needs a just-in-time notice naming the
model provider as a party and saying information may be processed outside
Canada.

**Cross-border processing (OPC Guidelines for processing personal data
across borders, 27 January 2009, P).**

- "A transfer for processing is a 'use' of the information; it is not a
  disclosure." No extra consent is needed if the information is used for
  its original purpose.
- Canada uses an "organization-to-organization approach that is not based
  on the concept of adequacy". No country list, no SCCs.
- The contract is "the primary means" of protection; the organisation
  should check the processor's policies, training and security and keep
  audit rights. "No contract can override the criminal, national security
  or any other laws of the country" of the recipient.
- **Notice is required:** tell individuals their information may be
  processed in a foreign jurisdiction and be accessible to its courts, law
  enforcement and national security authorities, "ideally ... at the time
  the information is collected".
- These guidelines date from 2009 and are still the OPC's published
  position. Bill C-36 would add a mandatory cross-border PIA (section 2).
  Quebec already requires one (section 4).

**Breach of security safeguards (P, ss 10.1 to 10.3; Breach of Security
Safeguards Regulations, SOR/2018-64, current to 2026-09-30).**

- Report to the Commissioner any breach "if it is reasonable in the
  circumstances to believe that the breach creates a real risk of
  significant harm" (s 10.1(1)), "as soon as feasible after the
  organization determines that the breach has occurred" (s 10.1(2)).
  Notify affected individuals on the same test and timing (s 10.1(3), (6)).
  No fixed hour count.
- "Significant harm" includes bodily harm, humiliation, damage to
  reputation or relationships, loss of employment, business or professional
  opportunities, financial loss, identity theft, negative effects on the
  credit record and damage to or loss of property (s 10.1(7)). Real-risk
  factors: sensitivity and probability of misuse (s 10.1(8)).
- Notify any other organisation or government institution that can reduce
  the risk (s 10.2).
- **Keep a record of every breach**, reportable or not (s 10.3(1)), for 24
  months after the day the breach is determined to have occurred (Regs s 6),
  and give it to the Commissioner on request (s 10.3(2)).
- Report contents (Regs s 2): circumstances and cause, timing, the
  information involved, number affected, steps to reduce harm, steps to
  notify, a contact. Notice contents (Regs s 3) and indirect notice by
  public communication where direct notice would cause harm or hardship
  (Regs s 5).
- **Offences.** Knowingly contravening s 10.1 or 10.3(1), or obstructing the
  Commissioner: up to $10,000 on summary conviction or $100,000 on
  indictment (s 28). PIPEDA has no administrative monetary penalties; the
  OPC cannot make orders. Enforcement is by complaint, findings, compliance
  agreements and Federal Court applications (S for the Federal Court route;
  not re-read today).

**(b) Triggers.** Canadian customers or users whose personal information
the agent handles in a commercial activity, outside Quebec, Alberta and BC
or crossing a border; any federal work (bank, airline, telecom) whose
employees or applicants are data subjects; personal information sent from
Canada to Australia or the US (model endpoint, log sink, consultancy access).

**(c) Paperwork.** Memo "Canada: PIPEDA and provincial privacy laws" with
the roles and the substantially-similar screen; input pack consent and
notice inputs (the four key elements), a Schedule 1 check, recipients and
regions with the cross-border notice wording; security questionnaire
"as soon as feasible" clock and 24-month breach record; transfer facts for
Canada live in the input pack (no annex mechanism, no SCC equivalent).

**(d) Counsel.** Is the client's handling a commercial activity, and which
of PIPEDA or a provincial law governs each flow? Is the consultancy acting
only for the client (a transfer for processing) or for its own purposes
too? Is implied consent enough for each purpose, or is express consent
needed? Does the cross-border notice need to name Australia and the US?

## 2. Federal reform: Bill C-27 died; Bill C-36 is at first reading

**(a) Status.**

- **Bill C-27** (Digital Charter Implementation Act, 2022: the Consumer
  Privacy Protection Act, the Personal Information and Data Protection
  Tribunal Act and the Artificial Intelligence and Data Act) died on the
  Order Paper when Parliament was prorogued on 6 January 2025 (S, Torys
  and Norton Rose Fulbright summaries; the prorogation date was not
  re-read at a primary source today).
- **No AI statute has been reintroduced.** ISED's Bill C-36 backgrounder
  describes no separate AI regime (P). ISED instead ran a consultation,
  *Enhancing trust in artificial intelligence through increased
  transparency*; the OPC's submission is dated 23 September 2026 and
  says the government is considering "whether and what action may be
  required" (P, OPC page). Nothing in it is law.
- **Bill C-36 (45th Parliament, 1st session)**, *An Act to enact the
  Protecting Privacy and Consumer Data Act, to amend the Personal
  Information Protection and Electronic Documents Act and to make
  amendments to other Acts*, was introduced and read a first time in the
  House of Commons on 15 June 2026 by the Minister of Artificial
  Intelligence and Digital Innovation, Evan Solomon (P: ISED backgrounder
  of 15 June 2026; OPC statement of 15 June 2026). Its stage on 26 October
  2026: awaiting second reading, with no second reading debate found (S:
  search summaries of LEGISinfo, Gowling's timeline current to 15 June
  2026, The Hub's September 2026 previews). **LEGISinfo and the bill text
  on parl.ca refused automated reads today; re-check the stage before
  relying on it.** The OPC's speech of 8 October 2026 still calls it a
  proposal (P).
- **Bill C-34** (Safe Social Media Act, enacting the Digital Safety Act and
  the Digital Safety Commission of Canada Act), first reading 10 June 2026,
  also awaiting second reading (S). Bill C-36 would rename the Commission
  the Digital Safety and Data Protection Commission of Canada and give it
  private sector privacy enforcement; the PPCDA's enforcement depends on
  C-34 passing (S, Gowling, 24 June 2026).

**What C-36 would do, if passed (P for the backgrounder items; section
numbers S, from Gowling's reading of the first-reading text).**

- Recognise privacy as a fundamental right; a documented privacy
  management program and designated accountable individuals (ss 8, 9).
- **Automated decision systems (s 63).** Transparency about automated
  decision systems "including those powered by AI" (P). On request, explain
  a prediction, recommendation or decision with a "legal or similarly
  significant effect": the personal information used, its source and the
  principal factors (s 63(4)-(5)), with a right to make representations to
  a person who can review it (s 63(6)) (S).
- **Cross-border PIA (s 57):** "assess and mitigate any privacy risks
  before sending personal information outside of Canada" (P); the
  assessment goes to the Commission on request (S).
- Legitimate-interest exception to consent, conditional on a documented
  PIA (s 18(3)-(5)) (S).
- De-identified information stays personal information; anonymised
  information is outside the Act (S, Norton Rose Fulbright).
- Children (under 18) treated as sensitive; best interests of the child
  (P for the higher standard; S for s 86).
- Service providers: appropriate safeguards and consideration of privacy
  implications when using them (P).
- Penalties: administrative monetary penalties up to the greater of $10
  million or 3% of global revenue; fines up to the greater of $25 million
  or 5% for the most serious offences (P); a private right of action (s
  132) (S).
- Coming into force: not stated in the backgrounder (P); left to order and
  regulations (S).

**(b) Trigger.** None today. Every Canadian pack carries one "mention
only" line.

**(c) Paperwork.** Memo, "Canada: Pending law": one line with `checked
2026-10-26`. Design choices that make a later move cheap: keep the
decision-explanation facts (personal information used, source, principal
factors) that s 63 and Quebec s 12.1 both want, and write the cross-border
risk facts now, since Quebec already requires them.

**(d) Counsel.** None until second reading; then whether the client's
program and contracts need changing before the coming-into-force order.

## 3. OPC AI guidance and findings

**Principles for responsible, trustworthy and privacy-protective
generative AI technologies** (7 December 2023; page modified 6 May 2025;
issued jointly by the OPC and the provincial and territorial commissioners,
including Quebec, Ontario, BC and Alberta) (P). Guidance, not binding, but
"many listed considerations may be required under applicable law".

- Nine principles: legal authority and consent; appropriate purposes
  (no-go zones); necessity and proportionality; openness; accountability
  (explainability); individual access (including information in outputs);
  limiting collection, use and disclosure; accuracy; safeguards (including
  prompt injection and model inversion).
- **For organisations using generative AI (the client and, in operation,
  the consultancy):** undertake "Privacy Impact Assessments (PIAs) and/or
  Algorithmic Impact Assessments (AIAs)"; "clearly communicate to any
  affected party whether a generative AI tool will be used as part of a
  decision-making process", with safeguards and recourse; "accountability
  for decisions rests with the organization, and not with any kind of
  automated system"; give people "the opportunity to request human review
  and/or re-consideration of the decision"; if outputs are not meaningfully
  explainable, consider whether the use is appropriate; monitor for and
  report biased outcomes to the provider.
- **For developers and providers (the consultancy as builder):** red-team
  for inappropriate uses; make outputs traceable or say they are not;
  document training data; independent auditing; PIAs and AIAs.
- **Anticipated no-go zones:** malicious deepfakes, including to bypass
  authentication; "conversational bots to deliberately nudge people into
  revealing sensitive personal information"; generating false or
  defamatory information about a person. Heightened attention for
  children and high-impact areas such as health care, employment and
  policing.

**2026 findings and guidance (P).**

- **ChatGPT joint investigation** (OPC with Quebec, BC and Alberta; OPC
  statement 6 May 2026; PIPEDA Findings #2026-002). Initial training
  collection was "overly broad"; concerns on consent, transparency,
  accuracy, access, correction and deletion, and accountability;
  well-founded and "conditionally resolved". The CAI found OpenAI did not
  fully meet the Quebec Act and made four recommendations (S, search
  summary of the CAI page and report).
- **Grok** (OPC release 11 June 2026; PIPEDA Findings #2026-004). X Corp.
  and xAI violated PIPEDA by launching image generation "without proper
  safeguards or sufficient consideration of potential privacy harms".
  Takeaway the OPC states: assess and address privacy risks "at the outset
  of any new initiative"; commitments included quarterly reports and
  independent audits.
- **Joint statement on AI-generated imagery** (February 2026, OPC news
  release 23 February 2026; 60 to 66 authorities, the OPC pages differ).
- **Age assurance guidance** (May 2026, two documents) and a forthcoming
  Children's Privacy Code (OPC speech, 8 October 2026).
- **AI transparency submission** (23 September 2026): people should be told
  when automated systems make significant decisions about them and when AI
  systems, including chatbots, collect or use their personal information;
  disclose accuracy limits, intended uses and training-data limits; the
  OPC's "work on agentic AI is ongoing". No OPC agentic AI guidance has
  been published (P, absence in the submission and the 8 October speech).

**(c) Paperwork.** Measure the input pack against the nine principles;
the system card states whether a generative AI tool is part of a decision,
the recourse and the human review route; the impact assessment names the
no-go-zone check; evaluation and red-team results are the evidence.

**(d) Counsel.** Does any use fall into a no-go zone or fail s 5(3)? Is the
human review offered real reconsideration?

## 4. Quebec: Act respecting the protection of personal information in the private sector (as amended by Law 25)

**(a) Status.** CQLR c P-39.1, amended by the Act to modernize legislative
provisions as regards the protection of personal information (S.Q. 2021,
c. 25, "Law 25"). Phased in force on 22 September 2022, 22 September 2023
and 22 September 2024 (portability) (P, CAI aide-mémoire of 8 February
2023). **LégisQuébec and CanLII refused automated reads today, so the
section wording below comes from CAI guidance (P) where the CAI states it,
and from search summaries of the consolidated text (S) otherwise.** No
2025 or 2026 Quebec bill amending the Act for AI was found (S, search
only). The CAI's five-year report, tabled 11 June 2026, recommends
regulating algorithmic inferences, scraping, data brokers and deceptive
interfaces (S, search summary of the CAI release); its 2025 brief on AI at
work recommends requiring disclosure to employees of partly or fully
automated decisions (S). Both are recommendations, not law.

**Who it binds.** Every "person carrying on an enterprise" that collects,
holds, uses or communicates personal information about others, including
employee information (S). Unlike PIPEDA, it covers the client's Quebec
employees and applicants.

**Obligations an agent engages.**

| Provision | What it requires | Agent facts |
| --- | --- | --- |
| s 3.1 Person in charge | The person with the highest authority is in charge of protecting personal information, may delegate in writing, and the title and contact details are published on the website (P, CAI aide-mémoire, in force 22 September 2022) | Named owner in the memo's Roles |
| s 3.2 Governance policies | Policies and practices governing personal information, with detailed information published in clear terms (P, CAI, from 22 September 2023) | Policy inputs from the inventory |
| s 3.3 PIA for systems projects | A privacy impact assessment (EFVP) for any project to acquire, develop or overhaul an information system or electronic service delivery system involving personal information; the CAI lists "système d'intelligence artificielle" as an information system (P, CAI EFVP guide v3.1, April 2024, s 7.2). Proportionate to sensitivity, purpose, quantity, distribution and medium (P, guide s 3.3). From 22 September 2023 | **An agent project for a Quebec enterprise is an s 3.3 project.** The input pack is the EFVP input |
| s 3.5 to 3.8 Confidentiality incidents | Reasonable measures to reduce the risk of injury; notify the CAI and the person if the incident presents a "risk of serious injury"; keep a register of incidents, given to the CAI on request (P, CAI aide-mémoire) | Questionnaire incident clocks and register |
| s 8 Notice at collection; s 8.1 identify, locate, profile | Inform the person before using technology that can identify, locate or profile them, and of the means to activate those functions (P, CAI aide-mémoire) | Profiling features off unless activated |
| s 9.1 Privacy by default | Products or services offered to the public with privacy parameters must, by default, provide "le plus haut niveau de confidentialité" (P, CAI aide-mémoire); cookies are excluded (S) | Memory, personalisation, history sharing and training opt-ins default off for public-facing agents |
| s 12.1 Automated decisions | See below | |
| s 17 Communication outside Quebec | See below | |
| s 23 Destruction or anonymisation | Destroy when the purpose is achieved, or anonymise for serious and legitimate purposes (P, CAI aide-mémoire) | Retention of sessions, logs and evaluation sets |
| s 27 Portability | Computerised personal information collected from the person in a structured, commonly used format, from 22 September 2024 (P, CAI aide-mémoire) | Memory and profile stores export path |

**s 12.1 decisions based exclusively on automated processing (in force 22
September 2023, checked 2026-10-26; S for the wording).** An enterprise that
uses personal information to render a decision based exclusively on
automated processing of it must inform the person "au plus tard au moment
où elle l'informe" of the decision; on request, tell the person the
personal information used, the reasons and principal factors and
parameters that led to the decision, and their right to have the personal
information corrected; and give the person the opportunity to submit
observations to a member of staff who is in a position to review the
decision (S, search summaries of the consolidated text and of the CAI
aide-mémoire item "informer une personne lorsqu'elle fait l'objet d'une
décision fondée exclusivement sur un traitement automatisé", which is P).
Failing to inform, or to allow observations, is listed among the
contraventions for which an administrative monetary penalty may be imposed
(S). Points for the draft:

- The trigger is narrower than Australia's APP 1.7 and close to GDPR
  Article 22: **"exclusivement"**. Meaningful human intervention takes a
  decision out; a person who only confirms the machine's output arguably
  does not (S, firm commentary; Quebec government guidance on the public
  sector twin, Access Act s 65.2, describes the concept as no meaningful
  human intervention, S from search summary).
- It is a transparency and review duty, not a right to object.
- There is no "significant effect" threshold in the text (S): any decision
  about a person, based exclusively on automated processing, is in.

**s 17 communication outside Quebec (in force 22 September 2023; P, CAI
EFVP guide s 7.1).**

- A PIA is required **before communicating** personal information outside
  Quebec **and before entrusting** a person or body outside Quebec with
  collecting, using, communicating or keeping it on the enterprise's
  behalf. Outside Quebec includes the rest of Canada.
- The assessment considers the sensitivity of the information, the purpose
  of its use, the protection measures including contractual ones, and the
  legal framework of the destination State, including its privacy
  principles.
- Communication may proceed only if the PIA shows the information "would
  receive adequate protection", in particular with regard to generally
  recognised privacy principles (the CAI lists accountability, purposes,
  limited collection, consent, privacy by design and default, limited use
  and retention, accuracy, security, transparency, rights and recourse).
  If not, the enterprise must refuse to communicate or entrust it.
- The communication is subject to a **written agreement** that takes the
  PIA's results into account and, where needed, terms that mitigate the
  risks it found (P, CAI guide s 7.1).
- For an agent: a Gemini endpoint or processing region outside Quebec
  (including us-central1, a global endpoint, or a Canadian region in
  Ontario such as northamerica-northeast2 Toronto, which is outside Quebec),
  log sinks, grounding services and consultancy access from Sydney each need
  the s 17 assessment. Montréal is northamerica-northeast1 (S, Google Cloud
  region naming not re-read today).

**Service providers (s 18.3, S).** Communication without consent to a
person for the performance of a mandate or service contract is allowed if
the contract is in writing and specifies protection measures, use only for
the mandate, destruction at the end, and prompt notice of incidents (S,
search summary; the CAI aide-mémoire confirms new rules for "exécution d'un
contrat de service", P).

**Consent (s 14, S).** Consent must be manifest, free, enlightened, given
for specific purposes, requested for each purpose in clear and simple
terms, and separately from other information when written (P for "un
consentement valide distinct pour chaque fin spécifique en termes simples
et clairs" in the CAI aide-mémoire). Express consent for sensitive
information (S).

**Penalties (S, firm summaries; section numbers not confirmed today).**
Administrative monetary penalties imposed by the CAI up to the greater of
$10 million or 2% of worldwide turnover (s 90.12); penal fines up to the
greater of $25 million or 4% (s 91, doubled for a repeat offence); a
private right of action with punitive damages of at least $1,000 for an
intentional or grossly negligent infringement (s 93.1).

**CAI guidance (P).** EFVP guide v3.1 (April 2024) and generic report
template; the business aide-mémoire (8 February 2023); the guide on
preventing confidentiality incidents; the biometrics guide (biometric
identity verification must be disclosed to the CAI in advance, P,
aide-mémoire, under the Act to establish a legal framework for
information technology); the CAI's principles for generative AI (S,
title only); the ChatGPT report (S).

**(b) Triggers.** The client carries on an enterprise in Quebec; Quebec
residents are users, customers, employees or applicants; personal
information collected in Quebec goes to any system, region or person
outside Quebec, including other provinces; any decision about a person
made exclusively by the agent; a public-facing product with privacy
settings; profiling, location or identification functions.

**(c) Paperwork.** Memo "Canada: Quebec" section: the person in charge,
the s 12.1 table (one row per decision: exclusive or not, the review route,
the explanation the design can produce); input pack as the s 3.3 EFVP input
and, separately, the s 17 assessment facts for each flow leaving Quebec
(sensitivity, purpose, contractual measures, destination law), plus the
written agreement reference; system card s 12.1 disclosure block and s 9.1
default settings; questionnaire: incident register and "risk of serious
injury" notification.

**(d) Counsel.** Is any decision "fondée exclusivement" on automated
processing? Does the s 17 assessment show adequate protection for
Australia and the US, and is the Google Cloud agreement the written
agreement? Does the EFVP need to be redone when the model or region
changes? Which entity is "the enterprise" for a group?

## 5. Alberta PIPA and BC PIPA (substantially similar provinces)

### 5.1 Alberta Personal Information Protection Act (SA 2003, c P-6.5)

**(a) Status.** Office consolidation "current as of September 1, 2025" (P,
King's Printer PDF read 2026-10-26). **No PIPA amendment bill has been
introduced** (P: alberta.ca engagement page, last updated 3 March 2026,
speaks only of "potential updates"). The Standing Committee on Resource
Stewardship completed its review in February 2025 with 12 recommendations
(P, same page). The public survey ran 2 to 17 February 2026 and "results
are under review"; engagement with the OIPC was open in spring 2026 (P).
A law firm puts the wider consultation window at 2 February to 1 May 2026
(S). Alberta's public sector laws were replaced by the Protection of
Privacy Act and the Access to Information Act (in force 11 June 2025, S);
these bind Alberta public bodies, not private clients.

**What bites on an agent (P, Act text).**

- **Service providers outside Canada.** Policies must include "the
  countries outside Canada in which the collection, use, disclosure or
  storage is occurring or may occur" and the purposes the provider is
  authorised for (s 6(2)), available in writing on request (s 6(3)). Before
  or at the time of collecting or transferring information to a service
  provider outside Canada, notify the individual how to get that written
  information and the name or title of a person who can answer questions
  (s 13.1(1)-(3)). **This is the only Canadian statute that makes the
  country list mandatory.** A Gemini endpoint in the US, logs in another
  region or consultancy access from Sydney each go on the list.
- **Security (s 34):** "reasonable security arrangements".
- **Breach notification (s 34.1):** notify the Commissioner "without
  unreasonable delay" of any incident involving loss of, or unauthorised
  access to or disclosure of, personal information "where a reasonable
  person would consider that there exists a real risk of significant harm".
  Contents are prescribed by the PIPA Regulation s 19; the Commissioner may
  require notice to individuals (s 37.1) (S for ss 19 and 37.1, from the
  OIPC's PIPA Privacy Breach Process, April 2024). Failing to notify is an
  offence (s 59(1)(e.1)).
- **Personal employee information (ss 15, 18, 21):** collection, use and
  disclosure without consent where reasonable for establishing, managing or
  terminating employment, with notice (P for the sections' existence; the
  notice wording was not re-read).
- **Offences (s 59(2)):** up to $10,000 for an individual and $100,000 for
  others. The Commissioner can make orders (S).

### 5.2 BC Personal Information Protection Act (SBC 2003, c 63)

**(a) Status.** "Current to October 20, 2026" (P, BC Laws). No amendment
found (S, search only).

- Consent required unless an exception applies (s 6); deemed consent where
  the purpose is obvious and the information is volunteered (s 8(1)); opt-out
  consent with notice and "a reasonable opportunity to decline" (s 8(3))
  (P).
- Notice of purposes before collection (s 10) (P).
- **Employee personal information** (defined in s 1): no consent needed if
  reasonable for establishing, managing or terminating the relationship,
  but **notice in advance** (ss 13(3), 16(3), 19(3)) (P).
- Security: "reasonable security arrangements" (s 34) (P).
- **Retention:** information used to make a decision that directly affects
  an individual must be kept "for at least one year after using it"
  (s 35(1)) (P). For an agent: a prompt, retrieved record or output that fed
  a decision about a BC individual is kept at least a year, which can
  collide with a short session-retention design.
- **No breach notification duty and no provision on storage or access
  outside Canada** in the Act (P). Breach duties then come from contract and
  PIPEDA for cross-border flows.
- Offences: up to $10,000 (individual) and $100,000 (others) (s 56(2)) (P).

**(b) Triggers.** Client carries on business in Alberta or BC; Alberta or BC
residents or employees are data subjects; Alberta information goes to a
service provider outside Canada.

**(c) Paperwork.** Memo: one row each in "Canada: privacy laws and roles";
input pack: Alberta s 6(2) country-and-purpose list and s 13.1 notice text;
BC s 35 one-year retention line in the retention table; questionnaire:
Alberta "without unreasonable delay" clock; BC "no statutory clock".

**(d) Counsel.** Which law governs each flow (PIPEDA, Alberta, BC)? Does
consultancy access from Sydney make the consultancy a "service provider
outside Canada"? Does the BC one-year rule reach model prompts and logs?

### 5.3 Health information (brief)

- **Ontario PHIPA.** A health information custodian is accountable for its
  agents; an "electronic service provider" that is not an agent has
  specific PHIPA requirements; vendors may also fall under PIPEDA (P, IPC
  *AI Scribes: Key Considerations for the Health Sector*, January 2026).
  The IPC expects AI governance committees, criteria for PIAs, security,
  breach notification and training, restricts secondary use such as vendor
  model training, and says consent "would generally be required" for AI
  scribes (P for structure; S for the consent quote and the OntarioMD
  vendor rule that PHI be stored and processed in Canada).
- **Other provinces.** Alberta Health Information Act, BC and Quebec health
  laws (Quebec's Act respecting health and social services information is
  named in the CAI's 11 June 2026 release, P) and the PHIPA-like laws in New
  Brunswick, Nova Scotia and Newfoundland and Labrador. **counsel:** which
  applies; this note does not cover their rules.

## 6. Employment

### 6.1 Ontario Employment Standards Act: AI in job postings

**(a) Status.** Added by the Working for Workers Four Act, 2024, and O. Reg.
476/24 (S for the amending Act's name and the regulation number; P that
the rules are in O. Reg. 476/24 per the ministry guide). **Applies to
publicly advertised job postings made on or after January 1, 2026**,
checked 2026-10-26 (P, ontario.ca *Requirements related to publicly
advertised job postings*, published 4 February 2026, updated 24 February
2026).

- "If an employer uses artificial intelligence to screen, assess or select
  applicants for a publicly advertised job posting, the employer must
  disclose the use of the artificial intelligence in the posting" (P),
  including where a third party such as a recruiter does the screening (P,
  search summary of the same page). A general statement is enough (P).
- **Artificial intelligence** means a machine-based system that infers from
  its inputs how to generate outputs such as predictions, content,
  recommendations or decisions (P, paraphrase of the guide's definition).
- Exempt: employers with fewer than 25 employees on the day of posting;
  internal postings; general help-wanted signs; work performed outside
  Ontario (P).
- Also from January 1, 2026: compensation or a range (range capped at
  $50,000; not where pay exceeds $200,000), whether a vacancy exists, no
  Canadian-experience requirement, and telling interviewed applicants within
  45 days of the last interview whether a decision was made (P).
- **Records:** copies of each posting and version for 3 years after it is
  removed; interview notices for 3 years (P).

**(b) Trigger.** The agent screens, scores, ranks, summarises or filters
applicants for an Ontario employer with 25 or more employees.

**(c) Paperwork.** Memo employment row; system card "AI disclosure" with
the posting wording; records: 3-year retention of postings. A summariser
that a recruiter reads before deciding may still "assess" applicants:
`counsel:`.

### 6.2 Ontario written policy on electronic monitoring

**(a) Status.** In the ESA since 11 April 2022; employers with 25 or more
employees in Ontario on January 1 of a year must have the policy before
March 1 of that year (P, ontario.ca ESA guide, updated 8 July 2024).
Contents: whether the employer electronically monitors employees; if so,
how and in what circumstances, and the purposes for which information may
be used; dates prepared and changed. Copies to employees within 30 days;
keep each policy 3 years after it ceases to apply. The rules "do not
establish a right for employees not to be electronically monitored" (P).

**(b) Trigger.** An internal agent logs staff prompts, telemetry, or usage
tied to named employees in Ontario.

**(c) Paperwork.** Memo employment row; input pack "consultancy and client
logging" flow; a calendar wait `W` for the policy update and the 30-day copy
window.

### 6.3 Human rights codes

- Every jurisdiction has a human rights statute (Ontario Human Rights Code;
  Canadian Human Rights Act for federal works; Quebec Charter of human
  rights and freedoms) prohibiting discrimination, including adverse-impact
  discrimination, in employment and services (S, not re-read today).
- **Ontario guidance (P).** OHRC and Law Commission of Ontario *Human Rights
  AI Impact Assessment* (6 November 2024): Part A assesses implications,
  Part B mitigation; for "AI designers, developers, operators, and owners";
  "does not constitute legal advice". IPC and OHRC *Principles for the
  Responsible Use of Artificial Intelligence* (21 January 2026, S for the
  date; P for content): valid and reliable, safe, privacy protective, human
  rights affirming, transparent, accountable; they will "ground our
  assessment"; a "seemingly neutral" uniform use "may actually result in
  adverse impact discrimination". Addressed to the Ontario public and
  broader public sector.
- **Quebec:** the CAI's brief on AI at work recommends requiring employers
  to disclose partly or fully automated decisions to employees (S; not
  law).

**(c) Paperwork.** Impact assessment "Adverse impact and equality" with the
HRIA questions as the checklist for Ontario; `counsel_required: yes` for
any screening or ranking of people.

**(d) Counsel (section 6).** Does a summariser "assess" applicants? Is prompt
logging electronic monitoring? Is adverse-impact testing adequate under the
Code? Which human rights statute applies (federal or provincial)?

## 7. Government clients

### 7.1 Federal: TBS Directive on Automated Decision-Making and the AIA

**(a) Status.** The Directive is a Treasury Board policy instrument binding
federal institutions (S for scope; the TBS page refused automated reads
today). Its current version is dated 24 June 2025; systems developed or
procured before that date have until 24 June 2026 to meet the new or
updated requirements, and agents of Parliament the same date (S: search
summaries of the TBS page). The fourth review is complete; the AI Strategy
progress update says it "increased transparency, improved alignment,
enhanced testing and monitoring" and "strengthened senior level
accountability" (P, AI Strategy full text, page dated 2 October 2026). The
Directive and AIA are reviewed every two years (P).

**What the fourth review proposed (P, TBS consultation deck, Fall 2024;
adoption of each item in the June 2025 text not confirmed today):**
assistant deputy minister approval of the AIA before publication and a
signed compliance summary to TBS before production; applying the Directive
to agents of Parliament; the OECD definition of an AI system; testing and
monitoring for human rights impacts; Appendix C changes to notice,
explanation (principal factors, how humans used the output) and ADM
approval at levels I and II; and a list of unacceptable uses (manipulation,
social scoring, biometric categorisation, untargeted facial scraping,
real-time remote biometric identification, emotion recognition, predictive
policing on profiling alone).

**The AIA (P, canada.ca AIA page, modified 15 September 2026).** "65 risk
questions and 41 mitigation questions"; impact levels by score: Level I
little to no impact (0 to 25%), Level II moderate (26 to 50%), Level III high
(51 to 75%), Level IV very high (76 to 100%). Complete at the start of
design and again before production; publish final results on the Open
Government Portal in both official languages.

**Appendix C by level (S, from the archived 2023 text and secondary
summaries; re-read before use):** peer review (none at I; at least one
expert at II and III; two at IV); plain-language notice (from II, and
published documentation at III and IV); human involvement (decisions at I
and II may be made without direct human involvement; III and IV need
specific human intervention points and a human makes the final decision);
explanation with any decision; training and contingency scaled by level;
approval to operate (deputy head at III; Treasury Board at IV).

**(b) Trigger.** Client is a federal department or agency, and the agent
makes or informs an administrative decision about a client (benefits,
permits, entry, hiring into the public service, investigations); the
Directive applies to generative AI used to "make or inform administrative
decisions" (P, generative AI guide).

**(c) Paperwork.** The department completes and publishes the AIA; the pack
supplies inputs in the impact assessment ("Canada: AIA inputs"), names the
level as `counsel:`/client decision, and lists the Appendix C requirements
as waits (peer review, approval). System card: notice and explanation text.
Bilingual publication is the department's.

**(d) Counsel and client.** Is the output an administrative decision or
input to one? Which impact level? Who approves? Does the department's PIA
under the Privacy Act and TBS Directive on Privacy Impact Assessment apply
(S; not re-read)?

### 7.2 Guide on the use of generative AI (federal)

Second version; page modified 24 September 2026 (P). FASTER principles:
fair, accountable, secure, transparent, educated, relevant. "Don't enter
sensitive or personal information into any tools not managed by the GC";
consult privacy officials on whether a PIA is needed; the Directive on ADM
applies when generative AI is used "to make or inform administrative
decisions"; "Notify users that they are interacting with generative AI";
GBA Plus bias testing before and after deployment; consult legal services,
privacy and security experts and the CIO, and bargaining agents before
high-risk deployments (P).

### 7.3 AI Strategy for the Federal Public Service 2025–2027 and the AI Register

- Strategy pages dated 25 February 2026 and full text 2 October 2026 (P);
  release reported as late June 2025 (S). Four priorities: central AI
  capacity (AI Centre of Expertise), policy and governance, talent and
  training, engagement and transparency. Expectations for every federal
  organisation include inventorying AI use cases with their impacts,
  approved tools with training, and reviewing compliance with the Directive
  on ADM; a commitment to standard contract language on vendor
  responsibilities for responsible AI (P).
- **GC AI Register** launched 28 November 2025 on the Open Government
  Portal: 42 institutions, over 400 systems; fields include purpose, use and
  whether built in house or by a vendor (P, TBS release). Consultation on its
  design ran January to March 2026 (P, strategy progress update).
- **Paperwork.** The system card's purpose, use and vendor facts are the
  register inputs; the memo names the register entry as the client's.

### 7.4 Ontario public sector

- **Strengthening Cyber Security and Building Trust in the Public Sector
  Act, 2024** (Bill 194) enacted the Enhancing Digital Security and Trust Act,
  2024 (EDSTA) and amended FIPPA (S: Royal Assent 25 November 2024; EDSTA in
  force 29 January 2025). **The EDSTA's AI provisions are "awaiting
  regulations to be established"** (P, IPC AI scribes guidance, January
  2026); no AI regulation found since (S, search to October 2026). The
  cybersecurity and minors' digital information regulations take effect 1
  July 2026 (S, Hicks Morley, March 2026). Write: AI duties for prescribed
  public sector entities exist in the Act but have no prescribed content;
  `checked 2026-10-26`.
- **FIPPA amendments (S):** from 1 July 2025, a PIA before collecting
  personal information, and reporting breaches with a real risk of
  significant harm to the IPC and to individuals, for FIPPA institutions
  (not municipal MFIPPA bodies).
- **Responsible Use of Artificial Intelligence Directive** (Management
  Board of Cabinet; effective 1 December 2024; page updated 7 January 2026)
  binds ministries and provincial agencies: a five-step risk management
  process, disclosure where the public interacts with an AI service or AI
  affects a decision about a person, a published AI use-case inventory, and
  "clear ongoing human oversight" (P).
- Quebec public bodies: Access Act s 65.2 mirrors s 12.1 for decisions
  "where no natural person exercised significant control" (P, quebec.ca,
  updated 20 October 2025); PIA for systems projects (s 63.5) and outside
  Quebec (s 70.1) (P, CAI guide).

**(d) Counsel.** Is the client a prescribed EDSTA entity or a FIPPA
institution? Does the Ontario Directive's disclosure reach the system?

## 8. CASL (outbound messaging agents)

**(a) Status.** Canada's Anti-Spam Legislation (S.C. 2010, c. 23) is in
force. Justice Laws did not answer today, so figures are from ISED (P) and
the CRTC and search summaries (S).

- Three requirements for a commercial electronic message: consent,
  identification, unsubscribe (S, CRTC FAQ). Identification: the business
  name, anyone on whose behalf it is sent, a mailing address and a phone,
  email or web contact valid for 60 days (P, ISED page modified 1 April
  2019). Unsubscribe actioned "within 10 business days or less" at no cost
  (P).
- Express consent does not expire; implied consent "may be valid for up to
  2 years", 6 months for inquiries or applications (P). The sender proves
  consent (S, CRTC guidance).
- Covers email and SMS (P); interactive voice calls are not CEMs and fall
  under the CRTC's telemarketing rules (S).
- Maximum administrative monetary penalties $1 million (individuals) and
  $10 million (others) per violation (S).

**(b) Trigger.** An agent sends commercial email, SMS or instant messages
to recipients in Canada, including follow-ups it drafts and sends itself.

**(c) Paperwork.** System card outbound channel (consent source, sender
identification, unsubscribe path); questionnaire; for voice: `counsel:` on
the National Do Not Call List and telemarketing rules.

## 9. Competition Act (deceptive marketing and AI claims)

- Technology-neutral; "no 'AI exception' to the law"; performance claims
  need "adequate and proper testing" before they are made; businesses should
  not assume a dynamically AI-generated representation falls outside the
  deceptive marketing rules; developers and deployers are accountable for
  outputs they control (S: Competition Bureau submission *Advancing
  artificial intelligence transparency*, 23 September 2026, as summarised by
  BLG, 15 October 2026).
- Penalties under s 74.1: for a corporation, up to the greater of $10
  million ($15 million for a repeat order) and three times the benefit, or
  3% of annual worldwide gross revenues if the benefit cannot be determined
  (S, search summary of the Justice Laws section; not read today).
- The ISED transparency paper's case study of a dealership chatbot that
  made, then withdrew, a buy-back offer without saying it was not human
  (P) is the scenario the system card's AI disclosure and capability claims
  guard against.

**(c) Paperwork.** System card capability claims cite M records; AI
disclosure in consumer channels; impact assessment consumer row.

## 10. Federal AI policy context (mention only)

- **No federal AI statute.** AIDA died with C-27; C-36 has no AI act (P,
  ISED backgrounder).
- **AI for All**, the national AI strategy, launched 4 June 2026 (P, ISED
  transparency paper; minister's release of June 2026, S).
- **ISED transparency consultation** (23 July to 23 September 2026, S for
  dates; P for content): five areas, including "AI agents: tracking the
  activity and permissions of agents that act on users' behalf"; government
  action on agents "remains an open question"; Canada "currently has no law
  requiring developers or deployers of generative AI to disclose
  AI-generated content" (P).
- **Voluntary Code of Conduct on the Responsible Development and
  Management of Advanced Generative AI Systems** (September 2023): voluntary
  measures on accountability, safety, fairness, transparency, human
  oversight and robustness; about 40 signatories by November 2024 (S;
  ISED release of November 2024 seen only in search). Context only; Google
  and the consultancy's signatory status is a fact to look up, not assume.
- **Bill C-8, Critical Cyber Systems Protection Act**: Royal Assent 15 June
  2026, S.C. 2026, c. 9; provisions in force by order, phased (S). Screen
  only for designated operators (banks, telecom, energy, transport).
- **Bill C-34** (Safe Social Media Act, chatbot rules) at second reading (S).

## Not verified at a primary source

Re-read these before a reference file relies on them.

- LEGISinfo stage of Bills C-36 and C-34 (parl.ca refused automated reads);
  C-36 section numbers (ss 8, 9, 18, 57, 63, 114, 132, 145).
- The prorogation date that ended C-27 (6 January 2025).
- The wording of Quebec ss 3.1, 9.1, 12.1, 14, 17, 18.3, 90.12, 91 and 93.1 at
  LégisQuébec (blocked; CAI guidance confirmed the substance of 3.1, 3.3,
  3.5 to 3.8, 8.1, 9.1, 12.1, 17, 23 and 27).
- The Directive on Automated Decision-Making text of 24 June 2025 and its
  Appendix C (the TBS site rejected automated reads).
- CASL and Competition Act text and penalties (Justice Laws stopped
  answering during the session).
- PIPEDA's application to interprovincial flows in substantially similar
  provinces; the exemption orders.
- The Ontario amending Act's name and O. Reg. 476/24 text (e-Laws renders
  by script).
- Bill 194 Royal Assent and EDSTA commencement dates; the FIPPA PIA and
  breach amendments of 1 July 2025.
- Alberta PIPA Regulation s 19 and s 37.1; Alberta public sector Acts'
  commencement.
- The CAI's generative AI principles and the CAI ChatGPT report.
- Human rights statutes' text; the federal Privacy Act and TBS Directive on
  PIA for federal clients.
- Google Cloud Canadian regions (northamerica-northeast1 Montréal,
  northamerica-northeast2 Toronto) and Gemini ML processing in Canada for
  the pinned model.

## Must cover, should cover, mention only

**Must cover.** Every Canadian pack screens for these.

1. PIPEDA (Schedule 1 principles, s 5(3), s 6.1 valid consent), with the
   federal-provincial screen: which law governs each flow.
2. Quebec Law 25 whenever any Quebec person or enterprise is involved: s 3.3
   PIA for the agent project, s 17 PIA and written agreement for every flow
   outside Quebec, s 12.1 for exclusively automated decisions, s 9.1 privacy
   by default, s 3.1 person in charge.
3. Cross-border processing: PIPEDA accountability by contract plus foreign
   processing notice; Alberta s 6(2) and s 13.1 country list and notice;
   Quebec s 17.
4. Breach clocks and records: PIPEDA "as soon as feasible" and the 24-month
   record of every breach; Quebec CAI notice and incident register; Alberta
   "without unreasonable delay"; BC none.
5. OPC generative AI principles (December 2023) and the 2026 ChatGPT and Grok
   findings as the standard the PIA is measured against.
6. Directive on Automated Decision-Making, AIA level and the generative AI
   guide, for federal clients.

**Should cover.** Screen when the trigger fires.

1. Alberta and BC PIPA (employee notice; BC one-year retention).
2. Ontario ESA AI job-posting disclosure (from January 1, 2026) and the
   electronic monitoring policy.
3. Human rights codes and the OHRC HRIA for agents that screen or rank
   people.
4. Ontario public sector: Responsible Use of AI Directive, FIPPA PIA and
   breach duties, EDSTA (awaiting regulations).
5. Health: PHIPA and the IPC AI scribes guidance; other health Acts as
   counsel questions.
6. CASL for outbound messaging.
7. Competition Act for consumer-facing claims.
8. GC AI Register inputs for federal clients.

**Mention only.** One line in the memo with `checked 2026-10-26`.

1. Bill C-36 (PPCDA), first reading 15 June 2026, not law.
2. Bill C-34 (Safe Social Media Act), not law.
3. No AI statute; AIDA died; AI for All (4 June 2026); ISED transparency
   consultation.
4. Voluntary code of conduct (2023).
5. Alberta PIPA review (no bill).
6. CAI five-year report recommendations (11 June 2026).
7. Bill C-8 (critical cyber systems), for designated operators.

## Screening checklist

| # | Trigger (fact with its ID) | Law | Document → section |
| --- | --- | --- | --- |
| 1 | Personal information of people in Canada in prompts, tools, memory, logs or evaluation sets, in a commercial activity | PIPEDA Schedule 1, s 5(3), s 6.1 | Memo → Canada: privacy laws and roles; input pack → Canada: consent and notice inputs |
| 2 | Client carries on an enterprise in Quebec, or Quebec residents, customers or employees are data subjects | Quebec P-39.1 (Law 25) | Memo → Canada: Quebec; input pack (s 3.3 PIA input); `counsel:` on which law governs |
| 3 | The agent project acquires, develops or overhauls a system that handles personal information of a Quebec enterprise | s 3.3 PIA | Input pack serves as the EFVP input; plan wait for the client's EFVP |
| 4 | Endpoint, model processing, logs, grounding, abuse review, support or consultancy access outside Quebec (including Ontario regions, the US, Australia) | s 17 PIA, adequate protection, written agreement | Input pack recipients; transfer annex structure reused for each flow; `counsel:` |
| 5 | Any personal information leaves Canada | PIPEDA 4.1.3 and the 2009 cross-border guidelines; Alberta ss 6(2), 13.1 | Input pack recipients and regions; notice text naming foreign access; Alberta country list |
| 6 | A decision about a person is made exclusively by the agent (no meaningful human intervention), for a Quebec enterprise | Quebec s 12.1 (in force 22 September 2023, checked 2026-10-26) | Memo s 12.1 table; system card disclosure (information used, principal factors, observations to a reviewer); `counsel_required: yes` |
| 7 | Public-facing product or service with privacy settings, for Quebec | s 9.1 privacy by default | System card defaults; input pack necessity |
| 8 | Profiling, location or identification functions | Quebec s 8.1 | Input pack notice; functions off by default |
| 9 | Alberta or BC client, residents or employees | Alberta PIPA; BC PIPA | Memo roles; employee notice; BC s 35 retention row |
| 10 | Client is a bank, airline, telecom or other federal work, and employees or applicants are data subjects | PIPEDA s 4(1)(b) | Memo roles; employee rows |
| 11 | Employees of a provincially regulated employer outside Quebec, Alberta and BC | No general private sector statute | Memo `n/a:` for statute with `counsel:` on torts, collective agreements |
| 12 | Agent screens, assesses or selects applicants for an Ontario employer with 25 or more employees | ESA job posting disclosure (from January 1, 2026, checked 2026-10-26); human rights code | System card AI disclosure; records 3 years; impact assessment adverse impact; `counsel_required: yes` |
| 13 | Agent logs or analyses Ontario staff activity (employer with 25 or more) | ESA electronic monitoring policy | Plan wait for the policy update; input pack logging flow |
| 14 | Agent screens, ranks or decides about people | Human rights codes; OHRC HRIA; OPC no-go zones | Impact assessment adverse impact; `counsel_required: yes` |
| 15 | Client is a federal department or agency; output makes or informs an administrative decision | Directive on Automated Decision-Making; AIA; generative AI guide; GC AI Register | Impact assessment → Canada: AIA inputs; system card notice and explanation; `counsel_required: yes` |
| 16 | Client is an Ontario ministry, provincial agency or FIPPA institution | Responsible Use of AI Directive; FIPPA PIA and breach; EDSTA (awaiting regulations) | Memo government row; impact assessment |
| 17 | Health information; client is a health information custodian | PHIPA and provincial health Acts | Memo sector row; input pack consent and secondary-use lines; `counsel_required: yes` |
| 18 | Outbound commercial email, SMS or instant messages to Canada | CASL | System card outbound channel |
| 19 | Consumer-facing agent or claims about the product | Competition Act ss 52 and 74.01 | System card claims and AI disclosure |
| 20 | Children likely to use it | OPC principles (children high risk); C-36 under-18 sensitivity (pending) | Input pack children; `counsel_required: yes` |
| 21 | Any personal information held | PIPEDA s 10.1 and 10.3 and SOR/2018-64; Quebec ss 3.5 to 3.8; Alberta s 34.1 | Questionnaire incident clocks and the 24-month breach record |

## Checker patterns

**Jurisdiction code.** Suggest `ca`, regex `\bCanad(?:a|ian)\b|\bQu[eé]bec\b`.
Do not match `\bCA\b`: US sections use "CA" for California (Cal. Civ. Code,
CA SB 7), which would put Canada in scope by accident.

**Law references a date check should recognise** (add to `LEGAL_REF`):

- `PIPEDA`, `PPCDA`, `Bill C-\d+` (C-36, C-34, C-27, C-8), `AIDA`. Avoid
  `CPPA` for Canada: it already means the California Privacy Protection
  Agency in the checker, and the Canadian CPPA is dead.
- `Law 25`, `Loi 25`, `P-39\.1`, `CQLR`, `Quebec (?:private sector )?Act`,
  `art\.` (already covered by `Art\.`), `s 12\.1` (covered by the `s \d+`
  pattern), `EFVP`.
- `PIPA`, `PHIPA`, `FIPPA`, `MFIPPA`, `EDSTA`, `ESA`, `O\. Reg\. \d+/\d+`,
  `SOR/\d{4}-\d+`, `S\.C\. \d{4}`, `SA \d{4}`, `SBC \d{4}`.
- `CASL`, `Competition Act`, `Human Rights Code`, `Directive on Automated
  Decision-Making`, `DADM`, `Algorithmic Impact Assessment`, `AIA`.
- Canadian statute titles carry a comma before the year ("Working for
  Workers Four Act, 2024"; "Enhancing Digital Security and Trust Act,
  2024"). The current `Act\s(?:19|20)\d\d` misses them; use
  `Act,?\s(?:19|20)\d\d`.

**Dates written in words to expect:** "22 September 2023" (Quebec ss 3.3,
12.1, 17), "22 September 2024" (portability), "January 1, 2026" (Ontario job
postings), "24 June 2025" and "24 June 2026" (DADM), "15 June 2026" (C-36
first reading), "1 July 2025" (FIPPA), "1 December 2024" (Ontario AI
Directive). Each needs `checked 2026-10-26`.

**Counsel trigger phrases to add** (most employment phrases are already
covered by "recruitment", "job applicants", "monitoring employees"):

- automated decisions: `based exclusively on automated processing`,
  `fondée exclusivement sur un traitement automatisé`, `exclusively
  automated decision`;
- public-body clients: `federal (?:department|institution|agency)`,
  `Government of Canada (?:department|institution)`, `administrative
  decisions?`, `Algorithmic Impact Assessment`, `impact level (?:III|IV|3|4)`,
  `Ontario ministr(?:y|ies)`, `provincial agenc(?:y|ies)`;
- employment: `screen, assess or select applicants`, `publicly advertised
  job posting`, `electronic monitoring`;
- health care: `personal health information`, `health information
  custodian`, `AI scribes?`;
- children: `under 18` is too broad as a bare phrase; prefer
  `children's personal information`.

The negation guard already handles "n/a: no Quebec persons".

## How Canada differs in ways that change a draft

**From Australia.**

- **Two layers, split by province and sector.** Australia has one federal
  Act; Canada has PIPEDA plus Quebec, Alberta and BC private sector laws,
  and provincial health laws. The memo needs a per-flow "which law" table,
  not one regime row.
- **No small business exemption and no employee records exemption.** PIPEDA
  has neither; instead employee data is covered only for federal works,
  Quebec, Alberta and BC. The Australian Roles analysis does not transfer.
- **Consent is the default basis.** Australia runs APP 3 and APP 6 without
  consent for most collection; PIPEDA and Quebec require meaningful
  consent, with s 5(3) as an overriding reasonable-person test (no
  Australian equivalent until tranche 2's fair and reasonable test).
- **Cross-border is closer to APP 8's "use" idea, but with notice.** The OPC
  treats transfer for processing as a use, like the OAIC's effective
  control, but requires telling people their data may be accessible to
  foreign authorities; Alberta requires the country list; Quebec requires a
  documented PIA and written agreement before any flow leaves Quebec,
  including to Toronto.
- **Automated decisions are narrower in Quebec.** APP 1.7 catches programs
  "substantially and directly related" to a decision even with human
  review; Quebec s 12.1 catches only decisions "based exclusively" on
  automated processing, but adds an individual explanation and review
  route, which APP 1.7 does not.
- **Breach: no 30-day assessment.** PIPEDA is "as soon as feasible" with a
  record of every breach for 24 months, including non-reportable ones.
- **Language.** Quebec-facing notices and documents may need French
  (Charter of the French Language, S); federal AIA results are published in
  both official languages (P).

**From the US.** Canada has a general private sector privacy law everywhere
(PIPEDA as the floor), so there is no revenue or volume threshold screen;
no state-style ADMT opt-out; no FTC-style Section 5 unfairness, but the
Competition Act's "adequate and proper test" for performance claims is
stricter than a reasonable-basis standard (S).

**From the EU.** No AI Act and no risk tiers; no lawful-basis menu; no
controller and processor terms in the statutes (PIPEDA speaks of the
organisation "responsible for personal information under its control" and
transfers "to a third party for processing"; Quebec speaks of mandates and
service contracts); no adequacy or SCCs: Canadian outbound transfers rest on
contract and accountability, and Quebec's s 17 PIA is the closest analogue
to a transfer impact assessment. Quebec penalties (2% and 4%) are
GDPR-scale; PIPEDA's are small fines only. Canada itself holds an EU
adequacy decision for PIPEDA-covered commercial organisations (S, not
re-read), which matters for EU data flowing to a Canadian client.

## What the skill needs for Canada

- A `ca` regime with three memo sections: "Canada: Privacy laws and roles"
  (PIPEDA, Quebec, Alberta, BC, the per-flow table), "Canada: Automated
  decisions" (Quebec s 12.1 table; DADM for federal clients), "Canada:
  Employment, sector and government AI policy".
- Input pack sections: "Canada: Consent and notice inputs" (the OPC four key
  elements; foreign-processing notice; Alberta country list and s 13.1
  contact) and "Canada: Quebec PIA and s 17 facts" (s 3.3 project facts; per
  flow: sensitivity, purpose, contractual measures, destination legal
  framework, written agreement reference).
- Transfer annex: allow `ca` when Quebec personal information leaves Quebec,
  reusing the destination and access facts table; no SCC module column.
- System card: a Quebec s 12.1 block (information used, reasons and principal
  factors, correction right, how to submit observations to a reviewer); AI
  job-posting disclosure; DADM notice and explanation for federal clients.
- Questionnaire clocks: PIPEDA "as soon as feasible" and the 24-month record;
  Quebec CAI notice for "risk of serious injury" and the incident register;
  Alberta "without unreasonable delay"; BC none.
- Impact assessment: "Canada: AIA inputs" for federal clients; OHRC HRIA as
  the equality checklist for Ontario.
- Documents the client's process produces: the federal AIA and its
  publication, the GC AI Register entry, the Quebec EFVP, the Ontario
  electronic monitoring policy and the ministry AI use-case inventory.
- Words: personal information, organisation, individual, meaningful
  consent, privacy impact assessment (EFVP in Quebec), breach of security
  safeguards (PIPEDA), confidentiality incident (Quebec), person in charge of
  the protection of personal information, real risk of significant harm.
  Never "lawful basis", "controller" or "processor" in Canadian sections.

## Questions counsel usually gets

- Which law governs each flow: PIPEDA, Quebec, Alberta or BC?
- Is the consultancy acting only for the client, so that its handling is a
  transfer for processing, and does its access from Sydney need the Quebec
  s 17 assessment and the Alberta country list?
- Is implied consent enough, or is express consent needed for each purpose?
- Is any decision based exclusively on automated processing under s 12.1?
- Does the s 17 assessment show adequate protection for the US and Australia,
  and is the Google Cloud agreement the written agreement?
- Does the agent "assess" applicants under the Ontario ESA?
- For federal clients: what impact level, and who approves operation?
- Which entity reports a breach to which commissioner?
