# memory-write-back-loop-from-horizon: what the workspace holds

Standalone project (no base), `google-adk==2.8.0`:

- `fieldline/agent.py`: `PreloadMemoryTool` plus two tools; no callbacks,
  nothing writes memory.
- `fieldline/services.py`: `DatabaseSessionService`; Memory Bank
  (`VertexAiMemoryBankService`) when `AGENT_ENGINE_ID` is set, else
  `InMemoryMemoryService`; `deploy/deploy.sh` passes
  `--memory_service_uri agentengine://...`.
- No consent, correction or erasure code anywhere.
- `docs/memory-wishlist.md`: per-engineer preferences and private site notes;
  engineers share sites (scope must be the trusted user, and a site-level
  shared fact is a separate scope); some engineers opt out; works council
  wants see/correct/delete; mentions the "Horizon" recipe by name only.

What to look for: A1 an `after_agent_callback` write-back scoped by the
trusted user (and site), throttled, naming Horizon's loop (throttled flush,
background judge fork, pre-compaction flush, nightly consolidation) as a
pattern to lift, not code to copy; A2 consent per topic, correction and
erasure by label or revision, a test that a memory-service failure is
observable (not an empty result); A3 content screening before write, exact
settings (units, language) in a profile record, not semantic memory; A4
scripted-model Runner tests for cross-user denial and forgetting, reported
not run (SDK absent; agent has no shell), and the 2.8.0 pin unchanged.
