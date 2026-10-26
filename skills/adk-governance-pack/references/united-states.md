# United States

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `us` in
scope. The United States has no AI Act and no federal privacy statute, so
the US sections of the regulatory memo assign no risk tier. They screen the
federal and state laws the agent falls under, from facts the design
records: where the client is, which states' residents and staff it serves,
its revenue and data volumes, the data categories, whether an output feeds
a consequential decision, whether the agent is used on employees or
applicants, and whether it chats with consumers.

## Sources and their status

Read at the primary source on 26 October 2026 unless a line says
"reported; not confirmed at the source on 2026-10-26". Several state sites
refused automated reads on that day (California's legislature, Illinois's
legislature), so laws resting on them are marked reported. US rows move
fast: re-check anything a decision rests on rather than waiting for the
checker's 180-day warning.

- Federal Register and govinfo: EO 14365 (90 FR 58499); the FTC's proposed
  policy statement on AI accuracy (91 FR 41638); the amended COPPA Rule (90
  FR 16918); Regulation B final rule of 22 April 2026; CFPB withdrawals.
- eCFR, current to 22 October 2026: 45 CFR 160.103 and 92.210; 12 CFR 1016;
  16 CFR 314; 12 CFR 1002.9; 29 CFR 1607.4.
- FTC press releases and case pages: Workado, the Rytr set-aside, Rite Aid,
  the 7 August 2026 statement on disparate impact
  (<https://www.ftc.gov/news-events/news/press-releases/2026/08/ftc-ditches-disparate-impact>).
- api.congress.gov for federal bills; the White House legislative
  recommendations of 20 March 2026.
- California Privacy Protection Agency regulations text
  (<https://cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_appr_text.pdf>)
  and update page (<https://cppa.ca.gov/regulations/ccpa_updates.html>);
  Civil Rights Council automated-decision system regulations
  (<https://calcivilrights.ca.gov/wp-content/uploads/sites/32/2025/06/Final-Text-regulations-automated-employment-decision-systems.pdf>).
- Colorado SB 26-189 bill page and fiscal note
  (<https://leg.colorado.gov/bills/sb26-189>) and HB 26-1263
  (<https://leg.colorado.gov/bills/hb26-1263>); Texas HB 149 enrolled
  (<https://capitol.texas.gov/tlodocs/89R/billtext/html/HB00149F.htm>); Utah
  SB 226 (2025) and HB 320 (2026) enrolled; NYC DCWP AEDT page
  (<https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page>);
  Connecticut PA 26-15 summary; New York GBL §§1700, 1703; Minnesota Stat.
  325M; Washington RCW 19.375 and 19.373; FCC 24-17; the NAIC model
  bulletin; the NIST AI RMF page.

The full research note, with every secondary item marked, is
`docs/research/us-ai-privacy-law-2026-10-26.md` in the skills repository.

## Federal preemption status

No federal statute preempts state AI or privacy laws (checked 2026-10-26).
EO 14365 (11 December 2025) set up a DOJ AI Litigation Task Force, a
Commerce evaluation of state laws, funding conditions and an FTC policy
statement; it preempts nothing by itself. The FTC statement exists only as a
proposed statement of 7 July 2026. The White House legislative
recommendations of 20 March 2026 are non-binding, and no preemption bill has
left committee. No Commerce list or broadband funding notice was found on
2026-10-26. DOJ intervened on 24 April 2026 in *X.AI LLC v. Weiser*, which
challenges Colorado's law. Every US memo carries a one-line preemption
status with the date checked and names any court order staying a state law
it relies on.

## Roles

Record each as facts with `counsel:` on the conclusion: CCPA business and
service provider or contractor (a service provider must cooperate with the
client's risk assessment and audit, CPPA §7050(h)); state-law controller and
processor (processor contracts include assistance with the controller's
assessments); Colorado developer and deployer; HIPAA business associate;
under the California FEHA regulations an "agent" acting for the employer,
including through an automated-decision system, is itself an employer
(§11008(a)). That a vendor can be liable as the employer's agent is also
tested in *Mobley v. Workday*, reported; not confirmed at the source on
2026-10-26.

## FTC Act Section 5 and federal statutes

- **Claims about the agent.** FTC enforcement targets deceptive capability
  claims. The Workado order (final 28 August 2025) requires competent and
  reliable evidence for accuracy claims about AI. Every capability, accuracy,
  autonomy, "bias-free" or savings claim the client will make cites an M
  record in the system card. The Rite Aid order (filed 8 March 2024) is the
  clearest federal statement of reasonable safeguards for a biometric
  system: risk assessment, pre-deployment and ongoing accuracy and bias
  testing, notice, complaints, retention limits, and shutdown if risks
  cannot be controlled. On 7 August 2026 the FTC said it will not bring
  disparate-impact claims under Section 5 or ECOA; disparate treatment stays
  in scope, and private plaintiffs and states are unaffected.
- **COPPA.** The amended rule's compliance date was 22 April 2026 (checked
  2026-10-26): separate verifiable parental consent before disclosing
  children's data to third parties, including for AI training, and a
  written retention policy and security programme. Trigger: a service
  directed to children under 13, or actual knowledge of their data.
- **HIPAA.** The consultancy becomes a business associate (and Google Cloud
  a subcontractor) when the agent creates, receives, stores, logs or
  transmits PHI for a covered entity (45 CFR 160.103). Record the business
  associate agreement chain. Section 1557's rule on patient care decision
  support tools (45 CFR 92.210) is in force, with the duty to identify and
  mitigate risk from 1 May 2025 (checked 2026-10-26), for HHS-funded
  clients.
- **GLBA.** A financial institution may share with a vendor under a contract
  limiting use (12 CFR 1016.13); the Safeguards Rule requires vendor
  oversight and notice to the FTC within 30 days of an unencrypted breach
  affecting 500 or more consumers (16 CFR 314.4(j), from 13 May 2024,
  checked 2026-10-26).
- **ECOA and Regulation B.** Adverse action notices need specific principal
  reasons; "failed to reach a qualifying score" is not enough (12 CFR
  1002.9(b)(2)). The CFPB's AI circulars were withdrawn on 12 May 2025, but
  the rule is unchanged. A credit agent must be able to produce principal
  reasons per decision, shown by an evaluation case.
- **FCRA.** An agent that assembles third-party information about people
  for credit, insurance, employment or tenancy decisions risks making the
  client or consultancy a consumer reporting agency: a memo line and
  `counsel:`.
- **Title VII and ADA.** Disparate impact (Title VII §703(k)) and the
  accommodation duty are statute; the four-fifths rule (29 CFR 1607.4(D))
  is codified. The EEOC's 2022 and 2023 AI technical-assistance documents
  return 404. Any employment use needs the impact assessment's adverse
  impact section and an accommodation route in the system card.
- **TCPA.** AI-generated voices are "artificial" voices; calls need prior
  express consent, written for telemarketing (FCC 24-17, 8 February 2024).
- **Federal agency clients.** OMB memoranda M-25-21, M-25-22 and M-26-04
  bind federal agencies and, through their contracts, their suppliers;
  M-26-04 asks LLM vendors for model, system or data cards and
  acceptable-use policies, which the system card supplies. They impose
  nothing on a private client.
- **TAKE IT DOWN Act** (mention only): platforms hosting user images or
  video remove reported non-consensual intimate images, including AI
  forgeries, within 48 hours; FTC enforcement from 19 May 2026 (checked
  2026-10-26).

## California

**CPPA regulations: risk assessments and ADMT.** In force from 1 January
2026 (checked 2026-10-26). The client is a "business" when it does business
in California and has over $26,625,000 gross revenue (2025 figure), or buys,
sells or shares personal information of 100,000 or more consumers or
households, or earns 50% of revenue from selling or sharing. California's
law is the only state privacy law covering employees and B2B contacts.

- **Risk assessment before** (§7150(b)): selling or sharing; processing
  sensitive personal information (routine employee payroll and benefits
  processing is exempt); using ADMT for a significant decision; automated
  inference of intelligence, aptitude, performance, health or behaviour
  from systematic observation of applicants, students, employees or
  contractors; training ADMT for significant decisions or biometric
  identification.
- **ADMT** (§7001(e)): technology that processes personal information and
  replaces or substantially replaces human decision-making. A human
  reviewer who can interpret the output, reviews it with other information
  and has authority to change the decision takes it out. Record those three
  facts; whether they hold is `counsel:`.
- **Significant decision** (§7001(ddd)): financial or lending, housing,
  education, employment or contracting (hiring, allocation, pay, promotion,
  discipline, termination), healthcare. Advertising is not.
- **Assessment content** (§7152), which the input pack carries: purpose;
  categories and minimum necessary; collection, use and retention per
  category; approximate number of consumers; disclosures and each service
  provider; for ADMT, the logic with its assumptions and limits and how the
  output is used; benefits; negative impacts; safeguards; **whether the
  business will proceed**; contributors; **the approver's name, position and
  approval date**. Review every three years, update within 45 days of a
  material change, keep five years. One assessment can cover comparable
  processing, and one made for another state can be reused if supplemented
  (§7156).
- **Dates** (checked 2026-10-26): assessments before new in-scope processing
  from 1 January 2026; for processing begun before 2026, by 31 December
  2027; ADMT duties for existing significant-decision use by 1 January 2027;
  first risk-assessment submission and executive attestation by 1 April
  2028. The research read gives the ADMT duties (pre-use notice, opt-out or
  human appeal, access) as applying from 1 January 2027; whether a use that
  starts earlier needs the notices from its first day is `counsel:`.

**Not covered by this reference**, so named only as `counsel:` questions:
federal and state age-discrimination law, New York State law, and state
breach-notification statutes.
- **ADMT notices**: a pre-use notice (§7220) with purpose, the opt-out or the
  exception relied on, the access right, plain-language logic and an
  alternative process; an opt-out with two methods honoured within 15
  business days (§7221) or a human appeal exception; access responses
  explaining purpose, logic and outcome (§7222). The system card's
  automated-decision disclosure holds the facts; the client writes the
  notice.

**FEHA automated-decision system regulations.** In force 1 October 2025
(checked 2026-10-26), 2 CCR §11008 et seq. They cover a "computational
process that makes a decision or facilitates human decision making regarding
an employment benefit" used on California applicants or employees. Anti-bias
testing (its quality, recency, scope, results and the response) is evidence
for any claim or defence (§11009(f)); selection criteria and ADS data are
kept four years (§11013(c)).

**Chatbots.** AB 1609, the Right to Human Customer Service Act, was signed
and is in force from 1 January 2027 (checked 2026-10-26): large businesses
serving Californians offer human service in business hours, try in good
faith to connect within 15 minutes of a request or schedule an appointment,
disclose when the representative is a chatbot, and post contact details. Its
$500 million revenue threshold is reported; not confirmed at the source on
2026-10-26. SB 243 on companion chatbots has been in force since 1 January
2026 (checked 2026-10-26) and excludes bots used only for customer service,
operations, productivity, internal research or technical help; a persona
that sustains a relationship with the user brings it in. The 2019 bot
disclosure law (B&P §§17940 to 17943, sales and votes) is reported; not
confirmed at the source on 2026-10-26.

**Rule out in the memo:** SB 53 (frontier developers training above 10^26
operations or with over $500 million revenue; an ADK build on Gemini is not
one).

## Other state AI laws

- **Colorado SB 26-189.** Signed 14 May 2026; it repealed and re-enacted
  SB 24-205 as an automated decision-making technology law. Its main duties
  apply to consequential decisions made from 1 January 2027 (checked
  2026-10-26). The bill page and fiscal note describe: notice before use in
  a consequential decision; within 30 days of an adverse outcome, a
  plain-language explanation of the decision, the technology's role and the
  consumer's rights; access, correction and human review where commercially
  reasonable; developer documentation to deployers; three-year records. The
  fiscal note records a federal court order of 27 April 2026 stopping the
  Attorney General enforcing SB 24-205 or legislation amending it until
  rulemaking finishes and *X.AI v. Weiser* is decided. That SB 26-189 drops
  SB 24-205's impact assessment, risk-management programme and NIST or ISO
  affirmative defence is reported; not confirmed at the enacted text on
  2026-10-26. Triggers: a system whose output "materially influences" a
  consequential decision about a Colorado consumer in education,
  employment, housing, financial or lending services, insurance, health care
  or essential government services.
- **Colorado HB 26-1263 (Chatbot Safety Act).** Signed 29 May 2026; operator
  duties from 1 January 2027 (checked 2026-10-26): AI disclosure, age
  estimation, a self-harm protocol and minor protections for publicly
  available conversational services; tools primarily for commerce or
  transactional assistance are excluded, and whether a support agent fits
  is `counsel:`.
- **Texas TRAIGA (HB 149).** In force 1 January 2026 (checked 2026-10-26).
  Private-sector prohibitions turn on intent (to incite harm, infringe
  constitutional rights, or discriminate unlawfully; disparate impact alone
  is not intent). The Attorney General's civil investigative demand can ask
  for the system's purpose, training-data types, inputs and outputs,
  performance metrics and limits, monitoring and safeguards: the system
  card and impact assessment answer it. A violation found through
  red-teaming or an internal review substantially complying with the NIST
  AI RMF Generative AI Profile carries no liability (§552.105(e)), so the
  impact assessment records the AI 600-1 actions performed and the
  red-team results.
- **Utah.** Consumer AI disclosure on a clear request; regulated occupations
  disclose high-risk interactions up front (SB 226, in force 7 May 2025,
  checked 2026-10-26). "The AI did it" is no defence.
- **New York City Local Law 144.** Enforced since 5 July 2023: an employer or
  employment agency using an automated employment decision tool on NYC
  candidates or employees needs an independent bias audit within a year
  before use and yearly, a published summary with selection or scoring
  rates and impact ratios by sex, race and ethnicity and their
  intersections, notice 10 business days before use naming the
  qualifications assessed and the route to an alternative process, and
  data-source and retention information on request. Whether a tool
  "substantially assists or replaces" discretionary decisions under the
  DCWP definition, and who the independent auditor is, are `counsel:`
  questions. The audit is the client's; the pack supplies inputs.
- **Connecticut PA 26-15.** Companion chatbot duties from 1 January 2027;
  automated employment decision notices before the decision from 1 October
  2027 (checked 2026-10-26; the OLR summary's date).
- **New York GBL Article 47** (AI companion models), in force 5 November
  2025 (checked 2026-10-26); customer-service and internal tools excluded.
- **Illinois HB 3773** (Human Rights Act: no discriminatory effect, no zip
  code proxies, notice to employees, from 1 January 2026) is reported; not
  confirmed at the source on 2026-10-26. Screen it for any Illinois
  employee or applicant and write it as `counsel:`.
- **Insurers.** The NAIC model bulletin (4 December 2023) expects a written
  AI Systems programme, vendor due diligence with audit clauses and
  consumer notice, and names the NIST AI RMF as an acceptable basis.

## State privacy laws

California's thresholds are above. For the other states, the in-force
dates and thresholds in the research note come from the IAPP tracker and
memory of the statutes: reported; not confirmed at the source on
2026-10-26. Confirm each state's threshold at the statute before the memo
relies on it, and write the conclusion as `counsel:`. Two primary readings
anchor the pattern: Minnesota (in force 31 July 2025) gives a right to
question a profiling result, learn the reason, review the data and have the
decision re-evaluated (325M.14 subd. 1(g)), and requires a data inventory
and a named privacy lead (325M.18). The pattern the input pack screens for
each state the client meets: a profiling opt-out for decisions with legal or
similarly significant effects; a data protection assessment before targeted
advertising, sale, sensitive-data processing or risky profiling; opt-in
consent for sensitive data; processor contracts that include assistance with
assessments. Only California counts employees and B2B contacts as
consumers.

## Biometrics

Texas CUBI as amended by TRAIGA requires consent before capture; Washington
RCW 19.375 requires notice and consent or an opt-out before enrolment;
Colorado (C.R.S. 6-1-1314, from 1 July 2025, checked 2026-10-26) requires a
public biometric policy with retention and incident response; the
Washington My Health My Data Act (RCW 19.373, from 31 March 2024) treats
voice and face biometrics and health inferences as consumer health data,
with separate consent to collect and to share and no threshold. Illinois
BIPA (written release before collection, private right of action) is
reported; not confirmed at the source on 2026-10-26. A voiceprint, face
geometry or health inference about Washington consumers forces counsel.

## Standards that carry legal weight

NIST AI RMF 1.0 (January 2023) is current and being revised; NIST AI 600-1,
the Generative AI Profile (July 2024), is current. Texas is the only state
found where conformity gives a defence (above). The impact assessment's
NIST mapping does real work there and is good evidence elsewhere; cite AI
600-1 as the most recent version with its date.

## Screening checklist

| Trigger fact (with an ID) | Law | Document and section |
| --- | --- | --- |
| Any US client or US residents served | Preemption status; FTC Section 5 | Memo "United States: Preemption status and FTC claims"; system card public claims |
| Client meets the CCPA business test and has Californian consumers or staff | CPPA regulations | Input pack US sections (§7150 screening, §7152 fields, approver, go/no-go) |
| Output replaces or substantially replaces a human in a significant decision about a Californian | CPPA ADMT (by 1 January 2027) | System card automated-decision disclosure; client notices |
| Output materially influences a consequential decision about a Colorado consumer | Colorado SB 26-189 | Memo; system card; records three years |
| Use on job applicants or employees | Title VII and ADA; FEHA (California); NYC Local Law 144; Illinois; Connecticut | Impact assessment adverse impact; memo; bias audit named; `counsel_required: yes` |
| Consumer-facing chatbot | Utah, California AB 1609 (large businesses), companion-law exclusions | System card AI disclosure and hand-off with measured time |
| Persona, memory of the user or relationship features | Companion chatbot laws (California SB 243, New York, Colorado HB 26-1263, Connecticut) | System card disclosure cadence and self-harm protocol; memo exclusion analysis |
| Users may be under 13 | COPPA | Input pack parental consent and retention; `counsel_required: yes` |
| PHI for a covered entity | HIPAA | Input pack business associate chain; questionnaire risk analysis |
| Credit decisions | ECOA Regulation B; FCRA | Impact assessment and system card principal reasons; `counsel_required: yes` |
| Financial institution client | GLBA | Questionnaire vendor safeguards and 30-day notice |
| Voiceprint, face geometry or health inferences | State biometric laws; FTC Rite Aid | Input pack consent, retention, destruction; `counsel_required: yes` |
| Outbound calls or voicemails | TCPA | System card caller identification and opt-out |
| Texas residents served | TRAIGA | Impact assessment NIST AI 600-1 actions and red-team results |
