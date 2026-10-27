---
document: regulatory-memo
system: Shortlisting assistant (Kestrel Logistics)
version: design accepted 2026-09-04; build v0.6.0 (M1 to M4)
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Anouk de Vries, counsel, Kestrel Logistics
sources: docs/discovery/shortlisting.md, docs/architecture/shortlisting.md, docs/plans/shortlisting.md
---

# Regulatory memo: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Kestrel Logistics' counsel. It records which regimes the jurisdiction
screen found in scope, the facts the design records, and the provisions that
appear relevant in each regime: the EU AI Act classification, and a screen of
the existing Australian laws that reach the consultancy's own handling.
Australia has no AI Act and assigns no risk tier. Conclusions are proposals for
counsel; not legal advice.

## Summary

- **Regimes in scope:** EU (through the client, the applicants and the use of the output) and Australia (only through Southgate Labs' own handling, from Sydney). United States, United Kingdom, New Zealand, Singapore and Canada are out of scope, each with its reason in the Jurisdiction screen (counsel: confirm the screen).
- **Proposed EU classification:** high-risk under Annex III point 4 (recruitment: ranking applicants), profiling of natural persons, with no Article 6(3) derogation proposed (docs/architecture/shortlisting.md R1, D1; M3; counsel: confirm). Annex III obligations apply from 2 December 2027 (Art. 113(c), checked 2026-10-26); GDPR applies to the pilot now.
- **Main obligation, EU, now:** a DPIA signed before the first live vacancy (W2), GDPR Article 22 analysis of a ranking that recruiters rely on (D1, D7), a transfer mechanism for Sydney access (D5, W4) and works council consultation (W1). Main obligation from 2 December 2027: the Chapter III provider duties and Article 26 deployer duties (checked 2026-10-26).
- **Main obligation, Australia:** only Southgate Labs' own handling is in view: whether the Privacy Act reaches Sydney staff reading EU applicants' logs and evaluation set (D5, D6; counsel). The client's own APP 1.7 duty is n/a: Kestrel is not an Australian entity (docs/discovery/shortlisting.md §1).
- **Fact that blocks the decision:** the adverse-impact ratio for applicants aged 50 and over is 0.71, below the 0.8 four-fifths comparison the measurement uses, against 0.93 to 1.00 for the other age bands and 0.96 for gender (M3). C7 names "pilot paused" as its failure outcome (C7). No mitigation goal exists in the plan (gap: plan has no goal for it).
- **Proposed roles:** Kestrel as AI Act provider and deployer and as GDPR controller; Southgate Labs as developer and, in GDPR terms, processor; Google as processor (Roles below; counsel: confirm).
- **Blocking questions:** counsel: 14 questions, listed under Questions for counsel.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes (counsel: whether the Privacy Act reaches it) | Southgate Labs engineers in Sydney have read access to logs and the evaluation set during the pilot and six weeks after (D5); consultancy home Sydney (docs/discovery/shortlisting.md §6) | The consultancy's own handling only; assumption: consultancy home Australia (default). The client's own APP 1.7 and sector rows are n/a: client and applicants are not in Australia |
| United States | no | Applicants are in the Netherlands, Germany, Poland and Romania (docs/discovery/shortlisting.md §4); client is in Rotterdam and Duisburg (docs/discovery/shortlisting.md §1) | n/a: no US client, applicant or processing location in the record; assumption: no US residents apply (counsel: confirm; Kestrel to confirm vacancy advertising reach) |
| EU | yes | Client established in the Netherlands and Germany (docs/discovery/shortlisting.md §1); applicants in four EU states (docs/discovery/shortlisting.md §4); output used in the EU (R1) | Establishment, EU data subjects and EU use of the output; AI Act and GDPR scope are counsel conclusions |
| United Kingdom | no | No UK entity, applicant or vacancy in the record (docs/discovery/shortlisting.md §1, §4) | n/a: no UK trigger fact; assumption: no UK applicants (counsel: confirm) |
| New Zealand | no | No New Zealand entity, applicant or data in the record (docs/discovery/shortlisting.md §4); Southgate does not access New Zealand data (D5) | n/a: no trigger fact |
| Singapore | no | No Singapore entity, applicant or data in the record (docs/discovery/shortlisting.md §4) | n/a: no trigger fact |
| Canada | no | No Canadian entity, applicant or province in the record (docs/discovery/shortlisting.md §4) | n/a: no trigger fact |

- **Processing locations:** Cloud Run and Cloud SQL in europe-west4 (docs/architecture/shortlisting.md, Scope gate); Gemini endpoint in europe-west4 (D2); applicant data stays in project `kestrel-talent-pilot` (D3). gap: the model's processing region from the provider's model page was not read (no network access in this run); gap: the log sink and its region (D4); consultancy access from Sydney (D5).
- **Government client:** private client; assumption: Kestrel Logistics B.V. is a private company (docs/discovery/shortlisting.md §1); no Commonwealth or NSW agency, so no government form answers are drafted.

## System and intended purpose

- **What it does:** ranks the applicants for a vacancy against its must-have requirements and gives a rationale per applicant citing passages of their own CV (R1, R2, C2, C5).
- **Who uses it and who it affects:** three recruiters in an eight-week pilot on warehouse and driver vacancies (docs/architecture/shortlisting.md, Scope gate); it affects applicants in the Netherlands, Germany, Poland and Romania (docs/discovery/shortlisting.md §4).
- **What the model decides and what code or people decide:** the model ranks and writes rationales; a recruiter decides who is shortlisted; the assistant changes nothing in the ATS and sends no messages (D1, R4, C3, docs/architecture/shortlisting.md Scope gate).
- **Effects it can cause:** a ranked list that decides which CVs a recruiter reads first; a suitable applicant ranked low "is never read" (docs/discovery/shortlisting.md §5). C6 (bottom-half applicants stay visible) is planned, not built (C6, G04 in_progress).
- **Human review of decisions about people:** the recruiter reviews every shortlist (R4, D7). gap: no measured share of ranked applicants a recruiter opens, and no override rate; M1 measures agreement with past recruiter decisions (81%), which is not a review rate (M1).

## Roles

- **Facts:** Kestrel Logistics B.V. commissions the system and its decider is the Head of Talent Acquisition (docs/discovery/shortlisting.md §3, §6); Southgate Labs builds it under an engagement (docs/discovery/shortlisting.md §6); recruiters in Rotterdam and Duisburg use it (docs/discovery/shortlisting.md §1); Southgate engineers read logs and the evaluation set (D5). gap: the contract between Kestrel and Southgate Labs, the data processing agreement and the Kestrel Logistik GmbH arrangement are not in the record.
- **Australia, Privacy Act:** Southgate Labs may be an APP entity in its own right; gap: annual turnover not recorded (counsel: s 6D small business exemption). The employee records exemption does not cover unsuccessful job applicants or a recruitment provider working under contract to an employer (source: adk-governance-pack reference australia.md, read 2026-10-28, not re-read at the source). No State or Commonwealth contract is in the record (counsel: confirm none). Whether the Act reaches EU applicants' data read from Sydney is counsel.
- **EU AI Act:** Kestrel "has the system developed" and uses it for its own recruiting, so provider and deployer, with Southgate Labs as the builder under contract (D1, docs/discovery/shortlisting.md §6); Southgate becomes a provider only if it places the system on the market under its own name or reuses it across clients (assumption: it does not; counsel: confirm, including whether an EU authorised representative would be needed if it were). Article 25(4) requires a written agreement between the provider of a high-risk system and a third party supplying components or services (checked 2026-10-26); gap: no such agreement in the record.
- **EU GDPR, separately:** Kestrel Logistics B.V. and Kestrel Logistik GmbH as controllers (which entity decides for which vacancies is counsel: single controller, joint controllers or separate); Southgate Labs as processor while it reads logs and the evaluation set (D5); Google Cloud as processor under the client's agreement (D2, D3). gap: no processor agreement or sub-processor list in the record. See privacy-impact-input-pack.md.

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed, and obligations come from existing laws (source: adk-governance-pack reference australia.md, checked 2026-10-26).
- **Scope of these sections:** Southgate Labs' own handling only (D5, D6); the client's own APP duties are n/a: Kestrel is not an Australian entity.
- **APPs engaged:** APP 3 and 5 (collection and notice for personal information Southgate reads or holds; D5), APP 6 (use for support and evaluation only; D5, D6), APP 8 and s 16C (Southgate accessing data held in the Netherlands is not an overseas disclosure by Southgate on these facts; counsel: confirm), APP 11 (security of logs and evaluation set; D4, D6; gap: no SB row covers Southgate's own access), APP 12 and 13 (gap: no access and correction route for logs and evaluation set). See privacy-impact-input-pack.md.
- **Notifiable data breaches:** I1 sent six unredacted CVs with dates of birth to the model in a test run (I1, closed 2026-10-07). gap: no record that Southgate or Kestrel assessed I1 as a breach under any regime; counsel: which entity assesses and notifies.
- **Pending, not law:** the tranche 2 privacy reform exposure draft (source: adk-governance-pack reference australia.md, checked 2026-10-26); not relied on.

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| n/a: the decision is Kestrel's about EU applicants; Southgate Labs makes no decision about a person | n/a: APP 1.7 applies from 10 December 2026 (checked 2026-10-26) to an APP entity that arranges the program; Kestrel is not one | n/a: the EU analysis is in the EU sections | n/a | n/a | D1, R4 |

- **Privacy policy inputs (APP 1.8):** n/a: no Australian client; system-card.md still carries the automated-decision disclosure for Kestrel's own notices.

## Australia: Sector, state and government AI policy

- **Sector laws:** n/a: no Australian sector regime reaches the work (recruitment for a Dutch logistics company, docs/discovery/shortlisting.md §1); counsel: confirm no Australian employment or anti-discrimination law applies to Sydney staff reading Dutch applicants' data.
- **Government AI policy:** n/a: private client; no Commonwealth or NSW agency (docs/discovery/shortlisting.md §1).

## EU: Prohibited practices (Article 5)

| Point | Applies? | Facts | Evidence |
| --- | --- | --- | --- |
| (a) manipulation, (b) exploiting vulnerabilities | no (counsel: confirm) | The tool ranks CVs for a recruiter; it does not address applicants | R1, D1 |
| (ba), (bb) generated intimate or abuse material | no | Text rationales only | R2, C2 |
| (c) social scoring, (d) crime prediction by profiling | no (counsel: confirm) | Scores fit to one vacancy's requirements, not behaviour across contexts | R1, C5 |
| (e) facial scraping, (g) biometric categorisation, (h) real-time remote identification | no | Photos are removed before the model sees a CV | C4 |
| (f) emotion inference at work or in education | no | No emotion inference function; applicants are not yet workers | R1, R2 |

Prohibitions applied from 2 February 2025; points (ba) and (bb) apply from 2 December 2026 (Art. 113(a), checked 2026-10-26).

## EU: High-risk classification (Article 6 and Annex III)

- **Annex I product:** no (assumption: a CV ranking tool is not a safety component of an Annex I product; D1).
- **Annex III area touched:** point 4, employment and workers' management: screening and ranking applications for recruitment (R1, docs/discovery/shortlisting.md §2).
- **Profiling of natural persons:** yes: the ranking evaluates each applicant's suitability from personal data (R1, R2, C5; counsel: confirm). A system that profiles natural persons is always high-risk (source: adk-governance-pack reference eu-ai-act.md, checked 2026-10-26).
- **Article 6(3) derogation facts, if argued:** not proposed. For argument: D1 (no automatic rejection) and R4 (recruiter decides) point to human control; against it, the ranking determines which CVs are read first (docs/discovery/shortlisting.md §5), M1 shows the ranking agrees with recruiters 81% of the time, M3 shows a disparity for one age band, and "a human reviews it" does not by itself remove material influence. counsel: decide.
- **If high-risk:** Chapter III provider duties (risk management, data governance, technical documentation, logging, transparency, human oversight, accuracy and robustness, quality management, conformity assessment, registration) and Article 26 deployer duties (use per instructions, competent human oversight, logs kept at least six months, informing workers' representatives before use at work, informing the people subject to the decision) apply from 2 December 2027 (Art. 113(c), checked 2026-10-26). Facts for each: oversight (R4, D7, C6 planned under G04); logs (D4 keeps prompts and responses 14 days, shorter than six months; gap: counsel: whether Article 26 log retention applies to the pilot); workers' representatives (W1); data governance (D6, M3). gap: the plan has no goal for technical documentation, quality management, conformity assessment or registration (proposed goals in Gaps below).
- **Pilot timing:** the pilot runs before the Annex III date. Whether a pilot on live applicants is "putting into service", and so whether design changes after that date bring the system under Article 111, is counsel (checked 2026-10-26: systems on the market before the date are caught only on significant design change).
- **FRIA (Article 27):** not apparent for a private logistics employer under Annex III point 4 (docs/discovery/shortlisting.md §1); counsel: confirm Kestrel does not provide public services. The impact assessment carries the crosswalk in case counsel finds otherwise.
- **Article 25(4) agreement (if high-risk):** gap: no written agreement between Kestrel and Southgate Labs in the record (counsel: confirm what Southgate supplies and what Kestrel needs).
- **Bias monitoring and special categories (Article 4a):** M3 measures age band and gender (M3), neither an Article 9 special category. gap: how age band and gender were derived for the 1,400 past applications, given that C4 removes dates of birth only before the model call and D6 removes names and contact details; if any special category was inferred, counsel: Article 4a conditions (a) to (f), Article 6 basis and Article 9 condition.

## EU: Transparency obligations (Article 50)

| Paragraph | Applies? | How the design meets it | Evidence |
| --- | --- | --- | --- |
| 50(1) told they interact with AI | counsel: recruiters are the users and know it is an AI tool; applicants do not interact with it | Applicant notice is a GDPR and Article 26 matter; gap: no applicant notice in the record | R4, D1 |
| 50(2) machine-readable marking of generated content | counsel: rationales are generated text a recruiter perceives; exception relied on, if any | gap: no marking decision recorded | R2, C2 |
| 50(3) emotion recognition or biometric categorisation notice | n/a: no such function | Photos removed before the model | C4 |
| 50(4) deepfakes or public-interest text | n/a: internal ranking, no publication | No publishing step | R4 |

Article 50 applies from 2 August 2026 (Art. 113, checked 2026-10-26).

## EU: General-purpose AI model

- **Model and provider:** Gemini 3.5 Flash pinned as gemini-3.5-flash-001 on Vertex AI, provided by Google (D2). gap: retirement date of the pinned model and its processing region were not read from the provider's model page or a lifecycle table (not installed; no network access); proposed goal for adk-model-and-output-contracts.
- **Obligations under Articles 53 and 55:** sit with the model provider; Kestrel relies on its documentation (source: adk-governance-pack reference eu-ai-act.md, read 2026-10-26; counsel: confirm).
- **Fine-tuning or modification:** none recorded (D2); counsel: n/a unless any is planned.
- **Downstream modification compute:** none recorded (D2).

## EU: Other regimes

- GDPR Articles 22, 35 and Chapter V: see privacy-impact-input-pack.md and transfer-assessment.md (D4, D5).
- NIS2: counsel: whether Kestrel, a logistics company, is an essential or important entity; gap: sector and size not recorded (docs/discovery/shortlisting.md §1).
- Cyber Resilience Act, Data Act, Digital Services Act, DORA, MDR: n/a: a bespoke hosted tool for one client, no platform, no financial entity, no medical purpose (D3, R1).
- Product Liability Directive: applies to products placed on the market after 9 December 2026 (Arts 2(1), 22, checked 2026-10-26); counsel: manufacturer and update ownership, if the pilot build is "put into service" after that date.
- National employment law, works council rights and national equality law of the Netherlands, Germany, Poland and Romania: not covered by this pack's references; counsel: each applies? (W1).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| EU | Article 50 transparency | 2 August 2026 (Art. 113, checked 2026-10-26) | Marking and notice decisions for the pilot; D2 |
| EU | New prohibitions Art. 5(1)(ba), (bb) | 2 December 2026 (Art. 113(a), checked 2026-10-26) | n/a: text rationales only |
| EU | High-risk obligations, Annex III, and Articles 26 and 27 | 2 December 2027 (Art. 113(c), checked 2026-10-26) | Production duties; plan has no goal yet |
| EU | AI literacy (revised Article 4) | 27 July 2026 (Reg. 2026/1744 entry into force, checked 2026-10-26) | Training for the three pilot recruiters; gap: no plan goal |
| EU | Product Liability Directive | 9 December 2026 (Arts 2(1), 22, checked 2026-10-26) | Counsel question above |
| Australia | APP 1.7 to 1.9 | 10 December 2026 (checked 2026-10-26) | n/a: client's duty, not in scope |

- **AI literacy (EU AI Act Article 4) and staff training:** gap: no training or guidance goal for the recruiters in the plan; proposed goal for adk-presenter's rollout pack.
- **Documents the client's own process produces:** works council consultation outcome (W1); DPIA signed by the DPO (W2); legal review of these papers (W3); transfer mechanism and transfer impact assessment (W4); Article 36 prior consultation only if triggered (W5); Article 49 EU database registration and the conformity assessment before the Annex III date (gap: no plan goal; counsel: owner). Date checks above were not re-read at the source on 2026-10-28.

## Questions for counsel

- counsel: Is the system high-risk under Annex III point 4, and is Article 6(3) unavailable because it profiles; regime EU; facts at R1, D1, M1, M3; needed before the 2026-11-20 pilot decision.
- counsel: Does the pilot on live applicants fall under the AI Act before 2 December 2027, and does any later design change bring it under Article 111; regime EU; needed before G07.
- counsel: Are Kestrel Logistics B.V. and Kestrel Logistik GmbH single, joint or separate controllers, and which is the exporter for the Sydney access; regime EU; facts at D5; needed before W4.
- counsel: Does a ranking recruiters rely on amount to a decision under GDPR Article 22 (SCHUFA), and what does the Article 22(3) route look like; regime EU; facts at D1, D7, C6; needed before W2.
- counsel: Is a disparity ratio of 0.71 for applicants aged 50 and over (M3) a breach of EU or Dutch, German, Polish or Romanian equality law, or justifiable; the four-fifths comparison is the measurement's method, not a legal test this pack has verified; regime EU; needed before the pilot decision.
- counsel: Does C7's "pilot paused" outcome apply to M3 now, and who decides; regime EU; facts at C7, M3; the decider is the Head of Talent Acquisition (docs/discovery/shortlisting.md §3).
- counsel: Does Kestrel have a lawful basis and a compatible purpose for reusing 1,400 past applications (2024 to 2026) as an evaluation set, and for the Sydney reading of it; regime EU; facts at D5, D6.
- counsel: Was I1 a personal data breach to be assessed or notified under GDPR Articles 33 and 34; regime EU; facts at I1.
- counsel: What works council consent, information or consultation rights apply in the Netherlands and Germany, and does W1 have to finish before live data; regime EU; facts at W1 (requested 2026-10-02, no date).
- counsel: Is a written Article 25(4) agreement and a GDPR Article 28 processor agreement with Southgate Labs required, and do they exist; regime EU; needed before W4.
- counsel: Which supervisory authority leads for a group in the Netherlands and Germany, and is Article 36 consultation likely (W5); regime EU.
- counsel: Is Kestrel an essential or important entity under NIS2; regime EU.
- counsel: Does the Privacy Act reach Southgate Labs' handling of EU applicants' data from Sydney, and is Southgate an APP entity; regime Australia; facts at D5.
- counsel: What national employment and equality rules in the four applicant countries apply; not covered by this pack's references; regime EU.

## Assumptions and questions the session could not put to anyone

- Assumption: consultancy home is Australia (default); question: confirm where Southgate staff and systems that can see project data are (the brief names two engineers in Sydney; docs/discovery/shortlisting.md §6).
- Assumption: Kestrel is a private company with no public-service function; question: confirm.
- Assumption: no applicant is in the US, UK, New Zealand, Singapore or Canada; question: do vacancies reach any of them.
- Question: is the 0.8 threshold the steering group's pilot gate? The design names "pilot paused" for C7 but states no threshold (C7).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Anouk de Vries, counsel | This document | pending | pending |
