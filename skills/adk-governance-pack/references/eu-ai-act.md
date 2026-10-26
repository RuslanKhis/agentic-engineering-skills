# EU AI Act classification

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `eu` in
scope and you are writing the EU sections of the regulatory memo or the
proof-of-concept note. The EU sections classify the system the design
describes under the AI Act. They do not decide the law: they give counsel
the facts, the provisions that look relevant and the questions only counsel
can settle. GDPR material (Article 22, transfers, the DPIA) is in
[privacy and records](privacy-and-records.md).

Every provision below was read in the Official Journal text on 26 October
2026: Regulation (EU) 2024/1689 (the AI Act, OJ L 12.7.2024,
<https://eur-lex.europa.eu/eli/reg/2024/1689/oj>) as amended by Regulation
(EU) 2026/1744 (the Digital Omnibus on AI, OJ L 24.7.2026, in force 27 July
2026, <https://eur-lex.europa.eu/eli/reg/2026/1744/oj>). No consolidated
version was read. When a draft states a provision or a date, it carries
`checked <date>` with the day the drafter last confirmed it; copy
`checked 2026-10-26` only while this file is the newest check, and re-check
at the source when the checker warns that the date is old.

## Work in this order

1. **Is it an AI system?** Article 3(1). An ADK agent built on a Gemini
   model infers outputs from inputs and almost always is. The Commission's
   non-binding guidelines on the definition (6 February 2025) help in edge
   cases such as a rules engine with one model call.
2. **Who is the provider and who the deployer?** See [Roles](#roles).
3. **Prohibited practice?** Article 5. Stop and escalate if any applies.
4. **High-risk?** Article 6 with Annex I (product safety) and Annex III.
5. **Transparency?** Article 50, which applies whether or not the system
   is high-risk.
6. **General-purpose AI model?** Usually the model provider's duty, not
   the client's.
7. **AI literacy and dates.** Article 4 and the applicability table.

## Roles

- **Provider** (Article 3(3)): develops an AI system, or has one developed,
  and places it on the market or puts it into service under its own name
  or trademark.
- **Deployer** (Article 3(4)): uses an AI system under its authority in a
  professional activity.

In agency work the usual facts are: the client commissions the system and
runs it under its own name for its own staff or customers, so the client is
both provider (it "has it developed") and deployer, and the agency builds
it under contract. The agency becomes a provider when it places the system
on the market under its own name: a product it sells or reuses across
clients. Article 25(1) makes a deployer or other party the provider of a
high-risk system when it puts its name on it, substantially modifies it, or
changes the intended purpose of a non-high-risk system so that it becomes
high-risk. Since the Omnibus, Article 25(2) also says what the original
provider must hand over in that case (documentation, known limits and failure
modes, targeted technical access), unless it clearly specified that its
system is not to be changed into a high-risk system. New Article 25(4)
requires the provider of a high-risk system and any third party that
supplies "an AI system, AI model, tools, services, components, or
processes" used in it to agree in writing the information, technical
access and assistance the provider needs. Article 99(4)(da) makes 25(2)
and 25(4) finable. An agency building a high-risk system for a client
is such a third party. State the facts (who commissions, whose name, who
changes the purpose, what the agency supplies) with their IDs and write the
role and the 25(4) agreement as `counsel:` to confirm; a contract that
assigns the role differently is counsel's to read.

Under GDPR the same facts usually make the client controller, the agency a
processor while it touches personal data during build or support, and the
cloud provider a processor under the client's agreement. Keep the two
regimes apart in the memo: an AI Act provider is not automatically a GDPR
controller.

## Prohibited practices (Article 5)

Applies since 2 February 2025; points (ba) and (bb) since the Omnibus apply
from 2 December 2026. Article 5(1) prohibits:

| Point | Practice | Where an agent could get near it |
| --- | --- | --- |
| (a) | Subliminal, purposefully manipulative or deceptive techniques that materially distort behaviour and cause significant harm | Sales or retention agents tuned to pressure people |
| (b) | Exploiting vulnerabilities due to age, disability or a social or economic situation | Debt collection, offers to vulnerable customers |
| (ba), (bb) | Generating realistic non-consensual intimate material of an identifiable person, or child sexual abuse material | Any open image or video generation. Placing on the market is banned only where this is the intended purpose, or a reasonably foreseeable and reproducible outcome without adequate safeguards (Art 5(1a)); a deployer's use is banned when it uses the system for that purpose. |
| (c) | Social scoring leading to detrimental or disproportionate treatment | Scoring customers or staff across unrelated contexts |
| (d) | Predicting that a person will commit a crime based solely on profiling or personality traits | Fraud or risk scoring of individuals |
| (e) | Untargeted scraping of facial images to build recognition databases | Image-collecting tools |
| (f) | Inferring emotions in the workplace or education, except for medical or safety reasons | Sentiment or emotion scoring of employees' calls, chats or video; student engagement scoring |
| (g) | Biometric categorisation to infer race, political opinions, trade union membership, religious beliefs, sex life or sexual orientation | Photo or voice analysis |
| (h) | Real-time remote biometric identification in public spaces for law enforcement (narrow exceptions) | Rare in agency work |

Point (f) is the one agency projects hit most often: a contact-centre agent
that scores the *employee's* emotion or stress is prohibited, while scoring
customer sentiment is not under (f) but may be emotion recognition under
Article 50(3). The Commission's guidelines on prohibited practices (4
February 2025, non-binding) give examples. Any plausible match sets
`counsel_required: yes` and blocks the production goal.

## High-risk (Article 6, Annex III)

A system is high-risk when it is a safety component of, or is, a product
under Annex I legislation that needs third-party conformity assessment
(medical devices, toys, lifts and others; machinery moved to Section B
under the Omnibus; rare for agency agents). Since the Omnibus, Article
6(1a) says systems used solely for non-safety user assistance,
performance optimisation, service efficiency, automation, convenience
or quality control are not safety components. A system is also high-risk
when it falls in an Annex III area:

| Annex III point | Area | Agent examples that land here |
| --- | --- | --- |
| 1 | Biometrics (remote identification, categorisation, emotion recognition) | Voice or face analysis of people |
| 2 | Critical infrastructure safety components (digital infrastructure, road traffic, water, gas, heating, electricity) | Agents operating utility or network controls |
| 3 | Education and vocational training (admission, assessing learning outcomes, steering learning, proctoring) | Admissions triage, essay grading, exam monitoring |
| 4 | Employment, workers' management, access to self-employment (recruitment, screening and ranking applications, evaluating candidates; promotion, termination, task allocation by behaviour or traits, monitoring and evaluating performance) | CV screening and ranking, interview scoring, performance reviews, shift allocation by traits |
| 5 | Essential private and public services (public benefits eligibility, creditworthiness and credit scoring except fraud detection, life and health insurance risk and pricing, emergency call triage and dispatch) | Loan pre-qualification, claims pricing, benefits eligibility assistants |
| 6 | Law enforcement | Rare in agency work |
| 7 | Migration, asylum and border control | Visa or asylum application assistants |
| 8 | Administration of justice and democratic processes (assisting judicial authorities or alternative dispute resolution; influencing elections or voting behaviour) | Legal research for courts, political campaigning tools |

**Article 6(3) derogation.** An Annex III system is not high-risk when it
does not pose a significant risk of harm to health, safety or fundamental
rights, including by not materially influencing the outcome of decisions,
and it meets one condition: (a) a narrow procedural task; (b) improving the
result of a completed human activity; (c) detecting decision patterns or
deviations without replacing or influencing the human assessment absent
proper review; or (d) a preparatory task. **A system that profiles natural
persons is always high-risk.** A provider relying on 6(3) documents the
assessment before placing the system on the market (Article 6(4)) and still
registers it (Article 49(2)), with the shorter Annex VIII
Section B the Omnibus introduced. The Commission's guidelines on
classification (Article 6(5)) were still a draft on 26 October 2026:
published for consultation 19 May 2026, targeted consultation closed 23
July 2026. Cite them as draft
(<https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems>).

Write the derogation argument as facts with IDs (for a ranked shortlist:
the ranking is deterministic over extracted criteria (D-ID), a recruiter
reviews every shortlisted candidate (C-ID)) and leave the conclusion to
counsel. "A human reviews it" does not by itself remove material influence;
ranking people is profiling in most readings.

**What follows from high-risk** (for counsel and the plan; the pack does
not produce these): the provider's risk management, data governance,
technical documentation, logging, transparency to deployers, human
oversight, accuracy and robustness, quality management, conformity
assessment and registration (Chapter III Sections 2 and 3). The deployer
uses it according to the instructions, assigns competent human oversight,
keeps logs at least six months, informs workers' representatives before
using it at work, informs people subject to its decisions, and uses the
provider's information for its DPIA (Article 26).

A fundamental rights impact assessment (Article 27) is required, before
first use, of deployers of Annex III systems other than point 2 that are
bodies governed by public law or private entities providing public
services, and of any deployer of Annex III points 5(b) (credit) and 5(c)
(life and health insurance). The deployer notifies the market
surveillance authority of the results on the AI Office template
(Article 27(3)); the template is not yet published. Article 27 applies
with the Annex III obligations from 2 December 2027 (Art. 113(c),
checked 2026-10-26). Since the Omnibus, Article 27(4) lets the FRIA
cross-reference or include the relevant parts of the GDPR DPIA, so the
[privacy impact input pack](privacy-and-records.md) is written to be cited by
section, and the impact assessment carries the FRIA crosswalk (Article
27(1)(a) to (f) to pack sections).

Article 4a (added by the Omnibus) lets providers of high-risk systems
(4a(1)), and providers and deployers of other AI systems and deployers
of high-risk systems (4a(2)), exceptionally process special categories
of personal data where strictly necessary to detect and correct bias.
All of conditions (a) to (f) apply: other data, including synthetic or
anonymised data, would not do; re-use limits and pseudonymisation;
access controls; no transmission to others; deletion once the bias is
corrected; and the records of processing state why it was strictly
necessary. It applies in addition to the GDPR, not instead of it, and
imposes no duty to run such checks. A bias-monitoring contract such as
an adverse-impact check names it as `counsel:`, with the Article 6 basis
and the Article 9 condition alongside.

## Transparency (Article 50)

Applies from 2 August 2026, high-risk or not.

| Paragraph | Duty | On whom | Typical agent design evidence |
| --- | --- | --- | --- |
| 50(1) | People are told they are interacting with an AI system, unless obvious to a reasonably well-informed person | Provider (designs it in) | The chat discloses it is an AI (a C-ID with a UI test). An agent acting for someone towards others also discloses on whose behalf it acts, and discloses itself to its instructing user at key steps (Commission guidelines of 20 July 2026, paragraph 31) |
| 50(2) | Synthetic audio, image, video or text output is marked in a machine-readable, detectable way; exceptions for assistive standard editing and outputs that do not substantially alter the input | Provider | Marking decision (watermark, metadata, provenance) for every output people perceive, agent text included (guidelines paragraph 63); intermediate steps and web requests are out of scope. Exceptions: standard editing or no substantial alteration (paragraphs 90 and 91); narrow B2B or industrial use meeting all three paragraph 87 conditions. The exception relied on is `counsel:` |
| 50(3) | People exposed to emotion recognition or biometric categorisation are informed | Deployer | Notice in the workflow |
| 50(4) | Deepfakes disclosed; AI-generated text published to inform the public on matters of public interest disclosed unless human-reviewed under editorial responsibility | Deployer | Publishing workflow with editorial review |

50(5): the information is given clearly, at the latest at the first
interaction or exposure. Systems placed on the market before 2 August 2026
have until 2 December 2026 for 50(2) (Article 111(4), added by the
Omnibus, checked 2026-10-26). The Commission's Article 50 guidelines were
published on 20 July 2026 (C(2026) 5054,
<https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems>).
The Code of Practice on Transparency of AI-generated Content (final
text 10 June 2026) was found adequate for Article 50(2), (4) and (5) by
the Commission on 8 July 2026. Signing is voluntary and is not
conclusive evidence of compliance; non-signatories show equivalent
means
(<https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content>).

## General-purpose AI models

Articles 53 and 55 bind providers of general-purpose AI models, so for a
system built on Gemini through Vertex AI those duties sit with Google, not
with the client or the agency. Record the model ID and that the client
relies on the model provider's documentation. Fine-tuning or otherwise
modifying a model can raise whether the modifier becomes a model provider:
write it as `counsel:`. The Commission's GPAI guidelines (C(2025) 7719)
treat a downstream modifier as a model provider when the compute used for
the modification exceeds a third of the original model's training compute
(paragraphs 59 to 61); ordinary fine-tuning by an agency rarely reaches
it. Record the compute used as a fact. Google is a signatory of the GPAI
Code of Practice (published 10 July 2025, found adequate), which the
client can cite as the provider's compliance route
(<https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai>,
read 2026-10-26).

## AI literacy (Article 4)

Applies since 2 February 2025; replaced by the Omnibus with effect from 27
July 2026. Providers and deployers take measures to support the AI literacy
of staff and others operating or using the system on their behalf, taking
their knowledge and the context into account; the duty does not require
guaranteeing any individual's level. The proposal's version, an
encouragement duty on the Commission and Member States only, was not
adopted. A deployment plan answers it with the training and guidance given
to the system's users (a plan goal or the people plan in the discovery
brief).

## Penalties

Member States set penalties within the caps in Article 99. Prohibited
practices: up to EUR 35 million or 7 % of worldwide turnover. Most
operator duties, including deployers under Article 26, transparency
under Article 50 and, since the Omnibus, Article 25(2) and (4): EUR 15
million or 3 %. Misleading information to authorities: EUR 7.5 million
or 1 %. SMEs and, since the Omnibus, small mid-caps pay the lower of the
two. The Commission fines GPAI model providers up to EUR 15 million or
3 % (Article 101), from 2 August 2026 (Art. 113(b), checked
2026-10-26). GDPR fines under Article 83 run alongside.

## Applicability dates

Copy rows into the memo with the date you confirmed them.

| Obligation | Applies from | Source |
| --- | --- | --- |
| Entry into force of the AI Act | 1 August 2024 | Art. 113 Reg. 2024/1689 (checked 2026-10-26) |
| Prohibitions (Art. 5) and AI literacy (Art. 4) | 2 February 2025 | Art. 113(a) (checked 2026-10-26) |
| New prohibitions Art. 5(1)(ba), (bb) | 2 December 2026 | Art. 113(a) as amended by Reg. 2026/1744 (checked 2026-10-26) |
| General-purpose AI models (Chapter V), governance, penalties (except Art. 101) | 2 August 2025 | Art. 113(b) (checked 2026-10-26) |
| Commission fines on GPAI model providers (Art. 101) | 2 August 2026 | Art. 113(b) and general date (checked 2026-10-26) |
| GPAI models placed on the market before 2 August 2025 | 2 August 2027 | Art. 111(3) (checked 2026-10-26) |
| General application, including Art. 50 transparency | 2 August 2026 | Art. 113 (checked 2026-10-26) |
| Art. 50(2) marking for systems placed on the market before 2 August 2026 | 2 December 2026 | Art. 111(4) as added by Reg. 2026/1744 (checked 2026-10-26) |
| High-risk obligations, Annex III systems (Art. 6(2)) | 2 December 2027 | Art. 113(c) as replaced by Reg. 2026/1744 (checked 2026-10-26) |
| High-risk obligations, Annex I products (Art. 6(1)) | 2 August 2028 | Art. 113(c) as replaced by Reg. 2026/1744 (checked 2026-10-26) |
| FRIA (Art. 27) and deployer duties (Art. 26) for Annex III systems | 2 December 2027 | Art. 113(c)(i) as replaced by Reg. 2026/1744 (checked 2026-10-26) |
| Right to explanation (Art. 86) | 2 August 2026 (Chapter IX); in practice tied to Annex III classification from 2 December 2027, counsel to confirm | Art. 113 (checked 2026-10-26) |
| Revised Art. 4 AI literacy wording | 27 July 2026 | Reg. 2026/1744 entry into force (checked 2026-10-26) |

High-risk systems already on the market before their date are caught only
when their design changes significantly afterwards, except systems used by
public authorities, which comply by 2 August 2030 (Article 111(2) as
amended). Building now for a December 2027 obligation is a design choice
the plan records, not a reason to defer the classification.

## Other EU regimes

The memo's optional "EU: Other regimes" list screens these. Each line is
`n/a:` with its reason or `counsel:` with the facts. Read at the
Official Journal text on 26 October 2026 unless marked otherwise
(<https://eur-lex.europa.eu/eli/dir/2024/2853/oj>,
<https://eur-lex.europa.eu/eli/reg/2024/2847/oj>,
<https://eur-lex.europa.eu/eli/dir/2022/2555/oj>,
<https://eur-lex.europa.eu/eli/reg/2022/2554/oj>,
<https://eur-lex.europa.eu/eli/reg/2023/2854/oj>).

| Regime | When an agent project is in scope | What the pack records |
| --- | --- | --- |
| Product Liability Directive (EU) 2024/2853 | Products placed on the market or put into service after 9 December 2026 (Arts 2(1), 22, checked 2026-10-26). Software, including AI systems and SaaS, is a product (Art 4(1), recital 13). Whoever develops it is a manufacturer (Art 4(10)), so the agency and the client can both be. Liability to the injured person cannot be excluded by contract (Art 15). Damage covers death, personal injury, property and non-professional data | System card intended use, out-of-scope use, limits and update ownership; counsel: who is the manufacturer, indemnities, who supplies safety updates |
| Cyber Resilience Act (EU) 2024/2847 | Only a product made available on the market: a downloadable app, an on-premises install, an SDK or an accelerator licensed to several clients. A bespoke agent hosted for one client is not (recital 12). Reporting duties apply from 11 September 2026 and the rest from 11 December 2027 (Arts 14, 69(3), 71, checked 2026-10-26) | Questionnaire incident response and vulnerability management; counsel: is any deliverable a product |
| NIS2 Directive (EU) 2022/2555 | Client side: the client is an essential or important entity, so its supply-chain clauses reach the agency and the agent's incidents feed its 24-hour and 72-hour reports (Arts 21, 23). Agency side: only if it is a medium or larger managed service provider operating the system after go-live in the EU, which needs an EU representative (Art 26(3)) | Questionnaire incident response; counsel: is the agency a managed service provider for this client |
| DORA, Regulation (EU) 2022/2554 | Financial-entity clients, from 17 January 2025 (checked 2026-10-26). Article 30 sets the mandatory terms of ICT third-party contracts, which reach an agency supplying or operating the agent | Questionnaire; counsel: does the client classify the agency as supporting a critical or important function |
| Medical devices (MDR) | An agent intended to give information used for diagnostic or therapeutic decisions can be medical-device software. Under MDCG 2025-6 / AIB 2025-1 (June 2025, not a Commission position), class IIa or above is high-risk under AI Act Article 6(1), with obligations from 2 August 2028 (checked 2026-10-26) | Memo "Annex I product" row; counsel: MDR qualification and class |
| Data Act, Regulation (EU) 2023/2854 | Only where the agent is a related service of a connected product, is offered as a data processing service at scale (Article 31(1) exempts mostly custom-built services), or a data-sharing term is imposed. A bespoke internal agent usually triggers none | `n/a:` with the reason, or counsel |
| Digital Services Act | Only where the agent is part of an intermediary service (hosting user content, an online platform) | `n/a:` unless the client is a platform |
| AI Liability Directive | Proposal withdrawn; notice published in the Official Journal on 6 October 2025 (<http://data.europa.eu/eli/C/2025/5423/oj>, read 2026-10-26). National tort law applies | Do not cite it as pending law |

For insurers, the EIOPA Opinion on AI governance and risk management (6
August 2025,
<https://www.eiopa.europa.eu/eiopa-publishes-opinion-ai-governance-and-risk-management-2025-08-06_en>,
read 2026-10-26) sets expectations for AI that is not high-risk or
prohibited: data governance, record-keeping, fairness, cybersecurity,
explainability and human oversight. Use them as measures in the impact
assessment.
