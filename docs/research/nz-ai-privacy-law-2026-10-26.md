# New Zealand: privacy and AI law for the governance pack

*Read 26 October 2026. Research for adding New Zealand to
`skills/adk-governance-pack` at screen depth. Drafts, not legal advice.*

## Conclusion

New Zealand has no AI Act and no AI bill. Cabinet chose a light-touch,
principles-based approach in July 2024, and the AI Strategy of July 2025 says
"The adoption of these principles does not require additional regulatory
overlay beyond existing law". A New Zealand memo is therefore a **regime
screen**, like the Australian and UK ones: which existing laws and government
policies the agent falls under, triggered by facts the design records.

The Privacy Act 2020 carries most of the weight. What changes the pack:

1. **One Act, no exemptions that matter here.** The Act binds every
   "agency", public or private, of any size, and the Crown. There is **no
   small business exemption and no employee records exemption**. It also
   binds an overseas agency "in the course of carrying on business in New
   Zealand", without a place of business or profit motive (s 4(1)(b), (3)).
   Whether the Sydney consultancy is caught in its own right is `counsel:`.
2. **Agents, not processors.** Section 11 treats information an agent holds
   "for or on behalf of" a principal as held by the principal, wherever the
   agent is, and the transfer to and from the agent is not a use or
   disclosure. The agent becomes an agency in its own right if it uses the
   information "for its own purposes" (s 11(3)). The OPC says a provider that
   uses data for AI training is using it for its own purposes. This is the
   New Zealand equivalent of Australia's "use, not disclosure" test, but it
   is in the statute.
3. **Cross-border (IPP 12) bites only on disclosures.** Sending prompts to
   Gemini in Australia, or giving the consultancy in Sydney access, is not a
   disclosure while they act only as agents (s 11; OPC AI guidance p 11). If
   a recipient uses information for its own purposes, IPP 12 requires one of
   six grounds: informed authorisation, the recipient subject to the Act,
   comparable laws, a prescribed scheme, a prescribed country, or comparable
   safeguards by agreement. **No country or scheme is prescribed** (Privacy
   Regulations 2020, checked 2026-10-26). The Vertex AI data residency page
   (updated 22 October 2026) lists **no New Zealand region for Gemini ML
   processing**, so every design processes prompts offshore; the nearest
   listed region is australia-southeast1.
4. **IPP 3A applies from 1 May 2026, checked 2026-10-26.** Agencies that
   collect personal information "other than from the individual concerned"
   must make the person aware of six matters "as soon as is reasonably
   practicable", unless an exception applies and is documented. An agent
   that pulls data from CRMs, partner systems, web search or users' uploads
   naming other people engages it; the principal, not the s 11 agent,
   notifies. Whether AI-generated statements about a person are indirect
   collection is `counsel:`; the OPC already treats generated information as
   collected.
5. **IPP 8 is a precondition to use.** No use or disclosure without
   reasonable steps to ensure the information is "accurate, up to date,
   complete, relevant, and not misleading". The OPC says "Simply having a
   'human in the loop' may not be enough" and that higher-risk uses may need
   "independent testing and auditing". This replaces Australia's APP 1.7 as
   the hook for automated decisions: New Zealand has **no automated-decision
   transparency rule** and no Article 22 equivalent.
6. **The OPC expects a PIA before using AI tools**, senior leadership
   approval, transparency, human review, no retention or disclosure by the
   tool, and engagement with Māori (AI and the IPPs, September 2023). The Act
   does not require a PIA; the public service GenAI guidance asks agencies to
   do one "for any testing or use of GenAI".
7. **Biometrics have their own code.** The Biometric Processing Privacy Code
   2025 has been in force since 3 November 2025, and for existing processing
   since 3 August 2026, checked 2026-10-26. It covers voice. Rule 1 requires a
   proportionality judgement including "cultural impacts on Māori"; rule 10
   bars inferring emotion, mood, personality, attention, fatigue or health,
   or categorising by a Human Rights Act ground, subject to narrow
   exceptions.
8. **Breaches go to the Commissioner "as soon as practicable"**, and the OPC
   ideally wants them "within 72 hours". Failing to notify the Commissioner
   is an offence with a fine up to $10,000. **There is no civil penalty
   regime**; the Commissioner asked Parliament for one on 28 April 2026.
9. **Government clients bring policy, not statute.** The Public Service AI
   Framework (January 2025) is "not binding"; the GenAI guidance (February
   2025) recommends a register of AI use, a PIA, risk classification and
   NZISM certification and accreditation; the Algorithm Charter (July 2020)
   binds signatory agencies by commitment, with "must be applied" for high
   risk. Cloud First's jurisdictional risk assessment ("Agencies must carry
   out") and the RESTRICTED ceiling for public cloud are the hardest rules a
   supplier meets. There is no counterpart to Australia's DTA mandatory AI
   impact assessment or transparency statement.
10. **Te Tiriti and Māori data appear in guidance, not statute.** The
    Algorithm Charter commits signatories to "Embedding a Te Ao Māori
    perspective ... consistent with the principles of the Treaty of
    Waitangi"; the OPC asks agencies to "Engage with Māori about potential
    risks and impacts to the taonga of their information"; the GenAI
    guidance recommends the Māori Data Governance Model.

Recommended shape: a `nz` code in the jurisdiction switch.
- **Regulatory memo.** "New Zealand: Privacy Act and IPPs" (with roles under
  s 11 and s 4); "New Zealand: Sector, consumer and government AI policy".
- **Privacy impact input pack.** "New Zealand: IPP compliance check" (IPPs 1
  to 13 and 3A, with any code's rules substituted) and "New Zealand:
  Collection and notice inputs" (IPP 3 and 3A matters, overseas recipients).
- **Records of processing.** Not written for `nz` alone; New Zealand has no
  Article 30 register. The input pack's notice inputs replace it.
- **Transfer assessment annex.** Write a New Zealand row per offshore party
  with the s 11 agent facts, and the IPP 12 ground only where a party uses
  information for its own purposes; for public-sector clients, the
  jurisdictional risk assessment inputs.
- **System card.** AI disclosure and alternative channel (OPC); Algorithm
  Charter transparency and appeal fields for signatory agencies; capability
  claims with substantiation (Fair Trading Act s 12A).
- **Security questionnaire.** Notifiable privacy breach clock; RBNZ and FMA
  72-hour clocks (S); NZISM and the agentic AI joint guidance as baselines.
- **Impact assessment.** MBIE Responsible AI Guidance mapping for private
  clients; Algorithm Charter risk matrix for signatory agencies; Māori impact
  and engagement; Human Rights Act s 65 analysis.

## Sources

"P" means read on the primary source on 26 October 2026. "S" means taken from
secondary reporting or search summaries only; re-read before relying on it.
Two research forks read the government AI policy sources (fork B) and the
other laws (fork C) on the same day under the same rules.

### Privacy Act and OPC (read by the coordinator)

| Source | Status | Used for |
| --- | --- | --- |
| Privacy Act 2020, 2020 No 31, latest version as at 8 October 2026 (<https://www.legislation.govt.nz/act/public/2020/31/en/latest/>), downloaded and read for ss 4, 7–12, 22 (IPPs), 23–28, 44, 63, 69, 112–128, 193, 201, 212–214 and the history notes | P | Every Privacy Act statement in sections 1 to 10 |
| Privacy Amendment Act 2025, 2025 No 53, assent 23 September 2025 (<https://www.legislation.govt.nz/act/public/2025/53/en/latest/>) | P, read in full | IPP 3A text; commencement (Part 1 on 1 May 2026, Part 2 on 24 September 2025); s 25A; transitional cls 16–18; s 18(3) bloc assessment |
| Privacy Regulations 2020, SL 2020/194 (<https://www.legislation.govt.nz/secondary-legislation/pco-drafted/2020/194/en/latest/>) and a legislation.govt.nz title search for prescribed countries and binding schemes | P | No prescribed country or binding scheme under IPP 12 |
| OPC, Artificial intelligence and the Information Privacy Principles, September 2023 (<https://www.privacy.org.nz/assets/New-order/Resources-/Publications/Guidance-resources/AI-Guidance-Resources-/AI-and-the-Information-Privacy-Principles.pdf>) | P, pp 1–11 read | Expectations; collection; IPP 5, 6–7, 8, 10–13; Te Ao Māori; s 11 reading of IPP 12 |
| OPC, AI topic page (<https://www.privacy.org.nz/resources-and-learning/a-z-topics/ai/>) | P | Only 2023 guidance listed; "including prompts and training data (IPP5)" |
| OPC, IPP 3A pages (<https://www.privacy.org.nz/privacy-principles/3a/>, <https://www.privacy.org.nz/resources-and-learning/a-z-topics/ipp3a/>); guidance PDF dated 16 December 2025 by file name | P (pages); PDF not opened | Service provider example; documenting exceptions; publicly available; layered notices |
| OPC, Working with third-party providers, 26 November 2024 (<https://www.privacy.org.nz/resources-and-learning/a-z-topics/working-with-third-party-providers/>) | P | s 11 reading; contract terms; AI training as own purpose; 72-hour expectation for providers |
| OPC, NotifyUs page (<https://www.privacy.org.nz/responsibilities/privacy-breaches/notify-us/>) | P | "Ideally ... within 72 hours"; harm factors including cultural perspectives |
| OPC, Privacy impact assessments page (<https://www.privacy.org.nz/responsibilities/privacy-impact-assessments/>) | P | Toolkit documents |
| OPC, Biometric Processing Privacy Code page, overview, rules overview and rule 10 pages (<https://www.privacy.org.nz/privacy-principles/codes-of-practice/biometric-processing-privacy-code/>, `/1-bppc-overview/`, <https://www.privacy.org.nz/resources-and-learning/a-z-topics/biometrics/overview-of-code-rules/>, `/rule-10/`) and the August 2025 summary PDF | P (the code's own text not read) | Dates, Amendment No 1, scope including voice, rules 1, 3, 10, 12, 13 |
| OPC, Privacy Commissioner's submission to the Petitions Committee, signed 28 April 2026 (<https://www.privacy.org.nz/assets/DOCUMENTS/Submissions/2026-04-20-Submission-on-the-Petition-of-Katja-Feldtmann-A1181292-copy-A1184798.pdf>) | P, read in full | No civil penalty regime; reforms sought |
| NCSC-NZ, Careful Adoption of Agentic AI Services, 1 May 2026 (<https://ncsc.govt.nz/protect-your-organisation/careful-adoption-of-agentic-ai-services/>) | P (page; PDF not read) | Date and co-authors |
| Google Cloud, Vertex AI generative AI data residency, last updated 2026-10-22 (<https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/data-residency>) | P | No New Zealand region for ML processing |
| Google Cloud New Zealand region announced August 2022 (Google Cloud press corner) | S | Whether an Auckland region is open was not confirmed |
| Searches for a Privacy Act civil penalty bill and an OPC agentic AI guidance (2026-10-26) | S | None found |

### Government AI policy (fork B)

| Source | Status | Used for |
| --- | --- | --- |
| MBIE, New Zealand's Strategy for Artificial Intelligence: Investing with confidence, July 2025 (<https://www.mbie.govt.nz/assets/new-zealands-strategy-for-artificial-intelligence.pdf>) | P | Light-touch, no regulatory overlay; OECD principles; Māori data sovereignty concern |
| MBIE, Responsible AI Guidance for Businesses, July 2025 (<https://www.mbie.govt.nz/assets/responsible-ai-guidance-for-businesses.pdf>) | P | Voluntary status; inventory, PIA, security, transparency; Māori data; July 2024 Cabinet decision |
| Cabinet paper and minute "Approach to work on Artificial Intelligence", minute 26 June 2024, released 25 July 2024 (mbie dmsdocument 28913 and 28919) | S (blocked) | Light-touch approach |
| CAB-25-MIN-0216 "Going for Growth: Enabling AI uptake", 30 June 2025 (mbie dmsdocument 31025) | S (blocked) | Strategy direction |
| Public Service AI Framework, last updated 29 January 2025 (<https://standards.digital.govt.nz/nz/generative-ai-guidance-gcdo/public-service-ai-framework/2025/en/>; canonical digital.govt.nz page blocked) | P (operational copy) | "not binding"; principles and pillars |
| Joint system leads, Initial advice on Generative AI in the public service, July 2023 (<https://www.digital.govt.nz/assets/Standards-guidance/Technology-and-architecture/Generative-AI/Joint-System-Leads-tactical-guidance-on-public-service-use-of-GenAI-July-2023.pdf>) | P | No personal information in external tools; PIA copied to the GCPO; Te Tiriti-based governance |
| Responsible AI Guidance for the Public Service: GenAI, sub-pages last updated 3 February 2025 (<https://standards.digital.govt.nz/docref/public-service-gen-ai-guidance-responsible-ai/2025/en/> and governance, transparency, privacy, security, procurement, Māori pages) | P (operational copy) | Register, risk classification, PIA, NZISM C&A, transparency |
| GCDO Cloud Jurisdictional Risk Guidance, last updated 14 August 2024 (<https://standards.digital.govt.nz/docref/public-service-gen-ai-guidance-cloud-jurisdictional-risk/2024/en/>) | P (operational copy) | "Agencies must carry out jurisdictional risk assessments"; RESTRICTED ceiling |
| Algorithm Charter for Aotearoa New Zealand, July 2020 (<https://data.govt.nz/assets/data-ethics/algorithm/Algorithm-Charter-2020_Final-English-1.pdf>) | P | Commitments; risk matrix; Māori Data Sovereignty statement |
| Algorithm Charter signatories (29 as of 31 July 2023), Taylor Fry review December 2021 | S | Signatories; review |
| Ministry for Regulation, Responsible AI in action, v1.1 updated 25 August 2026 (<https://www.regulation.govt.nz/publications-and-resources/resource-library/responsible-ai-in-action/>) | P | Regulator guidance; Māori data sovereignty resources |
| NCSC, PSR annual self-assessment (<https://www.ncsc.govt.nz/protect-your-organisation/psr-annual-self-assessment/>) | P | 2014 Cabinet direction; 20 mandatory requirements |
| 2026 cross-agency AI survey; PSC OIA response of 9 October 2026; Online Safety Bill; Procurement Rules 5th edition; NZISM 3.9; DPUP; Minister change | S | Context only |

### Other laws (fork C)

| Source | Status | Used for |
| --- | --- | --- |
| Fair Trading Act 1986, as at 1 July 2026 (<https://www.legislation.govt.nz/act/public/1986/121/en/latest/>) | P | ss 3, 9, 12A, 12B, 13, 26A, 26B, 36K, 40, 45, 46I–46M |
| Fair Trading Amendment Bill 299–1 (<https://www.legislation.govt.nz/bill/government/2026/299/en/latest/>) | P | Status and civil liability tiers |
| Commerce Commission, Navigating the rise of AI (<https://www.comcom.govt.nz/assets/pdf_file/0029/367481/Paper-Navigating-the-rise-of-AI-Perspectives-from-a-Competition-and-Consumer-Regulator.pdf>) | P | FTA lens on AI; *Moffatt* |
| Human Rights Act 1993, as at 27 November 2025, and NZ Bill of Rights Act 1990, as at 30 August 2022 (legislation.govt.nz) | P | ss 20J, 20L, 21, 22, 23, 44, 65; NZBORA ss 3, 5, 19, 27 |
| Human Rights Commission, AI and Digital Technologies executive summary (tikatangata.org.nz) | P content; date S | Advocacy |
| Harmful Digital Communications Act 2015, as at 9 March 2022; Approved Agency Order 2026; Deepfake Digital Harm and Exploitation Bill 213–1 | P (stages S) | Principles, safe harbour, NetSafe, deepfake bill |
| Unsolicited Electronic Messages Act 2007, as at 28 October 2021; DIA spam pages; Marketing Association Do Not Call page | P | Consent, unsubscribe, voice exclusion, voluntary DNC |
| Health Information Privacy Code 2020 consolidated 1 May 2026 and Amendment No 2; Credit Reporting and Telecommunications Information Privacy Codes consolidated 1 May 2026 (privacy.org.nz) | P | Rule 3A, rule 12, scope |
| Customer and Product Data Act 2025, as at 24 January 2026; SL 2025/228, SL 2026/150, SL 2026/267 | P (electricity S) | Status, designation, s 47 |
| Employment Relations Act 2000, as at 10 July 2026; Employment Relations Amendment Act 2026; HSWA 2015; OPC AskUs 214 (updated October 2025) | P | s 4(1A)(c), s 4(4); s 58; monitoring |
| RBNZ material cyber incident reporting; FMA standard condition | S (sites blocked) | 72-hour clocks |
| Financial Markets Conduct Act 2013, as at 19 September 2026; Bill 135 | P | CoFI ss 446B–446J |
| Copyright Act 1994; Crimes Act 1961 | P | s 5(2)(a); s 216G |

## 1. Privacy Act 2020: scope, agencies and agents

**(a) Status.** Privacy Act 2020, 2020 No 31, latest version as at 8 October
2026 (P). In force since 1 December 2020. The substantive changes since 2025
are IPP 3A (from 1 May 2026, checked 2026-10-26), the Part 2 amendments of the
Privacy Amendment Act 2025 (from 24 September 2025, checked 2026-10-26), the
replacement of IPP 12(1)(e) and s 120(6) by the Statutes Amendment Act 2025
(from 27 November 2025, checked 2026-10-26), and consequential edits. The
history notes show no other 2026 privacy change; the only 2026 amendment is
from the Arms Act 2026 (23 September 2026), which does not touch the IPPs.

- **Who it binds (s 4).** A New Zealand agency for anything it does with
  personal information it collects or holds, wherever the information or
  the person is (s 4(1)(a), (2)). An **overseas agency** "in relation to any
  action taken by B in the course of carrying on business in New Zealand"
  (s 4(1)(b)). It "may be treated as carrying on business in New Zealand
  without necessarily" being commercial, having a place of business in New
  Zealand, being paid, or intending to profit (s 4(3)). So an Australian
  consultancy delivering a project for a New Zealand client may itself be an
  agency under the Act; that is `counsel:`.
- **"Agency" is the Act's word.** Public sector agencies (Ministers,
  departments, organisations, local authorities) and private sector agencies
  alike. There is **no small business exemption and no employee records
  exemption** in the Act's definition or in s 8; the Act "binds the Crown"
  (s 6). News entities carrying on news activities, the House, MPs and a few
  others are excluded (s 8(b)).
- **Personal information** "means information about an identifiable
  individual" (s 7(1)). The OPC adds that it "includes information about a
  person that is inaccurate or made up, including fake social profiles and
  deepfake images" (AI and the IPPs, September 2023, p 1).
- **Collect** "means to take any step to seek or obtain the personal
  information, but does not include receipt of unsolicited information"
  (s 7(1)). The OPC: "asking an AI system a question that generates
  information about that person (including false information)" is
  collection; "Even if the AI model gives you information that you know to
  be far-fetched or inaccurate, that is personal information you have
  collected" (AI and the IPPs, p 5).
- **Agents and service providers (s 11).** If agency A holds information
  "for or on behalf of" agency B ("as a representative or agent of B, or for
  safe custody or processing on behalf of B"), the information is treated as
  held by B and not A (s 11(1)–(2)). It is held by A as well "if A uses or
  discloses the information for its own purposes" (s 11(3)). It "does not
  matter whether A is outside New Zealand; or holds the information outside
  New Zealand" (s 11(4)). The transfer to A, and the return of the
  information "and any information derived from the processing of that
  information", is not a use or disclosure by either (s 11(5)).
  - The OPC's third-party providers guidance (26 November 2024) says the
    provider "is 'you' for the purposes of the Privacy Act", the client
    stays fully responsible, and a provider that uses information for AI
    training is using it for its own purposes and can become responsible in
    its own right.
  - Recommended contract terms (same guidance): security proportionate to
    sensitivity with reporting; locate and retrieve quickly for access and
    correction deadlines; "the contract requires the third-party provider to
    notify you of all breaches"; retention limits and return or deletion
    including backups; use only to deliver the services; subcontractors held
    to the same standard.
- **Staff (s 12).** Actions of employees in their duties are the agency's.
- **Privacy officer (s 201).** Every agency "must appoint as privacy
  officers ... 1 or more individuals (within or outside the agency)".
- **Overseas law (s 23).** Action on information held overseas does not
  breach the IPPs if required by the law of another country.

**(b) Triggers.**
- Personal information about anyone in New Zealand in prompts, tools,
  memory, logs, traces or evaluation sets.
- The client is a New Zealand company, a public service department, a
  Crown entity or a local authority (all are agencies).
- The consultancy holds or accesses the client's information from
  Australia (build, test, trace review, support).
- Any provider (Google Cloud, a telemetry vendor) may use the information
  for its own purposes, for example abuse monitoring or training.

**(c) Paperwork.**
- Regulatory memo, Roles: the client as the agency; the consultancy and
  Google as s 11 agents **if** they hold only on the client's behalf;
  `counsel:` whether either uses any information "for its own purposes"
  (s 11(3)); `counsel:` whether the consultancy is an overseas agency
  "carrying on business in New Zealand" (s 4(1)(b)).
- Privacy impact input pack, Recipients and regions: one row per agent with
  the contract terms the OPC lists, and whether the provider's terms permit
  any own-purpose use (abuse monitoring, service improvement, training).
- Privacy impact input pack: the client's privacy officer by name (s 201).
- Security questionnaire: provider breach notice to the client.

**(d) Counsel.**
- Is the consultancy an agent under s 11 only, or also an agency in its own
  right (s 4(1)(b), s 11(3))?
- Does Google's abuse monitoring, logging or any retention of flagged
  prompts count as use "for its own purposes"?
- Is a group company in Australia (if the client has one) a separate agency?

## 2. Collection: IPPs 1 to 4

**(a) Status.** In force; text as at 8 October 2026 (P).

- **IPP 1.** Collect only "for a lawful purpose connected with a function
  or an activity of the agency" where "the collection of the information is
  necessary for that purpose" (IPP 1(1)). If the purpose does not need
  identifying information, "the agency may not require" it (IPP 1(2)).
- **IPP 2.** Collect from the individual concerned (IPP 2(1)), unless the
  agency believes on reasonable grounds that an exception applies:
  no prejudice to the individual; compliance would prejudice the purpose;
  the individual authorised collection from someone else; "publicly
  available information"; maintenance of the law and the other public
  interest grounds; "not reasonably practicable"; or non-identifying,
  statistical or research use (IPP 2(2)).
- **IPP 3.** When collecting from the individual, reasonable steps so they
  know: the fact of collection; the purpose; the intended recipients; the
  name and address of the collecting and holding agencies; any law
  authorising it and whether supply is voluntary; consequences of not
  providing it; and the access and correction rights (IPP 3(1)). Before
  collection or, if not practicable, as soon as practicable after
  (IPP 3(2)). Not needed if done on "a recent previous occasion" for the
  same kind of information (IPP 3(3)); exceptions in IPP 3(4).
- **IPP 4.** Collect only by lawful means and by means that are fair and do
  "not intrude to an unreasonable extent upon the personal affairs of the
  individual concerned", "particularly in circumstances where personal
  information is being collected from children or young persons".

**What the OPC says about AI (AI and the IPPs, September 2023, P).**
- Expectations: "Have senior leadership approval based on full
  consideration of risks and mitigations"; "Review whether a generative AI
  tool is necessary and proportionate"; "Conduct a privacy impact
  assessment before using these tools"; "Be transparent, telling people
  how, when, and why the tool is being used"; "Engage with Māori about
  potential risks and impacts to the taonga of their information"; "Develop
  procedures about accuracy and access"; "Ensure human review prior to
  acting on AI outputs to reduce risks of inaccuracy and bias"; "Ensure
  that personal information is not retained or disclosed by the AI tool".
- "If you're providing a service such as a chatbot or phone line, and want
  to collect information to train, refine, or use AI tools, you may need to
  take particular care to clearly explain this to people, and to consider
  offering people a chance to opt out from this use of information."
- On the publicly available exception: scraped training data may include
  login-only sources, so "you may need to be cautious about assuming this
  material is 'publicly available'".
- Fairness: "people cannot readily avoid using banking services,
  supermarkets, or telecommunications. This may mean more care is needed".

**(b) Triggers.**
- The agent asks users for information, or captures free text, voice or
  uploads.
- The agent generates or infers statements about a person (summaries,
  scores, classifications, drafts about named people).
- The design collects more than the task needs (whole records when a field
  would do; identity when anonymous use would work).
- Children or young people could be users.
- A chatbot or phone channel whose transcripts are kept for evaluation,
  tuning or training.

**(c) Paperwork.**
- Privacy impact input pack, Necessity and proportionality: one line per
  data item with its purpose (IPP 1), and whether identity is required
  (IPP 1(2)).
- Input pack, a new "New Zealand: IPP compliance check" section: IPP 1 to
  13, IPP 3A and any code rule that substitutes.
- Input pack, a new "New Zealand: Collection and notice inputs" section:
  the IPP 3 matters for direct collection and the IPP 3A matters for
  indirect collection, as proposed notice text, plus the opt-out for
  training or evaluation use of transcripts.
- System card, AI disclosure and hand-off: how, when and why AI is used
  (the OPC's transparency expectation), and the alternative channel the
  OPC suggests ("providing a website, an online form, and a phone number
  may still be important").
- Impact assessment: senior leadership approval as a named decision and a
  calendar wait.

**(d) Counsel.**
- Is each collection "necessary" for the lawful purpose (IPP 1)?
- Is generated or inferred information a "collection" from someone other
  than the individual, engaging IPP 2 and IPP 3A? (The OPC treats it as
  collection; the source analysis is counsel's.)
- Is the manner of collection fair, especially for children (IPP 4)?

## 3. IPP 3A: indirect collection (Privacy Amendment Act 2025)

**(a) Status.** Privacy Amendment Act 2025, 2025 No 53, assent 23 September
2025 (P). Part 1 (IPP 3A and consequential changes) "comes into force on 1
May 2026"; Part 2 "comes into force on 24 September 2025" (s 2, P). IPP 3A
applies from 1 May 2026, checked 2026-10-26. It "does not apply to personal
information collected before 1 May 2026" (s 25A). It does not apply to
information collected under an approved information sharing agreement or
information matching agreement in force before 1 May 2026 (Schedule 1, new
Part 2, cls 17–18). Several codes were amended to mirror it (Amendment No 1
to the Biometric Processing Privacy Code, March 2026, in force 1 May 2026;
HIPC rule 3A per the OPC's IPP 3A page, P).

- **The duty (IPP 3A(1)).** When an agency collects personal information
  "other than from the individual concerned", reasonable steps so the
  individual is aware of: the fact of collection; the purpose; the intended
  recipients; the name and address of the collecting and holding agencies;
  any law authorising or requiring it; and the access and correction
  rights.
- **Timing (3A(2)).** "as soon as is reasonably practicable after the
  information has been collected (unless taken sooner)".
- **Already aware (3A(3)).** Not needed if the person "has previously been
  made aware by any means of all of the matters". The statutory example:
  agency A, when complying with IPP 3, told the person their information
  would go to B and gave the B matters; B need not notify.
- **Exceptions (3A(4)–(7)).** Reasonable belief that non-compliance would
  not prejudice the individual; the information is publicly available;
  maintenance of the law and other public interest grounds; compliance
  would prejudice the purpose; "not reasonably practicable"; a serious
  threat to public health or safety or another person's health or safety;
  non-identifying or statistical use; archiving; security, defence and
  international relations; trade secrets or unreasonable commercial
  prejudice.
- **OPC guidance (final PDF dated 16 December 2025 by its file name;
  flowchart 4 November 2025; IPP 3A page, P).**
  - "IPP3A applies to all personal information agencies collect
    indirectly, from any source."
  - Service providers: where Swiftstart NZ hosts Clear Consulting's
    database and does not use it for its own purposes, "Clear Consulting is
    responsible for meeting any IPP3A requirements." The s 11 agent does
    not notify; the principal does.
  - The publicly available exception may cover a website or public social
    media page, not material behind a login or private account.
  - "Having incompatible systems or processes is not a valid reason to rely
    on this exception" (not reasonably practicable).
  - "Documenting your rationale and decision-making will be important";
    the "already aware" exception must rest on "evidence rather than an
    assumption"; keep evidence of prior notices.
  - Contract terms requiring another agency to notify can help, "but
    responsibility stays with the collecting agency".
  - Layered notices (short notices on forms or screens, fuller online
    text) are acceptable formats.

**(b) Triggers.** Collections from 1 May 2026 where the agent:
- pulls information about a person from a third-party system, CRM,
  partner API, public web search or grounding service;
- reads documents, emails or tickets that name other people (third parties
  in a user's upload, colleagues in an HR file, referees);
- enriches a record from another source, or builds a profile across tools;
- generates or infers information about a person who is not the user
  (whether generation is an indirect collection is `counsel:`).

**(c) Paperwork.**
- Input pack, "New Zealand: Collection and notice inputs": one row per
  indirect source with the six IPP 3A matters, who notifies (the
  principal agency, not the s 11 agent), how (layered notice, upstream IPP
  3 notice under 3A(3)), and any exception relied on **with its documented
  rationale** (OPC).
- Input pack, Data flows: mark each flow direct or indirect and the date
  collection began relative to 1 May 2026.
- Memo: one line with the commencement date and `checked 2026-10-26`.

**(d) Counsel.**
- Is AI-generated or inferred information about a person an indirect
  collection under IPP 3A, or a collection from no "source" at all?
- Does an exception apply, especially "not reasonably practicable" and "no
  prejudice", for large volumes of third parties named in user uploads?
- Does an upstream notice by the client's partner satisfy 3A(3)?

## 4. Security: IPP 5

**(a) Status.** In force (P). An agency must ensure the information "is
protected, by such security safeguards as are reasonable in the
circumstances to take, against— (i) loss; and (ii) access, use,
modification, or disclosure that is not authorised by the agency; and (iii)
other misuse" (IPP 5(a)), and, if it must be given to a person "in
connection with the provision of a service to the agency, everything
reasonably within the power of the agency is done to prevent unauthorised
use or unauthorised disclosure" (IPP 5(b)).

The OPC on AI: "You must keep personal information secure, including prompts
and training data (IPP5)" (AI topic page, P); AI tools "may lead to more
sharing of information with third party providers"; some "can leak sensitive
information"; and agencies "may need privacy breach response plans" (AI and
the IPPs, pp 7–8, P, citing the OWASP LLM top 10).

The NCSC-NZ co-authored "Careful Adoption of Agentic AI Services" with ASD's
ACSC, CISA, NSA, the Canadian Cyber Centre and NCSC-UK, published 1 May 2026
(P, NCSC-NZ page; the PDF was not read). It "primarily focuses on large
language model (LLM)-based agentic AI systems".

**(b) Triggers.** Any personal information held; prompt injection reaching
tools with data access; cross-user memory; logs and traces with personal
information; consultancy access from Australia.

**(c) Paperwork.** Security questionnaire: map controls (SB and C IDs) to
IPP 5(a) and to the agentic guidance as a baseline; IPP 5(b) facts on each
service provider (contract, access control, breach notice). Input pack, Risks
and measures: prompt and trace storage, retention, access.

**(d) Counsel.** Are the safeguards "reasonable in the circumstances" given
the sensitivity, and is "everything reasonably within the power of the
agency" done for providers (IPP 5(b))?

## 5. Access and correction: IPPs 6 and 7

**(a) Status.** In force (P). An individual may receive "confirmation of
whether the agency holds any personal information about them" and "access to
their personal information" (IPP 6(1)), subject to Part 4. An individual may
request correction; the agency must take reasonable steps so the information
is "accurate, up to date, complete, and not misleading"; a statement of
correction must be attached on request if the agency declines; and other
recipients must be told of a correction "so far as is reasonably
practicable" (IPP 7). The agency responds "as soon as is reasonably
practicable, and in any case not later than 20 working days after the day on
which the request is received" (s 44(1), as amended from 24 September 2025,
checked 2026-10-26; correction, s 63(1), same limit). Failure to meet the
time limits is treated as a refusal and can be an interference with privacy
(s 69(3)–(5)).

The OPC: "The original training data, the pre-trained model, and the outputs
may all potentially contain personal information while providing no practical
way to access or correct it"; "It is essential that you develop procedures";
check identity, because "AI tools may make it easier to realistically
impersonate someone" (AI and the IPPs, p 8, P).

**(b) Triggers.** Session history, memory stores, vector stores, traces,
evaluation sets or generated documents that hold information about a person;
an agent that answers people's own requests.

**(c) Paperwork.** Input pack, Data flows and Retention: per store, whether it
is searchable by person and correctable, and how a statement of correction
is attached; the 20-working-day clock. Questionnaire: identity verification
for requests. There is **no general right to erasure** in the Act; the
Commissioner asked Parliament for one on 28 April 2026 (see section 10).

**(d) Counsel.** Is a model's weights or an embedding "personal information
held"? Can a Part 4 withholding ground apply to agent memory?

## 6. Accuracy before use: IPP 8

**(a) Status.** In force (P). An agency "must not use or disclose that
information without taking any steps that are, in the circumstances,
reasonable to ensure that the information is accurate, up to date, complete,
relevant, and not misleading" (IPP 8). Unlike Australia's APP 10, the duty is
framed as a **precondition to use or disclosure**, which catches acting on an
AI output.

The OPC (AI and the IPPs, pp 8–10, P):
- It applies "at all stages from gathering training data, to training a
  model, to implementing a tool, accepting input, providing output, and
  taking actions as a result".
- "Generative AI tools produce confident errors of fact and logic, so you
  cannot rely on their apparent performance or self-declared capabilities as
  evidence of accuracy."
- Most tools were trained overseas on data "that may not be relevant,
  reliable, and ethical for use in Aotearoa New Zealand"; New Zealand's mix
  of "cultural perspectives, demographics, and use of languages including
  English and Te Reo Māori" means tools not designed with local communities
  may produce "inaccuracy in the form of bias, exclusion".
- "Depending on the nature of the intended use and level of risk, this may
  require independent testing and auditing. Doing and updating a PIA will be
  an essential part of this process."
- Automated decisions: "it will generally be necessary to develop processes
  for human review of decisions, and to empower and adequately resource the
  people doing this work. Simply having a 'human in the loop' may not be
  enough to uphold the accuracy principle, given the well-known problem of
  automation blindness".
- Use case, screening job applications: "The track record of AI tools in
  this area is not good, so you need to be very confident the system you want
  to use will be transparent, accurate, and fair before you ask anyone to rely
  on it."

**(b) Triggers.** Any output about a person that is used, sent, stored or
acted on; summaries of case files, HR records, complaints, health notes;
outputs in te reo Māori or about Māori or Pacific people; screening or
ranking people.

**(c) Paperwork.** Impact assessment: evaluation results (M records) on
New Zealand data, including te reo Māori where relevant, and disaggregated
error rates; system card, Limits and Evaluation results; input pack, IPP 8
row citing the M records and the review step (contract ID, reviewer's
authority and training, share reviewed). Do not write that a reviewer
satisfies IPP 8; write the review facts.

**(d) Counsel.** Are the steps "reasonable in the circumstances" for this use
and risk level? Does the review step address automation blindness?

## 7. Retention, use and disclosure: IPPs 9, 10 and 11

**(a) Status.** In force (P).
- **IPP 9.** Do not keep information "for longer than is required for the
  purposes for which the information may lawfully be used".
- **IPP 10.** Information obtained for one purpose may not be used for
  another unless the agency believes on reasonable grounds that: the purpose
  is "directly related"; it is used in non-identifying form or for
  statistics or research not published identifiably; the individual
  authorised it; the source is a publicly available publication and the use
  is not unfair or unreasonable; or a law-enforcement, revenue,
  proceedings, or serious-threat ground applies (IPP 10(1)).
- **IPP 11.** No disclosure "to any other agency or to any person" unless a
  listed ground applies: a purpose of collection or directly related; to the
  individual; authorised; publicly available publication; law enforcement
  and similar; serious threat; intelligence agencies; non-identifying or
  research; sale of a business (IPP 11(1)). "This IPP is subject to IPP
  12" (IPP 11(2)).
- **Use versus disclosure with agents.** Passing information to an s 11
  agent and receiving it back "is not a use or disclosure" (s 11(5)). The
  OPC: "Using offshore technology providers to store or process your data is
  not treated as a disclosure under IPP12, so long as they are not using that
  information for their own purposes" (AI and the IPPs, p 11, P).
- **OPC on AI re-use (p 10, P).** "if you want to use personal information to
  train an AI tool, you need to make sure that is clear at the time you
  collect it"; supplying existing information in a prompt "may go beyond the
  purpose for which you collected that information"; prefer tools "where the
  contractual terms stop the provider from using input data for training".

**(b) Triggers.** Re-use of existing customer, staff or case data for
grounding, evaluation sets or fine-tuning; prompts that carry records into a
model; the agent sending information to third parties (emails, tickets,
APIs); retention of sessions, memory and traces beyond the task.

**(c) Paperwork.** Input pack: one line per re-used dataset with its original
purpose and the IPP 10 ground proposed (`counsel:`); one line per outbound
disclosure with the IPP 11 ground; Retention and erasure with periods per
store (IPP 9); Model provider data use stating that the contract bars
training on inputs (or the gap).

**(d) Counsel.** Is grounding or evaluation on existing data a "directly
related" purpose? Is any provider an agent, or a recipient of a disclosure?

## 8. Cross-border disclosure: IPP 12

**(a) Status.** In force; IPP 12(1)(e) replaced from 27 November 2025
(Statutes Amendment Act 2025), checked 2026-10-26 (P).
- An agency may disclose personal information "to a foreign person or
  entity" in reliance on IPP 11(1)(a), (c), (e), (f), (h) or (i) **only if**
  one of these holds (IPP 12(1)):
  - (a) the individual authorises it "after being expressly informed by A
    that B may not be required to protect the information in a way that,
    overall, provides comparable safeguards to those in this Act";
  - (b) B "is carrying on business in New Zealand" and A believes on
    reasonable grounds B "is subject to this Act";
  - (c) B is subject to privacy laws that, overall, provide comparable
    safeguards;
  - (d) B participates in a prescribed binding scheme;
  - (e) B is subject to the laws of a prescribed country, within any
    prescribed limits;
  - (f) A "otherwise believes on reasonable grounds that B is required to
    protect the information in a way that, overall, provides comparable
    safeguards ... (for example, pursuant to an agreement entered into
    between A and B)".
- **Foreign person or entity** includes a body "not established under the
  law of New Zealand" that "does not have its central control and management
  in New Zealand" (s 7(1)). An Australian company is one.
- **No country or scheme is prescribed.** The Privacy Regulations 2020 (SL
  2020/194) contain no prescribed countries or binding schemes, and a title
  search of legislation.govt.nz found no privacy prescribed-country
  regulations (P, 2026-10-26). The Privacy Amendment Act 2025 s 12 lets the
  Commissioner assess a country "on the basis of the country being a member
  of a bloc", for example the EEA under the GDPR (s 18(3), from 24
  September 2025, checked 2026-10-26).
- **Agents are outside IPP 12.** Under s 11 and the OPC's reading, sending
  information to the consultancy in Sydney or to Google's model endpoint is
  not a disclosure while they hold it only for the client. IPP 12 bites when a
  recipient uses information for its own purposes (s 11(3)). The client
  "remain[s] responsible for protecting that information" (AI and the IPPs,
  p 11) and IPP 5(b) applies.
- **Commissioner's transfer prohibition (s 193).** The Commissioner may
  prohibit onward transfer of information received from another country to a
  third country without comparable safeguards. Rarely relevant.
- **Where Gemini processes.** The Vertex AI data residency page (updated 22
  October 2026, P) lists no New Zealand region for ML processing; the nearest
  Google-model processing region listed is Australia (australia-southeast1).
  So prompts from a New Zealand agent are processed outside New Zealand in
  every design today.

**(b) Triggers.** Any processing, logging, grounding, abuse review, support or
evaluation outside New Zealand; any provider whose terms allow own-purpose use;
the consultancy's staff in Australia accessing data.

**(c) Paperwork.** A **transfer assessment annex row for New Zealand** (new),
or an input pack section, per offshore recipient: country; agent or recipient
(s 11 facts: contract, own-purpose use); if a disclosure, the IPP 12(1)
ground proposed, with the model contract clauses as the usual (f) evidence;
the IPP 3 or 3A notice text about overseas recipients. The OPC model clauses
for IPP 12(1)(f) exist (reported by firms in 2020–2021; S, not confirmed at the
source on 2026-10-26).

**(d) Counsel.** Is each offshore party an agent (s 11) or a foreign recipient
(IPP 12)? If a recipient, does Australian law give "comparable safeguards"
(IPP 12(1)(c)), or is a contract needed (IPP 12(1)(f))?

## 9. Unique identifiers: IPP 13

**(a) Status.** In force (P). Assign a unique identifier only if "necessary to
enable A to carry out 1 or more of its functions efficiently" (IPP 13(1)); do
not assign the same identifier another agency assigned, except for associated
persons or statistics (13(2)); simply recording another agency's identifier to
communicate with that agency is not assigning (13(3)); identity "clearly
established" and misuse minimised, "for example, by showing truncated account
numbers" (13(4)); do not require disclosure except for the purpose (13(5)).
The OPC: AI "may lead to AI tools finding patterns in a person's behaviour
that qualify as a unique identifier"; ask whether training data "include
unique identifiers that can be revealed in outputs" (AI and the IPPs, p 11, P).

**(b) Triggers.** The agent mints user, case or session IDs used to identify
people; it re-uses IRD numbers, NHI numbers, driver licence numbers or
another agency's customer numbers as keys; outputs echo identifiers.

**(c) Paperwork.** Input pack, People and data categories: identifiers held,
assigned or echoed; output masking contract (C ID) for identifiers.
Biometric templates as unique identifiers fall under rule 13 of the
Biometric Code (section 12).

**(d) Counsel.** Is an internal key an IPP 13 "unique identifier"?

## 10. Notifiable privacy breaches (Part 6) and the Commissioner's powers

**(a) Status.** In force since 1 December 2020; s 120(6) inserted from 27
November 2025, checked 2026-10-26 (P).
- **Privacy breach** (s 112): "unauthorised or accidental access to, or
  disclosure, alteration, loss, or destruction of" the information, or "an
  action that prevents the agency from accessing the information on either a
  temporary or permanent basis", whoever caused it and whether or not
  ongoing. A **notifiable** breach is one "it is reasonable to believe has
  caused serious harm ... or is likely to do so".
- **Serious harm factors** (s 113): steps taken to reduce harm; sensitivity;
  the nature of the harm; who has or may obtain the information; security
  protection; any other matters. The OPC adds cultural perspectives on harm
  (NotifyUs page, P).
- **Notify the Commissioner** "as soon as practicable after becoming aware"
  (s 114). The OPC: "Ideally you'll do that within 72 hours after you're
  aware ... even if you're still investigating it" (NotifyUs page, P), and
  for service providers it "generally expects to be told about notifiable
  breaches within 72 hours" of the provider becoming aware (third-party
  providers guidance, P).
- **Notify affected individuals** as soon as practicable, or give public
  notice if not reasonably practicable (s 115); exceptions and delay in s 116
  (security, law, safety, trade secret; under-16s; health); contents in s 117;
  information may be given incrementally (s 117(5)).
- **Offence** (s 118): failing to notify the Commissioner without reasonable
  excuse, fine "not exceeding $10,000". Failing to notify individuals can be
  an interference with privacy (s 115(5), s 69(2)(a)(iv)).
- **Agents** (s 120): an agent's acts count as both the agent's and the
  principal's; an agent's liability depends on whether it holds the
  information under s 11; "a person (A) is an agent of an agency (B) if A
  holds information for or on behalf of B" (s 120(6)).
- **Commissioner's powers.** Complaints and investigations (Part 5);
  interference with privacy needs a breach plus harm (s 69(2)), or a
  refusal without proper basis of access or correction (s 69(3)); the Human
  Rights Review Tribunal awards remedies (s 102). **Compliance notices**
  for a breach of the Act or a code (s 123), with information powers
  (s 128). Transfer prohibition notices (s 193). Offences of $10,000 for
  obstruction, false statements, impersonation to obtain information, and
  destroying requested documents (s 212).
- **No civil penalty regime.** The Commissioner told the Petitions Committee
  on 28 April 2026: "in New Zealand there's no civil penalty regime"; he
  seeks "significant fines", audit powers and a right to erasure (P). No
  government bill was found (S, search 2026-10-26).

**(b) Triggers.** Any personal information held. Agent breach paths: prompt
injection exfiltrating data; cross-user memory leaks; traces in the wrong
sink; a provider using data outside the contract; a lost or encrypted store
(ransomware is an "action that prevents the agency from accessing").

**(c) Paperwork.** Security questionnaire, Incident notification: New
Zealand clock "as soon as practicable" with the OPC's 72-hour expectation;
who notifies (the principal agency); the consultancy's contractual duty to
tell the client promptly (OPC: "notify you of all breaches"); NotifyUs as the
channel. Input pack: breach response plan reference.

**(d) Counsel.** Is a given incident "likely" to cause "serious harm"? Which
entity notifies when the consultancy also holds information for its own
purposes?

## 11. OPC AI guidance and the PIA toolkit

**(a) Status.**
- "Artificial intelligence and the Information Privacy Principles",
  September 2023, and a one-page summary (P). The OPC AI page shows only
  2023 material; no update or agentic guidance was found on privacy.org.nz
  (P page check; S search, 2026-10-26).
- "Commissioner's expectations around AI use", issued May 2023, updated 15
  June 2023 (P, listed as earlier guidance).
- PIA toolkit (P): an initial "brief privacy analysis template" (threshold),
  "How to do a Privacy Impact Assessment" guide, "Template 2 – PIA Report
  (updated)", "Examples of Risks and Mitigations" and "Template 3 – Risk and
  Mitigation Table (updated)". The link titles carry "100924"; the page does
  not say whether PIAs are mandatory. The Act itself does not require a PIA.
  The OPC "expect[s] organisations to do a privacy impact assessment (PIA)
  before using AI tools" (AI and the IPPs, p 2). Public service PIA
  requirements come from government policy (see the government section).
- Te Ao Māori in the AI guidance (p 2, P): "You need to consider Māori
  perspectives on privacy"; concerns include "bias from systems developed
  overseas that do not work accurately for Māori", collection "without work
  to build relationships of trust", and "Exclusion from processes and
  decisions of building and adopting AI tools that affect Māori whānau,
  hapū, and iwi, including use of these tools by the Crown". The
  Commissioner "must take account of cultural perspectives under s 21".

**(b) Triggers.** Any New Zealand AI deployment that touches personal
information.

**(c) Paperwork.** Input pack: built to the OPC toolkit's shape (threshold,
full report, risk and mitigation table); the OPC's eight expectations as a
checklist row each; Māori engagement as a stakeholder line with owner or
`gap:`. Impact assessment: senior leadership approval; independent testing
where risk warrants.

**(d) Counsel.** Is a full PIA warranted after the threshold assessment (the
privacy officer decides)?

## 12. Biometric Processing Privacy Code 2025

**(a) Status.** Issued 21 July 2025 under s 32 (P, OPC page). In force for new
biometric processing from 3 November 2025; processing that began before then
had until 3 August 2026 to comply (both checked 2026-10-26; P, OPC page and
the August 2025 summary). Amendment No 1 (March 2026) reflects IPP 3A; the
current text is "in force from 1 May 2026" (P). The 13 rules "substitute for
the 13 principles of the Privacy Act" for biometric information (summary, P).

- **Scope.** Agencies that collect biometric information "in an automated
  process to verify, identify or categorise" people (P). Biometric
  information covers physical and behavioural features, "such as faces,
  fingerprints, voices, keystroke patterns, or gait" (P), including how a
  person "sounds when they speak"; templates are covered. Health agencies
  providing health services fall under the HIPC instead; personal consumer
  devices are generally outside.
- **Rule 1.** Collection must be for a lawful purpose, necessary, with
  safeguards, and proportionate: the agency must believe on reasonable
  grounds that the processing is proportionate to the likely impacts,
  weighing privacy risk, "cultural impacts on Māori", and whether the
  benefit outweighs the risk (P). The pages do not say the assessment must be
  written down; documenting it is prudent (`counsel:`).
- **Rule 3.** Notice before or at collection, "clear and obvious", including
  whether a non-biometric option exists (P).
- **Rule 10, biometric categorisation limits.** Unless an exception applies,
  do not use biometric processing to obtain, infer or generate information
  about health; "emotion, mood, personality, mental state, or intention";
  "attention, state of fatigue, or alertness"; or categorise people by a
  prohibited ground in s 21(1) of the Human Rights Act (P). The ordinary
  directly related purpose and authorisation exceptions do not apply.
  Exceptions: express authorisation (health limit only); health agencies;
  accessibility; serious threat; research with ethical oversight; health and
  safety (attention and fatigue only). OPC examples: inferring two
  employees' emotions from verbal interaction is restricted; inferring an
  applicant's personality from a video interview is restricted; monitoring
  office workers' alertness for productivity does not fit an exception.
- **Rule 12** mirrors IPP 12; **rule 13** limits templates as unique
  identifiers.

**(b) Triggers.** Voice agents that verify callers by voiceprint; face or
liveness checks; sentiment or emotion detection from voice or video;
analysing staff or customer speech for stress, mood or attention; inferring
sex, ethnicity or disability from images or voice.

**(c) Paperwork.** Input pack, Necessity and proportionality: a written rule 1
proportionality assessment with the cultural impacts on Māori; rule 3 notice
text and the non-biometric alternative; rule 10 check (yes or no per
inference, exception relied on). System card: biometric functions. Memo:
`counsel_required: yes`.

**(d) Counsel.** Is a function "biometric processing" (automated, to verify,
identify or categorise)? Does a rule 10 exception apply? Is speech-to-text
alone outside the Code (it does not identify or categorise)?

## 13. Government AI policy

Fork B read these sources on 2026-10-26. digital.govt.nz, beehive.govt.nz,
data.govt.nz HTML pages and mbie.govt.nz HTML pages refused automated reads
(MBIE sits behind a bot wall). MBIE and data.govt.nz PDFs, the 2023 interim
guidance PDF, standards.digital.govt.nz (the GCDO's operational copy, whose
disclaimer says digital.govt.nz is authoritative), regulation.govt.nz,
ncsc.govt.nz and privacy.org.nz were readable. Pages read on
standards.digital.govt.nz are marked P with that caveat.

### 13.1 No AI Act: Cabinet decisions and the AI Strategy

**(a) Status.**
- Cabinet agreed "in July 2024 to a strategic approach to work on
  Artificial Intelligence", including "endorsement of the ... OECD AI
  Principles" (MBIE business guidance, Appendix Four, P). The Cabinet
  paper "Approach to work on Artificial Intelligence" and its minute of 26
  June 2024 were proactively released on 25 July 2024 (S; the MBIE
  dmsdocument links refused reads). Law firms describe a "light-touch,
  proportionate and risk-based approach" that discourages a standalone AI
  Act (S, Buddle Findlay, MinterEllisonRuddWatts).
- Cabinet minute CAB-25-MIN-0216, "Going for Growth: Enabling AI uptake
  across the economy", 30 June 2025 (S). A search summary says rules
  should be "no more restrictive than ... comparator OECD countries"
  (S, unverified wording).
- "New Zealand's Strategy for Artificial Intelligence: Investing with
  confidence", MBIE, July 2025 (P; launch 8 July 2025, S): "New Zealand is
  taking a light-touch and principles-based approach to AI policy"; "The
  adoption of these principles does not require additional regulatory
  overlay beyond existing law"; existing frameworks such as "privacy,
  consumer protection, human rights" "can be updated as and when needed".
  It "confirms New Zealand's adoption of the OECD's AI Principles".
- **2026.** No AI bill and no Strategy update found (S). The Ministry for
  Regulation published "Responsible AI in action" for regulators on 27 May
  2026, version 1.1 updated 25 August 2026, adding Māori data sovereignty
  resources (P); advisory ("Agencies are encouraged to start small";
  "people remain responsible for decisions"). The Online Safety (Minimum
  Age and Child Safety Risk Assessment) Bill, introduced in late August
  2026, would set a minimum age of 16 for some platforms including "social
  AI companions" (S; stage not verified). Paul Goldsmith is reported as
  Minister for Digitising Government since 7 April 2026 (S, Wikipedia).

**(b) Triggers.** Every New Zealand pack (the memo says there is no AI Act);
a regulator client (Ministry for Regulation guidance); a companion-style
chatbot reachable by under-16s (the Online Safety Bill, pending).

**(c) Paperwork.** Memo: one line, "No AI-specific statute applies in New
Zealand; the July 2025 AI Strategy relies on existing law", with `checked
2026-10-26`; the rest of the New Zealand sections screen existing law.

**(d) Counsel.** Has a sector regulator issued binding AI rules for the
client's sector? Would the Online Safety Bill, as introduced, reach this
agent?

### 13.2 MBIE Responsible AI Guidance for Businesses (July 2025)

**(a) Status.** Dated July 2025 (P,
<https://www.mbie.govt.nz/assets/responsible-ai-guidance-for-businesses.pdf>).
"a voluntary resource", "in line with New Zealand's proportionate risk based
approach to AI (agreed by Cabinet)", and it "does not remove the need to
follow all relevant and applicable New Zealand legislation" (P).

What it asks (P):
- Catalogue legal obligations (Fair Trading Act, Human Rights Act and
  NZBORA, Privacy Act, Copyright Act and others). "Any business interacting
  with personal information is required to have a privacy officer."
- Risk cycle with a "risk inventory" and a "stakeholder impact
  assessment"; cites the Stats NZ Algorithm Impact Assessment toolkit,
  ISO/IEC 42001, ISO/IEC 23894 and ISO 31000.
- Records: "AI model cards"; "Each AI system should have an
  organisation-wide inventory" covering purpose, use cases,
  accountabilities, legal obligations, risks, stakeholders, capabilities
  and limitations including testing, human oversight, technical
  specifications and audit outcomes.
- "Conduct a Privacy Impact Assessment at the design stage", including
  "Will data inputs be transferred to companies located overseas (out of
  New Zealand)?"
- "conduct a security risk assessment" including "jurisdictional risk
  (where data is stored or processed outside of New Zealand...)"; prompt
  injection, RAG repository protection, data poisoning, denial of service.
- "good practice to let people know when/where a GenAI system is being used
  ... (e.g. a chatbot on a website)"; the transparency checklist covers
  data jurisdiction and "if and how Māori have been consulted".
- For decisions "about money, health, or the law – a person should always
  be involved".
- Glossary defines "Agentic AI" as a system that "can autonomously perform
  tasks on behalf of a user ... by designing its workflow and using
  available tools".

**(b) Triggers.** Any private-sector New Zealand client.

**(c) Paperwork.** Impact assessment: a "New Zealand: Responsible AI Guidance
mapping" section (the counterpart of the Australian Guidance for AI Adoption
mapping); system card as the model card; the inventory fields map to the
system card and records; questionnaire: security risk assessment and
jurisdictional risk.

**(d) Counsel.** Does voluntary guidance set a standard of care in negligence
or for directors' duties?

### 13.3 Public Service AI Framework and GCDO generative AI guidance

**(a) Status.**
- **Public Service AI Framework**, last updated 29 January 2025 (P,
  operational copy). "Agencies are encouraged to align with the direction
  set by this Framework, however it's not binding." Five OECD-based
  principles (inclusive and sustainable development; human-centred values;
  transparency and explainability, "The Public Service needs to commit to
  transparency in its use of AI"; safety and security; accountability,
  "subject to oversight by accountable humans") and six pillars
  (governance, guardrails, capability, innovation, social licence, global
  voice). A work programme includes a "Public Service AI assurance model
  and toolkit" (S).
- **Interim guidance, July 2023**, joint system leads (P, PDF on
  digital.govt.nz): "Don't use GenAI tools for data classified at SENSITIVE
  or above"; "Don't input personal information to GenAI tools if they are
  external to your environment"; do a PIA with "senior approval ... for any
  testing or use of GenAI" and "copy your PIA to the GCPO"; "Opt out of the
  GenAI tools retaining and using your data for training purposes, if
  possible"; governance should "be Te Tiriti-based".
- **Responsible AI Guidance for the Public Service: GenAI**, sub-pages last
  updated 3 February 2025 (P, operational copy): "keep a register of AI use
  in your agency"; pending the "AI Assurance Regime", "conduct a risk
  assessment" classifying uses as low or high risk; PIAs "for any testing or
  use of GenAI"; "Be transparent to the public about when and how you're
  using AI" and say how the public can challenge outcomes; systems
  "certified and accredited before they're made available to users" (NZISM
  Chapter 4); "sensitive or classified information is not entered in public
  GenAI tools"; contracts requiring vendors to give advance notice of
  material changes; "include an exit strategy".
- **2026.** No published AI Assurance Regime and no agentic AI guidance found
  (S). A 2026 cross-agency survey reports 545 use cases from 59
  organisations (S). A Public Service Commission OIA response of 9 October
  2026 refers to advice on "a central register, inventory or other
  mechanism" for tracking agencies' AI use (S, snippet). No mandatory AI
  register, transparency statement or AI impact assessment like
  Australia's DTA policy was found.

**(b) Triggers.** Client is a Public Service department or departmental
agency (Public Service Act 2020); other state-sector clients may align.
Personal information; a public-facing channel; data classified SENSITIVE or
above.

**(c) Paperwork.** Input pack: PIA with senior approval and, per the 2023
advice, a copy to the Government Chief Privacy Officer; training opt-out
evidence. Questionnaire: classification of data, security risk assessment,
NZISM certification and accreditation, vendor change notice. Records or
system card: the agency's AI register entry and low or high risk
classification. System card: public transparency text and challenge route.
Memo: "non-binding, expected of agencies".

**(d) Counsel.** Is a Vertex AI enterprise endpoint "external to your
environment" in the 2023 sense? Does the contract make the guidance binding
on the supplier?

### 13.4 Algorithm Charter for Aotearoa New Zealand (July 2020)

**(a) Status.** Dated July 2020 (P,
<https://data.govt.nz/assets/data-ethics/algorithm/Algorithm-Charter-2020_Final-English-1.pdf>).
"a commitment by government agencies to carefully manage how algorithms will
be used to strike the right balance between privacy and transparency,
prevent unintended bias and reflect the principles of the Treaty of
Waitangi". Signed by agency chief executives; says nothing about suppliers.
- **Commitments (P):** Transparency ("clearly explaining how decisions are
  informed by algorithms", plain English documentation, information about
  data and processes, how data are collected, secured and stored);
  Partnership ("Embedding a Te Ao Māori perspective in the development and
  use of algorithms consistent with the principles of the Treaty of
  Waitangi"); People (engage and consult those impacted); Data
  ("Understanding its limitations, Identifying and managing bias");
  Privacy, ethics and human rights ("Regularly peer reviewing algorithms to
  assess for unintended consequences"); Human oversight ("Nominating a point
  of contact for public inquiries", "Providing a channel for challenging or
  appealing of decisions informed by algorithms", "Clearly explaining the
  role of humans in decisions").
- **Risk matrix (P):** likelihood (probable, occasional, improbable) by
  impact (low, moderate, high); Low "could be applied", Moderate "should be
  applied", High "must be applied".
- It "cannot fully address important considerations, such as Māori Data
  Sovereignty" (P).
- **Signatories:** 29 as of 31 July 2023 (S, data.govt.nz snippet); MBIE (P)
  and Police (P) confirm they sign; reported examples include Corrections,
  Inland Revenue, DIA, Health, MSD-adjacent agencies and Waka Kotahi (S).
  Independent review by Taylor Fry, December 2021 (S); no 2024–2026 refresh
  found (S); the text is still the July 2020 version.

**(b) Triggers.** Client agency is a signatory (check the current list) and
the agent informs decisions about people; the matrix rating is moderate or
high.

**(c) Paperwork.** Impact assessment: a "New Zealand: Algorithm Charter
inputs" block with the likelihood and impact rating; system card:
plain-English documentation, data handling, the role of humans, the public
contact point and the appeal channel; records: peer review log; memo:
signatory status.

**(d) Counsel.** Is the client still a signatory, and does the contract pass
Charter commitments to the supplier?

### 13.5 Te Tiriti o Waitangi and Māori data sovereignty (as the sources state)

- Algorithm Charter: "reflect the principles of the Treaty of Waitangi";
  the Partnership commitment above; "cannot fully address ... Māori Data
  Sovereignty" (P).
- Public Service AI Framework: lists the "Treaty of Waitangi" in its
  policy context; no other Māori reference (P).
- 2023 interim advice: "Consider also appropriate involvement of your Te
  Tiriti partners"; "Engage Iwi Māori about the impacts of GenAI for Māori
  data and/or outcomes"; consider data status "across 'tapu' or 'noa,' and
  how Māori Data Governance might apply" (P).
- 2025 GenAI guidance, Māori, Pacific Peoples and Ethnic Communities page
  (P): "regular engagement and, where sensible, shared decision-making with
  iwi Māori"; consider whether inputs "may put data sovereignty at risk";
  recommends the "Māori Data Governance Model" published by Te Kāhui
  Raraunga (May 2023, S).
- MBIE business guidance (P): defines Māori data as "digital or digitisable
  data, information or knowledge that is about, from or connected to
  Māori"; distinguish noa and tapu data; "Involve Māori in AI development
  and decision-making that could impact them"; storing data on New Zealand
  servers "may better support data sovereignty than offshore storage".
- AI Strategy (P): Māori see "risks of misappropriation and loss of data
  sovereignty, especially when cultural knowledge is used to train AI
  models without consent".
- OPC (P): "Engage with Māori about potential risks and impacts to the
  taonga of their information"; rule 1 of the Biometric Code weighs
  "cultural impacts on Māori"; the Commissioner takes account of cultural
  perspectives (s 21).

**Triggers.** Data about Māori; services to Māori; te reo Māori or mātauranga
Māori in grounding, evaluation or outputs; a public-sector client.
**Paperwork.** Impact assessment: Māori impact and engagement (owner or
`gap:`), noa or tapu classification of Māori data, offshore storage
rationale. **Counsel.** What, if any, Te Tiriti obligations of the client
pass to a private supplier by contract? Are there iwi data agreements?

### 13.6 Public-sector requirements a supplier meets through the client

- **Cloud First and jurisdictional risk** (GCDO Cloud Jurisdictional Risk
  Guidance, last updated 14 August 2024, P operational copy): Cloud First
  refreshed April 2023; "Agencies must carry out jurisdictional risk
  assessments" for cloud services including free trials and renewals;
  "only store data classified as RESTRICTED or below in a public cloud
  service, whether it's hosted onshore or offshore"; "over time, host
  RESTRICTED information in a New Zealand-based data centre, where a
  suitable onshore service exists".
- **Protective Security Requirements**: Cabinet directed public service
  departments to implement them in 2014; annual self-assessment against "20
  mandatory requirements" (P, NCSC). **NZISM**: version 3.9 (April 2025) is
  reported (S); certification and accreditation before use (GenAI guidance,
  P).
- **Government Procurement Rules, 5th edition**: published 9 October 2025,
  in force from 1 December 2025 (S); no AI-specific rule found.
- **Data Protection and Use Policy**: Cabinet-endorsed 2019 good-practice
  rules for social-sector data, including NGOs and service providers (S).

**Triggers.** Public-sector client using cloud; data above RESTRICTED (a
blocker for public cloud); PSR-mandated agency; social-sector client.
**Paperwork.** Transfer assessment annex: the jurisdictional risk assessment
inputs (hosting region, model processing region, provider jurisdiction,
foreign-law access, consultancy access from Sydney). Questionnaire:
classification ceiling, NZISM controls and accreditation, PSR alignment.
**Counsel.** Is Sydney-based access, or Gemini processing in Australia,
"offshore" for the agency's jurisdictional risk assessment, and does any
onshore service count as "suitable"?

## 14. Other laws an agent can breach

Fork C read the consolidations on legislation.govt.nz by direct download (the
fetch tool got 403) and the OPC code PDFs on 2026-10-26. mbie.govt.nz,
rbnz.govt.nz, fma.govt.nz, nzism.gcsb.govt.nz, digital.govt.nz and
bills.parliament.nz refused automated reads; statements resting on them are S.

### 14.1 Fair Trading Act 1986

**(a)** In force; consolidation as at 1 July 2026 (P).
- s 9: "No person shall, in trade, engage in conduct that is misleading or
  deceptive or is likely to mislead or deceive." Civil remedies only (s 40(1)
  excludes s 9 from the offences).
- s 12A: "A person must not, in trade, make an unsubstantiated
  representation" — one made without "reasonable grounds for the
  representation, irrespective of whether the representation is false or
  misleading" (inserted 17 June 2014). s 12B(1)(c): the court considers "any
  research or other steps taken ... before the person made the
  representation".
- s 13: false or misleading representations about goods and services,
  including (b) services "supplied by any particular person or by any person
  of a particular trade, qualification, or skill" (a bot implying a human
  expert), (e) performance characteristics, (g) price, (i) "the existence,
  exclusion, or effect of any condition, warranty, guarantee, right, or
  remedy, including ... under the Consumer Guarantees Act 1993".
- Unfair contract terms in standard form consumer contracts (s 26A, from 17
  March 2015) and small trade contracts (s 26B, from 16 August 2022); only the
  Commerce Commission applies for a declaration (s 46I); test in s 46L.
- s 3: extends to conduct outside New Zealand "by any person resident or
  carrying on business in New Zealand" relating to supply in New Zealand.
  s 45: conduct of a "director, servant, or agent" is the body corporate's.
- Offences: maximum fine $600,000 for a body corporate (s 40). Uninvited
  direct sales by telephone (s 36K–36M) apply to outbound phone selling above
  $100.
- **Pending: Fair Trading Amendment Bill (Bill 299–1)**, introduced 27 May
  2026, reported back by the Finance and Expenditure Committee on 25
  September 2026 recommending it pass (P); not enacted. It would make s 7,
  ss 10–12, 12A, 13, 26A and 26B "tier 1 civil liability provisions" (s 9 is
  not listed) with a maximum of the greatest of the consideration, three
  times the gain, and "$1 million ... by an individual, or $5 million in any
  other case"; commencement "6 months after Royal assent, with some
  exceptions".
- **Commerce Commission**, "Navigating the rise of AI" (from a webinar of 7
  July 2025, P): "we assess the consumer harms caused by AI through the lens
  of the Fair Trading Act"; "businesses should monitor AI-generated content
  from their business to ensure it is accurate"; cites *Moffatt v Air Canada*
  as "a reminder that companies ... can be liable for the actions of their AI
  tools, even if the AI tool is faulty"; watch for "dark patterns"; do not
  "mislead or oversell AI capability". No New Zealand chatbot decision or
  Commission chatbot enforcement found (S).

**(b)** Consumer-facing agent answering on price, features, eligibility,
refunds or Consumer Guarantees Act rights; generated marketing, reviews or
endorsements; a persona that could be taken for a human or a professional;
performance claims about the agent; standard-form terms; outbound phone
selling; nudging or cancellation friction.

**(c)** System card: capability claims cite M records (s 12A substantiation),
AI disclosure, grounding for price and policy answers, refusal scope.
Impact assessment: consumer harm, vulnerable consumers, dark-pattern review.
Records: substantiation file kept at the time of each claim. Memo: s 9, 12A,
13 and the pending Bill 299 tiers with `checked 2026-10-26`.

**(d)** Is a hallucinated answer the client's own conduct under s 9 or
attributed under s 45? Does a disclaimer cure it, or is an exclusion of
liability for chatbot errors an unfair term (s 46L)? Is the consultancy
"involved in" a contravention?

### 14.2 Human Rights Act 1993 and New Zealand Bill of Rights Act 1990

**(a)** HRA as at 27 November 2025; NZBORA as at 30 August 2022 (P).
- Prohibited grounds (s 21(1)): sex (including pregnancy and childbirth),
  marital status, religious belief, ethical belief, colour, race, ethnic or
  national origins (including nationality or citizenship), disability, age
  (from 16 for employment), political opinion, employment status, family
  status, sexual orientation; extended to relatives and associates and to
  past or suspected grounds (s 21(2)).
- Employment (s 22): unlawful for "an employer, or any person acting or
  purporting to act on behalf of an employer" to refuse to employ, offer
  worse terms, dismiss or subject to detriment on a prohibited ground;
  s 22(2) reaches anyone "procuring employees for any employer"; s 23
  forbids application forms or inquiries that indicate an intention to
  breach s 22.
- Goods and services (s 44), including "banking or insurance or ... grants,
  loans, credit, or finance".
- **Indirect discrimination (s 65):** a neutral practice that "has the
  effect of treating a person or group of persons differently on 1 of the
  prohibited grounds" is unlawful "unless the person ... establishes good
  reason for it".
- Government (Part 1A, from 1 January 2002): acts of the three branches or
  of bodies performing public functions conferred by law breach Part 1A if
  "inconsistent with section 19 of the New Zealand Bill of Rights Act 1990"
  and not justified under s 5, "even if it is authorised or required by an
  enactment" (s 20L). NZBORA s 27(1): natural justice by any public authority
  determining a person's rights.
- Human Rights Commission, "AI and Digital Technologies: A Human Rights and
  Te Tiriti o Waitangi Approach" (P content; release date August 2026, S):
  "The private sector must undertake human rights due diligence"; calls for
  "rights and Tiriti-based impact assessment for digital systems". Advocacy,
  not binding.

**(b)** Screening, ranking or interviewing candidates; promotion, discipline,
rostering or dismissal inputs; triage of access to goods, services, credit or
insurance; proxy features (name, age signals, postcode, language, benefit
status); a public body exercising statutory functions.

**(c)** Impact assessment, "Adverse impact and equality": measured
disparities by s 21 ground where lawful (M records), proxies removed, the s 65
"good reason" facts; for public bodies, the NZBORA s 5 justification inputs
and the s 27 review path. Memo: Part 2 or Part 1A routing.

**(d)** Is the consultancy "acting on behalf of an employer" or "procuring
employees"? What evidence is "good reason" under s 65? Is the client
performing a public function under s 20J and NZBORA s 3?

### 14.3 Harmful Digital Communications Act 2015

**(a)** In force; as at 9 March 2022 (P). Ten communication principles (s 6),
including "should not disclose sensitive personal facts", "should not make a
false allegation", "should not incite or encourage an individual to commit
suicide" and "should not denigrate an individual by reason of his or her
colour, race, ... gender, sexual orientation, or disability". An "online
content host" has a safe harbour for content "posted by a person" if it runs
the 48-hour notice process (ss 23–24). Offence of posting with intent to harm
(s 22). NetSafe is the Approved Agency for two years from 1 July 2026 (P,
Order 2026). The **Deepfake Digital Harm and Exploitation Bill** (Member's
Bill 213–1), introduced 23 October 2025 (P), would extend "intimate visual
recording" to synthesised likenesses in the Crimes Act and HDCA; its later
stages (first reading reported 29 April 2026, committee report due 19 November
2026) are S.

**(b)** Public agent that generates text or images about identifiable people;
self-harm prompts; the client hosts user content or shared outputs; image
generation of real people.

**(c)** System card: content safety mapped to the s 6 principles, self-harm
escalation, real-person image limits. Records: takedown log with 48-hour
timestamps if s 24 is relied on.

**(d)** Is model output "posted by a person" for the safe harbour, or is the
deployer the author?

### 14.4 Unsolicited Electronic Messages Act 2007

**(a)** In force; as at 28 October 2021 (P). A commercial electronic message
(s 6) with a New Zealand link (s 4(2): recipient or device in New Zealand,
".nz" address or "64" number) needs consent: express, inferred from "the
conduct and the business and other relationships", or deemed from a
conspicuously published business address (s 4). The sender bears "the onus of
proof" (s 9(3)). Sender identification valid for 30 days (s 10) and a
functional unsubscribe in the same channel, at no cost (s 11); consent is
withdrawn "5 working days after the day on which the unsubscribe facility was
used" (s 9(2)). **Voice calls are excluded**: "voice calls made using— (i) a
standard telephone service; or (ii) voice-over Internet protocol (IP)", and a
voice call includes "a call that involves a recorded or synthetic voice"
(Schedule cls 1–2). Penalties up to $500,000 for an organisation (s 45);
reaches organisations carrying on business in New Zealand (s 8). DIA
enforces. **No statutory do-not-call register**: the Marketing Association
runs a voluntary Do Not Call service (P for the service; the absence of a
statutory register is S).

**(b)** Outbound commercial SMS, email or instant messages; promotional links
in transactional messages; address harvesting; outbound AI voice calls (outside
UEMA; FTA s 36K and the Privacy Act apply).

**(c)** System card and questionnaire, Outbound channel: consent source and
type per recipient, sender identification, unsubscribe within 5 working days,
no harvesting; voice calls routed to the FTA and Privacy Act rows.

**(d)** Is a mixed service-and-promotion message commercial? How far does
inferred consent reach?

### 14.5 Codes of practice: health, credit, telecommunications

**(a)**
- **Health Information Privacy Code 2020**, in force 1 December 2020;
  Amendment No 2 "comes into force on 1 May 2026" (P), inserting **rule 3A**
  (indirect collection; not for health information collected before 1 May
  2026) and amending rule 12(1)(e). Applies to health agencies listed in
  cl 4(2): providers of health or disability services, in-house occupational
  health units, ACC, training and registration bodies and others. Rules 1–13
  substitute for the IPPs; rule 12 adds (g) a s 30 authorisation.
- **Credit Reporting Privacy Code 2020**, in force 1 December 2020; Amendment
  No 1 in force 1 May 2026 for IPP 3A (P). "This code applies to credit
  reporters"; subscribers are bound through Schedule 3 subscriber
  agreements.
- **Telecommunications Information Privacy Code 2020**, in force 1 December
  2020; amendments in force 8 December 2025 and 1 May 2026 (P). Applies to
  network operators, ISPs and "a call centre which provides call centre
  services on contract to another agency" for subscriber, traffic and
  content information.

**(b)** Health or disability client, or health information in free text for an
occupational health unit; credit reporter client, or the agent reads credit
reports as a subscriber; telco or ISP client, or an AI voice agent run as a
contracted contact centre.

**(c)** Input pack: the code's rules in place of the IPPs in the compliance
check (HIPC rules 3, 3A, 11, 12; CRPC subscriber limits); transfer annex: the
code's rule 12 basis per offshore recipient.

**(d)** Is the client a "health agency" under cl 4(2)? Does an AI contact
centre on contract fall under the TIPC?

### 14.6 Customer and Product Data Act 2025

**(a)** Assent 29 March 2025; in force 30 March 2025 (P). Banking designation
(SL 2025/228) in force 1 December 2025 for ANZ, ASB, BNZ, Westpac and opted-in
deposit takers; Kiwibank data from 1 December 2026; amendments in force 29 May
2026 (P). Accredited requestors keep request and authorisation records "for 5
years" (s 47). Electricity designation, "Open Electricity" from mid-2027, is
S. Applies to overseas agencies carrying on business in New Zealand (s 11).

**(b)** Only if the agent requests customer data through the regime (as or for
an accredited requestor) or works inside a designated bank's data-holder flows.
Otherwise not relevant.

**(c)** Memo: data holder or requestor role; questionnaire: s 112 security;
records: s 47.

**(d)** Does the consultancy need accreditation, or act as a service provider
to an accredited client?

### 14.7 Employment: monitoring, consultation and health and safety

**(a)**
- **Employment Relations Act 2000**, as at 10 July 2026 (P). Good faith
  (s 4(1)). An employer "proposing to make a decision that will, or is
  likely to, have an adverse effect on the continuation of employment" must
  give affected employees "access to information, relevant to the
  continuation of the employees' employment, about the decision" and "an
  opportunity to comment ... before the decision is made" (s 4(1A)(c)).
  Good faith covers consultation on "the effect on employees of changes to
  the employer's business", proposals to contract out work and redundancy
  (s 4(4)). The Employment Relations Amendment Act 2026 (in force 21 February
  2026, P) does not amend s 4.
- **No employee records exemption** in the Privacy Act (text search, P).
  OPC AskUs on monitoring work computers (updated October 2025, P): collect
  only what is necessary, tell staff clearly; "Covert collection is unfair
  unless you have a particularly strong reason for not telling people".
  No statutory workplace surveillance notice period like New South Wales.
- **Health and Safety at Work Act 2015**: a PCBU "must, so far as is
  reasonably practicable, engage with workers" directly affected by a work
  health or safety matter (s 58); health includes mental health.

**(b)** The agent monitors staff communications, productivity, keystrokes or
voice; processes HR, performance or disciplinary files; supports
restructuring or automates roles; biometric time-keeping or voice ID.

**(c)** Input pack: employees as data subjects with full IPP rights, the
monitoring notice and policy, necessity; impact assessment: consultation plan
(ERA s 4, HSWA s 58) as a calendar wait; records: information given to
affected employees before adverse decisions (s 4(1A)(c)).

**(d)** When does s 4(1A)(c) require sharing an agent's output about an
employee? Does introducing the agent need collective consultation?

### 14.8 Incident reporting beyond privacy breaches

**(a)** No general statutory cyber incident reporting duty for private
businesses was found (S); NCSC reporting is voluntary on its page (P).
Government agencies are reported to be required to report cyber security
incidents to the NCSC under the NZISM (S). RBNZ: material cyber incidents
reported within 72 hours of detection, from 8 April 2024, for registered
banks, non-bank deposit takers and insurers (S, Chapman Tripp). FMA: a
standard condition from 1 July 2024 requiring notice "as soon as possible, or
no later than 72 hours" after determining a material incident, for market
services licensees, with similar conditions for financial advice providers and
CoFI institutions (S).

**(b)** Government agency, bank, insurer, deposit taker or FMA licensee client.

**(c)** Questionnaire, Incident notification: the regulator clock beside the
Privacy Act clock, and the consultancy's notice to the client inside it.

**(d)** Is a prompt-injection or harmful-output event a "material incident"?

### 14.9 Financial conduct (CoFI)

**(a)** Financial Markets Conduct Act 2013 Part 6 Subpart 6A (CoFI), in force
31 March 2025 (P): "a financial institution must treat consumers fairly"
(s 446C), including "assisting consumers to make informed decisions" and "not
subjecting consumers to unfair pressure or tactics or undue influence"; it
applies to "any dealings or interactions with a consumer" (s 446D); a written
fair conduct programme covers distribution channels and records (s 446J). The
Financial Markets Conduct Amendment Bill (Bill 135, reported back 30 January
2026) would amend s 446J; not enacted (P). Regulated financial advice to retail
clients is restricted (s 431F). FMA and RBNZ AI publications are research, not
rules (S).

**(b)** Bank, insurer or deposit-taker client; the agent deals with consumers,
complaints or claims; it recommends products.

**(c)** Impact assessment: fair conduct rows; memo: the fair conduct programme
update as a client deliverable; system card: no regulated advice unless
authorised.

**(d)** Does the agent give "regulated financial advice", and under whose
licence?

### 14.10 Mention only

- **Copyright Act 1994**: the author of a computer-generated work is "the
  person by whom the arrangements necessary for the creation of the work are
  undertaken" (s 5(2)(a), P); no 2025–2026 AI copyright decision found (S).
- **Crimes Act 1961 s 216G**: intimate visual recordings do not yet cover
  synthesised images (P); the deepfake bill above would change that.
- **Online Safety (Minimum Age and Child Safety Risk Assessment) Bill**:
  introduced late August 2026, would cover "social AI companions" (S).
- **NCSC-NZ joint guidance "Careful Adoption of Agentic AI Services"** (1 May
  2026, P page): a security baseline for the questionnaire, not law.

## Not verified at a primary source

Re-read these before a reference file relies on them.

**Privacy and the OPC**
- The text of the Biometric Processing Privacy Code itself (only the OPC's
  pages and summary were read), and whether it requires the rule 1
  assessment to be documented.
- The IPP 3A guidance PDF of 16 December 2025 (the web pages were read).
- The OPC model clauses for IPP 12(1)(f) (reported by firms; not opened).
- Whether a government bill on Privacy Act penalties exists (searches found
  none).
- The full PDF of the agentic AI joint guidance.
- Whether Google Cloud's Auckland region is open, and whether any Gemini
  model processes there (the data residency page lists none).

**Government AI policy**
- The text of the July 2024 Cabinet paper and minute and of CAB-25-MIN-0216.
- The canonical digital.govt.nz pages and any 2026 updates, including the AI
  Assurance Regime and any agentic AI guidance.
- The current Algorithm Charter signatory list and any post-2022 change.
- The Public Service Commission OIA response of 9 October 2026 on a central
  AI register.
- NZISM's current version; the Cloud First Cabinet minute; DPUP's mandate;
  the Procurement Rules 5th edition text.
- The Online Safety Bill text and stage.

**Other laws**
- RBNZ's 72-hour material cyber incident reporting and FMA's 72-hour
  standard condition (sites blocked).
- NZISM's mandatory incident reporting for agencies.
- The deepfake bill's stages after introduction.
- The electricity consumer data designation.
- The FTA s 36M cancellation period and s 26C thresholds.
- The Health and Safety at Work Amendment Bill's content.

## Must cover, should cover, mention only

**Must cover.** Every New Zealand pack screens for these.

1. Privacy Act 2020 and the IPPs (1 to 13 and 3A), with the roles: the client
   as agency; the consultancy and Google as s 11 agents unless they use
   information for their own purposes; the s 4(1)(b) question for the
   consultancy.
2. IPP 3A, from 1 May 2026, checked 2026-10-26: one row per indirect source.
3. IPP 12 and s 11 for model processing (no New Zealand region), logs,
   grounding, abuse review and Sydney access, with no prescribed countries.
4. IPP 8 accuracy before use, with evaluation evidence and the review step.
5. Notifiable privacy breaches (s 114, "as soon as practicable", OPC 72
   hours) and the agent contract term.
6. OPC AI guidance (September 2023) as the standard the PIA is measured
   against, built on the OPC PIA toolkit.
7. Fair Trading Act ss 9, 12A and 13 for consumer-facing agents.
8. Public sector clients: the GenAI guidance (PIA, register, risk
   classification, NZISM C&A), the jurisdictional risk assessment and the
   RESTRICTED ceiling.

**Should cover.** Screen for these when the trigger fires.

1. Biometric Processing Privacy Code (voice or face; any emotion or attention
   inference). Promote to must when the trigger fires.
2. Algorithm Charter, for signatory agencies whose agent informs decisions.
3. Human Rights Act ss 21, 22, 44 and 65, and Part 1A with NZBORA for public
   bodies, for agents that decide about people.
4. Health Information Privacy Code (rule 3A from 1 May 2026), for health
   clients; Credit Reporting and Telecommunications codes when their scope
   fits.
5. Employment Relations Act s 4 consultation and the OPC monitoring position,
   for agents touching staff.
6. Unsolicited Electronic Messages Act for outbound text; FTA s 36K for
   outbound phone selling.
7. RBNZ, FMA and NCSC incident clocks, and CoFI fair conduct, for financial
   and government clients.
8. MBIE Responsible AI Guidance mapping in the impact assessment for private
   clients.
9. Te Tiriti and Māori data: Māori impact and engagement whenever the agent
   handles data about Māori or serves Māori, and always for public-sector
   clients.

**Mention only.** One line in the memo, with the date checked.

1. No AI Act: the AI Strategy of July 2025 relies on existing law.
2. No civil penalty regime; the Commissioner's call for penalties, audit
   powers and erasure (28 April 2026); no bill found.
3. Fair Trading Amendment Bill 299 (reported back 25 September 2026; not law).
4. Harmful Digital Communications Act and the deepfake bill (public
   generative agents only).
5. Online Safety (Minimum Age and Child Safety Risk Assessment) Bill
   (companion chatbots; not law).
6. Customer and Product Data Act (only if the agent uses the regime).
7. Copyright Act s 5(2)(a) authorship of computer-generated works.
8. Public Service AI Framework (not binding) and the Ministry for Regulation
   guidance.
9. NCSC-NZ joint agentic AI guidance (1 May 2026) as a security baseline.

## Screening checklist

Each trigger is a fact the brief or design already records. A "yes" adds the
law to the regime screen and a section to the named document. Where a trigger
needs a legal judgement, the line is a `counsel:` item.

| # | Trigger (fact with its ID) | Law | Document → section |
| --- | --- | --- | --- |
| 1 | Personal information about anyone in New Zealand in prompts, tools, memory, logs or evaluation sets | Privacy Act 2020, IPPs | Memo → New Zealand: Privacy Act and IPPs; input pack → Data flows, New Zealand: IPP compliance check |
| 2 | Client established or carrying on business in New Zealand, including public service departments, Crown entities and local authorities | Privacy Act s 4, s 8 | Memo → Jurisdiction screen, Roles |
| 3 | Consultancy staff or systems in Australia hold or access New Zealand data (build, test, trace review, support) | s 11 agent; s 4(1)(b) overseas agency; IPP 5(b) | Memo → Roles (`counsel:`); transfer annex → New Zealand row; questionnaire → provider controls |
| 4 | Model endpoint, ML processing, logs, grounding or abuse review outside New Zealand (always true for Gemini today) | s 11; IPP 12 if any party uses information for its own purposes | Input pack → Recipients and regions, Model provider data use; transfer annex → New Zealand row |
| 5 | Provider terms allow abuse monitoring, service improvement or training on inputs | s 11(3); IPP 10, 11, 12; OPC third-party guidance | Input pack → Model provider data use (`counsel:`) |
| 6 | Agent pulls information about people from third-party systems, partner APIs, web search, or users' uploads naming others, collected from 1 May 2026 | IPP 3A | Input pack → New Zealand: Collection and notice inputs (one row per source, exception rationale) |
| 7 | Agent collects directly from users (chat, voice, forms) | IPPs 1, 3, 4 | Input pack → Collection and notice inputs; system card → AI disclosure and hand-off |
| 8 | Agent output about a person is used, sent or acted on | IPP 8; OPC on automation blindness | Impact assessment → Evaluation (M records); system card → Limits, Human oversight; input pack → IPP 8 row |
| 9 | Re-use of existing customer, staff or case data for grounding, evaluation or tuning | IPP 10; OPC AI guidance | Input pack → Necessity and proportionality (purpose per dataset) |
| 10 | Sessions, memory, vector stores or traces hold information about people | IPPs 6, 7, 9; s 44 (20 working days) | Input pack → Data flows (searchable, correctable), Retention and erasure |
| 11 | Agent assigns or echoes identifiers (IRD, NHI, licence, customer numbers) | IPP 13 | Input pack → People and data categories; output masking contract |
| 12 | Any personal information held | Part 6 notifiable privacy breaches (s 114; OPC 72 hours) | Questionnaire → Incident notification; contract term for the agent's notice |
| 13 | Voice or face verification or identification; emotion, mood, attention or trait inference; categorising by sex, ethnicity or disability | Biometric Processing Privacy Code 2025 rules 1, 3, 10 | Input pack → proportionality (with cultural impacts on Māori), rule 10 check; `counsel_required: yes` |
| 14 | Consumer-facing agent; claims about products, prices, refunds or the agent's own capability | Fair Trading Act ss 9, 12A, 13; Bill 299 (pending) | System card → claims with M records, AI disclosure; impact assessment → consumer harm |
| 15 | Agent screens, ranks or decides about candidates, staff, customers, credit, insurance or services | Human Rights Act ss 21, 22, 44, 65; OPC screening use case; IPP 8 | Impact assessment → Adverse impact and equality; `counsel_required: yes` |
| 16 | Client exercises public functions conferred by law | HRA Part 1A; NZBORA ss 5, 19, 27 | Impact assessment → justification and review path; `counsel_required: yes` |
| 17 | Client is a Public Service department or departmental agency | Public Service AI Framework (not binding); GenAI guidance; PSR; NZISM | Input pack → PIA with senior approval (GCPO copy); records or system card → AI register entry, risk class; questionnaire → NZISM C&A |
| 18 | Public-sector client using cloud; data classified above RESTRICTED | Cloud First jurisdictional risk guidance | Transfer annex → jurisdictional risk inputs; memo → blocker above RESTRICTED |
| 19 | Client agency is an Algorithm Charter signatory and the agent informs decisions about people | Algorithm Charter (risk matrix) | Impact assessment → Algorithm Charter inputs; system card → contact point, appeal channel, role of humans |
| 20 | Data about Māori, services to Māori, te reo Māori or mātauranga Māori in grounding, evaluation or outputs | OPC expectations; Algorithm Charter partnership; GenAI Māori page; MBIE guidance | Impact assessment → Māori impact and engagement; transfer annex → offshore storage rationale |
| 21 | Health or disability client; occupational health unit; health information in free text | Health Information Privacy Code 2020 (rule 3A from 1 May 2026) | Input pack → code rules in place of IPPs; transfer annex → rule 12 |
| 22 | Credit reporter client, or agent reads credit reports as a subscriber | Credit Reporting Privacy Code 2020 | Memo → reporter or subscriber; input pack → subscriber limits |
| 23 | Telco or ISP client, or an AI contact centre run on contract | Telecommunications Information Privacy Code 2020 | Memo → code applicability (`counsel:`) |
| 24 | Agent monitors staff, processes HR files, or supports restructuring | ERA s 4(1A)(c), s 4(4); OPC monitoring; HSWA s 58 | Input pack → monitoring notice; impact assessment → consultation as a calendar wait |
| 25 | Outbound commercial SMS, email or instant messages | UEMA ss 9–11 | System card and questionnaire → Outbound channel |
| 26 | Outbound voice calls, including synthetic voice | Outside UEMA; FTA s 36K–36M; Privacy Act; voluntary Do Not Call | Outbound channel → voice row |
| 27 | Bank, insurer, deposit taker or FMA licensee client | RBNZ and FMA 72-hour clocks (S); CoFI s 446C–446J | Questionnaire → Incident notification; impact assessment → fair conduct |
| 28 | Government agency client | NZISM incident reporting to NCSC (S) | Questionnaire → Incident notification |
| 29 | Public generative agent producing text or images about real people | HDCA s 6 principles; deepfake bill (pending) | System card → content safety |
| 30 | Agent requests customer data through the consumer data right | Customer and Product Data Act 2025 | Memo → role; records → s 47 |

## Checker patterns

**Date check (LEGAL_REF additions).** The current pattern already matches
"Privacy Act", "Code", "Schedule", "Act 19xx/20xx" and "s 123". It misses
the New Zealand principle and code names, so a line such as "IPP 3A applies
from 1 May 2026" passes without a check. Add:

```text
\bIPPs?\s?\d+[A-Z]?\b            IPP 3A, IPP 12, IPPs 1
\bHIPC\b|\bCRPC\b|\bTIPC\b|\bBPPC\b
\brule\s?\d+[A-Z]?\b             rule 3A, rule 10 (codes) — case-insensitive, may need a code word nearby
\bPrivacy Amendment Act\b        (already caught by "Act 2025")
\bUEMA\b|\bHDCA\b|\bNZBORA\b|\bCoFI\b|\bFair Trading\b|\bAlgorithm Charter\b
\bCustomer and Product Data\b
\bNZISM\b|\bPSR\b
```

New Zealand dates a draft is likely to write, each needing `checked`:

| Date in words | Provision |
| --- | --- |
| 1 May 2026 | IPP 3A (Privacy Amendment Act 2025 Part 1); HIPC rule 3A; CRPC, TIPC and Biometric Code IPP 3A amendments |
| 24 September 2025 | Privacy Amendment Act 2025 Part 2 (s 18(3), ss 44, 49, 63) |
| 27 November 2025 | IPP 12(1)(e) replaced; s 120(6) inserted (Statutes Amendment Act 2025) |
| 3 November 2025 | Biometric Processing Privacy Code in force (new processing) |
| 3 August 2026 | Biometric Code applies to processing that began before 3 November 2025 |
| 1 December 2020 | Privacy Act 2020 and the HIPC, CRPC and TIPC in force |
| 31 March 2025 | CoFI (Financial Markets Conduct Act Part 6 Subpart 6A) in force |
| 30 March 2025; 1 December 2025; 1 December 2026 | Customer and Product Data Act; banking designation; Kiwibank data |
| 21 February 2026 | Employment Relations Amendment Act 2026 in force |
| 1 July 2026 | NetSafe appointed Approved Agency under the HDCA |
| 8 April 2024; 1 July 2024 | RBNZ and FMA incident reporting (S) |

**Counsel triggers (COUNSEL_TRIGGERS additions).** The existing lists already
fire on biometrics (including "voiceprint", "emotion recognition",
"speaker verification"), employment, credit, insurance, housing, health and
children. Add:

- public-body clients: `Public Service (?:department|agency)`,
  `departmental agency`, `Crown entit(?:y|ies)`,
  `public function conferred`, `Algorithm Charter signatory`;
- biometrics: `emotion (?:inference|detection|analysis)`,
  `(?:mood|attention|fatigue|alertness) (?:detection|monitoring|inference)`,
  `voice (?:verification|identification|biometrics?)`,
  `biometric categorisation`;
- health care: `Health Information Privacy Code`, `\bHIPC\b`,
  `\bNHI\b` (case-sensitive), `health agency`;
- essential services: `credit report(?:s|ing)?`, `\bCoFI\b` (case-sensitive)
  for consumer financial decisions;
- automated decisions: New Zealand has no automated-decision statute, so no
  phrase; the employment and essential-services phrases cover the cases the
  OPC singles out (job application screening).

Phrases that should **not** trigger: "IPP 3A" or "IPP 12" alone; "Māori";
"Algorithm Charter" without "signatory".

## How New Zealand differs from Australia in ways that change a draft

1. **No exemptions to screen.** Australia's s 6D small business and s 7B(3)
   employee records exemptions have no New Zealand equivalent. Delete the
   turnover row; employees and job applicants get full IPP rights, including
   access to what the agent holds about them.
2. **Agent instead of "effective control".** Australia's use-or-disclosure
   test for overseas cloud comes from OAIC guidance (APP Guidelines 8.14);
   New Zealand's is statutory (s 11), applies wherever the agent is, and
   turns on whether the agent uses information "for its own purposes".
   Write the s 11 facts, not "effective control".
3. **No s 16C liability, but the client stays responsible.** New Zealand has
   no deemed liability for an overseas recipient's breaches. If a recipient
   is a true discloser, IPP 12 sets six grounds; Australia's APP 8.1
   "reasonable steps" plus s 16C does not apply. No country is prescribed in
   either jurisdiction.
4. **No APP 1.7 automated-decision transparency.** Drop the "Automated
   decisions (APP 1.7)" memo table and the APP 1.8 block. The New Zealand
   hooks are IPP 8 (accuracy before use), the OPC's human-review expectation,
   the Human Rights Act and, for signatory agencies, the Algorithm Charter's
   appeal channel and role-of-humans explanation.
5. **Indirect collection notice is new law.** IPP 3A (from 1 May 2026) has no
   APP counterpart beyond APP 5's "reasonable steps"; it needs documented
   exceptions. Australia's APP 5 already covers third-party collection, so
   the Australian inventory row is not enough for New Zealand.
6. **Accuracy is a gate, not a quality duty.** APP 10 requires reasonable
   steps for quality; IPP 8 forbids use or disclosure without them. Cite
   evaluation evidence before any statement that an output is used.
7. **Unique identifiers are their own principle.** IPP 13 has no general APP
   equivalent outside government identifiers (APP 9); add an identifiers row.
8. **Breach clocks differ.** Australia allows up to 30 days to assess (s 26WH)
   then "as soon as practicable"; New Zealand requires notice to the
   Commissioner "as soon as practicable after becoming aware", with the OPC
   wanting 72 hours. A notifiable breach includes loss of access (ransomware).
9. **Penalties are small.** No civil penalties (Australia: up to $50 million
   or 30% of turnover); offences up to $10,000; remedies through the Human
   Rights Review Tribunal. Do not import Australian penalty language.
10. **Biometrics code.** New Zealand's Biometric Code substitutes rules for
    the IPPs and bans emotion and trait inference outright, subject to narrow
    exceptions; Australia relies on APP 3.3 consent and determinations.
11. **Government clients carry guidance and a cloud rule, not a mandatory AI
    assessment.** No DTA-style AI impact assessment, transparency statement
    deadline or NSW-style platform. Name instead: the agency's PIA (copied to
    the GCPO per the 2023 advice), its AI register entry, NZISM certification
    and accreditation, the jurisdictional risk assessment and, for
    signatories, the Algorithm Charter. Writing "DTA" or "APP" in a New
    Zealand section is wrong.
12. **Te Tiriti and Māori data.** No Australian counterpart in the pack.
    New Zealand sections add Māori impact and engagement, and the Biometric
    Code's "cultural impacts on Māori".
13. **No workplace surveillance notice period.** No NSW-style 14-day notice;
    the New Zealand duties are fair collection (IPP 4), notice (IPP 3) and
    good-faith consultation (ERA s 4). The calendar wait becomes consultation,
    not a statutory notice.
14. **Outbound messaging.** UEMA: unsubscribe effective within 5 working
    days, voice excluded as in Australia's Spam Act; but New Zealand has no
    statutory Do Not Call Register and no telemarketing standard.
15. **Terms to use.** "agency" (not "APP entity" or "controller"), "agent"
    (s 11), "personal information", "IPP", "notifiable privacy breach",
    "serious harm", "Privacy Commissioner" or "OPC", "foreign person or
    entity", "privacy officer". New Zealand has no statutory "sensitive
    information" category; the OPC and the s 113 factors speak of information
    "sensitive in nature".
