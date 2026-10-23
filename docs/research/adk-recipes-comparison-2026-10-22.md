# google/adk-recipes compared with this toolkit — 22 October 2026

## Scope and snapshot

A file-level review of [google/adk-recipes](https://github.com/google/adk-recipes)
(formerly adk-samples) at commit `be63596` (2026-10-20), cloned on
22 October 2026 into its own directory and read, never run. Licence:
Apache-2.0 at the root, no NOTICE file; two recipes carry their own Apache
LICENSE (`core/python/cross-session-memory`,
`contrib/python/brand-aligned-presentations`). The repository README says
recipes are "for demonstration and as starting points, not production use".
Latest tag: `ambient-quality-agent/v0.1.0`. The parts the
[integration memo](external-sources-integration-report-2026-10-21.md) named
were read in full: the repository and `plugins/` READMEs, the Ambient
Quality Agent (AQuA) README, the ambient-expense-agent README and
`expense_agent/` code, the long-horizon-harness ("Horizon") `AGENTS.md`,
`docs/memory.md`, `docs/security-model.md`, `horizon/guardrails/` sources,
`default_policies.jsonl`, the eighteen evalsets with `eval_config.json` and
their README, the three RAG recipe READMEs with `multiformat-hybrid-rag`'s
`architecture.md`, the `staged-ui-widgets` README and `pyproject.toml`, and
the retail plugin's `EVAL.yaml` and `SKILL.md`. Two ADK claims the
staged-widgets recipe rests on were confirmed in the google/adk-python
source at main commit `ed76f94`.

**Conclusion.** The repository is Google's ADK-native pattern library and,
with AQuA, now also ships an operator product. This toolkit decides; the
recipes show one working shape and AQuA operates a loop. So: facts were
imported where a recipe settles an ADK mechanism or shows a production shape
a specialist was missing (write-back memory, deterministic-first graphs,
repeated-failure signatures, staged widget emission, managed RAG options);
AQuA was routed, not rebuilt; evalsets were used as templates, not vendored;
and the disclaimer travels with every pattern.

## Method

For each named item: read the recipe file, classify it (fact for a named
specialist file; routing or companion line; method to restate; verbatim
asset to vendor; spike needed; do not import), check Phase A's map so an
existing paragraph is extended rather than duplicated, verify any ADK claim
against the ADK source snapshot, then write it at the decision it serves
with the citation `(google/adk-recipes be63596, <file>, read 2026-10-22)`
and the "vendor sample" label. Scenario cases were added for the three
changed journeys and one fresh-agent trial run per journey (see the
[testing record](../testing/adk-recipes-alignment-2026-10-22.md)).

## Drift corrected

None beyond Phase B's row 14 (the Horizon stack row says ADK 2.5.x, not
2.8.x; already fixed in the optimise skill). The memo's "eight recipes with
zero citations" was checked: `deep-search` was already cited by the workflow
and guardrails skills; the others were uncited and are covered below or
left out with a reason.

## Imported, by specialist

- **adk-engineer, adk-system-designer.** The disclaimer rule: a change or a
  route that lifts a recipe pattern names the recipe and file, repeats "not
  production use", and lists the controls the recipe lacks; the three-layer
  layout (`core/`, `contrib/`, `plugins/`) and the two per-folder licences.
- **adk-release-engineering.** A new section in the production-feedback
  reference on AQuA: what it reads (BigQuery Agent Analytics table,
  `_AllSpans` linked dataset, agents-cli logging), when it runs (schedule,
  after deploy, on demand), what it produces (insights `NEW`, `RECURRING`,
  `RESOLVED` with occurrence history; root cause against a published source
  snapshot), how it installs (agents-cli extension pinned by `--ref`,
  `--apply-aqua`, `--deploy-aqua`, `agents-cli aqua attach`) and its
  prerequisites (agents-cli 1.6+, Terraform, an organisation project for
  IAP). Two rules are this toolkit's: the release record says which insights
  gate; a missing or failed investigation is NOT RUN, never a clean week.
- **adk-agent-evaluation.** Horizon's evalsets as case and rubric templates
  (18 files, 78 cases; `rubric_based_final_response_quality_v1` at 0.8;
  judge `gemini-3.7-flash` with `numSamples: 1`; rubrics that name the
  context the judge cannot see; `tool_uses` as documentation; the README's
  warning that `agents-cli eval run` rejects content-less events), with this
  skill's rules kept where they differ (trajectory expectations graded or
  removed; majority voting). The retail plugin's rubric-plus-assertion
  `EVAL.yaml` as a pattern, its "80%+" labelled as that skill's figure. A
  scheduled production evaluator as a stage whose missing run is incomplete
  evidence.
- **adk-agent-observability.** AQuA insights as a source row in the
  trace-to-evaluation table.
- **adk-agent-security.** Horizon's guard shape in detail (callback
  contract, argv classifier verdicts and demotion rule, seed denylist and
  protected paths, grant narrowing, one-time upload grant, all-or-nothing
  sandbox egress) and the `exfil_injection` rubric trio for the live
  campaign; the graceful-handoff divergence recorded.
- **adk-operational-guardrails.** The repeated-failure signature
  (`tool:sha256(canonical args)`), what counts as a failure, the 600 s decay,
  the threshold floor, the shared halt state and `last_error` mirror, the
  no-progress guard and iteration budget; ask-as-deny on headless chains;
  sub-agent approval resurfacing with one confirmation per call; the
  ambient-expense approval UI reading pending sessions.
- **adk-workflow-design.** The deterministic-first graph (threshold in
  code, `Event(route=...)`, `RequestInput` on the review node, Pub/Sub push
  to the trigger endpoint) and the per-stage callback chain written down as
  the contract.
- **adk-memory-architecture.** The write-back loop (throttled flush, memory
  tool with scopes and limits, content scan at write, background review
  fork, pre-compaction flush, nightly `memories.generate` consolidation) with
  Horizon's own honesty notes and the controls it lacks; the three managed
  RAG recipes and the inspection-point consequence of `VertexAiSearchTool`;
  the managed RRF twin; `pool_pre_ping` is not enough.
- **adk-frontend-integration.** "Widgets emitted by tools": staging in state,
  one emitting callback, declared order, single render call site, the two
  ADK facts behind the bugs (duplicate-id check per call context; no event
  without content or a state delta), suppression of byte-identical
  re-renders, the model never writing component JSON.
- **optimise-adk-on-google-cloud.** The pre-compaction memory flush as a
  summariser hook, owned by the memory skill.
- **adk-agent-interoperability.** Horizon's pins as a data point for the
  A2A 1.x-with-0.3-compat configuration Gemini Enterprise needs.

## Routed, not copied

`agents-cli-aqua`, the skill the AQuA extension installs, is named at the
decision it serves in adk-release-engineering in the standard form; the
engineer's composition reference lists it beside the Agents CLI skills and
maps it to adk-release-engineering and adk-agent-evaluation; the designer's
handoff table has a row for it, named in a goal as
`google/adk-recipes:agents-cli-aqua`. The division is the same as for every
Google collection: the specialist decides whether insights gate a release,
Google's extension operates the evaluator.

## Vendored assets

None. Evalsets, SQL and code were paraphrased with links; no licence action
was needed.

## Left out, with reasons

- Rebuilding AQuA's scheduler, dedup store or dashboard: it is a product.
- Horizon's `GuardrailsPlugin` graceful handoff as a default: it spends one
  more model call after a halt; this toolkit's static stop stands, the
  option is recorded.
- Horizon's `_is_failure` as the repeat definition on its own: it does not
  separate a terminal failure from an ambiguous write.
- `numSamples: 1` for a judge metric: below this toolkit's majority-vote rule.
- `intermediate_data.tool_uses` kept as ungraded documentation: here a
  trajectory expectation is graded or removed.
- The "80%+ passing" target: a plugin's own figure, not a threshold for a
  project.
- `llm-auditor`, `high-volume-document-analyzer`, `genmedia-for-commerce`,
  the retail and brand recipes: no fact in them changes a specialist's
  decision beyond patterns already carried.
- The nine maintainer skills under `.agents/skills`: they maintain recipes,
  not applications.
- The plugins format (Agent Plugins v1.0.0) and `npx skills add
  google/adk-recipes --skill ...`: distribution of Google's skills, not a
  decision here.

## Limits

Read, not run: no recipe was executed, no evalset scored, no AQuA deployed.
AQuA is v0.1.0 and the repository warns that recipes are not for production;
every imported fact carries the vendor-sample label and the commit. The
Horizon facts describe one harness's choices at ADK 2.5.x to 2.8.x; the
mechanisms were cross-checked against the ADK source only where a sentence
asserts ADK behaviour. The review prompt now covers this repository so the
facts are re-read when it moves.
