I couldn't run anything: Bash is disabled in this session. I wrote `scripts/agreement_alpha.py` but have not executed it, and its self-test against the published Krippendorff example (nominal .743, ordinal .815, interval .849) has not run either. The figures below that I computed myself are hand sums read from the CSVs.

## 1. Measuring agreement

**The current numbers.** `judges/README.md` quotes exact match 0.25 and kappa 0.07. Both are the wrong tools for a 1–5 ordinal scale. Exact match counts a 4 against a 5 the same as a 1 against a 5. Plain Cohen's kappa treats the scale as nominal, so it understates agreement. The `../scripts/judge_agreement.py` that the README cites is not in the workspace, so I can't tell how that kappa was computed.

**What to report, for judge A vs B and for each judge vs the human labels:**
- **Krippendorff's α at the ordinal level.** Record the level next to the figure, give a bootstrap CI over traces, and report nominal and interval as sensitivity checks. The script does all of this.
- **Within-1 agreement and the mean difference.** These show whether the disagreement is a calibration offset or noise.
- **False accepts and false rejects against the human labels at a stated threshold.** I assumed a rating of 4 or more counts as acceptable. Please confirm that threshold, because it changes those numbers.
- **Judge-B's two failed calls (traces 018 and 043)** reported as incomplete, not silently dropped. Those two traces drop out of A–B comparisons, leaving 58. Both humans rated them 4.

**What the raw data already shows (hand sums, unverified):**
- Mean ratings are roughly human 3.63, judge A 4.07 and judge B 3.09 (over its 58 scored traces).
- Judge A is about 0.4 above the humans and judge B about 0.5 below, so the A–B gap is mostly a leniency offset. If so, α will be low while rank correlation stays reasonable.
- The two judges are not a controlled comparison. They differ in model (`gemini-flash-latest` vs `gemini-3.5-pro`), in prompt, and in what they see. B is told to read the tool calls and penalise unsupported claims, while A has only a bare scale. Each of these could explain the gap, and one comparison cannot separate them.
- `judge-a.md` uses the floating alias `gemini-flash-latest`. Pin a dated version before comparing runs over time.

**Limits of the evidence.** One panel produced the human labels, so there is no human–human agreement to set a ceiling. Without it, "the judges disagree more than expected" has no baseline. If the panel members rated independently, keep their separate ratings. Judge repeatability is also unmeasured. Re-score the same traces several times to separate sampling noise from real disagreement.

## 2. Running the ADK agent under Inspect

**Yes, without rewriting the agent, with caveats.** The evaluation skill records a 2026-10-22 spike on google-adk 2.12.0 and inspect-ai 0.3.283. Inspect's `agent_bridge()` intercepts the google-genai client, so an `LlmAgent` on `Gemini(model="inspect")` runs under `inspect eval --model mockllm/model`. That spike used one function tool and a mock model. A real tool round trip was not exercised. I did not reproduce it here, and neither inspect-ai nor ADK was installed or run.

- **Model swap.** `app/agent.py` builds the agent at import with `root_agent = build_agent()`, and `build_agent` takes `Settings`, not a model. Either derive a copy with `root_agent.model_copy(update={"model": Gemini(model="inspect")})`, or add an optional `model=` argument to `build_agent`. The second is the smaller, cleaner change.
- **Streaming.** The bridge rejects `:streamGenerateContent`, so the run must not use `StreamingMode.SSE`.
- **Fakes.** Import-time `build_agent()` configures real payments and mail clients through `services.configure`. Under Inspect, build the services from `tests/fakes.py` instead, per AGENTS.md.
- **Placeholder key.** The Gemini client needs a placeholder `GOOGLE_API_KEY` at construction.
- **What Inspect adds.** Its epochs and reducers give pass^k and mean@k over repeated agent trials. The agreement figures in section 1 need only the stored traces, not Inspect. Inspect's `krippendorff` metric would also do the α computation.
- **What stays primary.** Scripted-model Runner tests and ADK's own evaluators remain the primary evidence. Inspect is a way to run repeated trials.

## Assumptions (nobody could answer)
- Acceptable means a rating of 4 or more.
- `helpfulness-v2` is genuinely ordinal, so ordinal α is the headline figure.
- The human labels are the reference. Adjudication has not happened.
- Both judges scored the same fixed traces.

## Done
- Read the data, judge prompts and agent code.
- Wrote `scripts/agreement_alpha.py` (stdlib only), which I have not run.
- Hand-computed the rough means above.

## Not done
- Running the script or its self-test.
- Judge TPR and TNR on a held-out split. The 60 traces are one set with no dev/test split, so any rates computed on them can't be reported as calibration.
- Any Inspect run.
- Repeat-scoring to measure judge noise (needs model access).
- Locating the missing `judge_agreement.py`.
- I also invoked the update-config skill by mistake. It changed nothing.

To run the script from the repo root: `python3 scripts/agreement_alpha.py --selftest`, then `python3 scripts/agreement_alpha.py labels/human-ratings.csv judges/scores-judge-a.csv judges/scores-judge-b.csv`.