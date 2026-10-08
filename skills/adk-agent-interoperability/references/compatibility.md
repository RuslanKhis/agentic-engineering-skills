# Compatibility and evidence boundaries

This skill was written against the `google-adk` **2.8.0** source (tag
v2.8.0, released 2026-08-25) and the `adk-python` main branch at **2.11.0**
(2026-10-01) with its CHANGELOG, both read on **2026-10-08**. Behaviour was
verified by reading source, not by running it. Treat every statement as
**source-verified, not executed** until the checks in
[validation](validation.md) have run on the target's interpreter and pins.

## The three contracts and their dates

| Contract | What ADK 2.8.0 pins or implements | Current upstream | Consequence |
| --- | --- | --- | --- |
| MCP Python SDK | `mcp>=1.24,<2` (`pyproject.toml`); `initialize` handshake, `Mcp-Session-Id` sessions, server-initiated sampling and elicitation callbacks, `_read_field` tolerates camelCase and snake_case | main pins `mcp>=1.24,<3`; 2.9.0 "support MCP SDK 2.x alongside 1.x" but "keep resolving MCP 1.x by default"; 2.11.0 "add an opt-in modern-protocol connect path for MCP SDK 2.x" | The installed `mcp` version is the contract. Under 2.x, closed models drop unknown `CallToolResult` and tool-declaration keys except `_meta` (2.9.0 CHANGELOG note); servers should carry extensions under `_meta` |
| MCP specification | Behaviour matches the 2025-xx revisions SDK 1.x implements | Revision **2026-07-28** (previous 2025-11-25): removes protocol sessions and `Mcp-Session-Id`, removes the `initialize` handshake in favour of per-request `_meta` version and capabilities plus a mandatory `server/discover`, moves Tasks to an extension, replaces server-initiated requests with Multi Round-Trip Requests (`resultType: "input_required"`), requires `ttlMs` and `cacheScope` on list results, deprecates Roots, Sampling, Logging, HTTP+SSE and Dynamic Client Registration (Client ID Metadata Documents instead), removes SSE resumability (normative changelog, read 2026-10-08) | Treat the spec date as a compatibility note, not as a description of what your ADK does. `mcp_tool_inventory.py` speaks the SDK 1.x handshake and falls back to `server/discover` best-effort; a server that only speaks the 2026 revision is a version decision for the whole stack |
| a2a-sdk | `a2a-sdk[http-server]>=0.3.4,<2`; `_compat.IS_A2A_V1` selects the branch by `a2a.types.StreamResponse`; 0.3 cards (`url`, `preferredTransport`, pydantic) and 1.x cards (`supportedInterfaces`, proto) both built and parsed; 1.x server routes keep `enable_v0_3_compat=True` | A2A specification 1.0.0 (`A2A-Version` header, `REJECTED` state, three bindings). 2.11.0 fixes a2a-sdk 0.3.4 to 0.3.10 breakage (5b079ee) | `agent_card_check.py --installed-a2a-sdk` compares the card's `protocolVersion` with the SDK generation. Numbers in 1.x data parts round-trip as floats (`_compat.data_part_dict` docstring) |

## Version-dependent interoperability surfaces

| Surface | 2.8.0 (pinned) | Later (CHANGELOG, main source) |
| --- | --- | --- |
| MCP tool and parameter descriptions | Reach the model unmodified | 2.10.0 fences them (`adk-agent-security` owns the consequence) |
| MCP session pool | Idle eviction (900 s), dead-task detection under `_MCP_GRACEFUL_ERROR_HANDLING` (on by default) | 2.10.0 rebuilds a session the server no longer holds (#7060); 2.11.0 detects a dead session behind a dispatcher; 2.10.0 stops probing mTLS on every session |
| ADC on MCP hosts | mTLS probe with `google.auth.default` for any HTTP connection; bearer injected when mTLS configured, host-limited | 2.9.0 only Google API hosts; 2.10.0 only over https |
| MCP tool list cache | `tool_list_cache_ttl_seconds` (2.7.0 feature), per header identity, 64 entries | Unchanged |
| Reserved MCP tool names | Skipped in `get_tools`, raise in `McpTool.__init__` (2.7.0) | Unchanged |
| stdio MCP in YAML configs | Rejected unless `ADK_ALLOW_CONFIG_STDIO_MCP_SERVERS` (2.7.0) | 2.11.0 loads validated MCP toolsets under `adk web` (#6735) |
| `to_mcp_server` | FastMCP (SDK 1.x), one tool, session per connection, experimental `MCP_AGENT_SERVER` | Import routed through a `dependencies._mcp` shim for SDK 2.x |
| `RemoteA2aAgent` card validation | RPC URLs https or loopback, same origin as the fetched card (2.7.0) | 2.9.0 requires https for a non-loopback card URL itself; stops caching a card that failed validation |
| Remote card description | Adopted when yours is empty (2.7.0); relayed unmodified | 2.9.0 quotes a fetched card description; main caps it at 1024 characters |
| Relayed auth and credentials | Credential requests not forwarded to the peer (2.8.0); credential responses scrubbed | 2.9.0 drops relayed auth responses |
| Stream ending early | Silent | 2.10.0 reports it (#6585) |
| Human-input pause resume | Flattened on resume (2.7.0) | 2.11.0 resumes a remote agent when a human answers its relayed pause (#6721) |
| Task mode and later delegations | Native task mode (2.8.0 "add native task mode support") | 2.9.0 stops a completed delegation breaking later peers (#6831); skips summarisation for terminal states |
| `RemoteA2aAgent` options | `use_legacy`, `config`, `auth_scheme`, `a2a_request_meta_provider` | 2.10.0 `context_builder` and `forward_session_id_as_context_id` |
| Approvals over A2A | Guard shipped and reverted in 2.8.0; #6461 open | PR under review at research time; contract rule in [a2a-contracts](a2a-contracts.md) stands on every version |
| `to_a2a` | `rpc_path`, `task_store`, `lifespan`, `agent_executor_factory`; instructions kept out of the card (2.7.0) | 2.11.0 documents the `Workflow` stuck-in-`working` and output-schema limits |
| `adk api_server --a2a` | Folders with `agent.json`, mounted under `/a2a/<name>` | Unchanged |

## Version floor guidance

| Floor | Why |
| --- | --- |
| At least 2.7.0 | RPC-target constraint on fetched cards; instructions out of the published card; stdio-in-config gate; tool list cache |
| Prefer 2.10.0 | Fenced MCP descriptions; early-ending A2A streams reported; stale MCP sessions rebuilt; https required for remote card URLs (2.9.0) |
| Prefer 2.11.0 | Human-input pause resume over A2A; dead-session detection behind dispatchers; a2a-sdk 0.3.4 to 0.3.10 fix |

The repository's 2.8.0 pin sits between these. Preserve it and present the
upgrade as a decision with the entries above.

## Evidence labels used in this skill

| Label | Meaning |
| --- | --- |
| Vendor guidance | Google, Anthropic or A2A project documentation and measurements |
| Documented behaviour | ADK docs, MCP specification, A2A specification |
| Independent evidence | Peer-reviewed paper or benchmark |
| Community report | Issue tracker, forum thread, practitioner blog |
| Source-verified | Read in the named google-adk file at the stated version |

Issue numbers, forum threads and platform documentation details marked
"supplied by research" were provided by the coordinator on 2026-10-08 and
were not re-fetched here except where a read date is given; confirm each
before quoting it to an owner.
