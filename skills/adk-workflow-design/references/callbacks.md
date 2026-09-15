# Callback and tool boundaries

Use callbacks when the requested change belongs at an existing agent, model or
tool boundary. Preserve parameter names: the runtime invokes them by keyword.
Check the pinned implementation before relying on return-value semantics.

In ADK 2.8.0, `LlmAgent` has eight callback fields including the two inherited
agent callbacks:

| Boundary | Hooks | Decision-changing contract |
| --- | --- | --- |
| Agent | `before_agent_callback`, `after_agent_callback` | After-agent content adds an event; it does not replace past events. Failure/early termination can skip it, so it is not guaranteed cleanup. |
| Model | `before_model_callback`, `after_model_callback`, `on_model_error_callback` | Before-model may return `LlmResponse` to skip the request. `None` leaves normal execution unchanged. |
| Tool | `before_tool_callback`, `after_tool_callback`, `on_tool_error_callback` | Before-tool may return a dictionary to skip execution and substitute a result. |

Model-error fallbacks use `LlmResponse`; tool-error fallbacks use a dictionary.
Returning `None` leaves an error unhandled by that callback; propagation occurs
if no registered error callback supplies a fallback. Test the chain's actual
effect rather than asserting that a hook was merely registered.

`CallbackContext` and `ToolContext` are aliases of the unified `Context` in the
checked version. Tool-call information is populated at its execution boundary.
Do not write compatibility logic assuming they are separate subclasses.

## Tool visibility is not authorisation

A custom `BaseToolset` can choose tools using its asynchronous
`get_tools(readonly_context)` method. Resolved tools are cached per invocation by
default in ADK 2.8.0; changing a state flag does not necessarily change exposure
mid-invocation. If a safe query must precede a flexible fallback, encode the order
in orchestration and authorise the proposed fallback at call time.

Use trusted caller context, deterministic argument checks and service-side
permissions. A model-provided user ID, role or consent claim is not authority.
Short-circuit tests must prove the forbidden tool never ran, including repeat
attempts, while an authorised control request still works.

## Logging and scope

Log allowlisted metadata and redact values before model/log exposure. Avoid raw
prompts, state, credentials or provider responses. Keep callbacks quick enough
that they do not become a latency bottleneck. Read the session-storage policy as
well; safe logging does not make raw persisted events safe.

The source demo verified a before-model log and `None` passthrough. SQL policy,
dynamic tool selection, auth enforcement, caching and error recovery above are
SDK behaviour or production principles, not demonstrated features of that demo.
Implement and test them only when the target task requires them.
