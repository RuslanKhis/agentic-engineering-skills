# Discovery and presenter skills · 15 October 2026

This records how `adk-discovery` and `adk-presenter` were built and what the
checks establish. Both skills are new; nothing here compares them with a
no-skill baseline, and no live model evaluation or cloud operation was run.

## Method

- **Research first.** Four parallel subagents each wrote a dated
  primary-source note: [opportunity discovery](../research/ai-opportunity-discovery.md),
  [technology-fit triage](../research/technology-fit-triage.md),
  [stakeholder presentations](../research/stakeholder-presentations.md) and
  [case studies and Google programs](../research/case-studies-and-google-programs.md).
  Each separates what a source establishes from what it recommends; the
  skills' references cite the notes rather than repeating the bibliography.
- **Package.** Each skill has a `SKILL.md`, references, assets, a
  standard-library helper with unittest tests, Codex display metadata and a
  licence. The discovery helper adds up the portfolio scores and reports
  what blocks the handoff; the presenter helper checks a deck outline for
  evidence per slide, numbers without a source, stage coverage, timing from
  the notes' word count, and, on a case study, wording Google's co-branding
  guidelines do not allow.
- **Wiring.** The designer reads a discovery brief as answered scope, asks
  who approves the next step and when, and plans presentation goals at phase
  boundaries; its handoff table, delivery profiles and plan template carry
  both skills. The router's table sends discovery and presentation requests
  to them. The README gained a "Where to start" table, a Journey C and two
  catalogue entries; the handoff guide gained the discovery and presentation
  sections.
- **Evaluation cases.** Eight activation cases (two positives and two
  near-misses per skill) and two contextual scenarios were added to
  `evals/`; their structure is validated, their selection is not measured.
- **Fresh-agent trials.** Two subagents, each with only the skill files and
  a synthetic scenario, followed the skills and wrote a friction log. The
  discovery trial simulated a product owner at a media company with funnel
  counts by step; the presenter trial built a synthetic record (brief,
  compact design, plan with two acceptance cases marked not run and an open
  decision) and prepared the production-approval decks for both audiences.
  Artifacts: [discovery](artifacts/discovery-presenter-2026-10-15/discovery/)
  and [presenter](artifacts/discovery-presenter-2026-10-15/presenter/).

## Results

| Check | Result |
| --- | --- |
| Skill packages | **22 validated**, zero errors or warnings |
| Evaluation input structure | 65 activation cases and 55 scenarios valid |
| Offline helper suites | **688 tests** passed, **59 optional SDK checks skipped**, including 10 discovery and 16 presenter helper tests |
| Discovery trial | Brief produced with four candidates, a chosen first use case (`llm` fit: one model call behind a short form, code looking up price and availability), a measured baseline and counter-metrics, and the designer's prompt; helper exit 0. Ease rated **3 of 5**, 20 friction items |
| Presenter trial | Business and technical outlines passed the deck check on the first run; every number traced to the record; the two not-run cases and the open decision appeared on their own slides and in the ask; the agent made the funding ask conditional because the record held no production estimate. Ease rated **4 of 5**, 16 friction items |

## What the trials found, and what changed

| Finding | Change |
| --- | --- |
| Three disagreeing copies of the designer prompt (skill, handoff reference, template) | One prompt, in the handoff reference, with a sponsor and decider slot; the brief and the closing message copy it |
| The helper was to be run before the brief existed, and the template spelled its path wrongly | The skill starts the brief before ranking; one command spelling with `$SKILL_DIR` everywhere; the template has a slot for the helper output |
| The rough-area opener was a stance, not a question; no split between must-ask and optional questions | Each mode names its opener row; the question table has a "when" column (always, if not inferable, before handoff) |
| A fourteen-item sentence duplicated the template's section 4 | The skill says "fill section 4 completely" and the template holds the fields |
| The stakeholder sentence asked discovery for a cost estimate the handoff forbids; hybrids had no fit rule | The cost slot now defers to the design; a hybrid takes the fit of its model-driven step |
| Vendor pricing and lifecycle numbers inside a discovery reference | Replaced by ownership statements; the designer estimates cost |
| A template link relative to the skill, dead once the brief is saved in a project | Plain text |
| The ranker stripped underscores from identifiers | Only surrounding emphasis is stripped; regression test added |
| The presenter asked for the decider before reading the record that held it | The record is read first; asks cover only what it leaves open |
| No rule for arithmetic on recorded numbers | Allowed when both inputs and the operation are on the slide in the estimate voice; stacked assumptions are not |
| The storyline's appendix advice contradicted the checker's timing warning | Appendix slides are tagged and excluded from timing; the checker also estimates spoken minutes from the notes at 130 words a minute |
| No front-matter keys or file names for the decider, the date, the memo and the pre-wiring table | `decider:` and `date:` keys (the checker warns when missing); `decision-memo.md` and `pre-wiring.md` beside the outline |
| The memo template demanded criteria the record may lack | Propose from the last thresholds, marked "proposed, not yet agreed" |
| "State the demo build" assumed a demo existed; nothing on statistical noise | Say when there is no demo; a rough margin rule (one over the square root of n) with a title that says "within the margin" |
| The checker missed "8 of 10" counts and printed "$500" as "$5" | Count and full-currency patterns added, with tests |
| Technical outline for a proof of concept read as if the controls existed | A note that most operations slides will say "not yet built; G<n>", and that they stay |

Not changed: the discovery conversation still reads about 900 lines of
instruction before the first question. The trial judged the structure sound
and the length the cost; a later pass may move the question table into the
skill and shorten the references.

## Second round, same day

Three more research notes were added ([slide craft](../research/slide-craft.md),
[speech craft](../research/speech-craft.md) and
[why AI projects fail](../research/why-ai-projects-fail.md)) and folded in:
the presenter gained a speech reference (bottom line first, one case on the
story spine, three reasons, refuted failures, timings per stage, rehearsal
checklist, question protocol) and a slide-craft reference (assertion-evidence
slides, chart and diagram rules, a per-slide checklist), with checker
warnings for hype words, over-long titles and bodies, and notes that overrun
the minutes at 150 words a minute; the discovery skill gained a stall-causes
reference, a stall-checks table and new brief fields (two-voice problem
statement, data register, workflow before and after with validation points,
correction loop, embedding rule, senior owner and people plan), and offers
the proof-of-concept approval deck when it finishes; the designer now asks
which of the three reviews (before the build, after the proof of concept,
after production) need a presentation and writes each as a goal and ticket;
Journey C in the README carries the final-results stage.

## End-to-end trials · 16 October 2026

Two simulated projects ran through every stage: discovery, the
proof-of-concept approval deck from the brief alone, the design with
presentation goals and tickets, the approval deck again from the full
record, then production approval, final results and a public case study
after the simulated user reported the tickets complete. One started from a
rough idea (selling advertising to small businesses), the other from no use
case at all (a logistics firm whose director did not know how AI works).
Interruptions from a sleeping laptop split each run across several fresh
agents that continued from the files on disk. Reports, transcripts and every
document produced are under [the trial artifacts](artifacts/end-to-end-2026-10-16/).

| Stage | Rough idea | No use case |
| --- | --- | --- |
| Discovery | done earlier, 3 of 5 | 3 of 5 |
| Approval deck from the brief | 4 of 5 | 4 of 5 |
| Design, plan, tickets | 3 of 5 | 2 of 5 |
| Approval deck from the full record | 3 of 5 | 4 of 5 |
| Production approval | 4 of 5 | 3 of 5 |
| Final results | 3 of 5 | 4 of 5 |
| Case study | 4 of 5 | 3 of 5 |

What worked: every handoff carried what the next stage needed; the
designer turned the brief's decision calendar into presentation goals and
waits; no slide in either project carried a number without a source; the
not-run acceptance cases and open decisions reached the slides and the asks;
the no-use-case run picked order intake for the right reason (the largest
reported hours, inputs that exist, a person before every effect), explained
the choice in plain words and named a customer order form and the TMS
vendor's own intake as non-AI alternatives; the case-study reference was
rated the most useful single document.

What changed as a result: the checker's word budgets were widened for
technical decks and the ask slide, tables and appendix slides are no longer
budgeted, decimals count as one word, and code spans are not read as hype;
the notes timing now expects about two thirds of the slot; the
final-results ask became optional; memos and pre-wiring are named per stage;
a `--prose` mode lints case-study text; the plan gained numbered measurement
and incident records (`M1`, `I1`) that `adk-engineer` writes and the checker
accepts as citations, so results after a pilot are citable by ID; the
designer's compact form now agrees with its skill on the schedule helper,
one file, the failure grid and ticket length, and its cost reference gives a
symbolic formula usable without live prices; discovery's ranker warns on an
estimated baseline, the brief names the single decider, the publicity
approver and the Google Cloud relationship, and the baseline is measured on
the scope production will reach; the presenter outlines handle no demo,
proof-of-concept profiles with deferred observability, information-only
reviews and an external IT firm as the technical audience, and the question
bank has results-review and case-study questions.

Not changed: the designer's skill is still long for a four-week proof of
concept, and later presentation stages still repeat the same mechanics
(memo, pre-wiring, premortem) by design. The fixes were not re-trialled.

## Limits

One run per trial, one synthetic scenario each, the agents' own friction
logs and ratings, and the skills loaded from files rather than discovered by
a fresh host. The fixes were applied after the trials and have not been
re-trialled; the two trial decks and the trial brief still pass the updated
helpers. Selection from descriptions, host behaviour across clients and the
quality of a real discovery conversation remain to be measured.
