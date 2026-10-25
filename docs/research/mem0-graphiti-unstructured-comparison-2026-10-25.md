# mem0, graphiti and unstructured compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [mem0ai/mem0](https://github.com/mem0ai/mem0) at commit `2c81af3`
(2026-10-20; PyPI `mem0ai` 2.2.1), [getzep/graphiti](https://github.com/getzep/graphiti)
at commit `8ce6d63` (2026-10-24; `graphiti-core` 0.31.2) and
[Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured)
at commit `c74e6c4` (2026-10-24; 0.27.34), cloned on 25 October 2026 into
their own directories and read, never run. This builds on the
[memory sources note](memory-sources-comparison-2026-10-23.md) and covers
only what is new.

**Licence.** Apache-2.0, except mem0's `integrations/n8n-nodes-mem0` (MIT);
mem0-strands has a NOTICE. Nothing is copied.

**Maintenance.** All three active.

**Conclusion.** The memo's "swallowed-error anti-pattern" is confirmed and
worse: Mem0's published ADK service returns no memories on any error or a
missing key, and its write and read scopes do not match. ADK's own
`PreloadMemoryTool` also turns a failed search into "no memories". "Add-only"
and "bi-temporal" are true in detail, and both mean "newest wins" needs a
current-only read in code on these backends. Erasure leaves residue on all
of them, and all three send telemetry by default. Unstructured adds one
fact for the ingestion check and nothing else over the existing Docling
guidance.

## Method

The ADK sample's exception handling, `delete_linked`, `latest_only`, Mem0's
history and message tables, graphiti's `remove_episode` and raw-content
default, the telemetry switches and unstructured's per-document `auto`
decision and fallbacks were confirmed in the snapshots, and
`PreloadMemoryTool`'s exception path in google-adk 2.12.0, before editing.
One scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/mem0-graphiti-unstructured-alignment-2026-10-25.md).

## Drift corrected

None.

## Imported, by specialist

- **adk-memory-architecture.** In `memory-bank.md`: a vendor memory service
  raises or reports "unavailable" rather than returning empty, the preload
  path's swallowed error, a write-then-read scope test, a current-only read
  per backend, and the residue and telemetry each leaves on erasure. In
  `failure-recovery.md`: a symptom row for silent empty recall. In
  `document-ingestion.md`: unstructured's per-document strategy and silent
  fallback. After the trial: the scope fix (`app_id` as an entity field on
  both sides), what the model is told when recall fails, hosted versus
  open-source Mem0 deletion with their per-user calls, a key-rotation
  pointer, a routing row for vendor services, and an inspector that no
  longer reports a `BaseMemoryService` subclass as Memory Bank.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Mem0 or graphiti as recommended services, and unstructured as a second
  extractor recommendation beside Docling.
- The ADK guide's description of `load_memory` as automatic injection
  (that is `PreloadMemoryTool`).
- The licences of the model weights `hi_res` downloads were not checked.

## Limits

Nothing was run; Mem0 Platform behaviour comes from its documentation and
client code.
