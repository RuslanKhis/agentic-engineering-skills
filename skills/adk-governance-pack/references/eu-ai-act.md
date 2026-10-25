# EU AI Act classification

Read when writing the classification memo or the proof-of-concept note. The
memo classifies the system the design describes. It does not decide the law:
it gives counsel the facts, the provisions that look relevant and the
questions only counsel can settle.

Every provision below was read in the Official Journal text on 25 October
2026: Regulation (EU) 2024/1689 (the AI Act, OJ L 12.7.2024,
<https://eur-lex.europa.eu/eli/reg/2024/1689/oj>) as amended by Regulation
(EU) 2026/1744 (the Digital Omnibus on AI, OJ L 24.7.2026, in force 27 July
2026, <https://eur-lex.europa.eu/eli/reg/2026/1744/oj>). No consolidated
version was read. When a draft states a provision or a date, it carries
`checked <date>` with the day the drafter last confirmed it; copy
`checked 2026-10-25` only while this file is the newest check, and re-check
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
provider must hand over in that case (documentation, known limits, technical
access). State the facts (who commissions, whose name, who changes the
purpose) with their IDs and write the role as `counsel:` to confirm; a
contract that assigns the role differently is counsel's to read.

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
| (ba), (bb) | Generating realistic non-consensual intimate material of an identifiable person, or child sexual abuse material | Any open image or video generation |
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
(machinery, medical devices, toys and others; rare for agency agents), or
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
registers it (Article 49(2)). The Commission's guidelines on classification
(Article 6(5)) were still a draft on 25 October 2026 (published for
consultation 19 May 2026); cite them as draft.

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
provider's information for its DPIA (Article 26). A fundamental rights
impact assessment (Article 27) is required of deployers that are public
bodies or private entities providing public services, and of deployers of
Annex III points 5(b) (credit) and 5(c) (life and health insurance). Since
the Omnibus, Article 27(4) lets the FRIA cross-reference or include the
relevant parts of the GDPR DPIA where it already meets an obligation, so
the [DPIA input pack](privacy-and-records.md) is written to be cited by
section.

Article 4a (added by the Omnibus) gives a legal basis for processing special
categories of personal data to detect and correct bias, under conditions;
a bias-monitoring contract such as an adverse-impact check should name it as
`counsel:` rather than assume GDPR Article 9 alone covers it.

## Transparency (Article 50)

Applies from 2 August 2026, high-risk or not.

| Paragraph | Duty | On whom | Typical agent design evidence |
| --- | --- | --- | --- |
| 50(1) | People are told they are interacting with an AI system, unless obvious to a reasonably well-informed person | Provider (designs it in) | The chat discloses it is an AI (a C-ID with a UI test) |
| 50(2) | Synthetic audio, image, video or text output is marked in a machine-readable, detectable way; exceptions for assistive standard editing and outputs that do not substantially alter the input | Provider | Watermark or metadata decision; counsel on whether chat text is in scope |
| 50(3) | People exposed to emotion recognition or biometric categorisation are informed | Deployer | Notice in the workflow |
| 50(4) | Deepfakes disclosed; AI-generated text published to inform the public on matters of public interest disclosed unless human-reviewed under editorial responsibility | Deployer | Publishing workflow with editorial review |

50(5): the information is given clearly, at the latest at the first
interaction or exposure. Systems placed on the market before 2 August 2026
have until 2 December 2026 for 50(2) (Article 111(4), added by the
Omnibus). The Commission's voluntary Code of Practice on marking and
labelling AI-generated content was published on 10 June 2026.

## General-purpose AI models

Articles 53 and 55 bind providers of general-purpose AI models, so for a
system built on Gemini through Vertex AI those duties sit with Google, not
with the client or the agency. Record the model ID and that the client
relies on the model provider's documentation. Fine-tuning or otherwise
modifying a model can raise whether the modifier becomes a model provider:
write it as `counsel:`.

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

## Applicability dates

Copy rows into the memo with the date you confirmed them.

| Obligation | Applies from | Source |
| --- | --- | --- |
| Entry into force of the AI Act | 1 August 2024 | Art. 113 Reg. 2024/1689 (checked 2026-10-25) |
| Prohibitions (Art. 5) and AI literacy (Art. 4) | 2 February 2025 | Art. 113(a) (checked 2026-10-25) |
| New prohibitions Art. 5(1)(ba), (bb) | 2 December 2026 | Art. 113(a) as amended by Reg. 2026/1744 (checked 2026-10-25) |
| General-purpose AI models (Chapter V), governance, penalties | 2 August 2025 | Art. 113(b) (checked 2026-10-25) |
| General application, including Art. 50 transparency | 2 August 2026 | Art. 113 (checked 2026-10-25) |
| Art. 50(2) marking for systems placed on the market before 2 August 2026 | 2 December 2026 | Art. 111(4) as added by Reg. 2026/1744 (checked 2026-10-25) |
| High-risk obligations, Annex III systems (Art. 6(2)) | 2 December 2027 | Art. 113(c) as replaced by Reg. 2026/1744 (checked 2026-10-25) |
| High-risk obligations, Annex I products (Art. 6(1)) | 2 August 2028 | Art. 113(c) as replaced by Reg. 2026/1744 (checked 2026-10-25) |
| Revised Art. 4 AI literacy wording | 27 July 2026 | Reg. 2026/1744 entry into force (checked 2026-10-25) |

High-risk systems already on the market before their date are caught only
when their design changes significantly afterwards, except systems used by
public authorities, which comply by 2 August 2030 (Article 111(2) as
amended). Building now for a December 2027 obligation is a design choice
the plan records, not a reason to defer the classification.
