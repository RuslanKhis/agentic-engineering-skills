# Implementation plan: support-email triage PoC

Status: draft. Ready goals identified (G00 is a human task; G01 is ready once G00 is done).
Architecture: [docs/architecture/support-email-triage.md](../architecture/support-email-triage.md)
Continuation source of truth: this plan

## Destination and constraints

**Destination:** by the end of today, the repository holds a frozen run over the
50 anonymised emails, a one-page summary with dev and holdout accuracy, and a
static demo page. Non-goals and deferred controls are listed in the design.

**Authorization:** this plan authorizes only local code and a bounded number of
model calls on the user's own key (600 calls at most).

**Inherited pins:** `google-adk==2.8.0` (assumed, confirm in G01),
`gemini-3.8-flash`, and prompt version `v1`, which is bumped on each change.

**Inspected:** an empty repository. Every module below is **proposed**.

Proposed layout:

```
triage/agent.py      # CATEGORIES constant, TriageResult schema, build_agent()
triage/prompt.py     # instruction text rendered from CATEGORIES; PROMPT_VERSION
triage/runner.py     # CLI: --split dev|all, --only-failed, call counter, writes results/run-<ts>.jsonl
triage/score.py      # joins labels.csv, accuracy and confusion per split, writes results/summary.md
triage/demo.py       # renders demo/index.html from a run file
tests/               # offline tests (scorer: no ADK; agent and runner: need ADK)
data/                # emails.jsonl, labels.csv (user-supplied)
```

## Implementation map

| Decision | Component and integration point | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1, D7 | `LlmAgent` built in `triage/agent.py` and driven by `Runner` + `InMemorySessionService` in `runner.py`, with one session per email | None | `adk-workflow-design` | Constructor names against the installed ADK pin |
| D2 | `output_schema=TriageResult`. Validation and one repair happen in `runner.py` | Gemini API | `adk-model-and-output-contracts` | Schema enforcement on the Gemini API backend |
| D3 | Instruction in `prompt.py`, rendered from `CATEGORIES` | — | `adk-agent-instructions` | Rendered-request test |
| D5 | Model ID constant in `agent.py` | Gemini API key | `adk-model-and-output-contracts` | Price and rate limit on the day |
| D6 | `score.py` with `labels.csv` splits | — | `adk-agent-evaluation` | — |
| Budget | `RunConfig(max_llm_calls=2)` plus a global counter | — | `adk-operational-guardrails` (light) | — |

## Goals and dependencies

| ID and goal | Type | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- |
| G00 Prepare data, taxonomy and labels | discovery (human) | — | none (user task) | ready |
| G01 Triage all dev emails end to end, measured | implementation | G00 | `adk-model-and-output-contracts` | blocked on G00 |
| G02 Improve on dev, then run the frozen full set | implementation | G01 | `adk-agent-evaluation` | proposed |
| G03 Build and rehearse the demo pack | implementation | G02 | `adk-agent-evaluation` | proposed |

The time budget for the 5 hours is G00 0:30, G01 1:45, G02 1:15, G03 0:45 and a buffer of 0:45.

### G00 — Prepare data, taxonomy and labels (≈30 min, user)

- **Outcome:** `data/emails.jsonl` (`id, subject, body`) holds 50 rows. `data/labels.csv` (`id, category, split`) has 15 `dev` and 35 `holdout` rows, stratified by category. One extra adversarial dev email is optional. The category list with one-line definitions goes in `data/categories.md`.
- **Decision it settles:** A4, A5 and A6.
- **Acceptance:** 50 unique IDs, every label is in the category list, and every category has at least one dev email.
- **Stopping condition:** if labelling takes over 40 min, label only the categories and mark ambiguous emails `other`.

### G01 — Triage all dev emails end to end, measured

- **Outcome and linked decisions:** running `python -m triage.runner --split dev` produces a valid row for each dev email, and `python -m triage.score` prints dev accuracy. Implements D1–D5 and D7.
- **Scope:** the agent, schema, prompt v1, runner with budget, scorer and offline tests. Excludes the demo page and prompt tuning.
- **Implementation route:** the proposed modules above. The runner never reads `labels.csv`.
- **Prerequisites:** G00. Install `google-adk` (confirm the pin, assumed 2.8.0) and set `GOOGLE_API_KEY` in a local `.env` that git ignores.
- **Primary skill:** `adk-model-and-output-contracts`, for the output schema, repair budget and pinned model.
- **Supporting skills:** `adk-agent-instructions` for the prompt and rendered-request test; `adk-agent-evaluation` for the scorer and dev/holdout discipline.
- **Acceptance:**
  1. A scripted model returning prose, fenced JSON or an off-enum category gives 1 repair and then a `contract_failure` row, never a guessed category.
  2. A model that always fails stops at 2 calls per email, and the global counter halts at the cap.
  3. The agent has no tools.
  4. The scorer gets the right accuracy on fixture rows.
  5. A live dev run produces 15 rows (or 16 with the adversarial email) with zero contract failures.
  6. The ADK pin is recorded and the constructor names are confirmed against it.
- **Verification:** `pytest tests/`. The scorer tests run without ADK; the agent and runner tests need ADK. The live dev run is bounded at ≤ 32 calls.
- **Execution scope:** local code plus live calls on the user's key, within the 600-call cap.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/support-email-triage.md. Read docs/architecture/support-email-triage.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Improve on dev, then run the frozen full set

- **Outcome:** each iteration gets one dated row in `results/summary.md` with error categories before and after. Categories: `wrong_category`, `invented_commitment`, `missed_placeholder`, `tone`, `needs_human_wrong`, `contract_failure`. The final frozen run on all 50 gives the holdout accuracy and a confusion table.
- **Scope:** at most 2 iterations, each making one change (prompt definitions, tie-break rules, an exemplar, or the model). Holdout rows are never inspected before the final run.
- **Primary skill:** `adk-agent-evaluation`, using the quality-iteration loop.
- **Supporting skills:** `adk-agent-instructions` for prompt changes.
- **Acceptance:** the final run file records the prompt version and model ID on every row. The holdout is scored exactly once. Any change made after that triggers a re-run, or the summary states that it wasn't re-run.
- **Status:** proposed.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/support-email-triage.md. Read docs/architecture/support-email-triage.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Build and rehearse the demo pack

- **Outcome:** `demo/index.html` (static) lists all 50 emails with the email, category, rationale, `needs_human`, draft and a dev/holdout marker. The holdout accuracy is at the top. An optional live email runs in `adk web`, with the pre-computed page as the fallback.
- **Primary skill:** `adk-agent-evaluation`, so the page is regenerated from the final run only.
- **Supporting skills:** none.
- **Acceptance:** the page opens offline, its numbers match `results/summary.md`, and the rehearsal shows 5 hand-picked emails, including the adversarial one and one failure.
- **Status:** proposed.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/support-email-triage.md. Read docs/architecture/support-email-triage.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| `demo/index.html` | Per-email results from the frozen run |
| `results/summary.md` | Dev iterations, holdout accuracy and known limits |
| this design | Method and deferred controls |

## Open decisions for further planning

See the design's Open decisions table. A4 (taxonomy) and A8 (data policy) are the two that block work.

## Resume here

- **Next goal:** G00, the user's data preparation. It is ready now. G01 follows.
- **Read first:** the design, then this plan.
- **Next action:** export the 50 samples to `data/emails.jsonl` and write `data/categories.md`.
- **Continuation prompt (after G00):**

```text
/adk-engineer Carry out G01 — Triage all dev emails end to end, measured — from docs/plans/support-email-triage.md.
Read docs/architecture/support-email-triage.md and preserve its accepted decisions.
Use adk-model-and-output-contracts with adk-agent-instructions and adk-agent-evaluation.
Work within local code and at most 600 model calls on my Gemini API key, verify the G01 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```
