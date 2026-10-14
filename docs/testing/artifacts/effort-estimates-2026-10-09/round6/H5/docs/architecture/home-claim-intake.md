# System design: home-insurance claim intake agent

Status: **draft**. Every product answer below was assumed in a headless
session (see [Assumed answers](#assumed-answers)); decisions that depend on them
are marked *provisional*. Nothing here is user-accepted yet.

Decisions and their rationale live here. The plan
([docs/plans/home-claim-intake.md](../plans/home-claim-intake.md)) holds
estimates, owners and goals, and refers to these decisions by ID (D1, I2, …).

## Summary

- **What:** an ADK agent in the existing customer portal that helps an
  authenticated policyholder report home damage in conversation, attach photos,
  review a structured claim draft and, on their explicit confirmation, creates
  the claim (with photos as documents) in Guidewire ClaimCenter.
- **Profile:** production service, EU general availability on 2027-03-12
  (assumed date, Q1), preceded by a controlled pilot.
- **Shape:** one `LlmAgent` with four narrow tools that edit only the
  customer's own draft; a separate tool-less photo reader; claim submission is
  ordinary application code behind a Confirm button, never a model tool (D1, D3, D4).
- **Largest risks:** the Guidewire replay/idempotency contract is unverified
  (G01); EU regional availability of the pinned model and screening services is
  unverified (G02); the calendar is dominated by external waits (sandbox,
  DPIA, pen test, pilot), not engineering hours.
- **Decisions needed from the business:** the open decisions table at the end;
  the first five rows move dates.

## Assumed answers

Asked in no turn because the user was unavailable. Each row is a question I
would have asked, the answer assumed, and what depends on it.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | Exact GA date, and is it continued after GA? | 2027-03-12 (five months from 2026-10-14; 100 working days with a 24 Dec–1 Jan shutdown); continued | Plan calendar, cut line |
| Q2 | Are the six people dedicated, how many focused hours, how familiar with ADK and GCP? | Five engineers and one ML engineer dedicated at ~6 focused h/day; security reviewer ~2 h/day; experienced with Python and GCP, new to ADK (estimates ×1.5) | All estimates, schedule |
| Q3 | Model and cloud budget? | Moderate; no figure given. Costs stay symbolic; spend limits are provisional numbers to confirm | D10, cost section |
| Q4 | Who uses it and on which channel? | Retail home policyholders, signed in to the existing customer web portal (desktop and mobile web); claims handlers read the resulting claims in ClaimCenter | D5, D11 |
| Q5 | Which Guidewire product, deployment and API? | ClaimCenter on Guidewire Cloud, Cloud API (REST), OAuth2 client credentials; a sandbox tenant can be granted | D4, G01, G13 |
| Q6 | Which EU market(s) and languages at GA? | One EU country; its national language plus English | D7, G22, eval set |
| Q7 | Does an identity provider and a policy API exist? | Yes: portal OIDC IdP; an internal policy API returns a customer's active home policies and insured address | D5 |
| Q8 | Which claim types are in scope? | Home property damage (building and a contents summary) from water, fire, storm, theft, accidental damage, other. Bodily injury, third-party liability and commercial use go to a human | D9, scope |
| Q9 | May the system make or hint at coverage, payout or fraud decisions? | No. It records what the customer reports; ClaimCenter rules and adjusters decide | D1, I7 |
| Q10 | Region? | Data and processing in the EU: Cloud Run, Cloud SQL, GCS and logs in `europe-west4` (provisional), Gemini on Vertex AI in an EU region | D6, D7, G02 |
| Q11 | Expected volume? | ~2,000 online home claims per month at GA; a storm can bring 10× the daily average for two days | Budgets, G23 |
| Q12 | Retention periods? | Provisional: unsubmitted drafts 30 days; local photo copies 7 days after confirmed transfer to ClaimCenter; conversation sessions 90 days after submission. DPIA (G04) decides | D14 |
| Q13 | Human handoff channel? | Existing claims phone line; the saved draft reference is shown to the customer and noted on the claim when one is created | D9 |
| Q14 | Who operates it after GA? | This team in business hours, with the existing platform on-call for infrastructure | G19, G27 |
| Q15 | Existing IaC and CI? | Terraform and a CI system exist on the platform and are reused | G03, G21 |
| Q16 | Pen testing? | External vendor already contracted; window bookable with ~3 weeks notice | G24 |
| Q17 | Accessibility requirement? | WCAG 2.1 AA, as the portal already targets | G22 |
| Q18 | Historical claim descriptions for evaluation? | An anonymised extract of past first-notice-of-loss (FNOL) texts can be approved by the claims data owner | G12 |

## Purpose and constraints

**Journey (running example).** Anna's kitchen floods from a burst pipe on a
Sunday. Today she either phones the claims line (queues at weekends) or fills a
long web form with loss-cause codes she does not understand, then emails photos
separately; handlers often call back for missing details. With the agent she
opens "Report damage" in the portal, writes "pipe under the sink burst, water
everywhere, floor ruined", is asked whether the water is still running (safety
first), when it happened and which rooms are affected, uploads four photos,
sees a draft showing *loss cause: escape of water, date, rooms, damaged items as
she described and as the photos suggest*, corrects one item, presses
**Confirm and submit**, and receives a ClaimCenter claim number with the photos
attached.

**Outcome to improve (hypothesis, not measured):** fewer claims returned for
missing information and less abandonment than the web form, without more
handler correction effort. Baseline must come from current form and phone FNOL
data (G12, G26).

**Model contributes:** language understanding, follow-up questions, mapping a
description to the loss-cause taxonomy, describing visible damage in photos.
**Code controls:** identity, which policy, which fields are required, the draft
record, completeness, handoff rules, confirmation, submission, retries,
retention and budgets.

**Non-goals:** coverage, payout, fraud or liability decisions; contacting
third parties; motor or life claims; changing an existing claim (phase 2).

**Observed repository facts:** the repository holds only skill files; there is
no application code, manifest or dependency pin. All modules below are
proposed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | GA 2027-03-12 (Q1), pilot before it; continued |
| People and hours | 5 engineers + 1 ML engineer dedicated, part-time security reviewer (Q2); this team operates it (Q14) |
| Money | Not given (Q3); symbolic estimate below, provisional caps |
| Users and what they read | External customers using a running service; claims handlers reading ClaimCenter claims |
| Data and effects | Personal data and home photos; creates real claims and documents in ClaimCenter |
| Delivery profile | **Production service**: external customers, personal data and a write to the system of record |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: gated evaluation set (G12, G21) | — |
| Identity and per-customer scope | Build (G08) | — |
| Secrets and credentials | Build: workload identity, Secret Manager, rotation of the Guidewire client secret (G03) | — |
| External writes | Build: durable operation record, replay contract, reconciliation (G13) | — |
| Sensitive data | Build: minimisation, EXIF strip, screening, content-free telemetry, retention jobs (G09, G15) | — |
| Prompt injection and agency | Build: structural split, adversarial suite (G05, G20) | — |
| Budgets and loop limits | Build: per invocation, per customer, global stop (G16) | — |
| Memory | Sessions and the draft only; no cross-session memory | Returning-customer personalisation requested |
| Frontend | Build into the portal (G14, G22) | — |
| Hosting | Cloud Run with rollback (G18, G21) | — |
| Observability | Build: SLIs, alerts, runbook (G19) | — |
| Release engineering | Build: manifest, CI gate, canary, joint rollback (G21) | — |
| Performance and cost tuning | Defer | Measured p95 or cost per claim over target after pilot |

**Floor kept:** no secrets in code, prompts or logs; `max_llm_calls` plus
per-customer and global stops; no claim created without the customer's
explicit confirmation of the exact draft; personal data only what the journey
needs, kept out of telemetry content; pinned model ID.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Model failover (`FallbackModel`, ADK ≥ 2.9) | Draft is saved and the form/phone path exists when the model is down | Model unavailability breaching the SLO in pilot |
| Context caching and latency tuning | No measured problem | p95 turn latency or cost per claim above target |
| Cross-session memory | Journey is single-claim | Product asks for profile-based prefill |
| Editing a submitted claim, adding later photos | Separate ClaimCenter contract | Phase 2 goal G30 |

**Capacity and cut line:** phase 1 is G01–G27, 428–723 human hours against
2,850 hours after a 25 % reserve; finish 61–97 of 100 working days (schedule
check in the plan). Hours are not the constraint; external waits are. Contents
itemisation, a second market, follow-up documents and failover wait for
phase 2.

## Guarantees and acceptance

| ID | Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads or changes only their own sessions, drafts and photos | Gateway verifies the OIDC token and derives `customer_id`; every store query filters on it; IDs in requests only locate | 404 without disclosure | Cross-customer tests on every route (G08, G20) |
| I2 | One confirmed draft version produces at most one ClaimCenter claim | Unique operation record per `(draft_id)`; Guidewire replay contract verified in G01; reconciliation by external reference | "We are checking your submission" with operation ID; no fresh dispatch | Duplicate click, timeout-after-commit, restart tests against a fake and the sandbox (G13, G23) |
| I3 | No claim without the customer confirming the exact payload shown | Confirm POST carries `draft_id`, `version`, `payload_hash`; adapter recomputes and rejects mismatch | 409 "draft changed, review again" | Stale-version and tampered-hash tests (G13, G14) |
| I4 | No model-reachable path to ClaimCenter or any outside party | Agent tool inventory has no egress; submission is a separate route | — | Tool-inventory test and scripted-model attempt (G20) |
| I5 | Shown status reflects ClaimCenter receipts only | UI renders from the operation record; claim number only after receipt | "Pending" or "needs follow-up" | Lost-response test shows pending, not success (G13) |
| I6 | Personal data processed and stored in the EU | Region pins on every service; telemetry sinks EU | Deployment blocked | Config read-back + provider terms check (G02, G18) |
| I7 | The agent never states coverage, payout or fraud outcomes | Instruction + output review + eval rubric | Reply replaced by neutral text | Eval and adversarial cases (G11, G20) |
| I8 | Spend bounded per invocation, per customer and globally | `RunConfig.max_llm_calls`; per-customer counters in Postgres; operator stop flag | "Please continue later" or form fallback; draft kept | Budget-exhaustion tests (G16) |
| I9 | Only allowed images reach the model or ClaimCenter, EXIF stripped | Upload pipeline: type/size check, malware scan, re-encode | Upload rejected with reason | Fixture tests incl. polyglot and EXIF-GPS files (G09) |
| I10 | Emergencies get safety guidance in the first reply | Code-level keyword check plus model flag; fixed safety text | — | Eval cases (G11, G12) |

Provisional targets (Q3, Q11; owners: product for acceptance, Dev B for
alerting): time to first streamed text p95 ≤ 3 s; complete turn p95 ≤ 10 s;
photo assessment p95 ≤ 15 s; confirm-to-claim-number p95 ≤ 30 s (bounded by
ClaimCenter); intake availability 99.5 % monthly with form fallback.

## Architecture and decisions

```text
Browser (portal page: chat + draft panel + upload + Confirm)
   │ HTTPS, portal OIDC token
   ▼
Cloud Run "claim-intake" (europe-west4)                 [trust boundary]
 ├─ Gateway: verify token → customer_id; policy API lookup; budgets; one turn per session
 ├─ ADK Runner (App) ── intake LlmAgent ── tools: get_claim_draft, update_claim_draft,
 │                     │                        record_photo_observations, request_handoff
 │                     └─ (no egress tools)
 ├─ Photo reader: tool-less model call, output_schema DamageObservations
 ├─ Submission service (no model): operation record → Guidewire adapter
 └─ Retention jobs (Cloud Scheduler → job endpoint)
   │                    │                         │
Vertex AI Gemini (EU)  Cloud SQL Postgres (EU):   GCS bucket (EU): photos
                       ADK sessions, drafts,       │
                       operations, budgets         ▼
                                       Guidewire ClaimCenter Cloud API (OAuth2 client credentials)
```

Submission sequence: Confirm(draft_id, version, hash) → load draft, check
owner, version, completeness, policy still active → insert operation
(`op_id`, `draft_id` unique, canonical payload, hash) or load existing →
create claim with replay key `op_id` → record receipt (claim number) →
per-photo document operations → mark complete. A timeout leaves the operation
`uncertain`; reconciliation looks up the claim by external reference
`op_id` before any new dispatch.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Conversational intake; model must not decide outcomes or write externally | One `LlmAgent` with four function tools that only read/edit the caller's draft; follow-ups driven by a code-computed `missing_fields` list in state | Language work needs a model; the rules are known, so code owns them | Versus a multi-agent triage/photo/submit split: no distinct authority to justify it. Versus a plain form: kept as fallback and as the draft panel | Rendered-request test; eval completion rate (G11, G12) |
| D2 | Draft survives disconnects and is editable outside chat | Versioned `claim_draft` record in Postgres, owner-scoped; chat refers to it by ID; UI edits go through the same API | Same authoritative draft for chat, panel and submission | Revision handling versus draft-in-session-state | Restart and reopen returns the version to its owner, 404 for others (G07) |
| D3 | Photos are untrusted content | Separate tool-less reader call with `output_schema` (rooms, damage types, visible items, `unclear` refusal shape); its output is a proposal the customer confirms | Injected text in a photo cannot reach a tool | One extra model call per photo | Injection-photo fixtures leave draft and tools untouched (G10, G20) |
| D4 | One confirmed draft → one claim | Submission is application code with a durable operation record and the provider replay contract; reconciliation by external reference | Duplicate clicks, retries and restarts refer to one business operation | Depends on a Guidewire contract still unverified (G01) — **provisional** | I2 tests (G13, G23) |
| D5 | Customers act only on their own policies | Gateway derives `customer_id` from the verified token; the UI picks a policy from the policy API list; the policy summary enters session state as trusted context | Identity and scope never come from the model | Needs the policy API (Q7) — **provisional** | Cross-customer and inactive-policy tests (G08) |
| D6 | EU production hosting with custom auth and transactional records | Cloud Run (one service) + Cloud SQL Postgres + GCS, `europe-west4` | Gateway, Runner and submission share one transactional store; team controls middleware | Versus managed Agent Runtime: less control of the auth middleware and operation store; revisit if operations load is high | Deploy read-back, region checks (G18) |
| D7 | Stable, comparable model behaviour through GA | Agent and photo reader: `gemini-3.8-flash` on Vertex AI, pinned; judge: `gemini-3.8-flash`, pinned, deterministic metrics first. Source: `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, checked_on 2026-10-08: stable, released 2026-09-02, no shutdown or Vertex retirement listed. Not `gemini-3.7-flash` (Vertex retirement 2027-01-28, inside the plan) | Avoids a migration before GA | Newest model has the least field history; EU region availability unverified — **provisional** (G02) | Release manifest has no alias (G21) |
| D8 | Sensitive data minimised and protected | Model sees description, policy summary (no name, no payment data), photos re-encoded without EXIF; telemetry content capture off; SDP on log sinks; Model Armor on user text and photos if available in the EU region | Fields minimised first; screening is a layer, not the control | Screening latency; availability unverified (G02) | Captured request and log inspection (G15) |
| D9 | Unsafe or out-of-scope situations reach a human | `request_handoff(reason_code)` tool + code rules (emergency, injury, liability, commercial, customer asks); code shows fixed text and the phone line, saves the draft | Safety text and routing are not left to generation | Some customers are diverted who could have finished | Eval cases per reason (G11) |
| D10 | Bounded spend and abuse | `max_llm_calls`=8 per invocation; per customer per day 60 turns, 30 photos, 3 drafts; global operator stop flag; Cloud Billing budget alerts as observation only (values provisional, Q3) | Limits enforced in code before model work | Legitimate heavy users may hit limits; form fallback | Exhaustion tests (G16) |
| D11 | Responsive chat in the existing portal | Custom JSON API: SSE for assistant text, completed JSON events for draft updates, Confirm as a separate POST | Simple contract; portal stack unknown | Versus AG-UI/CopilotKit: less tooling, fewer dependencies | Real-socket stream test (G14) |
| D12 | Incidents attributable and SLOs visible | OpenTelemetry to Cloud Trace/Monitoring, content capture off, session/invocation/op IDs on spans | Alert leads to a session without exposing content | Less debugging detail; redacted sampling for eval | In-memory exporter test (G19) |
| D13 | Releases roll forward and back as one unit | Manifest (image digest, prompt version, model and judge IDs, tool-schema hash, eval-set hash, secret versions); CI gate; Cloud Run canary; joint rollback | Prompt/model/image combinations stay tested | Slower releases | Rollback rehearsal (G21) |
| D14 | GDPR retention and erasure | Scheduled jobs delete expired drafts, sessions and photo copies; ClaimCenter is the system of record after submission | Each store has an owner and an expiry | Periods are provisional (Q12, G04) | Job tests with seeded expired rows (G15) |
| D15 | No overlapping turns in one conversation | One active invocation per session, enforced with a Postgres row lock; overlap gets 409 | Prevents interleaved draft edits | A double-sent message is rejected, not queued | Concurrency test (G07) |

ADK version: no installed version. Working assumption **google-adk 2.8.0**
(the version the specialists were read against), with a recommendation of
**≥ 2.10.0** for production telemetry
(`adk-agent-observability/references/compatibility.md:40`). Confirming the pin
and re-checking `App`, `Runner`, `RunConfig.max_llm_calls`,
`DatabaseSessionService` and `output_schema` behaviour is acceptance for G06.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Intake agent: gather facts, ask one question at a time, safety first, never assess coverage, defer to `missing_fields` from state; policy, customer and date come from state, not the prompt author | `adk-agent-instructions`; rendered-request test (G11) |
| Tool interfaces | `get_claim_draft()`, `update_claim_draft(fields)` (taxonomy enums, returns `missing_fields`), `record_photo_observations(photo_id, accepted)`, `request_handoff(reason_code)`; four tools, all write-tier only to the caller's draft; results < 2 KB | `adk-tool-interface-design`; declaration dump and size (G11) |
| Output contracts | Photo reader `DamageObservations` with `status: ok \| unclear \| not_a_damage_photo`; repair budget 1, then `unclear`; pinned model per D7 | `adk-model-and-output-contracts`; scripted prose/fenced/invalid outputs (G10) |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| ADK session events | Customer; keyed by `customer_id` | Runner / gateway | Postgres (`DatabaseSessionService`) | 90 days after submission or 30 after abandonment (Q12) |
| Claim draft (versioned) | Customer | Tools, UI API / agent, UI, submission | Postgres, authoritative until submission | Same as session |
| Policy summary | Insurer | Policy API / gateway → state | Read at session start and rechecked at submit | Not stored beyond session |
| Photos | Customer | Upload pipeline / reader, adapter | GCS EU, object per photo, owner metadata | 7 days after confirmed ClaimCenter upload; 30 days if never submitted |
| Submission operation | Insurer | Submission service / UI status, reconciliation | Postgres, unique per draft | 1 year (audit, provisional) |
| ClaimCenter claim and documents | Insurer (system of record) | Adapter / handlers | ClaimCenter | ClaimCenter policy |
| Budget counters | Insurer | Gateway | Postgres, daily window | 30 days |

Identities: end user = portal OIDC subject; workload = Cloud Run service
account (Vertex, Cloud SQL, GCS, Secret Manager); Guidewire = OAuth2 client
credentials held in Secret Manager, selected in adapter code, never a model
argument. Session ID locates; it never authorises.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Intake `LlmAgent` | Own policy summary, own draft | Customer text; reader output (validated structure) | Write to own draft only | No egress tool; write scoped by trusted `customer_id` in `before_tool_callback`; external effect needs the customer's click in code (I3, I4) |
| Photo reader | None beyond the photo | Photo pixels and embedded text | None | No tools; schema-validated output |
| Submission service | Draft, policy | None reaching a model | ClaimCenter write | Not a model; triggered only by confirmed POST |

Tool tiers: read (`get_claim_draft`), write-own-draft (others); irreversible
(claim creation) is outside the agent. Adversarial cases (G20): prompt asking
to submit, to read another customer's draft, to state coverage; injected text in
photos; forged confirm; oversized and polyglot uploads. No code executor.
Findings mapped to OWASP LLM IDs in G20.

## Budgets and capacity

Per claim (assumed): ~10 intake turns, each ≤ 3 model calls (expected 1–2),
~6k input and ~300 output tokens per call; ~5 photo reader calls of ~2k input
and ~400 output tokens; no judge in production. Bound per invocation:
`max_llm_calls`=8. Monthly ~2,000 claims (Q11) → roughly 30–60k model calls.
Prices were not looked up (no network): cost = calls × tokens × current Vertex
EU price, to be filled in G02 with source and date. Storm peak: 10× daily
average for two days, about 650 claims/day; concurrency ≈ arrival rate × time
in flight, measured in G23. Fixed costs: Cloud SQL instance with HA, Cloud Run
minimum instances (1 in production to avoid cold starts on first turn).
On exhaustion: per-customer stop keeps the draft and offers the phone line;
global operator stop disables new sessions, leaves submission and
reconciliation running.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success | Claim number, photos listed as attached | Operation complete with receipt | — |
| Another customer's draft or session ID | 404 | Nothing read | — (I1) |
| Model unavailable or malformed reply | "We saved your draft; try again or use the form/phone" | Draft at last version; no partial claim | Retry later; Dev B alert on error rate |
| Reader returns prose/invalid | Photo marked "couldn't read, please describe" | Photo stored; no observations | Customer describes; counted as reader failure |
| Browser disconnect mid-turn | Reopen shows saved draft and last complete reply | Session events up to the last completed one | Customer continues |
| ClaimCenter commits, response lost | "We're checking your submission" with reference | Operation `uncertain`; claim may exist | Reconciliation job looks up by `op_id`; manual queue after 3 failed lookups (Dev B on-call) |
| Claim created, a photo upload fails | Claim number shown, "1 photo still being attached" | Claim + per-photo operations | Document retry job; handler notified after N failures |
| Double click / two tabs confirm | Same operation result in both | One operation row | — (I2) |
| Policy lapses between draft and confirm | "This policy isn't active — call us" | Draft kept | Phone handoff |
| Restart during submission | Status from operation record | Operation persisted before dispatch | Reconciliation resumes |
| Erasure request while submission pending | Erasure waits for operation to finish, then deletes local copies | ClaimCenter retains under its own policy | Data-protection process owner |
| Screening service unavailable | Upload/turn rejected with retry message (fail closed) | Nothing sent to model | Alert; operator may switch to form |
| Budget exhausted / storm peak | "Please continue later" or form; queue none | Draft kept | Operator raises limits deliberately |
| Model retirement announced | No user effect | — | Planned re-baseline release (G21 calendar) |
| Bad release | Canary metrics breach | Previous revision kept ready | Joint rollback of image, prompt, model ID (G21) |

## Verification and implementation handoff

- **Offline:** scripted-model Runner tests for tools, scope, budgets, schema
  failures; fake ClaimCenter for replay, timeout-after-commit and restart.
- **Local integration:** real Postgres restart for sessions, drafts and
  operations; real sockets for SSE.
- **Bounded live:** ClaimCenter sandbox for the replay contract (G01, G13);
  Vertex EU calls for the eval set with a spend limit (G12).
- **Release/operation:** CI gate, canary, rollback and recovery rehearsal (G21,
  G23); pen test (G24); pilot with handler review against the form baseline (G26).

SLIs (G19): completed intakes / started; submissions with receipt / confirmed;
uncertain operations older than 15 min (alert); tool-error rate by tool; tokens
per completed claim; p95 first-text and turn latency. Content capture off;
traces 30 days, logs EU buckets. Product benefit (fewer handler call-backs,
lower abandonment) is a hypothesis measured in G26, separately from eval
quality.

The [plan](../plans/home-claim-intake.md) maps each decision to goals,
skills and acceptance.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Guidewire replay contract (transaction-ID header or equivalent), external-reference lookup, draft-then-submit flow | Without replay or lookup, I2 needs manual reconciliation | Dev B via G01 against docs and sandbox | G13 design detail |
| Gemini 3.8 Flash, Model Armor and SDP in the chosen EU region; data residency terms | D7, D8 and I6 may need another region or model | ML via G02 | G15, G18 |
| DPIA outcome: retention, lawful basis, photos of people, AI Act Art. 50 notice | D14, UI text, pilot start | DPO via G04 | G26 |
| Market, languages and GA date (Q1, Q6) | Eval set, translation, calendar | Product owner | G12, G22 |
| Team dedication (Q2) | Every date in the plan | Engineering manager | Plan |
| Budget figure (Q3) | D10 limits, minimum instances | Product owner | G16 |
| Policy API and portal frontend stack (Q7, Q4) | D5, D11 | Platform/portal owners | G08, G14 |
