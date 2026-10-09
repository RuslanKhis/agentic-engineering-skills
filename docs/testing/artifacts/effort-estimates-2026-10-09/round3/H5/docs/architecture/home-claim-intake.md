# System design: home-insurance claim intake agent (FNOL with photos → Guidewire ClaimCenter)

Status: **draft**. Written in one pass without the user; every row of the
Assumed answers table below is unconfirmed, and the decisions that depend on
them are marked *provisional*. No decision here is user-accepted yet.
Plan: [docs/plans/home-claim-intake.md](../plans/home-claim-intake.md).
Tickets: [docs/tickets/home-claim-intake/](../tickets/home-claim-intake/).

## Purpose and constraints

**Running journey.** Maria, a home-insurance customer in Germany, finds water
coming through her kitchen ceiling on a Sunday evening. Today she phones the
claims hotline or fills a long web form, then emails photos separately; a
claims handler re-keys the notice into Guidewire ClaimCenter on Monday, and
often calls her back for missing facts (date, cause, rooms, emergency steps
taken). With this system she signs in to the existing customer portal, opens
"Report damage", describes what happened in her own words, uploads six photos,
answers two or three follow-up questions, reviews a structured summary that the
application renders from the claim draft, and presses **Submit claim**. She
sees a submission reference immediately and the ClaimCenter claim number once
the claim exists; the handler receives a complete first notice of loss (FNOL)
with photos attached.

**Outcome to improve** (hypotheses until measured; baselines come from claims
operations, see O3):
- share of digital home FNOLs that a handler accepts without a call-back for
  missing facts (target: higher than the current web form);
- time from first contact to claim number in ClaimCenter;
- guardrail: handler correction effort and customer complaints must not rise.

**Non-goals.** The agent does not decide or hint at coverage, liability,
reserves or payout; does not estimate repair cost; does not detect fraud
(ClaimCenter's existing rules do); does not update or close existing claims;
does not handle motor, liability or contents-only products at GA.

**What the model contributes:** understanding free-text descriptions, asking
for missing facts in natural language, mapping the story to claim fields
(loss cause, date, affected rooms, mitigation), and describing visible damage
in photos as *suggestions*. **What ordinary code controls:** who the customer
is, which policies are theirs, required-field validation, the confirmation
screen, the claim payload, the Guidewire write, idempotency, retries,
retention and every budget.

Observed repository facts: the repository contains only `.claude/skills/`; there
is no application code, manifest or document convention, so this is a
greenfield design and every module path below is **proposed**.

## Assumed answers

The user was not available. Each row is the question I would have asked, the
answer assumed, and what depends on it.

| # | Question | Assumed answer | Decisions that depend on it (provisional) |
| --- | --- | --- | --- |
| A1 | When is GA, and is the system continued after it? | GA on 2027-03-09 (five months from 2026-10-09); continued and operated by this team | Phase dates, D11 |
| A2 | Hours and familiarity of the team? | Five full-time engineers and one full-time ML engineer, experienced in Python and GCP, **new to ADK**; security reviewer about 40% (two days a week); focus factor 0.6 | Capacity, ×1.5 estimate multiplier |
| A3 | Model and cloud budget? | ≤ €1,500/month during phase 1, ≤ €6,000/month at GA volume (including evaluation runs) | D9 model tier, D10 budgets |
| A4 | Who uses it and who judges it? | Retail home policyholders, signed in to the existing customer portal (web and mobile web); claims handlers read the resulting ClaimCenter claim; claims leadership judges the pilot | D1, D4, pilot goal |
| A5 | What data, what effects? | Personal data, photos of homes (may show people or documents), free text that may contain health data (injury, GDPR Art. 9). One effect: create an FNOL claim with documents in ClaimCenter. No payments, no coverage decisions | Floor, D6, D7, D8 |
| A6 | Which Guidewire product and interface? | ClaimCenter on Guidewire Cloud with the Cloud API (REST, OAuth 2 client credentials via Guidewire Hub) and a sandbox tenant; policy lookup through the PolicyCenter/Policy API or an existing policy service | D5, G01 discovery |
| A7 | Markets and languages at GA? | Germany only, German and English | Evaluation set, instructions; more markets are "later" |
| A8 | Existing customer identity? | The portal's customer IAM issues OIDC tokens our API can verify; it already maps login to a policyholder ID | D2 |
| A9 | Frontend? | A chat widget added to the existing portal; native app later | D4 |
| A10 | Volume? | ~1,500 digital home FNOLs/month at GA; storm events produce 10× daily peaks | D10, G19, G20 |
| A11 | Data residency? | All processing and storage in the EU; model inference on a regional EU Vertex AI endpoint, not the global endpoint | D9, G02 |
| A12 | Retention? | Transcripts 90 days after submission; abandoned drafts 30 days; our photo copies deleted 30 days after ClaimCenter confirms the documents; ClaimCenter is the record of the claim | D8 |
| A13 | May the agent give coverage guidance? | No; it says a handler will assess cover | Instruction contract, eval case class |
| A14 | Who resolves a submission whose outcome is uncertain? | Claims operations, through a reconciliation queue, within one business day | D5, failure table |
| A15 | Availability target? | 99.5% monthly for chat and submission acceptance; when unavailable the portal links to the existing web form and hotline | SLOs, D10 |
| A16 | GCP environment? | Existing organisation; the platform team creates EU projects and IAM through Terraform on request (days) | G10 wait |
| A17 | Emergencies (ongoing flood, gas, fire)? | A static emergency banner with the hotline is always shown by the page; the agent repeats it when it recognises danger; no triage | Instruction contract |
| A18 | Delivery profile and cut line acceptable? | Production; cut line as in "Capacity and cut line" | Whole plan |

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | Internal end-to-end on Guidewire sandbox by 2026-11-20 (phase 1); closed pilot with real customers from late January 2027; GA 2027-03-09; continued (A1) |
| People and hours | 5 engineers + 1 ML engineer full time, security reviewer ~40%; experienced Python/GCP, new to ADK (A2); the team runs it after GA with claims-IT on-call |
| Money | A3 (assumed) |
| Users or judge, and what they read | External policyholders use the running service; handlers read ClaimCenter claims; claims leadership reads the pilot report (A4) |
| Data touched and effects allowed | Personal and possibly special-category data; one consequential write (FNOL claim + documents) after explicit customer confirmation (A5) |
| Delivery profile | **Production service**: external customers, regulated personal data and a write into the system of record. Phase 1 is an internal, staging-only slice of that production design |

Depth per concern:

| Concern | Depth now (phase 1) | At GA (phase 2) | Trigger that raises it further |
| --- | --- | --- | --- |
| Core judgment, measured | Build: labelled eval set and baseline (G07) | Gated evaluation in CI (G17), pilot error analysis (G22) | A new market or language |
| Identity and per-customer scope | Build on staging IAM (G03) | Production customer IAM (G15) | Brokers or agents filing for customers |
| Secrets and credentials | Build: workload identity, Secret Manager, worker-only Guidewire credential (G06, G10) | Build with rotation | — |
| External write | Build: durable submission ledger, idempotent steps, reconciliation (G06) | Production connection and ops queue (G14) | A second write (claim updates) |
| Sensitive data | Build: data map, content capture off, DPIA submitted (G09) | Screening, retention and erasure jobs (G16) | Special-category data found in pilot samples above expectation |
| Prompt injection and agency | Build: structural split (D6), adversarial suite (G08), security review (G13) | External penetration test (G23) | Any new tool with write or egress |
| Budgets and loop limits | Build: `max_llm_calls`, per-session and per-customer limits (G03, G08) | Surge admission and degrade-to-form (G19) | Storm-season traffic measurements |
| Memory and retrieval | Sessions and the claim draft only; no cross-session memory, no RAG | Same | Customers asking policy questions the draft cannot answer |
| Frontend | Build: portal widget on staging (G11) | Accessibility and mobile polish (G25) | Native app |
| Hosting | Build: staging Cloud Run in EU (G10) | Production with rollback and DR rehearsal (G24) | Multi-region requirement |
| Observability | Build: traces, token cost, no content (G10) | SLOs, alerts, runbook (G18) | — |
| Release engineering | Minimal: pinned model, manifest, deterministic CI (G10) | Eval gate, canary, joint rollback (G17) | Model retirement notice |
| Performance and cost tuning | Defer | Load and cost test at storm peak (G20) | Measured p95 or cost per claim over target |

**Floor kept from day one:** no secrets in code, prompts, logs or documents;
`RunConfig.max_llm_calls` on every invocation plus a project budget alert;
nothing reaches ClaimCenter without the customer pressing Submit on a
code-rendered summary; phase 1 uses synthetic customers and the Guidewire
sandbox only, no real customer data; model ID pinned. No risks are accepted on
the user's behalf.

**Who may use it now:** phase 1 — team members on staging, synthetic data,
Guidewire sandbox. **Graduation conditions before real customers (pilot):**
DPIA signed off (wait on G21); production Guidewire connection with
reconciliation runbook (G14); production customer IAM with cross-customer
denial tests (G15); screening, retention and erasure in place (G16); eval gate
in CI and joint rollback (G17); SLOs and alerts (G18); security review findings
closed (G13). **Before GA:** pilot go/no-go, penetration test sign-off (G23),
surge controls and load test (G19, G20), DR and rollback rehearsal (G24).

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Model Armor / SDP screening at ingress | Phase 1 has no real data; structural split (D6) already removes the write leg from the model | Any real customer data (pilot) — scheduled as G16 |
| Load and cost tuning | No traffic measurements yet | G20, or p95 > target in the pilot |
| Multi-region failover | 99.5% target met by one EU region plus fallback to the web form (A15) | Availability target raised |
| Cross-session memory | The journey is one claim per session | Customers resuming across devices at scale |

**Capacity and cut line** (figures from the plan's schedule check): phase 1 is
G01–G13, an internal staging end to end; phase 2 is G14–G25, pilot and GA. See
[plan, delivery profile and capacity](../plans/home-claim-intake.md#delivery-profile-and-capacity).

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer sees and acts only on their own sessions, drafts, photos, policies and submissions | Chat API middleware verifies the OIDC token, derives `customer_id`; every repository query is keyed by it; session/draft rows carry `customer_id` | 404 for another customer's IDs; nothing disclosed to the model | Cross-customer denial tests per route (G03, G15); adversarial case "use policy P-of-someone-else" (G08) |
| I2 One confirmed submission creates at most one ClaimCenter claim, with each photo attached once | Submission worker with a durable ledger (`submission_id` unique per frozen draft) and per-step idempotency keys; Guidewire replay contract confirmed in G01 | Uncertain outcome → status `needs_reconciliation`, never a blind re-create | Fake-Guidewire tests: lost response, timeout, worker restart, duplicate click (G06); sandbox replay check (G12) |
| I3 Nothing is written to ClaimCenter without the customer confirming exactly the summary that is sent | Confirmation endpoint freezes the draft and stores its hash; the worker sends the payload built from that frozen version only | Draft edited after confirmation → new confirmation required | Test: edit-after-confirm is rejected; payload hash equals confirmed hash (G06) |
| I4 The model cannot cause a ClaimCenter write or read another customer's data | The intake agent has no Guidewire credential or tool; its tools write only the session's own draft (`before_tool_callback` checks trusted state) | A hostile instruction in text or photo changes, at most, the customer's own draft, which they review | Scripted-model adversarial suite asserting no forbidden call or disclosure (G08) |
| I5 The agent makes no coverage, liability or payout statement | Instruction contract + eval case class; the summary is rendered by code | Statement in streamed text is an accepted residual risk (cannot be retracted), measured | Eval metric "coverage-promise rate" = 0 on the dev set; pilot sampling (G07, G21) |
| I6 Content does not reach logs or telemetry | ADK/OTel content capture disabled; structured logs carry IDs only | — | Exporter test shows no prompt/response content (G10) |
| I7 Bounded work per turn and per customer | `RunConfig.max_llm_calls`, per-session turn and photo limits, per-customer daily session limit | Friendly stop, draft kept, link to web form | Offline limit tests (G03, G08) |
| T1 Time to first token p95 ≤ 3 s, complete turn p95 ≤ 12 s (provisional) | Measured in staging and pilot | — | G20 load test; pilot telemetry |
| T2 Draft completeness: ≥ 90% of confirmed drafts have all handler-required fields (provisional) | Required-field validator in code | Customer is asked for the missing field | Eval set (G07) |

## Architecture and decisions

```text
 Browser (customer portal, chat widget)
   │  OIDC token (customer IAM)                       trust boundary ─────────────
   ▼
 chat-api  (Cloud Run, europe-west3, SA: chat-api@)
   ├─ auth middleware: verify token → customer_id (trusted)
   ├─ policy lookup (code, read-only Policy API) → state: eligible home policies
   ├─ upload endpoint → signed URL → GCS bucket claims-photos-eu (CMEK)
   ├─ photo-analysis call (model, output_schema, NO tools) → draft.suggestions
   ├─ ADK Runner(App: intake_agent)  ── Vertex AI Gemini (EU regional endpoint)
   │     tools: update_claim_draft, select_policy, request_photo   (draft-only)
   ├─ confirm endpoint: freeze draft version + hash → submissions ledger → Cloud Tasks
   └─ status endpoint: ledger status (owner-checked)
 Cloud SQL Postgres (EU): ADK sessions, claim_drafts, submissions, submission_steps
 Cloud Tasks queue (EU) ──► submission-worker (Cloud Run, SA: claim-writer@)
                                ├─ Guidewire OAuth client secret (Secret Manager; this SA only)
                                └─ ClaimCenter Cloud API: create claim → upload documents → submit
                                   reconcile by external reference on uncertainty
```

Sequence of the running journey: Maria's message → `chat-api` verifies her
token → loads her two policies (home, contents) into session state → agent
asks which address → `select_policy(policy_ref)` validated against state →
photos uploaded to GCS, analysed into suggestions ("ceiling stain, water
damage, kitchen") → agent asks date and whether the water is stopped →
validator reports the draft complete → page renders the summary from the draft
(not model text) → Submit → ledger row `ACCEPTED` and task enqueued in one
transaction → worker creates the ClaimCenter claim, uploads six documents,
submits → ledger `COMPLETED` with claim number → widget shows it.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Language understanding over a small, fixed capability set (A4, A5) | **One `LlmAgent`** (intake) plus one tool-less structured photo-analysis call; ordinary code for everything deterministic | Fields and ordering are known; one agent with three narrow tools is enough | Multi-agent routing rejected: no distinct responsibility or credential; a sequential workflow rejected because customers tell the story in any order | Selection accuracy and field accuracy on eval set (G07) | proposed |
| D2 | I1 (A8) | `customer_id` derived from the verified OIDC subject in `chat-api` middleware, stored in session state under an app-owned key, passed to tools as trusted context; never a model argument | Identity is known by code; a session ID is a locator, not permission | Requires every route and repository to take `customer_id` | Cross-customer denial tests (G03) | provisional (A8) |
| D3 | Survive restarts and multiple replicas | ADK `DatabaseSessionService` on Cloud SQL Postgres for sessions; app-owned `claim_drafts` table is the authoritative draft, session state holds only `draft_id` | The draft must outlive chat history and be read by the confirmation page | Postgres to operate vs. Firestore; one store for sessions, drafts and ledger allows the confirm transaction | Restart test resumes the draft (G03) | proposed |
| D4 | Browser experience in the existing portal (A9) | Custom JSON API with SSE for text deltas; tool activity shown as status chips; summary and submission status are application-owned JSON, not model text | Portal is not ours to replace; AG-UI adds a dependency the portal team must adopt | Custom contract to maintain | Browser test of streaming and summary rendering (G11) | provisional (A9) |
| D5 | I2, I3 (A6, A14) | **Durable submission ledger + Cloud Tasks worker**: confirm writes frozen draft hash and `submission_id` atomically, worker runs idempotent steps (create claim with external reference = `submission_id`, upload each document with its own key, submit), records receipts; uncertainty → reconcile by searching the external reference, else `needs_reconciliation` for claims ops | Claim creation plus N document uploads can partially fail and outlast a request; the customer must not resubmit | Asynchronous status UI; depends on Guidewire offering a replay header or a searchable external reference — **unverified, G01** | Fake-Guidewire failure matrix (G06); sandbox replay (G12) | provisional (A6) |
| D6 | I4: untrusted text/photos + private data + a write | **Structural split**: the model never holds the Guidewire write or credential; its tools write only its own draft; the write is a customer button executed by a separate worker identity | Removes the write leg from the agent; an injection can only alter the customer's own draft, which they review | One extra step (confirmation page) that is wanted anyway | Adversarial suite (G08), security review (G13) | proposed |
| D7 | Photos as evidence without bloating context | Photos go to GCS by signed URL (type, size, count limits, EXIF stripped); a separate `output_schema` call returns `{damage_types[], rooms[], visible_hazards[], quality_issue, refusal}` per photo; the conversational agent sees only these structured suggestions | Bounds tokens; makes photo quality separately measurable; image text can't instruct a tool-holding agent | One extra model call per photo batch | Schema tests with prose/fenced/invalid outputs (G05); photo labels in G07 | proposed |
| D8 | GDPR minimisation and retention (A11, A12) | All stores in EU region with retention jobs; content capture off in telemetry; eval data synthetic or redacted with SDP; DPIA before pilot | Personal and possibly special-category data | Less debugging content; redaction pipeline to build | Data map review and exporter test (G09, G10); erasure test (G16) | provisional (A11, A12) |
| D9 | Pinned, EU-resident, multimodal model | `gemini-3.8-flash` on Vertex AI, regional EU endpoint, for agent and photo call; same ID pinned as judge for tone-only checks; field accuracy is scored deterministically | From `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (checked_on 2026-10-08): stable, no shutdown announced; `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28) retire before GA; `gemini-3.5-flash` "2027-05-19 or later" is two months after GA | EU regional availability **unverified** (G02); same model as judge risks self-preference, so judge only scores tone | G02 confirms region; release manifest contains no alias | provisional (A11) |
| D10 | Spend and surge safety (A3, A10) | `max_llm_calls`=15 per invocation, 40 turns and 20 photos per session, 3 new claim sessions per customer per day, project budget alert; at GA an admission gate that degrades to the web form during storms | Floor plus storm peaks | Some legitimate long conversations stop early (draft kept) | Limit tests (G08); load test (G20) | provisional |
| D11 | Hosting | Two Cloud Run services (`chat-api`, `submission-worker`) in `europe-west3`, Cloud SQL, Cloud Tasks, GCS, Secret Manager | Custom gateway and worker with separate identities; team knows Cloud Run | Agent Runtime rejected for now: we need our own gateway, worker and EU region control; GKE: more operations than five people need | Staging deployment readback (G10) | provisional (A16) |
| D12 | ADK version | Working assumption **google-adk 2.8.0** (the version every installed specialist's `references/compatibility.md` records); confirming against the chosen pin is an acceptance item of G03 | No installed version exists | 2.10+ changes trace shape (observability compatibility notes) | G03 acceptance | proposed |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Intake agent: collect a home FNOL; ask one question at a time; never state cover, liability or payout; repeat the emergency hotline when danger is described; reply in the customer's language (de/en). Customer name, policies, date and limits come from state templating, not prose | `adk-agent-instructions`; rendered-request test |
| Tools | `select_policy(policy_ref)` (must be in trusted state list); `update_claim_draft(fields)` (typed: loss_date, cause enum, rooms, description, mitigation, third_party_involved); `request_photo(reason)`; all draft-tier writes on the caller's own draft; results `{status, missing_fields[], error}` ≤ 1 KB | `adk-tool-interface-design`; declaration dump and size |
| Output contract | Photo call: `output_schema` above with a `refusal` field (not a photo of damage / unreadable); max 1 repair attempt then "photo stored, no suggestion". Summary is code-rendered, no model output schema needed for chat | `adk-model-and-output-contracts`; scripted invalid-output test |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | Customer IAM | Middleware reads | Token per request | Not stored beyond `customer_id` |
| Eligible policies | PolicyCenter / policy API | Code reads at session start | Re-read at confirm (policy still active?) | Session only |
| ADK session events | `customer_id` | chat-api | — | 90 days after submission, 30 days if abandoned (A12) |
| Claim draft (versioned) | `customer_id` | Agent tools (draft fields), customer edits, confirm freezes | Authoritative until confirmed | As session |
| Photos | `customer_id`, `draft_id` | Upload endpoint writes; photo call and worker read | — | Deleted 30 days after ClaimCenter acknowledges each document |
| Submission ledger and steps | `customer_id`, `submission_id` | Confirm endpoint, worker | Receipts from ClaimCenter | 7 years? **open (O5)** — needed for audit |
| ClaimCenter claim | Insurer; ClaimCenter is system of record | Worker creates; handlers own afterwards | — | Insurer's records policy |

Identities: customer (OIDC), `chat-api@` workload (Vertex, Cloud SQL, GCS
write, Cloud Tasks enqueue; **no** Guidewire secret), `claim-writer@` workload
(Secret Manager Guidewire client secret, GCS read, Cloud SQL ledger), Guidewire
service client (scoped to FNOL creation and document upload, requested in G01).

### Security posture

| Agent / call | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Intake agent | Customer's own policies and draft | Customer text; photo suggestions (derived from images) | Draft-only tools on own draft | Write to ClaimCenter removed (D6); capability check in `before_tool_callback` keyed on trusted `customer_id`/`draft_id` |
| Photo analysis call | Photos | Image content, including text in images | None (no tools) | Reader without tools; schema-validated output |
| Submission worker | Frozen draft, photos | None model-generated beyond reviewed draft fields | ClaimCenter write | Not an agent; payload from frozen confirmed draft only |

Tool tiers: draft writes (no confirmation; customer reviews summary);
ClaimCenter write (irreversible-ish: customer confirmation in code, worker
identity only). No code executor. Adversarial cases (G08): instructions inside
a photo, "file this under policy X" for a foreign policy, request to reveal
another claim, request to skip confirmation, coverage-promise extraction,
loop/token exhaustion. Threats map to OWASP LLM01, LLM02, LLM06, LLM10.

## Budgets and capacity

Per claim session (assumption, to be measured in G07/G20): 8–14 agent turns,
≈ 1.3 model calls per turn, one photo call per batch of up to 6 photos,
≈ 6k input tokens per call with a stable instruction prefix. Expected ≈ 20
model calls per claim; bounded by D10 limits at ≤ 40 × 15 = 600 calls
(never expected; the per-customer daily limit caps abuse). Cost per claim is
symbolic until G02 records EU regional prices with a date; at A10 volume the
budget A3 is the ceiling the G20 test must show headroom against. Concurrency
at a storm peak: 10 × 1,500/30 ≈ 500 claims/day, peaking ≈ 60 concurrent
sessions; Vertex quota and Cloud SQL connections are the limits checked in G20.
Billing budgets alert only; admission is enforced by the application (G19).

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Token invalid or another customer's session ID | 401 / 404 | None | None (I1) |
| Model unavailable or quota exhausted | "Our assistant is unavailable; your draft is saved" + web form link | Draft and session | Retry later; on-call if SLO burns |
| Photo call returns prose or invalid JSON | Photo stored without suggestion | Photo | One repair attempt; counted metric |
| Browser disconnects mid-stream | Reopen shows the saved draft and last complete turn | Partial event not saved | Customer continues |
| Worker crashes after ClaimCenter created the claim, before the receipt | "Submitted — claim number coming" | Ledger `IN_PROGRESS`, step `create_claim` uncertain | Task retry searches by external reference first; found → record receipt; not found and replay contract unknown → `needs_reconciliation` for claims ops (A14) |
| Claim created, photo 4 upload fails repeatedly | Claim number shown, "one photo still transferring" | Claim exists; 5/6 documents | Worker retries document step with its own key; after bound → ops queue; claim not reported as "failed" |
| Guidewire down for hours (or maintenance) | "Received, reference SUB-…" | Ledger `ACCEPTED` | Cloud Tasks retry with backoff up to 24 h, then ops queue |
| Customer double-clicks Submit / two tabs | One submission | Unique constraint on frozen draft version | Second request returns the same `submission_id` |
| Policy lapsed between draft and confirm | Clear message, contact hotline | Draft | Code recheck at confirm |
| Hostile text in photo / message | No change beyond own draft | — | G08 tests |
| Erasure request during queued submission | Submission completes into ClaimCenter (lawful basis: claim); local copies deleted afterwards | Ledger keeps IDs | Erasure job waits for terminal state (G16) |
| Model retirement announced | None | — | Planned re-baseline release (G17) |
| Rollback | Previous revision serves; in-flight submissions continue (worker version-tolerant payload) | Ledger schema migrations backward-compatible | Release owner (G24) |

## Verification and implementation handoff

Planned (none executed yet): offline Runner tests with a scripted model and a
fake Guidewire (G03–G08); local integration with real Postgres and a real
process restart (G03, G06); bounded live checks against Vertex EU and the
Guidewire sandbox on staging (G02, G12); release evidence — eval gate, load
test, rollback and DR rehearsal, pen test — in phase 2.

Judged deliverable and regeneration rule: not applicable. This is a running
service, not an assignment whose output is judged; pilot quality evidence
comes from G21 and the eval gate from G17.

Observability and release: SLIs — chat turn success ratio, submission
completion within 15 minutes, reconciliation queue age, tool-error rate by
tool, tokens and cost per completed claim; content capture off; one telemetry
owner per service; `session_id`, `invocation_id`, `submission_id` on every
span and log. Release bundle: image digest, prompt version, model and judge
IDs, tool schema hash, eval-set hash, secret versions, recorded in a manifest
in the repository; rollback moves them together.

Implementation routes per decision are in the
[plan's implementation map](../plans/home-claim-intake.md#implementation-map).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| O1 Guidewire Cloud API: FNOL endpoints, replay header or searchable external reference, document upload limits | D5's at-most-once guarantee rests on it | G01 with claims IT; sandbox calls | G06 final shape (fake adapter can start) |
| O2 Gemini 3.8 Flash available on a regional EU Vertex endpoint with enough quota; Model Armor and SDP EU regions | D9, D8 residency | G02 | G05/G07 live runs |
| O3 Baseline metrics for digital FNOL call-backs and time-to-claim | Benefit claims are hypotheses without it | Claims operations | Pilot success criteria (G21) |
| O4 EU AI Act: confirm the intake chatbot is not high-risk and the Art. 50 AI-interaction disclosure wording | Disclosure text and documentation | Legal / DPO | G11 copy, G21 |
| O5 Retention of the submission ledger and transcripts | Erasure jobs, audit | DPO, claims compliance | G16 |
| O6 All A1–A18 assumptions | See table | User | Marked provisional |
