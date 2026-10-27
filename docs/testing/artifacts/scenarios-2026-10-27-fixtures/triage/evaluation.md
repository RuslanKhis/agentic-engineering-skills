# Triage: evaluation group (batches eval1, eval2)

Scope: every assertion that failed by majority, and every pass on split votes, in eval1 and eval2
(adk-agent-evaluation scenarios plus the designer rerun designer-names-google-product-skills).
Skill paths are relative to `skills/`. The run had no shell, so assertions that require running
tests, helpers or dispatch counters, with no "or says it could not" escape, are classed (b).

| Scenario | A# | Votes | Class | Evidence | Proposed action |
| --- | --- | --- | --- | --- | --- |
| evaluation-preinference-contract-qualification | A1 | FFF | c | Skill loaded (1 reference read). contract-qualification.md covers tracing requirements to source, instruction, schema and validator; the agent traced by reading but left the duplicate-label requirement unresolved. | none |
| evaluation-preinference-contract-qualification | A2 | FFF | b | "Demonstrates ... passing ... failing" requires executing the reviewed references and invalid controls; no shell. | flag: needs a shell |
| evaluation-preinference-contract-qualification | A3 | FFF | c | The preflight was added but duplicate labels were left unrepaired; contract-qualification.md:106 covers repairing the earliest boundary. | none |
| evaluation-preinference-contract-qualification | A4 | FFF | c | provider-compatibility.md separates native validation, wire schema and semantic support; the answer named the wire-schema concern only. | none |
| evaluation-preinference-contract-qualification | A5 | FFF | b | "Exercises normal orchestration/storage" requires running; the judge credited honest reporting but failed on "not exercised". | flag: needs a shell |
| evaluation-preinference-contract-qualification | A6 | FFF | c | contract-qualification.md:106 "Once staged execution stabilizes" sets out the staged-then-frozen schedule; the agent proposed one run. | none |
| evaluation-bound-spans-versus-model-paraphrase | A1 | FFF | a | No skill loaded (skills_loaded [], 0 skill files). Description (evaluation SKILL.md:3-12) names "strict result checks" but nothing on quote/citation support or saved-stage repair, so a bug-fix prompt is not routed to it. | owner: description wording; see defects |
| evaluation-bound-spans-versus-model-paraphrase | A2 | FFF | a | Same routing miss; source-support-calibration.md covers paraphrase and mutations but was never read. | as above |
| evaluation-bound-spans-versus-model-paraphrase | A3 | FFF | a | Same routing miss; the exception-removing claim was still accepted. | as above |
| evaluation-bound-spans-versus-model-paraphrase | A4 | FFF | a | Writing served-route tests with a counted double needs no shell; it was not done, and the skill was not loaded. | as above |
| evaluation-bound-spans-versus-model-paraphrase | A5 | FFF | a | Same routing miss; dependency manifests for saved stages are in progressive-validation.md. | as above |
| evaluation-progressive-downstream-repair | A1 | FFF | b | "Reproduces the retained failure offline" requires running; no skill loaded either (skills_loaded []). | flag: needs a shell; routing noted under (a) |
| evaluation-progressive-downstream-repair | A2 | FFF | b | "Runs focused regressions ... checks" requires execution. | flag: needs a shell |
| evaluation-progressive-downstream-repair | A3 | FFF | b | "using actual dispatch counters" requires execution. | flag: needs a shell |
| evaluation-progressive-downstream-repair | A4 | FFF | a | The scheduling is gradeable from text; progressive-validation.md (SKILL.md:68) covers it, but the skill was not loaded, and the agent framed a downstream continuation as a review rerun. | owner: description routing |
| evaluation-progressive-downstream-repair | A5 | FFF | b | Requires reporting an executed offline continuation; nothing could run, so it is unsatisfiable as worded. | flag: needs a shell |
| evaluation-reviewer-coverage-versus-uncertainty | A3 | FFP (pass) | c/b | Applicability was reasoned from facts, but the positive-control replay was never run (no shell). | none |
| evaluation-improve-decisions-error-analysis | A1 | FPF | b | "Runs the baseline through the plainest contract" requires execution; categorising from saved outputs was done. | flag: needs a shell |
| evaluation-improve-decisions-error-analysis | A3 | FFF | b | "re-measures on all development cases" requires execution. | flag: needs a shell |
| evaluation-improve-decisions-error-analysis | A4 | FFF | c | Skill loaded; quality-iteration.md covers prompt restructuring and leave-one-out exemplars; not done. | none |
| evaluation-improve-decisions-error-analysis | A5 | FFP (pass) | c | Holdout untouched; quality-iteration.md:167 "the report names the largest remaining category". | none |
| evaluation-generalization-and-deliverable-budget | A3 | PPF (pass) | c | Named in substance without the word "overfitting". | none |
| evaluation-generalization-and-deliverable-budget | A4 | FFF | c | progressive-validation.md:92 "record that as a plan failure" covers it; skill not loaded (0 files), and the agent proposed drawing on unreserved allowance. | none (routing noted) |
| evaluation-recovery-is-not-full-route-acceptance | A6 | FFF | b | Conditional "When delegating, ..."; the agent had no subagent tool and did not delegate. progressive-validation.md:118 covers the split. | flag: conditional on a capability the run lacks |
| evaluation-incident-regression-fail-to-pass | A3 | PFP (pass) | c | Rule stated in full; one dissenting vote. | none |
| evaluation-incident-regression-fail-to-pass | A4 | FFF | c | evaluation-design.md:20 shows base_ref/reference_fix; the commits are in docs/incidents/INC-0412.md, but the agent wrote UNKNOWN. | none |
| evaluation-self-hosted-harnesses-mlflow-deepeval-opik | A1 | PFP (pass) | c | Covered; "pinned" loosely. | none |
| evaluation-self-hosted-harnesses-mlflow-deepeval-opik | A2 | FFF | c | provider-compatibility.md:101-103 "an exception raised by the scorer is a row with an error and no value (NOT RUN)"; the agent read 3 files but omitted it. | none |
| evaluation-self-hosted-harnesses-mlflow-deepeval-opik | A4 | FFF | c | Judge pinned and Vertex used, but no contrast with a Gemini API key and no statement that Runner tests stay primary; covered in SKILL.md and live-evaluations.md. | none |
| evaluation-judge-agreement-and-harness-bridge | A1 | FFF | c | evaluation-design.md:57 "α of 1 is perfect agreement, 0 is chance, below 0 systematic disagreement"; not repeated. | none |
| evaluation-judge-agreement-and-harness-bridge | A2 | FFP (pass) | c | Mostly covered. | none |
| evaluation-judge-agreement-and-harness-bridge | A3 | FFF | c | result-auditing.md:9 "treats NaN, a raised error and a missing row alike: not run, never passed"; not stated. | none |
| evaluation-judge-agreement-and-harness-bridge | A4 | FFF | c | evaluation-design.md:51 "record its model, settings, rubric version"; rubric versions not pinned. | none |
| evaluation-collateral-damage-no-op-control | A3 | PFF | a | grep over skills/adk-agent-evaluation finds no "no-op"/"do-nothing" control. evaluation-design.md:78-86 ("Grade the end state") never says to run a do-nothing scripted model through every grader, or that collateral-damage checks pass a no-op by construction. | owner: add the no-op control to evaluation-design.md step 2-4 |
| evaluation-collateral-damage-no-op-control | A4 | FFF | c | live-evaluations.md:7 "a server change is a new baseline"; the agent recorded versions but not that rule. | none |
| evaluation-tool-fault-matrix-and-resilience | A2 | FFF | c | execution-evidence.md:37 "match_args does not match ... the real tool runs"; the agent read 5 files and named only the misspelt tool. | none |
| evaluation-tool-fault-matrix-and-resilience | A4 | PPF (pass) | c | Covered. | none |
| evaluation-repeated-trials-pass-hat-k-and-end-state | A3 | FFF | c | evaluation-design.md:82 "Component rewards multiply ... A run that ended for any reason other than ... scores zero ... not evaluated"; not applied. | none |
| evaluation-repeated-trials-pass-hat-k-and-end-state | A4 | FFF | c | "A judge change is a new baseline" is at adk-release-engineering/references/versioning.md:18 (installed for this scenario), but not in the evaluation skill; the agent gave only a vague note. | none (cross-skill pointer would help; see defects, minor) |
| evaluation-underwriter-labelling-session | A1 | FFF | c | expert-review.md and SKILL.md:50 "One decision-maker named"; the agent left it "to be named". Arguably correct to ask the user, but the assertion wants a named role. | none |
| evaluation-underwriter-labelling-session | A2 | FFF | b | "Runs scripts/label_agreement.py" requires a shell; the hand-computed kappas matched the real output. | flag: needs a shell (best Bash-enabled candidate) |
| evaluation-selected-source-support | A3 | FFF | c | source-support-calibration.md:37 distinguishes "unsupported physical value from a contradicted claim"; h12 labelled contradicted. Skill not loaded (0 files). | none |
| evaluation-selected-source-support | A5 | FFF | c | AI-only framing is in evaluation-design.md:59 and validation.md:44; not stated. Skill not loaded. | none |
| designer-names-google-product-skills | A2 | FFF | b | Judge reason: "the goals that would need them (such as G11) are truncated". eval2 ran before the head-and-tail clip (f2af40c), so the judge saw a cut plan. Skill covers it at SKILL.md:315-319. | re-judge on unchanged evidence |
| designer-names-google-product-skills | A4 | FFF | c | implementation-handoff.md:74-76 covers install/fetch at execution; not stated, and no execution-scope prerequisites recorded. | none (re-judge with A2) |

## Suspected skill defects

1. **adk-agent-evaluation, description (SKILL.md:3-12): routing.** Three plain-language repair
   prompts loaded no skill at all: bound-spans, progressive-downstream and generalization (0 skill
   files read). selected-source-support also loaded nothing. The description names "strict
   result checks" and "evaluation reliability", but nothing about source/quote support checks,
   saved-stage (paid) recovery or holdout budget decisions. Those workflows exist in the body
   (SKILL.md:68, progressive validation; source-support calibration), but the description does
   not reach them. This is borderline: some of the miss is agent behaviour (other groups show
   plain prompts going straight to code).
2. **adk-agent-evaluation, `references/evaluation-design.md` "Grade the end state" (lines
   78-86): missing no-op control.** It never says to run a do-nothing scripted model through
   every case's graders and require each action case to fail it. It also never notes that
   collateral-damage (nothing-else-changed) assertions pass a no-op by construction. grep for
   "no-op", "do-nothing" and "by construction" finds nothing in the skill.
3. **Minor, adk-agent-evaluation:** "a judge change is a new baseline" lives only in
   adk-release-engineering `references/versioning.md:18`. The evaluation skill's judge-pinning
   lines (evaluation-design.md:51) do not point to it.

## Fixture or assertion defects

- **Shell-dependent, flag rather than loosen:**
  - preinference A2 and A5
  - progressive A1, A2, A3 and A5 (A5 is unsatisfiable without an executed continuation)
  - improve-decisions A1 and A3
  - underwriter A2: the best candidate for a deliberate `--agent-tools` run with Bash, recorded as unconfined
- **evaluation-recovery-is-not-full-route-acceptance A6:** the assertion is conditional on delegating, but the scenario agent has no subagent tool. Flag it, or grade "when delegating" as not applicable when the agent did not delegate.
- **designer-names-google-product-skills A2/A4:** judged on a truncated plan (pre-clip runner). Re-judge on the unchanged evidence; no fixture change is needed.
- No fixture files were changed.
