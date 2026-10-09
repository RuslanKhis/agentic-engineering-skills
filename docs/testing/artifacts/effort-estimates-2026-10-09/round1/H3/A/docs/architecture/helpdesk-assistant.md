# System design: IT helpdesk runbook and ticket assistant

Status: **draft**. Every product answer below is assumed (the user was not
available), so the decisions that depend on them are provisional until the user
confirms the Assumed answers table.
Plan: [docs/plans/helpdesk-assistant.md](../plans/helpdesk-assistant.md)

## Assumed answers

These are the questions I would have asked before designing. Each answer is
assumed, and the decisions in the right-hand column stay provisional until it is
confirmed.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When is the first useful version due, and is it continued? | In two weeks; it will be continued | Phase 1 code is kept (D1–D6) |
| A2 | How many hours is "half their time"? | 3 focused-day hours each of a 6-hour day, 10 working days | Capacity, cut line |
| A3 | What can be spent on models and cloud? | Up to about US$100 a month during phases 1–2 | D5 model tier, spend stop |
| A4 | Who uses it and who judges phase 1? | All 25 helpdesk staff in the end. Phase 1 is judged by the helpdesk lead from a demo and a measured gold-question score | Cut line, G03 |
| A5 | Which identity provider do staff sign in with? | Google Workspace or Cloud Identity, so Identity-Aware Proxy (IAP) can admit a Google group | D7 (phase 2) |
| A6 | Are Confluence and Jira Atlassian Cloud or Data Center? | Atlassian Cloud, reachable over the public REST APIs | D2, D3, G01 |
| A7 | Is the runbook space readable by all 25 staff, with no page-level restrictions? | Yes, one or two spaces (for example `ITRB`) that every helpdesk member can read | D2: a single read-only bot account |
| A8 | Do runbooks contain credentials or personal data? | No credentials (policy forbids them). Conversations may name end users and devices | Floor, D8 logging, G03 secret scan |
| A9 | Which Jira project, issue types and fields? Who is the reporter? | One project (`ITHD`), Incident or Service Request, with summary, description, priority and component. The reporter is the bot in phase 1, with a "Requested by" line | D3, G04, G10 |
| A10 | Create only, or also update, comment and transition? | Create only | D3 tool set |
| A11 | Is there an existing GCP organisation and billing account? | No; an admin must create a project and link billing | G01 calendar wait |
| A12 | Is Vertex AI (Gemini) approved for internal runbook text, and is there a residency constraint? | Approved; no residency constraint | D5, region |
| A13 | Where should staff use it: a web page, Google Chat or Slack? | A simple internal web page | D7 (phase 2) |
| A14 | Who labels the gold questions? | The helpdesk lead, about 2 hours | G03 |

## Purpose and constraints

**Journey.** A helpdesk analyst is on a call: "VPN fails with error 809 since
the macOS update." Today they search Confluence by hand, often land on an
outdated page, and then retype the details into a Jira ticket for the network
team. With the assistant, they ask the question in chat and get the steps from
the matching runbook with a link to it. Then they say "raise a ticket for
network". The assistant shows the exact ticket it would create, the analyst
confirms, and the reply gives the ticket key (`ITHD-1234`).

**Outcome to improve (hypothesis, not yet measured).** Less time to find the
right runbook, and fewer mis-filed tickets. The baseline is unknown. Phase 1
measures runbook retrieval on gold questions; a time-to-answer comparison
follows in phase 2 (G11).

**Model decides:** which search terms to use, which runbook answers the
question, how to summarise its steps, and the wording of the ticket draft.
**Code controls:** which Confluence spaces can be read, the Jira project and
allowed fields, the confirmation before any write, who the user is, call
limits, and what is logged.

**Non-goals:** editing Confluence, updating or transitioning Jira issues, end
users (non-helpdesk staff) using the tool, and Slack or Chat integration.

**Observed repository facts:** the repository is empty apart from `.claude/`.
There are no manifests, pins or code, so everything below is proposed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | 2 weeks; continued (A1) |
| People and hours | 2 engineers × half time × 10 days. Both are new to ADK and have never used GCP (given). Afterwards the same two run it (assumed) |
| Money | ≤ US$100 a month for models and cloud (A3) |
| Users or judge | 25 helpdesk colleagues daily. Phase 1 is judged by the helpdesk lead: a demo plus the gold-question score |
| Data and effects | Internal runbooks (read). Creates internal Jira tickets: a reversible write visible to colleagues, never to outside people |
| Delivery profile | **Internal tool.** Known colleagues, real internal data and one internal write. Phase 1 is a local pilot; phase 2 graduates it to all 25 staff |

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment (runbook answer), measured | **Build**: 20 gold questions, scored | Hit rate below 70% → semantic retrieval (Later) |
| User identity and per-user scope | **Defer** to G06/G07. Phase 1 runs locally for the two engineers and the lead only | Any user other than the two engineers → G06/G07 first |
| Secrets and credentials | **Build**: Atlassian tokens in Secret Manager, keyless GCP access through ADC | Hosting (G07): use the service account, not developer ADC |
| External writes (Jira) | **Build**: confirmation enforced in code, one project, allow-listed fields, no automatic retry | Any second write type → a new decision |
| Sensitive data | **Minimal**: no message content in logs; secret-pattern scan of the runbook space | Personal data in runbooks, or a wider audience → `protect-adk-sensitive-data` |
| Prompt injection and agency | **Minimal**: confirmation with the exact payload, no egress tool, page allow-list in code | Phase 2 G09 adversarial cases |
| Budgets and loops | **Minimal**: `RunConfig.max_llm_calls=8`, a billing budget alert | Hosted use → per-user daily cap (Later) |
| Memory and retrieval | Live Confluence search; in-memory sessions | Restart loss hurts users → durable sessions (Later) |
| Frontend | `adk web` locally | G06 page |
| Hosting | Local only | G07 Cloud Run behind IAP |
| Observability | Console logs | G07 structured logs and token cost |
| Release engineering | **Minimal**: pinned model and ADK, unit tests | G08 tests in CI |

**Floor kept:** no secrets in code, prompts or logs; a spend stop
(`max_llm_calls` per invocation, plus a budget alert on the project); no Jira
ticket without a human confirming the exact payload; real data limited to the
runbook space(s) and one Jira project; a pinned model ID. No risks are accepted
beyond those stated in the Security posture section.

**Who may use phase 1:** the two engineers, and the helpdesk lead during a
demo, on real runbooks and the real `ITHD` project, or a sandbox project if the
Jira admin prefers one (open decision O4).

**Graduation conditions before the other 23 staff use it:** verified identity
on every request (G06), hosting behind IAP with a service account (G07), tests
in CI with pinned versions (G08), and adversarial cases for the write tool (G09).

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Per-user Confluence permissions (OAuth 3LO) | Assumed: the whole space is readable by all staff (A7) | Page restrictions in the space, or users outside the helpdesk |
| Reporter set to the real user | Bot plus a "Requested by" line is enough for a pilot | Phase 2 G10, or a Jira reporting need |
| Durable sessions (Cloud SQL) | Lookups are short; tickets are durable in Jira | Complaints about lost chats, or more than one Cloud Run instance |
| Semantic retrieval (Vertex AI Search connector) | Live CQL search costs no ingestion | G03 hit rate below 70% |
| SLOs and alerts | 25 internal users; failures are visible | Daily use by all 25, or an incident |

**Capacity and cut line.** 2 × 0.5 × 10 days × 6 h × 0.6 focus ≈ **36 focused
hours**. Holding back 25% (9 h) leaves 27 h. Phase 1 (G01–G04) is estimated at
**15–26 h**, so it fits at the high end. Phase 2 (G05–G11, about 23–42 h) waits
for the next block of time. The cut line is in
[the plan](../plans/helpdesk-assistant.md#delivery-profile-and-capacity) and is
open for the user to move (O1).

## Guarantees and acceptance

| Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1. The assistant reads only the configured runbook space(s) | `confluence.py` adds `space in (...)` from config to every CQL query, and `read_runbook` checks the page's space before returning its body | An out-of-scope page ID returns `status: not_allowed` | Offline: a fake Confluence holds a page in space `HR`, and `read_runbook` refuses it (G02) |
| I2. No Jira issue without a human confirming the exact payload | `create_jira_ticket` is wrapped with ADK tool confirmation. Code loads the stored draft by `draft_id` and checks its hash against the confirmed hash | The tool is not executed; the chat says "not created" | Offline: a scripted model calls create without confirmation, or with a changed draft, and the fake Jira records 0 calls (G04) |
| I3. One confirmation causes at most one create attempt | Draft state moves `proposed → submitted → created / failed / uncertain` in session state. There is no automatic retry; a submitted draft cannot be resubmitted | Timeout → "uncertain: check Jira for label `hda-<op_id>`" | Offline: a fake timeout gives 1 call and an `uncertain` status; a second confirm is refused (G04) |
| I4. Answers cite their runbook, or say none was found | Instruction plus the tool result shape `{status, results:[{title,url,excerpt}]}`; an empty search returns `no_results`, never a broadened scope | "No runbook found in ITRB for …" | G03 gold questions include 3 with no runbook (expect a "none found" answer) |
| I5. Spend is bounded per request | `RunConfig.max_llm_calls=8`; tool results bounded (5 hits, page ≤ 8,000 characters) | Over-limit error shown; nothing written | Offline Runner test with a looping scripted model (G02) |

## Architecture and decisions

```
analyst ──(phase 1: adk web, local │ phase 2: IAP → Cloud Run page)──▶ FastAPI + Runner
                                                     │  user_id = verified email (phase 2)
                                                     ▼
                                       LlmAgent "helpdesk_assistant" (gemini-3.8-flash, Vertex AI)
                 read tier ─────────────┬───────────────────────┐   write tier (confirmation)
        search_runbooks(query)   read_runbook(page_id)   draft_jira_ticket(...)  create_jira_ticket(draft_id)
                 │  space allow-list in code               │ stores draft      │ Jira bot token, project ITHD
                 ▼                                          ▼                   ▼
        Confluence Cloud REST (read bot)            session state       Jira Cloud REST (create-only bot)
Secrets: Secret Manager (Atlassian tokens)  ·  Model: Vertex AI  ·  Sessions: in-memory
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Language lookup plus one write, built by an ADK-new team (given) | One `LlmAgent` with four function tools. No sub-agents | One judgment (answer, then draft); the tools are separate capabilities | Multi-agent routing is not needed; revisit if write tools grow | Declaration dump shows 4 tools (G02) |
| D2 | Read runbooks with live freshness (A6, A7) | A Confluence Cloud REST CQL search through a read-only bot account, limited to the configured spaces | No ingestion pipeline; always current; permissions come from the space | Keyword search quality is lower than semantic search; Vertex AI Search is the alternative (Later) | G03 gold hit rate; I1 test |
| D3 | Create tickets on request, safely (A9, A10) | Two tools. `draft_jira_ticket` validates the fields and stores a canonical draft; `create_jira_ticket(draft_id)` requires ADK confirmation and writes with a create-only bot to `ITHD`. Each write carries a `hda-<op_id>` label | The confirmation is in code the model cannot reach; one project and fixed fields limit the effect | Per-user OAuth would attribute properly but costs 8–16 h plus a wait; deferred | I2, I3 tests (G04) |
| D4 | Tool sources | Hand-written function tools, not the Atlassian MCP server or the OpenAPI toolset | Exactly 4 small declarations; results bounded at the tool | We write the HTTP code ourselves (about 2 short clients) | Declared bytes recorded (G02) |
| D5 | Pinned, supported model within budget (A3, A12) | `gemini-3.8-flash` on Vertex AI, `thinking_level` low. Picked from `model-lifecycle-2026-10-01.json` (checked_on 2026-10-08): stable, with no shutdown date | Newest stable Flash. `gemini-3.6-flash` retires on Vertex 2026-11-19 and `3.7-flash` on 2027-01-28, inside the plan horizon | If 3.8 is not offered on Vertex in the chosen region, fall back to `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later) | G01: a smoke call with the pinned ID, and the Vertex model page re-read |
| D6 | Pinned framework | `google-adk==2.8.0`, Python 3.11, the versions the specialist skills were checked against. The working assumption is to confirm it against the chosen pin in G02 | Specialist guidance (for example the confirmation and callback behaviour) was verified on 2.8.0 | A newer ADK might need re-verification | G02 acceptance: the pin recorded and the confirmation API checked |
| D7 | Colleagues use it with their own identity (phase 2, A5, A13) | A small FastAPI app owning the `Runner`. Every request's `x-goog-iap-jwt-assertion` is verified, and `user_id` is the verified email. It runs on Cloud Run with ingress restricted to IAP for the Google group `it-helpdesk` | `adk web` sessions are not authenticated application sessions (`adk-tool-auth-and-secrets` identity-and-output.md:9) | Agent Runtime needs a gateway anyway; GKE is too heavy for the team | G06 cross-user session denial test |
| D8 | No conversation content in logs (A8) | Log only event metadata (tool name, status, latency, token counts, op_id); content capture in spans turned off | Conversations name end users | Debugging needs reproduction from the session, not the logs | A log capture test asserts there is no message text (G07) |

Runtime and versions are working assumptions: ADK 2.8.0, Vertex AI in a
region to be confirmed (G01), and Cloud Run in the same region (phase 2).
Provider prices and quotas were not looked up (no network in this session), so
they are verification items in G01.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Answer from runbooks only, and cite the page URL. Say "no runbook found" rather than guess. Offer a ticket draft only when asked. Never claim a ticket exists without a key from `create_jira_ticket`. Spaces, project and user identity stay in code | `adk-agent-instructions`; rendered-request test |
| Tools | `search_runbooks(query: str)` → ≤5 `{title, url, page_id, excerpt}`. `read_runbook(page_id: str)` → text ≤8,000 characters. `draft_jira_ticket(summary, description, issue_type, priority, component)` → `{draft_id, rendered}`. `create_jira_ticket(draft_id)` → `{status, key or reason}`. Tiers: read, read, read (state only), write with confirmation | `adk-tool-interface-design`; declaration dump |
| Output and model | Free-text answer, no `output_schema`. Pinned `gemini-3.8-flash`, no failover in phase 1 | `adk-model-and-output-contracts`; scripted bad-tool-argument test |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Runbook pages | IT knowledge owners; spaces in `CONFLUENCE_SPACES` | Read bot / agent | Confluence, live per call | Not stored beyond the session's tool events |
| Conversation and drafts | The analyst (phase 2: the verified email) | Runner / the same user | In-memory session | Lost on restart; nothing persisted |
| Jira issue | Project `ITHD` | Create-only bot / all helpdesk staff | Jira is authoritative; the key is the receipt | Jira retention |
| Atlassian tokens | Engineer B (owner) | Secret Manager → app | Rotated manually | Revoke in Atlassian admin |

There are three identities: the analyst (phase 2: IAP-verified email), the
workload (developer ADC in phase 1, a Cloud Run service account in phase 2) and
the two Atlassian bot accounts. The model never chooses credentials, project or
space.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| helpdesk_assistant | Internal runbooks and caller details | Runbook text (anyone with space edit rights can author it) and text pasted from end users | Jira create in one internal project | The trifecta is present but the write is internal and confirmation-gated. The exact payload is shown before execution; there is no URL fetch, email or other egress tool. **Accepted risk until G09** (owner: Engineer B): an injected runbook could shape a draft, but cannot create it without a human |

## Budgets and capacity

Workload (assumed): 25 users × about 15 questions a day ≈ 375 invocations a
day. Expected ≈ 3 model calls each (search, read, answer); the bound is 8. At
about 6k input and 0.5k output tokens a call that is about 7M input and 0.6M
output tokens a day. The price for `gemini-3.8-flash` was not looked up, so
**G01 computes the monthly cost from the current Vertex pricing page**. If it
exceeds A3, switch the default to `gemini-3.5-flash-lite` and re-run G03.
Concurrency is low (under 5 in flight), so one Cloud Run instance is enough.
A Cloud Billing budget alert only notifies; the enforced stops are
`max_llm_calls` and, in phase 2, a per-user daily cap (Later).

## Failure and recovery

| Failure window | User-visible outcome | Retained state / effects | Safe next action and owner |
| --- | --- | --- | --- |
| Confluence unavailable or 401 | "Runbook search unavailable", with no invented answer | None | Retry later; Engineer B checks the token |
| Search finds nothing | "No runbook found in ITRB" | None | Analyst rephrases, or files a doc gap |
| Model unavailable or over the call limit | Error message; no ticket | Session events so far | Retry the turn |
| Jira create times out after confirmation | "Creation uncertain — search label `hda-<op_id>`" | Draft `uncertain`; a ticket may exist | Analyst checks Jira; no automatic retry (I3) |
| Jira rejects the payload (400) | "Not created: <field error>" | Draft `failed`, which can be edited into a new draft | Analyst edits and confirms the new draft |
| Process restart | Chat lost; tickets already created remain | In-memory sessions gone | Start a new chat (durable sessions in Later) |
| Injected text in a runbook asks for a ticket | A draft may appear; nothing is created without confirmation | No effect | G09 asserts that create is never executed without confirmation |
| Model retirement | None if planned | — | Calendar the dates; re-run G03 before switching |

## Verification and implementation handoff

Offline (G02, G04): a fake Confluence and Jira, a scripted model through the
real `Runner`, and tests for I1–I3 and I5. Live and bounded (G03, G04): about 20
gold questions against real Confluence (≤ 200 model calls), plus one confirmed
ticket in `ITHD` or a sandbox. Hosted (G07): IAP denial and cross-user session
denial. The outcome hypothesis (faster runbook finding) is measured separately
in G11 from a before/after sample. Release bundle: ADK pin, model ID, prompt
file hash and tool schema hash, recorded in `release.json` from G08.

Goals, estimates and run prompts are in the
[implementation plan](../plans/helpdesk-assistant.md); phase 1 tickets are in
`docs/tickets/helpdesk-assistant/`.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence | What it blocks |
| --- | --- | --- | --- |
| O1. Confirm the cut line (G01–G04 now; hosting in phase 2) | Users other than the engineers need G06/G07 | User | Nothing in phase 1 |
| O2. Identity provider (A5) | A non-Google IdP needs workforce identity federation with IAP: more hours and admin time | IT admin | G06, G07 |
| O3. Atlassian Cloud vs Data Center (A6) | Data Center needs private connectivity from GCP | Atlassian admin | G01, G02 live calls |
| O4. Real `ITHD` or a sandbox project for phase 1 | Real tickets from a pilot need Jira admin agreement | Jira admin | G04 live check |
| O5. `gemini-3.8-flash` on Vertex in the chosen region, and its price | Model pin and cost | G01 lookup | G03 |
| O6. ADK confirmation works with the chosen frontend and session service at 2.8.0 | I2 relies on it; the fallback is a confirm endpoint in the G06 page | G04 check | G04 |
