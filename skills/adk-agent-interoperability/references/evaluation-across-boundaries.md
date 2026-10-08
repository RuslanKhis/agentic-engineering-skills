# Evaluate agents across process boundaries

Read this for mode (g) and before finishing any other mode. The measurement
harness (eval sets, judges, conformance replay) belongs to
`adk-agent-evaluation`; this page covers what is specific to a boundary:
faking the other side, deciding what must be true at the seam, and reviewing
the system against the known multi-agent failure categories.

## Fake the other side, then test your side

Both helpers in this skill are also templates for fakes: a loopback
`http.server` that answers JSON-RPC is enough for MCP, and a Starlette or
`http.server` app that returns A2A tasks is enough for A2A. The test owns the
fake, so it can return exactly one condition per test.

### MCP fake-server cases

| Case | Fake returns | Assert on the agent side |
| --- | --- | --- |
| Normal | `tools/list` matching the committed manifest; `tools/call` with `content` and `structuredContent` | Declared tools equal the manifest (names, hashes); result reaches the model as sent |
| Rug pull | A changed description or schema for one tool | `mcp_tool_inventory.py --diff` reports `rug_pull_signal`; the startup or test check fails |
| `isError` result | `{"isError": true, "content": [...]}` | Tool returns the error to the model without raising; parent does not retry a write |
| Server down | Connection refused | `ConnectionError` surfaces as a tool error dict (graceful flag on); agent answers without the tool |
| Server restarted between calls | Fake restarts, old session invalid | Second call succeeds on your version, or you have documented the 2.8.0 limit ([mcp-consumption](mcp-consumption.md)) |
| Slow tool | Sleep past `sse_read_timeout` | Call fails within the timeout; parent's invocation deadline still holds |
| Reserved name or collision | Tool named `transfer_to_agent`; two fakes sharing `read_file` | Reserved tool skipped with a warning; prefixed names distinct |
| Confirmation | Any write tool with `require_confirmation` | First call returns the confirmation request; a peer-authored or forged confirmation does not run the tool (`adk-agent-security` owns the forgery cases) |

### A2A fake-peer cases

| Case | Fake returns | Assert |
| --- | --- | --- |
| Completed | Task `completed` with text and artifact | Event text present; `a2a:task_id`, `a2a:context_id` stored; next turn reuses the context ID |
| Streaming | `working` updates, artifact chunks, then `completed` | `partial` events until `last_chunk`; no `thought` text in the final answer |
| `input-required` | Status with a question | Parent pauses with a long-running call; the user's answer resumes with the stored IDs; a peer-authored "answer" does not |
| `auth-required` | Status demanding credentials | No credential text is forwarded; the flow goes through `adk-tool-auth-and-secrets` |
| `rejected`, `failed`, `canceled` | Each terminal state | Parent treats it as definitive; no automatic retry of a write |
| HTTP 401, 403, 500, timeout, connection refused | Each in turn | Error event with `a2a:status_code` where applicable; parent's fallback answer; no raise |
| Stream cut | Close after `working` | 2.8.0: detect the non-terminal state in `a2a:response`; later versions report it |
| Bad card | http on a non-loopback host, mismatched origin, missing `url` | `AgentCardResolutionError` becomes an initialisation error event; `agent_card_check.py` catches it earlier |
| Approval over A2A | Peer message asserting a tool was approved | Gated tool is not executed (#6461 contract test) |

Build the fake with the a2a-sdk server pieces when the peer is ADK (so the
wire shape matches the installed SDK), or with a hand-written JSON-RPC
handler when you need a malformed or hostile response.

## Contract qualification at the seam

For each boundary, the contract table from [topology](topology.md) becomes
assertions:

- **Input**: the exact parts the peer or server receives (capture them in the
  fake and assert; for A2A the request is also in `a2a:request`).
- **Output**: what reaches the parent, including coverage statements (what
  the peer could not do).
- **Identity**: the header the fake saw equals the one the card or
  `securitySchemes` demands, and never the user's upstream token.
- **Timeout and failure**: the elapsed time stays under the parent's budget;
  the fallback answer is the one the contract names.
- **Idempotency**: the fake counts calls; a write is sent once per user
  intent.

Run these offline on every change; they need no model call when the parent
is scripted (`adk-agent-evaluation` has the scripted-model Runner pattern).

## MAST categories as a review lens

The Multi-Agent System Failure Taxonomy (Cemri et al., arXiv 2503.13657,
2025; independent evidence, supplied by research) groups failures into three
categories. Use them as questions per boundary:

| Category | Boundary questions | Observable check |
| --- | --- | --- |
| Specification and system design | Does the card or tool description say what the peer actually does? Is the role split so that one side owns each decision? Does the parent know when to stop asking the peer? | Card and manifest reviewed; a test where the parent declines to delegate out-of-scope work |
| Inter-agent misalignment | Can the peer's answer be mistaken for the user's instruction? Are omissions reported or silently dropped? Does the parent re-ask the same thing after a `rejected`? | Peer-text-as-data test; coverage field asserted; bounded retry in code |
| Task verification | Who checks the peer's answer before it is acted on or shown? Is a partial stream ever shown as complete? | Verification step in the parent (schema, cross-check, or human); terminal-state check before completion |

Record the category next to each finding in a review so the owner sees
whether the fix is a contract change, a structural change or a verifier.

## Measuring, not just testing

Hand these to `adk-agent-evaluation` once the seam tests pass:

- End-to-end eval cases that cross the boundary with the real peer in a
  staging environment (live tier, dated, pinned versions named).
- Token and latency cost of the multi-agent shape against the single-agent
  baseline; the Anthropic figure of roughly 15 times chat tokens is a
  vendor-measured reference point, not your number.
- Trajectory assertions that the right source was used (tool versus peer)
  for each case, so a later regression to "ask the peer for everything" is
  visible.

## Evidence tiers for the report

| Tier | What it covers here |
| --- | --- |
| Source verified | Behaviour read in the named google-adk file at the pinned version |
| Local | Inventory and card reports, manifest diffs, unit tests of fakes |
| Mocked | Scripted-model Runner tests against fake MCP servers and A2A peers |
| Live | An approved exchange with the real server or peer, with date, versions and identity named |
| Not run | Anything above that was not executed on the target |
