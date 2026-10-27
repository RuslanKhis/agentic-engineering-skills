# Situation: observability-cost-reconciliation-agenttool-litellm

Standalone project (no base). What the fixture contains and which assertion it serves:

- `research/agent.py`: root LlmAgent with two `AgentTool` children (literature_scout on
  o-mini-2, numbers_analyst on o-reasoner-2), every model through `LiteLlm` to an
  OpenAI-compatible gateway, `HttpOptions(retry_options=HttpRetryOptions(attempts=2))`.
- `research/cost.py`: prices only the saved parent session and computes output as
  `candidates_token_count + thoughts_token_count` (A2: on LiteLlm completion tokens already
  include reasoning, so thoughts are added twice and output is overstated).
- `sessions/...json`: the parent session holds only the root agent's three model events; the
  two AgentTool children's model calls are absent (A1: AgentTool runs children in a separate
  in-memory session; aggregate by trace or use single_turn).
- `billing/` invoice and per-request log: 7 o-reasoner-2 requests vs 3 visible root responses
  (the analyst's two calls, a billed 500 and a billed 504 each followed by a retry), and four
  o-mini-2 scout calls never in the session (A1 and A3: child calls and retried/failed-but-billed
  attempts are invisible to ADK usage; reconcile against gateway records, report unknown rather
  than zero). `attempts=2` (A4: becomes LiteLLM num_retries; measure attempts).
- Dashboard 0.2650 vs invoice 0.4498; dashboard output 30,780 vs provider completion 22,475 for
  the reasoner (root completions 5310+4980+6020=16,310 already include reasoning; ADK adds thoughts
  again: 30,780).
- `prices.json` is the project's own table dated 2026-09-01 (A5: quote no price from memory).
- invocation_summary.py (named in the prompt) is the observability skill's helper; the agent
  has no shell, so running it can only be proposed.

Context unchanged.
