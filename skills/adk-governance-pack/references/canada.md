# Canada

<!-- verified: 2026-10-26; re-check every 180 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) puts `ca` in
scope. Canada has no AI Act and no AI bill, so the Canadian sections of the
regulatory memo assign no risk tier. They screen which privacy laws govern
each flow (federal PIPEDA, Quebec, Alberta and British Columbia), the
employment, sector and government rules the agent falls under, and leave
every legal conclusion to counsel. This reference is at screen depth: the
triggers, the key duties, the pack section each lands in and the questions
for counsel.

Name the regime "Canada" or "Quebec" in drafts, never "CA": US sections use
"CA" for California, and the checker does not read "CA" as Canada.

## Sources and their status

Read at the primary source on 26 October 2026 unless a line says
"reported; not confirmed at the source on 2026-10-26". Copy `checked
2026-10-26` into a draft only while this file is the newest check. Several
primary sites refused automated reads that day (parl.ca, LégisQuébec,
CanLII, the Treasury Board policy site, the CRTC FAQ and, late in the
session, Justice Laws); claims resting on them are marked.

- PIPEDA, S.C. 2000, c. 5, Justice Laws consolidation current to 2026-09-30
  (<https://laws-lois.justice.gc.ca/eng/acts/P-8.6/>): ss 4, 5(3), 6.1, 10.1
  to 10.3, 26(2)(b), 28 and 30, and Schedule 1. Breach of Security
  Safeguards Regulations, SOR/2018-64.
- Office of the Privacy Commissioner of Canada (OPC,
  <https://www.priv.gc.ca>): Guidelines for obtaining meaningful consent
  (modified 11 August 2025); Guidelines for processing personal data across
  borders (27 January 2009); the joint Principles for responsible,
  trustworthy and privacy-protective generative AI technologies (7 December
  2023); statements on the ChatGPT (6 May 2026) and Grok (11 June 2026)
  findings and on Bill C-36 (15 June 2026); the submission on AI
  transparency (23 September 2026). ISED's Bill C-36 backgrounder (15 June
  2026).
- Commission d'accès à l'information du Québec (CAI,
  <https://www.cai.gouv.qc.ca>): the business aide-mémoire (8 February
  2023), read in full, and the privacy impact assessment guide v3.1 (April
  2024), sections 1 and 7. **The Act's own text at LégisQuébec was not
  read**: section substance below comes from the CAI where it states it.
- Alberta Personal Information Protection Act, consolidation current as of 1
  September 2025; BC Personal Information Protection Act, current to 20
  October 2026.
- ontario.ca: the Employment Standards Act guides on publicly advertised job
  postings (updated 24 February 2026) and on written electronic monitoring
  policies (updated 8 July 2024); the Responsible Use of Artificial
  Intelligence Directive (updated 7 January 2026).
- canada.ca: the Algorithmic Impact Assessment tool (modified 15 September
  2026); the Guide on the use of generative AI (modified 24 September 2026);
  the AI Strategy for the Federal Public Service, full text dated 2 October
  2026; the GC AI Register release (28 November 2025).

The full research note, with every secondary item marked, is
`docs/research/ca-ai-privacy-law-2026-10-26.md` in the skills repository.

## No AI Act; pending law

The Artificial Intelligence and Data Act died with Bill C-27 when
Parliament was prorogued (the prorogation date, 6 January 2025, is
reported; not confirmed at the source on 2026-10-26). ISED's backgrounder
describes no AI statute in its successor. Bill C-36, the Protecting Privacy
and Consumer Data Act, was introduced and read a first time on 15 June 2026
(checked 2026-10-26); that it still awaits second reading is reported; not
confirmed at the source on 2026-10-26. It is not law. The memo says so in
one line each, with `checked 2026-10-26`. Design choices that make a later
move cheap: keep the decision-explanation facts (information used, source,
principal factors) that Quebec s 12.1 already wants.

## Which law governs each flow

Canada has two layers, chosen flow by flow. Write a per-flow table in the
memo's "Canada: Privacy laws and roles" section, not one regime row; which
law governs each flow is `counsel:`.

- **PIPEDA** binds every organisation that collects, uses or discloses
  personal information "in the course of commercial activities" (s 4(1)(a)),
  except where a province has a law declared substantially similar and the
  information stays in that province. Quebec, Alberta and BC have such laws
  (the exemption orders were not re-read; reported; not confirmed at the
  source on 2026-10-26). That PIPEDA governs flows that cross a provincial or
  national border is likewise reported; not confirmed at the source on
  2026-10-26.
- **Employees.** PIPEDA reaches employee and applicant information only at a
  federal work, undertaking or business (s 4(1)(b)): banks, airlines,
  telecommunications, interprovincial transport. Quebec, Alberta and BC
  cover employees under their own laws. **A provincially regulated
  employer's staff data elsewhere (Ontario, for example) has no general
  private sector privacy statute**; write that as `n/a:` for the statute
  with `counsel:` on collective agreements and common law torts, never as
  freedom from privacy duties.
- **Roles.** The statutes have no controller and processor: PIPEDA speaks of
  the organisation "responsible for personal information under its control",
  including information transferred to a third party for processing
  (Schedule 1, 4.1.3); Quebec speaks of mandates and service contracts.
  Whether the consultancy acts only for the client, or for its own purposes
  too, is `counsel:`.

## PIPEDA principles an agent engages

| Principle | What it requires (Schedule 1 and the Act) | Agent facts to record |
| --- | --- | --- |
| 4.1.3 Accountability for transfers | "shall use contractual or other means to provide a comparable level of protection" while information is processed by a third party | Contracts with Google Cloud and the consultancy; where staff access from |
| 4.2, 4.3 and s 6.1 Purposes and meaningful consent | Purposes stated at or before collection; consent "only valid if it is reasonable to expect" the audience to understand "the nature, purpose and consequences" | Just-in-time notice naming the model provider |
| s 5(3) Appropriate purposes | Purposes "a reasonable person would consider are appropriate in the circumstances" | The OPC's no-go zones |
| 4.4, 4.5 Limiting collection, use and retention | Only what is necessary; destroy, erase or anonymise when no longer needed | Prompt minimisation; retention per store |
| 4.6 Accuracy; 4.7 Safeguards | As accurate as necessary; safeguards proportionate to sensitivity | Evaluation results; SB and C IDs |
| 4.8, 4.9 Openness and access | Policies available; access and an account of use and disclosure on request | Memory, history and evaluation sets an access request reaches |

The OPC's consent guidelines put four elements up front: what personal
information, with which parties, for what purposes, and the risk of harm.
Express consent is generally required for sensitive information. Never write
"lawful basis" or "legitimate interests" in a Canadian section.

**Cross-border (OPC, 27 January 2009).** "A transfer for processing is a
'use' of the information; it is not a disclosure." Canada uses an
"organization-to-organization approach that is not based on the concept of
adequacy": no country list and no standard clauses. The contract is "the
primary means" of protection, and people are told their information may be
processed in a foreign jurisdiction and be accessible to its courts, law
enforcement and national security authorities, "ideally ... at the time the
information is collected".

**Breaches.** Report to the Commissioner and notify affected people "as soon
as feasible" when a breach "creates a real risk of significant harm"
(s 10.1), and **keep a record of every breach**, reportable or not, for 24
months (s 10.3; Regulations s 6). Knowingly failing to is an offence up to
$100,000 on indictment (s 28). PIPEDA has no administrative monetary
penalties.

## Quebec: the private sector Act as amended by Law 25

Quebec's law is the strictest Canadian regime and is in force, phased in on
22 September 2022, 22 September 2023 and 22 September 2024 (CAI
aide-mémoire, checked 2026-10-26). It covers the client's Quebec employees
and applicants as well as customers.

- **s 3.1 Person in charge.** The person with the highest authority, who may
  delegate in writing; title and contact details published on the website.
- **s 3.3 PIA for systems projects** (from 22 September 2023, checked
  2026-10-26). A privacy impact assessment for any project to acquire,
  develop or overhaul an information system or electronic service delivery
  system involving personal information; the CAI lists an artificial
  intelligence system among them (EFVP guide v3.1, s 7.2). **An agent
  project for a Quebec enterprise is an s 3.3 project**; the input pack is
  the input to the client's EFVP.
- **s 17 Communication outside Quebec** (from 22 September 2023, checked
  2026-10-26). A PIA before communicating personal information outside
  Quebec, or entrusting someone outside Quebec with it, considering its
  sensitivity, the purpose, the protection measures including contractual
  ones, and the destination's legal framework. It may proceed only if the
  information "would receive adequate protection"; otherwise the enterprise
  must refuse. The communication is subject to a **written agreement** that
  takes the assessment into account. Outside Quebec includes the rest of
  Canada: a Toronto region, a US endpoint, a global endpoint, log sinks and
  consultancy access from Sydney each need it. Which Google Cloud regions
  are in Montréal and Toronto is reported; not confirmed at the source on
  2026-10-26.
- **s 12.1 Decisions based exclusively on automated processing.** In force
  since 22 September 2023 (CAI aide-mémoire, checked 2026-10-26); the
  section's wording is reported; not confirmed at the source on 2026-10-26.
  As reported: inform the person no later than when they are told of the
  decision; on request, give the personal information used, the reasons and
  principal factors and parameters, and the right to have the information
  corrected; and let the person submit observations to a staff member who
  can review the decision. The trigger is narrower than APP 1.7 and close to
  GDPR Article 22: meaningful human intervention takes a decision out, and a
  person who only confirms the output arguably does not (`counsel:`). It is
  a transparency and review duty, not a right to object.
- **s 9.1 Privacy by default.** Products offered to the public with privacy
  settings default to the highest level: memory, personalisation, history
  sharing and training opt-ins default off for a public-facing agent.
- **s 8.1** notice before using technology that can identify, locate or
  profile a person; **ss 3.5 to 3.8** confidentiality incidents: notify the
  CAI and the person on a "risk of serious injury" and keep an incident
  register; **s 23** destruction or anonymisation; **s 27** portability from
  22 September 2024 (checked 2026-10-26).
- **Penalties** up to the greater of $10 million or 2% of worldwide turnover
  (administrative) and $25 million or 4% (penal) are reported; not
  confirmed at the source on 2026-10-26. Quebec-facing notices may need
  French (reported; not confirmed at the source on 2026-10-26).

Any decision about a Quebec person made by the agent alone sets
`counsel_required: yes`.

## Alberta and British Columbia

- **Alberta PIPA.** Policies must list "the countries outside Canada in
  which the collection, use, disclosure or storage is occurring or may
  occur" by service providers (s 6(2)), and the person is told how to get
  that information and who can answer questions (s 13.1). It is the only
  Canadian statute that makes the country list mandatory: a US endpoint or
  consultancy access from Sydney goes on it. Breaches with "a real risk of
  significant harm" go to the Commissioner "without unreasonable delay"
  (s 34.1). No amendment bill has been introduced (alberta.ca, updated 3
  March 2026).
- **BC PIPA.** Consent unless an exception applies; employee information
  with notice in advance; information used to make a decision that directly
  affects a person kept "for at least one year after using it" (s 35(1)),
  which can collide with a short session-retention design. **No breach
  notification duty and no provision on storage outside Canada** in the Act.

## Breach clocks to list

PIPEDA: as soon as feasible, and the 24-month record of every breach.
Quebec: the CAI and the person on a risk of serious injury, and the incident
register. Alberta: without unreasonable delay. BC: no statutory duty. Which
entity reports to which commissioner is `counsel:`.

## OPC guidance on AI

The joint generative AI principles (7 December 2023, with the provincial
commissioners) ask organisations using generative AI for "Privacy Impact
Assessments (PIAs) and/or Algorithmic Impact Assessments (AIAs)"; to tell
affected people "whether a generative AI tool will be used as part of a
decision-making process"; to give "the opportunity to request human review
and/or re-consideration"; and say "accountability for decisions rests with
the organization, and not with any kind of automated system". Anticipated
no-go zones include "conversational bots to deliberately nudge people into
revealing sensitive personal information". The Grok finding (11 June 2026)
says to assess privacy risks "at the outset of any new initiative". The
OPC's "work on agentic AI is ongoing"; it has published no agentic guidance
(23 September 2026). Measure the input pack against the nine principles.

## Employment

- **Ontario job postings.** For publicly advertised postings on or after
  January 1, 2026 (checked 2026-10-26), an employer with 25 or more
  employees that uses AI "to screen, assess or select applicants" must say
  so in the posting, including when a recruiter does the screening; records
  are kept 3 years. Whether a summariser a recruiter reads "assesses"
  applicants is `counsel:`.
- **Ontario electronic monitoring policy.** Employers with 25 or more
  employees on January 1 must have a written policy before March 1, with
  copies to employees within 30 days; prompt logging tied to named staff is
  a fact for it (`counsel:`).
- **Human rights codes** apply to any screening or ranking, including
  adverse-impact discrimination (statutes not re-read; reported; not
  confirmed at the source on 2026-10-26). For Ontario, use the OHRC and Law
  Commission of Ontario Human Rights AI Impact Assessment (6 November 2024)
  as the adverse-impact checklist. Screening or ranking people sets
  `counsel_required: yes`.

## Government clients

- **Federal institutions.** The Directive on Automated Decision-Making binds
  federal institutions; its current version (dated 24 June 2025, with
  systems built before then given until 24 June 2026) and its Appendix C
  requirements by level are reported; not confirmed at the source on
  2026-10-26, because the Treasury Board site refused automated reads.
  The Algorithmic Impact Assessment has 65 risk and 41 mitigation questions
  and scores Level I (0 to 25%), II (26 to 50%), III (51 to 75%) and IV (76
  to 100%); it is completed at the start of design and again before
  production, with results published in both official languages (canada.ca,
  modified 15 September 2026). The generative AI guide applies the Directive
  when generative AI is used "to make or inform administrative decisions"
  and says "Notify users that they are interacting with generative AI".
  The GC AI Register launched on 28 November 2025. The department completes
  and publishes the AIA; the pack supplies inputs in the impact assessment's
  "Canada: AIA inputs" section and names the level as `counsel:` and the
  department's decision. A federal client sets `counsel_required: yes`.
- **Ontario.** The Responsible Use of AI Directive (effective 1 December
  2024) binds ministries and provincial agencies: a risk management process,
  disclosure where the public interacts with AI or AI affects a decision
  about a person, and a published use-case inventory. The Enhancing Digital
  Security and Trust Act's AI duties for the public sector await
  regulations (IPC Ontario, January 2026).
- **Quebec public bodies** have a twin of s 12.1 for decisions "where no
  natural person exercised significant control" (quebec.ca, updated 20
  October 2025).

## Screen when the trigger fires

| Law | Trigger | What the pack records |
| --- | --- | --- |
| PHIPA and other provincial health laws | Health information; a health information custodian client | IPC Ontario's AI scribes guidance (January 2026) for structure; which law applies is `counsel:`; `counsel_required: yes` |
| CASL | Outbound commercial email, SMS or instant messages | Consent (implied consent up to 2 years, 6 months for inquiries), identification, unsubscribe within 10 business days (ISED); voice: `counsel:` on telemarketing rules |
| Competition Act | Consumer-facing agent or performance claims | Claims cite M records; the Bureau's position that there is "no 'AI exception'" is reported; not confirmed at the source on 2026-10-26 |
| Bill C-8 (Critical Cyber Systems Protection Act) | Designated operator client (bank, telecom, energy, transport) | Royal Assent on 15 June 2026 is reported; not confirmed at the source on 2026-10-26; screen only for designated operators |

## Screening checklist

| Trigger fact (with its ID) | Law | Document and section |
| --- | --- | --- |
| Personal information of people in Canada in a commercial activity | PIPEDA Schedule 1, s 5(3), s 6.1 | Memo "Canada: Privacy laws and roles"; input pack "Canada: Consent and notice inputs" |
| Quebec enterprise, or Quebec residents, customers or employees | Quebec private sector Act (Law 25) | Memo; input pack "Canada: Quebec PIA and s 17 facts" |
| The agent project builds a system handling a Quebec enterprise's personal information | s 3.3 PIA | Input pack as the EFVP input; a calendar wait for the client's EFVP |
| Endpoint, processing, logs, support or consultancy access outside Quebec | s 17 PIA and written agreement | Transfer annex Canada rows; `counsel:` |
| Any personal information leaves Canada | PIPEDA 4.1.3 and the 2009 guidelines; Alberta ss 6(2), 13.1 | Input pack recipients and notice; Alberta country list |
| A decision about a Quebec person made by the agent alone | Quebec s 12.1 | Memo "Canada: Automated decisions"; system card s 12.1 block; `counsel_required: yes` |
| Public-facing product with privacy settings, for Quebec | s 9.1 | System card defaults |
| Bank, airline, telecom or other federal work with employee data | PIPEDA s 4(1)(b) | Memo Roles |
| Ontario employer of 25 or more; the agent screens applicants or logs staff activity | ESA job postings; electronic monitoring policy | System card disclosure; plan waits; `counsel_required: yes` for screening |
| Federal department or agency; output makes or informs an administrative decision | Directive on Automated Decision-Making; AIA | Impact assessment "Canada: AIA inputs"; `counsel_required: yes` |
| Ontario ministry or provincial agency | Responsible Use of AI Directive | Memo government row |
| Any personal information held | PIPEDA ss 10.1, 10.3; Quebec ss 3.5 to 3.8; Alberta s 34.1 | Questionnaire incident row and the 24-month record |

## Questions counsel usually gets

- Which law governs each flow: PIPEDA, Quebec, Alberta or BC?
- Is the consultancy acting only for the client, and does its access from
  Sydney need the Quebec s 17 assessment and the Alberta country list?
- Is implied consent enough for each purpose, or is express consent needed?
- Is any decision based exclusively on automated processing under s 12.1?
- Does the s 17 assessment show adequate protection for the US and
  Australia, and is the Google Cloud agreement the written agreement?
- Does the agent "assess" applicants under the Ontario ESA?
- For federal clients: is the output an administrative decision, what
  impact level, and who approves operation?
- Which entity reports a breach to which commissioner?

## Words to use

Personal information, organisation, individual, meaningful consent,
privacy impact assessment (EFVP in Quebec), breach of security safeguards
(PIPEDA), confidentiality incident (Quebec), person in charge of the
protection of personal information, real risk of significant harm. Never
"lawful basis", "controller" or "processor" in a Canadian section.
