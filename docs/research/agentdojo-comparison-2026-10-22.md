# AgentDojo compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo)
at commit `089ed46` (2026-06-02; MIT; version 0.1.35, the same version on
PyPI since 2025-10-27), cloned on 22 October 2026 into its own directory and
read, never run. Files read: the four v1 suites' `injection_tasks.py`
(goals and `security()` checks), `attacks/important_instructions_attacks.py`
(the envelope), `agent_pipeline/base_pipeline_element.py` (`query`),
`data/suites/banking/injection_vectors.yaml` (how injections enter the
environment) and `README.md`.

**Conclusion.** The memo's two routes are right and the first is done: the
injection goal classes of the four suites are now four attributed, synthetic
cases in the security skill's adversarial asset, in the asset's own shape,
with the "important instructions" envelope restated in their fixtures, and
the reference explains that AgentDojo grades by inspecting the environment
after the run, which is the discipline the asset already uses. The live
route, an adapter wrapping the ADK `Runner` as one pipeline element to report
attack success rate, is written as an approved paid campaign and
version-conditionally, because the README says the API may change and the
package's model list predates current Gemini models. No benchmark data was
imported.

## Method

Goals were read in source and restated as goal classes; fixtures were
invented (`.invalid` hosts, made-up accounts and codes) so nothing is copied;
each case carries an `origin` field and the asset's scope says what the four
cases are. The reference's seed-case table and the sources file were
updated. One scenario case covers the journey; the fresh-agent trial is in
the [testing record](../testing/agentdojo-alignment-2026-10-22.md).

## Drift corrected

- The memo's suite counts (16/9, 17/5, 20/7, 33/6) match the source.
- "Last commit June 2026" holds; the PyPI release is older (2025-10-27),
  so a pinned install does not carry the newest source.

## Imported, by specialist

- **adk-agent-security.** Four cases and four fixtures in the asset; the
  table row, the attribution, the end-state note and the live adapter route
  in the adversarial-testing reference.

## Routed, not copied

The inspect_evals port the memo names is left to the Inspect source note;
nothing to route.

## Vendored assets

None; the cases are paraphrases with attribution, not copies.

## Left out, with reasons

- CaMeL, LlamaFirewall, NeMo Guardrails and Presidio shapes the memo lists
  beside AgentDojo: separate sources, not reached in this pass.
- The user tasks and environments: benchmark data.
- Running the suites: needs a model and the package.

## Limits

Read, not run; the ported cases prove the toolkit's gates with a scripted
model, not a model's susceptibility, as the asset's scope says.
