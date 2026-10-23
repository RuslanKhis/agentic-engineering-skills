# GoogleCloudPlatform/generative-ai `agents/` compared with this toolkit — 22 October 2026

## Scope and snapshot

A file-level review of the `agents/adk/` subtree and the `gemini/evaluation/`
listing of [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)
at commit `3a716a8` (2026-10-21), sparse-cloned on 22 October 2026 into its
own directory and read, never run. Licence: Apache-2.0 at the root, no
NOTICE; `contract-compliance-pipeline` carries its own Apache LICENSE. Read:
`agents/adk/zero-trust-agents/README.md`,
`agents/adk/zero-trust-agents-2/README.md` and its `demo/` listing,
`agents/adk/agent-quality-flywheel/README.md` and `fx_footer_config.yaml`,
`agents/adk/contract-compliance-pipeline/README.md` and the
`RemoteA2aAgent` wiring in its `python-extraction-agent/app/agent.py`, and
the `gemini/evaluation/` notebook names. Two product questions the memo left
open were settled on Google's documentation the same day: Semantic Governance
Policies exist as a Preview feature enforced on Agent Gateway
(https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/semantic-governance-overview,
updated 2026-10-21), and "Agent Anomaly Detection" appears only as a
navigation entry on the governance overview page (updated 2026-10-21), with
no description in the body; the blueprint's `sgp_guard.py` and
`aad_engine.py` are local simulations.

**Conclusion.** Four blueprints, four patterns this toolkit already argues
for, now with Google's own worked examples beside the rules: build-time
controls that hold with screening off (signed writes, a hermetic sandbox, a
deterministic gateway with CI tests); a runtime policy layer that is
probabilistic by the vendor's own statement and is therefore a layer, with the
multi-turn aggregate exploit that shows why the bound lives in trusted code;
a rubric metric paired with a deterministic one in the same evaluation loop;
and a deterministic policy service as an A2A peer. Imported as facts at those
decisions; nothing vendored.

## Method

Each README was read in full, each item classified and checked against the
specialist that owns the decision, and written there with the citation
`(GoogleCloudPlatform/generative-ai commit 3a716a8, <file>, read 2026-10-22;
vendor sample)`. One scenario case and one fresh-agent trial cover the
refund-hardening journey (see the
[testing record](../testing/generative-ai-agents-alignment-2026-10-22.md)).

## Drift corrected

- Semantic Governance Policies: the memo could not say whether they are a
  product. They are, in Preview, with `ALLOW` and `DENY` verdicts, natural
  language constraints evaluated by an LLM policy engine on Agent Gateway,
  and the vendor's own warning that verdicts may be inaccurate.
- Agent Anomaly Detection: still unconfirmed as a product on Google's pages;
  the skills say so and treat the blueprint's version as a simulation.
- The contract-compliance Go agent serves its card at
  `/.well-known/agent.json`, the pre-0.3 path; the memo did not note it.

## Imported, by specialist

- **adk-agent-security.** Semantic Governance Policies as a second screening
  layer with their Preview status and probabilistic caveat; the blueprint's
  eight-refund aggregate exploit and why the bound is code; the three
  build-time pillars of part one.
- **adk-operational-guardrails.** The aggregate bound keyed on the business
  object in the operation record, with the smurfing case as the reason.
- **safe-api-tool-calls.** The signed-write pattern (HMAC locally, Cloud KMS
  in production, a ledger audit that fails on an edited amount) as an
  integrity control beside the idempotency key.
- **adk-agent-interoperability.** The deterministic policy service as an A2A
  peer, the caller-set policy values in the data part, and the legacy card
  path.
- **adk-system-designer.** The same peer pattern in the handoff route row.
- **adk-agent-evaluation.** The flywheel's rubric-plus-code metric pair, its
  "trust the delta" rule, and its `judge_model` omission, with this skill's
  full-resource-name rule kept.
- **adk-release-engineering.** The model-migration notebook named as a worked
  example, not read.

## Routed, not copied

Nothing: the blueprints are samples. The Agent Gateway skills from
google/skills remain the operating route for Model Armor and gateway policy.

## Vendored assets

None.

## Left out, with reasons

- The `new-hire-onboarding` blueprint, the `agent_engine/`, `cloud_run/`,
  `gke/`, `gemini_data_analytics/`, `invoice-processing/`,
  `managed-agents/`, `personalized-agent-swarms/` and `skill-registry/`
  subtrees, and the Memory Bank governance notebooks: not read in this pass;
  no decision here depends on them.
- The `gemini/evaluation/` notebooks beyond their names: listed, not read.
- Part two's closed-loop "auto-drafted policy" as a control: it drafts a
  policy for a human to attach; the toolkit's rule that an operation record
  enforces the aggregate stands.

## Limits

Read, not run; the blueprints' demos simulate the cloud services they name.
Product status was taken from two Google pages on one day.
