# Compatibility and evidence boundaries

This skill was written against the `google-adk` **2.8.0** source (tag v2.8.0)
and the `adk-python` main branch at **2.11.0** with its CHANGELOG, both read on
**2026-10-07**. The 2.12.0 release (2026-10-13) was read from `CHANGELOG.md`
at main commit ed76f94 on 2026-10-22; its entries are labelled 2.12.0 below
and the fixed code paths were not read. Behaviour statements were verified by
reading that source, not by running it. Treat every statement as **source-verified, not executed**;
confirm on the target's own interpreter with the checks in
[validation](validation.md) before relying on it.

## Version-dependent security surfaces

| Surface | 2.8.0 (this toolkit's reference baseline, not your project's pin) | Later versions (CHANGELOG, main source) |
| --- | --- | --- |
| Relayed other-agent output | Fenced: `flows/llm_flows/_fencing.py` wraps another agent's text in `<<<BEGIN_QUOTED_AGENT_CONTENT>>>` markers, elides forged markers, and prepends a preamble saying the block is data, not instructions (2.8.0 "fence relayed agent output so it cannot pose as instructions") | Module moved to `flows/llm_flows/context/_fencing.py`; same markers |
| MCP tool and parameter descriptions | Reach the model unmodified (`mcp_tool.py` passes `mcp_tool.description` straight into the declaration) | 2.10.0 "fence server-supplied tool description before reaching the model": `fence_tool_description` and `fence_schema_descriptions` wrap them in `<<<BEGIN_UNTRUSTED_TOOL_DESCRIPTION>>>` markers |
| Remote A2A agent-card description | Not fenced | main `_remote_a2a_agent.py` caps and quotes the description with `quote_untrusted` |
| The agent's own tool results (`function_response` parts), OpenAPI descriptions, inline blobs | Not fenced | Not fenced; 2.12.0 makes `after_tool_callback` the supported point to intercept and filter a tool's output before the model sees it ("add after_tool_callback to screen tool output", fdda17c, closes #6966); screen there on every version (see [tool supply chain](tool-supply-chain.md)) |
| Stored function-call integrity | None | 2.11.0 optional `ToolCallIntegrityPlugin` (`plugins/_tool_call_integrity_plugin.py`): HMAC stamp on each emitted function call, checked before each run; a tool runs only with a valid stamp |
| Tool confirmation hold | `FunctionTool.run_async` checks `tool_context.tool_confirmation.confirmed` and requests confirmation otherwise; a custom `BaseTool` must do this itself | 2.10.0 "hold a tool call that requires confirmation in the framework" and "only hold a tool call when its confirmation hook answers True"; 2.11.0 workflow tool nodes pause via `RequestInput`; 2.12.0 runs a confirmed tool once per approval (bfdeb4a, closes #7434) and lets workflow nodes (`@node`, `FunctionNode`) take `require_confirmation` (988fd1a) |
| Confirmation forgery | 2.5.0 and 2.6.0 "Prevent continuation forgery in tool confirmation" (CVE-2026-18236 range below 2.5.0 per the community disclosure; verify on the target's exact pin) | 2.10.0 "skip confirmation requests authored by other agents before resolving history" |
| Approvals over A2A | 2.8.0 shipped "reject tool confirmations arriving over A2A" and in the same release "revert the A2A guard that broke every HITL tool confirmation"; the gap (google/adk-python#6461) remains open | PR #7134 (caller principal) under review at time of writing |
| Resume dispatch | Caller-authored function calls could be dispatched on resume | 2.10.0 "require agent authorship before resume-dispatching a function call" (#7076) |
| Serving and dev endpoints | Pre-fix behaviour implied by the 2.12.0 entries; not re-read in the 2.8.0 source | 2.12.0 "stop OAuth2 secrets from leaking over /run, /run_sse, /run_live, dev_server, and session endpoints" (63aed55); mutating `/dev` and agent-builder endpoints restricted to local clients by default (97f9379); built-in agents enabled only when `adk web` binds loopback, 403 otherwise (eca36ac, 7e4407f); warning when the dev server binds a non-loopback address (ec7756b) |
| ADK user id | Pre-fix behaviour implied by the 2.12.0 entry; not re-read in the 2.8.0 source | 2.12.0 "take the ADK user id only from an authenticated principal" (d0c4060); auth credentials kept out of the caller's tool args (d8483a0, closes #7162); non-OAuth credential secrets redacted from the auth request event (82af2ef); Google credential encrypted in session (42a17a9) |
| Tool sub-branch events | In the calling agent's LLM context | 2.12.0 "keep tool sub-branch events out of the calling agent's LLM context" (2e06fdc) |
| Trigger redelivery | No delivery id for a tool to check | 2.12.0 exposes the trigger delivery id so tools can detect redeliveries (74cd0ef, closes #7322); OIDC audience required when trigger endpoints are enabled (b3ccb29) |
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
| At least 2.12.0 when the agent serves several users over ADK's HTTP endpoints or holds delegated OAuth credentials | OAuth2 secrets no longer leak over the serving and session endpoints; the ADK user id comes only from an authenticated principal; mutating `/dev` and agent-builder endpoints are loopback-only by default; a confirmed tool runs once per approval; `after_tool_callback` can filter tool output (CHANGELOG 2.12.0, read 2026-10-22). Below it, the application's own identity verification and output projection (`adk-tool-auth-and-secrets`) are the only guard. |

This toolkit's 2.8.0 reference baseline sits between these floors: it has relayed-output
fencing and the forged-confirmation fixes, but not description fencing, the
integrity plugin or the 2.12.0 serving-endpoint and principal fixes. Preserve
the pin and present the upgrade as a decision.

## Open issues to carry in the review (community reports, verify status)

| Report | Consequence | Mitigation on any version |
| --- | --- | --- |
| google/adk-python#6461 (open) | A2A inbound content has `role=user`, so approval checks on author alone can be self-approved by a peer | Accept approvals only from the authenticated controlling user at the API layer; never from A2A or an unauthenticated `/run` |
| #7148 (open, 2.9.1+) | Deny verdict not enforced for custom `BaseTool`; the framework never reads `ToolConfirmation.confirmed` for them | Custom tools check `tool_context.tool_confirmation.confirmed` themselves; the inspector reports `custom_tool_ignores_confirmation` |
| #7010 (open) | `require_confirmation` callable returning a non-bool skips the gate | Return a strict `bool`; the inspector reports `confirmation_callable_review` |
| #6828 (closed 2026-08-20) | `before_run_callback` early exit ignored on the node path, so plugin-based input blocking was bypassed | Test that the blocking plugin blocks, through the Runner, on the pinned version |
| #7311 (open) | `AuthCredential` secrets in span attributes | Set `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; `adk-tool-auth-and-secrets` owns credential handling |
| #5112 (open) | No `secret:` state scope; OAuth tokens persisted in session services | Keep tokens out of state; `adk-tool-auth-and-secrets` |
| #7103, #6964 (pending) | Own tool results unfenced; Model Armor plugin does not screen tool inputs | `after_tool_callback` provenance and screening (a supported output-filtering point from 2.12.0); `protect-adk-sensitive-data` for the plugin's limits |

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
