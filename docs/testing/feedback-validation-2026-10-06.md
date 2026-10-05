# Feedback round 3: making the output good, not only verified

*6 October 2026 · What changed, what the checks establish, what remains untested.*

The third feedback round came from a time-boxed planning assignment judged on
unseen cases. Rounds 1 and 2 had fixed how an application verifies itself;
the reviewer's note was about what the application does: performance on unseen
cases, handling of scans, tables and drawings, depth of retrieval, safeguards
an officer sees, and the prompting approach. This record lists the changes
made for each recommendation and the evidence behind them.

## Changes by recommendation

| Recommendation | Change | Where |
| --- | --- | --- |
| R1 Scope gate | Three scope-gate questions open the interview; answers and deferred controls recorded at the top of the design; proportionality rule with a worked example; one-line check in the entry skill and README step 1 | `adk-system-designer/SKILL.md`, `references/design-decisions.md#size-the-first-slice-to-the-judge`, `assets/system-design-template.md`, `adk-engineer/SKILL.md`, README |
| R2 Quality loop | New reference: labelled development set, baseline, error categories as data, one change per iteration, prompt skeleton, leave-one-out exemplars, two-stage model escalation, reasoning effort as a factor | `adk-agent-evaluation/references/quality-iteration.md`; routing row in `adk-engineer`; evaluation description claims the branch; five exclusions point at it |
| R3 Generalisation | Deliverable-first, deliverable-budget and cross-case rules; two new evidence-gate rows; generalising acceptance criteria; reserved deliverable line in the campaign envelope | `progressive-validation.md`, `evaluation-design.md`, `live-campaigns.md`, design template |
| R4 Ingestion | New reference, four real-byte synthetic PDFs with a generator, a standard-library qualification report (density, route, origin, dimensions and scale statements, reading order, image budget) | `adk-memory-architecture/references/document-ingestion.md`, `assets/ingestion-fixture/`, `scripts/make_ingestion_fixture.py`, `scripts/qualify_ingestion.py` |
| R5 Retrieval | New reference and helper: heading units with page spans, screening, FTS5 BM25, deterministic reference lookup, one bounded second round, RRF hybrid, sufficiency report, gold-set recall | `adk-memory-architecture/references/retrieval-strategy.md`, `assets/retrieval-gold.json`, `scripts/local_retrieval.py` |
| R6 Safeguards | New reference and helper: documents as data, five in-code consistency rules, warning triage, abstention, adversarial review prompt | `adk-workflow-design/references/content-safeguards.md`, `scripts/draft_consistency.py` |
| R7 Stage contracts | Coverage-output and identity-and-limits columns; one bounded upstream request before failing | `adk-workflow-design/references/orchestration.md` |
| R8 Reader budget | Living evaluation summary, raw runs as data, ADRs for architecture only, context-file ceiling, "what the reviewer reads" in the plan template | `execution-evidence.md`, `implementation-plan-template.md`, `live-campaigns.md` |
| R9 Voice and example | Prohibitions converted to recipes in the four most-used entry files; spanning walkthrough; six scenarios and five activation cases | `evals/scenarios.json`, `evals/activation.json`, `docs/integrations/quality-judged-build.md` |
| R10 Build order | Alternative seven-step sequence beside the ticket walkthrough | README |

## What the checks establish

```bash
.venv/bin/python scripts/check_repo.py
```

Run on macOS with Python 3.12.9 on 6 October 2026. The package validator
accepted all 13 packages. The memory suite passed 57 tests with one skip
(optional `pypdf` path); the new workflow draft-consistency suite passed 18;
the repository runner now selects it as a third workflow job. The walkthrough's
commands were executed against the fixtures: the ingestion report routed the
scanned page to OCR or vision, the retrieval run resolved the SPD table and
scored recall 1.0 on the synthetic gold set with precision 0.5 and two listed irrelevant hits on the splay question at k=4, and the contradictory draft exited
1 while the corrected draft exited 0.

These are offline fixture and helper checks on synthetic data. They establish
that the mechanisms behave as described and that the packages are well formed.

## Fresh-agent trials

Two fresh general-purpose agent sessions ran the R1 and R2 maintainer tests
against the repository files, with the skill given by path because the copy
installed under the user's home directory predates this round. No expected
answers were supplied. Both passed on their artifacts, which are retained
unedited:

| Trial | Record | Result |
| --- | --- | --- |
| R1 scope gate on the planning brief | [r1-scope-gate](artifacts/feedback-round-3/r1-scope-gate/README.md) | Scope gate at the top, ten deferred controls with reasons, goals ordered probe → ingest → retrieve → draft and baseline → iterate → freeze and holdout; no revisions, export or hosting goals. Limitation: 567 lines of design and plan for a four-hour brief, now addressed by a document-size rule in the designer. |
| R2 "improve the decisions" | [quality-iteration/trial-1](artifacts/feedback-round-3/quality-iteration/trial-1/README.md) | Error analysis recorded as data before any edit; contract failure repaired first; first quality change targeted the largest category (retrieval), explicitly not a checker; seven measured iterations with one reverted; 3/5 to 5/5 on the double. |

## Voice census

Control words per thousand (do not, never, cannot, must not, is not, does
not, insufficient, not a, only when, separate), before → after the pass:

| File | Before | After |
| --- | --- | --- |
| adk-workflow-design/SKILL.md | 23.1 | 10.6 |
| adk-agent-evaluation/SKILL.md | 12.2 | 10.8 |
| adk-memory-architecture/SKILL.md | 11.5 | 5.3 |
| adk-operational-guardrails/SKILL.md | 11.5 | 9.7 |
| adk-system-designer/SKILL.md | 10.8 | 5.8 |
| rag.md | 22.1 | 5.5 |
| live-campaigns.md | 15.2 | 4.2 |
| review-contracts.md | 14.2 | 5.1 |
| orchestration.md | 14.0 | 4.8 |
| progressive-validation.md | 12.6 | 3.0 |
| checkpoint-reuse.md | 12.1 | 2.9 |
| evaluation-design.md | 11.6 | 3.0 |

Every one of the twelve files now carries at least one "for example", and the
seven references each gained a code or record block. Hard guardrails
(authorisation, deletion, credential exposure, version-bound SDK facts) were
kept and paired with the target behaviour.

## What remains untested

- The other new scenarios (version N versus N-5 budget decision, header-only
  scan, SPD table lookup, contradictory draft) and the five activation cases
  have not been run by a fresh agent; the two trials above are explicit
  file-path invocations, not natural activation.
- No OCR engine, vision model, embedding model or provider call was exercised;
  the R2 trial's model is a rule-based double.
- The fictional policies, drafts and gold set received no domain review.
- The census covered the five entry files and seven references, not the whole
  collection.

Record the first fresh-agent trials beside this file when they run, keeping
failed trials and the exact prompts.
