# LiteLLM alignment — 25 October 2026

Source note: [comparison](../research/litellm-comparison-2026-10-25.md).

## Changed journey

`adk-agent-observability`, token and cost accounting.

## Fresh-agent trial

A fresh agent with only the skill packages built an ADK 2.12 research
agent with two `AgentTool` children, all on `LiteLlm` with an OpenAI-style
reasoning model and two retry attempts, ran it offline through the real
`LiteLlm` adapter over a scripted client, and reconciled the saved session
and spans against synthetic gateway rows with one retried attempt and one
failed-but-billed call. No real price was used.

It reproduced all three causes the skill names, and found a fourth:

| Figure | Value |
| --- | --- |
| Root call: provider completion vs ADK span output | 300 vs 500 |
| Parent session model calls vs trace `generate_content` spans | 4 vs 7 |
| Gateway billed attempts for 7 logical calls | 8 |
| Output summed over every span vs `generate_content` only | 10,600 vs 5,300 |
| Session cost (helper) vs gateway cost, synthetic units | about 1 to 3 |

`pytest`: **8 passed**; the skill's own helper tests 21 passed. The helper
flagged `reasoning_counted_twice_on_4_calls`.

Ease: 4 of 5.

## Frictions and fixes (same day)

1. The helper flagged the double count but still priced it. Fixed: a
   flagged call's output is priced from candidates alone, with a test.
2. On 2.12 the `call_llm` span repeats the usage of its `generate_content`
   span. Fixed (checked in 2.12.0 telemetry source).
3. Which span id the gateway sees. Fixed: check the gateway records the
   trace context; otherwise the call is unknown.
4. A failed `AgentTool` child is recorded as result text, not a tool error.
   Fixed, as observed.
5. Running `LiteLlm` offline needs `litellm` installed and a
   `LiteLLMClient` subclass. Fixed.
6. Price-table keys on `LiteLlm`. Fixed: the session's `model_version`.
7. Version labelling of the 2.12 facts. Not changed: each 2.12 fact carries
   its own date and source.
8. "Ignore the reported total" against the guardrails skill's "prefer
   provider totals". Fixed: on `LiteLlm` the provider total is the reliable
   one.
9. No session dump call. Fixed.

## Limits

No provider or gateway was called; the reconciliation used synthetic rows.
