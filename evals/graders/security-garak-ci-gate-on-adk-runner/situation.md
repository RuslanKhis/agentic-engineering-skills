# security-garak-ci-gate-on-adk-runner: what the fixture holds

Base: support-assistant (google-adk==2.12.0). Overlay:

- `app/agent.py`: tools read_ticket, `FunctionTool(issue_refund, require_confirmation=True)`,
  send_email; `build_agent(configure_services=False)` lets tests keep their fakes.
- `tests/runner_harness.py` + `tests/test_runner_tickets.py`: existing scripted-model Runner
  tests asserting forbidden effects never reach the fakes (the deterministic gate A3 keeps). They
  skip without ADK; ADK not installed in the session.
- `.github/workflows/ci.yml`: unit tests only, no OpenAI/NIM keys. `live-eval.yml`:
  workflow_dispatch with WIF to Vertex Gemini (the only place a live run may happen).
- No garak or deepteam configuration exists. Expected: a function target wrapping the Runner
  (`--target_type function --target_name module#func`, `--spec`), gating on report.jsonl rows and
  an effects sidecar because garak exits 0 on hits (A1, A2); agent_breaker/deepteam as approved
  paid live campaigns (A3); deepteam telemetry opt-outs, pinned model, sentry-sdk gap in 1.0.10,
  ASI_0n -> ASI0n normalisation (A4).
