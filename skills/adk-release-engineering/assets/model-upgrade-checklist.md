# Model upgrade checklist and go/no-go record

Copy into the project's release records. Fill every field; "not run" and "not required because ..." are valid values, blank is not. Label each evidence item local, mocked, live or not run.

## Identity

| Field | Value |
| --- | --- |
| Release candidate ID | |
| Date opened | |
| Owner / approver | |
| Current model ID (pinned) | |
| Candidate model ID (pinned, no alias) | |
| Reason (deprecation notice with date and URL, cost, quality, capability) | |
| Retirement date of current model: Gemini API page (date) / Vertex page (date) | |
| Judge model ID and `num_samples` (unchanged for this upgrade: yes/no) | |
| User simulator model ID, if scenarios are used | |
| `google-adk` / `google-genai` versions | |

## Frozen inputs (hashes)

| Input | sha256 or version |
| --- | --- |
| Development set (`eval_set_id`, file) | |
| Holdout set (`eval_set_id`, file; last used on) | |
| Prompt(s) | |
| Exemplars / retrieval snapshot | |
| Tool schema hash | |
| Eval config (`test_config.json`) | |
| Candidate settings that differ from current (`thinking_level`, `max_output_tokens`, other) | |

## Calendar check

- [ ] Both deprecation calendars read on (date); dates recorded above
- [ ] Alias IDs (`-latest`, `-preview`, `-exp`) absent from agent, fallback, judge and simulator config
- [ ] Short-term model? If yes, the 45-day migration path is rehearsed

## Code regression (tier 1, deterministic)

- [ ] Scripted-model tests pass against the candidate ID (finish reasons, tool-call formatting, schema save path)
- [ ] `adk conformance test --mode replay` passes, or recordings re-baselined with a reviewed diff
- [ ] Tool schema hash unchanged, or change explained

## Model-performance regression, offline (tier 2 and 3)

| Metric | Current | Candidate | Delta | Evidence tier |
| --- | --- | --- | --- | --- |
| Category counts (one row per category, successes / attempts) | | | | |
| `tool_trajectory_avg_score` (mean over runs; strict per-run pass count) | | | | |
| `response_match_score` | | | | |
| Judge metric(s), with judge agreement rate | | | | |
| Schema validity / wrong-valid-schema | | | | |
| Prompt tokens / output tokens / thought tokens per case | | | | |
| p50 / p95 latency per case | | | | |
| Cost per case and per 1,000 invocations | | | | |

- [ ] Stage 1 (plainest contract) and stage 2 (full workflow) both run; a gain lost in stage 2 is recorded as a workflow defect
- [ ] Components evaluated independently where the application is composed (retrieval, tools, chain)
- [ ] Every evaluation done since launch repeated, or the omitted ones listed with a reason
- [ ] Holdout run once with the frozen winner: score, date

## Load test

- [ ] Run with the candidate at expected concurrency, or "not required because ..." with the owner's name
- [ ] `max_output_tokens` headroom re-measured for the candidate's token counts

## Online comparison (staged rollout)

- [ ] Canary plan: steps, minimum sample, duration, stop rule
- [ ] Metrics compared online: error rate, p95 latency, cost per request, sampled judge score
- [ ] Rollback bundle for the current release recorded (digest or revision, prompt hash, model ID, schema hash, secret versions)

## Decision

| Field | Value |
| --- | --- |
| Go / No-go | |
| Decided by, date | |
| Conditions (thresholds adjusted, cases moved to tier 3, follow-ups) | |
| Changelog row reference | |
| Prompt adjustment needed (separate changelog row): yes/no | |
