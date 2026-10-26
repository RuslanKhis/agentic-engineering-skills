---
document: regulatory-memo
system: <system name>
version: <design revision or build screened>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk, nz, sg, ca>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <client counsel or AI governance lead>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md>
---

# Regulatory memo: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for <client>'s counsel. It records which regimes the jurisdiction
screen found in scope, the facts the design records, and the provisions that
appear relevant in each regime: the EU AI Act classification where the EU is
in scope, and a screen of the existing laws that apply in Australia, the
United States, the United Kingdom, New Zealand, Singapore and Canada, none of
which has an AI Act or assigns a risk tier. Conclusions are proposals for
counsel; not legal advice.

<!-- Keep only the regime sections, and the regime bullets inside shared
sections (Summary, Roles, Applicable dates), whose code is in jurisdictions,
in the order Australia, United States, EU, United Kingdom, New Zealand,
Singapore, Canada. The screen table keeps all seven rows. When Australia is
in scope only through the consultancy's own handling, scope the Australian
sections to that handling and say so. Keep "Australia: Government client"
only for a Commonwealth or NSW agency client. Delete this comment. -->

## Summary

- **Regimes in scope:** <Australia, United States, EU, United Kingdom, New Zealand, Singapore, Canada: those in jurisdictions> (Jurisdiction screen below; counsel: <confirm the screen>).
- **Proposed EU classification, if the EU is in scope:** <prohibited / high-risk (Annex III point) / Article 6(3) derogation argued / transparency obligations only / minimal risk> (counsel: <confirm>).
- **Main obligations in the other regimes:** <one line per regime: for example APP 1.7 privacy-policy entries from 10 December 2026; CPPA risk assessment; UK GDPR Article 22C safeguards> (<IDs>; checked <YYYY-MM-DD>).
- **Proposed roles:** <one line per regime> (Roles below; counsel: <confirm>).
- **Blocking questions:** counsel: <count> questions, listed under Questions for counsel.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | <yes / no / yes (gap: fact missing)> | <client establishment, data subjects, consultancy staff access> (<IDs or source:>) | <reason, or n/a: why not> |
| United States | <yes / no / yes (gap:)> | <US client, US residents, federal client> (<IDs or source:>) | <reason, or n/a: why not> |
| EU | <yes / no / yes (gap:)> | <EU establishment, people in the EU, EU market or output use> (<IDs or source:>) | <reason, or n/a: why not> |
| United Kingdom | <yes / no / yes (gap:)> | <UK establishment, people in the UK, central government client> (<IDs or source:>) | <reason, or n/a: why not> |
| New Zealand | <yes / no / yes (gap:)> | <NZ client or agency, people in New Zealand, consultancy access from Australia to NZ data> (<IDs or source:>) | <reason, or n/a: why not> |
| Singapore | <yes / no / yes (gap:)> | <Singapore client, people in Singapore, public agency client> (<IDs or source:>) | <reason, or n/a: why not> |
| Canada | <yes / no / yes (gap:)> | <Canadian client, people in Canada and their province, Quebec enterprise, federal client> (<IDs or source:>) | <reason, or n/a: why not> |

- **Processing locations:** <hosting region; model processing region from the model page; logs; grounding; abuse monitoring; telemetry; consultancy access from Australia> (<D IDs>, source: <model page>, <YYYY-MM-DD>).
- **Government client:** <private client; Commonwealth agency; NSW agency; other state; NZ public service; Singapore public agency; Canadian federal or provincial body> (<source: or gap:>).

## System and intended purpose

- **What it does:** <one or two sentences> (<R/C IDs>).
- **Who uses it and who it affects:** <users; people its outputs are about> (<docs/discovery/<topic>.md §n, R IDs>).
- **What the model decides and what code or people decide:** <split> (<D/C IDs>).
- **Effects it can cause:** <reads, drafts, writes, messages, decisions about people> (<C IDs>).
- **Human review of decisions about people:** <where a person decides, share reviewed, override rate> (<C ID, M ID or gap:>).

## Roles

- **Facts:** <who commissions it; whose name it runs under; who changes its purpose; who operates it; what the agency supplies; who handles personal data during build and support> (<D IDs, source:>).
- **Australia, Privacy Act:** <client APP entity? consultancy APP entity in its own right? small business, employee records or State contract exemptions; no processor category in Australian law today> (counsel: <confirm>).
- **United States:** <CCPA business and service provider; state-law controller and processor; Colorado developer and deployer; FEHA agent of the employer; HIPAA business associate> (counsel: <confirm>).
- **EU AI Act:** <client provider and deployer; agency developer under contract, provider only if it markets the system under its own name; Article 25 triggers; Article 25(4) agreement if high-risk> (<D/G IDs>; counsel: <confirm>).
- **EU GDPR and UK GDPR, separately:** <controller, processors, sub-processors> (privacy-impact-input-pack.md; counsel: <confirm>).
- **New Zealand, Privacy Act 2020:** <client as agency; consultancy and Google as s 11 agents if they hold only on the client's behalf; any use "for its own purposes"; whether the consultancy is an overseas agency carrying on business in New Zealand (s 4(1)(b)); the client's privacy officer> (counsel: <confirm>).
- **Singapore, PDPA:** <client as organisation (or a public agency outside the PDPA); consultancy as data intermediary under a written contract; Google as model provider; uses that would break the intermediary role; the client's DPO and business contact> (counsel: <confirm>).
- **Canada:** <which law governs each flow (PIPEDA, Quebec, Alberta, BC); client as the organisation responsible for information under its control; consultancy acting only for the client (a transfer for processing) or for its own purposes too; Quebec person in charge (s 3.1)> (counsel: <confirm>).

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed, and obligations come from the laws screened here (checked <YYYY-MM-DD>).
- **APPs engaged:** <APP 1, 3, 5, 6, 8, 10, 11, 12 and 13, each with the fact that engages it> (privacy-impact-input-pack.md; <IDs>).
- **Overseas disclosure (APP 8, s 16C):** <model endpoint and processing region, logs, grounding, support or abuse review outside Australia; use or disclosure facts> (<D IDs>; counsel: <use or disclosure>).
- **Notifiable data breaches:** <who assesses within 30 days and who notifies; contract flow-down> (security-questionnaire.md; counsel: <which entity notifies>).
- **Pending, not law:** <tranche 2 exposure draft; Children's Online Privacy Code> (checked <YYYY-MM-DD>).

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| <decision, or n/a: no decision about a person> | <which> | <contract ID; M ID or gap:> | <effect> | <kinds> | <C/M IDs; counsel: significantly affects?> |

- **Privacy policy inputs (APP 1.8):** system-card.md, Automated-decision disclosure (<C ID>).

## Australia: Sector, state and government AI policy

- **Sector laws:** <APRA CPS 234 and CPS 230; health records and My Health Records s 77; workplace surveillance notice; Spam Act and telemarketing; Australian Consumer Law ss 18 and 29; or n/a: with the reason> (<IDs>; counsel: <question>).
- **Government AI policy:** <DTA policy and AI impact assessment for a Commonwealth client; state framework; or n/a: private client> (<IDs>; checked <YYYY-MM-DD>).

## Australia: Government client (Commonwealth or NSW agency)

<!-- Keep this section only when the client is a non-corporate Commonwealth
entity or a NSW public sector agency; delete it otherwise, with this
comment. The agency's officers complete the official forms; the pack drafts
answers in government-form-answers-<form>.md. -->

- **Client and policy:** <non-corporate Commonwealth entity under the DTA Policy for the responsible use of AI in government v2.1; or NSW agency under DCS-2026-02 and the NSW AI Operational Policy v1.1> (<source:>; checked <YYYY-MM-DD>).
- **Official forms and where the pack's answers are:** <DTA AI impact assessment tool, transparency statement inputs, use-case register row, agentic addendum; or AIAF Platform registration and AIAF assessment, IPC AI PIA guide> (government-form-answers-<form>.md; agency: <who completes and approves>).
- **Review committee:** <Commonwealth AI Review Committee for residual high risk or highly sensitive, novel or complex use cases; or NSW AI Review Committee referral within 5 business days of completing the AIAF for a high or critical band> (agency: <band>; counsel: <referral needed?>; wait <W ID or gap:>).
- **Privacy Act roles:** <Commonwealth: s 95B contract terms and the Agencies Privacy Code PIA; NSW: the consultancy's acts for a State contract fall under s 7B(5), its other handling stays under the APPs> (counsel: <does s 7B(5) cover every act?>).
- **NSW privacy:** <PPIP Act IPPs and s 19(2) for any recipient outside NSW, including other Australian states; HRIP Act and HPP 14 for health information; Part 6A mandatory data breach notification> (privacy-impact-input-pack.md; counsel: <use or disclosure; which s 19(2) ground>).
- **NSW access and records:** <GIPA contracts register entry for a contract of $150,000 or more and s 121 if the agent serves the public for the agency; prompts, outputs and metadata as State records under the State Records Act 1998> (agency: <register and disposal authority>; counsel: <s 121>).
- **NSW security:** <NSW Cyber Security Policy: Essential Eight Maturity Level One baseline; cyber incidents reported within 24 hours of detection and classification> (security-questionnaire.md; <SB IDs>).
- **NSW contract AI clauses:** <ICTA clause 6.11: the AI systems listed in the Order Form (model IDs), the model-change notice period (six months by default) against the pinned model's retirement date, AI system records, data location> (<D ID>; source: <model page or lifecycle table>, <YYYY-MM-DD>; gap: <retirement inside the notice window>; counsel: <notice period and Order Form terms>).

## United States: Preemption status and FTC claims

- **Federal preemption:** no federal statute preempts the state laws screened below; <court orders staying a state law, for example Colorado> (checked <YYYY-MM-DD>).
- **FTC Act Section 5:** <public claims the client will make about the agent and the M records that substantiate them> (<M IDs or gap:>).

## United States: Automated decisions and state AI laws

- **CPPA ADMT and risk assessment:** <is the client a CCPA business; does the output replace or substantially replace a human in a significant decision; the three-part human review facts> (<C/M IDs>; counsel: <ADMT or not>).
- **Colorado SB 26-189 and other state AI laws:** <consequential decisions about state residents; enforcement status> (<IDs>; checked <YYYY-MM-DD>).
- **Chatbot and companion laws:** <consumer chat disclosure duties; whether a persona or memory brings companion laws in> (<C IDs>; counsel: <exclusion holds?>).

## United States: Privacy, sector and employment laws

- **State privacy laws:** <states whose thresholds the client meets; profiling opt-out; data protection assessment; sensitive-data consent> (<IDs>; counsel: <thresholds>).
- **Employment AI rules:** <NYC Local Law 144, Illinois, California FEHA, Title VII and ADA, or n/a: no employment use> (<IDs>; counsel: <question>).
- **Sector statutes:** <HIPAA, GLBA, FCRA, ECOA Regulation B, TCPA, COPPA, or n/a: with the reason> (<IDs>).

## EU: Prohibited practices (Article 5)

| Point | Applies? | Facts | Evidence |
| --- | --- | --- | --- |
| (a) manipulation, (b) exploiting vulnerabilities | <no / counsel:> | <why> | <C IDs> |
| (ba), (bb) generated intimate or abuse material | <no / counsel:> | <why> | <C/D IDs> |
| (c) social scoring, (d) crime prediction by profiling | <no / counsel:> | <why> | <C IDs> |
| (e) facial scraping, (g) biometric categorisation, (h) real-time remote identification | <no / counsel:> | <why> | <D IDs> |
| (f) emotion inference at work or in education | <no / counsel:> | <why> | <C/D IDs> |

## EU: High-risk classification (Article 6 and Annex III)

- **Annex I product:** <no / which product legislation> (<D ID or assumption:>).
- **Annex III area touched:** <none / point and area> (<R/C IDs>).
- **Profiling of natural persons:** <yes / no, with facts> (<C/D IDs>; counsel: <confirm>).
- **Article 6(3) derogation facts, if argued:** <narrow procedural / improves completed human work / detects patterns under human review / preparatory; and why it does not materially influence the outcome> (<C/D IDs>; counsel: <decide>).
- **If high-risk:** <what Chapter III requires of the provider and Article 26 of the deployer; FRIA under Article 27 if the deployer is in scope (not Annex III point 2), notified to the market surveillance authority (27(3)); Article 86 explanation; the plan goals or gaps for each> (<G IDs or gap:>).
- **Article 25(4) agreement (if high-risk):** <what the agency supplies; whether the written agreement exists> (<contract reference or gap:>; counsel: <confirm>).

## EU: Transparency obligations (Article 50)

| Paragraph | Applies? | How the design meets it | Evidence |
| --- | --- | --- | --- |
| 50(1) told they interact with AI | <yes / no / n/a:> | <disclosure; for agents, also on whose behalf it acts> | <C ID, G/A> |
| 50(2) machine-readable marking of generated content | <yes / no / counsel:> | <marking decision, or exception relied on: standard editing, no substantial alteration, B2B (guidelines para 87)> | <D ID> |
| 50(3) emotion recognition or biometric categorisation notice | <yes / n/a:> | <notice> | <C ID> |
| 50(4) deepfakes or public-interest text | <yes / n/a:> | <disclosure or editorial review> | <C ID> |

## EU: General-purpose AI model

- **Model and provider:** <model ID, model provider> (<D ID>).
- **Obligations under Articles 53 and 55:** sit with the model provider; <client> relies on its documentation (<source:>, counsel: <confirm>).
- **Fine-tuning or modification:** <none / what> (<D ID>; counsel: <if any>).
- **Downstream modification compute:** <none / compute used versus one third of the original> (<D ID>; counsel: <if any>).

## EU: Other regimes

- <GDPR Article 22 (privacy-impact-input-pack.md), Product Liability Directive, Cyber Resilience Act, NIS2, DORA, MDR, Data Act, DSA: each n/a: with its reason, or counsel: with the facts> (<IDs>).

## United Kingdom: UK GDPR and automated decisions

- **No AI-specific statute:** the UK has no AI Act; the regimes below apply (checked <YYYY-MM-DD>).
- **Regulator:** the Information Commission (formerly the ICO) (checked <YYYY-MM-DD>).
- **Significant decisions (Articles 22A to 22D):** <does an output decide with no meaningful human involvement; special category data; the four Article 22C safeguards> (privacy-impact-input-pack.md; <C/M IDs>; counsel: <significant? meaningful?>).
- **Restricted transfers:** <consultancy access from Australia; endpoints outside the UK; mechanism> (transfer-assessment.md; counsel: <data protection test met?>).

## United Kingdom: Equality, consumer, online safety and sector

- **Equality Act 2010:** <decisions about people; protected characteristics or proxies; public sector equality duty for a public body> (impact-assessment.md; counsel: <justified?>).
- **Consumer law, Online Safety Act, FCA, ATRS:** <each applies or n/a: with the reason> (<IDs>; counsel: <question>).

## New Zealand: Privacy Act and IPPs

- **No AI-specific statute:** New Zealand has no AI Act; the July 2025 AI Strategy relies on existing law (checked <YYYY-MM-DD>).
- **IPPs engaged:** <IPPs 1 to 4 collection, 3A indirect collection, 5 security, 6 and 7 access and correction, 8 accuracy before use, 9 to 11 retention, use and disclosure, 12 cross-border, 13 unique identifiers, each with the fact that engages it> (privacy-impact-input-pack.md; <IDs>).
- **Offshore processing (s 11 and IPP 12):** <model processing outside New Zealand; logs, grounding, abuse review; consultancy access from Australia; whether any party uses information for its own purposes> (transfer-assessment.md; <D IDs>; counsel: <agent or foreign recipient>).
- **Notifiable privacy breaches:** <who notifies the Commissioner as soon as practicable; the agent's contract duty to tell the client> (security-questionnaire.md; counsel: <serious harm>).
- **Biometric Processing Privacy Code:** <voice or face verification, emotion or trait inference, or n/a: none> (<C IDs>; counsel: <rule 10>).

## New Zealand: Sector, consumer and government AI policy

- **Consumer and human rights law:** <Fair Trading Act ss 9, 12A and 13 for consumer claims; Human Rights Act ss 21, 22, 44 and 65 for decisions about people; or n/a: with the reason> (<IDs>; counsel: <question>).
- **Sector codes and clocks:** <Health Information Privacy Code, Credit Reporting or Telecommunications code; RBNZ or FMA incident reporting; or n/a: with the reason> (<IDs>).
- **Government client:** <Public Service GenAI guidance (PIA, AI register, risk classification, NZISM certification and accreditation); Cloud First jurisdictional risk assessment and the RESTRICTED ceiling; Algorithm Charter for signatories; or n/a: private client, MBIE Responsible AI Guidance as voluntary> (<IDs>; checked <YYYY-MM-DD>).
- **Māori data and engagement:** <data about Māori, services to Māori, te reo Māori in grounding or outputs; engagement owner> (<IDs or gap:>).

## Singapore: PDPA and roles

- **No AI-specific statute:** Singapore has no AI Act (MDDI written answer, 7 July 2026; checked <YYYY-MM-DD>).
- **Consent or exception per purpose:** <consent, deemed consent (conduct, contractual necessity, notification) or the business improvement, research or legitimate interests exception, each with its kept assessment> (privacy-impact-input-pack.md; counsel: <basis per purpose>).
- **Transfer Limitation Obligation:** <the client's duty for every transfer out of Singapore, including those its data intermediaries make and consultancy access from Australia> (transfer-assessment.md; counsel: <mechanism>).
- **Data breach notification:** <data intermediary to client without undue delay; client assessment; PDPC within 3 calendar days of determining a breach notifiable> (security-questionnaire.md; counsel: <who leads>).
- **Penalty cap and pending law:** <the cap with its date; data portability not in force> (checked <YYYY-MM-DD>).

## Singapore: AI governance frameworks

- **Voluntary frameworks:** <IMDA Model AI Governance Framework for Agentic AI v1.5; Transparency Guidelines for Generative AI Chatbots for external chat agents; the starter kits; PDPC AI guidelines of 1 March 2024 and 20 July 2026> (impact-assessment.md; system-card.md; checked <YYYY-MM-DD>).

## Singapore: Sector and employment

- **Sector rules:** <MAS AI risk management guidelines, FEAT, TRM Notice and Notice 658 for financial clients; AIHGle 2.0 and HSA for health; Cybersecurity Act for CII owners; or n/a: with the reason> (<IDs>; checked <YYYY-MM-DD>).
- **Employment:** <Tripartite Guidelines now; Workplace Fairness Act expected end-2027 (MOM target, not gazetted); or n/a: no employment use> (<IDs>; counsel: <question>).
- **Public agency client:** <outside the PDPA; the consultancy's PDPA status; s 26E breach notice to the agency; or n/a: private client> (<IDs>; counsel: <question>).

## Canada: Privacy laws and roles

- **No AI-specific statute:** Canada has no AI Act; the Artificial Intelligence and Data Act died with Bill C-27, and Bill C-36 is not law (checked <YYYY-MM-DD>).
- **Which law governs each flow:** <PIPEDA, Quebec's private sector Act (Law 25), Alberta PIPA, BC PIPA, by flow; employee data at federal works, in Quebec, Alberta and BC> (<IDs>; counsel: <which law>).
- **Consent and appropriate purposes:** <meaningful consent (s 6.1), the s 5(3) reasonable-person test, express consent for sensitive information> (privacy-impact-input-pack.md; counsel: <implied or express>).
- **Cross-border and out-of-Quebec flows:** <PIPEDA contract and foreign-access notice; Alberta country list (s 6(2)) and notice (s 13.1); Quebec s 17 PIA and written agreement before any flow leaves Quebec> (transfer-assessment.md; counsel: <adequate protection>).
- **Breach clocks and records:** <PIPEDA as soon as feasible and a 24-month record of every breach; Quebec CAI notice and incident register; Alberta without unreasonable delay; BC none> (security-questionnaire.md).

## Canada: Automated decisions

| Decision the agent touches | Exclusive automation (Quebec s 12.1) | Review route and measured share | Explanation the design can produce | Evidence |
| --- | --- | --- | --- | --- |
| <decision, or n/a: no decision about a person> | <which, Quebec s 12.1> | <contract ID; M ID or gap:> | <information used, reasons and principal factors> | <C/M IDs; counsel: does s 12.1 apply?> |

- **Federal client:** <Directive on Automated Decision-Making and the AIA level, or n/a: not a federal institution> (impact-assessment.md; counsel: <administrative decision? level?>).

## Canada: Employment, sector and government AI policy

- **Employment:** <Ontario job-posting AI disclosure for employers with 25 or more employees; Ontario electronic monitoring policy; human rights codes; or n/a: no employment use> (<IDs>; checked <YYYY-MM-DD>; counsel: <question>).
- **Sector and consumer:** <PHIPA and other health laws; CASL for outbound messages; Competition Act claims; or n/a: with the reason> (<IDs>).
- **Government client:** <federal generative AI guide and GC AI Register; Ontario Responsible Use of AI Directive; or n/a: private client> (<IDs>; checked <YYYY-MM-DD>).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| <regime> | <obligation> | <date in words> (<provision>, checked <YYYY-MM-DD>) | <why it matters; plan goal> |

- **AI literacy (EU AI Act Article 4) and staff training:** <training and guidance for users> (<goal ID or gap:>).

## Questions for counsel

- counsel: <question>; regime <regime>; facts at <IDs>; needed before <goal or wait ID>.

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
