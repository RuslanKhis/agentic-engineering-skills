# System design: home-insurance claim filing agent

Status: **draft**. Written 2026-10-09 in a one-pass session without the
product owner. Every answer the user did not give is in the **Assumed
answers** table below. The decisions that depend on those answers are marked
*provisional*. No decision here has been accepted by the user yet.

Plan: [docs/plans/home-claim-agent.md](../plans/home-claim-agent.md).
Tickets: [docs/tickets/home-claim-agent/](../tickets/home-claim-agent/).

## Assumed answers

The user was not available. These answers stand in for the scope-gate and
architecture questions. Change one and the dependent decisions must be
reviewed.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | GA date, launch market and languages | GA about 2027-03-12 (five months from 2026-10-12). Launch in **one EU country**, in its official language plus English. | D1, D13, plan phases, G30 |
| A2 | Which Guidewire, and which version? | **Guidewire Cloud Platform ClaimCenter** with Cloud API (REST, OAuth2 client credentials through Guidewire Hub), Homeowners line of business. Version, endpoint and idempotency semantics are unverified. | D3, D6, I2, G01, G09/G10 |
| A3 | Customer login | An existing customer portal with OIDC sign-in (CIAM), plus an authoritative customer→policy lookup. | D5, I1, G04 |
| A4 | Existing channels | A standard web claim form and a 24-hour phone line already exist and stay available. They are the fallback. | D11, I9 |
| A5 | Team and familiarity | 5 full-time engineers, experienced with Python and GCP but **new to ADK**; 1 ML engineer; 1 security reviewer at about 40 %. Focused hours: 5 h/day each, 2 h/day for the reviewer. | Estimates (×1.5 ADK multiplier), plan capacity |
| A6 | Model and cloud budget | Phase 1 at most about €2,000/month across dev and staging. At GA a monthly cap the business sets, illustratively €15,000. **Unconfirmed.** | D7, D11 |
| A7 | Volume | About 60,000 home claims a year in the launch market; 30 % filed through the agent after a year; storms bring 10× spikes over a day. **Illustrative.** | Budgets and capacity, G27 |
| A8 | Agent scope | **First notice of loss (FNOL) intake only.** The agent does not decide coverage or liability, does not estimate cost and does not collect bank details. | D2, I5, security posture |
| A9 | Who may file | Only the authenticated policyholder files, for their own policy. No brokers, no third-party claimants. | D5, I1 |
| A10 | Data residency and keys | All customer content (inference, storage, logs, backups) stays in the EU. Google-managed encryption keys, unless the security policy requires CMEK. | D7, D8, I7 |
| A11 | Retention | Abandoned drafts and their photos are deleted after 30 days. After submission our copy of the photos is deleted 7 days after Guidewire confirms the attachment. The conversation is kept 30 days after submission for support, then deleted. Guidewire's own retention governs the claim. | D8, I10, G13 |
| A12 | DPIA and legal | A DPIA is needed and the DPO's sign-off takes 4 to 6 weeks. The EU AI Act transparency duty (telling the customer it is an AI) applies. Home-claims intake is assumed **not** high-risk under Annex III; legal must confirm. | G21, D12, phase 2 gate |
| A13 | Historical claim photos for evaluation | Not used until the DPIA permits it. Phase 1 evaluates on licensed, synthetic and staff-staged photos. | G06, G08 |
| A14 | GCP region and landing zone | A GCP organisation with a landing zone exists and Cloud Run is permitted. `europe-west4` is the provisional region, to be confirmed against model availability. | D6, D7, G02 |
| A15 | Claim follow-ups in chat (add photos later, check status) | Out of scope for GA; on the Later list. | Scope |
| A16 | Delivery profile and cut line | Production. Phase 1 (60 working days) ends with an internal staff pilot on staging plus a dark production Guidewire connection. Phase 2 (40 working days) ends at GA. | Plan |

## Purpose and constraints

**Journey (running example).** Anna's kitchen ceiling is dripping after a pipe
burst upstairs at 07:30. Today she signs into the portal, finds the claim form,
types a free-text description, is asked for policy and contact data the
company already holds, and cannot attach more than two photos. A third of
such claims need an adjuster call-back for missing facts (*hypothesis,
baseline to be measured*). With the agent, Anna signs in and says "water is
coming through my kitchen ceiling". The agent first checks she is safe and
whether the water is off, and gives the 24-hour line if not. It confirms which
of her policies applies, asks only for missing facts (when, cause, rooms, what
she has done to stop the damage), takes up to ten photos and describes what they
show for her to correct. It then displays a summary. When she presses
**Confirm and file**, the claim is created in Guidewire ClaimCenter and she
sees the claim number. If the agent is unavailable, she is shown the standard
form.

**Fixed constraints.** EU GA in five months; personal data of external
customers; one irreversible, outside-visible effect (a claim in the system of
record, which starts adjuster work and customer correspondence); Guidewire
ClaimCenter is the authority for claims, and the policy system is the
authority for policies and coverage.

**What the model contributes:** interpreting Anna's language, asking for
missing facts, describing photos, writing the loss description. **What code
controls:** who Anna is and which policies are hers, the draft record and its
versions, validation of required fields, the confirmation binding, the
submission, retries, budgets, retention, and every statement of claim status.

**Outcome to improve (hypothesis).** A higher share of claims filed digitally
end to end, and fewer adjuster call-backs for missing information, without a
higher correction rate by adjusters. The baseline comes from today's form and
the claims data (G24 measures; phase 2 pilot G31 compares).

**Non-goals for GA:** coverage or liability decisions, damage cost estimation,
payouts and bank details, motor or other lines, brokers and third parties,
updates to an existing claim, voice.

Repository facts: the repository is empty apart from the skills (one commit,
`be513ae fixture`). Everything below is proposed, not observed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | GA in the EU about 2027-03-12 (A1); launched and continued |
| People and hours | 5 engineers and 1 ML engineer full time, focused 5 h/day; security reviewer about 40 %, 2 h/day; new to ADK, familiar with GCP (A5). The team runs it after GA together with claims operations |
| Money | Phase 1 about €2k/month; GA cap set by the business (A6, unconfirmed) |
| Users or judge, and what they read | External customers (policyholders), who use the running service; claims adjusters, who read the claims it creates; the DPO, security and legal, who read this design and the DPIA |
| Data touched and effects allowed | Personal data: name, address, policy, contact details, photos of the home that may show people and documents. It creates claims in the system of record: irreversible and visible to the customer and the claims team |
| Delivery profile | **Production service**: external customers, personal data and an irreversible write into the system of record. Phase 1 reaches staging and a staff pilot; phase 2 graduates to GA |

Depth per concern:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment end to end, measured | Build, with a labelled evaluation set and a gate in CI (G08, G16) | — |
| Identity and per-customer scope | Build: OIDC verified in the gateway, ownership checks on every route (G04) | — |
| Secrets and credentials | Build: workload identity, Guidewire secret only in the submitter's service account (G02, G09/G10); rotation documented with the production client (G23) | — |
| External writes | Build: confirmation bound to the draft version, durable operation, replay or reconciliation (G09/G10) | — |
| Sensitive data | Build: field minimisation, SDP redaction of payment and ID numbers, no content in logs, retention jobs (G13) | Face or document blurring if the DPIA asks for it (Later) |
| Prompt injection and agency | Build: tool-less photo reader, no submission tool on the model, capability checks, adversarial suite (G06, G14); Model Armor as an evaluated extra layer (G32) | — |
| Budgets and loop limits | Build: per-invocation call cap, per-customer allowance, admission limit, kill switch (G15) | Storm load test results (G27) |
| Memory and retrieval | Minimal: ADK sessions in Cloud SQL, plus the draft record. No semantic memory, no RAG | A follow-up journey that needs earlier claims (Later) |
| Frontend | Build: chat, upload, confirmation card and status in the existing portal (G11/G12) | — |
| Hosting | Build: Cloud Run in the EU, two services, staging then production with rollback (G16, G25) | — |
| Observability | Build: traces, token cost and operation SLIs in phase 1 (G17); SLO alerts and on-call in phase 2 (G26) | — |
| Release engineering | Build: release manifest and eval gate in phase 1 (G16); canary and joint rollback in phase 2 (G25) | — |
| Performance and cost tuning | Defer until measured (G27 measures) | p95 latency or cost per filed claim over target |

**Floor kept:** no secrets in code, prompts, logs or documents; spend stop
(`RunConfig.max_llm_calls`, the application allowance and a kill switch, plus
budget alerts); no claim without the customer pressing Confirm on the exact
summary; real personal data enters staging only after the DPIA allows it
(phase 1 uses synthetic customers and staff-staged photos); pinned model and
judge IDs.

**Accepted risks:** none yet. The user has accepted nothing because they were
unavailable.

**Who may use it:**

- Phase 1: staff, on staging, with synthetic policies and the Guidewire
  sandbox.
- Phase 2 pilot: invited customers in the launch market.
- GA: all policyholders in the launch market.

**Graduation conditions** (staff pilot → customer pilot → GA): DPIA signed
(G21); security review passes with no open high findings (G18 to G20), then the external pen
test (G28); production Guidewire connection (G22, G23) with the reconciliation runbook rehearsed (G26);
canary and rollback rehearsed (G25); SLO alerts and on-call (G26); storm load
test (G27); accessibility audit (G29); evaluation thresholds met in the launch
language (G08, G30).

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Face and document blurring in photos | Adjusters need the unaltered photo; the DPIA decides | A DPIA condition |
| Model Armor screening | Structural controls carry the guarantee; Model Armor's added value and EU availability are unmeasured | G32 shows it catches cases the suite misses at acceptable latency |
| Multi-region failover | The fallback form covers outages | An SLO above 99.5 % or a regulator requirement |
| Cost and latency tuning | No traffic measured yet | G27 or production p95 over target |
| Historical claim photos in evaluation | Needs a DPIA legal basis | DPIA permits it |

**Capacity and cut line** (figures from `check_schedule.py`, run 2026-10-09;
details and the command are in the plan). Phase 1 is G01 to G24: 620 to 1,052
human hours against 1,440 focused hours after a 25 % reserve, so the **hours
fit**. Its calendar finish is 36.6 to 61.5 of 60 working days, which fits
**at the low end only**. Across the whole programme to GA (G01 to G34,
876 to 1,482 hours), the finish is 67.5 to 106.1 of 100 working days, also
**low end only**. At the high end GA slips by about 6 working days. The
critical chain runs through the part-time security reviewer and the pen test
(G03 → G09 → G10 → G19 → G20 → G28 → G31 → G34). Options are in *Open
decisions*. The user has not confirmed the cut line.

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1. A customer reads or changes only their own sessions, drafts and photos, and sees only their own policies | Gateway middleware verifies the OIDC token and derives `customer_id`. Every route loads the resource and compares its owner. Tools read `customer_id` from state written by code, never from model arguments. The policy lookup is authoritative | 404 with no disclosure; the attempt is logged with metadata only | Cross-customer denial suite on every route and tool (G04, G14) |
| I2. One confirmed draft version produces at most one Guidewire claim | Unique `submission_operation` per `draft_id` in Cloud SQL, created in the confirm transaction. The worker sends an idempotency key or an external reference to Guidewire and looks it up before any re-create. **Guidewire's replay contract is unverified (G01)** | Duplicate confirm returns the existing operation. Uncertain outcome → `uncertain` state, lookup, then manual reconciliation | Fake Guidewire: double click, worker crash after commit, lost response, timeout; sandbox replay test (G09/G10) |
| I3. No claim exists without the customer confirming the exact summary shown | The model has no submission tool. `POST /drafts/{id}/confirm` requires the `version_hash` that was displayed, which must equal the current hash. Policy ownership and policy status are re-checked at confirm | 409 "summary changed, please review"; nothing is dispatched | Scripted model tries to submit, gets edited after display, or forges a confirm; the forbidden effect is absent (G09, G14) |
| I4. "Filed, claim number X" is shown only from a Guidewire receipt | The status endpoint renders the operation record, written only by the worker from Guidewire's response | "Submitting…" or "We are checking your claim, we will email you", never a false success | Worker test: the UI state follows the operation states (G10, G12) |
| I5. The assistant never states coverage, liability, payout or cost | Instruction, plus a release-time evaluation, plus a post-response check for forbidden commitments (model-judged, probabilistic) | Response replaced with a fixed sentence pointing to the adjuster | Eval: 0 violations on the adversarial "will I be covered" set; judge calibrated (G07, G08) |
| I6. Danger signals (fire, gas, electrical hazard, injury, structural collapse, active flooding) show the emergency guidance and 24-hour line in the same turn | Deterministic keyword trigger in the gateway plus an `emergency` field in the agent's turn contract. The guidance is rendered by the UI from fixed text | Guidance shown, then filing continues | Recall ≥ 0.98 on the labelled emergency set, *provisional target* (G08) |
| I7. Customer content is processed and stored only in the EU | Vertex AI regional EU endpoint (no global endpoint); EU Cloud SQL, GCS, Logging buckets and Trace; org policy `gcp.resourceLocations` | Deploy fails the readback check | Configuration readback in CI and the org policy check (G02, G16) |
| I8. No payment card, IBAN or national-ID numbers in sessions, logs or Guidewire free text | SDP inspection at gateway ingress, before persistence and before the model, with redaction. Telemetry content capture off | Redacted text; the customer is told not to share such numbers | Seeded test strings never reach the session DB, spans or logs (G13) |
| I9. Agent outage or exhausted budget never blocks filing | Admission and kill switch in the gateway; the UI falls back to the standard form and the phone line | "Use the standard form" with a link | Kill-switch and model-outage tests (G15, G12) |
| I10. Drafts, photos and conversations are deleted on schedule and on erasure request | Retention job on Cloud SQL and the GCS lifecycle policy; an erasure endpoint for the DPO process | Deletion is logged; Guidewire records follow claims retention | Retention and erasure test against a local DB and an emulator (G13) |
| T1. Time to first visible token, p95 ≤ 3 s; photo description ≤ 15 s; claim number ≤ 2 min after confirm, p95 | Measured by the gateway and worker | — | **Provisional targets**, measured in G24 and G27 |
| T2. Confirmed submissions reach `filed` or reconciled within 1 h: ≥ 99.5 % | Operation record SLI | Alert to on-call | G17 metric, G26 alert |

## Architecture and decisions

```mermaid
flowchart LR
  B[Customer browser\nexisting portal] -- OIDC token, JSON/SSE --> G
  subgraph EU GCP project (europe-west4, provisional)
    G[Cloud Run: claim-gateway\nFastAPI + ADK Runner\nSA: gateway-sa]
    W[Cloud Run: claim-submitter\nworker, no model\nSA: submitter-sa]
    SQL[(Cloud SQL Postgres\nADK sessions, drafts,\noperations, allowances)]
    GCS[(GCS EU bucket\nphotos, owner prefix)]
    T[[Cloud Tasks queue]]
    SDP[Sensitive Data Protection]
    V[Vertex AI Gemini\nregional EU endpoint]
    SM[Secret Manager\nGuidewire client secret]
  end
  G --> SQL & GCS & SDP & V
  G -- enqueue operation id --> T --> W
  W --> SQL & GCS & SM
  W -- OAuth2 client credentials, HTTPS --> GW[Guidewire ClaimCenter\nCloud API]
  G -- read: customer policies --> POL[Policy lookup\nGuidewire or policy system]
```

Trust boundaries: the browser is untrusted. The gateway trusts only the
verified token. Photos and customer text are untrusted content. Only
`submitter-sa` can read the Guidewire secret, and the submitter never calls a
model.

```mermaid
sequenceDiagram
  participant A as Anna (browser)
  participant G as claim-gateway
  participant M as Gemini (EU)
  participant D as Cloud SQL
  participant Q as Cloud Tasks
  participant S as claim-submitter
  participant C as ClaimCenter
  A->>G: message + OIDC token
  G->>G: verify token, owner check, SDP redact, emergency keywords
  G->>M: Runner turn (instruction, 3 tools, state)
  M-->>G: tool call update_claim_draft(fields)
  G->>D: validate + write draft v7
  G-->>A: SSE text; draft card from D
  A->>G: upload photo
  G->>G: validate, re-encode, store GCS
  G->>M: photo reader (no tools, output_schema)
  G->>D: observations into draft v8
  A->>G: POST confirm(draft_id, version_hash v8)
  G->>D: recheck owner, policy, hash; insert operation (unique draft_id)
  G->>Q: enqueue op id
  G-->>A: 202 "submitting"
  Q->>S: op id
  S->>C: create claim (idempotency key / external ref = op id)
  C-->>S: claim id
  S->>C: attach documents (per-photo sub-operation), submit
  S->>D: operation filed, claim number
  A->>G: GET status → "Filed: CLM-…"
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification and expected result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Five months to EU GA; external customers | Production profile in two phases: staging and staff pilot, then customer pilot and GA | The gates DPIA, pen test and production Guidewire carry calendar waits that only a phased plan absorbs | Less feature scope at GA | Schedule check passes for both phases | proposed, provisional on A1 and A5 |
| D2 | Interpret language and photos; never decide coverage | **One** conversational `LlmAgent` with three tools, plus a separate **tool-less** photo-reader model call made by application code, plus deterministic submission code. No sub-agents | Each part has a distinct authority: the conversational agent edits its own draft, the reader has no authority at all, submission happens only in code. More agents would add routing without adding a boundary | Multi-agent intake/photo/submit: more routing failure modes, no new security boundary | Rendered request shows 3 tools; photo reader request shows 0 tools | proposed |
| D3 | I2, I3: irreversible write only after the customer confirms, at most once | Submission is **not a model tool**. A UI button calls a confirm endpoint bound to `version_hash`. A durable `submission_operation` row is written and dispatched through Cloud Tasks to a separate worker | Confirmation must bind to the material details and survive a disconnect. A worker with its own identity keeps the Guidewire credential away from the model's process | ADK tool confirmation keeps the action inside the agent loop and the documented [known limitations](https://adk.dev/tools-custom/confirmation/#known-limitations) apply; a synchronous call loses the outcome when the browser leaves. Cost: a queue, a worker and an operation table | G09/G10 duplicate, crash and lost-response tests | proposed |
| D4 | The draft must survive a disconnect and render the same everywhere | `claim_draft` is a versioned application record in Cloud SQL, and chat refers to it by `draft_id`. ADK session state holds only `draft_id` and `customer_id`, both written by code | The authoritative summary does not depend on conversation replay | Revision handling and owner checks in code | Restart the service, reopen: same version for the owner, 404 for another customer | proposed |
| D5 | I1: customers see only their own data | OIDC verification in gateway middleware; `customer_id` comes from the token subject through the CIAM mapping; policies come from the authoritative lookup; tools take scope from trusted state | A conversation ID locates a resource but does not authorise access; the model cannot choose whose data it reads | A per-request policy lookup costs latency; cache 5 min per customer *(provisional)* | Denial suite (G04) | provisional on A3 |
| D6 | Custom upload, two identities, egress to Guidewire, a team new to ADK | **Cloud Run**, two services (`claim-gateway`, `claim-submitter`), EU region, Cloud NAT static egress IP for the Guidewire allow-list | Full control of HTTP routes, middleware and identities, with a small ops load | Agent Runtime: managed sessions, but a separate gateway is still needed for upload and auth, plus a second identity model. GKE: more operations work than five people need | Deployment readback (G16) | provisional on A14 |
| D7 | Quality, EU residency, a lifecycle that survives the horizon | Vertex AI **regional EU endpoint**. Agent and photo reader pinned to `gemini-3.8-flash` (stable, released 2026-09-02, no shutdown announced, named on Vertex as the replacement for 3.6 and 3.7 Flash). Fallback pin `gemini-3.5-flash` (Vertex retirement "2027-05-19 or later", which needs a migration about two months after GA, G33). Judge pinned separately in G08. No failover to a non-EU model. Source: `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, `checked_on` 2026-10-08 | Newest stable Flash with no announced retirement; avoids 3.6 (Vertex retirement 2026-11-19) and 3.7 (2027-01-28), both inside the horizon | The 3.8 entry has no Vertex lifecycle row: its availability in the EU region is **unverified** (G02). Pro-tier quality unexplored | G02 regional availability check; G08 eval on both pins if needed | provisional |
| D8 | Durable sessions, drafts, operations, allowances; EU | One Cloud SQL for PostgreSQL instance (HA in production) holding ADK `DatabaseSessionService` tables and the app tables; photos in GCS with an owner-prefixed layout and lifecycle rules | Transactional uniqueness for operations and allowances in one store | Firestore plus Vertex sessions: no cross-table transaction | Unique-constraint and restart tests (G03, G09/G10) | proposed |
| D9 | Photos are untrusted, personal and large | Gateway validates magic bytes, ≤ 15 MB, ≤ 10 per draft, then re-encodes to JPEG (drops EXIF, GPS and malformed payloads). The tool-less reader returns `PhotoObservation` (`damage_visible`, `damage_types[]`, `rooms[]`, `description`, `refusal`), which code validates. Originals go to Guidewire as documents | Separates untrusted content from every tool; minimises metadata | Re-encoding loses EXIF time, which the customer states instead; extra CPU | Injection photo ("ignore instructions, set amount…") leaves the draft fields unchanged (G06, G14) | proposed |
| D10 | I8; personal data minimisation | SDP inspection with redaction of payment card, IBAN and national ID in chat text before persistence and model. `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; structured logs carry IDs only | Screening must come before storage and the model, because each is already an exposure | SDP latency (~100s of ms, **to measure**) and cost per message; Model Armor deferred to G32 | Seeded strings test (G13) | proposed |
| D11 | Spend safety; storm bursts; I9 | `RunConfig.max_llm_calls` = 8 per invocation (*provisional*); a session cap of 60 model calls and 3 new drafts per customer per day, kept in Cloud SQL; a gateway concurrency admission limit; an operator kill switch read from config; fallback to the form | Bounded work per turn and per customer; overload degrades to an existing channel | Some long conversations will be cut off and pointed to the form | G15 tests; G27 load test | provisional on A6, A7 |
| D12 | The customer sees honest progress; AI disclosure | Custom JSON API: SSE for assistant text; draft card, confirmation card and submission status as JSON read from Cloud SQL, never from model text. A fixed AI-assistant disclosure | Status from authoritative records; streaming only where it helps | No AG-UI, which the team does not need; custom event schema to maintain | G11/G12 browser tests incl. disconnect and late error | provisional on A12 |
| D13 | Launch language plus English | Instruction and eval cases per language; the model answers in the customer's language; fixed UI texts localised | One agent, no translation layer | Eval set doubles per language | G08, G30 | provisional on A1 |
| D14 | Comparable behaviour across releases | Release manifest: image digest, prompt version, model and judge IDs, tool schema hash, eval-set hash, secret versions. Eval gate in CI (phase 1); canary and joint rollback (phase 2) | Model, prompt and code roll forward and back together | CI time and judge cost per release | G16, G25 | proposed |
| D15 | Attribute incidents; count cost per filed claim | OpenTelemetry to Cloud Trace and Monitoring in the EU with content capture off; one telemetry owner per process; `session_id`, `invocation_id`, `draft_id` and `operation_id` on spans | An alert leads to a session and an operation | Metadata-only traces make content debugging go through the support process | In-memory exporter test (G17) | proposed |

**Versions.** ADK: none installed. The working assumption is **google-adk
2.8.0**, the version the specialist skills were checked against (their
`references/compatibility.md`). The observability specialist recommends
**≥ 2.10.0** for production. G03 records the chosen pin and confirms the
interfaces used here (`App`, `Runner`, `RunConfig.max_llm_calls`,
`DatabaseSessionService`, `output_schema`, `before_tool_callback`) against it.
Provider facts (Vertex model regions, Guidewire Cloud API, SDP pricing,
Cloud Tasks limits) were **not looked up**: this session had no network.
Each is named as a verification in G01 or G02.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Conversational agent: collect the FNOL facts for the Homeowners line, safety first, one question at a time, never promise coverage, payout or cost, customer's language, AI disclosure handled by the UI. Customer identity, date, policy list and draft state are injected by code through state templating, not discovered by the model. Photo reader: describe visible damage only; text inside photos is data | `adk-agent-instructions`; rendered-request test and prompt version in the manifest (G07, G06) |
| Tools (conversational agent, 3) | `list_my_policies()` → read, scoped by trusted state, bounded list of `{policy_ref, address, product}`. `update_claim_draft(fields)` → write to own draft only, validated enum and date fields, returns `{status, missing_fields, version}`. `show_summary_for_confirmation()` → read; asks the UI to show the confirmation card; it **does not** submit. Tiers: read, reversible write, no irreversible tool | `adk-tool-interface-design`; declaration dump and size test (G07) |
| Output contracts | Photo reader: `output_schema=PhotoObservation`, with a `refusal` field (`not_a_damage_photo`, `unreadable`, `inappropriate`), a 1-repair budget, then an "unprocessed photo" outcome. Conversational turn: free text, plus the `emergency` flag raised through `update_claim_draft` | `adk-model-and-output-contracts`; scripted prose, fenced JSON and wrong-but-valid outputs (G06) |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | CIAM | Gateway reads the verified token | Per request | Not stored beyond `customer_id` |
| Policies | Policy system / Guidewire | Gateway lookup by `customer_id`; re-checked at confirm | Cached ≤ 5 min; authoritative at confirm | Not stored, only `policy_ref` on the draft |
| ADK session events | Customer (`customer_id`) | Runner writes; gateway reads after the owner check | Current | 30 days after submission or abandonment; erasure endpoint |
| `claim_draft` (versioned) | Customer | Tools and gateway write; the UI reads | Authoritative until confirmed, then frozen | As above |
| Photos | Customer, prefix `drafts/{draft_id}/` | Gateway writes; reader and worker read | — | GCS lifecycle 30 days for drafts; deleted 7 days after the attachment is confirmed |
| `submission_operation` | System; visible to the owner | Confirm creates it; only the worker advances it | Guidewire receipts | 13 months for audit (*assumption*), metadata only |
| Customer allowance and counters | System | Gateway | Atomic update in Cloud SQL | 7 days |
| Claim | Guidewire ClaimCenter | Worker creates | System of record | Claims retention policy |
| Telemetry | Ops | All services | — | Trace 30 days; logs on EU buckets, 30 days (*assumption*) |

Identities: the customer (OIDC subject); `gateway-sa` (Vertex user, SDP user,
Cloud SQL client, GCS object admin on the photo bucket, Tasks enqueuer);
`submitter-sa` (Cloud SQL client, GCS read, Secret Manager accessor on the
Guidewire secret only); the Guidewire OAuth client (service-level, acting for
the insurer). The submitter checks business authority again: the operation's
`customer_id` must own `policy_ref`.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Conversational agent | Yes (own policies, draft) | Customer text (the user's own input); photo observations as **validated structured fields** | Write to own draft only | No irreversible tool, no egress; capability check in `before_tool_callback` (owner, draft not frozen); confirmation in code. Injection can at most alter a draft the customer reviews |
| Photo reader | No (photo only) | Yes (raw photo) | None | Tool-less, schema output, validated; cannot act |
| Submitter (code, no model) | Yes | Draft contents as data | Guidewire write | No model in the process; sends only the frozen, validated canonical payload |

Adversarial cases (G14): text in a photo instructing a change of policy or
amount; a customer asking for another person's policy; forged `draft_id` or
`version_hash`; a request to "just file it now"; a request to promise payout;
an oversized photo and a polyglot file; HTML or script in the description
reaching Guidewire (the worker escapes the payload and Guidewire renders it
as text, **to verify**). No code executor is used.

## Budgets and capacity

*Illustrative, from A6 and A7.* 60,000 claims a year at 30 % gives about 50
agent-filed claims a day, with about 2.5× that in started conversations. A
storm day brings 10×, about 500 filed and 1,250 started. One conversation
takes about 12 conversational model calls (≈ 6k input and 400 output tokens
each, the prefix cacheable), one photo-reader call per photo (≤ 10, typically
4), about 12 SDP inspections, and one submission with up to 10 document
uploads.

Per-conversation cost = 12 × (6k·p_in + 0.4k·p_out) + 4 × (photo tokens·p_in
+ 0.3k·p_out) + 12 × SDP unit + Cloud Run, SQL and Tasks share. **Prices not
looked up (no network)**; G02 fills them from the pricing pages, with date.
Bound per conversation: 60 model calls. A storm burst reaches about 40
concurrent conversations at peak hour (*arrival × time in flight*, to be
validated in G27). Vertex quota and the Guidewire rate limit, not Cloud Run,
are the likely ceilings. When the allowance or the admission limit is
exhausted, new conversations are sent to the form, open drafts can still be
confirmed (that needs no model), and submission and reconciliation keep their
own capacity.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Successful filing | "Filed: CLM-…" from the operation record | Operation `filed`, photos `attached` | — |
| Another customer's draft ID or session | 404 | Nothing read; denial metric | — |
| Model unavailable or malformed | "Assistant unavailable, use the form" after a bounded retry (SDK retry, owned by the gateway: ≤ 2) | Draft saved | The customer resumes later or uses the form |
| Photo reader returns invalid output twice | Photo kept, marked "not described, please describe" | Draft without observations | The customer types the description |
| Browser disconnects mid-stream | On reconnect, history and the draft card from Cloud SQL; partial text not saved | The turn's completed tool writes persist | The customer continues |
| Duplicate confirm, or two tabs | The second gets the same operation status | One operation (unique `draft_id`) | — |
| Draft changed after the summary was displayed | 409, the new summary is shown | Nothing dispatched | The customer re-confirms |
| Policy lapsed or ownership changed between display and confirm | "This policy can't be used; call us" | Nothing dispatched | Claims phone line |
| Worker crashes after Guidewire committed, before recording | "Submitting…", then "checking" | Claim exists in Guidewire; operation `dispatched` | Task retry: look up by external reference or replay with the same key (**contract from G01**); never a fresh create without that check. Owner: worker, then the reconciliation queue |
| Guidewire timeout (uncertain) | "We're confirming your claim; you'll get an email" | Operation `uncertain` | The worker reconciles with backoff ≤ 1 h; then a manual queue for claims ops (runbook rehearsed in G26) |
| Claim created, a photo attachment fails | "Filed: CLM-…; 2 photos still uploading" | Claim plus partial documents | Per-photo sub-operation retries; never re-create the claim |
| Guidewire rejects (validation) | "We couldn't file this automatically; an agent will call you" or the form | Operation `rejected` with the reason code | Alert and a call-back task for claims ops |
| Process restart or overlapping workers | No change | Cloud SQL operation row; Cloud Tasks redelivers | The worker leases the row with a version check, so a stale lease cannot record twice |
| Erasure request while an operation is in flight | Erasure waits for a terminal state of the operation | Guidewire claim is out of scope for this erasure | DPO process (G13) |
| SDP or the telemetry exporter unavailable | SDP down: message rejected with "try again" (**fail closed**). Exporter down: no effect | No unscreened text stored | Alert |
| Storm burst or exhausted budget | Form fallback for new conversations | Open drafts remain confirmable | Admission (G15) |
| Model retirement inside the horizon | None | — | G33 re-baseline release before the date |
| Rollback | Previous revision serves | Session and draft schema migrations must be backward compatible for one release | G25 rehearsal |

## Verification and implementation handoff

- **Offline deterministic (CI):** scripted-model Runner tests for tools,
  capability checks, confirmation binding, operation state machine with a fake
  Guidewire, SDP redaction with a fake, budgets.
- **Local integration:** Postgres in a container for restart and uniqueness;
  a real process restart; SSE through a real socket; a browser test of the
  confirmation card.
- **Bounded live:** the Guidewire sandbox (G01, G09/G10), Vertex EU model calls
  within a set call cap (G06, G08), each on a named staging project.
- **Release and operation:** eval gate, staff pilot (G24), load test (G27), pen
  test (G28), canary (G25).

**Benefit measurement:** the baseline is today's digital FNOL completion rate,
time to file and the adjuster call-back rate for missing information (claims
data, G24). Pilot comparison in G31; guardrail: the adjuster correction rate
does not rise. These are hypotheses until measured.

**Observability and release:**

- SLIs: filed-or-reconciled within 1 h (T2), duplicate claims per confirmed
  draft (target 0), uncertain operations older than 15 min, tool error rate by
  tool, tokens and cost per filed claim, first-token and complete latency.
- Telemetry owner: each service's startup; content capture off; EU sinks with
  30-day retention.
- Release bundle as in D14, recorded in `release-manifest.json` per deploy.
- Promotion gate: deterministic tests on every change; judge metrics on
  release candidates with a pinned judge; a cost ceiling per eval run.
- Rollback unit: the previous revision with its manifest, kept ready for 7
  days.

Implementation routes, goals, estimates and tickets are in the plan.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Guidewire version, FNOL endpoints and replay/idempotency contract (A2) | I2 rests on it; without replay safety, reconciliation is lookup-only | Guidewire platform team; sandbox evidence (G01) | G10 replay detail, G23 |
| Is `gemini-3.8-flash` served at the chosen EU regional endpoint? (D7) | Otherwise use the 3.5 pin and plan a migration before 2027-05-19 | Vertex docs, region check (G02) | G06 and G07 live runs |
| Launch country and languages (A1) | Eval set size, instruction, UI texts | Product owner | G30 |
| Monthly spend cap (A6) | D11 thresholds, model tier | Business owner | G15 thresholds |
| AI Act classification and disclosure wording (A12) | Could add high-risk obligations | Legal | GA (G34) |
| DPIA outcome: photo blurring, retention, use of historical photos (A11, A13) | Adds controls or evaluation data | DPO (G21) | Customer pilot G31 |
| CMEK required? (A10) | Key ring setup and service configuration | Security policy | G02 |
| Profile and cut line (A16) | Everything | Product owner | — |
| GA high-end slip of about 6 working days | The critical chain runs through the reviewer at 2 h/day and the pen test. Options: (a) raise the reviewer to about 4 h/day in weeks 8 to 12 (**recommended**); (b) a 1-week invited pilot instead of 2; (c) accept GA up to about 2027-03-20 | Product owner and the security lead | G18 to G20, G28, G31, G34 |
