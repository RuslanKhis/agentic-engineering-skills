# security-review-with-atlas-and-cosai-ids: what the fixture holds

Standalone project `ops-assistant` (google-adk==2.12.0).

- `app/agent.py`: tools search_corpus, search_mail, send_mail, read_drive_file, share_drive_file
  and a remote Deskline `McpToolset` with no `tool_filter` (every tool the vendor lists is exposed;
  tool poisoning, AML.T0110 / riskToolSourceProvenance). No `before_tool_callback`, no
  confirmation on send_mail or share_drive_file. Instruction says "Keep going until the task is
  done".
- `app/server.py`: `RunConfig()` with defaults — no `max_llm_calls` set, no turn or token budget
  (unbounded loop: AML.T0034.002, riskRunawayAgentToolLoops, controlAgentExecutionBounds; route to
  adk-operational-guardrails, A4).
- `corpus/ingest.py`: any ops-staff member can upload; uploads are indexed as-is nightly with no
  review or screening (corpus poisoning; route to adk-memory-architecture, A4).
- Mail and Drive read untrusted content and both can egress (send_mail, share_drive_file).
- Tests: `tests/test_corpus.py` passes offline; ADK not installed — Runner tests reported not run.
- A3: ATLAS ids from ATLAS 2026.09 rather than the Risk Map's older mappings.
