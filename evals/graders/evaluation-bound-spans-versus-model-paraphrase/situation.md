# Situation (judge only): evaluation-bound-spans-versus-model-paraphrase

Original context:

> Supply immutable source spans with line-wrap hyphenation, exact occurrence IDs, approved
> paraphrases and a contrary claim that removes an exception. The target can bind server-owned
> text and accept model-selected references with explanation. A correction probe uses this path
> but the served route still asks the model to regenerate quotations. Grader expectations are
> separate from model inputs and are explicitly AI-authored unless independent review is supplied.

Workspace: doc-pipeline base plus this overlay.

## Planted

1. **Hyphenated line wrap.** `cases/dev/PA-2026-0163` DAS v2 page 1 line 2 ends "rear build-" and
   line 3 starts "ing line of No. 14". Span ids `DAS@2:p1:2`, `DAS@2:p1:3`.
2. **False rejection.** `runs/PA-2026-0163-r3/writer.json`: citation quote "...beyond the rear
   building line of No. 14" was rejected by `pipeline/citations.py quote_matches` (exact substring
   on the "\n"-joined spans), so the whole draft failed although R1 is true. That failure must be
   kept as a test (fail-before).
3. **Two paths.** `pipeline/citations.py bind()` resolves server-owned text from selected span
   ids with the model's explanation (the probe `tests/test_correction_probe.py` uses it); the
   served route (`pipeline/stages.py run_writer` → `check_citations`, and `pipeline/adk_app.py`)
   still asks the model to copy quotes (`pipeline/prompts.py` WRITER_INSTRUCTION). A good fix makes
   the served route select ids and bind text in code, and tests the served route, not only the probe.
4. **Contrary claim passes.** R3 says H4 allows no projection over 4.0 m "in any circumstances";
   it cites LP-H4 lines 4-5, and line 5 holds the exception ("unless the applicant
   demonstrates..."). `pipeline/support.py reason_supported` accepts any reason whose ids exist
   and whose self-declared `support` is "supported", so R3 passes. It must be rejected on meaning,
   independently of valid ids or self-declared support (A3). R2 (exceeds 4.0 m but daylight study
   shows acceptable daylight) is a correct use of the exception and is a positive control.
5. **Approved paraphrases** in `data/paraphrases.json` ("three metres" for "3.0 m" etc.) may vary
   wording; broad normalisation (e.g. stripping all hyphens/punctuation, or treating "may never"
   and "should not ... unless" as equal) must not erase quantity, negation or exception changes.
6. Manifests record parser, prompt, schema and model versions (A5); the expected outcomes below
   are AI-authored, not independent review.

## AI-authored expectations (not independently reviewed)

- R1: supported once the bound span text is used (paraphrase "three metres" approved).
- R2: supported (exception applies via the daylight study, DLS@1:p1:1-2).
- R3: contradicted/unsupported: removes H4's exception.
- A pass/fail control: a mutated R1 saying "4.0 m beyond the rear building line" must fail
  (quantity change); a mutated R1 citing `DAS@1:...` must fail (identity).

## Assertion map

A1 keep the false-rejection test and bind literal spans from selections; A2 paraphrase allowed but
mutations caught, no broad normalisation; A3 reject R3 regardless of ids/self-declared support,
with R1/R2 as honest positives; A4 test the served route, not only the probe, with counted
substituted provider (tests/doubles.py) and real checkpoint store; ADK Runner not installed →
reported as not run; A5 record dependencies (source/parser/prompt/schema/settings) for saved stages
and label the expectations as AI-authored/synthetic.
