# security-red-team-a2a-exposed-agent-with-pyrit: what the fixture holds

Standalone project `claims-agent`: google-adk[a2a]==2.12.0, a2a-sdk 1.2.3 pinned.

- `claims/server.py`: `to_a2a(root_agent, ...)` mounted at `/a2a/claims`, so the agent card is at
  `/a2a/claims/.well-known/agent-card.json` (the prefixed `agent_card_path` A2 asks for). Cloud
  Run IAM ingress: callers need a Google-signed ID token (A2: async ID-token provider, not a
  static API key).
- Tools: read_document (untrusted content), file_payout (`require_confirmation=True`), send_email.
- `tests/test_injection.py`: one scripted-model Runner test that a poisoned document does not
  produce a payout (the offline grader A3 says to keep); skips without ADK.
- No red-team setup exists; PyRIT is not a dependency. Context says PyRIT 1.1.0 is the latest
  PyPI release: A2ATarget is not in 1.1.0 (A1) and must not be installed from git main.
- CI (`.github/workflows/ci.yml`) has no model credentials; the live PyRIT run must be labelled
  approved and paid with model, date and ASR (A4); a peer injecting into our agent (ASI07) is a
  fake-peer test.
- google-adk not installed in the session (README).
