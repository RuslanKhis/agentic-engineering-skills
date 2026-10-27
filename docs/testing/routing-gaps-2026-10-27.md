# Three routing gaps from the held-out run · 27 October 2026

The held-out run found three requests with no clear owner. The owner chose
one for each, and the choices are recorded in
`skills/adk-engineer/references/ownership.md`.

| Gap | Owner | Defers |
| --- | --- | --- |
| Retries on the model's own 429 or quota errors | adk-model-and-output-contracts | safe-api-tool-calls (tool API retries) |
| A new feature across several areas of an existing application | adk-engineer | adk-system-designer (new application or substantial redesign) |
| `{key}` placeholders after an `output_key` handoff | adk-workflow-design | adk-agent-instructions (template syntax only) |

## Changes

- **Descriptions.** Six descriptions changed: model-output, safe-api,
  engineer, designer, workflow and instructions. Model-output's and
  instructions' were tightened to stay under 950 characters.
- **Allowlist.** `scripts/boundary_allowlist.json` gains designer →
  engineer, because the router has no exclusion clause.
- **Leaked held-out cases.** The six held-out cases read while making these
  edits are now `dev`, following the held-out rule: `api-heldout-3`,
  `engineer-heldout-1`, `guardrails-heldout-3`, `model-output-heldout-3`,
  `frontend-heldout-3` and `workflow-heldout-1`. Six replacements came from
  the same isolated generator (round 3; `labels-round3.json` and
  `raw/*-round3.json` in
  [the held-out artifacts](artifacts/heldout-activation-2026-10-27/)).
- **New dev cases.** Three cases cover the other side of each gap:
  `model-output-own-429-retry-positive`,
  `designer-existing-app-feature-near-miss` and
  `instructions-output-key-handoff-near-miss`.

The corpus now holds 163 dev and 78 held-out cases.

## Results

| Model | Split | PASS | PARTIAL | FAIL |
| --- | --- | --- | --- | --- |
| Sonnet 5.5 ×2 | dev | 315 | 11 | 0 |
| Sonnet 5.5 ×2 | held-out | 156 | 0 | 0 |
| Haiku 5.5 ×1 | dev | 151 | 11 | 1 |
| Haiku 5.5 ×1 | held-out | 77 | 1 | 0 |

The comparison is with the held-out record, before these changes.
- Sonnet held-out went from 152/2/2 to 156/0/0. Note that six of the
  held-out cases are new.
- Haiku dev went from 3 FAIL to 1. The one left is
  `designer-checkpoint-positive`, which has flipped on Haiku before.
- Sonnet dev stays at 0 FAIL.

Every dev PARTIAL left is a near-miss in which the owner in the ownership
map was primary. The one exception is `observability-eval-handoff-positive`,
whose label the owner has parked.

Artifacts: [routing-gaps-2026-10-27](artifacts/routing-gaps-2026-10-27/).
