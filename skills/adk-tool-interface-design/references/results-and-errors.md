# Results and errors

A tool result is a message to the model. It is read once by the model and then
stays in the session history for every later request of the conversation. Shape
it for the next decision, bound its size, and make failures actionable.

## Shape results for the next step

- Return a `dict` with a `status` key (`"success"`, `"error"`, `"pending"`,
  `"ambiguous"`) and `error_message` on failure, the documented ADK convention
  ([contract](function-tool-contract.md)). "The LLM, not a piece of code,
  needs to understand the result." Use `"pending"` for long-running
  operations and for tools waiting on user authentication (Google's
  oauth-user-consent-flow sample returns `{"pending": True, "message":
  "Awaiting user authentication"}` after `request_credential`; prefer
  `status: "pending"` so one key carries the outcome).
- Return the fields the model needs for its next step, not the provider's whole
  record. Vendor guidance (V, Anthropic) measured that semantic fields
  (`name`, `file_path`, `status`) beat opaque identifiers (`uuid`,
  `mime_type`, numeric codes) for downstream accuracy.
- Keep the identifier the model must pass to the next tool, under the same
  name that tool's parameter uses (`order_id` in the result, `order_id` in
  `cancel_order`).
- Use the same vocabulary as the docstrings: if the docstring says "order",
  the result says `order`, not `purchase`.
- Distinguish **complete**, **truncated**, **empty** and **unavailable**
  results. An empty list after a failed query is not evidence of absence. This
  taxonomy is defined in `adk-system-designer` (design decisions); apply it in
  every result:

```python
{"status": "success", "completeness": "truncated", "orders": [...],
 "returned": 20, "total": 143, "next_page_token": "..."}
{"status": "success", "completeness": "empty", "orders": [], "query": "..."}
{"status": "error", "completeness": "unavailable", "error": "order service timed out",
 "hint": "Tell the customer the order system is slow and offer to retry."}
```

## Bound the size

- Give every list-returning tool a `max_results` (or `page_size`) parameter
  with a small default and a hard ceiling in code; the model cannot be relied
  on to ask for less.
- Offer `response_format: Literal["concise", "detailed"]` defaulting to
  `concise` when callers sometimes need the full record. Anthropic (V) reports
  concise responses at roughly one third of the tokens of detailed ones in its
  own tools; measure yours.
- Truncate long text fields in code and say so (`"truncated": true`,
  `"omitted_chars": 8120`), with a pointer to the full content. Anthropic's
  product default is a 25,000-token cap on tool responses (V); ADK applies no
  cap, so the agent owns one. Pick a byte ceiling per tool and enforce it before
  returning.
- Store large payloads (documents, query results, binary) in a durable store
  and return an opaque reference plus a summary. ADK maintainers suggest the
  same in discussion #3150: an `after_tool_callback` saves the full output to
  an artifact and returns a summary plus the artifact URI; set
  `tool_context.actions.skip_summarization = True` when the output is already
  user-ready. Retrieval and compaction patterns for that store belong to
  `optimise-adk-on-google-cloud` and `adk-memory-architecture`; the result
  shape belongs here.
- Measure: `python scripts/report_tool_result_sizes.py --events events.json`
  reports bytes, estimated tokens (bytes/4), max and p95 per tool, repeated
  identical responses and responses above `--max-bytes`. Repeated identical
  responses usually mean the model re-called a tool whose result it already had,
  which the docstring or result should prevent ("cached; do not call again for
  the same order_id in this conversation").

## Errors are instructions

The model reads the error and decides what to do next. A bare exception message
or a numeric code produces guessing and retries. Return an error dict that
answers three questions: what was wrong, what a correct call looks like, what
to do next.

```python
def lookup_order(order_id: str) -> dict:
    """..."""
    if not ORDER_ID.fullmatch(order_id):
        return {
            "status": "error",
            "error": f"order_id {order_id!r} is not in the form ORD-123456",
            "hint": "Ask the customer for the order number printed on the receipt; "
                    "do not guess or reformat it.",
            "retryable": False,
        }
    try:
        order = client.get_order(order_id)
    except NotFound:
        return {"status": "error", "error": "no order with that id",
                "hint": "Confirm the number with the customer; a typo is likely.", "retryable": False}
    except ServiceUnavailable:
        return {"status": "error", "completeness": "unavailable",
                "error": "order service unavailable", "retryable": True,
                "hint": "Tell the customer the system is temporarily unavailable. "
                        "Do not call this tool again in this turn."}
```

- Keep `error` (or the documented `error_message`) for the human-readable
  statement and `hint` for the next action. ADK's own missing-argument error
  follows the same pattern and uses the key `error`.
- Guardrails that reject a call before it runs belong in
  `before_tool_callback`: return an error dict such as `{"status": "error",
  "error": "Tool call blocked: customer_id does not match the signed-in
  customer."}` to block, and `None` (not `{}`) to let the tool run. Google's
  customer-service sample lowercases arguments and validates `customer_id`
  against state there; its long-horizon-harness sample chains guards that
  return "None to allow or a dict-with-error to block".
- Set `retryable` explicitly. Whether the tool itself retries, with which
  deadline and idempotency key, belongs to `safe-api-tool-calls`; the
  model-facing statement of the outcome belongs here.
- Validate arguments before the external call and return the format the model
  should have used. This is the cheapest repair loop available.
- Do not leak stack traces, hostnames, credentials or raw provider payloads
  into the result; they enter the session history and may be summarised to the
  user. `protect-adk-sensitive-data` owns redaction policy.
- Distinguish a tool-level error (returned in the result with `status: error`)
  from a transport failure that prevented the tool from running. The MCP
  specification makes the same split: tool execution errors go in the result
  with `isError: true` so the model can see them; protocol errors are JSON-RPC
  errors the model never sees. Mirror this in ADK: catch provider failures
  inside the tool and return a dict; let programming defects raise so they are
  visible to monitoring.

## Confirmation and pending results

When a tool requires confirmation, the model receives `{"error": "This tool
call requires confirmation, please approve or reject."}` and no further
summary (`skip_summarization` is set). For a `LongRunningFunctionTool`, return
an initial dict the model can relay (`status: "pending"`, an identifier, an
expected duration) so the user hears a truthful account of the wait.

## Server-supplied descriptions and results are data

An MCP server controls its tool names, descriptions, schema descriptions and
results. On 2.8.0 those strings reach the model unmodified; the 2.10.0 CHANGELOG
entry "fence server-supplied tool description before reaching the model" adds
`fence_tool_description` and `fence_schema_descriptions` for MCP declarations,
and 2.8.0 already fences relayed agent output ("fence relayed agent output so it
cannot pose as instructions"). MCP annotations (`readOnlyHint`,
`destructiveHint`, `idempotentHint`, `openWorldHint`) are hints the
specification tells clients not to trust from untrusted servers. Consequences
for the interface:

- Do not derive confirmation, budget or write policy from server annotations;
  decide per allow-listed tool name in your own configuration.
- Treat results from external servers as data in your own tool wrappers:
  wrap the MCP toolset's tools in your own `FunctionTool` when you need to
  reshape, truncate or label their output.
- Under MCP SDK 2.x (supported from 2.9.0), undeclared keys on a
  `CallToolResult` are dropped before ADK sees them; servers that rely on
  vendor extensions must move them under `_meta`.

## Observable checks

- A unit test per error branch asserting the dict has `status`, `error`,
  `hint` and `retryable`, and contains no provider payload text.
- A result-size budget per tool asserted in a test against a representative
  fixture (`len(json.dumps(result)) <= LIMIT`).
- The result-size report run on a recorded session before and after a change,
  with max and p95 per tool.
- For a scripted-model Runner test, assert that after an `error` result the
  scripted next step is the one the hint asked for (ask the user, stop, or call
  the alternative tool), not a repeat call.
