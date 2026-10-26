# Australian government form crosswalks

<!-- verified: 2026-10-26; re-check every 90 days -->

Read when the [jurisdiction screen](jurisdiction-screen.md) finds a
Commonwealth client (a non-corporate Commonwealth entity) or a NSW public
sector agency client. This file maps the official forms those agencies
complete to the project's records. It ships the maps, never the forms:
official forms change faster than laws, so this file is re-checked every 90
days, and each form below carries the version and the date it was checked.

The NSW and Commonwealth law behind these forms is in
[Australia](australia.md); this file covers only the forms.

## What it produces

One pack document per official form, written from the
[government form answers template](../assets/government-form-answers-template.md)
and named `government-form-answers-<form>.md` (for example
`government-form-answers-dta-impact-assessment.md`,
`government-form-answers-nsw-aiaf-registration.md`). Each holds draft
answers in the official form's own order, for the agency's officers to check
and paste into the official tool, where they complete, rate and approve it.
Every answer cites a record ID or pack document, or says who answers it:

- `agency:` for what only the agency can answer (officer names, its approved
  products, its legislation, its risk appetite, its records systems);
- `counsel:` for a legal question;
- `assumption:` for a proposed rating, with its basis.

## Rules for every form

- **Never reproduce the form.** Give the question number and a short
  paraphrase, never the full text, and say in the preamble that the draft is
  not the official form (the checker requires it).
- **Re-read the form's official page first.** Record the version it shows
  and the date in `form_version` and `form_checked`. If the version differs
  from the one below, write a `gap:` in "Form and version" and do not draft
  answers to the changed questions until this file is updated. If the page
  cannot be read (no web access, or the form sits behind the agency's
  login), use the version and checked date recorded below for `form_version`
  and `form_checked`, and write "gap: official page not re-read" in "Form
  and version"; the checker's 90-day warning then tracks the true age.
- **Number questions as the form does** ("Reg 1", "1.5", "Part 2"), never as
  a bare R, C, M or D number, which the checker reads as a design ID.
- **Which NSW assessment to draft.** The AIAF Platform's own questions are
  not public; draft the 2024 AIAF answers below and ask the agency which
  version it uses (`agency:`). Registration answers are drafted for every
  NSW use case.
- **Never fill an officer's decision.** Officer names, approvals, the risk
  ratings the officer sets, the review committee's outcome and legal advice
  stay `agency:` or `counsel:`. Propose a rating only as `assumption:` with
  its basis.
- **Say which rating you propose.** The DTA tool rates inherent risk at
  section 3 and residual risk at section 12. The NSW Operational Policy uses
  an intrinsic band ("the risk of an AI use case as a function of what the
  use case involves and how it is intended to be used, rather than how it
  may later be managed or mitigated"); the 2024 AIAF rated residual risk.
- **Planned is not in place.** A planned treatment is "planned G<n>", never
  "in place".
- **Who signs each pack document** for a government client: the memo, the
  agency's counsel or Accountable Official; the input pack, its Privacy
  Officer; the questionnaire, its CISO; each form answers document, the
  officer who completes that form (assessing officer or Accountable Owner).
  Add a sign-off row for every other reviewer the record names.
- **The vendor is not the form-filler.** The DTA tool says it is "designed
  for Australian Government staff"; the NSW Operational Policy's registration
  rule "does not apply to third-party suppliers". The agency's officers own
  every form; the consultancy supplies evidence.

Record sources used below: the discovery brief (`docs/discovery/<topic>.md`),
the design (R, C, D and SB IDs), the plan (G and A goals; M, I and W
records), evaluation reports, and the pack documents (`regulatory-memo.md`,
`impact-assessment.md` with its H and B rows,
`privacy-impact-input-pack.md`, `system-card.md`,
`security-questionnaire.md`).

## Commonwealth: the policy behind the forms

All checked 2026-10-26 at <https://www.digital.gov.au/ai/ai-in-government-policy>.

- The DTA Policy for the responsible use of AI in government v2.0 took
  effect on 15 December 2025, and v2.1 minor updates were published on 21
  October 2026. Non-corporate Commonwealth entities must apply it; corporate
  entities are encouraged to; the defence portfolio and the national
  intelligence community are excluded.
- Agencies assess every new use case against Appendix C at design. For
  in-scope use cases, the impact assessment uses the DTA tool or an internal
  process giving "the same (or a higher) risk outcome", started at design
  and finalised, with treatments applied, before deployment. Assessments
  begin for in-scope use cases by 15 December 2026, and existing use cases
  not yet assessed are due by 30 April 2027.
- Inherent high risk: report to the accountable official, govern through a
  board or senior executive, report to the DTA once deployment is decided,
  and review at least every 12 months. Re-validate on a "material change",
  including vendor changes, which agencies "could also ask vendors to provide
  information on ... through contractual mechanisms".
- The Commonwealth **AI Review Committee** gives "expert and non-binding
  advice" before deployment on use cases "assessed as having a residual
  high-risk rating" or "identified as highly sensitive, novel or complex",
  up to PROTECTED. A possible referral is a calendar wait `W`.
- The **Agentic AI addendum** (updated 4 June 2026) is strongly recommended,
  not mandatory.
- The DTA AI model clauses (published 17 March 2025) are the vendor's
  contract duties; their text is reported (Australian Government Solicitor
  description read; the clause text itself not read); not confirmed at the
  source on 2026-10-26.

## Form: DTA AI impact assessment tool

- **Version checked:** v1.0, published 1 December 2025 (the template's
  document control shows one row), checked 2026-10-26.
- **URL:** <https://www.digital.gov.au/ai/impact-assessment-tool>
- **Roles:** the assessing officer completes it and sets the ratings; the
  approving officer approves it, including the inherent ratings; the
  accountable use case owner is a separate policy role. All are agency
  officers.
- **Flow:** sections 1 to 4 are the threshold assessment; if any inherent
  risk at section 3 is medium or high, sections 5 to 12 follow. The 5 by 5
  matrix gives low, medium or high.
- **Known form quirks** (quote as written, never repair): question 1.7 lists
  four usage patterns while Appendix D v2.1 lists seven (decision-making and
  administrative action; analytics; strategic support; workplace
  productivity; workflow automation; image processing; coding); the
  template applies "possible", a likelihood level, to consequence; question
  3.7's "Major" and "Moderate" descriptors are identical. Draft with the
  Appendix D v2.1 names and ask the agency which list its copy uses
  (`agency:`).

| # | Question (paraphrase) | From our records, or who answers |
| --- | --- | --- |
| 1.1 | Use case name, reference, lead agency | Name: design title. Reference and lead agency: `agency:` |
| 1.2 | Assessing officer, use case owner, approving officer | `agency:` for all three; `gap:` until named |
| 1.3 | Others with responsibilities, including external suppliers | Memo Roles; design operations decisions (D); the consultancy as developer, Google as model and cloud provider |
| 1.4 | Plain-language description | System card Intended use; memo System and intended purpose (R, C) |
| 1.5 | Which of the five in-scope criteria apply | Brief harms; decision contracts (C); channels and review share (C, M); data register (brief §4); DTA direction `agency:`; in scope or not `counsel:` / `agency:` |
| 1.6 | Type of AI technology | Model decision (D, pinned model ID); agent topology (D); tools table |
| 1.7 | Usage pattern | Design contracts and channels; usually workflow automation and/or decision-making and administrative action; `agency:` which list |
| 1.8 | Legislative authority for automating an administrative decision | `counsel:` always; facts: decision contracts (C) and the M share reviewed |
| 1.9 | Domain | Brief context; `agency:` confirms |
| 1.10 | Expert contributions | Reviewers on plan goals; security review (SB); evaluation lead (M); agency experts `agency:` |
| 1.11 | Review log | Plan goal history; re-validation triggers from impact-assessment.md Monitoring and review |
| 2.1 | Problem | Brief §1 |
| 2.2 | Purpose and how AI addresses it | Design purpose (R); system card Intended use |
| 2.3 | Non-AI alternatives | Options in the brief; rejected alternatives (D); `gap:` if none |
| 2.4 | Stakeholders (Attachment A aid) | impact-assessment.md Interested parties; threat model for malicious actors; unions and staff `agency:` |
| 2.5 | Expected benefits with analysis | impact-assessment.md B rows; M records, or `hypothesis:` |
| 3.1 | Service accessibility and inclusion | Channels and hand-off contracts (C); system card AI disclosure and hand-off; languages not evaluated |
| 3.2 | Unfair discrimination | impact-assessment.md Adverse impact and equality (M or `gap:`); proxies removed (C) |
| 3.3 | Stereotyping or demeaning representations; defamation | Evaluation reports; grounding and citation contracts (C); system card Limits |
| 3.4 | Harm | Brief harms; H rows; tool tiers and confirmation (C, SB18) |
| 3.5 | Privacy concerns; threshold assessment and PIA | privacy-impact-input-pack.md; `counsel:` high privacy risk |
| 3.6 | Security, data aspects | Data register and classification (D); input pack Model provider data use and Recipients; questionnaire logging (SB14) and incident rows; classification `agency:` |
| 3.7 | Security, system aspects (pretrained model, shutdown, monitoring, servers in Australia) | Model and lifecycle (D); adversarial suite (M, SB17); kill switch (D); hosting and model processing region (D, model page `source:`) |
| 3.8 | Reputation and public confidence | Brief harms; H rows; risk appetite `agency:` |
| 3.1 to 3.8 ratings | Consequence, likelihood, inherent rating and rationale | `assumption:` with basis; the assessing officer sets each (`agency:`) |
| 3.9 | Overall inherent rating (highest of 3.1 to 3.8) | Computed from the proposals; `agency:` approves |
| 4.1 | Assessing officer's recommendation | `agency:`; the pack may propose, for example "full assessment necessary: 3.5 rated medium (assumption: personal information in prompts)" |
| 4.2 | Approving officer's review | `agency:` only; a calendar wait `W` |
| 5.1 | Definition of fairness | impact-assessment.md Adverse impact and equality; acceptance criteria (R, C); the service's fairness policy `agency:` |
| 5.2 | Measuring fairness | M records by group; `gap:` with a goal for adk-agent-evaluation |
| 6.1 | Data suitability, permissions and rights | Data register; RAG and memory design (D); evaluation set provenance; permissions `agency:` |
| 6.2 | Indigenous data | Data register; data custodians `agency:`; usually `n/a:` with reason or `gap:` |
| 6.3 | Suitability of a procured model; contract terms | Model decision (D) with model page and lifecycle; input pack Model provider data use; questionnaire Sub-processors; contract `agency:` / `counsel:` |
| 6.4 | Testing | Evaluation reports; M records; system card Evaluation results and Not yet measured |
| 6.5 | Pilot | Pilot goal (G), acceptance cases (A), pilot M records |
| 6.6 | Monitoring plan | Observability design; impact-assessment.md Monitoring and review |
| 6.7 | Intervening or disengaging | System card Human oversight; approval contracts (SB18); kill switch (D) |
| 6.8 | Operator training | Handover goal; agency training `agency:` |
| 7.1 | APP compliance | Input pack "Australia: APP compliance check"; `counsel:` |
| 7.2 | Where the threshold assessment and PIA are stored | `agency:`; the input pack is the PIA input |
| 7.3 | Security measures; IT Security Adviser | security-questionnaire.md; SB table; ITSA review `agency:` and a wait `W` |
| 8.1 | Stakeholder consultation | Brief interviews (dated sources); community and union consultation `agency:` |
| 8.2 | Public visibility | Public system card; the agency's transparency statement `agency:` |
| 8.3 | Documentation and records across the lifecycle | System card (factsheet); data register (datasheet); decision lineage (C); records retention `agency:` |
| 8.4 | Disclosing AI interactions; non-AI alternative | System card AI disclosure and hand-off; disclosure contract (C); hand-off route and M time to connect |
| 8.5 | Explanations of factors | System card Automated-decision disclosure; grounding and citation (C); trace retention (SB14) |
| 9.1 | Notification when AI materially influenced an administrative action | System card disclosure; memo APP 1.7 table; `counsel:` |
| 9.2 | Challenging AI-influenced administrative actions | System card contest route; internal and external review `agency:` |
| 10.1 | Diversity across the lifecycle | Evaluation set composition (M); stakeholders consulted; `agency:` |
| 10.2 | Human rights alignment | `counsel:` always; the pack lists the facts |
| 11.1 | Accountability mechanisms | Memo Roles; design owners; residual risk acceptance; governance board `agency:` |
| 12.1 | Agency-specific legislation | Memo screen and Australian sections; agency statutes `agency:` / `counsel:` |
| 12.2 | Legal advice: needed, and where stored | `agency:` only; the pack lists its `counsel:` questions, never advice |
| 12.3 | Risk summary: treatments and residual risk per medium or high risk | impact-assessment.md Measures and Residual risk (H to C and SB with status) |
| 12.4 | Overall residual rating | `assumption:` from 12.3; `agency:` sets it |
| 12.5 | Internal governance body review (required if inherent risk is high) | `agency:`; a calendar wait `W` |

## Form: AI transparency statement inputs

- **Version checked:** Standard for AI transparency statements v2.1,
  updated 20 October 2026, checked 2026-10-26.
- **URL:** <https://www.digital.gov.au/ai/ai-in-government-policy/standard-ai-transparency-statements>
- The statement is agency-level and need not list use cases; the agency
  writes and publishes it, reviews it yearly or on a significant change,
  and notifies the DTA. The pack supplies this use case's facts.

| Required content (paraphrase) | From our records, or who answers |
| --- | --- |
| Why the agency uses AI | `agency:`; the use case's purpose from the system card feeds it |
| Usage patterns and domains (Appendix D) | As DTA tool 1.7 and 1.9 |
| Where the public may interact with, or be significantly affected by, AI without human review | Channels and review contracts (C); M share reviewed |
| Monitoring and protection against negative impacts | impact-assessment.md Monitoring and review; system card Human oversight |
| Compliance with the policy | `agency:` |
| Compliance with legislation | Memo screen; `counsel:` / `agency:` |
| When last updated; contact; plain language | `agency:`; the pack flags when this use case changes the agency's AI profile |

## Form: internal AI use case register row

- **Version checked:** Standard for accountability v2.1, updated 20 October
  2026, checked 2026-10-26.
- **URL:** <https://www.digital.gov.au/ai/ai-in-government-policy/accountability>

| Minimum field (paraphrase) | From our records, or who answers |
| --- | --- |
| Use case name; agency reference | Design title; reference `agency:` |
| Description, business objective, product name | System card Intended use; model and product (D) |
| AI technology type | Model decision (D) |
| Lifecycle stage | Plan status |
| Use of the technical standard | Agentic addendum table below; `agency:` confirms |
| Domain and usage pattern | As DTA tool 1.9 and 1.7 |
| Accountable use case owner | `agency:` |
| In-scope criteria met | As DTA tool 1.5 |
| Inherent and residual ratings; date last updated | DTA tool 3.9 and 12.4, set by the agency (`agency:`) |
| High risk only: last and next review dates | `agency:`; a plan wait `W` |

## Form: Agentic AI addendum conformance

- **Version checked:** Agentic AI addendum, PDF last updated 4 June 2026,
  checked 2026-10-26. Strongly recommended, not mandatory.
- **URL:** <https://www.digital.gov.au/policy/ai/agentic-ai-addendum>

| Statement (paraphrase) | Toolkit evidence |
| --- | --- |
| AGT.1 Governance and safeguards: responsibilities, human oversight, explaining decisions, an orchestration layer | Memo Roles; agent and tool ownership (D); approval contracts (SB18); trace lineage; workflow design (D) |
| AGT.2 Memory management | Memory scope, retention and erasure contracts |
| AGT.3 Workflow design: goals, task order, guardrails, self-correction, tools, branches, scale | Design R, D, C; invocation limits and budgets (SB19, SB25); repair loops |
| AGT.4 Routing and data flow between agents | Session-state handoff contracts; A2A or MCP decisions |
| AGT.5 Choice of agent, model and technique | Model decision (D) with lifecycle; instruction design records |
| AGT.6 Continuous evaluation: unexpected inputs, tool, environment and memory interaction | Evaluation reports; adversarial suite (M, SB17); memory replay tests |
| AGT.7 Tools and protocols | MCP allowlist and pinning (SB); A2A cards |
| AGT.8 Ongoing monitoring and a control tower | Observability dashboards, alerts and SLOs; the kill switch |
| Decommissioning | Cleanup and teardown goals |

**Vendor evidence for the DTA AI model clauses** (clause text reported; not
confirmed at the source on 2026-10-26): human oversight (cl 5.1) → system
card Human oversight; training, testing and monitoring for disparity, bias,
hallucination and drift (cl 6.2.4) → M records and evaluation reports; no
ingestion of buyer data into a model (cl 11) → input pack Model provider data
use; an AI risk management system (cl 13) → the NIST AI RMF mapping in the
impact assessment.

## NSW: the policy behind the forms

All checked 2026-10-26.

- **DCS-2026-02**, "Use of Artificial Intelligence by NSW Government
  Agencies", was issued on 30 July 2026, updated on 1 September 2026, is
  mandatory and replaces DCS-2024-04
  (<https://arp.nsw.gov.au/dcs-2026-02-use-of-artificial-intelligence-by-nsw-government-agencies>).
  It mandates the **NSW AI Operational Policy, Final v1.1** (cover date 30
  July 2026; a version table inside reads v1.1 approved on 31 August 2026,
  so re-read it before quoting a date), which replaces the NSW AI Ethics
  Policy and adopts Australia's eight AI Ethics Principles.
- Agencies register **all** AI use cases on the AIAF Platform, which has
  been the mandatory platform for registering and assessing them since 30
  September 2026; registration decides whether a full AIAF assessment is
  needed. Agencies without platform access, and agencies during the
  transition, "continue to apply the existing AIAF Excel-based assessment
  process ... until the platform is fully adopted".
- Risk bands are low, medium, high and critical. Agencies "must refer
  critical and high-risk AI use cases" to the NSW AI Review Committee, by
  email to the AI Secretariat "within 5 business days of completing the
  AIAF"; its advice is advisory and the agency keeps decision-making
  authority.
- Projects with a budget over $5 million, or funded through the Digital
  Restart Fund, get additional central oversight through the Digital
  Assurance Framework; cost alone does not trigger AI Review Committee
  referral.
- The first annual attestation is due by 31 October 2027.
- The Operational Policy is not mandatory for third-party suppliers;
  supplier AI is governed by procurement and contract clauses (ICTA clause
  6.11 and the Core& terms; see [Australia](australia.md)).

## Form: NSW AIAF Platform registration

- **Version checked:** the baseline registration questions published in the
  NSW AI Operational Policy, Final v1.1, Attachment A, checked 2026-10-26.
  The platform's own wording sits behind SectorLink and is not public:
  confirm it with the agency (`agency:`). The policy says the questions
  "will evolve".
- **URL:** <https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-strategy-and-operational-policy/nsw-ai-operational-policy>

| # | Question (paraphrase) | From our records, or who answers |
| --- | --- | --- |
| Reg 1 | Using an agency-approved AI system, platform or product? | `agency:` (approved list); model and hosting decisions (D) |
| Reg 2 | Automates or materially influences consequential decisions about a person? | Decision contracts (C); memo APP 1.7 table; M share reviewed |
| Reg 3 | Elevated risk beyond routine productivity or analytical assistance? | Autonomy and tools (C, SB18); public channel; personal data. An ADK agent with tools embedded in a public-facing service is normally "yes" |
| Reg 4 | Experimental use only, on synthetic, public or non-sensitive data in an isolated environment? | Yes only for a proof of concept on synthetic data (design profile; POC note) |
| Registration | Agency, responsible officer and use case details | Owner `agency:`; description from the system card |

## Form: NSW AIAF self-assessment (2024 framework, Excel and offline process)

- **Version checked:** The NSW AI Assessment Framework, Digital NSW 2024 (88
  pages), checked 2026-10-26. The official PDF is no longer linked from
  digital.nsw.gov.au; the copy read was a mirror, so its provenance is
  reported; not confirmed at the source on 2026-10-26. Questions 14 and 30
  were not fully recovered: ask the agency for its copy (`agency:`).
- **URL:** <https://www.digital.nsw.gov.au/policy/artificial-intelligence/ai-governance-assurance-and-frameworks/nsw-ai-assessment-framework>
- Most questions branch on yes, partially, no, unclear or n/a, each with a
  control (such as "pause the project"), and every answer must be
  explained. Its five sections use the superseded five NSW principles
  (community benefit, fairness, privacy and security, transparency,
  accountability) as headings.

| # | Question (paraphrase) | From our records, or who answers |
| --- | --- | --- |
| Part 1 | Elevated-risk screen: administrative decisions, real-world actions, autonomy, automated decision steps, sensitive data, unintended harms, explainability; "All Generative AI solutions should be classified elevated risk"; buy, embed or develop | Decision contracts (C); tool tiers (C, SB18); workflow design (D); data register; H rows. A consultancy-built agent on Gemini is elevated risk and "develop" or "embed" |
| Part 2 | Human rights prompts; responsible officers (project sponsor, executive sponsor, technical owner, data governance owner, not all one person) | `counsel:` for human rights; officers `agency:` (the consultancy's lead is not a responsible officer) |
| Info | Name, delivery, phase, contributors, next review, goals, problem, why AI | Design profile and plan phase; brief §1; next review a wait `W` |
| 1 | Improves on existing approaches against NSW outcome frameworks | `agency:`; brief KPIs |
| 2 | Non-AI systems considered | As DTA 2.3 |
| 3 | Aligns with legislation (PPIP Act, Anti-Discrimination Act, GIPA Act, State Records Act, HRIP Act, agency Acts) | Memo NSW rows; `counsel:` |
| 4, 5 | Reversible harms; significant or irreversible harms | Correction and override paths (C); H rows; `counsel:` at mid-range or higher |
| 6 | Secondary or cumulative harms | Memory design; H rows |
| 7, 8, 9 | Data selection, availability and quality, representativeness | Data register; RAG decisions (D); evaluation set composition (M) or `gap:` |
| 10, 11 | Diversity, inclusion, gender and minority groups | Evaluation coverage; system card Limits |
| 12, 13 | Performance and fairness targets; monitoring and calibration | Acceptance and release thresholds; observability and scheduled evaluation |
| 14 | Privacy and security by design (text not recovered) | Input pack measures; SB table; `agency:` |
| 15 | PIA completed | privacy-impact-input-pack.md as input; the agency's PIA `agency:` |
| 16 | Consent or authority for using identifiable information | Input pack; `counsel:` |
| 17 | NSW Cyber Security Policy mandatory requirements | security-questionnaire.md Government security policy row; SB table |
| 18 | Sensitive information under PPIP s 19 | Data register; screening; `counsel:` |
| 19, 20 | Community consulted; scope and safeguards public | `agency:`; public system card |
| 21, 22 | Appeal route; explanation of factors, or a reversal process | System card contest route and logic; override (C); `agency:` |
| 23, 24 | Who is responsible for outputs, outcomes, monitoring, data, technical governance, redress; intervention and over-reliance controls | Memo Roles; human oversight design; M override rate; `agency:` |
| Summary | Highest risk per principle | `assumption:` proposals; `agency:` sets them |
| 25 | Mitigations; independent audits for high and very high | impact-assessment.md Measures |
| 26 | Residual elevated risk and next steps | impact-assessment.md Residual risk; `agency:` |
| 27, 31, 32 | Treatments as system requirements or contract controls; their order | Design C and SB; contract `agency:` / `counsel:` |
| 28 | Contract clauses sufficient (ICTA Order Form items) | `counsel:` / `agency:`; the ICTA 6.11 items the design relies on |
| 29 | Questions unanswerable because of supplier products | The pack's `gap:` and `counsel:` lists; Google model page facts with `source:` |
| 30 | Contract framework (text not recovered; reads as ICTA for high risk, Core& otherwise) | `agency:` |
| End | Review committee referral, pilot, records, officers' approval | Waits `W`: referral within 5 business days for high or critical; pilot goal |

## Form: IPC Guide to undertaking PIAs on AI systems and projects

- **Version checked:** IPC NSW guide, December 2024, checked 2026-10-26. It
  says "If an AI system or project involves handling personal information, a
  PIA will typically be required", that "AI-generated inferences about
  individuals are also considered personal information, even if they are
  incorrect", and that PIAs are refreshed before purchase, launch,
  reconfiguration, a new use case or contract renewal.
- **URL:** <https://www.ipc.nsw.gov.au/resources/guide-guide-undertaking-privacy-impact-assessments-ai-systems-and-projects>
- For a NSW agency the input pack's "Australia: NSW IPP and HPP check"
  section carries these rows; a form answers document is optional.

| Principle (guide heading) | Guide's questions (paraphrase) | From our records, or who answers |
| --- | --- | --- |
| IPP/HPP 1 Lawful | Necessary for a function; outputs as "collection through creation" | Input pack flows and categories; generated outputs and memory (C); `counsel:` |
| IPP 2 / HPP 3 Direct | Collected from the person; created information; hidden AI features | Data flows; grounding sources (D) |
| IPP 3 / HPP 4 Open | Notice of collection, recipients and training use; chatbot notice during the conversation | System card AI disclosure; proposed s 10 notice; Model provider data use |
| IPP 4 / HPP 2 Relevant | Each input relevant, accurate, not excessive; free-text risk | Data register; screening contracts |
| IPP/HPP 5 Secure | Access, cross-user exposure, retention to State Records Act minimums, contract terms | SB table; per-user scope (SB03, SB04); retention table; cross-user tests (M); contract `agency:` / `counsel:` |
| IPP/HPP 6 Transparent | Privacy management plan updated for AI | System card; `agency:` |
| IPP/HPP 7, 8 Accessible, Correct | Access to inferences; correction path | Store-by-store access and correction (C or `gap:`) |
| IPP/HPP 9 Accurate | Checks before use; human validation | Evaluation reports (M); review contracts and share reviewed |
| IPP/HPP 10 Limited | Use limited to the purpose; no vendor own-purpose use | Necessity and proportionality; Model provider data use; `counsel:` |
| IPP 11 / HPP 11 | Disclosure; vendor access for the contracted service "is likely to be a 'use'" | Recipients and regions; consultancy access (D); `counsel:` |
| IPP 12 Safeguarded; HPP 14 | Sensitive categories; disclosure outside NSW or to a Commonwealth agency | Screening; processing region (D, model page `source:`); `counsel:` s 19(2) or HPP 14 |
| Risks and mitigations | Inaccuracy, bias, opacity, secondary use, disclosure, retention, re-identification, third parties, breaches | Input pack Risks and measures, one row per guide risk with C and SB IDs and status |

## Documents the agency produces

The pack names these in the memo with their owner and wait, and supplies
inputs; it never drafts them as the official record: the DTA assessment,
transparency statement and register entry; the AIAF registration and
assessment; the review committee referral; the agency's PIA under the IPC
guides; the privacy management plan update; the GIPA contract register
entry; the Part 6A data breach policy entry; the Digital Assurance
Framework gateway review.

## Re-check list (every 90 days, and before each new form answers document)

- The DTA tool's version and document control table; Appendix D and the
  tool's usage-pattern list.
- The DTA policy version; the transparency and accountability standards.
- The agentic addendum's update date.
- DCS-2026-02 and the Operational Policy's version table.
- The AIAF Platform's registration questions (ask an agency with access).
- AIAF 2024 questions 14 and 30, and whether the framework PDF is back on
  digital.nsw.gov.au.
- The IPC AI PIA guide's date.
