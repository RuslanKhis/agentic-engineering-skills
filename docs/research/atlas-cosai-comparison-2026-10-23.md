# MITRE ATLAS and the CoSAI Risk Map compared with this toolkit — 23 October 2026

## Scope and snapshot

A review of [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data)
at commit `3259f38` (2026-09-10; Apache-2.0; `dist/ATLAS-latest.yaml`
version 2026.09) and
[cosai-oasis/secure-ai-tooling](https://github.com/cosai-oasis/secure-ai-tooling)
at commit `622605a` (2026-10-20; Apache-2.0; `risk-map/yaml/risks.yaml`,
`controls.yaml`, `frameworks.yaml`), both cloned on 22 October 2026 into
their own directories and read on 23 October, never run.

**Conclusion.** Vocabulary only, as the memo said: the security skill's
findings keep their enforcement points and observable checks and gain, for
readers who track ATLAS or the Risk Map, the identifier to put beside the
OWASP one. Eleven ATLAS agent techniques and ten Risk Map risks plus six
controls are named by id with links; `controlAgentExecutionBounds` is
recorded as the vendor-neutral statement of what the guardrails skill's
runtime bounds enforce. Two corrections to the memo came from the data
itself, below.

## Method

The ATLAS file was parsed for ids and names (no YAML copied); the Risk Map's
risk, control and framework files were read for ids, the ATLAS pin and the
mappings. Ids are cited in the threat-model reference's identifier section,
the checklist asset's companion line and the sources file; nothing is
vendored because id tables are the frameworks' own content. One scenario
case covers the journey; a fresh-agent trial is in the
[testing record](../testing/atlas-cosai-alignment-2026-10-23.md).

## Drift corrected

- The memo's "120 techniques" is 136 by count of ids without a sub-technique
  suffix in `ATLAS-latest.yaml` 2026.09; tactics (16) and sub-techniques
  (88) match.
- The memo said the Risk Map "pins `mitre-atlas@2026.09`"; its
  `frameworks.yaml` does, but all 37 technique mappings in `risks.yaml`
  still carry `@5.0.1`, so the skill says to take ATLAS ids from ATLAS.
- The two ids the memo named (`AML.T0086`, `AML.T0110`) exist with the names
  given.

## Imported, by specialist

- **adk-agent-security.** The identifier paragraph in the threat-model
  reference and the companion line in the checklist asset.
- **adk-operational-guardrails.** Named through `controlAgentExecutionBounds`
  in that paragraph; no edit in the guardrails package.

## Routed, not copied

Nothing; frameworks cited by id.

## Vendored assets

None.

## Left out, with reasons

- A mapping column in the checklist table: the table is already wide and
  the companion line carries the same information.
- OWASP MCP Top 10 and CoSAI WS4 runbooks: CC BY-SA and CC BY sources named
  in the memo's medium tier, not reached.
- The Risk Map's lifecycle, persona and component taxonomies: no decision
  here depends on them.

## Limits

Ids only; neither framework's narrative was imported, and the Risk Map's
mappings will change when it re-pins ATLAS.
