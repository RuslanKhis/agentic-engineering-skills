# Re-entry record, autumn validation, 2026-10-27

Offline diagnosis only. No provider call was made, no file under `attempts/`, `probes/`, `campaign/` or
`runs/` was edited. Earlier summaries keep their "diagnosis at the time" text; this record supersedes
them by linking, not rewriting.

**Not executed:** this session had no shell, so none of the code or tests below has been run. Every
"expected" below is from reading the code, and the first action next session is
`python -m unittest discover -s tests -t .`.

## Experiment/revision and hashes

- Cohort A, six development cases fixed 2026-10-06 (rules: `campaign/cohort-rules.md`, unchanged).
- Revisions run: batch1 `71c0d4a` (writer-v5/draft-v4/review-v3), batch2 `9be22f1` (writer-v6/draft-v4/review-v3),
  batch3 `c41e8b0` (writer-v7/draft-v6/review-v4).
- This revision: writer-v8, draft-v7, review-v4. The workspace is not a git repo, so there is no commit id.
- Source/config/dataset hashes: **not computed** (no shell). Before any dispatch, record
  `manifest(spans)["sha256"]` per case, the sha256 of `pipeline/*.py`, `pyproject.toml` and the serialized
  request for each stage.
- Only `cases/dev/PA-2026-0141` exists in this workspace. Fixtures for 0144, 0146, 0149, 0152, 0158 are absent,
  so nothing below was checked against them.

## Prior attempts; first reached failure; later known blockers

| Batch | First reached failure | Later known blockers (not reached, or not recognised) |
| --- | --- | --- |
| 1 (0/6) | review: policies T2/T2.1/ENV3 "not addressed". Retrieval passed only the first policy document. Fixed in `9be22f1`; `case_spans` now takes all four documents. | none identified |
| 2 (5/6) | 0146 review: R2 cites `LP-H4@2024:p31:7`; the sentence continues on `:8` and the reason relies on it. | Condition-template enum (below) was not yet in play; it arrived with draft-v6. |
| 3 (0/6) | writer, 4 of 6: HTTP 400. 2 of 6: 120 s deadline, no response, no receipt. | (a) `stages.export` reads `c["text"]`, which no draft shape contains, so any `approve_with_conditions` draft would have raised KeyError at export. (b) `validate_review` accepts `verdict: accept` beside an `unsupported` claim and does not check claim `span_ids` against the draft. (c) The stop rule (two consecutive same-stage failures) did not stop batch 3: all six cases were sent. `workflow.py` runs one case and has no batch driver, so the rule is not enforced in code. |

## Failure classification and evidence

1. **Batch 3, four 400s: transport/schema incompatibility, deterministic.** `probes/writer-schema-probe-2026-10-22.json`
   sent the exact serialized draft-v6 schema and got 400 "enum value at properties.conditions.items.properties.template
   contains a line break". The condition templates in `schemas.py` contain `\n`. The same schema went out on every
   writer call, so the "gateway instability" diagnosis at the time was wrong for these four.
2. **The other probe, `review-generic-probe-2026-10-22.json`, does not support "failures were transient".** It sent a
   one-field `{"ok": boolean}` schema on the review route. It says the gateway accepts some structured output. It says
   nothing about draft-v6, draft-v7 or the real review schema. Its conclusion is withdrawn; the file is kept as is.
3. **Batch 3, two timeouts (0146, 0152): cause unknown.** A 400 returns quickly, so the same schema fault does not
   explain a 120 s silence unless the gateway behaves differently per request, and nothing here shows that. They are
   not evidence of "instability" either. Usage and charge are uncertain, not zero (ledger: two reservations of
   $0.40, still `reserved`).
4. **Batch 2, 0146: copying/coverage plus an unrepresentable granularity.** Spans are one physical line. LP-H4 line 7 is the
   first half of a sentence ending on line 8. Likewise the 4.0 m rule is lines 4-6 and its "unless" clause is
   lines 5-6. A one-line citation of either is a partial quotation, which the reviewer correctly rejected. Batch 2's note
   "not reproduced locally" is now reproducible (test below). The reviewer's judgement was right; this is a draft/citation
   defect, not a review error.
5. **Why local tests were green every time:** the suite used a scripted transport that returns 200 for any payload, a
   hand-written draft with no conditions, and a reference draft that cited `LP-H4@2024:p31:4` alone (a partial quotation
   of the 4.0 m rule that omits its "unless" clause). None of them serialized the real schema against anything
   that could reject it, none exercised conditions through export, and the reference draft was itself defective.

## Retained minimal reproducers

- 400: `tests/doubles.RejectingTransport` rejects any request whose schema has a line-break enum value. It models only the
  one rejection recorded in the probe. Test `test_rejecting_transport_still_rejects_the_draft_v6_shape` keeps the
  negative control.
- Batch 2: `test_citing_one_line_of_a_wrapped_sentence_is_invalid` (cites `p31:7` alone: error; `p31:7` and `:8`: valid).
- Export blocker: `test_export_renders_condition_text_from_the_template_id`.
- Timeouts: no reproducer. Retained as an unknown.

## Honest passing reference, through the actual schema/checker/runtime

`DRAFT`/`REVIEW` in `tests/test_pipeline.py` for PA-2026-0141 now cite `LP-H4@2024:p31:4-6`, run through
`run_case` with the real `ChatModel`, `RejectingTransport`, checkpoint store and ledger. It is a hand-authored double,
not a provider response, and it is not evidence of provider behaviour. It has no conditions, conflicts or gaps. The
neighbour's light objection (NBR-1) is non-decisive at 3.6 m against the 4.0 m limit, so a truthful reference may carry no gap for
it; a human should confirm that against the officer's label before it is used as a gold reference.

## Negative controls

- False association / unsupported evidence: unknown span id (existing test); one-line citation of a wrapped sentence (new);
  unknown condition template id (new).
- Missing safeguard: **not covered.** No test for a draft that omits the "unless" clause's consequence, or for a review that says
  `accept` while a claim is `unsupported`. See remaining unknowns.

## Changed boundary; offline regressions; remaining unknowns

Changed (expected, unrun):
- `pipeline/schemas.py`: `draft-v7`; `CONDITION_TEMPLATES` is a dict, the schema enum holds the ids
  (`COND-PLANS`, `COND-GLAZING`, `COND-AMS`) under `template_id`, text is server-owned; `missing_continuations()`; `validate_draft`
  takes the ordered spans.
- `pipeline/stages.py`: writer passes spans to the validator; export renders text from `template_id`.
- `pipeline/prompts.py`: writer-v8 (cite every line of a wrapped sentence; choose conditions by `template_id`).
- `tests/doubles.py`, `tests/test_pipeline.py`: 6 new tests, 2 reference citations corrected.
- Spans, cohort rules, ledger, `runs/`, pins and the `google.adk` import boundary untouched.

Commands to run: `python -m unittest discover -s tests -t .` (expect 5 old + 6 new, all passing; **not run**).

Remaining unknowns:
- Whether the gateway accepts the whole draft-v7 schema. The 400 names only the first rule it hit, and the next rule may
  be behind it. Only a real send answers this.
- Whether the review route accepts the real `REVIEW_SCHEMA` (only a one-field schema was probed).
- Cause of the two timeouts; whether a 120 s limit is adequate for this prompt size.
- `validate_review` weaknesses (b above) are not fixed; a model's support label is a judgement, not an oracle.
- Whether `missing_continuations` (a lower-case-follows heuristic) over-rejects honest drafts on the five fixtures I cannot see.
- Unsettled $0.80 (two batch 3 reservations). They need the provider's usage record to settle; do not zero them.

## New hypothesis and distinguishing observation

H1: batch 3's four 400s were caused by the line-break enum alone, and with draft-v7 the writer call is accepted.
Distinguishing observation: a 200 with a body that parses and passes `validate_draft` with spans. A second 400 names
a different rule (H1 incomplete); a timeout leaves H1 untested and the batch 3 timeout cause open.
H2: batch 2's rejection was a one-line citation of a wrapped sentence. Observation: on 0146, the writer's R2 cites both lines
(or its draft is rejected at writer stage by `missing_continuations`, which names the span).
Neither is decided by a cohort pass count.

## Phases and their purpose

| Phase | Purpose | Class |
| --- | --- | --- |
| 0 offline repairs and regressions (this session) | remove known structural blockers | local fix, no spend |
| 1 canary: writer + review on PA-2026-0141, real serialized requests, one send each | test the transport contract and latency for both routes | **diagnostic**; not counted in the cohort |
| 2 fixed cohort A, six cases, normal path | outcome evidence under the unchanged rules | **release evidence**, only if the Phase 1 gate passes |

## Route, identity, inputs, trial IDs

Route `https://gateway.example.invalid/v1/chat/completions`, writer and review `gemini-3.5-flash`, writer-v8/draft-v7/review-v4,
temperature 1.0, max_tokens 8192, timeout 120 s (same as batch 3). Phase 1: case PA-2026-0141, trial `canary-1`. Phase 2:
PA-2026-0141, 0144, 0146, 0149, 0152, 0158, trial `b4-1` each, in that order. The five missing fixtures must be present and hashed before Phase 2.

## Admission and stop/continue rules (declared before any send)

- Phase 1 passes only if both calls return 200, the writer JSON passes `validate_draft` with spans, the review JSON passes
  `validate_review`, a usage receipt is recorded for each, and each call finishes inside 120 s. It establishes the observed
  contract, not cohort quality.
- Phase 1 fails on any 400, timeout, validator error or missing receipt. A failure ends the plan; the error body is stored and
  nothing is retried or sent to "see if it passes now".
- Phase 2 runs only after a Phase 1 pass. Cohort rules apply as written: $0.80 per case, 120 s, two consecutive failures at
  the same stage stop the batch, no replaced cases, no added cases, no retries, no early stop beyond the stop rule. Unrun cases
  stay `not dispatched` and count against the fixed denominator of six.
- Because no code enforces the stop rule, a driver or a manual gate must enforce it. **Not built.**
- Report attempted / completed / published / matched-the-officer-label / missing separately.

## Submissions, sends, limits

Phase 1: at most 2 sends (1 writer, 1 review), 0 retries. Phase 2: at most 12 sends (6 writer, 6 review), 0 retries.
Retries count as actual sends if they ever happen, and none are planned.

## Cost, allowance, authorization

- Reservation per `workflow.RESERVE_USD`: writer $0.40, review $0.25, so $0.65 per case. Phase 1 $0.65; Phase 2 $3.90 (ceiling $0.80/case = $4.80).
  Total reserved at most $4.55, ceiling $5.45.
- Ledger (read, not changed): allowance $25.00; settled $7.57; reserved and unsettled $0.80; remaining per the ledger's formula $16.63.
- Authorization: AP-1 (Morgan Hale, 2026-10-06) covers "cohort A batches within the allowance". `AGENTS.md` additionally requires
  the owner's approval for *that run*. Whether AP-1 covers a diagnostic canary on a cohort case is unclear. **Assumption: no
  approval exists for either phase; no send until the owner says so.** A different route or a case outside cohort A needs a
  new approval under the cohort rules.

## Ledger and evidence destination

Use `campaign/ledger.json` and its existing `reserve`/`settle`. Before dispatch, reserve for every call that may be sent; settle only
from the provider's usage record (dedupe by receipt id); a timeout without a receipt stays `reserved` and uncertain. Record the
canary as a separate run id (for example `2026-10-xx-canary1`) and write it under a new `runs/<id>/` directory; never reuse or edit an
existing run directory. Later reconciliation of batch 3's two reservations is a linked event, not a rewrite.

## Questions for the owner (not answered; assumptions stated)

1. Do you approve the Phase 1 canary ($0.65 reserved) and, on a pass, Phase 2 ($3.90 reserved)? *Assumed: no.*
2. Does AP-1 cover a diagnostic canary on PA-2026-0141 that is not scored in cohort A? *Assumed: not without confirmation.*
3. Where are the fixtures for the other five cohort A cases, and the officer labels? *Assumed: they exist elsewhere and
   will be supplied unchanged.*
4. Can the provider's usage records for the two timed-out batch 3 calls be obtained, so their $0.80 can be settled or released?
   *Assumed: not yet; both stay uncertain.*
5. Is a one-line "wrapped sentence" citation acceptable to a planning officer, or must a citation always include the whole sentence?
   *Assumed: the whole sentence is required, per the batch 2 review finding.*
