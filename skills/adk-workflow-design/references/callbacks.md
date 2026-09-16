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

For **agent-level** callbacks, these keyword names are part of the checked API:

| Hook | Parameters |
| --- | --- |
| Before/after agent | `callback_context` |
| Before model | `callback_context, llm_request` |
| After model | `callback_context, llm_response` |
| Model error | `callback_context, llm_request, error` |
| Before tool | `tool, args, tool_context` |
| After tool | `tool, args, tool_context, tool_response` |
| Tool error | `tool, args, tool_context, error` |

`BasePlugin` hooks have a different contract (for example `tool_args` and
`result` instead of the agent hook's `args` and `tool_response`). Inspect the
registration site as well as the function. Returning `types.Content` from
before-agent skips that agent; after-model can return a replacement `LlmResponse`,
and after-tool a replacement result. Replacements affect downstream consumption;
they do not undo an already completed tool side effect or remote model request.

Model-error fallbacks use `LlmResponse`; tool-error fallbacks use a dictionary.
Returning `None` leaves an error unhandled by that callback; propagation occurs
if no registered error callback supplies a fallback. Test the chain's actual
effect rather than asserting that a hook was merely registered.

## Compose policy hooks deliberately

Inspect plugin precedence and callback-list order. An earlier substitute may
short-circuit later hooks, so an authorisation check placed after a cache or
fallback might never run. Apply required checks before substitution, or enforce
the invariant in the deterministic tool/service boundary independently.

In the checked **ADK 2.8.0 agent `before_tool_callback` list**, iteration stops on a
truthy result, while execution is skipped when the final result is not `None`.
Consequently, `{}` followed by a callback returning `None` can allow the tool to
execute. Use a nonempty, explicit denial such as
`{"status": "denied", "reason": "not authorised"}`; return `None` only to allow
normal execution. Do not infer identical list behaviour for every hook/release.
The bundled [runtime tests](../tests/test_runtime_contracts.py) reproduce the
empty-result trap and exercise repeated nonempty denials with a working control.
That control uses synthetic local policy, not authenticated tenant identity.

Test the whole chain through the Runner: forbidden action count stays zero,
authorised action count is correct, the model receives only the safe substitute,
and errors still surface. A callback log proves it ran, not that it enforced the
required policy. Keep mandatory resource cleanup in an application lifespan or
`try/finally`, as detailed in [model-call-controls.md](model-call-controls.md).

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
