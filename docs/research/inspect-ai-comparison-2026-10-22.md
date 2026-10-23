# Inspect AI compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai)
at commit `c2fc3d9` (2026-10-21; MIT), sparse-cloned on 22 October 2026
into its own directory and read, with the published package
`inspect-ai` 0.3.283 (PyPI, 2026-10-21) installed in a scratch virtual
environment outside the repository for one spike. Files read:
`src/inspect_ai/scorer/_reducer/reducer.py` (`at_least`, `pass_at`,
`pass_k`), `src/inspect_ai/scorer/_metrics/krippendorff.py`,
`docs/agent-bridge.qmd`, and the installed package's
`agent/_bridge/bridge.py` (`init_google_request_patch`).

**Conclusion.** Three method facts and one proven integration. The
reducers give the evaluation skill the "incomplete" sentinel it lacked:
`pass_at` and `pass_k` return NaN when fewer than `k` scored trials remain,
and `pass_k` is the same unbiased estimator tau2-bench uses, so the two
sources agree on the formula and differ only in what happens when `k`
exceeds the trials (NaN versus an exception). `krippendorff_alpha` is a
ready statistic for judge agreement with its scale levels and its relation
to Scott's π and Fleiss' κ stated by the maintainers. The spike settled the
memo's open question: `agent_bridge()` does intercept google-adk, because
it patches the google-genai client's `async_request` for `:generateContent`
paths whose model name targets Inspect; an ADK 2.12.0 `LlmAgent` on
`Gemini(model="inspect")` run through `InMemoryRunner` inside the bridge
produced the mock model's output with one Inspect model event. Streaming
(`:streamGenerateContent`) is rejected by the bridge by design, so ADK's SSE
streaming mode cannot be bridged.

## Method and spike

Reducer bodies and the metric docstring were read in the snapshot; the
bridge patch was read in the installed package. The spike ran
`inspect eval spike_task.py --model mockllm/model` on an ADK agent with one
function tool and a placeholder `GOOGLE_API_KEY` (the Gemini client is
constructed before interception), no network beyond the package install;
the eval log shows the agent's answer as the mock model's default output
and a single `mockllm/model` model event. Facts are placed in the
evaluation skill with the commit, the package version and the spike date.
One scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/inspect-ai-alignment-2026-10-23.md).

## Drift corrected

- The memo's "whether it intercepts ADK's google-genai calls needs a spike
  first": spiked, it does, for non-streaming calls; the streaming limit is
  new.
- The memo's `at_least` description holds; `pass_at` is the Chen 2021
  estimator and `pass_k` its draw-without-replacement dual, as the
  docstrings say.

## Imported, by specialist

- **adk-agent-evaluation.** The NaN sentinel and the `at_least` reducer in
  result auditing; `krippendorff_alpha` in judge calibration; the bridge
  mechanism, the spike result and the streaming limit in provider
  compatibility.

## Routed, not copied

Nothing; Inspect is a harness, invoked by its package name.

## Vendored assets

None.

## Left out, with reasons

- Inspect's sandboxing, tools, approval policies and its own agents: a
  different harness's internals.
- The sandbox bridge: needs a container runtime.
- Adopting Inspect as the toolkit's harness: the toolkit's rule is to keep
  ADK's own evaluators and scripted-model Runner tests as the primary
  evidence; Inspect is named as a way to run the same agent under a
  harness that already has repeated-trial reducers and the agreement
  statistic.

## Limits

One spike on one SDK pair with a mock model and no tools called; the
bridge's behaviour with ADK's function-calling round trips under a real
model was not exercised.
