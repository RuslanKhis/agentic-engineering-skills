# System design: home-insurance claim intake agent (photos → Guidewire FNOL)

Status: **draft**. The design was written in one pass without the user available.
Every row in the assumed-answers table below is provisional, and so is every
decision that depends on one. Nothing here has been user-accepted yet.
Implementation plan: [docs/plans/home-claim-intake.md](../plans/home-claim-intake.md).
Tickets: [docs/tickets/home-claim-intake/](../tickets/home-claim-intake/).
Date: 2026-10-09.

## Assumed answers

These are the questions I would have asked. The user was not available, so each
answer is an assumption. Decision IDs refer to [Architecture and decisions](#architecture-and-decisions).

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | What is the GA date and market, and is the service continued after GA? | GA on **2027-03-09** (five months from 2026-10-09), in **one EU country**. The service is continued afterwards and more markets follow in phase 2. | Phase plan, D5, D14 |
| A2 | Who builds it, and how familiar are they with ADK and GCP? | 5 full-time engineers who know Python and GCP but are **new to ADK**. 1 ML engineer who knows evaluation. 1 security reviewer for **one day a week**. | Capacity, ×1.5 multiplier, G15 sizing |
| A3 | What budget is there for models and cloud? | Enough for three environments and pilot traffic. The per-claim model cost target is set after G02 prices it, and no number is assumed. | D11, G17 |
| A4 | Who uses it? | Authenticated policyholders in the **existing customer web portal** (responsive web; no native app at GA). Claims operations reads the resulting claims. Compliance and the DPO judge the launch. | D9, D8, G09 |
| A5 | What data does it touch, and what can it change? | Real personal data: the customer's identity, policy, free-text incident account and **photos** of their home, which may show people, documents or special-category hints. Its only external effect is **creating a first-notice-of-loss (FNOL) claim plus documents in Guidewire ClaimCenter**. It moves no money and makes no coverage decision. | Profile, D2, D3, D10 |
| A6 | What is Guidewire's deployment and API? | **Guidewire Cloud ClaimCenter with Cloud API** (Claim API and its document endpoints). A sandbox tenant can be obtained from the Guidewire admin team. | D3, G01, G08 |
| A7 | Where must data stay? | All processing and storage stays in the **EU**: model inference, sessions, photos, logs and backups. The Guidewire tenant is in the EU. | D4, D5, D6, D7 |
| A8 | Which languages? | The local language of the launch market plus English. | G10, G19 |
| A9 | What volume should we expect? | About 25 agent-filed claims per business day on average. A storm peak of 10–20× that over 1–3 days. These are illustrative numbers to replace with the user's figures. | Budgets and capacity, G17 |
| A10 | How long are conversations and photos kept? | Drafts and conversations: 30 days after submission or abandonment, then deleted. Photos in our bucket: deleted 30 days after a confirmed upload to Guidewire. Guidewire holds the record of claim under the insurer's own retention. | D6, D7, G11 |
| A11 | Should the agent judge coverage or fraud? | **No.** Adjusters decide coverage, liability, payout and fraud. The agent collects facts and photos and says what happens next. | D13, I4 |
| A12 | Which claim types are in scope? | Home buildings and contents: escape of water, storm, fire (after the emergency), accidental damage and theft (with a police reference). Injury, third-party liability and an unsafe home go to a human. | D13, G10 |
| A13 | What fallback exists? | The existing classic web claim form and the phone line stay available and are the fallback. | D11, failure table |
| A14 | How is the AI Act treated? | Working assumption: claim intake for home insurance is **not** an Annex III high-risk use, because Annex III lists life and health insurance risk and pricing. Article 50 transparency still applies, so the customer is told they are talking to an AI. **Legal must confirm.** | D14, G05 |
| A15 | Which infrastructure-as-code and CI does the org use? | Terraform and an existing CI system. A cloud platform team creates projects. | G04 |
| A16 | How do customers get their claim number and later updates? | They see it on the confirmation screen. Guidewire's existing customer notifications carry later updates. | D3, failure table |

## Purpose and constraints

**Journey (running example).** On a Saturday, Maria finds that a burst pipe
under her kitchen sink has soaked the floor and a base cabinet. She signs in to
the insurer's portal and opens "Report damage". She tells the assistant what
happened and when. It identifies her home policy, asks the questions an FNOL
needs (date, cause, affected rooms, emergency measures taken, whether water is
still escaping) and asks for photos. She uploads four phone photos. The
assistant confirms what it sees ("standing water near a base cabinet; swollen
cabinet panel") and asks about anything missing. It then shows a summary card
rendered by code from the stored draft, and Maria presses **Submit claim**. The
backend creates the claim and its documents in ClaimCenter and shows her claim
number and the next steps. It does not tell her whether she is covered.

**Current friction (assumed).** Customers phone the call centre or fill in a
long static form. Adjusters often have to ask again for photos and missing
facts. The FNOL arrives incomplete, and first adjuster contact is delayed.

**Outcome to improve.** These are hypotheses until measured against a baseline
that G05/G20 obtain from claims operations:
- the share of FNOLs that need no information request from an adjuster,
- the time from incident report to a claim with photos,
- the completion rate of started digital claims,
- with guardrails: no rise in the misfiled-claim rate, the complaint rate or
  call-centre contacts per claim.

**Non-goals.** Coverage decisions, payout estimates, fraud scoring, claim status
follow-up (phase 2, G23), non-home lines, voice and native apps.

**What the model contributes, and what code controls.** The model interprets
the customer's account, chooses the next question, phrases replies with empathy,
and describes visible damage in photos. Code controls identity, which policy may
be used, draft validation, the completeness rules, the rendered summary,
confirmation, the Guidewire write, retries, budgets, screening and retention.

**Facts versus assumptions.** Observed in this repository: there is no
application code yet. The only content is the ADK skill set under `.claude/skills/`.
Everything about Guidewire, the portal, the IdP and GCP comes from the assumed
answers above.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | GA 2027-03-09 (A1). Internal dogfood about week 9, closed pilot about weeks 15–18. The service is continued afterwards. |
| People and hours | 5 engineers (E1–E5), 1 ML engineer, a security reviewer at about 1 day a week (A2). Focused capacity is about **3,124 h** (see [plan](../plans/home-claim-intake.md#delivery-profile-and-capacity)). The same team runs it after GA, with an on-call rota from G21. |
| Money | Three environments and pilot traffic. The per-claim cost target is set after pricing in G02 (A3). |
| Users or judge, and what they read | External customers use the running service. Claims operations reads the claims in Guidewire. DPO, legal and security read the DPIA, the threat model and the pentest. |
| Data touched and effects allowed | Personal data and photos. One external write: an FNOL claim and its documents in ClaimCenter (A5). |
| Delivery profile | **Production service.** It serves external customers, uses real personal data under GDPR and writes to the system of record, with a regulated EU launch. |

Depth per concern:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: evaluation set with a CI gate (G10, G14, G16) | A new market or language (G24) |
| Identity and per-customer scope | Build (G06) | n/a |
| Secrets and credentials | Build: workload identity, Secret Manager, rotation of the Guidewire client secret (G04, G08) | n/a |
| External writes | Build: durable operation record, duplicate prevention, reconciliation (G08) | n/a |
| Sensitive data | Build: SDP on ingress text, Model Armor, content-free telemetry, retention and erasure (G11) | A new data category (e.g. injury) |
| Prompt injection and agency | Build: quarantined photo reader, no model-held write to Guidewire, adversarial suite, pentest (G07, G15) | A new tool or untrusted source |
| Budgets and loop limits | Build: per-invocation, per-session and per-customer limits, and a kill switch (G12) | Storm-surge measurement (G17) |
| Memory | Minimal: sessions plus a resumable draft (G18). No long-term memory. | A cross-claim continuity requirement |
| Frontend | Build: integration into the existing portal (G09, G19) | Native app (later) |
| Hosting | Build: Cloud Run in the EU, staged rollout and rollback (G04, G14, G21) | Multi-region DR requirement (later) |
| Observability | Build: SLIs, alerts, runbooks (G13) | n/a |
| Release engineering | Build: manifest, CI gates, manual staged rollout (G14). Automated canary waits for phase 2 (G22). | Traffic big enough for comparable canary samples |
| Performance and cost tuning | Defer until measured (G27) | p95 or cost over target in the pilot |
| Retrieval / RAG | Not used. The journey needs no document knowledge base. | Agent must answer policy-wording questions |
| Analytical SQL | Not used | n/a |
| Interoperability (MCP/A2A) | Not used. Guidewire is called by our own code over REST. | Partner network or remote agent integration (later) |

**Floor kept:** no secrets in code, prompts or logs. A spend stop through
`max_llm_calls`, per-session and per-customer limits, a kill switch and budget
alerts. Nothing reaches Guidewire without the customer confirming the
code-rendered summary of that exact draft version. Real data is scoped to the
customer and kept out of logs. Model IDs are pinned.
**Accepted risks:** none proposed. The coverage-promise risk (I4) is reduced
and measured, not eliminated. It is recorded as an open decision for the user
to accept.

**Who may use it:** phase 1 runs internal staff on sandbox data (dogfood) first,
then a pilot cohort of real customers, then all portal customers in the launch
market at GA.
**Graduation conditions** before the pilot (G20): DPIA signed off, pentest
critical/high findings closed, evaluation thresholds met (G16), runbooks and
alerts live (G13). Before GA (G21): pilot SLIs within target for 2 weeks,
rollback and erasure drills passed.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Automated canary with statistical thresholds (G22) | Pilot traffic is too small for comparable samples | More than ~200 sessions a day |
| In-EU model failover (G26) | Needs measured regional error rates | Vertex EU incidents in the pilot, or an SLO miss |
| Cost and latency tuning (G27) | Not measured yet | Pilot p95 or cost per completed claim over target |
| Multi-region disaster recovery | One region with backups meets the assumed recovery target | An RTO below 4 h from the business |

**Capacity and cut line:** phase 1 (G01–G21) estimates **872–1,468 h** against
about 2,343 plannable hours (3,124 focused hours minus a 25% reserve). Hours do
not bind. The **calendar** does: the chain G01 → G08 → G15 → G20 → G21 plus its
waits takes about 19–21 of 21 weeks. If it runs high, G18 moves to phase 2
first, then the storm-surge half of G17, then the automation in G14. See
[plan](../plans/home-claim-intake.md#cut-line).

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| **I1** A customer can read and change only their own drafts, photos and policies | API middleware verifies the portal OIDC token. The repository layer scopes every query by the verified `customer_id`. Policy ownership comes from the policy system via a trusted lookup (G06). | 404 and no disclosure. The denial is logged without content. | Cross-customer denial tests on every route and tool (G06). Pentest (G15). |
| **I2** One confirmed draft version produces **at most one** ClaimCenter claim | `submission_operation` row is unique on `(draft_id, draft_version)`. The operation ID is sent as Guidewire's duplicate-prevention key (contract to verify in G01). Reconciliation looks up the claim by our external reference. | Uncertain: shown as "confirming", never as failed-and-retryable | Fake-Guidewire tests for timeout after commit, double click, restart mid-submit and changed payload (G08) |
| **I3** No claim is created without the customer confirming the summary of that exact version | Only the `/submit` endpoint writes, and it requires the version hash shown on the card. The model has no submit tool. | 409 when the version is stale. Nothing is written. | Tool-list assertion. A scripted model "tries to submit". Stale-hash test (G08, G15). |
| **I4** The assistant does not state coverage, payout or liability decisions | The instruction (G03) plus a response-release check (G11) block or rewrite such statements. This is probabilistic and measured. | The reply is replaced with the standard "an adjuster will assess" text | Eval metric: coverage-promise rate below the threshold set in G16 on the adversarial subset, target 0 observed in N≥100 probes |
| **I5** Photo content cannot cause actions or change authority | The photo reader is single-turn with **no tools**. Its output is validated against a schema. Observations are suggestions that the customer sees and confirms (D1). | Invalid output becomes "photo could not be analysed", and the photo is still attached | Injection-photo suite asserts that no tool call and no field change happens without customer text (G07, G15) |
| **I6** No customer content in logs, traces or metrics | Telemetry content capture off (`ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`, OTel GenAI capture `NO_CONTENT`). A structured-log allowlist. | A leak counts as an incident | In-memory exporter test (G13). Log-scan test with canary PII (G11). |
| **I7** Data stays in the EU | Every service sits in an EU region. Vertex uses a regional EU endpoint, not `global`. Buckets are regional. | A deployment check fails | Residency checklist in G02. Terraform policy test (G04). |
| **I8** Spend and work are bounded | `RunConfig.max_llm_calls` per invocation. Per-session turn and photo caps. A per-customer daily session admission. A global kill switch (G12). | A polite stop, with the classic form offered and the draft preserved | Offline loop and limit tests. Load test (G17). |
| **I9** A submission outcome is never misreported | The UI shows status from the operation record: `confirmed` (claim number), `pending`/`uncertain` (confirming) or `rejected` (with a fix). | n/a | UI state tests for each status (G09) |
| **I10** Retained content is erased on schedule and on request | A retention job deletes sessions, drafts and photos. The erasure endpoint is owned by the DPO process. | Failures are alerted | Erasure drill (G21) |
| Target: p95 turn latency ≤ 8 s for text, ≤ 15 s with photo analysis (provisional, A9) | Cloud Run plus Vertex EU | A progress indicator; graceful timeout | Load test (G17), pilot SLIs (G20) |
| Target: intake API availability 99.5% monthly; ≥ 99% of confirmed submissions reach `confirmed` within 5 min; every `uncertain` resolved within 1 h (provisional) | Cloud Run, reconciliation job, on-call | Fallback to the classic form | Pilot SLIs (G20). Targets reset from the pilot baseline in G21. |

## Architecture and decisions

```text
 Customer browser (existing portal, signed in via customer IdP)
        │  HTTPS, portal session → OIDC ID token
        ▼
 ┌─────────────────────── Cloud Run: claim-intake-api (EU region) ───────────────────────┐
 │ FastAPI middleware: verify token → customer_id (trusted)                               │
 │   /turns       → admission (budgets) → SDP screen → ADK Runner(App: claim_intake)      │
 │                    intake LlmAgent (gemini-3.8-flash) tools:                           │
 │                      list_my_policies, get_policy_summary, update_claim_draft,         │
 │                      prepare_submission_summary, escalate_to_human                     │
 │                  → response release check → JSON reply                                 │
 │   /photos      → signed upload URL (bound to draft) ; on finalize: validate, strip EXIF│
 │                  copy, run photo_damage_reader (single-turn, no tools, output_schema)  │
 │   /submit      → verify version hash → submission_operation → Guidewire adapter        │
 │   reconciler   → Cloud Scheduler-triggered job for pending/uncertain operations        │
 └──────────┬──────────────┬──────────────────┬─────────────────────┬──────────────────────┘
            │              │                  │                     │ OAuth2 client creds
            ▼              ▼                  ▼                     ▼ (Secret Manager)
   Cloud SQL Postgres   GCS photos bucket   Vertex AI (EU regional) Guidewire Cloud
   - ADK sessions       (EU, no public)     Gemini; Model Armor;    ClaimCenter Cloud API
   - claim_draft        originals + model   SDP (EU)                (EU tenant): policy
   - submission_op      copies                                       lookup, claim, documents
```

Trust boundaries: the browser and all customer content (text and photos) are
untrusted. The middleware is the only source of `customer_id`. The serving
service account (`sa-intake-run`) can reach Cloud SQL, the bucket, Vertex,
SDP/Model Armor and Secret Manager (Guidewire secret only). The Guidewire
integration user has only FNOL-create, document-add, policy-search and
claim-read roles (to confirm in G01).

**Submission sequence.**
1. The customer presses Submit on the card for draft *d*, version *v*, hash *h*.
2. `/submit` checks ownership (I1) and that the current version is *v* with hash *h* (I3).
3. In one transaction, it inserts or loads `submission_operation(op_id, d, v, payload_hash, state=pending)`. A different payload for the same *(d, v)* is rejected.
4. It re-checks that the policy is active and owned by the customer.
5. It calls Guidewire to create the claim with the external reference `op_id` and the duplicate-prevention key `op_id`. It stores the claim ID.
6. It submits the claim. It uploads each photo as a separate idempotent sub-operation `(op_id, photo_id)`.
7. It marks the operation `confirmed` with the claim number.

A timeout at any step leaves the operation `uncertain`. The reconciler finds
the claim by external reference and resumes from the recorded step. It never
creates a new claim for the same `op_id`.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | A5, I5: photos are untrusted. The model must describe damage, not act on it. | One conversational `LlmAgent` plus a **quarantined single-turn photo reader** with no tools. Code runs the reader on each upload, and its validated observations enter the draft as `suggested`. | Removes the untrusted-content-plus-write leg from the reader. Code triggers analysis deterministically. | An extra model call per photo, and observations reach the agent only as typed fields. Alternative: the intake agent sees photos directly. That is simpler, but the agent holding tools then reads untrusted images. | Injection photos (G07, G15). Schema-invalid reader output (G07). | Proposed |
| D2 | I3: a claim needs explicit customer confirmation | **The model holds no Guidewire write.** `prepare_submission_summary` freezes a draft version. The UI renders the card from the stored draft. Submit is a customer HTTP action bound to the version hash. | Confirmation is enforced in code the model cannot reach. The card shows stored data, not model prose. | The agent cannot "just file it" in chat, which costs one click. Alternative: an ADK tool with confirmation. Its semantics are version-dependent (2.10.0 changed the confirmation hold), and the model would still own the effect. | Tool-list assertion. Stale hash returns 409. A scripted model cannot submit (G08). | Proposed |
| D3 | I2: at most one claim, even when replies are lost | A durable `submission_operation` in Cloud SQL, with the operation ID as the Guidewire external reference and duplicate-prevention key, reconciliation by lookup, and per-photo sub-operations | ADK session events do not provide durable execution or replay contracts | More tables and a reconciler job. Alternative: retry the HTTP call blindly, which can create duplicate claims for adjusters. | Fake-Guidewire fault matrix (G08). Sandbox replay check (G01). | Provisional on G01 |
| D4 | A7, A2: EU hosting the team can operate | **Cloud Run** in an EU region (working assumption `europe-west4`, set by the market in G02), min instances 1, serving a FastAPI app around the ADK `Runner` | Full control of middleware, upload endpoints, the submit path and traffic splits. Familiar to a GCP team. | We own the gateway and scaling. Alternative: managed Agent Runtime. Less ops, but it would still need a separate API for upload and submit, and its EU availability and session controls need checking. GKE is too heavy for this team. | First deploy readback (G04). Region checklist (G02). | Provisional on G02 |
| D5 | Quality and lifecycle beyond GA, plus A7 | Agent and reader on **`gemini-3.8-flash`** via a **Vertex AI EU regional endpoint**. It is stable with no announced shutdown in the lifecycle snapshot checked 2026-10-08. Fallback candidate: `gemini-3.5-flash` (Vertex retirement "2027-05-19 or later"). `thinking_level` low for the agent, minimal for the reader. | Avoids `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28), which retire inside the plan. Avoids 2.5 models (2026-10-20). | Newest model, so less field history. Regional availability in the EU is unverified. | G02 confirms EU regional availability, image limits and data-use terms. G16 measures quality. | Provisional on G02 |
| D6 | Drafts must survive restarts and resumption (G18). Retention (A10). | ADK `DatabaseSessionService` on **Cloud SQL for PostgreSQL** (EU, private IP). Application tables `claim_draft` (versioned) and `submission_operation` in a separate schema of the same instance. | One transactional store for drafts and operations. Sessions are durable across replicas. | We own a database. Alternative: Vertex AI session service, which leaves business records in another store with no shared transaction. | Restart test (G03/G18). Migration rehearsal (G21). | Proposed |
| D7 | Photos are evidence for adjusters. The model needs only content. | A regional EU bucket with no public access. Upload through a V4 signed URL bound to `(customer, draft, photo_id)` with a size cap. On finalize, the server validates type and size and decodes, then stores the original plus an EXIF-stripped, downscaled copy for the model. Guidewire gets the original after confirmation. | Adjusters keep the full evidence, and location metadata never reaches the model | Two copies stored for up to 30 days. Alternative: upload straight to Guidewire before confirmation, which creates records the customer never confirmed. | Upload validation tests and EXIF-strip test (G07) | Proposed |
| D8 | I4, I6: screen before showing | Per turn, the browser gets a **completed JSON reply** plus a typing indicator. No token streaming. | A full-response release check is possible before display. The contract is simpler. | Slower first content (about 2–6 s). Alternative: streaming, which cannot retract a coverage promise once shown. | UI contract tests (G09). p95 measured (G17). | Proposed |
| D9 | I1 | The portal's OIDC ID token is verified in middleware (issuer, audience, expiry, signature). `customer_id` and the policy list go into trusted session state under the `temp:`/app-owned key. Tools read scope from `ToolContext` state, never from model arguments. `select_policy` accepts only an index into the trusted list. | Identity never passes through the model | We depend on the portal IdP's claims. A policy lookup is needed per session. | Cross-customer denial tests (G06) | Provisional on IdP details (G06) |
| D10 | GDPR minimisation, I6 | **SDP** inspects the customer's text **before persistence**: IBANs, cards and national IDs are masked and the customer is told. **Model Armor** screens input for injection and jailbreak, and output for sensitive data. OTel content capture is off. Retention jobs run per A10. | Screening sits before storage, the model and display, which are the exposure points | Adds latency and per-call cost. Model Armor is a probabilistic layer behind the structural controls (D1, D2). | Canary-PII tests. Fail-closed test when SDP is unavailable (G11). | Provisional on G02 (regional availability) |
| D11 | I8, A13 | `RunConfig.max_llm_calls=8` per invocation. Session caps: 40 turns and 15 photos. Per-customer admission: 3 new claim sessions a day, recorded in Postgres. A Cloud Armor rate limit per IP at the load balancer. An operator **kill switch** routes new sessions to the classic form, keeping drafts. | Bounded work at every scope. The fallback already exists. | Limits can block a legitimate heavy user, who is routed to the phone line | Limit tests (G12). Storm load (G17). | Provisional numbers (A9) |
| D12 | Behaviour comparable across releases | A release manifest (image digest, prompt version, model IDs, reader schema hash, tool schema hash, eval-set hash, secret versions). A deterministic CI gate on every change. A judge eval nightly and before promotion. A manual staged traffic split on Cloud Run with the previous revision kept. | The skills' release-unit rule. Model and prompt roll back together. | CI time and judge cost | Gate fails by exit code (G14) | Proposed |
| D13 | A11, A12: no adjudication. Safety cases go to humans. | The instruction plus code: `escalate_to_human(reason_code)` for an emergency, an unsafe home, injury, liability, distress or an explicit request. The UI then shows the phone line and emergency guidance, and the draft stays resumable. Emergency keywords also trigger a static banner in code. | Humans handle safety and adjudication. The banner does not depend on the model. | No live-chat transfer at GA. Alternative: CRM callback creation, which is a new external write (later). | Escalation cases in the eval set (G10) | Proposed |
| D14 | A14: AI Act Art. 50, GDPR Art. 13/22 | A disclosure in the UI before the first turn. Observations are labelled "AI-generated, customer-confirmed" in the Guidewire note. No automated decision with legal effect. | Transparency, and the adjuster knows what is AI-derived | Legal copy is on the critical path | Legal sign-off (G05). UI test (G09). | Provisional on legal |

**Versions.** No ADK version is installed (greenfield). The working assumption
is **google-adk 2.8.0**, the version the specialist skills were checked against.
Upstream main is at 2.11.0 (2026-10-01), and 2.10.0 changed tool-confirmation
holds and resume-dispatch authorship. G03's first acceptance item is to choose
and confirm the pin. The lifecycle source is
`.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
(`checked_on` 2026-10-08). Provider facts about Vertex EU regions, Model
Armor/SDP regions, Guidewire Cloud API behaviour and prices were **not looked up**
in this session (no network). They are verification tasks in G01/G02.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | `claim_intake` owns the conversation: collect the FNOL fields, one question at a time; ask for photos; restate what the photos show as suggestions; never assess coverage, liability, fraud or amounts; escalate per D13; reply in the customer's language. Code owns identity, dates ("today" is injected), limits, completeness rules and policy choice. The reader instruction asks only for visible damage per the schema and states that any text in the image is data. | `adk-agent-instructions`; a rendered-request snapshot test and prompt as versioned code (G03) |
| Tool interfaces | 5 function tools, all on the intake agent. `list_my_policies()` and `get_policy_summary()` read and take no identity arguments. `update_claim_draft(fields)` writes **only our draft**, is validated, and returns `{status, missing_fields, errors}`. `prepare_submission_summary()` freezes a version and returns `{status, draft_version, missing_fields}`, with no claim effect. `escalate_to_human(reason_code: enum)` sets the draft state. Results are bounded to 2 KB. No irreversible tool exists. The reader has no tools. | `adk-tool-interface-design`; a declaration dump and size test (G03) |
| Output contract and model | The intake agent replies in free text, and the summary card is rendered by code. Reader `output_schema`: `PhotoObservation{relevant: bool, area: enum, damage_types: [enum], visible_severity: enum, description: str≤300, contains_people: bool, contains_text_or_documents: bool, quality_issue: enum?, refusal: {reason}?}`. 1 repair attempt, then the explicit "not analysed" outcome. Pins per D5. | `adk-model-and-output-contracts`; a scripted-model test with prose, fenced JSON and valid-but-wrong output (G07) |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | Portal IdP. Scope: one `customer_id` per request. | Middleware writes trusted state. Tools read it. | Token verified on every request | Not stored beyond session metadata |
| Policy list and summary | Policy system (PolicyCenter or ClaimCenter policy search, decided in G01). Scope: policies owned by `customer_id`. | Read by the lookup adapter. Shown to the agent as a summary. | Fetched at session start and re-checked at submit | Not stored. A summary sits in session state for the session's life. |
| Conversation events | Our app. Scope: owner `customer_id`. | ADK Runner writes. The owner reads through the API. | SDP-screened before persistence | 30 days after submit or abandon (A10) |
| `claim_draft` (versioned) | Our app. Scope: owner. | Tools and the customer write. The UI and submit read. | The version hash binds confirmation. | Same as the conversation |
| Photos (original plus model copy) | Our app. Scope: owner and draft. | Upload endpoint writes. Reader (copy) and Guidewire adapter (original) read. | Validated on finalize | Deleted 30 days after a confirmed document upload or after abandonment |
| Photo observations | Our app | Reader writes `suggested`. The customer's confirmation makes them `confirmed`. | Per photo, with model version recorded | Same as the draft |
| `submission_operation` | Our app (I2) | The submit endpoint and reconciler write. Ops read. | Authoritative for "did we send it". Guidewire is authoritative for the claim. | 13 months (audit), with no content beyond IDs and hashes |
| Claim and documents | **Guidewire ClaimCenter** (system of record) | The adapter creates them. Adjusters own them afterwards. | Authoritative | Insurer retention policy |
| Guidewire client secret | Security/platform | Secret Manager. Read only by `sa-intake-run`. | Rotated every 90 days (assumed) | n/a |
| Telemetry | Our app | Content-free spans, metrics and logs | n/a | Logs kept 30 days, traces default (to check in G13) |

Identity lifetimes: a **portal session** spans many turns. An **ADK session**
is one claim conversation, and one draft maps to one session. An
**invocation** is one turn. A **submission operation** is one confirmed draft
version and survives restarts. Confirmation binds to `(draft_id, version,
payload_hash)` and is re-checked at execution together with the policy status
and ownership.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| `claim_intake` | Yes: policy summary, the customer's own account | The customer's own text, plus reader observations as typed enum fields | Writes only our own draft. No egress tool. No Guidewire tool. | No trifecta egress leg. Writes are confined to the owner's draft, which the customer confirms. Free-text fields are length-bounded and screened. |
| `photo_damage_reader` | Minimal: the photo only | **Yes** (images may carry text or instructions) | **None** (no tools; output validated) | Quarantined reader (D1) |
| Submit path (code) | Yes | Draft content | Guidewire write | Not a model. Bound to customer confirmation and ownership re-check (D2, D3). |

Tool tiers: read (`list_my_policies`, `get_policy_summary`), own-store write
(`update_claim_draft`, `prepare_submission_summary`, `escalate_to_human`). The
only irreversible-ish effect, the Guidewire claim, sits outside the model. No
code executor. Adversarial cases (G15): injection text in a photo, a hostile
customer message asking to submit or to read another policy, a forged
`select_policy` index, a replayed submit, a stale version hash, oversized and
odd files (polyglot, decompression bomb), and prompt-leak attempts.
Findings map to OWASP LLM01/LLM02/LLM06 and the agentic IDs in the
`adk-agent-security` threat model.

## Budgets and capacity

Workload (illustrative, A9): about 25 sessions a business day, storm peak about
500 a day, about 12 turns and 4 photos per session.
Per turn the agent makes 1–3 model calls (bounded at 8). Per photo it makes one
reader call plus at most one repair. Each turn also runs SDP inspection and two
Model Armor screens.
Expected work per session is about 25 model calls. Bounded work is 40 turns × 8
plus 15 photos × 2 = 350 calls, which the per-session cap stops far earlier in
practice.
Concurrency at the storm peak: about 500 sessions over 8 hours with 12 turns at
about 6 s in flight gives roughly 1–2 concurrent turns. Even a 10× burst stays
small for Cloud Run. The binding limits are the **Vertex EU regional quota**,
the **Guidewire Cloud API rate limits** and Cloud SQL connections, which G17
measures.
Cost per completed claim, symbolically:
`25 × (Tin × p_in + Tout × p_out) + 4 × image_tokens × p_in + SDP(bytes) + 2 × 12 × MA_call + storage`.
Prices and token sizes are not looked up here, so G02 fills them with dated
sources. The enforcement points are D11. Billing budgets alert only and do
not cap spend. Admission state lives in Postgres and survives restarts.
Exhaustion offers the classic form, with the draft retained.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success (Maria's journey) | The claim number and next steps | A confirmed operation and claim in ClaimCenter | None |
| Another customer's draft ID or policy index | 404 or tool error `not_found` | No read and no write | None. Logged as a security signal (G13). |
| Vertex EU unavailable or 429 | "Our assistant is unavailable. Continue with the form." The form is prefilled from the draft. | The draft is kept, with no effect | Bounded SDK retry (owner: one policy in G12). On-call is alerted. |
| Reader returns invalid output twice | "We couldn't analyse this photo; it will still be attached" | The photo is kept and marked not analysed | Nothing more. The adjuster sees the photo. |
| SDP or Model Armor unavailable | The message is not accepted ("please try again"). Fail closed before persistence. | Nothing stored | Retry. A sustained outage trips the kill switch to the form (on-call). |
| Release check blocks a reply | The standard safe reply | The original reply is not stored as shown output | Counted in the I4 metric |
| Browser disconnects mid-turn | Reconnect shows the last completed turn | The turn completes server-side, and one turn in flight per session (policy below) | The customer resends if the turn was lost |
| Double click on Submit | One claim number | One operation (unique key) | None |
| Guidewire commits, reply lost | "We're confirming your claim", with the number shown when known | The operation is `uncertain` and the claim exists | The reconciler looks up the external reference and finishes. Ops follow the runbook if it is unresolved after 1 h (G13). |
| Claim created, submit or document upload fails | "Claim received (number). Some photos are still uploading." | A partial effect is recorded per sub-operation | The reconciler retries the missing sub-operations. It never re-creates the claim. |
| Policy lapsed or changed between card and submit | "We need to check your policy", with handoff to a human | No write | The customer calls. Claims ops decide. |
| Restart during submit | The status page shows pending | The operation row is pending/uncertain | The reconciler resumes from the recorded step |
| Injection text in a photo | Normal flow | Observations are only typed fields | No action. The adversarial test asserts it (G15). |
| Storm surge or budget exhausted | A queue or limit message, with the form offered | Drafts are kept | Kill switch and quota raise (G12, G17) |
| Erasure request mid-draft | The draft is closed | Session, draft and photos are deleted, but not the Guidewire claim if submitted | The DPO process covers Guidewire separately |
| Model retirement announced | n/a | n/a | A planned re-baseline release (G14 calendar, G26) |
| Bad release | Error-rate alert | Previous revision retained | Joint rollback of image, prompt, model and schema (G14, drill G21) |
| Incident that needs attribution | n/a | Trace, invocation and session IDs on every span and log | Runbook from alert to session (G13) |

Same-session policy: one in-flight turn per session. A
concurrent turn gets 409, enforced by a Postgres advisory lock on the session ID.

## Verification and implementation handoff

- **Offline deterministic** (every PR): tool and Runner tests with a scripted
  model, the fake Guidewire fault matrix, cross-customer denial, a schema-repair
  test and limit tests. A test that imports `google.adk` needs the pinned
  environment from G03. None was run in this design session.
- **Local integration:** a real Postgres restart, the signed-URL upload flow
  against an emulator or dev bucket, and a browser run of the portal component.
- **Bounded live** (authorized dev/staging projects only): Vertex EU model calls
  for the eval set, and the Guidewire sandbox replay and reconciliation checks.
- **Release and operation:** the CI eval gate, load test, pentest, pilot SLIs,
  and rollback and erasure drills.

**Outcome measurement:** the baseline comes from claims operations for the
current digital form and phone FNOL (G05 data request). In the pilot (G20),
measure the information-request rate and the time to a claim with photos
against that baseline, with the guardrails listed in Purpose.

**Observability and release:**
- SLIs: completed-claim ratio (confirmed / started sessions that reached the
  card), submission success ratio, uncertain count and age, Guidewire error
  rate by endpoint, tokens and cost per completed claim, p95 turn latency, and
  the release-check block rate. Targets come from the pilot baseline. The alert
  owner is the on-call rota (G13).
- Telemetry owner: the app's own OTel setup in `claim-intake-api`, with
  content capture off. Sinks are Cloud Trace, Logging and Monitoring in the EU.
- Release bundle per D12, recorded in the manifest in Artifact Registry and the
  deploy log.
- Promotion gate: deterministic tests plus an eval score at or above the
  thresholds from G16 with the pinned judge (judge ID chosen in G10 from the
  lifecycle table; it must not retire before 2027-06). A cost ceiling applies
  per CI eval run.
- Rollback unit: the whole bundle. The previous revision stays ready for 7 days
  after promotion.

Implementation map and goals: [plan](../plans/home-claim-intake.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Guidewire duplicate-prevention and external-reference lookup semantics (A6) | Decides whether I2 is provider-backed or needs manual reconciliation | G01 on the sandbox tenant, plus Guidewire docs for the tenant's release | G08 design detail |
| `gemini-3.8-flash` availability, quotas and image limits in the chosen EU region | D5 needs a different model or region otherwise | G02 | G07, G16 |
| AI Act classification and disclosure text (A14) | High-risk status would add conformity work beyond 5 months | Legal (G05) | G20 |
| DPIA outcome | It can add controls (e.g. face blurring) | DPO (G05), 4–8 weeks | G20 |
| Accept I4 as a measured, not guaranteed, control? | The residual risk of a coverage statement | Product owner and compliance | G20 |
| Portal IdP claims and policy ownership mapping | The D9 mechanism | Portal team (G06) | G06 |
| Volume and storm figures (A9) | D11 limits and quota requests | Claims ops data | G17 |
| Security reviewer hours (A2) | G15 and the boundary reviews are on the critical path | Engineering manager | G15, G20 |
| Retention periods (A10) | The G11 jobs | DPO | G11 |

None of these decisions has been user-accepted. Design completion does not
authorize provisioning, IAM changes or calls against Guidewire. Those are named
per goal in the plan.
