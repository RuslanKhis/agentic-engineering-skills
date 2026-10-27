# sensitive-data-local-tool-result-screen-llamafirewall: what the fixture holds

Standalone project `contract-assistant` (google-adk==2.12.0). Tools fetch_url (untrusted web
pages), read_contract (client documents), send_email (`require_confirmation=True`).

- `contracts/policy.py` (`before_tool_callback`): email allow-list per matter and https-only
  fetch — the enforcement A4 says to keep. No `after_tool_callback`; tool results are not
  screened at all. `fetch_url` returns up to 20,000 characters (far beyond PromptGuard's
  512-token window; A1 chunking).
- README states the residency requirement: no third-party API may receive contract text or tool
  results (AlignmentCheck sends the trace to Together AI under a static key: A3).
- Tests: `tests/test_policy.py` passes offline; `tests/test_runner_poisoned_page.py` is a
  scripted-model Runner case with a poisoned page (`tests/fakes.py: POISONED_TERMS`), skips
  without ADK. No HF token, no network, no model access: PromptGuard weights cannot be fetched;
  the live detector run stays pending (A5) and the weights licence needs an owner decision.
- LlamaFirewall is not a dependency.

Changed on 28 October 2026 (Phase 11): `expected_primary` is now protect-adk-sensitive-data, which owns the local Prompt Guard 2 screen and screen placement (`references/boundaries.md`, "A local screen for tool results"); adk-agent-security keeps the threat-model view.
