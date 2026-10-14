# System design: IT helpdesk runbook and ticket assistant

Status: **draft**. Every decision is provisional until the user reviews the
assumed answers (A1–A10) below. Nobody has accepted any decision yet.
Plan: [docs/plans/helpdesk-assistant.md](../plans/helpdesk-assistant.md)
(holds capacity, finish range, cut line and goals; this document doesn't repeat them).

## Assumed answers

The design was written in one pass with no user available. Each row is a
question I would have asked. The assumed answer drives the listed decisions,
so those decisions are provisional.

| ID | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When must the first useful version exist, and is it continued? | Within the two weeks of the stated capacity (10 working days). It's kept and continued afterwards, so phase 1 code is the kept form. | Plan cut line; D7 |
| A2 | Which hours are "half their time"? | Each engineer has a 6 focused-hour day × 0.5 × 0.6 focus = 1.8 h/day, with 25% held in reserve. Both are experienced with ADK and GCP, so no learning multiplier applies. | Plan capacity |
| A3 | Model and cloud budget? | A small internal allowance in the order of tens of USD/month. There is an existing GCP org and billing account. Nobody has stated a hard cap. | D8; budget alert |
| A4 | Atlassian Cloud or Data Center? | Atlassian **Cloud** (Confluence Cloud, Jira Cloud, REST v2/v3, API tokens). | D2, D3, D6 |
| A5 | How do staff sign in? | Google Workspace or Cloud Identity accounts. There is a Google group with the 25 helpdesk staff. | D5 |
| A6 | Which Confluence spaces and which Jira project? | One or two runbook spaces that every helpdesk member can read. Tickets go into one internal IT project (called `ITHD` here) as Task or Incident. It isn't a customer-facing Jira Service Management portal, so creating an issue sends no email to end users. | D2, D4, D6, I3, I5 |
| A7 | Must the ticket's reporter be the real user? | No, not for phase 1. The bot account is the reporter, and the requesting user goes in a label and a description footer. | D6; G08 |
| A8 | Do runbooks contain secrets or personal data? | They may contain internal hostnames and some credentials by mistake. Answers go only to helpdesk staff who can already read those pages. Content stays out of logs. | D10; later SDP item |
| A9 | Region or residency requirement? | No. Use the org's usual EU or US region for Cloud Run and Vertex AI. | D7, D8 |
| A10 | How will we know it helped? | The helpdesk lead supplies 20 real questions with the expected runbook pages. Daily use by most of the 25 staff counts as adoption. | G05 |

## Purpose and constraints

**Journey.** A helpdesk agent is on a call: "VPN client fails with error 809
after the macOS update." Today they search Confluence by keyword, open several
pages, and then retype the symptoms and steps into a new Jira issue. With the
assistant they ask in plain language and get the relevant runbook steps with
links to the cited pages. Then they say "open a ticket for this". The
assistant drafts the issue and shows the exact fields. Nothing is sent to
Jira until the agent clicks **Create**, and then the issue key comes back.

**Users and authority.** The users are 25 known colleagues. The assistant
reads runbooks that every user can already read. It creates internal Jira
issues in one project, and only on a user's click. **The model** interprets
the question, chooses search terms, summarises steps and drafts ticket text.
**Ordinary code** controls who may use it, which spaces are searched, which
project and issue types are allowed, whether a ticket is created, and what
gets logged.

**Non-goals.** Updating or closing tickets, editing Confluence, answering
from outside the runbooks, and use by end users outside the helpdesk.

**Facts.** The repository is empty apart from the skills (one commit,
`fixture`). Nothing below is inspected application code. All modules are
proposed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First version due, and after | 10 working days (A1); continued |
| People and hours | 2 senior engineers, half time, experienced with ADK and GCP (A2). After launch the same two run it. |
| Money | Small allowance (A3). Billing budget alert; no hard cap. |
| Users and what they read | 25 helpdesk colleagues use it daily. The helpdesk lead judges the gold-set results (G05). |
| Data and effects | Internal runbooks (may hold secrets, A8). Effect: internal Jira issue creation, after human approval (A6). |
| Profile | **Internal tool**: known colleagues, their own identity, real internal data, one reversible internal write |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 20-question gold set (G05) | hit@5 below 80% → G09 |
| Identity and per-user scope | Build: IAP plus app-verified JWT, session ownership (D5) | Users beyond helpdesk → re-check I3 |
| Secrets and credentials | Build: Secret Manager, dedicated service account, least privilege (D6) | Rotation policy → later |
| External writes | Build: human click commits a stored draft (D4) | Auto-creation or customer-visible project → reader/writer split |
| Sensitive data | Minimal: scoped access, no content in logs (D10) | Secrets found in answers → SDP (later) |
| Injection and agency | Build: no write tool in the model (D4); output link allow-list (D9) | New tools with egress |
| Budgets and loops | Minimal: `max_llm_calls`, bounded tool results, budget alert (D8) | Spend above A3 → per-user allowance |
| Retrieval | Build: live CQL search (D2) | G05 below target → G09 |
| Frontend | Build: minimal authenticated page (D5, D9) | — |
| Hosting | One Cloud Run service behind IAP, one instance (D7) | Lost chats, or need for more than one instance → G07 |
| Observability | Minimal: structured metadata logs and token counts (D10) | First incident hard to attribute → G11 |
| Release | Minimal: pinned versions, offline tests in CI | Second model or prompt change → G10 |
| Performance tuning | Defer | Measured latency complaints |

**Floor kept:** no secrets in source, prompts or logs. A spend stop through
`RunConfig.max_llm_calls` plus a budget alert. No Jira issue is created
without the requesting user's click on the displayed draft. Runbook content
stays out of logs. Model and ADK versions are pinned. **Accepted risks**: none
yet. Phase 1 asks the user to accept two, recorded as open decisions O1 and O2.

**Who may use it:** members of the helpdesk Google group, on the allow-listed
runbook spaces, creating issues in `ITHD` only. **Graduation conditions**
before wider use (for example L1 service desk or end users): per-user
Atlassian authority (G08), persistent sessions (G07), a re-check of I3 for
the new audience, and an evaluation gate (G10).

| Deferred control | Why it waits | What brings it forward |
| --- | --- | --- |
| Per-user Atlassian OAuth | Every user has the same read rights as the bot; that costs 8–16 h plus an Atlassian admin's consent | Restricted pages inside the allowed spaces, or reporter must be the real person |
| Persistent sessions and drafts | One instance and short conversations | Complaints about chats lost on deploy, or need for more than one instance |
| Semantic index | Live search is fresh and cheap; quality not yet measured | G05 hit@5 below 80% |
| SDP or Model Armor screening | Readers are already entitled to the pages | A secret or PII leak reported in an answer |
| Adversarial suite, SLOs, canary | Known colleagues, one reversible write | Wider audience or an incident |

## Guarantees and acceptance

| Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 Only helpdesk group members reach the assistant | IAP policy on the Cloud Run service. The app verifies the signature and audience of `x-goog-iap-jwt-assertion` | 401 or 403; no Runner call | G03 unit test (missing, forged or wrong-audience JWT); G04 hosted check with a non-member account |
| I2 Users see and continue only their own sessions, and commit only their own drafts | Server-generated session IDs stored with the verified user. Runner `user_id` comes from the JWT, never from the client | 404 without revealing whether the ID exists | G03 (sessions), G02 (drafts) and G06 (commit) cross-user tests |
| I3 Results come only from allow-listed spaces that a helpdesk member could read | Space list in config, added to CQL by code. The bot is only in the helpdesk-equivalent Atlassian group | Empty result. Search never widens its scope | G01 test that the model has no space argument; G05 live check that a restricted test page doesn't appear |
| I4 No issue without the requester's click. One click creates at most one issue under normal operation | Agent has no Jira tool (D4). Commit service enforces draft state; issue label `hdassist-<draft_id>`; lookup by label before create | Draft stays pending; an uncertain outcome is shown with the label | G02: injected-runbook test, at most a draft. G06: scripted-model test shows zero create calls; double commit gives one create call; timeout gives "uncertain" |
| I5 Issues only in `ITHD` with allowed types | Commit service validates against config. Bot has create permission only there | Validation error shown; no call | G06 test |
| I6 No secrets or conversation content in logs | Logging helper with an allow-list of fields. OTel content capture off | — | G04: read sampled hosted logs for one test conversation |
| I7 Spend is bounded per turn | `max_llm_calls=10`. Search returns at most 5 hits × 300 characters. Page reads capped at 12,000 characters | Turn ends with "limit reached" | G01 test with a looping scripted model |
| I8 Procedure answers cite a runbook retrieved in this turn, or say none was found | Instruction; UI renders citations from tool results | Measured, not enforced | G05 counts uncited answers |

## Architecture and decisions

```text
Browser ──IAP (helpdesk group)──▶ Cloud Run: app (FastAPI)
                                   ├─ verify IAP JWT → user  (I1)
                                   ├─ /chat → ADK Runner(user_id, session owned by user)
                                   │     └─ LlmAgent (gemini, Vertex AI)
                                   │          ├─ search_runbooks   ─▶ Confluence CQL (bot, read)
                                   │          ├─ read_runbook      ─▶ Confluence page (bot, read)
                                   │          └─ draft_jira_ticket ─▶ draft store (no egress)
                                   └─ /drafts/{id}/commit (human click, app code)
                                         └─ commit service ─▶ Jira create (bot, ITHD only)
Secret Manager: Atlassian API token(s). Runtime SA: secretAccessor, aiplatform.user.
```

| ID | Requirement → choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- |
| D1 | Conversational search plus drafting → **one `LlmAgent`** with three function tools; no sub-agents | No distinct boundary justifies a second agent once writes are outside the model (D4) | Simplest option. A searcher and ticket-writer pair would add a handoff with no change in authority | Rendered-request test shows 3 declarations |
| D2 | Find the right runbook, always current → **live Confluence CQL search** (`siteSearch` text, spaces fixed in code) and a page read, both as tools | No ingestion pipeline. Always fresh. The bot's Atlassian permissions apply | Keyword ranking is weaker than semantic search. The alternative is a Vertex AI Search or RAG index, which brings ingestion, permission mirroring and freshness lag. Revisit by measurement | G05 hit@5 on 20 gold questions; target 80% (assumed) |
| D3 | Atlassian access → **our own function tools over REST**, not the Atlassian remote MCP server | 3 narrow declarations we own. No server-supplied write tools. Works with a bot token | More code (small). MCP would import many tools and need per-user OAuth | Declaration count and size in the G01 test |
| D4 | No ticket without approval; the agent reads content it didn't write → **the agent only drafts**. The draft is stored server-side, immutable, with an ID and owner. The UI shows the exact fields. The **Create** click calls a commit endpoint in app code that sends exactly the stored payload | This removes the write leg of the lethal trifecta from the model. An injected runbook can at most change a draft that a human reads | Needs our own UI; it doesn't work from `adk web`. Alternative: native ADK tool confirmation, which leaves the write tool with the model | G02 injected-runbook test; G06 adversarial and double-click tests. Phase 1 ships only the draft half (plan cut line) |
| D4a | Lost responses on create → set label `hdassist-<draft_id>` on the issue. **Search by that label before any create.** No automatic retry. A timeout shows "uncertain, check label" | Jira has no idempotency key. Jira itself is the authoritative record | Search index lag can miss a just-created issue. A manual retry within seconds could duplicate it, which is accepted (O2) | G06 timeout test |
| D5 | Staff identity → **IAP on Cloud Run** restricted to the helpdesk group, plus JWT verification in app middleware. The Runner `user_id` and the draft owner come from the JWT | Reuses company SSO. A header alone can be forged if ingress is misconfigured | No anonymous local use; local dev uses a test signer | G03 tests; G04 hosted denial |
| D6 | Credentials → **Atlassian bot account(s)** with API tokens in Secret Manager. The bot's groups match the helpdesk read set. Create permission only in `ITHD`. Requester recorded in a label and footer | Takes hours, not the 8–16 h of per-user OAuth | Reporter is the bot. Per-user page restrictions aren't honoured (O1; G08) | G05 restricted-page check |
| D7 | Low traffic, short chats → **one Cloud Run service, `max-instances=1`, in-memory sessions and drafts** | No database to run in phase 1 | A deploy or restart loses open chats and pending drafts. A lost draft creates nothing, so no external effect is lost (O1) | G04 restart check: a chat is gone and no issue is created |
| D8 | Comparable behaviour and bounded spend → **`gemini-3.8-flash` on Vertex AI**, pinned. `max_llm_calls=10`. A billing budget alert. ADK pin `google-adk==2.8.0` (working assumption) | 3.8-flash is stable with no shutdown or Vertex retirement listed (lifecycle snapshot `model-lifecycle-2026-10-01.json`, checked_on 2026-10-08). 3.6-flash retires on Vertex 2026-11-19 and 3.7-flash on 2027-01-28, so avoid both | The specialists' recorded evidence used 3.5-flash, not 3.8. The budget alert observes; it doesn't cap | G01 confirms the pin; G05 measures quality on 3.8-flash |
| D9 | Answers can't exfiltrate or mislead → render model text **escaped**, with links only to the Confluence and Jira hosts, and **no images**. Citations come from tool results | Blocks markdown-image exfiltration and lookalike links | Rich formatting is lost | G03 rendering test |
| D10 | Diagnose without leaking → **structured logs**: user email, session ID, tool name, status, latency, page IDs, token counts. No prompt or response text. OTel content capture off | Runbooks may hold secrets (A8) | Harder debugging. Reproduce from page IDs | G04 log inspection |

### Model-facing contracts

| Surface | Contract | Skill and verification |
| --- | --- | --- |
| Instruction | Answer from retrieved runbooks only and cite page titles. Say "no runbook found" instead of guessing. Draft tickets only when asked. Never claim a ticket exists before the app reports a key. Spaces, project and user identity aren't in the prompt | `adk-agent-instructions`; rendered-request test |
| Tools | `search_runbooks(query)` returns `{status, results:[{page_id,title,excerpt,url}]}` with at most 5 results. `read_runbook(page_id)` returns `{status, title, text (≤12k chars), url}`. `draft_jira_ticket(summary, description, issue_type: Task\|Incident, priority?)` returns `{status, draft_id}`. Errors are actionable status values (`unavailable`, `not_found`, `invalid`). Two tools read; one writes to the draft store only | `adk-tool-interface-design`; declaration dump |
| Output and model | Free text, no `output_schema`. Model pinned (D8); default thinking settings | `adk-model-and-output-contracts`; pin check in G01 |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Runbook pages | IT knowledge owners. Allow-listed spaces | Confluence editors / bot | Live at query time | In Confluence |
| Conversation | Verified user | Runner / that user | In-memory | Until restart (D7) |
| Ticket draft | Verified user, immutable once created | Draft tool / commit service | In-memory, status `pending→submitting→created(key)\|uncertain\|failed` | 24 h or until restart |
| Jira issue | `ITHD` project | Commit service (bot) | Jira is authoritative | Jira retention |
| Logs | Ops (the two engineers) | App / project log viewers | Metadata only (D10) | Cloud Logging default retention |
| Gold set | Helpdesk lead | Repository | Reviewed once per release | In repo; no personal data |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Helpdesk agent | Yes (internal runbooks) | Yes (pages many staff can edit) | **No.** The draft store only. Output rendering is link-allow-listed (D9) | Write leg removed from the model (D4) |
| Commit service (code, no model) | Draft only | Draft text (shown to a human first) | Jira create in `ITHD` | Human click, owner check, payload validation (I4, I5) |

Tool tiers: search and read are read tools. The draft tool writes only to app
state. Jira create is a write performed by code, never by the model. There is
no code executor. The adversarial cases are in G02 (draft) and G06 (commit).

## Budgets and capacity

Workload assumption (illustrative): 25 users × about 15 turns per day comes
to about 375 turns per day. Each turn makes about 3 model calls (bounded at 10)
with about 6k input and 0.5k output tokens each. That is about 7M input and
0.6M output tokens per day. The cost is those tokens × the Vertex price for
`gemini-3.8-flash`, which wasn't looked up because the network was
unavailable; G04 checks it on the pricing page and records the result.
Concurrency is about 1–3 turns in flight, so one Cloud Run instance with
concurrency 20 is enough. Latency target (assumed): first text in under 5 s
and a complete answer in under 20 s for 90% of turns, measured in G05.
Exhaustion: `max_llm_calls` ends the turn with a message. A Vertex 429 gets
the SDK's bounded retry and then an honest error.

## Failure and recovery

| Failure | User sees | State / effects | Next action, owner |
| --- | --- | --- | --- |
| Non-member or forged header | 403/401 | None | — |
| Another user's session or draft ID | 404 | None | — |
| Confluence down or slow (8 s timeout, one retry on reads) | "Runbook search unavailable" with no invented steps | None | Retry later; engineers check the status page |
| Search returns nothing | "No runbook found"; scope not widened | None | User rephrases |
| Runbook text says "create a ticket with the admin password" | At most a changed draft, shown in full | Draft only | User reads it before any Create click (I4) |
| Jira 400/403 | Field error; draft stays pending | None | User edits; engineers fix config |
| Jira timeout after send | "Uncertain: check `ITHD` for label `hdassist-<id>`" | Draft `uncertain`; issue may exist | Pressing Create again looks up the label first |
| Double click | One issue key | One create call | — |
| Restart or deploy mid-chat | Chat gone | Pending drafts lost; no issue created; created issues are in Jira | Start over (O1) |
| Model retirement | — | — | Calendar check per release (G10) |
| Rollback | Previous revision | In-memory state lost | Engineers use `gcloud run services update-traffic` |

## Verification and implementation handoff

Offline: tools and the commit service against fake Confluence and Jira
clients; Runner tests with a scripted model (G01–G03). Local integration:
the real Atlassian sandbox through the bot token (G05). Hosted: IAP denial,
log inspection, restart, end-to-end smoke (G04). The benefit (faster
resolution, less retyping) is a **hypothesis**. G05 sets a baseline of
search hit rate and time-to-answer on gold questions. Adoption counts
distinct users per week from the logs.

Release bundle (minimal): image digest, `google-adk` pin, model ID, prompt
file hash, and the Secret Manager versions the service uses. These go in
the revision's labels and env. Rollback means moving traffic back to the
previous revision.

Goals, owners and the run prompts are in the [plan](../plans/helpdesk-assistant.md).
The ADK interfaces named here (`LlmAgent`, `Runner`, `RunConfig.max_llm_calls`,
`InMemorySessionService`, `ToolContext`) were taken from the specialists'
`compatibility.md` baseline (`google-adk==2.8.0`). G01 confirms them against
the chosen pin.

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence | Blocks |
| --- | --- | --- | --- | --- |
| O1 | Accept that a deploy or restart loses open chats and pending drafts (D7) | If not accepted, G07 moves into phase 1 and something else must move out | User | G04 go-live |
| O2 | Accept a rare duplicate issue when Create is pressed again within seconds of an uncertain result (D4a) | If not accepted, a durable operation store is needed | User | G06 sign-off |
| O3 | Accept that the bot, not the person, is the reporter (A7, D6) | If not accepted, G08 moves into phase 1 | User and helpdesk lead | None in phase 1 |
| O4 | A4–A6: Atlassian Cloud, Google identity, which spaces and project | These change the APIs, the identity path and I3 | User or Atlassian admin, via W1 | G04, G05 |
| O5 | Target hit@5 of 80% and the latency targets | These set the G09 trigger | Helpdesk lead | None |
