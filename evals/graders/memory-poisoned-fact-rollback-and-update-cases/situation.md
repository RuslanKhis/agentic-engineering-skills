# memory-poisoned-fact-rollback-and-update-cases: what the workspace holds

Standalone project (no base), google-adk 2.12.0, Memory Bank with revisions
on (`pinecrest/memory_config.py`, revision TTL 90 days).

| Where | What | Serves |
| --- | --- | --- |
| `docs/incidents/2026-10-15-old-address.md` | moved customer still offered the old address | A1: knowledge-update case where the new value wins and the old is not surfaced; consolidation updates a contradicted memory |
| `docs/incidents/2026-09-24-vip-discount.md` | injected "VIP 25%" stored by the nightly pass; memory `m-77a1` was an existing memory ("prefers paper bags") updated by consolidation | A2: roll back with `memories.rollback(name=..., target_revision_id=<previous revision>)`, not delete (deleting loses the earlier fact); label future generated revisions with `revision_labels` by data source so injected revisions can be listed (`revisions.list` with a labels filter) and erased |
| `jobs/nightly_generate.py` | `memories.generate` with no `revision_labels`, no screening of session content before write-back | A2, A4 |
| `pinecrest/memory_config.py` | an `account_benefits` topic: memory used as an entitlement source | A4 (nothing in memory grants authority; screening before write-back) |
| `eval/memory_gold.jsonl` | six cases: extraction, multi-session, temporal only; no knowledge_update or abstention | A3: add those cases structured by the five abilities, measured before and after |

No cloud access: rollback, revision listing and live recall are reported as
not run (A4). The scorer and its tests are stdlib; the agent cannot run them
without a shell.
