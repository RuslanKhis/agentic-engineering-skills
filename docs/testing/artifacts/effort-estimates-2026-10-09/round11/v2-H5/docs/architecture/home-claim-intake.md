# System design: home-insurance claim intake agent (EU)

Status: **draft**. Every product decision rests on an assumed answer (table
below) because the user was not available; decisions marked *provisional*
change if an assumed answer changes. Nothing here has been implemented or
tested. Plan: [docs/plans/home-claim-intake.md](../plans/home-claim-intake.md).
Tickets: [docs/tickets/home-claim-intake/](../tickets/home-claim-intake/).

Decisions and their rationale live here; the plan and tickets refer to them
by ID (D1, D2 …). Capacity, finish range and cut line live in the plan's
summary and are not restated here.

## Assumed answers

The request fixed: production service; customers file a home-insurance claim
with photos; the claim is created in Guidewire; five engineers, one ML
engineer, one part-time security reviewer; five months to general
availability (GA) in the EU. Everything else is assumed.

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | Start date and exact GA date; is it continued after GA? | Start Mon 2026-10-19, GA Mon 2027-03-15; 95 working days after holidays and leave; continued and extended after GA | Plan calendar, D3 model choice (retirement dates) |
| Q2 | How familiar is the team with ADK and GCP? Full time? | Experienced Python/GCP engineers, new to ADK (×1.5 on all estimates); five engineers and the ML engineer full time at 5 focused h/day; security reviewer about 1 h/day | All estimates, load table |
| Q3 | Which Guidewire product and version, and how do we reach it? | ClaimCenter on Guidewire Cloud with the Cloud API (Claim API for draft claims, submit and documents); policy verification through ClaimCenter's policy search against PolicyCenter; a non-prod tenant exists but needs an access request | D7, D8, G01, G25, W1, W7 |
| Q4 | Which EU markets and languages at GA? | One market (Germany), German and English; more markets after GA | D3 region, G06, G25 phase 2 goal G27 |
| Q5 | How do customers sign in, and where does the journey live? | Existing customer portal (web and mobile web, React) with an existing OIDC customer identity provider (CIAM); the team can change the portal | D6, D12, G03, G10 |
| Q6 | Expected volume and peaks? | About 2,000 digital home claims per month at GA; storm (catastrophe) peaks of 10× the daily average for 2–3 days | D13, G18, G20, budgets |
| Q7 | Budget for models and cloud? | Non-prod model and cloud spend capped at €3,000 per month (budget alert plus application ceiling); production cost per claim to be measured in G20 and approved before GA | D13, G07, G18 |
| Q8 | Which data may we collect, and is any of it out of bounds? | Personal data needed for first notice of loss (FNOL): contact, policy, loss facts, photos. No bank details, no health details beyond "is anyone hurt / in danger". Photos may incidentally show people or documents | D9, D5, G12, G13 |
| Q9 | What may the system change? | Creates one claim per confirmed draft in production ClaimCenter and attaches its photos. It never decides coverage, liability, reserves or payments | D1, D7, D8 |
| Q10 | Who signs off GA? | Claims operations, the DPO (DPIA), security (pen test findings closed) and the change board | W2, W3, W6 |
| Q11 | Is there an existing GCP landing zone and approved region? | Yes, an organisation with EU-only resource-location policy; project creation by the platform team is quick | D2, G16 |
| Q12 | Regulatory classification under the EU AI Act? | Not high-risk (Annex III covers life and health insurance pricing, not property FNOL); transparency duty applies. Legal to confirm | D16, G13 |
| Q13 | Is there an existing classic web claim form we can fall back to? | Yes; it can accept a prefilled draft through a small change | D13, G10, G18 |
| Q14 | Must data use customer-managed encryption keys (CMEK)? | No at GA (Google default encryption); CMEK in the later list | Later list |

## Purpose and constraints

**Journey (running example).** On a Sunday evening a pipe bursts in a
policyholder's kitchen in Munich. Today they phone a claims line with long
waits during storms, or fill in a long web form, and are later emailed to
send photos; the adjuster often calls back for missing facts (date, cause,
affected rooms, whether the water is stopped). With this service they sign
in to the portal, pick "report home damage", describe what happened in
German, upload six photos, answer a few targeted follow-up questions, review
a summary the server renders, press **Confirm**, and within about a minute
see a claim number; the photos appear on the claim in ClaimCenter.

**Outcome to improve (hypothesis, not yet measured).** More home claims
filed digitally with complete FNOL data and fewer adjuster call-backs for
missing facts, without more corrections by claims handlers. Baseline and
measurement: G24 (claims-handler review of staging claims against current
web-form claims); production measurement in the SLIs of G17.

**What the model contributes:** understanding the customer's description and
photos, asking for what is missing in their language, and proposing typed
field values for the draft. **What ordinary code controls:** identity, which
policy, which fields are required and whether the draft is complete, the
summary the customer confirms, claim creation, photo transfer, retries,
budgets, retention and every status shown.

**Non-goals at GA:** coverage or payout statements, damage valuation,
fraud scoring, adjuster-facing AI notes, voice, native mobile apps, other
lines of business, markets beyond Germany.

**Observed repository facts:** the repository holds only the skills
(`.claude/skills/`); there is no application code, manifest or lockfile.
All modules below are proposed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | GA 2027-03-15 (Q1); launched and continued |
| People and hours | 5 engineers + 1 ML engineer full time, 5 focused h/day; security reviewer ≈1 h/day; new to ADK (Q2); the same team runs it with claims IT on call |
| Money | Non-prod €3,000/month cap; production per-claim cost approved before GA (Q7) |
| Users or judge, and what they read | External customers in Germany using the portal; claims handlers read the created claims in ClaimCenter |
| Data touched and effects allowed | Personal data and photos of homes (regulated under GDPR); creates real claims in production ClaimCenter |
| Delivery profile | **Production service**: external customers, personal data and a write to the system of record, with a fixed GA date |

Depth per concern (production column of the delivery profile, adjusted):

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: evaluation set with held-out cases and a CI gate (G07, G19, G23) | — |
| Identity and per-customer scope | Build (G03, G04) | — |
| Secrets and credentials | Build: workload identity, Secret Manager, rotation rehearsed (G16) | — |
| External writes | Build: confirmation, durable operation, replay and reconciliation (G08, G09) | — |
| Sensitive data | Build: minimisation, content-free telemetry, screening, retention, erasure, residency (G12, G33) | — |
| Prompt injection and agency | Build: structural split D1, threat model, adversarial suite (G14) | — |
| Budgets and loop limits | Build: per-draft allowance, admission, kill switch, fallback (G18) | — |
| Memory and retrieval | Minimal: sessions and the draft only; no long-term memory or RAG | Cross-claim continuity requested (G28) |
| Frontend | Build in the existing portal (G10, G11) | — |
| Hosting | Build: Cloud Run with rollback (G16, G22) | — |
| Observability | Build: traces, SLOs and alerts (G17) | — |
| Release engineering | Build: CI gate, manifest, canary, joint rollback (G19) | — |
| Performance and cost tuning | Minimal: measure in G20; tune after GA | p95 turn latency above target or cost per claim above the approved figure |

**Floor kept:** no secrets in source, prompts or logs; spend stop (`RunConfig.max_llm_calls`
per invocation plus a per-draft allowance and a budget alert, G18); nothing
reaches ClaimCenter without the customer confirming a server-rendered summary
(D8); real personal data only in staging/production with content-free logs
(G12); pinned model ID (D3). No accepted risks beyond R1–R3 below.

**Accepted residual risks (need the user's confirmation):**

| ID | Risk | Owner | Ends when |
| --- | --- | --- | --- |
| R1 | A coverage-like statement by the model is prevented by instruction, screening and evaluation (G06/A3, G23/A1), not by a deterministic check | Claims product owner | A deterministic output check or a reviewed-template reply for coverage topics is built (later list) |
| R2 | Photos are forwarded to ClaimCenter as received; no authenticity or manipulation check | Claims fraud lead | Fraud signals item in the later list |
| R3 | Single-region deployment; a regional outage sends customers to the phone line and classic form | Platform lead | Multi-region item in the later list |

**Who may use it:** at GA, signed-in customers of the German market with a
home policy. Before that, staging with synthetic and test policies only.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| CMEK for stores | Not required by assumed policy (Q14) | Security or regulator requirement |
| Multi-region failover | Fallback channels exist; one region keeps residency simple | Availability target above 99.5 % or a regional incident |
| Context caching and cost tuning | Needs measured traffic | Cost per claim above the approved figure in G20 or production |
| Long-term memory across claims | Journey needs only the current draft | Product asks for "continue my previous claim" across devices (G28) |

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer can read, change or confirm only their own drafts, photos and status | Auth middleware derives `customer_id` from the verified token; every store query filters on it (D6) | 404 without data; no model call | G03/A2, G05/A4 |
| I2 A claim is created only for a draft version the customer confirmed, against a policy that is theirs and in force at the loss date when submitted | Submission service checks confirmation binding and re-checks policy just before create (D7, D8) | No claim; customer told why | G08/A2, G08/A7, G04/A4 |
| I3 One confirmed draft version produces at most one ClaimCenter claim | Operation record unique on (draft, version) + Guidewire dedup header or reference lookup (D7) | Second request joins the first operation | G08/A3, G08/A4, G08/A8, G25/A2 |
| I4 A confirmed claim is never silently lost; uncertain outcomes are reconciled | Durable operation record before acknowledgement, Cloud Tasks dispatch, sweeper, alert (D7) | "Received, number follows"; ops alert after 15 min | G08/A5, G08/A12, G17/A3 |
| I5 The model cannot cause an external write or egress | Agent's only tools write the customer's own draft; submission is application code behind a confirm endpoint (D1) | Forbidden call never runs | G14/A1, G14/A2, G36/A1 |
| I6 Customer content does not appear in logs or traces; data stays in the EU | Content capture off, EU endpoints only (D9) | Release blocked | G12/A1, G12/A5 |
| I7 Displayed status comes from the operation record, never from model text | Status API reads operation state (D12) | — | G11/A2 |
| T1 Turn latency p95 ≤ 8 s with photos, ≤ 5 s text only (provisional) | Measured in G20; G17 SLI | Tune or change model tier | G20/A1 |
| T2 Confirm → claim number p95 ≤ 60 s; photos attached p99 ≤ 15 min (provisional) | G17 SLI | Alert | G35/A1 |
| T3 Field accuracy on required FNOL fields ≥ 95 % on the held-out set; coverage statements 0 (provisional thresholds) | G23 with the G07 harness | GA blocked | G23/A1 |

## Architecture and decisions

```text
 Browser (portal, React) ──HTTPS──► Portal BFF / API gateway (existing)
        │  signed-URL PUT                │ customer access token
        ▼                                ▼
 GCS uploads bucket (EU) ◄──── claim-intake API (Cloud Run, europe-west3)
        │ finalize event                 │  FastAPI routes + auth middleware
        ▼                                │  ADK Runner ─► LlmAgent "intake"
 photo processor (same service)          │        tools: update_claim_draft, get_draft_status,
   validate, re-encode, strip EXIF       │               record_safety_concern, request_human
                                         │  Model Armor (EU) on user text and model reply
                                         │  Vertex AI Gemini (EU regional endpoint)
                                         ▼
                         Cloud SQL PostgreSQL (EU): ADK sessions, drafts,
                         photo records, submission operations, allowances
                                         │
                         Cloud Tasks queue ─► submission worker (same service, separate route)
                                         │   Guidewire client (OAuth client credentials from Secret Manager)
                                         ▼
                         Guidewire ClaimCenter Cloud API (policy search, draft claim, submit, documents)
```

Trust boundaries: the browser and everything a customer types or uploads is
untrusted; the BFF passes the customer's access token; the claim-intake
service is the only component holding Guidewire credentials; the model sees
only what the service puts in the request.

**Sequence (success).** (1) The browser sends a message with a client
message ID; middleware verifies the token and loads the customer's draft.
(2) Model Armor screens the text; the Runner calls the model with the
instruction, the code-computed list of missing fields, the selected policy
summary and photo derivatives. (3) The model calls `update_claim_draft`;
code validates and writes draft version *n+1*. (4) The reply is screened and
returned as one completed JSON turn. (5) When code marks the draft complete,
the UI shows the server-rendered summary of version *n*; **Confirm** sends
`(draft_id, version, summary_hash)`. (6) The API inserts a submission
operation and enqueues a named Cloud Task, then answers 202. (7) The worker
re-checks policy, creates the draft claim with a dedup key, submits it,
records the claim number, then attaches each photo. (8) The status page reads
the operation record.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | The agent reads untrusted text and photos and the service holds personal data and a write to ClaimCenter (lethal trifecta) | **One `LlmAgent`** whose tools only change the signed-in customer's own draft; no tool can create a claim, send a message or fetch a URL. Claim creation is application code reached only through the confirm endpoint | Removes the external write and egress legs from the agent, so an injected instruction can at most propose draft values the customer then sees in the summary | A second "submit" tool with ADK tool confirmation would be fewer screens but puts the write within the model's reach; separate photo-reader agent rejected as unnecessary once the write leg is gone | G14/A1, G14/A2 | proposed |
| D2 | EU hosting, custom upload, confirm and status routes, team operates it | **Cloud Run** service (FastAPI + ADK Runner) in `europe-west3`, min instances ≥ 1 in prod; worker as a separate route on the same image with its own concurrency | Custom routes and Cloud Tasks targets fit Cloud Run; no cluster to run | Agent Runtime gives managed sessions but adds a gateway for uploads and confirm and its EU availability must be checked; GKE adds operations work the team does not need | G16/A1, G22/A1 | provisional (Q11) |
| D3 | Multimodal understanding in German and English, stable for the plan horizon, data in the EU | **`gemini-3.8-flash` on Vertex AI, EU regional endpoint**, pinned; judge pinned to the same ID with human calibration (G07/A3). Lifecycle table `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (checked_on 2026-10-08): 3.8-flash stable, released 2026-09-02, no retirement listed. `gemini-3.7-flash` retires on Vertex 2027-01-28 and `gemini-3.6-flash` 2026-11-19, both before GA; `gemini-3.5-flash` Vertex retirement "2027-05-19 or later", two months after GA | Newest stable model with no announced retirement inside the horizon | Same-family judge may share blind spots (mitigated by human calibration); EU regional availability of 3.8-flash **unverified**: G02/A6 checks it; fallback candidate `gemini-3.5-flash` with a planned migration | G02/A2, G02/A6 | provisional |
| D4 | Conversation must survive restarts and replicas; drafts are business records | ADK `DatabaseSessionService` on **Cloud SQL for PostgreSQL** (EU, HA in prod); drafts, photo records, operations and allowances in application tables in the same instance | One transactional store; draft versions and operation uniqueness need SQL constraints | Firestore would need its own uniqueness design; session events are not the draft's authority, the draft table is | G02/A7, G08/A3 | proposed |
| D5 | Photos up to 20 per claim, adjusters need originals, the model needs small images without location data | Browser uploads to a **private EU GCS bucket by signed URL** (15 min, path scoped to customer and draft); the service validates type by content, rejects > 20 MB, creates a re-encoded ≤ 1536 px derivative without EXIF for the model; originals go to ClaimCenter | Large bodies stay off the API; the model never sees GPS or full-size images | Sending images through the chat API is simpler but couples upload size to turn latency | G05/A1–A7 | proposed |
| D6 | Customers see only their own data; Guidewire credentials are service-wide | Middleware verifies the OIDC access token (issuer, audience, signature, expiry; cached JWKS) and sets `customer_id` in trusted session state; policies come from a code lookup by customer, chosen in the UI; tools never take customer or policy IDs as arguments | The service account can read any policy, so customer↔policy authority must be enforced in our code | Per-customer delegated access to Guidewire is not available in the assumed setup | G03/A1–A7, G39/A1–A2, G04/A1, G04/A4 | provisional (Q3, Q5) |
| D7 | At most one claim per confirmed draft version; no lost claims under timeouts, restarts or duplicates | **Durable submission operation**: row inserted (unique on draft and version, canonical payload hash) before the 202; named Cloud Task per step; worker steps `create_draft_claim → submit → attach_photo[i]` each with a stable dedup key and fencing on operation version; on an unknown outcome, look up the claim by our reference before any new create; a sweeper re-enqueues stale operations | Separates conversation, attempt and business operation; makes replay safe | More states and an ops alert compared with a synchronous call; the dedup header semantics are **unverified** (G01 from docs, G25 live) | G08/A1–A12, G09/A1–A6, G34/A1–A4 | proposed |
| D8 | The customer approves what is filed; changes after approval must be re-approved | Summary rendered by the server from draft version *n*; confirm binds `(draft_id, version, summary_hash)`; any later draft change makes the confirmation stale (409); the draft locks after confirm | Approval is bound to material details; the model's text is never the thing approved | One more screen than "the agent files it for you" | G08/A2, G11/A1, G11/A3, G11/A5 | proposed |
| D9 | GDPR minimisation, EU residency, no content in telemetry | Collect only the FNOL fields (Q8); telemetry with content capture off and IDs only; Model Armor (EU) on customer text and model replies, fail closed; sessions and drafts deleted 30 days after submission or abandonment, original photos 30 days after confirmed transfer; erasure endpoint for the DPO process | Each sink has a known policy before the first shared deployment | Fail-closed screening sends customers to the form during a screening outage; Model Armor EU availability **unverified** (G12/A2) | G12/A1–A5, G33/A1–A3 | proposed |
| D10 | Completeness must be reliable and not depend on model judgment | A Pydantic `ClaimDraft` with enums for cause of loss and room types (from G01/A3); code computes missing required fields and injects them into state each turn; `update_claim_draft` validates and returns actionable errors; the model never sets "complete" | The application already knows the rules; the prompt only asks for what code says is missing | Less freedom for the model to restructure the interview | G02/A4, G06/A4 | proposed |
| D11 | Turns must be screened before the customer sees them | **Completed-JSON turns, no token streaming**; the UI shows a progress state; stable client message IDs and turn IDs; reconnect fetches the turn result | Output screening before release; simpler failure states | Slower perceived first output than streaming | G10/A3, T1 via G20/A1 | proposed |
| D12 | Customers see what happened, not what the model said happened | Status page and claim number read only from the operation record; summary from the draft record | Avoids "your claim is filed" from a model before it is | — | G11/A2 | proposed |
| D13 | Storm peaks and spend must not break the service or the budget | Per-invocation `max_llm_calls` (8) and per-draft allowance (60 model calls, stored in Cloud SQL); global admission by Cloud Run max instances and concurrency plus a token-bucket on new drafts; operator kill switch independent of the agent; on exhaustion, quota errors or kill switch, customers continue in the **classic form prefilled from the draft** | FNOL stays available when the agent is not; spend is bounded per claim | Customers in a surge may get the form; the form needs a prefill change | G18/A1–A5, G20/A1 | provisional (Q6, Q13) |
| D14 | Incidents must lead to a session; SLIs tied to I1–I4 | OpenTelemetry to Cloud Trace/Logging/Monitoring; one telemetry owner per process; session, invocation, draft and operation IDs on every span; SLIs: confirmed→filed ratio, confirm→claim-number latency, turn latency, tool error rate by tool, tokens per filed claim, uncertain operations older than 15 min | Settled before the first shared deployment | Content-free traces make some debugging slower | G17/A1, G17/A3, G35/A1–A2 | proposed |
| D15 | Prompt, model, tool schema and image move together | Release manifest (image digest, prompt version, model and judge IDs, tool-schema hash, eval-set hash, secret versions); CI gate fails by exit code; canary 5 % → 50 % → 100 % with thresholds set before traffic moves; previous revision kept ready 7 days | Rollback restores a tested combination | Slower releases | G19/A1–A4 | proposed |
| D16 | EU AI Act transparency, GDPR, human alternative | AI disclosure at the start (static text), "talk to a person" at every turn, safety guidance from static text, DPIA before real data, AI Act classification memo for legal | Transparency and a human route are cheap and expected | — | G06/A2, G06/A6, G13/A1–A3 | provisional (Q12) |

**Versions.** No ADK version is installed. Working assumption: `google-adk==2.8.0`,
the version every specialist's `references/compatibility.md` was checked
against (main branch 2.11.0 noted there). G02/A6 confirms the chosen pin and
the model's EU availability from official documentation and records source
and date. Provider facts still to verify: Guidewire Cloud API endpoints,
dedup header and limits (G01, G25); Vertex model and Model Armor EU regional
availability (G02/A6, G12/A2); Cloud Run, Cloud SQL and Cloud Tasks in
`europe-west3` (G16/A1). No network lookup was possible for this draft.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions and routing | One agent, no sub-agents. Instruction owns: interview for missing fields in the customer's language, describe what the photos show only to ask better questions, never discuss coverage, amounts or liability, offer a person. Code owns: identity, policy, missing-field list (templated from state), disclosure text, safety text, completeness | `adk-agent-instructions`; rendered-request test G06/A1 |
| Tool interfaces | Four function tools, all write-own-draft or read-own-draft tier: `update_claim_draft(fields)`, `get_draft_status()`, `record_safety_concern(kind)`, `request_human(reason)`. No IDs in arguments. Results are bounded dicts with `status` and actionable errors | `adk-tool-interface-design`; declaration dump and size G06/A1, tool list assertion G14/A1 |
| Output contract and model | Free text reply plus tool calls; no `output_schema` on the conversational agent (tools carry the structure). Pinned `gemini-3.8-flash`; thinking level low (to measure in G23); no automatic failover to a non-EU endpoint | `adk-model-and-output-contracts`; scripted invalid-output test G02/A5 |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| ADK session events | Customer (`user_id` = verified `sub`) | Runner / Runner, status API | Cloud SQL | 30 days after submit or abandonment; erasure G12/A4, G33/A3 |
| Claim draft (versioned) | Customer | `update_claim_draft`, UI edits / summary, worker | Cloud SQL; authoritative before submit | As sessions |
| Selected policy summary | Customer, derived from verified identity | Policy lookup code / agent state | Guidewire policy search at selection and again before create | Not stored beyond the draft |
| Photo originals and derivatives | Customer and draft | Browser (signed URL), processor / worker, model (derivative) | GCS EU bucket | Originals 30 days after confirmed transfer (G33/A1); derivatives with the draft |
| Submission operation | Service; readable by the owning customer | Confirm endpoint, worker / status API, ops | Cloud SQL; authoritative for "what we did" | Minimal row (IDs, claim number, states) kept 2 years for reconciliation; payload deleted with the draft |
| Claim and documents in ClaimCenter | Insurer | Worker / claims handlers | Guidewire; authoritative after submit | Insurer retention policy, outside this service |
| Allowances and kill switch | Service operators | Admission code / ops console | Cloud SQL / config | Rolling |
| Guidewire client secret | Platform team | Secret Manager / service account | Secret Manager, rotated | Rotation G37/A1 |

Identities: **customer** (OIDC `sub`, verified in middleware), **workload**
(Cloud Run service account; separate deployer identity), **Guidewire
client** (OAuth client credentials, service-wide; customer authority enforced
by D6). Session ID locates a conversation; it is never permission.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| intake (`LlmAgent`) | Customer's policy summary and draft | Customer text, photos (may contain printed text) | Writes only the customer's own draft; no egress | Write leg restricted to own draft and gated by the customer's confirmation of a server-rendered summary; external write in code (D1). Adversarial suite G14/A2 |

Tool tiers: read own draft (`get_draft_status`), write own draft (the other
three); no irreversible tool. No code executor. Threat model, OWASP mapping
and adversarial suite: G14; independent review: G15, G26; external pen test:
W3 and G21.

## Budgets and capacity

Workload (Q6): ~2,000 claims/month ≈ 100 per working day; storm peak ~1,000
per day, with an hourly peak of perhaps 150 claims and ~1,500 turns per hour
(assumption). Per claim (assumption to measure in G20): 8–14 turns, 1–2 model
calls per turn, ≤ 60 model calls by allowance; input grows with history to
roughly 150–250k input tokens and ~5k output tokens per claim, plus 1–2 Model
Armor calls per turn. Concurrency ≈ arrival rate × time in flight: at 1,500
turns/hour and ~6 s per turn about 3 concurrent turns on average; size
Cloud Run for 10× that with a cap (G18/A2).

Cost per claim (symbolic, prices unverified as of 2026-10-15): `Σ_calls
(in_tokens × p_in + out_tokens × p_out) + screening_calls × p_screen +
Cloud Run, SQL and storage share`. G20/A1 measures token counts and computes
the figure with dated prices for approval before GA. Billing budget alerts
notify only; enforcement is the per-draft allowance and the daily token
ceiling in G18.

Deadlines: one turn ≤ 20 s total (model 15 s, screening 2 s each side);
Guidewire calls 10 s each with the operation retrying for up to 24 h before
`needs_ops`. One retry owner: the application's Guidewire client (SDK
retries off) and ADK's model retry options set once (G18/A4).

## Failure and recovery

Coverage grid, one row per external system:

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Customer identity provider (OIDC) | G03/A7 | G03/A3 | n/a: read only verification | n/a: single verification step | G03/A3, G39/A2 | n/a: local token verification | G03/A5 | G03/A6 |
| Vertex AI Gemini | G18/A4 | G02/A5 | n/a: model call has no effect | G02/A3 | G16/A5 | G18/A4 | G03/A5 | G02/A5 |
| Model Armor screening | G12/A2 | G12/A2 | n/a: inspection only, no effect | n/a: single inspection call | G16/A5 | G12/A2 | n/a: stateless inspection call | G12/A6 |
| Guidewire policy search | G04/A3 | G04/A7 | n/a: read only lookup | n/a: read only lookup | G04/A5 | G04/A3 | n/a: idempotent read only | G04/A6 |
| Guidewire claim create and submit | G08/A5 | G08/A6 | G08/A4 | G08/A5 | G08/A10 | G08/A9 | G08/A3 | G08/A11 |
| Guidewire documents | G09/A2 | G09/A4 | G09/A3 | G09/A2 | G09/A6 | G09/A6 | G09/A3 | G09/A3 |
| Cloud SQL | G20/A4 | G08/A3 | G20/A4 | G08/A1 | G16/A5 | G20/A1 | G08/A8 | n/a: own schema-validated rows |
| Cloud Storage (photos) | G05/A7 | G05/A2 | G05/A5 | G05/A7 | G05/A7 | n/a: low per-object write rate | G05/A5 | G05/A6 |
| Cloud Tasks | G08/A12 | G08/A12 | G08/A12 | G08/A12 | G16/A5 | G20/A1 | G08/A8 | G08/A13 |
| Secret Manager | G16/A6 | G16/A2 | n/a: read only access | n/a: read only access | G37/A1 | n/a: secrets cached per instance | n/a: read only access | n/a: platform-managed secret values |
| Portal and browser (ingress) | G10/A3 | n/a: browser is the caller | G10/A3 | G05/A7 | G03/A3 | G18/A1 | G11/A4 | G14/A3 |

Action grid, one row per action that changes something:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Update claim draft (agent tool) | G03/A4 | G02/A3 | G08/A14 | G02/A7 | G03/A5 |
| File claim in ClaimCenter | G08/A7 | G08/A5 | G08/A2 | G08/A4 | G08/A3 |
| Attach photos to the claim | G09/A5 | G09/A2 | G11/A5 | G09/A3 | G09/A3 |
| Erase a customer's data | G12/A4 | G33/A4 | G33/A2 | G33/A4 | G33/A2 |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Claim created, response lost, worker restarts | "We received your claim; the number will appear here shortly" | Operation `create_unknown`; claim may exist | Worker looks up by our reference, then continues; ops after 24 h (G08/A4, G35/A2 runbook) |
| Claim submitted, 3 of 10 photos fail | Claim number and "7 of 10 photos attached, retrying" | Claim exists; per-photo states | Worker retries; rejected photos: customer told to send another way (G09/A2, G09/A4) |
| Policy cancelled between confirm and create | "We could not file this online; please call" with draft kept | No claim | Customer calls; claims ops (G08/A7) |
| Model or screening unavailable mid-conversation | "Continue in the form" with fields prefilled | Draft kept | Customer continues in form; on-call checks quota (G18/A4, G12/A2) |
| Storm surge exceeds admission | New customers get the prefilled form; current drafts continue within allowance | Drafts kept | Ops may flip kill switch (G18/A3, G20/A1) |
| Erasure requested while a submission is pending | Erasure confirmed after filing completes | Claim in ClaimCenter follows insurer retention | Erasure job waits for terminal state (G33/A2) |
| Injected text in a photo tries to change the policy or file the claim | Nothing changes beyond proposed draft fields shown in the summary | No claim without confirm | Adversarial suite (G14/A2) |
| Model retires mid-release | No change to customers | Pinned ID | Planned re-baseline as its own release (later list, G19 manifest) |
| Bad release | Canary thresholds trip, traffic returns to previous revision | Sessions compatible across one version (G19/A4) | Release owner (G19/A3) |
| Incident without telemetry | — | Spans carry session and operation IDs from the first shared deployment | On-call (G17/A1, G35/A2) |

## Verification and implementation handoff

Verification ladder (all **planned**; nothing has run):

- **Offline deterministic:** scripted-model Runner tests and a Guidewire fake
  (G01/A2) for G02–G09, G14, G18, G33 and G34; these do not need cloud access.
- **Local integration:** Postgres container restart (G02/A7), worker restart
  and concurrent tasks (G08/A8), signed-URL flow against a local emulator or
  staging bucket (G05).
- **Bounded live:** Vertex calls for G06, G07 and G23 under the €3,000/month
  non-prod cap; Guidewire non-prod contract checks in G25 after W1.
- **Release and operation:** staging load and resilience (G20), external pen
  test (W3, G21), UAT with claims handlers (G24), canary in production (G22).

Benefit measurement: G24 sets the completeness baseline from current web-form
claims; after GA, the share of claims needing a call-back for missing facts
is tracked in G17's dashboard as a business metric separate from model
quality (T3) and technical success (I3, I4).

Observability and release: SLIs and alert owners in G17; release bundle,
promotion gate and rollback in G19; previous revision kept ready 7 days (D15).

Implementation map, goals, estimates and the next prompt: see the
[plan](../plans/home-claim-intake.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Q1–Q14 assumed answers | Each changes the decisions listed against it | Product owner confirms or corrects | Nothing local; changes re-plan |
| Guidewire dedup header and reference lookup semantics | D7 relies on one of them for I3 | G01 from docs, G25 live | G08 final acceptance |
| `gemini-3.8-flash` and Model Armor available in an EU region | D3, D9 residency | G02/A6, G12/A2 | Staging deployment of the model path |
| Classic form can accept a prefilled draft | D13 fallback | Portal team (wait W10, requested day 1) | G18/A3, G10/A4 |
| AI Act classification (Q12) | A high-risk classification adds conformity work well beyond 5 months | Legal, from G13/A3 (wait W18) | GA date |
| GA date versus the plan's high-end finish | After the independent review the plan finishes in 67–102 working days against 95; GA on 2027-03-25 (103 working days) fits | Product owner | G22 date |
| Accept residual risks R1–R3 | Floor and liability | Claims product owner | GA sign-off W6 |
