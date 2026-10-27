---
document: privacy-impact-input-pack
system: Staff HR assistant (Wattle & Co)
version: design accepted 2026-09-24; build v0.4.1 (M1 to M3)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Wattle & Co Pty Ltd (employer and deployer); Southgate Labs (builder and supporter, APP entity in its own right: counsel to confirm)
for: Privacy Officer (Grace Nguyen)
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# Privacy impact input pack: Staff HR assistant (Wattle & Co)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for Wattle & Co's privacy impact assessment of this system under the
Australian Privacy Principles. The client writes and signs the assessment;
this pack supplies the facts the design and plan record and the questions
only counsel can answer. Not legal advice.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | Real Workday leave, roster and attendance data of employees is read and summarised, and prompts are logged | D3, docs/discovery/hr-assistant.md §3 |

Result: counsel: a PIA is recommended, not required, for a private organisation (source: adk-governance-pack reference australia.md, read 2026-10-28; checked 2026-10-26). Proposed answer: complete one before the pilot because of union and medical information, the manager use in D6 and the US flow in D4. The Privacy Officer decides.

## Processing description

- **Purpose:** answer staff questions about leave, rosters and HR policy, and let managers ask about their team's leave and attendance, to reduce HR service centre tickets (baseline 3,900 a month) (R1, R2, docs/discovery/hr-assistant.md §2).
- **Nature:** reads Workday leave, roster and time APIs, generates answers and attendance summaries with Gemini, logs prompts and answers, and sends error bodies to Sentry (C3, D1, D3, D4). The summary is generated personal information about a team member (C5).
- **Scope:** pilot of 300 staff and 25 managers in NSW stores for 6 weeks (docs/discovery/hr-assistant.md §6); design population 4,800 staff, 2,100 in NSW, 1,600 in Victoria and 1,100 in Queensland (docs/discovery/hr-assistant.md §1).
- **Context:** employees expect HR data to be used for HR purposes; team members whose attendance is summarised are not users of the assistant (R2, D6). gap: whether staff have been told about prompt logging, Sentry or the manager summary.

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| User prompt | Questions, possibly health, family or union information | Staff browser, Entra ID sign-in | Cloud Run, australia-southeast1 | Logged 30 days (D3) | gap: whether logs carry employee ID | Phrase-list masking before logging; 82% of 150 synthetic prompts masked | D2, D3, D7, C4, M2 |
| Model request | Prompt and Workday data in context | Cloud Run | Gemini on Vertex AI, endpoint australia-southeast1 | gap: provider retention and abuse-monitoring storage | n/a: not stored by the client | gap: no screening before the model is recorded | D1 |
| Tool call | Leave, roster, attendance, leave reasons | Agent | Workday read APIs | gap: whether tool results persist in Cloud SQL | gap | Scoped to own record or direct and indirect reports | C1, C2, C3 |
| Logs | Prompts and answers after masking | Cloud Run | Cloud Logging, australia-southeast1 | 30 days | gap | C4 partially in place (M2) | D2, D3, C4 |
| Error tracking | Application errors with request and response bodies | Cloud Run | Sentry project `wattle-hr`, US region | gap: Sentry retention | gap | gap: C4 is not recorded as applying to this path | D4 |
| Consultancy access | Logs and Sentry content | Cloud Logging and Sentry | Southgate Labs engineers, Sydney | Pilot and a three-month support period | n/a: access is by engineers | gap: role-based access and number of engineers not recorded; three engineers named in docs/discovery/hr-assistant.md §5 | D5 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Employees in NSW, Victoria and Queensland (pilot: NSW) | Leave balances and history, rosters, attendance | Leave reasons may mention illness (health information) or union matters; prompts can carry health, family or union information; counsel: sensitive information under the Privacy Act | Workday (read), the person's own prompts, and generated summaries | docs/discovery/hr-assistant.md §3 and §4 |
| Managers | Questions about their team; their own prompts | As above for prompts | Their prompts | R2, D6 |
| Team members summarised by a manager | Clock-in, lateness, absences as summarised | Absence reasons if returned; gap: whether the tool returns reasons to the manager | Workday, then generated | docs/discovery/hr-assistant.md §3, C5 |

## Automated decisions

- **Facts:** the manager decides; the summary lists the records it is built from (C5, D6); gap: manager training, share of summaries checked and override rate. 95% of 60 summaries matched Workday (M3), so about 3 in 60 did not; the record does not say how they differed.
- **Explanation the design can produce:** the list of source records in the summary (C5); gap: an explanation to the team member is not designed.
- counsel: APP 1.7 substantially and directly related decision, from 10 December 2026 (APP 1.7, checked 2026-10-26), and whether the employee records exemption removes it.

## Necessity and proportionality

- Leave, roster and attendance reads are what the stated questions need (R1, R2); union and medical information is not needed for any stated purpose, yet it can arrive in prompts and leave reasons (docs/discovery/hr-assistant.md §3).
- Sending request and response bodies to Sentry goes beyond what error tracking needs; gap: no decision records why bodies are sent (D4). Proposed alternative for the decider: send error type and stack only, or scrub bodies, or use a region in Australia (hypothesis: Sentry offers one; not checked, no network access).
- The manager summary is optional to the stated outcome; the manager guide suggests it for performance conversations (D6). counsel: is this use within reasonable expectations of employees (APP 6; if the Act applies).
- Notices: gap: no staff notice text exists in the record; proposed text is below.
- Access, correction and deletion: gap: no route for a person to see or correct prompts held in logs or Sentry.

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Cloud Logging | Masked prompts and answers | 30 days | gap: erasure of one person's entries not designed | D3 |
| Cloud SQL | gap: content not recorded | gap | gap | D2 |
| Sentry `wattle-hr`, US | Error bodies | gap: not recorded | gap | D4 |
| Evaluation sets | Synthetic prompts (150) and 60 summaries compared manually | gap: whether the 60 summaries used real data | gap | M2, M3 |

## Recipients and regions

| Recipient (processor, service provider, agent or data intermediary, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud (Vertex AI, Cloud Run, Cloud SQL, Cloud Logging) | Cloud and model provider; no processor category in Australian law | australia-southeast1 for the endpoint and hosting; gap: model processing region unread | counsel: use or disclosure (APP 8); gap: contract terms not in the record | D1, D2 |
| Sentry | Error-tracking provider | United States | APP 8 and s 16C overseas recipient; counsel: use or disclosure and sufficiency of any contract; gap: no contract in the record | D4 |
| Southgate Labs | Builder and supporter; APP entity in its own right (counsel) | Sydney, Australia | n/a: no overseas access recorded | D5 |

## Model provider data use

- gap: whether Gemini prompts and outputs are used for training, cached or held for abuse monitoring is not recorded; the model page was not read in this session and the check is proposed as a goal for adk-model-and-output-contracts beside D1.
- gap: the retirement date of `gemini-3.5-flash-001` is unread (D1). Reported, not confirmed at the source on 2026-10-26: Gemini machine-learning processing is offered in australia-southeast1 (source: adk-governance-pack reference australia.md, read 2026-10-28).
- counsel: reliance on Google's statements about training data (D1).

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Union or medical information stored in logs and sent to the US and read by engineers | assumption: likely, because 18% of synthetic prompts were not masked; severe for a person's employment | Phrase-list masking; broader detection | Partially in place, tested locally; planned under G04 (in_progress) | C4, M2 |
| A staff member sees another's data | assumption: low; severe | Tool scoped to verified employee ID | In place, tested locally | C1, G02/A2 |
| A manager reads someone who does not report to them | assumption: low; severe | Supervisory organisation check | In place, tested locally | C2, G02/A3 |
| A wrong or context-free attendance summary affects someone's employment | assumption: possible (95% match, M3); severe | Summary lists source records | In place, tested locally; no measure of manager checking (gap) | C5, M3 |
| Leave reasons or other free text reach a manager | assumption: possible; gap: whether the tool returns reasons | None recorded | gap | docs/discovery/hr-assistant.md §3 |
| Error bodies hold personal data in the US without notice or contract | assumption: likely if bodies include answers; severe | None recorded | gap | D4 |
| Assistant changes leave or rosters | assumption: very low | Read-only integration user; no write tool | In place, tested locally; granted 2026-10-08 | C3, W1 |

## Australia: APP compliance check

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection (3.3 consent for sensitive information; generated or inferred information is collected) | Summaries are generated personal information; union and medical details can be typed in | counsel: is the log a collection of sensitive information without consent; gap: no consent step | C4, M2, C5 |
| APP 5 notice | gap: no notice text recorded | counsel: confirm the proposed notice below | D3, D4 |
| APP 6 use and disclosure (primary purpose; secondary use) | Workday data used for the assistant; logs kept "for support and quality review" | counsel: is quality review within reasonable expectations | D3 |
| APP 8 and s 16C overseas recipients | Sentry in the US; Gemini endpoint in Sydney | counsel: use or disclosure; gap: contract, retention, scrubbing, model processing region | D1, D4 |
| APP 10 quality; APP 11 security and destruction | 97% of 240 leave balances correct, 95% of 60 summaries matched; logs 30 days | gap: no Sentry retention or destruction rule; gap: SB table lists only SB01, SB03 and SB05 | M1, M3, D3, SB01, SB03, SB05 |
| APP 12 and 13 access and correction (memory, logs, evaluation sets) | Logs and Sentry hold prompts | gap: no search by person | D3, D4 |

- **PIA required?** Recommended for a private organisation (counsel: is this a high privacy risk project).
- **Employee records exemption:** counsel: if s 7B(3) applies to Wattle's handling, the APPs may not bind Wattle for these records, but they bind Southgate Labs for its handling (source: adk-governance-pack reference australia.md, read 2026-10-28; checked 2026-10-26). Wattle's own policy duties to staff are not settled by this pack.
- **Statutory tort (commenced 10 June 2025, checked 2026-10-26):** intentional or reckless invasion only; engineers reading union or medical text in logs is a risk line (D5, M2).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Leave balances, history, rosters | Answer staff questions | Workday | Google Cloud, Southgate Labs | None recorded for Google; gap: model processing region | 30 days in logs | R1, D1, D3 |
| Attendance (clock-in, lateness, absences) | Manager summaries | Workday, generated | Managers, Google Cloud, Southgate Labs, Sentry | United States (Sentry) | 30 days in logs; gap: Sentry | R2, D4 |
| Prompts and answers, including any health, family or union information | Support and quality review | The person; generated | Southgate Labs engineers, Sentry | United States (Sentry) | 30 days in logs; gap: Sentry | D3, D4, D5 |

- **Proposed staff notice (APP 5) and privacy-policy addition, including APP 1.8 entries:** "The HR assistant answers questions using your Workday leave, roster and attendance records. Your questions and its answers are kept for 30 days for support and quality review and can be read by Southgate Labs engineers in Sydney. Error reports that can include parts of your questions and answers are sent to Sentry in the United States. Please do not type health, family or union information into the assistant. Managers can ask it to summarise the attendance of people who report to them; the summary lists the records it uses and is not a decision. To see or correct information, contact the Privacy Officer." Every sentence depends on a decision still open (D4 scope, retention at Sentry, access route) and must be revised once these are settled (system-card.md; counsel: confirm).

## Questions for counsel

- counsel: Does s 7B(3) apply to Wattle's use of the assistant, and does Southgate Labs hold an APP entity's duties; needed before W6.
- counsel: Is the Sentry flow a use or a disclosure under APP 8, and what contract is needed; needed before the 2026-11-27 pilot decision (docs/discovery/hr-assistant.md §6).
- counsel: Is holding union and medical information in logs a collection requiring consent under APP 3.3; needed before the pilot decision.
- counsel: Is the manager summary a use within reasonable expectations, and can a wording change cover it under APP 5; needed before W5.
- counsel: Is a PIA required for this project; the Privacy Officer decides (W3 is separate).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy Officer (Grace Nguyen) | this document | pending | pending |
