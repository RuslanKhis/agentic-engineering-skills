# Compatibility and evidence boundaries

This skill was written against the `google-adk` **2.8.0** source (tag v2.8.0)
and the `adk-python` main branch at **2.11.0** with its CHANGELOG, both read on
**2026-10-07**. Behaviour statements were verified by reading that source, not
by running it. Treat every statement as **source-verified, not executed**;
confirm on the target's own interpreter with the checks in
[validation](validation.md) before relying on it.

## Version-dependent security surfaces

| Surface | 2.8.0 (pinned) | Later versions (CHANGELOG, main source) |
| --- | --- | --- |
| Relayed other-agent output | Fenced: `flows/llm_flows/_fencing.py` wraps another agent's text in `<<<BEGIN_QUOTED_AGENT_CONTENT>>>` markers, elides forged markers, and prepends a preamble saying the block is data, not instructions (2.8.0 "fence relayed agent output so it cannot pose as instructions") | Module moved to `flows/llm_flows/context/_fencing.py`; same markers |
| MCP tool and parameter descriptions | Reach the model unmodified (`mcp_tool.py` passes `mcp_tool.description` straight into the declaration) | 2.10.0 "fence server-supplied tool description before reaching the model": `fence_tool_description` and `fence_schema_descriptions` wrap them in `<<<BEGIN_UNTRUSTED_TOOL_DESCRIPTION>>>` markers |
| Remote A2A agent-card description | Not fenced | main `_remote_a2a_agent.py` caps and quotes the description with `quote_untrusted` |
| The agent's own tool results (`function_response` parts), OpenAPI descriptions, inline blobs | Not fenced | Not fenced; screen in `after_tool_callback` (see [tool supply chain](tool-supply-chain.md)) |
| Stored function-call integrity | None | 2.11.0 optional `ToolCallIntegrityPlugin` (`plugins/_tool_call_integrity_plugin.py`): HMAC stamp on each emitted function call, checked before each run; a tool runs only with a valid stamp |
| Tool confirmation hold | `FunctionTool.run_async` checks `tool_context.tool_confirmation.confirmed` and requests confirmation otherwise; a custom `BaseTool` must do this itself | 2.10.0 "hold a tool call that requires confirmation in the framework" and "only hold a tool call when its confirmation hook answers True"; 2.11.0 workflow tool nodes pause via `RequestInput` |
| Confirmation forgery | 2.5.0 and 2.6.0 "Prevent continuation forgery in tool confirmation" (CVE-2026-18236 range below 2.5.0 per the community disclosure; verify on the target's exact pin) | 2.10.0 "skip confirmation requests authored by other agents before resolving history" |
| Approvals over A2A | 2.8.0 shipped "reject tool confirmations arriving over A2A" and in the same release "revert the A2A guard that broke every HITL tool confirmation"; the gap (google/adk-python#6461) remains open | PR #7134 (caller principal) under review at time of writing |
| Resume dispatch | Caller-authored function calls could be dispatched on resume | 2.10.0 "require agent authorship before resume-dispatching a function call" (#7076) |
| stdio MCP in YAML configs | 2.7.0 rejects stdio servers in agent configs unless `ADK_ALLOW_CONFIG_STDIO_MCP_SERVERS` is set (`mcp_toolset.py` constant) | Unchanged |
| MCP SDK | 1.x | 2.9.0 adds 2.x; closed models drop unknown `CallToolResult` keys (`_meta` kept) |
| ADC on MCP hosts | Research note: ADC attached to non-Google or non-HTTPS MCP hosts was fixed in 2.9.0 and 2.10.0 (community report; not re-verified here) | Verify in the target's `mcp_session_manager.py` |
| `ContainerCodeExecutor` | `network_enabled: bool = False`; docstring: container starts with networking disabled and all capabilities dropped so code cannot reach the metadata endpoint `169.254.169.254`; prefers `GkeCodeExecutor` or a managed executor for untrusted code | Unchanged |
| GKE sandbox credential | 2.6.0 "do not mount a cluster credential into the GKE code sandbox" | Unchanged |
| `BashToolPolicy` | `allowed_command_prefixes: tuple[str, ...] = ("*",)` allows every command by default | Unchanged |
| adk web and API server | ADK Web is "not meant for use in production deployments" (docs); `adk deploy cloud_run` example passes `--no-allow-unauthenticated` | Same |
| GitHub-event prompt injection in samples | 2.6.0 "treat GitHub content as untrusted in the adk_team sample agents"; 2.8.0 "prevent prompt injection via GitHub event data in workflows" | Same |

## Version floor guidance

| Floor | Why (evidence) |
| --- | --- |
| At least 2.7.0 | Clears the adk web remote code execution range: CVE-2026-4810 (1.7.0 to 1.28.0, fixed 1.28.1) and CVE-2026-79696 (2.0.0 to 2.6.0, fixed 2.7.0, crafted test-session replay when pytest is installed); CVE-2026-79707 path traversal (1.9.0 to 1.21.0). Community and vulnerability-database reports; see [sources](sources.md). The inspector flags a lower pin as `known_cve_range`. |
| At least 2.10.0 | Server-supplied tool descriptions fenced; confirmation held in the framework; agent authorship required before resume dispatch (CHANGELOG, source-verified on main). |
| Prefer 2.11.0 | `ToolCallIntegrityPlugin` when session stores are writable by anything other than the Runner (CHANGELOG, source-verified on main). |

The repository's 2.8.0 pin sits between these floors: it has relayed-output
fencing and the forged-confirmation fixes, but not description fencing or the
integrity plugin. Preserve the pin and present the upgrade as a decision.

## Open issues to carry in the review (community reports, verify status)

| Report | Consequence | Mitigation on any version |
| --- | --- | --- |
| google/adk-python#6461 (open) | A2A inbound content has `role=user`, so approval checks on author alone can be self-approved by a peer | Accept approvals only from the authenticated controlling user at the API layer; never from A2A or an unauthenticated `/run` |
| #7148 (open, 2.9.1+) | Deny verdict not enforced for custom `BaseTool`; the framework never reads `ToolConfirmation.confirmed` for them | Custom tools check `tool_context.tool_confirmation.confirmed` themselves; the inspector reports `custom_tool_ignores_confirmation` |
| #7010 (open) | `require_confirmation` callable returning a non-bool skips the gate | Return a strict `bool`; the inspector reports `confirmation_callable_review` |
| #6828 (closed 2026-08-20) | `before_run_callback` early exit ignored on the node path, so plugin-based input blocking was bypassed | Test that the blocking plugin blocks, through the Runner, on the pinned version |
| #7311 (open) | `AuthCredential` secrets in span attributes | Set `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; `adk-tool-auth-and-secrets` owns credential handling |
| #5112 (open) | No `secret:` state scope; OAuth tokens persisted in session services | Keep tokens out of state; `adk-tool-auth-and-secrets` |
| #7103, #6964 (pending) | Own tool results unfenced; Model Armor plugin does not screen tool inputs | `after_tool_callback` provenance and screening; `protect-adk-sensitive-data` for the plugin's limits |

Issue numbers and statuses were supplied by the coordinator's research on
2026-10-07 and were not re-fetched here; confirm each before quoting it to an
owner.

## Evidence labels used in this skill

| Label | Meaning |
| --- | --- |
| Vendor guidance | Google, Anthropic, OpenAI or Microsoft documentation or measurements |
| Documented behaviour | ADK docs, Gemini API docs, MCP specification |
| Independent evidence | Peer-reviewed paper or published benchmark |
| Community report | Issue tracker, security disclosure, practitioner blog |
| Source-verified | Read in the named ADK source file at the stated version |

A control labelled vendor guidance or documented behaviour is a reasonable
default; one labelled independent evidence has been measured somewhere other
than the vendor; none is a measurement on the target until the suite in
[adversarial testing](adversarial-testing.md) has run against it.
