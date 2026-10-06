# Shape the model request

Use this reference when a session grows every turn, cached-token counts stay at
zero, tool results arrive unbounded, or a sub-agent receives history it does not
need. It covers what reaches the model on each call and how to keep that input
small, stable and complete. The runtime levers themselves (App compaction,
`ContextCacheConfig`, `include_contents`, result bounding) are introduced in
[skills-and-cache.md](skills-and-cache.md), [application.md](application.md) and
[runtime-application-integration.md](runtime-application-integration.md); read
those for wiring and this file for composition, budgeting and placement.
Session retention, replay and erasure belong to adk-memory-architecture;
checkpoint qualification belongs to adk-workflow-design. Link by skill name.

Every rule below pairs with an observable check. Source markers: **V** vendor
guidance, **E** measured evidence, **D** documented or inspected behaviour of the
pinned SDK or provider. Facts marked 2.8.0 were read from that tag's source on
6 October 2026 with no live run; check the pinned version against the changelog
before reusing them on another release.

## Trace how ADK composes one request

In ADK 2.8.0 the request processors build an `LlmRequest` in this order (D,
`flows/llm_flows/instructions.py` and `contents.py`):

1. **System instruction.** The deprecated `global_instruction`, then
   `static_instruction`, then `instruction` are appended to
   `config.system_instruction`. When `static_instruction` is set, `instruction`
   is no longer appended there: it is resolved with state injection and added
   as a `user` role `Content` in `contents`. Non-text `static_instruction` is
   kept as a stable prefix at index 0 of `contents` (2.8.0 "keep non-text
   static_instruction as a stable request prefix"). 2.9.0 labels that dynamic
   instruction so a model does not read it as a user turn; in 2.8.0 it is a
   plain user content.
2. **History.** With `include_contents='default'`, `_get_contents` applies
   rewinds, drops events from other branches (`_BranchPath` prefix match), other
   isolation scopes, empty content and ADK framework, auth and confirmation
   events, materialises compaction summaries at their end timestamp while
   removing raw events inside kept ranges, drops orphaned function responses
   and rewrites other agents' replies as user-role context. With
   `include_contents='none'`, `_get_current_turn_contents` scans backwards to
   the latest user or other-agent event that starts the current turn and builds
   contents from there only, so current-turn tool exchanges remain.
3. **Dynamic placement.** `_insert_transient_user_content` inserts the dynamic
   instruction and any tool-contributed instruction before the latest
   continuous user batch, or after a function response when the model is
   continuing a tool turn, and never ahead of a tracked static prefix.
4. **Tools.** `config.tools` carries the declarations of every tool the agent
   exposes for this call. `tool_config` follows.

Observable check: capture the outgoing `LlmRequest` with a deterministic
`BaseLlm` double (as in `tests/test_runtime_token_compaction.py`) or a
`before_model_callback(callback_context, llm_request)` that records a deep
copy and returns `None`. Assert where a synthetic marker lands: system
instruction, prefix content, history or the final user content. A model's
answer does not show composition.

## Split the budget and measure each slice

| Slice | What it holds in 2.8.0 | Measure from a captured `LlmRequest` | Authoritative count |
| --- | --- | --- | --- |
| Instructions | `config.system_instruction`, static prefix contents, serialised `config.tools` and `tool_config` | UTF-8 bytes of each, tools via `json.dumps(tool.model_dump())` | Provider `usage_metadata.prompt_token_count` on the response event covers all slices together |
| State | `{key}` interpolation inside `instruction` and dynamic instruction content | Diff the resolved instruction against the template; bytes added per key | Same |
| Retained history | Contents before the current turn, including materialised compaction summaries | Bytes per `Content` by role and part type, excluding the current turn | Same |
| Tool results | `function_response` parts in history and the current turn | Bytes of `json.dumps(response)` per call, largest first | Same |
| Current request | Latest user content plus transient dynamic content | Bytes of the last user batch | Same |

Record the split per model call, not per user turn: one turn can hold several
calls. The offline [context budget helper](../scripts/context_budget.py) reads a
saved session export and reports bytes and bytes/4 estimates by part type and
author, call/response pairs and orphans, the largest tool results, growth per
invocation, compaction spans and the last authoritative usage per invocation.
bytes/4 is the same heuristic the 2.8.0 compactor and cache manager use for
their own estimates (D); label it as an estimate and treat
`usage_metadata.prompt_token_count` as the measurement. Decide the overflow
rule for each slice before tuning: which slice shrinks first, and what must
never be dropped (current request, open function-call pairs, pending
approvals, authoritative locators).

## Place the request where the model reads it best

- **Put the current request last.** Gemini's long-context guidance says
  performance is better with the query at the end of the prompt (V). Liu et al.
  measured a U-shaped curve: information in the middle of long inputs is used
  worse than at the start or end (E). ADK's default composition already ends
  with the latest user batch; a `before_model_callback` that appends retrieved
  text after it reverses this. Check: the final `Content` in the captured
  request is the user's current message or the current function response.
- **Shorter inputs score higher on the same task.** Chroma's Context Rot report
  evaluated 18 models and found performance degrades with input length even on
  simple tasks, distractors hurt more as length grows, and needles with low
  similarity to the question degrade faster (E). Retained history is the slice
  most likely to carry distractors. Check: with the same tool results and a
  compacted versus raw history, compare answer correctness on a fixed
  evaluation set, not latency alone.
- **Recite the goal when the session is long.** Manus reports keeping a current
  objective near the end of context to counter drift in long tasks (V,
  production anecdote). In ADK the dynamic instruction sits before the latest
  user batch, so a goal placed in `instruction` or a `{plan}` state key is
  re-read each call without copying it into history. Check: the goal text
  appears once per request, in the dynamic position, and the summariser prompt
  preserves it across compaction.
- **Keep instructions at the right altitude.** Anthropic's context-engineering
  guidance favours a minimal set of high-signal instructions and canonical
  examples over exhaustive rules (V). Check: instruction bytes per request are
  flat across turns; growth belongs in state or retrieval, not the prompt.

## Keep the prefix stable

Implicit caching on Gemini keys off an identical request prefix (D). In 2.8.0
the explicit cache fingerprint covers `system_instruction`, `tools`,
`tool_config` and the first N contents (D, `gemini_context_cache_manager.py`),
and Runner warns when an app can transfer between agents without a
`context_cache_config` because every transfer swaps the system instruction and
tool set (2.7.0). Checklist, each with its check:

| Rule | Why | Check |
| --- | --- | --- |
| No timestamps, request IDs or per-user greetings in the system instruction | Any changed byte breaks the prefix | Two consecutive captured requests have byte-identical `system_instruction` |
| Deterministic serialisation of injected state and schemas | Dict ordering or float formatting can vary | Serialise with sorted keys; diff the resolved instruction across two turns with equal state |
| Stable tool declaration order and content | Tools are part of the fingerprint and provider prefix | `json.dumps([t.model_dump() for t in config.tools])` is identical across turns |
| Mask rather than add or remove tools mid-task | A changed tool set changes the prefix (Manus V; 2.7.0 transfer warning D) | Steer selection through instruction or state; the declared set is constant within a task |
| Static material first, dynamic material last | Caches extend only over an unchanged prefix | Dynamic instruction appears after the static prefix in the captured request |
| Meet the model's minimum | Implicit caching needs 2,048 tokens on Gemini 2.5 Flash and Pro and 4,096 on 3.x (Gemini API doc, D); the Vertex overview lists a higher floor for some 3.x implicit-only previews; ADK 2.8.0 applies 2,048 and 4,096 as explicit-cache floors by model name (D) | Read the exact model's row before expecting hits |
| Verify hits, not configuration | A configured cache is not a used cache | `usage_metadata.cached_content_token_count > 0` on the second and later calls; missing metadata means unknown |

`ContextCacheConfig.min_tokens` gates creation on the previous response's
`prompt_token_count` (`cacheable_contents_token_count`), scaled to the cached
prefix; the provider minimum applies independently. 2.8.0 removes cached
contents from the request after applying the cache; 2.9.0 "never empty the
request contents when applying a context cache" changed that edge case, and
2.6.0 canonicalised the fingerprint. Record the cache state on the LLM span
(2.8.0) alongside the usage counts.

When a configured cache never engages, work through this list (2.8.0 D unless
marked):

- The first request of a session is never cached: `min_tokens` gates on the
  previous request's actual prompt count and an explicit cache is created only
  when two consecutive fingerprints match. The 2.8.0 docstring states that
  caching begins on the second turn at the earliest and short or single-turn
  sessions are never cached.
- Defaults are `cache_intervals=10` (1 to 100), `ttl_seconds=1800` and
  `min_tokens=0`. `create_http_options=types.HttpOptions(timeout=10000)` bounds
  creation in milliseconds; a timed-out creation proceeds uncached.
- `CacheMetadata` carries name, expiry, fingerprint, invocations used and
  contents count, not token counts. Read `usage_metadata.cached_content_token_count`.
- A dynamic instruction that moves inside the fingerprinted prefix defeats the
  fingerprint match. Issue #6062 (June 2026, PR #6367) describes an explicit
  cache never created when `static_instruction` and `instruction` coexist;
  confirm the fix status on the pinned version by diffing two fingerprints.
- Measured example: Subramaniam (Google DevRel, 2026-09-01) reports a roughly
  38k-token static prefix over 4-5 turns reducing transmitted input tokens by
  74-79% and total cost by about 50-55%, with rules of thumb of not caching
  under roughly 32k tokens or three turns and placing dynamic variables at the
  end (E, one published run). Gemini bills cached tokens at a 90% discount on
  2.5 and later (75% on 2.0) with no storage cost for implicit caching;
  explicit caching bills creation plus hourly storage (V, caching doc).

## Admit tool results before compaction

Compaction summarises what already reached storage; it does not stop a large
result from reaching the next model call. Bound at the tool boundary first
(Anthropic "tool result clearing" V; [application.md](application.md) preview
rules).

In 2.8.0 `after_tool_callback(tool, args, tool_context, tool_response)` may
return `Optional[dict]`: a returned dict replaces the function response, `None`
keeps the original (D, `flows/llm_flows/functions.py`). With a list of
callbacks the first truthy result wins; a plugin `after_tool_callback` runs
first and, when it returns a value, the agent's callbacks are skipped. The
replacement is what the function-response event stores and what every later
request and summariser sees.

The optional [bounded result asset](../assets/bounded_tool_result.py) is a
teaching pattern for this callback: it keeps a UTF-8 safe preview, saves the
full payload as an artifact when the context offers `save_artifact`, and
returns `{"status": "success", "preview": ..., "artifact": name, "version": n,
"truncated": True}`. It leaves small results and non-dict results untouched and
preserves an explicit failure status rather than relabelling it. Adapt its
limits to the target's result contract.

Check: after one oversized call, the stored `function_response` holds the
bounded dict, `context_budget.py --max-result-bytes` flags nothing, and the
original payload is retrievable by name and version.

Two lighter alternatives exist. `ContextFilterPlugin(num_invocations_to_keep=,
custom_filter=, remove_amount=)` in `plugins/context_filter_plugin.py` (2.8.0
D; absent from the docs site) trims request contents without a summariser; it
changes what the model sees, not what storage holds, so test open tool pairs
across the cut. The adk-samples long-horizon harness (ADK 2.8.x) prunes old
large tool-result bodies behind `LHA_PRUNE_TOOL_OUTPUTS`, saves large outputs to
GCS artifacts and caps memory prefetch so a changing prefetch does not
invalidate the cached prefix each turn (V, sample repository, not inspected
here).

## Offload large payloads to artifacts

Verified 2.8.0 signatures (D, `agents/context.py`, inherited by `ToolContext`
and `CallbackContext`):

- `await tool_context.save_artifact(filename, artifact: types.Part, custom_metadata=None) -> int`
  returns the version; the first save is version 0 and the version is recorded
  in `actions.artifact_delta`.
- `await tool_context.load_artifact(filename, version=None) -> types.Part | None`
  returns the latest version when `version` is omitted.
- `await tool_context.list_artifacts() -> list[str]`.
- A filename starting with `user:` is user-scoped across sessions;
  `GcsArtifactService` stores it under `{app}/{user}/user/{filename}/{version}`
  and session files under `{app}/{user}/{session}/{filename}/{version}`.
- Both methods raise `ValueError('Artifact service is not initialized.')` when
  the Runner has no artifact service; `InMemoryArtifactService` serves tests
  and `GcsArtifactService` production.
- `LoadArtifactsTool` (`load_artifacts_tool`) lists artifact names in the
  request and loads content on demand, which is the just-in-time identifier
  pattern Anthropic describes (V) and the file-system-as-context pattern Manus
  reports (V).

Recipe: keep the identifier and a preview in the tool result (Manus: keep the
URL when truncating, V), save the body once, and let a later turn load it by
name and version. In 2.8.0 an `AgentTool` child reaches the parent's artifact
service through `ForwardingArtifactService`. Check: `artifact_delta` names the
file and version on the tool event; `load_artifact(name, version)` returns bytes
equal to the saved payload; the next captured request contains the preview and
name, not the body.

## Choose sub-agent isolation deliberately

Two production reports disagree, and both are right for their shape of work:

- Anthropic's multi-agent research system runs subagents in isolated context
  windows that return 1-2k token summaries; it reports roughly 15x the tokens
  of a single chat and justifies it for parallel, read-heavy research
  (2025-06-13, V).
- Cognition argues against multi-agent splits for sequential build tasks: share
  the full trace, because actions carry implicit decisions that a summary
  drops (2025-06-12, V).

Rule: isolate when the child's work is parallel or read-heavy and its output
is summarisable under an explicit handoff contract; share the full trace when
later steps depend on why earlier actions were taken. In ADK 2.8.0 (D):

- `include_contents='none'` keeps the child's own tool exchanges and current
  input while excluding prior turns.
- `AgentTool.run_async` builds its own `Runner` from the bare agent with an
  in-memory session, copies parent state (filtering `_adk` keys) into it,
  forwards `state_delta` back, and returns only the last content's text.
  `Runner._resolve_app` wraps that bare agent in an `App` without cache or
  compaction config, so the 2.7.0 changelog entry "propagate context cache
  config to the AgentTool sub-runner" needs confirmation in the pinned
  `agent_tool.py` before you rely on it.
- `mode='single_turn'` scopes events by `isolation_scope`; it is a delegation
  interface, not a one-call budget (see [application.md](application.md)). The
  2.8.0 `AgentTool` docstring discourages direct use and prefers a
  `single_turn` sub-agent in `sub_agents=[...]`, which runs inline in the
  parent session; add `load_artifacts_tool` to that sub-agent when it needs
  parent artifacts.
- Other agents' replies enter a request as user-role text fenced with
  `<<<BEGIN_QUOTED_AGENT_CONTENT>>>` markers (`flows/llm_flows/_fencing.py`),
  and user input is retained across `transfer_to_agent` (2.5.0). Issue #2207
  (closed, not planned) records that `include_contents='none'` still receives
  agent transition text inside a `SequentialAgent`; a `before_model_callback`
  that edits `llm_request.contents` is the recorded workaround.
- A community report describes recursive `AgentTool` calls growing a request
  from roughly 2k to over 80k tokens in five turns (discuss.google.dev thread
  396215, September 2026, anecdote). Count nested calls and bytes per level.

Check: the child's captured request lacks the parent's old-history marker and
contains the handoff fields; the parent's next request contains the child's
summary once; nested model and tool calls are counted in the shared budget.

## Know the compaction trigger in the pinned version

Facts read from 2.8.0 `apps/compaction.py` and `apps/_configs.py` (D):

- `EventsCompactionConfig(summarizer=, compaction_interval=, overlap_size=,
  token_threshold=, event_retention_size=)`; the token pair and the
  sliding-window pair must each be set together and at least one pair is
  required (2.6.0 "make EventsCompactionConfig sliding-window fields optional").
- Compaction runs after an invocation. The token path is preferred when both
  are configured. It reads the most recent event `usage_metadata.prompt_token_count`
  from any author, falling back to a chars/4 estimate over the effective
  contents that includes function call and response characters (2.8.0 "count
  tool call and response chars in compaction"); 2.10.0 measures the threshold
  against the agent's own prompt and stops the backwards scan at the
  compaction boundary.
- The trigger is `prompt_token_count >= token_threshold`; a large new input is
  not rejected (see `tests/test_runtime_token_compaction.py`).
- `event_retention_size` counts events and the split moves earlier to keep a
  function call with its response.
- The sliding window counts new invocations since the last compaction end
  timestamp and includes `overlap_size` earlier invocations.
- The summary is stored as a `user` authored event whose `actions.compaction`
  carries `start_timestamp`, `end_timestamp` and `compacted_content`; requests
  materialise it attributed to the reading agent. 2.11.0 keeps
  credential-request events out of the compaction prompt.

- With `summarizer=None`, 2.8.0 uses the root agent's `canonical_model` and
  raises `ValueError` when the root is not an `LlmAgent`. A workflow root such
  as `SequentialAgent` therefore needs an explicit
  `LlmEventSummarizer(llm=Gemini(...))`; a smaller Flash model is the usual
  choice (discussion #3374, V).
- Candidates exclude events inside a previous compaction range and the summary
  seed is the previous summary, so the next summary supersedes it. Earlier
  releases excluded pending function calls (1.28.0), human-in-the-loop events
  (1.34.0) and rewound invocations (2.5.0). Token compaction remains
  experimental (discussion #4215).
- Measured example: Bo Yang, "2-Minute ADK: Context Compaction", 2025-10-11,
  interval 3 and overlap 1 cut one prompt from 1,427 to 868 tokens, about 39%
  (E, one published run). A "60-80%" figure circulating on dev.to is
  unverified. The adk-samples long-horizon harness (ADK 2.8.x) ships
  `EventsCompactionConfig(summarizer=HorizonSummarizer, token_threshold=750_000,
  event_retention_size=20, compaction_interval=8, overlap_size=2)` with a
  `static_instruction` built once as a pure function of tool names, model and
  code-executor presence, and volatile data appended as trailing content (V,
  sample repository, not inspected here). Treat these as starting points to
  measure, not defaults.

Check: with a small `token_threshold`, observe the summariser input, the stored
compaction event and the next captured request separately; original events
stay in storage. The [context budget helper](../scripts/context_budget.py)
lists compaction events and the raw events each span covers.

## Observe token usage per call

ADK's metrics documentation lists `gen_ai.client.token.usage` per model call
and opt-in experimental per-invocation histograms
`adk.experimental.invoke_agent.{input,output,total,cache_read.input,reasoning.output,tool.input}_tokens`
(D). The 2.8.0 generate-content span records cache state (2.8.0) and 2.7.0
records implicit versus explicit cache type in analytics. Compaction has had
OpenTelemetry spans since 1.32.0. Check: the per-invocation input histogram
flattens after compaction and `cache_read.input_tokens` is positive when a
cache is claimed; a configuration print proves neither.

## Known pitfalls

| Issue | Observed | Status at writing | Detection |
| --- | --- | --- | --- |
| adk-python #7236 | An orphaned `function_call` (process died mid-tool) silently disables token compaction after the first compaction | Reported 2026-09-22 against 2.9.2, open | `context_budget.py` orphan report; ensure every call receives a response or prune orphans at the app layer |
| adk-python #3530 | Compaction crash on `DatabaseSessionService`, `'dict' object has no attribute 'start_timestamp'` | November 2025, closed; fix version unclear | Run a compaction through the real session backend offline before deploying |
| adk-python #6062 | Explicit cache never created while `static_instruction` and dynamic `instruction` coexist | June 2026, PR #6367; verify on the pinned version | Two consecutive fingerprints differ while system instruction and tools are equal |
| adk-python #6945 | Cache application emptied request contents | Fixed in 2.9.0 | Captured request after cache application still holds the current turn |
| adk-python #2207 | `include_contents='none'` still sees agent transitions in `SequentialAgent` | Closed, not planned | Old-history marker check on the child's captured request |
| adk-python #4700 | Human-in-the-loop `LongRunningFunctionTool` response triggers an extra summary turn | Open | Count model calls per approval round trip |

Issue links follow `https://github.com/google/adk-python/issues/<number>`.

## Sources

| Source | Type | Used for |
| --- | --- | --- |
| Chroma, "Context Rot", 2025-07-14, https://www.trychroma.com/research/context-rot | E | 18 models; degradation with input length on simple tasks; distractors; low needle-question similarity |
| Liu et al., "Lost in the Middle", arXiv 2307.03172, https://arxiv.org/abs/2307.03172 | E | Position effects; query last |
| Gemini long-context guide, https://ai.google.dev/gemini-api/docs/long-context | V | "Put your query at the end of the prompt" |
| Anthropic, "Effective context engineering for AI agents", 2025-09-29, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | V | Right altitude, minimal set, just-in-time identifiers, tool result clearing, compaction, structured notes, sub-agents, canonical examples |
| Anthropic, "How we built our multi-agent research system", 2025-06-13, https://www.anthropic.com/engineering/multi-agent-research-system | V | Isolated windows, 1-2k token summaries, roughly 15x tokens |
| Cognition, "Don't build multi-agents", 2025-06-12, https://cognition.com/blog/dont-build-multi-agents | V | Share full traces; actions carry implicit decisions |
| Manus, "Context engineering lessons", 2025-07-18, https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus | V, production anecdote | File system as context, keep the URL when truncating, recite goals, stable prefix, mask tools |
| Gemini caching, https://ai.google.dev/gemini-api/docs/caching | D | Implicit caching minimums 2,048 (2.5 Flash/Pro) and 4,096 (3.x); cached token field |
| Vertex context cache overview, https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | D | Per-model minimums including higher implicit-only floors |
| ADK compaction, https://adk.dev/context/compaction/ and caching, https://adk.dev/context/caching/ | D | Trigger descriptions; `min_tokens`, `ttl_seconds`, `cache_intervals` |
| ADK artifacts, https://adk.dev/artifacts/ and metrics, https://adk.dev/observability/metrics/ | D | Session state is not for large data; `GcsArtifactService` in production; token histograms |
| ADK CHANGELOG, tags 2.6.0 to 2.11.0 | D | Version-specific behaviour named above; check the pinned version against the changelog |
| Bo Yang, "2-Minute ADK: Context Compaction", 2025-10-11, https://medium.com/google-cloud/2-minute-adk-context-compaction-in-a-snap-470da15c30f4 | E, one run | 1,427 to 868 prompt tokens with interval 3, overlap 1 |
| Balaji Subramaniam, "How to Slash Token Costs with Context Caching in Agent Harnesses", 2026-09-01, https://medium.com/google-cloud/how-to-slash-token-costs-with-context-caching-in-agent-harnesses-6431ba16d931 | E, one run | 74-79% fewer transmitted input tokens; rules of thumb |
| adk-samples, `core/python/long-horizon-harness/AGENTS.md`, https://github.com/google/adk-samples | V, sample | Production-style compaction and static-prefix values; not inspected here |
| adk-python discussions #3374 and #4215, https://github.com/google/adk-python/discussions | V | Explicit summariser for workflow roots; experimental status |
