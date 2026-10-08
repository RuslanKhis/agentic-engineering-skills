# Calibrate document support judgments

Read this when claims rely on selected passages or a citation checker appears to
accept unsupported conclusions. The bundled cases use invented workshop records
and rules, not real policy or customer data. Their expectations are **AI-authored,
provisional and not reviewed by a domain-competent human**. Use them to reveal
specific evaluator mistakes; obtain substantive human review before adapting them
into a domain quality gate.

## Keep the evidence dimensions separate

Give the judge the observation, case context, selected excerpt and available full
source/context. Full-source context can expose an incomplete selection; it cannot
silently substitute for the passage actually cited. If the answer is elsewhere on
the same page, select and retain that complete span before claiming support.

| Dimension | Labels | Question |
| --- | --- | --- |
| `source_identity` | `valid`, `invalid` | Does the ID resolve to the stated document/page and does each quoted span occur there? |
| `span_completeness` | `complete`, `incomplete`, `unresolved` | Does the selected evidence unit preserve its answer, qualifications and relevant boundaries? A complete but unrelated field is still complete. |
| `applicability` | `applicable`, `not_applicable`, `unresolved` | Does the selected content concern this object and govern this situation? This does not decide whether the observation is true. |
| `contrary_evidence` | `none`, `contradiction`, `unresolved` | Does the available record contradict the observation, or leave competing evidence unresolved? Missing evidence alone is `none`. |
| `support` | `supported`, `unsupported`, `contradicted`, `unresolved` | Is the observation justified by the selected evidence in context? An empty field is unsupported; conflicting equally authoritative records are unresolved. |

Identity is mechanically checkable. The remaining judgments require the task's
meaning and evidence. Neither a matching substring nor the model's own
`supported` label supplies that judgment independently. Preserve the per-observation
judgments when several observations share a passage; a single source-level pass
cannot justify all of them. Here `supported` is the only accepted conclusion.

Adjudicate rubric ambiguities before using all five dimensions as a strict gate.
For invalid citations, specify whether secondary dimensions assess the supplied
text or only authenticated evidence. For pixel estimates, distinguish an
unsupported physical value from a contradicted claim that a measurement method
is valid. The provisional `s11` and `s17` labels expose these choices: retain
disagreements and rationales, and review the convention instead of rerunning the
judge until it agrees. Both remain rejection controls for conclusion support.

## Run the synthetic contrasts

Use [source-support-cases.json](../assets/source-support-cases.json) as judge input
and keep [source-support-expectations.json](../assets/source-support-expectations.json)
out of inference. The source registry contains full synthetic pages. Each case
specifies the exact selection and, where applicable, known contrary evidence.
The [diagram](../assets/source-support-diagram.svg) contrasts a written dimension
with an unscaled pixel measurement; this is not an OCR or visual-model benchmark.

The cases cover exact quotation and paraphrase, valid but unrelated citations,
question-only versus question-and-answer spans, an omitted policy exception versus
the qualified passage, two observations sharing one excerpt, written dimensions
versus pixels, and contradiction versus blank or conflicting records. Valid IDs,
truth somewhere in the page and complete quotations each have rejection controls.

From the installed skill directory, run the dependency-free demonstration:

```bash
python3 scripts/check_source_support.py --demo
```

It compares deliberately weak ID-only and literal-substring judges against the
authored expectations and reports false accepts, false rejects and mismatches by
dimension. An always-reject control exposes missing positive coverage. Label replay
checks the scorer can report agreement; **it is not an independent semantic judge**.
The demonstration makes no model or network calls.

For a real calibration, produce JSON with a `judgments` list containing one object
per `case_id`, the five dimensions above and a brief `rationale`. Then run:

```bash
python3 scripts/check_source_support.py --judgments .adk-evidence/source-judgments.json
```

The scorer reports every expected case, rejects missing/duplicate/unknown cases and
invalid labels, and exits nonzero for disagreement. It compares labels; it does not
derive semantic truth or evaluate the rationale. Record judge settings, rubric
version and disagreements separately. Review false accepts and false rejects with
a domain-competent human where possible before relying on an adapted judge.

## Forward-test the instructions

In an isolated directory give a fresh agent the skill, the cases and diagram, plus
this task: “Assess whether these selected passages justify their observations;
return judgments using the five-dimensional rubric.” Withhold the expectations
and prior results from that agent. Inspect its rationale and score its output only
afterward. A useful check accepts the full-answer case while rejecting the same
fact cited to only the form question, and accepts a supported paraphrase without
accepting a statement whose cited source contradicts it.

Report helper tests, fresh-agent judgment results and any paid/live calibration
separately. These small development contrasts demonstrate known failure modes,
not general document-review accuracy or retrieval completeness.
