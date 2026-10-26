# Portability planning: checks and fresh-agent trials

*26 October 2026. Skill: `skills/adk-portability-planning`, with the
designer's lock-in question and portability goal and the engineer's routing.
Research: [AWS](../research/portability-aws-2026-10-26.md),
[Azure](../research/portability-azure-2026-10-26.md),
[agent frameworks](../research/portability-agent-frameworks-2026-10-26.md),
[design principles](../research/portability-design-principles-2026-10-26.md).*

The toolkit's primary path is unchanged: the designer designs a Google ADK
application on GCP and the engineer builds it with the existing specialists.
Portability planning is optional and runs only when the user answers yes to
one scope-gate question.

## What was checked

| Layer | Result |
| --- | --- |
| Package validation (`scripts/validate_skills.py`) | 26 packages, 0 errors, 0 warnings; the designer's `SKILL.md` stays at 500 lines |
| Checker suite (`skills/adk-portability-planning/tests`) | 73 tests pass: a filled claims-triage fixture passes; the unfilled template fails on placeholders; each rule fails on its own mutation (sections, classes, invented IDs, undated or future sources, unsupported hours, prices and dates, overpromises with and without a nearby negation, missing dimension rows, Terraform, Bicep, CloudFormation and cloud CLI blocks, an uninstalled specialist) |
| Designer suite (`skills/adk-system-designer/tests`) | 63 tests pass, 8 in `test_document_goals.py`: a portability ticket with `(deliverable)` items and `contracts: []` passes `check_tickets.py`; the tag fails on implementation, presentation and governance tickets; a missing skill fails; the phase gate skips the portability goal; `check_schedule.py` reports a build goal that waits for it; the handoff's example front matter and acceptance pass the lint |
| Full `scripts/check_repo.py` (repo `.venv`, Python 3.12.9) | Passed: 1,130 tests run, 1,070 pass, 60 optional SDK checks skipped on the branch; after merging `main` at `ff87b9c` (the governance APAC and Canada work), 1,163 run, 1,103 pass, 60 skipped |
| Evaluation cases | 8 activation cases (3 positive, 5 near-miss) and 4 scenarios (no concern, concern, ticket carried out, unrelated goal); structure valid, model activation not run |
| Provider and framework facts | Read at official sources on 26 October 2026 (research notes); an independent reviewer re-checked eight decision-relevant claims at source and confirmed all eight |

Activation and scenario cases are labels, not measured selection; no
repeated fresh-session routing run was made.

## Independent review

A fresh reviewer read `git diff main...HEAD` with the brief and no answers.
It raised one blocker (this record and the README counts were still
placeholders), eleven should-fix items and nine nits. All should-fix items
were changed:

| # | Finding | Change |
| --- | --- | --- |
| 2 | The phase gate held the phase until the optional assessment finished | `plan_status.py` skips portability goals in the gate |
| 3 | Hyphenated, spelled-out and year-scale estimates and invented dates passed; one `M<n>` or "assumption" cleared a whole line | Patterns widened; the exemption must sit in the figure's own cell or sentence |
| 4 | A negation anywhere on a line cleared an overpromise; quoted stakeholder words failed | Negation counts only just before the phrase; quotes and blockquotes are skipped; three phrases added |
| 5 | Dimensions were a substring search | One table row per dimension, matched on its first cell |
| 6 | A design decision could drop out of the classification | Warning per uncited design `D` ID |
| 7 | CloudFormation, Bicep and cloud CLI blocks passed | Rejected |
| 8 | Two scenario assertions contradicted the skill | Reworded |
| 9 | Register pins disagreed with the references | Rows updated to the 26 October reads |
| 10 | LiteLLM caveat omitted ADK 2.13.0's cap below the compromised 1.107.0 | Added with the `pyproject.toml` source |
| 11 | `(deliverable)` also loosened presentation and governance tickets | Limited to portability tickets |
| 12 | Reference class labels were not the checker's class names | Each cell leads with an exact class |

Nits taken: the question reads the same in the designer and the
delivery-profiles table; "No recommendations.", "PydanticAI" and e-mail
addresses no longer trip the checker; source age warns after 90 days, as
the references say; the Agent Framework 1.0 date is now verified; the
fixture cites the AgentCore page that states the ARM64 contract.

## Trials

Four fresh general-purpose subagents (model inherited from the coordinator,
Claude Opus 5.5; reasoning setting not recorded). Each was given the path of
the installed skills directory and of one project, and one user request. No
expected answers were given. A and B played a user from an answer sheet in
the user's words; the trial logged each question it would ask.

| Trial | Fixture (sha256 prefix) | Request | Answer that matters |
| --- | --- | --- | --- |
| A | Empty repo, `README.md` `edcdcc5c` | `/adk-system-designer` HR policy assistant over 120 PDFs, design and plan | Lock-in: "No, … we're a Google shop" |
| B | Same | Same | Lock-in: "Yes … the parent company may standardise on AWS … stuck with Google's agent framework" |
| C | B's output, committed: design `887ddc43`, plan `010e0f41`, ticket `512e86c0` | `/adk-engineer Carry out docs/tickets/hr-policy-assistant/G05.md …` | none |
| D | B's output, committed | `/adk-engineer Carry out G03 from docs/plans/hr-policy-assistant.md.` (stop before editing) | none |

C's ticket is B's ticket (`d6c28e14`) brought up to the fix that B's
friction led to (A4 by `git hash-object` instead of a commit base, status
`ready`); nothing else in it changed. Fixtures and outputs are retained
under the coordinator's session scratchpad (`trials/caseA` to `caseD`),
outside the repository.

### Outcomes, inspected by the coordinator

| Assertion | A | B | C | D |
| --- | --- | --- | --- | --- |
| The lock-in question is asked once, in the scope-gate turn, without provider questions | Pass (question 9 of 9) | Pass | | |
| The design stays GCP + Google ADK | Pass | Pass | Pass: recommendation is "keep the build, hold an exit plan" | |
| No answer: no portability goal, ticket or skill load | Pass: scope-gate row "No"; plan says why | | | |
| Yes answer: portability goal, primary skill `adk-portability-planning`, `blocked_by: []` | | Pass (G05, phase 1) | | |
| Its ticket is written although no tickets were asked for, and lints clean | | Pass (`check_tickets.py` exit 0) | | |
| No build goal waits for it | | **Fail, fixed**: G04 waited on G05 to order one developer's work | | |
| The engineer routes the ticket to the skill | | | Pass | |
| A separate assessment with all fifteen sections, five dimensions and dated sources | | | Pass: 20 sources, 14 re-read that day; checker exit 0 | |
| Relative effort with drivers, no invented hours or prices; "not fully portable" stated | | | Pass | |
| Design and plan unchanged; no code; recommendations wait for a checkpoint | | | Pass: hash `8e98f0ef` before and after; one recommendation, for `adk-workflow-design` | |
| An unrelated goal routes to its own specialist, with no portability load or adapters | | | | Pass: `adk-memory-architecture`; reasons cite the plan and both skills |

### Friction log and what changed

| # | Friction (trial) | Change |
| --- | --- | --- |
| 1 | A4's `git diff <base>` cannot run on an uncommitted design, so the ticket was written `blocked` (B) | A4 compares `git hash-object` values recorded before and after; the ticket is `ready` from the start |
| 2 | The skill asked for an "accepted" design while the designer keeps designs marked draft (B) | A draft is enough; its open decisions go to Open questions |
| 3 | A build goal waited for the portability goal to order one person's work (B) | `check_schedule.py` reports it; the handoff says so |
| 4 | The import grep's unquoted `--include=*.py` aborts under zsh (C) | Quoted |
| 5 | The engineer's `.adk-evidence/` rule against a ticket that may touch only the assessment (C) | Checker output goes in the ticket's Evidence |
| 6 | `plan_status.py`'s next prompt against the skill's checkpoint prompt (C) | The skill says its checkpoint prompt replaces it |
| 7 | The template always had an Azure column (C) | Guidance: keep a column only for a target in scope |

Not changed, outside this feature, recorded for a later pass: the designer
trials' notes on wait entries without a goal type, expert hours in the
schedule helper, the overridden-default field note against
`field-feedback.md`, server-to-server callers in the web defaults, and
user-typed personal data in the governance trigger (A, B); the memory
specialist's local recipes for atomic index swaps and lockfiles (D); and
`plan_status.py` suggesting `/adk-engineer` for a wait or a presentation (A, C).

## Limits

- One trial per path. These are smoke trials of the workflow, not measured
  selection rates; the activation cases have not been run.
- Trials A and B simulated the user from an answer sheet. Whether a live
  user answers the lock-in question in one word, as intended, is not
  observed.
- Trial D stopped before implementation by instruction; it shows routing,
  not that G03 builds unchanged.
- The checker checks form. Whether each claim in an assessment is right
  still needs a human reviewer; C's acceptance A3 was shown by its source
  table, not by an independent re-read.
- Provider facts move quickly. The references carry
  `<!-- verified: 2026-10-26; re-check every 90 days -->`, and the
  validator's freshness check (merged from `main`) now requires that line in
  this skill's references and warns when one is due; a test covers the
  missing-marker case. The re-check procedure in
  `docs/maintenance/law-refresh.md` is written for law references; provider
  references are re-read at the sources each one lists.
