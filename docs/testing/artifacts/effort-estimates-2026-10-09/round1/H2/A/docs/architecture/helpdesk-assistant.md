# System design: IT helpdesk runbook and ticket assistant

Status: **draft**. Every product answer below was assumed because the user was
not available. Decisions that depend on an assumption are marked
*provisional*. Nothing here has been implemented or provisioned.
Plan: [docs/plans/helpdesk-assistant.md](../plans/helpdesk-assistant.md).

## Assumed answers

These are the questions we would have asked. Each row gives the answer assumed
and the decisions that rest on it. Correct any row and the decisions it names
change.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When must the first useful version exist, and what happens after it? | End of week 2 (2026-10-23); development continues afterwards | Phase 1 cut line; code from phase 1 is kept |
| A2 | Who builds it and who runs it afterwards? | Given: two senior engineers who have shipped ADK agents on GCP, about half time for two weeks. Assumed: the same two run it afterwards | Capacity (36 focused hours); no new-to-ADK multiplier |
| A3 | What can be spent on models and cloud? | Assumed small allowance: about USD 300 a month, with a budget alert | D6, model tier, one Cloud Run instance |
| A4 | Who uses and judges it? | The 25 helpdesk staff use it daily. The helpdesk lead judges whether it helps | Internal-tool profile, D4, gold set in G02 |
| A5 | What data does it touch, and what can it change? | It reads runbooks from Confluence (internal, no personal data intended). It creates issues in one helpdesk Jira project. Conversations may contain names and emails of end users | Floor, D3, D5, logging policy |
| A6 | Confluence and Jira: Cloud or Data Center? | Atlassian Cloud | D2, D3, client code in G01 and G03 |
| A7 | Which Jira project, issue types and required fields? | One project, `ITHD`; issue types Incident and Service Request; summary, description and priority are required | D3, propose_ticket schema |
| A8 | Whose name appears on a created ticket? | An Atlassian service account creates the issue. The requesting technician's email goes in the description and in a label. Mapping the reporter to the technician waits for phase 2 | D3, G07 |
| A9 | Where do technicians work: web page, Google Chat, Slack, Jira sidebar? | A small web page behind IAP | D4, G04 |
| A10 | Can IAP check membership of a Google group that matches the helpdesk? | Yes, through a Google group such as `it-helpdesk@` | D4, I1 |
| A11 | Which spaces count as runbooks? Are any pages restricted? | One to three spaces that every helpdesk technician can read. Pages with their own restrictions are excluded | D2, I3 |
| A12 | What do the team's existing agents use for hosting, region, ADK pin and session store? | Cloud Run in the team's usual region, through their existing deployment template. ADK pin assumed to be 2.8.0 (the version the specialist skills were checked against) | D4, D7, G05 |
| A13 | Are there data-residency limits on model inference? | None beyond keeping Vertex AI in the region the team already uses | D6 |
| A14 | How will success be measured, and is there a baseline? | No baseline exists. Measures: gold-set citation accuracy, plus the pilot's time to find a runbook and to raise a ticket, compared with technicians' own estimates | Verification section |
| A15 | Can a created ticket notify someone outside IT, such as a Jira Service Management customer? | Assumed not: `ITHD` is an internal project. If it is a JSM project with customer notifications, confirmation matters even more and D3 stays as it is | D3 floor |

## Purpose and constraints

**Journey.** A caller tells a technician that their VPN client fails with error
809. Today the technician searches Confluence by keyword and opens several
pages. Then they open Jira and retype the caller's details into a new issue.
With the assistant, they ask "VPN error 809 on Windows, what do I do?" and get
the steps from the matching runbook with a link to it. Then they say "raise a
P3 incident for jane.doe@…". The assistant drafts the issue, the technician
checks the fields and clicks **Create**, and exactly one `ITHD` issue appears.
Its key comes back in the chat.

**Model and code split.** The model interprets the question, writes search
queries, summarises runbook steps and fills a ticket draft. Code controls
everything else: who the user is, which spaces may be read, the Jira project and
issue types, the confirmation step, at-most-once creation and the call budget.

**Non-goals for now:** editing or commenting on existing tickets, end-user
self-service, writing to Confluence, per-user Atlassian OAuth, voice and chat
channels.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due | End of week 2 (A1); continued |
| People and hours | 2 senior ADK/GCP engineers × half time × 10 days (A2) |
| Money | About USD 300 a month (A3, assumed) |
| Users and judge | 25 helpdesk technicians; helpdesk lead (A4) |
| Data and effects | Internal runbooks (read); creates Jira issues in one project (reversible: an issue can be closed) (A5) |
| Profile | **Internal tool.** Known colleagues use it daily with their own identity on real internal data. It writes to an internal tracker, not to outside people |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 20–25 case gold set (G02) | Phase 2: gold set becomes a CI gate (G09) |
| Identity and per-user scope | Build: IAP plus a verified user ID in middleware (G04) | Users outside the helpdesk group |
| Secrets | Build: Secret Manager, runtime service account (G05) | — |
| External writes | Build: draft, human confirmation, at-most-once record (G03) | Automatic reconciliation in G07 once a duplicate or uncertain create is seen |
| Sensitive data | Minimal: no conversation content in logs or traces; restricted pages excluded | Personal data in runbooks, or users outside IT: SDP or Model Armor |
| Prompt injection and agency | Build structurally: the model holds no write tool (D3) | Phase 2 adversarial cases (G10) |
| Budgets | Minimal: `max_llm_calls`, tool-result bounds, one instance, budget alert | Spend above 50% of the allowance, or more users |
| Memory and retrieval | Live Confluence search, no index; in-memory sessions | Gold hit-rate below target, so G08; restarts hurt users, so G06 |
| Frontend | Minimal page from the same service | Request for Google Chat or a Jira panel |
| Hosting | One Cloud Run service behind IAP | — |
| Observability | Minimal: structured logs with no content, token counts per turn | Phase 2 G11 |
| Release | Minimal: pinned versions and offline tests | Phase 2 G09 |
| Performance tuning | Defer | Users complain of latency in a measured sample |

**Floor kept:** no secrets in code, prompts or logs. A spend stop through
`RunConfig.max_llm_calls` (the app owns the Runner) plus a project budget alert.
No Jira issue without a human clicking Create on the exact stored draft. Only
allowlisted runbook spaces are read. The model ID is pinned.

**Who may use it:** members of the helpdesk Google group, on internal runbooks
and the `ITHD` project only. **Graduation conditions** before other departments
or end users get access: per-user authorisation for Jira and Confluence, an
adversarial prompt-injection suite, screening for sensitive data, and durable
sessions. These are phase 2 goals and later-list items in the plan.

**Capacity and cut line.** Raw capacity is 2 × 0.5 × 10 days × 6 h × 0.6 focus,
about **36 focused hours**. Keeping a reserve of about 22% leaves 28 hours.
Phase 1 is G01–G05 at **18–28 hours**, so even its high end fits. Phase 2
(G06–G11) waits until the team has time. Details and the person-load table are
in the plan.

## Guarantees and acceptance

| Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 Only helpdesk group members reach the app | IAP on Cloud Run with group-based access; the app also verifies the IAP JWT | 403 before the app | G05 live check: a non-member gets 403 |
| I2 Users see, continue and confirm only their own sessions and drafts | Middleware derives `user_id` from the verified IAP JWT; the session service and draft store are keyed by it; client-supplied IDs only locate a resource | 404 for another user's session or draft | G04 offline cross-user tests |
| I3 Only allowlisted runbook spaces are read | CQL `space in (...)` is built in code; `read_runbook` checks the page's space before returning it; the service account can read only those spaces | Tool returns `status: not_allowed`; no text reaches the model | G01 offline test with a page ID from another space |
| I4 No issue without the owner's confirmation of the exact stored draft; at most one issue per draft | The model has no create tool. The confirm endpoint runs a Firestore transaction that moves the draft from `pending` to `dispatching` once, then calls Jira with the stored payload | A second confirm returns the existing status; a timeout becomes `uncertain`, with no automatic retry | G03 offline tests: double confirm, timeout, Jira 400 |
| I5 Answers cite runbook pages returned in this turn; when nothing is found, the assistant says so | Instruction and tool contract (a probabilistic control, not a guarantee) | An uncited answer is counted as a gold-set failure | G02: citation ⊆ URLs returned by tools, ≥ 80% expected-page hit (provisional target) |
| I6 Spend per turn and per month is bounded | `max_llm_calls=8`; tool results truncated; Cloud Run max instances 1; budget alert | Turn ends with a "too many steps" message | G01 unit test that the cap is set; G05 budget readback |
| I7 No secrets or conversation content in logs | Secret Manager; ADK content capture disabled; log only IDs, statuses and token counts | — | G05 log sample review |

## Architecture and decisions

```
Browser (technician) ──IAP (group check)──▶ Cloud Run: helpdesk-assistant (FastAPI, max 1 instance)
                                              ├─ IAP JWT middleware → user_id
                                              ├─ /api/chat → ADK Runner (InMemorySessionService)
                                              │     └─ LlmAgent (gemini-3.8-flash on Vertex AI)
                                              │          ├─ search_runbooks ─▶ Confluence Cloud REST (read token)
                                              │          ├─ read_runbook   ─▶ Confluence Cloud REST
                                              │          └─ propose_ticket ─▶ Firestore drafts (no Jira call)
                                              └─ /api/drafts/{id}/confirm (app code, not the model)
                                                    └─ transaction on draft ─▶ Jira Cloud REST create issue
Secrets: Secret Manager (Atlassian tokens) → runtime service account
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret questions and fill drafts (A4) | One `LlmAgent` with three function tools; no sub-agents | One responsibility and a small tool set; sub-agents would add routing without a separate authority | A routing layer would be needed later for many more tools | Tool declarations dumped in a test: 3 tools |
| D2 | Find the right runbook, fresh (A6, A11) *provisional* | Live Confluence CQL search over allowlisted spaces, then fetch the page body as text truncated to 8,000 characters | No ingestion pipeline and always current; fits two weeks | Keyword search can miss paraphrased questions, unlike a semantic index (Vertex AI Search) | G02 hit rate; below 80% triggers G08 |
| D3 | Tickets on request, never by accident (A5, A7, A8, A15) *provisional* | `propose_ticket` only writes a draft to Firestore. The browser shows the draft, and app code creates the issue when the owner confirms. Project and issue types come from a code allowlist. A label `hda-<draft_id>` is added for reconciliation | Removes the write leg from the agent: an injected runbook can at most produce a draft a human reads. Confirmation is bound to the stored payload | One extra click. The model does not learn the key unless the app writes it to session state. Native ADK tool confirmation was the alternative; it keeps the write inside the model loop | G03 tests; adversarial case in G10 |
| D4 | Colleagues use it with their own identity (A9, A10, A12) *provisional* | Cloud Run behind IAP restricted to the helpdesk group. FastAPI wraps the Runner and takes `user_id` from the verified JWT. A minimal HTML page, without streaming | Reuses existing SSO and the team's hosting pattern. Avoids `adk web`, which takes `user_id` from the client | A custom page to maintain. Google Chat would meet technicians where they work | G04 cross-user tests; G05 non-member 403 |
| D5 | Atlassian credentials (A6, A8) *provisional* | Two Atlassian service-account API tokens in Secret Manager: Confluence read-only on the runbook spaces, and Jira create on `ITHD`. Tokens are selected in code and never appear in model arguments | Least privilege without per-user OAuth (which costs 8–16 hours plus provider setup) | The Jira audit trail shows the bot as creator; Jira does not enforce per-user permissions | G05 readback of service-account grants |
| D6 | Bounded quality and cost (A3, A13) | Pin `gemini-3.8-flash` on Vertex AI: stable, released 2026-09-02, no announced retirement as of 2026-10-08 (lifecycle table `model-lifecycle-2026-10-01.json`). `max_llm_calls=8` | Newest stable Flash with no retirement inside the plan's horizon. `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28) would force a migration | Unmeasured against the 3.5 Flash default; Pro tier unused | G02 run records the model ID; check the lifecycle table before each release |
| D7 | Survive a restart for in-flight tickets, not for chat (A12) | `InMemorySessionService` on one instance; drafts and operations live in Firestore | Conversations last minutes; durable sessions add a store for little value now | A deploy or restart loses chat history; the user starts again, and drafts still work | G04 test: confirm still works after the runner is rebuilt |

**Versions.** ADK `google-adk==2.8.0` is a working assumption (A12): it is the
version recorded in the specialists' `references/compatibility.md`. G01's first
acceptance item confirms it against the team's pin. The Confluence endpoints
(`/wiki/rest/api/search` with CQL, `/wiki/api/v2/pages/{id}`) and Jira's
`POST /rest/api/3/issue` are written from memory. They were **not checked** in
this session (no network) and are verified in G01 and G03.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Answer only from runbook text returned by tools in this turn, and cite each page URL used. When search returns nothing, say so and suggest escalation; never widen the search. Propose a ticket only when the user asks for one, and say it is a draft awaiting their Create click. The user's identity and allowlists are not in the prompt | `adk-agent-instructions`; rendered-request snapshot test |
| Tools | `search_runbooks(query)` returns up to 5 `{page_id, title, url, excerpt, last_modified}`. `read_runbook(page_id)` returns `{title, url, version, text, truncated}`. `propose_ticket(issue_type, summary, description, priority, affected_user, runbook_urls)` returns `{draft_id, preview}`. Every tool returns `status` plus an actionable `error`. All three are read-tier: no tool writes outside the app's own draft store | `adk-tool-interface-design`; declaration dump and size test |
| Output | Free text with links; no `output_schema` (it would conflict with tool use) | `adk-model-and-output-contracts`; model ID pinned in config |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Runbook pages | Confluence; allowlisted spaces | Confluence editors / the assistant reads them | Live on every call | Not stored. Only appears in the in-memory session |
| Conversation | Verified user | Runner / the owner | In memory | Lost on restart; never logged |
| Ticket draft and operation | Verified user (`owner`) | `propose_ticket`, confirm endpoint / the owner | Firestore | Drafts expire after 30 minutes. Records deleted after 90 days (TTL policy) |
| Jira issue | Jira `ITHD` | Confirm endpoint (bot) / helpdesk | Jira is authoritative | Jira's own retention |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| helpdesk assistant | Internal runbooks | Runbook text (editable by many), user-pasted error text | None from the model. Drafts are internal; the Jira create runs in app code after a human click | Write leg removed (D3). **Accepted risk** (owner: helpdesk lead, ends when G10 lands): an injected runbook could mislead the technician's answer, mitigated by cited links |

## Budgets and capacity

Illustrative assumptions, not a bill: 25 users × 20 questions a day × 4 model
calls × about 10k input tokens is about 20M input tokens a day. Vertex Flash
pricing was **not checked** in this session; G05 records the current price and
date before the budget alert is set. A turn holds at most 8 model calls and 5
search results, and each page is truncated at 8,000 characters. One Cloud Run
instance comfortably carries 25 users (expected concurrency below 5). Latency
target, provisional: a complete answer within 15 seconds, measured in the pilot.

## Failure and recovery

| Failure window | User sees | Retained state / effects | Next action and owner |
| --- | --- | --- | --- |
| Success | Answer with links; draft card; issue key after Create | Draft `created` with key | — |
| Another user's session or draft ID | 404 | None | — |
| Confluence down or token rejected | "Couldn't search runbooks" plus the error class | None | User retries; engineers rotate the token |
| No matching runbook | "No runbook found", with a suggestion to escalate | None | Gap noted for the runbook owners |
| Model error or call cap reached | "Couldn't complete, try rephrasing" | No draft, or an unconfirmed draft that expires | User |
| Double click or two tabs | Second click shows the current status | One issue | — |
| Jira returns 4xx | Draft `failed` with Jira's message | No issue | User edits the request; a new draft is created |
| Jira timeout or 5xx after dispatch | "Uncertain: search Jira for label `hda-<id>` before retrying" | Draft `uncertain`; an issue may exist | User checks Jira. A manual retry is offered only on the same draft (G07 automates this) |
| Restart or deploy | Chat history gone | Drafts and keys remain in Firestore | User starts a new chat |
| Injected instructions in a runbook | At worst a misleading answer or draft | No effect without a click | G10 suite |
| Model retirement | — | Pinned ID | Check the lifecycle table at each release |

Rollback: redeploy the previous Cloud Run revision. Firestore drafts are
compatible because the schema is versioned by a `v` field. Cleanup: delete the
service, the Firestore collection, the secrets and the two Atlassian accounts.

## Verification and implementation handoff

- Offline (G01–G04): fake Confluence, Jira and draft store; Runner tests with a
  scripted model for tool calls; cross-user and double-confirm tests.
- Bounded live (G01, G02, G03): read-only Confluence calls; the gold-set run
  against Vertex (about 25 × 4 calls); Jira creates only in a sandbox project or
  with a `test` label, and those issues are closed afterwards.
- Hosted (G05): IAP denial, readback of the revision, a log sample, then a pilot
  with 3–5 technicians.
- Benefit is a **hypothesis**: shorter time to runbook and to ticket. Measure it
  through pilot technicians' timed tasks against their current estimate.
- Observability and release at this profile: structured logs (`session_id`,
  `invocation_id`, `draft_id`, tool status, token counts), no content capture,
  the pinned model and prompt version recorded in config. Rollback means the
  previous revision.

Goals, estimates, the cut line and the run prompts are in the
[plan](../plans/helpdesk-assistant.md).

## Open decisions

| Question | Why it matters | Who settles it | Blocks |
| --- | --- | --- | --- |
| A6–A8: Atlassian edition, project and fields | Client code and draft schema | Helpdesk lead / Atlassian admin | G01 and G03 live steps (offline work can proceed) |
| A9: web page or Google Chat | Frontend goal changes shape | Helpdesk lead | G04 |
| A12: existing ADK pin, region and deploy template | Pins and G05 effort | Engineers | G05 |
| Is Jira search fresh enough to find `hda-<id>` immediately after a create? | Whether automatic reconciliation (G07) is safe | Discovery inside G07 | G07 |
| D2 quality | Live search could be too weak | G02 result | G08 |
