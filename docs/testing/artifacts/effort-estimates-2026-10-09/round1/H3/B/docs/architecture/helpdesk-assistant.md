# System design: IT helpdesk runbook and ticket assistant

Status: **draft**. Written in one pass without the user; every row of the
assumed-answers table is provisional until the user confirms it. Plan:
[docs/plans/helpdesk-assistant.md](../plans/helpdesk-assistant.md).

## Assumed answers (user not available)

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Deadline, and what happens after it? | First useful version at the end of the two weeks; code is kept and continued | Phase 1 scope; kept (not throwaway) code form |
| A2 | Spend for models and cloud? | Small allowance: about USD 100 per month, with a billing alert at 50% and 100% | D5 budget alert, model tier (D6) |
| A3 | Which Atlassian edition? | Atlassian **Cloud** (`*.atlassian.net`), REST v2/v3 APIs | D2, D4; tool adapters |
| A4 | Which Confluence spaces, who may read them? | One or two IT runbook spaces that all 25 helpdesk staff can already read; no page-level restrictions inside them | D2 shared read-only credential; per-user Confluence auth deferred |
| A5 | Do runbooks contain secrets or personal data? | They should not; any found are a content clean-up, not a design feature. Pages labelled `restricted` are excluded | D2 exclusion filter, log policy |
| A6 | How do staff sign in? | Google Workspace accounts; a Google group `helpdesk@` lists the 25 staff | D5 IAP and identity |
| A7 | Where should Jira tickets go, and who should be reporter? | One Jira project (for example `HELP`), reporter is the staff member who asked | D4 human-submitted draft in phase 1 |
| A8 | Is it acceptable that phase 1 *drafts* tickets the user submits, with direct API creation in phase 2? | Yes (it fits capacity and keeps the human-approval floor) | Cut line; G04 vs G05 |
| A9 | Data residency? | No residency requirement beyond the company's normal GCP use; region `europe-west1` for hosting, Vertex model at `global` | D5, D6 |
| A10 | Is the ADK dev UI acceptable as the phase 1 front end for the helpdesk team? | Yes, for the 25-person team only, with the accepted risk in "Floor" below | D5; G06 replaces it |
| A11 | Who runs it after the two weeks? | The same two engineers, a few hours a month | Minimal observability, single instance |

## Purpose and journey

**Journey.** A helpdesk agent on a call hears "VPN client says certificate
expired". Today they search Confluence by keyword, open three pages, read the
right section and, if it needs escalation, retype the details into a Jira form.
With the assistant they ask in plain language, get the runbook steps with links
to the exact pages, and say "raise a ticket for network ops"; the assistant
prepares a ticket draft from the conversation and the agent submits it in Jira
under their own name.

**Outcome to improve (hypothesis, unmeasured).** Time from question to the
right runbook section, and ticket completeness. Baseline: none exists; G02's
regression set gives retrieval quality, and a one-week before/after sample of
"time to answer" from five volunteers is a phase 2 measurement (G08).

**What the model decides:** search terms, which passages answer the question,
the wording of the answer and of the ticket summary/description.
**What code controls:** which spaces are searched, result size, the Jira base
URL, project and issue type, the user identity, call limits and logging.

Non-goals: answering from outside the allowlisted spaces, changing Confluence,
closing or editing tickets, end-user (non-helpdesk) access.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due | End of two weeks (A1); continued afterwards |
| People and hours | 2 engineers × ~50% × 10 working days; new to ADK, never used GCP (stated) |
| Money | ~USD 100/month allowance (A2, assumed) |
| Users and what they read | 25 helpdesk colleagues using it daily (stated) |
| Data and effects | Internal runbooks (read); Jira tickets created on request (write, visible to other teams) |
| Delivery profile | **Internal tool**: known colleagues, real internal data, one write effect |

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment (search + answer) | Build, with a 15–20 question regression set | Answer-quality complaints → G07 eval set |
| User identity | Build: IAP with Google identity, group-restricted | Users outside helpdesk → per-user data scope |
| Per-user data scope | Minimal: everyone reads the same spaces (A4) | Restricted pages or new spaces → per-user Confluence OAuth |
| Secrets | Build: Secret Manager, runtime service account, least privilege | — |
| External writes | Minimal: ticket draft the human submits in Jira (D4) | Phase 2 direct create (G05) with confirmation and duplicate protection |
| Sensitive data | Minimal: no prompt/response content in logs or spans | Personal data found in runbooks or chats → `protect-adk-sensitive-data` |
| Prompt injection and agency | Minimal: no write or egress tool in phase 1; links built in code | G05 adds a write tool → split/confirm (`adk-agent-security`) |
| Budgets and loops | Minimal: per-invocation model-call cap in code + budget alert | Spend > 50% of allowance → per-user allowance |
| Memory and retrieval | Live Confluence search, in-memory sessions | Poor recall on regression set → indexed search (later) |
| Frontend | ADK dev UI behind IAP (A10) | Any user outside the team, or session privacy concern → G06 |
| Hosting | One Cloud Run service, max 1 instance, behind IAP | Concurrency complaints or session loss → G06 shared sessions |
| Observability | Minimal: structured logs, token counts, no content | First incident not diagnosable → G08 |
| Release | Minimal: pinned ADK, model ID, unit tests run before deploy | Second contributor or model migration → G07 |
| Performance tuning | Defer | Measured p95 latency complaint |

**Floor kept:** no secrets in code, prompts or logs (Atlassian token in Secret
Manager); a model-call cap per invocation plus a billing alert (alerts do not
cap spend); no ticket is created without a human submitting it; real data is
limited to allowlisted runbook spaces and is kept out of logs; model ID pinned.

**Accepted risk (provisional, owner: helpdesk engineering lead):** the ADK dev
UI lists sessions without per-user isolation, so team members could open each
other's conversations. Ends when G06 ships or when anyone outside the 25-person
team gets access.

**Who may use it:** members of the `helpdesk@` group, on the allowlisted
runbook spaces. **Graduation conditions** before more users or more data:
per-user session ownership (G06), direct ticket creation only with
confirmation and duplicate protection (G05), an evaluation set run before each
release (G07), and diagnosable failures (G08).

**Capacity and cut line.** 2 × 0.5 × 10 days × 6 h × 0.6 focus ≈ **36 focused
hours**; 25% reserve leaves **27 hours**. Phase 1 (G01–G04) is estimated at
**21–31 hours**: the low and middle of the range fit, the high end does not.
If work runs high, **G04 (ticket draft) moves to phase 2**; G01–G03 (18–25 h)
still deliver hosted runbook search. Phase 2: G05–G08.

## Guarantees and acceptance

| Invariant | Enforcing component | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 Only `helpdesk@` members reach the assistant | IAP on Cloud Run | 403 from IAP, no agent call | Non-member account gets 403 (G03) |
| I2 Search reads only allowlisted spaces, never `restricted` pages | `search_runbooks` adapter builds the CQL; the model supplies only free text | Out-of-scope page never returned | Unit test: model-supplied `space = HR` text is quoted, not executed; adapter output space set ⊆ allowlist (G02) |
| I3 Every answer that cites a runbook links a page the tool returned in this turn | Instruction only (a probabilistic control, not runtime-enforced at this profile); measured by the regression check | Answer without a source should say "no runbook found"; an uncited answer is a regression failure | Regression set: citation URL ∈ tool results (G02) |
| I4 No ticket exists unless a person submits it (phase 1) | No Jira credential or write tool exists in phase 1 | — | Tool list dump contains no write tool; no Jira secret in project (G04) |
| I5 One user turn makes at most 6 model calls | `before_model_callback` counter keyed on invocation ID | Turn ends with "I stopped; please rephrase" | Scripted-model test exceeds cap (G01) |
| I6 Prompt and response text never reach logs or spans | `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; log statements carry IDs and counts only | — | Log grep after a test turn finds no question text (G03) |

## Architecture and decisions

```
Browser (Google login) ──IAP (helpdesk@)──> Cloud Run: ADK app, 1 instance
                                              │  runtime service account
                                              ├─> Vertex AI Gemini (pinned)
                                              ├─> Secret Manager: Confluence token
                                              └─> Confluence Cloud REST (read, allowlisted spaces)
Ticket draft = Jira "create" URL built in code ──> user's browser ──> Jira (user's own login)
```

One `LlmAgent` with two function tools: `search_runbooks` (read) and
`draft_ticket` (builds a link, no network). No sub-agents: one responsibility,
one small tool set.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Answer runbook questions in plain language | One `LlmAgent`, two function tools | Single judgment, two capabilities; no routing contract to maintain | Multi-agent adds nothing until a write tool arrives (revisit in G05) | Tool dump shows two declarations |
| D2 | Find the right runbook passage, current | Live Confluence Cloud CQL search via a function tool, results bounded to 5 pages × ~1,500 chars of body text, with URL and last-modified date | Always fresh, no index or ingestion pipeline to learn in two weeks; reuses Confluence permissions on a read-only account | Keyword search recall is weaker than a semantic index (Vertex AI Search); Atlassian MCP server rejected: brings write tools and server-supplied descriptions | Regression set hit@5 ≥ 0.8 on 15–20 questions (provisional target) |
| D3 | Credentials never leak | Read-only Atlassian bot account; API token in Secret Manager read by the runtime service account | No secrets in code; one shared read credential matches A4 | Per-user OAuth (3LO) would honour page restrictions; deferred by A4 | Secret absent from repo and image; adapter fails closed when secret missing |
| D4 | "Create a Jira ticket on request" without unattended writes | Phase 1: `draft_ticket` returns summary, description and a Jira create link pre-filled in code (fixed site, project, issue type); the user reviews and submits in Jira under their own login | Keeps the human-approval floor with no write credential, no duplicate risk and no reporter mapping; ~3–5 h vs ~8–12 h for API create | One extra click; field pre-fill depends on Jira Cloud's create-URL support (unverified, G04 spike, fallback copyable text). Phase 2 G05 adds API create with confirmation | Link opens Jira create with fields filled (manual check); no Jira credential exists |
| D5 | Colleagues sign in with their own identity; new-to-GCP team | Cloud Run (one service, `max-instances=1`, in-memory sessions) behind IAP restricted to `helpdesk@`; ADK dev UI as front end (A10) | Smallest GCP surface a new team can stand up; IAP gives verified Google identity without app code | Sessions lost on restart/deploy; dev UI lacks per-user isolation (accepted risk); Agent Runtime rejected as more concepts for the team | Non-member 403; member completes the journey |
| D6 | Stable behaviour, low cost | `gemini-3.5-flash` on Vertex AI, pinned; ADK `google-adk==2.8.0` working pin | Stable in the lifecycle table (checked 2026-10-08); Vertex retirement "2027-05-19 or later", beyond phase 2; ADK 2.8.0 is what the specialist skills were verified against | `gemini-3.8-flash` is newer with no retirement date but less evidence in the skills; migration is a planned release (Later list) | Release note records model ID; G01 confirms pin and model availability |

Source: model lifecycle from
`.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
(`checked_on` 2026-10-08). ADK version from the specialists'
`references/compatibility.md` (google-adk 2.8.0). **Not verified in this
session (no network):** Confluence Cloud CQL search endpoint and fields, Jira
Cloud create-URL pre-fill parameters, IAP support directly on Cloud Run vs via
a load balancer, Vertex pricing for the chosen model. Each is an acceptance
item of the goal that first uses it.

### Model-facing contracts

| Surface | Contract | Skill and verification |
| --- | --- | --- |
| Instruction | Answer only from `search_runbooks` results, cite page URLs, say "no runbook found" otherwise; call `draft_ticket` only when the user asks for a ticket; never invent ticket keys. Identity, project and URLs stay in code | `adk-agent-instructions`; rendered-request test |
| Tools | `search_runbooks(query: str) -> {status, results:[{title,url,updated,excerpt}]}` (read); `draft_ticket(summary: str, description: str, component: str \| None) -> {status, create_url, summary, description}` (no effect). Bounded sizes, actionable errors | `adk-tool-interface-design`; declaration dump and size |
| Output | Free text with links; no `output_schema` in phase 1 | `adk-model-and-output-contracts` for model pin only |

## Data and authority

| Data | Owner / scope | Writers / readers | Source and freshness | Lifetime |
| --- | --- | --- | --- | --- |
| Runbook pages | IT knowledge owners | Confluence editors / assistant (read-only bot) | Live per query | Not stored by the assistant beyond the session |
| Conversation | Helpdesk user | ADK in-memory session | Per turn | Until instance restart; no persistence |
| Ticket draft | Helpdesk user | Assistant drafts; user submits in Jira | At draft time | Only in session and Jira once submitted |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Phase 1 assistant | Internal runbooks, user's question | Runbook text (edited by many staff) | None: `draft_ticket` makes no call; links use a fixed Jira base URL | Trifecta incomplete. Residual: the model could emit an arbitrary markdown link a user clicks; accepted at this profile, revisited in G05 |
| Phase 2 (G05) | Same + ticket content | Same | Jira create | Write gated by ADK tool confirmation in code; fields shown to the user are those submitted; `adk-agent-security` review in G05 |

## Budgets and capacity

25 users; assumed ≤ 300 questions/day, ≤ 3 concurrent. Per turn: expected 2–3
model calls (search, maybe re-search, answer), cap 6 (I5); each call ≲ 10k
input tokens because tool results are bounded (D2). Cost: symbolic,
`turns/day × 3 calls × (10k × input price + 1k × output price)`; prices not
looked up (no network). The billing budget alert is an observation, not a cap;
the call cap is the enforced limit. One Cloud Run instance with request
concurrency ~10 covers the assumed load; verify in G03.

## Failure and recovery

| Failure | User sees | Retained state / effects | Next action, owner |
| --- | --- | --- | --- |
| Confluence unavailable or token invalid | "Runbook search is unavailable" (tool `status: error`), not an invented answer | None | Retry later; engineer rotates token |
| Search returns nothing | "No runbook found", offer a ticket draft | None | User decides |
| Model error or call cap hit | Turn ends with an explicit stop message | Session keeps prior turns | User rephrases; engineer checks logs |
| Instance restart / deploy | Conversation history gone | No external effects exist (phase 1) | Start a new conversation |
| Runbook contains injected instructions | Answer may be wrong; no action possible | None (no write tool) | Page owner fixes page |
| User submits the same draft twice in Jira | Two tickets | Jira, under the user's name | User closes duplicate (phase 2 G05 adds duplicate protection) |
| Non-member reaches URL | IAP 403 | None | — |
| Model `gemini-3.5-flash` retirement | Planned migration before Vertex retirement | — | Engineers, Later list |

Not applicable in phase 1: provider-commit-reply-lost, approval races and
erasure races, because the assistant makes no external write and stores
nothing durable. They return with G05.

## Verification

Offline: unit tests for both tool adapters with recorded Confluence responses,
the call cap with a scripted model, and the rendered request. Local
integration: `adk web` against the real Confluence spaces (read-only) and the
regression set. Hosted: IAP denial and member journey on Cloud Run, log grep
for content. None of these has been run; they are planned in the goals.

Release (minimal): `pyproject.toml` pins `google-adk==2.8.0`; the model ID is a
constant in code and appears in the deploy note; unit tests run before each
`gcloud run deploy`.

## Open decisions

| Question | Why it matters | Owner / evidence | Blocks |
| --- | --- | --- | --- |
| A3–A7 Atlassian edition, spaces, restrictions, sign-in, Jira project | Change credentials and scoping | Helpdesk lead | G02 (spaces), G03 (group), G04 (project) |
| A8 Draft-then-submit acceptable for phase 1? | Moves the cut line | Helpdesk lead | G04 vs G05 order |
| A10 Dev UI acceptable for the team? | Accepted privacy risk | Helpdesk lead | G03; else G06 moves into phase 1 and G04 out |
| A9 Residency | Region and model location | IT / security | G01 region choice |
| Jira create-URL pre-fill on Cloud | D4 mechanism | G04 spike, 1 h | G04 only |
