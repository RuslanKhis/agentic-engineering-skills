Status: I've read the helper and the skill's references. No project code or session export is in this directory, so I'm answering from those and have not run anything.

## What is wrong

Two errors push the numbers in opposite directions. They don't cancel.

**1. Cost is too low because the saved parent session leaves out most of the spend.**
- **AgentTool children are missing.** Each `AgentTool` runs its own `Runner` with a throwaway in-memory session and a new invocation id. A saved parent session has none of the child's model calls or usage. Both sub-agents' calls are absent, and for a research turn that is probably most of the spend.
- **Retries are missing.** `retry_options attempts=2` on the `LiteLlm` path becomes LiteLLM's `num_retries`. That is not "2 attempts". The provider client's retry count and the retry loop's attempt limit differ, so the real number of billed attempts is unknown. ADK records one logical call per retried request, so billed attempts never appear in the session.
- **Failed calls are missing.** A failed call can be billed but stored with no usage. A failed child call comes back to the parent as plain tool-result text, not as a tool error. The helper's tool-error count therefore misses it.
- **Models can show as unpriced.** On `LiteLlm`, `model_version` is the provider's echo (for example `o4-mini`), not the request name (`openai/o4-mini`). A price table keyed on the request name leaves the call unpriced or priced with `default`.

**2. Output tokens are too high because reasoning is counted twice.**
- ADK stores the provider's `completion_tokens` as candidates and the reasoning tokens as thoughts, then adds them. On OpenAI-style routes `completion_tokens` already includes reasoning. The dashboard's output is therefore inflated by the reasoning tokens.
- `invocation_summary.py` detects this and prices those calls from candidates only. Its reported token totals still use ADK's figure, so they match the dashboard and look high. The dashboard has no such correction, so its cost uses the inflated figure.
- Cached input is also priced at the full input rate unless the price table has a `cached_input` entry.

My assumption: the dashboard sums `gen_ai.usage.*` spans, and the invoice is a provider or gateway total. If the dashboard sums both `call_llm` and `generate_content` spans, that adds a further double count on 2.12.0, because both span kinds carry the same usage.

## Fixes

- Aggregate cost by trace, not by session export. Sum `generate_content` spans only, because child calls sit under the parent's `execute_tool` span.
- Compute output as `completion_tokens` alone on the `LiteLlm` path, or take the gateway's totals.
- Reconcile against gateway or billing rows joined on trace and span. Check first that the gateway records the trace context it receives.
- Report a trace's cost as **unknown** when any model call has no join key. Never report a partial sum.
- Expect billed cost at or above observed cost on any trace with a retry or a failure.
- Key the price table by `model_version`. Add `cached_input` rates and a reasoning-token policy.

## Cost tests to add

All of these run offline, with a scripted `BaseLlm`, or a scripted `LiteLLMClient` subclass for the `LiteLlm` path. That path needs `litellm` installed to construct the model, so `LiteLlm(llm_client=...)` is how ADK's real usage conversion gets exercised.

1. **Streamed call.** Cumulative usage on each chunk. Assert totals equal the final chunk, not the sum of the chunks. Also cover the case where a final event has no usage and the newest partial's figures are used.
2. **LiteLlm reasoning call.** Assert that output does not exceed `total − prompt`. Assert the helper emits `reasoning_counted_twice_on_N_calls`, and that the dashboard query and the helper's priced output agree.
3. **AgentTool child.** Compare against an equivalent `single_turn` sub-agent. The parent session's call count must differ, while the per-trace sum must include the child. This pins down the missing-child failure.
4. **Failed call.** Assert it is flagged `usage_missing_on_N_model_calls`, shown as unpriced and never zero. Assert a failed child call is detected despite coming back as plain tool-result text.
5. **Retry attempts.** Script the client to fail once and then succeed. Count provider attempts at the client or gateway and assert billed is at or above observed. Another test sets `attempts=2` and asserts the real attempt count, since it isn't necessarily 2.
6. **Unknown-cost rule.** Remove the join key from one call and assert the trace's cost is `unknown`, not a partial sum.
7. **Span double count.** One logical call produces both `call_llm` and `generate_content` spans. Assert the dashboard query sums once.
8. **Price table.** A `model_version`-keyed entry prices the call. A request-name-only entry shows as `unpriced_model`. A missing `cached_input` produces the `cached_input_charged_at_input_rate` flag.
9. **Reconciliation gate.** Compare computed cost against a fixture of gateway rows within a stated tolerance. A fixture invoice with the same shape would catch this regression in CI.

## Questions I could not ask, and the assumptions I used

- Which gateway or provider produces the invoice, and does it log trace ids? I assumed a provider total joined on trace and span. If it doesn't log trace ids, the join key is unavailable and cost stays unknown until that is fixed.
- Does the dashboard read spans or session exports? I assumed spans, with ADK's own output arithmetic.
- Which exact model? I assumed an OpenAI-style reasoning model whose completion count includes reasoning.

## Summary

- **Done:** read `invocation_summary.py` and the skill's references, and diagnosed the cause from them.
- **Left undone:** no tests written or run, and no reconciliation done. There is no session export, dashboard query, price table or ADK source here to check the claims against.
- **Evidence status:** the claims about ADK 2.12.0 and LiteLLM come from the skill's notes ("read 2026-10-25"). Treat them as `guidance`, not as verified this session.