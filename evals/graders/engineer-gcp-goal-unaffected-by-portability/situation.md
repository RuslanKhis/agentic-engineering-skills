# engineer-gcp-goal-unaffected-by-portability: what the workspace holds

Standalone project (no base): Coastline claims assistant, google-adk 2.12.0,
Cloud Run, Vertex AI, Agent Platform sessions, Firestore.

- `docs/architecture/claims.md`: accepted GCP/ADK design, C2/C3 for memory,
  D1 Memory Bank with `PreloadMemoryTool`; the scope gate mentions the CTO's
  portability concern only as a separate assessment (G07).
- `docs/plans/claims.md`: G02 ready (primary adk-memory-architecture; route:
  `VertexAiMemoryBankService` on the existing engine, write-back
  `after_agent_callback` with a consent check, `InMemoryMemoryService` in
  tests; acceptance A1-A3); G07 portability (adk-portability-planning, not
  started).
- `claims/tools.py` already has a `ClaimRepository` protocol (existing code,
  not something G02 asks for).

What to look for: A1 adk-memory-architecture chosen for G02 and the plan's
GCP route built (Memory Bank service on the Runner, scope from the verified
ID, consent check, Runner tests with `InMemoryMemoryService` reported not
run); A2 adk-portability-planning not loaded (check skills loaded); A3 no
`MemoryProvider` abstraction, adapter or provider-neutral wrapper added for
portability's sake.
