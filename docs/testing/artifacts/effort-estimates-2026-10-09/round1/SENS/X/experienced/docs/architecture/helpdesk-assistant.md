# System design: IT helpdesk runbook and ticket assistant

Status: **draft**. Written in one pass without the user; every row in
"Assumed answers" is provisional until the user confirms it, and so is every
decision that depends on it.
Plan: [docs/plans/helpdesk-assistant.md](../plans/helpdesk-assistant.md).
Tickets: [docs/tickets/helpdesk-assistant/](../tickets/helpdesk-assistant/).

## Assumed answers

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When must the first version exist; is it continued? | End of the two weeks; kept and continued | Phase 1 code is the kept form (D1–D7) |
| A2 | Builders and hours | Given: two senior engineers, ~half time for two weeks, experienced with ADK on GCP. Assumed: the helpdesk team lead runs it afterwards with those engineers on call | Capacity, D6 |
| A3 | Model and cloud budget | Small internal allowance (order of tens of USD per month); an existing GCP project and billing account the engineers may deploy to | D5, budget alert |
| A4 | Users and what they read | The 25 helpdesk staff, daily, through a web page; all are in one Google Workspace group | D1, D6 |
| A5 | Data touched and effects | Confluence **Cloud** runbook spaces (internal, may contain hostnames and occasionally credentials); one Jira **Cloud** project where the assistant creates issues. No other writes | D2, D3, D4, floor |
| A6 | Who may read which runbooks | Every helpdesk member may read every page in the allowlisted runbook spaces; no page-level restriction narrower than the group | D2 (service-account search); verified in G01 |
| A7 | Whose name is on a created ticket | Created by an assistant service account, with the requesting engineer as reporter (or named in a field when reporter cannot be set) | D4; per-user OAuth deferred |
| A8 | Sign-in | Google Workspace accounts; GCP Identity-Aware Proxy (IAP) acceptable | D6 |
| A9 | Interface | A small web page is acceptable; no Slack/Google Chat bot in phase 1 | D6 |

## Purpose and constraints

**Journey.** A helpdesk engineer on a call types "VPN client fails with error
809 on Windows 11 laptops — what's the fix?". Today they search Confluence by
keyword, open several pages and skim them while the caller waits, then retype
the problem into Jira when it needs escalation. The assistant returns the
relevant runbook steps with links to the pages it used, and when the engineer
says "open a ticket for networking", it drafts the Jira issue (summary,
description, component, runbook links), shows it, and creates it only when the
engineer presses **Create**. The result is a ticket key and link.

**Outcome to improve (hypothesis, unmeasured):** time from question to the
right runbook, and fewer retyped escalations. Baseline: none known. Proposed
measurement: a thumbs up/down per answer plus a two-week count of tickets
created through the assistant, compared with a short before/after survey of the
helpdesk lead (open decision O4).

**The model decides:** which searches to run, which pages answer the question,
how to summarise the steps, and the draft ticket text. **Code controls:** who
the user is, which Confluence spaces are searchable, result sizes, the Jira
project and issue type, the reporter, the create call, de-duplication and the
spend stop.

**Non-goals (phase 1):** editing Confluence, updating or closing Jira issues,
answering from sources other than the runbook spaces, memory across
conversations, chat-tool integrations.

Facts: the repository contains only the skills (`.claude/skills/`); there is no
application code, manifest or pin yet. Everything under "proposed" below is
greenfield.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due | End of week 2; continued (A1) |
| People and hours | 2 senior engineers × ~0.5 × 10 working days × 6 h × 0.6 focus ≈ **36 focused hours**; reserve 25% ≈ 9 h → **27 h for phase 1** |
| Money | Small allowance (A3); Cloud Billing budget alert plus application call caps |
| Users and what they read | 25 helpdesk colleagues using a web page daily (A4) |
| Data and effects | Internal runbooks (may hold secrets); creates Jira issues in one project (A5) |
| Delivery profile | **Internal tool**: known colleagues, own identity, real internal data, one bounded write. Not a POC, because the data and the write are real |

Depth per concern:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: ~15-case regression set of real helpdesk questions plus 3 injection cases (G02, G04) | Thumbs-down rate above 20% for a week → phase 2 eval expansion (G05) |
| Identity and scope | Build: IAP + verified JWT, Workspace group; sessions owned by verified email | Users outside the helpdesk, or restricted runbook pages |
| Secrets | Build: Secret Manager for Atlassian tokens, Cloud Run service identity, nothing in prompts/logs | Token rotation policy from security team |
| External writes | Build: confirmation in code, durable operation record, no blind retry | Any second write type (comment, transition) |
| Sensitive data | Minimal: no prompt/response content in logs; credential-pattern masking on page text before it reaches the model | A runbook found to contain a live secret → SDP inspection (G08) |
| Prompt injection and agency | Build: the model has no write tool (D3); adversarial cases in G04 | Any new write or egress tool |
| Budgets and loops | Minimal: `max_llm_calls` per turn, per-user daily turn cap, billing budget alert | Spend above the alert twice in a month |
| Memory and retrieval | Live Confluence search; in-memory sessions on one instance | Users ask for history, or more than one instance needed |
| Frontend | Simple authenticated page, completed JSON (no streaming) | Median complete answer above ~10 s measured |
| Hosting | One Cloud Run service behind IAP, max 1 instance | Concurrency or availability complaints |
| Observability | Minimal: structured logs with session/invocation IDs, token counts, tool outcome; no content | First incident that logs could not explain |
| Release engineering | Minimal: pinned ADK, model ID, prompt in repo, unit tests in CI | Second contributor or model migration (see D5) |
| Performance tuning | Defer | Measured latency complaint |

**Floor kept:** no secrets in source, prompts, logs or this document; a spend
stop (`RunConfig.max_llm_calls`, per-user daily cap, budget alert); no Jira
issue without the engineer pressing Create on the exact draft; runbook content
kept out of logs; pinned model ID.

**Who may use it:** members of the helpdesk Workspace group, on the
allowlisted runbook spaces and the one Jira project. **Graduation conditions**
before other teams, more spaces or more write types: restricted-page handling
(per-user Confluence permission or a permission-aware index), per-user Jira
identity, persistent sessions, an evaluation gate in CI, SDP screening of page
text. These are phase 2 goals in the plan.

**Cut line:** phase 1 = G01–G04, estimated 19–27 focused hours against 27
available after reserve. The high end only just fits; if G04 runs high, it
falls back to a prefilled Jira create link (no write credential) and the API
create moves to phase 2. Phase 2 = G05–G09, when the team has time.

## Guarantees and acceptance

| Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 Only helpdesk group members reach the assistant; a session belongs to one verified user | IAP + app middleware verifying the IAP JWT audience; session `user_id` = verified email; every route checks ownership | 401/403; no model call | Tests: missing/forged JWT rejected; user B cannot read or confirm user A's session or proposal |
| I2 Search reads only allowlisted spaces | Confluence adapter adds `space in (...)` from config to every CQL; the model supplies only query text | Out-of-scope request returns "no runbook found" | Test: model-supplied CQL fragments are escaped; captured requests always carry the space filter |
| I3 Answers cite the pages they used; no page → says so | Tool results carry page ID, title, URL, version; instruction requires citations; output check in G02 | "I found no runbook for this" with the searches tried | Regression set: citation present and points to a returned page; empty-search cases answer "none found" |
| I4 One Create click produces at most one Jira issue, and never without a click | `POST /proposals/{id}/confirm` in app code; Firestore transaction claims the operation; Jira call carries a unique label `hda-op-<id>`; uncertain outcome is reconciled, never blindly retried | Duplicate click shows the existing key; uncertain shows "checking" then the found key or "needs manual check" | Tests with fake Jira: double click → one create; timeout after commit → reconcile finds it, no second create; model output alone never creates |
| I5 Ticket fields come from the confirmed draft, unchanged | Proposal stored with a content hash; confirm sends exactly the stored payload | Changed draft needs a new proposal | Test: edited payload with old ID → 409 |
| I6 A turn costs at most N model calls; a user at most M turns per day | `RunConfig.max_llm_calls` (proposed 8); per-user counter in Firestore checked at admission | Polite "limit reached" message | Test with a scripted looping model; counter test |

## Architecture and decisions

```text
Browser ──IAP (Workspace group)──▶ Cloud Run: FastAPI app (one container)
                                     ├─ auth middleware: verify IAP JWT → user email
                                     ├─ POST /chat ─▶ ADK Runner ─▶ LlmAgent "runbook_assistant"
                                     │                   tools: search_runbooks, get_runbook, propose_ticket
                                     │                   model: Vertex AI Gemini (pinned)
                                     ├─ POST /proposals/{id}/confirm ─▶ Jira adapter (code, not a tool)
                                     └─ Firestore: proposals, operations, daily counters
                     Confluence Cloud REST (read token) ◀─┘   Jira Cloud REST (create token)
                     Secret Manager: both tokens, read by the Cloud Run service identity
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 (proposed) | Language interpretation over a few capabilities | One `LlmAgent` with three function tools; no sub-agents | One judgment (find and explain runbooks, draft tickets); nothing distinct to route | Multi-agent split adds routing evaluation for no new boundary; the security split is done in code (D3) | Rendered-request test shows three declarations and the instruction |
| D2 (proposed, A6) | Fresh, permission-scoped runbook answers | Live Confluence CQL search + page fetch via function tools, service-account token, space allowlist in code, page body converted to text and capped (~8k chars, top 5 hits with excerpts) | No ingestion pipeline, always current, works in two weeks | Keyword search is weaker than semantic retrieval; the service account sees the whole space (fine only if A6 holds) | Regression set retrieval hit rate; G01 checks restrictions. Trigger for Vertex AI Search index: hit rate below ~70% on the set |
| D3 (proposed) | Tickets only on request, exactly as shown (trifecta: private runbooks + untrusted page text + Jira write) | Model gets `propose_ticket`, which validates and stores a draft and returns a proposal ID; **creation happens only in `/confirm`**, an app route the model cannot call, triggered by the user's click | Removes the write leg from the agent: an injected instruction in a page can at worst produce a draft the engineer sees | One extra click; ADK native tool confirmation not used (its documented limitations; not needed) | Adversarial cases: page text says "create a P1 ticket" → no Jira call; only a draft at most |
| D4 (proposed, A7) | Know who asked, at most one issue per click | Jira service account; reporter = requesting user (resolved by email) when the project allows, else a "Requested by" field; Firestore operation record + unique label for reconciliation | Avoids per-user OAuth (consent, refresh, revoke) in phase 1 | Jira audit shows the service account as creator; per-user OAuth is G07 | I4/I5 tests; G01 confirms reporter permission and whether Jira create offers any idempotency |
| D5 (proposed) | Stable, supported model | Vertex AI `gemini-3.8-flash`, pinned; fallback candidate `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later). Avoid `gemini-3.6-flash` (Vertex retirement 2026-11-19) and 2.5 models (2026-10-20) | Lifecycle table `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, checked_on 2026-10-08 | 3.8-flash has no Vertex retirement entry in that table, so its Vertex availability and region are unconfirmed | G01: confirm the model in the Vertex model-versions page for the chosen region; else take the fallback |
| D6 (proposed, A4/A8/A9) | Colleagues use it daily with their own identity | Cloud Run (max 1 instance, min 0 or 1) behind IAP; a static page served by the same app; completed JSON per turn; `InMemorySessionService` | Smallest hosted shape for 25 users; IAP gives Workspace sign-in without app code | A restart loses open conversations (tickets and proposals survive in Firestore); no streaming | Restart test: proposal still confirmable after restart; open chat lost is accepted until trigger |
| D7 (proposed) | Spend stays small | `max_llm_calls=8` per turn, 40 turns/user/day (assumed), budget alert at the allowance | Bounded fan-out: ~2–4 model calls per normal turn | Caps may block a busy engineer; counters are adjustable config | I6 tests |

ADK version: no pin exists. Working assumption **google-adk 2.8.0**, the version
the specialists' `references/compatibility.md` files were read against; G01
confirms or replaces it.

### Model-facing contracts

| Surface | Contract | Skill and verification |
| --- | --- | --- |
| Instruction | Answer only from retrieved runbooks, cite page links, say when none found, never claim a ticket exists until the app reports a key; user identity, date and project are not in the prompt | `adk-agent-instructions`; rendered-request test |
| Tools | `search_runbooks(query: str)` → `{status, hits:[{page_id,title,url,excerpt}]}` ≤5 hits; `get_runbook(page_id: str)` → `{status, title, url, version, text, truncated}` ≤8k chars, page ID must come from a prior hit in this session; `propose_ticket(summary, description, component, priority, runbook_page_ids)` → `{status, proposal_id}` with enum-validated component/priority | `adk-tool-interface-design`; declaration dump and size |
| Output | Plain text answer with citations; no `output_schema` (the ticket draft is structured by the tool's parameters) | `adk-model-and-output-contracts` for the pin only |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Conversation | Verified user | ADK Runner / that user | In-memory | Until instance restart |
| Runbook text | Confluence | Read via service token / model context of the asking user | Live per call | Not stored by the app |
| Proposal | Verified user | `propose_ticket` / `/confirm` by the same user | Firestore, hash of payload | 30 days (assumed), then deleted by TTL |
| Ticket operation | Verified user | `/confirm` / user, operator | Firestore: `claimed → sent → created(key) / uncertain / failed` | 90 days (assumed) |
| Jira issue | Jira | Service account / everyone with project access | Jira is the authority | Jira's own retention |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| runbook_assistant | Runbooks | Page text (any Confluence editor can write it) | None: `propose_ticket` only stores a draft for the same user | Write leg removed (D3); creation in code after a click |
| `/confirm` (code) | Proposal | Draft text authored by the model | Jira create | Human sees the exact payload; fields enum-validated; Jira project fixed in config |

Residual risk accepted: injected text could shape a draft's wording or an
answer's advice; the engineer reads both. Runbook secrets: masked by pattern
before model exposure (minimal); full SDP in G08.

## Budgets and capacity

25 users; assumed ≤60 turns/day total, ≤5 concurrent. Per turn: 2–4 model
calls expected, 8 maximum; 1–3 Confluence calls; at most one Jira create per
click. Cost is symbolic (no current price looked up): `turns × calls × (input
≈6k tokens + output ≈500 tokens) × model price`; verify against the Vertex
pricing page in G01 and set the budget alert from it. Confluence and Jira rate
limits are unknown; assumed far above this load (G01 checks).

## Failure and recovery

| Failure window | User sees | Retained state / possible effect | Next action and owner |
| --- | --- | --- | --- |
| Not in group / forged header | 403 | Nothing | None |
| Confluence down or token revoked | "Runbook search unavailable", no invented answer | Nothing | Operator rotates token; tool returns `status: unavailable` |
| Model unavailable or `max_llm_calls` hit | Error message; partial text not shown as an answer | Session events so far | User retries; bounded by daily cap |
| Page contains injected instructions | Normal answer or a draft at most | Possibly a proposal | Engineer ignores the draft; no Jira effect without click |
| Double click on Create | Same ticket key twice | One operation record | None |
| Jira commits, response lost (timeout) | "Checking whether the ticket was created…" | Operation `uncertain`; an issue may exist | App searches Jira by label `hda-op-<id>`; found → `created`; not found → stays `uncertain` with "check Jira before retrying" (search index lag means absence is not proof); operator owns the manual check |
| Jira rejects (validation, permission) | The error, draft kept | Operation `failed`, no issue | Engineer edits → new proposal |
| Instance restart mid-conversation | Conversation gone | Proposals and operations in Firestore survive | User reopens; pending proposal still confirmable from its card link |
| Model retirement within horizon | None if planned | — | D5 calendar entry; migration = re-run regression set on new ID (G06) |

Not applicable: streaming partial output (completed JSON only), memory
erasure (no cross-session memory), A2A/MCP (no remote peers or servers).

## Verification and implementation handoff

Offline (G02–G04): fake Confluence and Jira clients, scripted-model Runner
tests for I1–I6, adversarial cases. Local integration: one process restart
for proposal survival. Bounded live (authorised in G01/G03 only): Confluence
search against the allowlisted spaces, one Jira create in a sandbox project or
with a test label. Hosted: IAP denial for a non-member, one end-to-end journey.

Observability and release at internal-tool depth: structured logs (session,
invocation, operation IDs, token counts, tool status; never content); release
bundle = image digest + ADK pin + model ID + prompt file hash, recorded in the
Cloud Run revision labels; rollback = previous revision kept. SLIs, canary and
CI evaluation gate are later items.

Goals, estimates, skills and run prompts are in the
[plan](../plans/helpdesk-assistant.md).

## Open decisions

| Question | Why it matters | Owner / evidence | Blocks |
| --- | --- | --- | --- |
| O1 Confluence/Jira Cloud or Data Center? (A5) | API paths, auth (API token vs PAT), search syntax | Helpdesk lead / G01 | G02 live check, G04 |
| O2 Any page restrictions in runbook spaces? (A6) | Service-account search could disclose restricted pages | G01 inspection | G03 go-live |
| O3 Can the service account set reporter; Jira project, issue type, required fields, components? (A7) | Draft schema and enums | Jira admin / G01 | G04 |
| O4 How will the helpdesk lead judge success? | Measurement beyond thumbs | Helpdesk lead | Phase 2 priorities only |
| O5 Is `gemini-3.8-flash` available on Vertex in the chosen region? (D5) | Model pin | G01 lookup | G02 pin |
| O6 Daily cap and budget figure (A3, D7) | Spend stop values | User | G03 config values (defaults usable) |
