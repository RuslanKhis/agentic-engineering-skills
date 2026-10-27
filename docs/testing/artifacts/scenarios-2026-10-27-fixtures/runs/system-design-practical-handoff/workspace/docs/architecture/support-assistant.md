# System design: ADK support assistant (pilot)

Status: **draft**. No scope-gate answers were available (non-interactive run), so every provisional decision rests on the assumed answers below. Nothing here is user-accepted except what the request states: React, OIDC, PostgreSQL and Cloud Run are kept; users can save and delete a reply language; replies stream; failures are shown honestly; preferences are individual (the group-account question is outside this release); verified login supplies the user ID. Plan, capacity and finish range: [docs/plans/support-assistant.md](../plans/support-assistant.md).

## Assumed answers (nobody could be asked)

| # | Question I would have asked | Assumption I proceed on | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | Deadline, and is it continued after the pilot? | No deadline; continued | Phase 1 code is kept, not thrown away (D1, D8) |
| Q2 | Who builds, hours, ADK/GCP familiarity? | One developer, part time, new to ADK; 6 h/day × 0.6 focus = 3.6 focused h/day | Estimates carry a ×1.5 ADK multiplier (plan) |
| Q3 | Model and cloud allowance? | Small; the owner sets a model spend cap before any live call | G08 blocked on W3; C8 |
| Q4 | Who uses it, how many, who judges it? | Pilot users sign in through the existing OIDC provider, tens of users, not public | C8 allowance, D9 single instance |
| Q5 | Where is the existing React app, and does the assistant have its own URL? | A React app exists but its source is not available here; the assistant is a new FastAPI service on Cloud Run | G03 first step inspects the app, else builds a throwaway shell (D2) |
| Q6 | What data, what effects? | Support conversation text may contain personal data; the saved language is a per-user setting; no tools, no external writes | Floor, SB17/SB18, G12 governance |
| Q7 | Which reviews need a presentation? | A business go/no-go before the Cloud Run pilot (G07); dates unknown | W2 |
| Q8 | Lock-in concern? | No | No portability goal |
| Q9 | Client contract, proposal or statement of work? | No | None |
| Q10 | OIDC issuer, audience, token type, and does a verified bearer token reach our API (or a gateway header)? | A signed JWT bearer token our backend verifies against the issuer's JWKS; user ID is the pair `iss` + `sub` | C1, G04 (fixture issuer), G10 (real issuer, W1) |
| Q11 | Is there an existing PostgreSQL instance we may use? | Yes, a new schema for this application; ADK session tables in a separate schema | D3, D8; a new Cloud SQL instance would add a charging resource (G09) |
| Q12 | Which languages? | A code-owned allowlist of BCP 47 tags; the product owner supplies the list. Unset means "reply in the language the user wrote" | C2, C4 |
| Q13 | Does deleting the preference also purge past conversations? | No: it deletes the preference only; conversation retention is a separate policy (G12). The UI says so | C3 |
| Q14 | Must a conversation survive a restart? | Yes (Cloud Run restarts and scales) | C9, D8, G05 |
| Q15 | Group-account preferences? | Out of scope. Key stays `(issuer, subject)`; no speculative owner-type column | C2, Later |

## Purpose and constraints

**Journey.** A signed-in user opens the assistant, picks "reply in French" in settings, asks a support question and watches the answer arrive word by word in French. A later visit still uses French. They delete the setting and replies go back to the language they write in. If the model or network fails halfway, they see the partial text marked incomplete with a retry, never a finished-looking answer.

**Friction and outcome.** No baseline exists, so none is claimed. Outcome measure for the pilot (hypothesis, owner to confirm): share of replies in the user's saved language (C4, measured at G08), and share of failed runs that the user could distinguish from a completed answer (C6, G03).

**Model versus code.** The model writes the reply. Code decides identity, which preference applies, whether a run may start, what counts as finished and what the user is told. The agent has no tools in this release, so it cannot change a preference; a user asking "reply in French" in chat gets a per-message reply, and saving still happens only through the settings UI.

**Existing and fixed:** React frontend, OIDC login, PostgreSQL, Cloud Run. Observed facts: none; no source tree was provided. ADK version unselected; the specialists were checked against `google-adk` 2.8.0 and a gateway tested offline on 2.12.0 (frontend compatibility reference). G01 confirms the pin.

## Delivery constraints, depth and deferred controls

Profile: **MVP or pilot** (the request says accepted pilot). Phase 1 is local only, because this request authorises documentation only and local implementation is the next phase.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core journey end to end, measured | Build: scripted-model tests (G01–G06); live adherence measure in G08 | Model or prompt change re-runs G08 |
| Identity and per-user scope | Build (G04); real IdP in G10 | n/a, built now |
| Application data and deletion | Build (G02) | Group accounts (Later) |
| Streaming and honest failure | Build (G01, G03) | n/a |
| Spend and abuse | Build: per-user allowance, one active run, `max_llm_calls`, model quota (G05, G08) | More than one instance (shared limiter) |
| Memory and retrieval | Sessions only (G05); no RAG, no Memory Bank | A knowledge-base requirement |
| Observability | Minimal local, build in G11 | Pilot go-live |
| Release engineering | Minimal pins in G01, build in G11 | Pilot go-live |
| Governance papers | Phase 2 (G12) before pilot go-live | Real users or real data |
| Performance tuning | Defer | Measured first-token latency above target |

Floor kept: no secrets in source, prompts or logs (SB16); `max_llm_calls` plus an owner-set model spend cap (C8); no outward effects at all (the agent has no tools); no real personal data in phase 1 (synthetic only); every `/api` route fails closed (C1); model ID pinned (G08). Accepted risks: none yet. Who may use it: the builder with synthetic data in phase 1; signed-in pilot users from G09 on. **Graduation conditions** before real users: G08 to G12 evidenced and the go-ahead wait W2 resolved.

## Requirements and contracts

| ID | Requirement | Status |
| --- | --- | --- |
| R1 | A signed-in user can save a reply language (individual preference) | Confirmed |
| R2 | The user can delete it | Confirmed |
| R3 | Replies stream | Confirmed |
| R4 | Failures are shown honestly | Confirmed |
| R5 | Keep React, OIDC, PostgreSQL, Cloud Run | Confirmed |
| R6 | Conversations survive a restart | Assumed (Q14) |
| R7 | Spend and abuse are bounded | Assumed (floor, pilot) |

| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1, R2, R3 | The acting user is the verified token's `iss`+`sub`; a client-supplied user ID, session ID or body field never selects authority; with no verifier configured every `/api` route returns 401 | Every `/api` call and every ADK call | OIDC provider's signed token | Verified-principal dependency; user ID overwritten on each Runner call; session lookup filtered by owner | 401, or the same 404 as an unknown session; zero model calls | planned: G01/A1, G04/A1–A4, local; real IdP G10/A1 |
| C2 | R1 | At most one saved reply language per user, from the allowlist; reads, writes and deletes touch only the caller's row | Per user | PostgreSQL row keyed `(issuer, subject)` | Request model with allowlist; owner-scoped queries (no ID in the path); allowlist checked again on load | 422 and the old value stays; 503 if the store is down | planned: G02/A1, A2, A6, A9, local |
| C3 | R2 | After DELETE returns, the row is gone and no later run, session state, event or log we write holds the value | Per user | PostgreSQL | Hard `DELETE`, no tombstone; the value is never copied into session state or events (D4) | Retry is safe; a failed delete is shown as failed | planned: G02/A3, A4, A7, local; backups: gap, G12 |
| C4 | R1 | A run's reply-language instruction comes from the stored value loaded by code at run start, as a fixed phrase for an allowlisted tag; it is an instruction, not a guarantee, and adherence is measured | Per run | PostgreSQL via trusted code | Loader in the run route; allowlist check on load; a bad row is dropped with a warning | If the store is down the run proceeds in the user's language and a `notice` event says so | planned: G02/A4, A5, A10 local; G08/A2 live |
| C5 | R3 | The first reply text reaches the browser before the model finishes; every stream ends with exactly one terminal event (`done` or `error`); nothing follows it | Per run | The server's event stream | Run route owns the stream and its schema; client treats a stream that ends without a terminal event as an error | Browser sees `error`, or detects truncation and shows "connection lost" | planned: G01/A2–A4, A11; G03/A1, A11 local; G09/A3 hosted |
| C6 | R4 | A failed or cut-off reply is never presented, stored or counted as a completed answer; errors carry a generic message and a request ID, never provider text | Per run | Server error mapping | Terminal `error` event with a code and `partial: true`; the UI marks the text incomplete; one exception handler | Partial text kept, labelled incomplete, with retry | planned: G01/A3, A5, A7, A12; G03/A2, A8, A11 local |
| C7 | R1, R2, R4 | The UI shows a language as saved or deleted only after the server confirmed it by a successful reply and re-read; on failure or an unknown outcome it shows the real server state | Per user | The server's GET | Client re-reads after a write and after a timeout | "Not saved, still X" or "couldn't confirm, checking" | planned: G03/A3, A4, A5, local |
| C8 | R7 | A run needs a free slot (one active run per user), is bounded by `max_llm_calls` and the per-user daily allowance, and the model project has a quota; exhaustion refuses before any model call | Per user and per model project | Server counters; model project quota | Admission check in the run route; `RunConfig.max_llm_calls`; quota on the model project | 409 or 429 with a message and reset time; `limit_reached` event | planned: G05/A2–A6 local; G08/A3 live. Allowance values: owner to set (O3) |
| C9 | R6 | After a restart a user sees their own earlier completed turns, and only theirs; an incomplete turn is not shown as complete | Per user session | `DatabaseSessionService` tables | Session ownership check; incomplete-turn handling from D6 | Older turns missing is an error, not a silent empty chat | planned: G05/A1 local |

## Architecture and decisions

```text
Browser (React) --fetch+Bearer--> Cloud Run: one FastAPI process
   ^  SSE-style events                |- principal dependency (C1)       -> OIDC JWKS (cached)
   |  delta|notice|done|error         |- /api/me/reply-language (C2,C3)  -> PostgreSQL: app schema
   +----------------------------------|- /api/chat/stream (C4-C6,C8)     -> ADK Runner (no tools) -> Gemini
                                      '- sessions (C9)                   -> PostgreSQL: ADK schema
```

Trust boundaries: browser to API (token verified), API to model (instruction built only from code and allowlist), API to PostgreSQL (owner filter). ADK's own server routes are never exposed (SB05).

| ID | Enforces | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | R5 | Keep the React SPA; call `/api` with `fetch` and a bearer header; the generated client covers JSON routes and the stream is read with `fetch` plus a reader | Native `EventSource` cannot send headers (SB08) | A hand-written stream reader instead of a library; AG-UI/CopilotKit rejected: needs a Node runtime and shared-state features this journey lacks | G03/A7, A8 |
| D2 | R5 | New FastAPI service runs the ADK Runner in process behind the principal dependency, serves `/api`, and (later) the built SPA | One identity seam; fewer moving parts on Cloud Run | If an existing backend must host it, the route module moves; G03 inspects the React app first | G01/A1, A6 |
| D3 | C2, C3 | Reply language is an application-owned row, not ADK session state, Memory Bank or RAG | It is an exact setting; hard-delete is one statement; ownership is explicit | ADK `user:` state would be less code but is persisted inside ADK tables and harder to erase and audit | G02/A3, A4 |
| D4 | C3, C4 | The language instruction is rendered per run from the loaded value and is not written to session state or events | A copy in session history would survive DELETE | Each run costs one indexed lookup; the exact ADK mechanism (instruction provider vs a `temp:` state key) is an investigation at G01/G02 against the pin | G02/A4 rendered-request test |
| D5 | C5, C6 | Custom event contract: `delta` (text), `notice`, `done`, `error {code, retryable, partial, request_id}`, validated at run time in the browser | The server owns what "finished" means | A custom contract is ours to version; `adk-frontend-integration` owns it | G01/A2, A3; G03/A8 |
| D6 | C6, C9 | On failure after partial text the server emits `error`; the incomplete assistant turn is not stored as a completed turn. How ADK persists partial events on a mid-stream failure is unverified | Honesty needs the persisted state to match the screen | May need a marker or cleanup step in our code; scope depends on the finding | G01/A7 |
| D7 | C1 | Backend verifies issuer, audience, expiry, signature, algorithm allowlist and `kid` against cached JWKS; local runs use a dependency override that refuses to load outside a dev setting | The login supplies the ID; we never trust client fields | Cache means a short window where a revoked key or token is accepted; SB20 handles sensitive actions in G10 | G04/A1–A4 |
| D8 | C2, C9 | One PostgreSQL instance, two schemas (application, ADK sessions); migrations run as a job and never touch ADK's tables; `DatabaseSessionService` in G05 | Isolation and clean erasure | Cross-schema backups share lifecycle; a separate instance is the alternative | G02/A9, G05/A1 |
| D9 | C8 | Pilot runs one Cloud Run instance (`max-instances` 1) with a process-local run lock; overlapping revisions during a deploy are accepted for the pilot | Avoids a shared limiter now | Brief double-instance window at deploys; availability ceiling; trigger: more than one instance | G05/A3, G09 |
| D10 | C4 | The agent has no tools, no output schema; reply language is a fixed phrase from a display-name map in code; the model ID is chosen from the dated lifecycle table at G08 | The model cannot write a preference; an allowlisted tag cannot carry an instruction | Adherence is probabilistic, so it is measured, not promised (C4) | G01/A10; G08/A2 |

### Model-facing interfaces

| Surface | Interface | Implementing skill and verification |
| --- | --- | --- |
| Instructions | One short support-assistant prompt plus the language phrase; kept as versioned code | `adk-agent-instructions`; G02/A4–A5 rendered-request test |
| Tools | None | `adk-tool-interface-design` only if a tool is later added; G01/A10 asserts zero tools |
| Output and model | Free text, no schema; model ID unresolved (O4) | `adk-model-and-output-contracts`; G08 |

## Data and authority

| Data | Owner and scope | Writers / readers | Lifetime / erasure |
| --- | --- | --- | --- |
| `reply_language(issuer, subject, language_tag, updated_at)` | The user | The user via `/api/me/reply-language`; the run loader reads | Hard delete on request; Cloud SQL backups keep it until they expire (gap, G12) |
| ADK sessions and events | The user | The Runner | Retention policy: open (G12); never holds the language |
| Logs | Operator | The service | No prompts, replies or tokens (SB14) |

Identities: session ID locates a conversation; invocation ID identifies one run; there is no business-operation ID because nothing is written outside the user's own settings.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Support assistant | The user's conversation and language | The user's messages | None | Remove a leg: no tools, so an injected instruction cannot cause an effect (G01/A10) |

#### Web security baseline (tiers 1 to 5)

| Rule | Component | Depth now | Proved by |
| --- | --- | --- | --- |
| SB01 | `/api` routes | Build | G01/A1 |
| SB02 | Real OIDC login | Minimal, phase 2 | G10/A1 |
| SB03 | Run and session routes | Build | G04/A2, G04/A3 |
| SB04 | Preference records | Build | G02/A2 |
| SB05 | ADK server not exposed | Build | G01/A6 |
| SB06 | Same origin or allowlist | Build | G09/A4 |
| SB07 | Docs and schema off, headers | Build | G09/A4 |
| SB08 | Bearer in header | Build | G03/A7, G04/A5 |
| SB09 | Input bounds | Build | G02/A8, G05/A5 |
| SB10 | Browser rendering | Build | G03/A6 |
| SB11 | Uploads | n/a: no uploads in this release | none |
| SB12 | Outbound fetch | n/a: no URL-fetching tool or route | none |
| SB13 | Errors | Build | G01/A3, G04/A4 |
| SB14 | Logging | Build | G04/A5, G11/A1 |
| SB15 | Dependencies | Minimal | G06/A4 |
| SB16 | Secrets | Build | G01/A9 |
| SB17 | Agent with tools | Build (no tools) | G01/A10 |
| SB18 | Tools with effects | n/a: no tools | none |
| SB19 | Cost and abuse | Build | G05/A2, G05/A3 |
| SB20 | Token revocation | Build, phase 2 | G10/A2 |
| SB21 | ZAP baseline on staging | Build, phase 2 | G09/A5 |
| SB22 | ASVS L1 review | Build, phase 2 | G10/A3 |
| SB23–SB25 | Production tier | deferred: production profile | none |

## Budgets and capacity

Workload assumptions (provisional, owner to confirm, O3): tens of pilot users; one active run per user; at most one model call per turn since there are no tools, so `max_llm_calls` is set low. Target first-token latency: none stated yet; G08 measures it and the owner sets a target. Cost contract for the pilot (C8): ceiling = daily per-user allowance × users × measured cost per run, enforced by refusal and the model project quota, not by an alert; variable part = model tokens, fixed part = Cloud Run and PostgreSQL (read from current pricing at G09, not checked here); G13 reads the first live bill against it.

## Failure and recovery

Coverage grid:

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OIDC provider and JWKS | G04/A4 | G04/A1 | n/a: verification only reads | n/a: one verification step | G10/A2 | n/a: keys are cached, not fetched per request | n/a: stateless verification | G04/A1 |
| PostgreSQL | G02/A10 | G02/A1 | G03/A4 | n/a: single-row, single-statement writes | G09/A2 | G05/A6 | G02/A7 | G02/A5 |
| Model backend | G01/A11 | G01/A5 | n/a: a model call has no outward effect | G01/A3 | G08/A1 | G01/A12 | G05/A3 | G01/A5 |
| Browser to Cloud Run stream | G03/A11 | G03/A3 | G03/A4 | G03/A2 | G03/A12 | G05/A4 | G05/A3 | G03/A8 |

Action grid:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Save reply language | G02/A2 | n/a: one row, one statement | n/a: no confirmation step | G03/A4 | G02/A7 |
| Delete reply language | G02/A2 | G02/A4 | n/a: no confirmation step | G03/A4 | G02/A3 |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state | Next action and owner |
| --- | --- | --- | --- |
| Model fails after partial text | Text marked incomplete, error with request ID, retry | Incomplete turn not stored as complete (D6) | User retries; engineer owns the error mapping |
| Browser disconnects mid-run | Nothing to see; reload shows completed turns only | Run cancelled, slot released (G01/A4) | None |
| Cloud Run timeout cuts the stream | "Connection lost", partial text kept as incomplete | As above | Retry; G09/A3 sets the timeout |
| Delete during an in-flight run | That run finishes with the old value; the next uses none | No row, no copy | None (G02/A7) |
| Preference store down at run start | Reply in the user's language plus a notice | Nothing | Operator restores the database |
| Token expires mid-session | Prompt to sign in again, draft message kept | None | User (G03/A12) |
| Rollback of a deploy | Previous revision serves | Application schema migrations are additive until a rollback plan exists | G09 |

## Verification and implementation handoff

Offline and local: scripted-model tests through the real Runner and real sockets, a real process restart for persistence, Playwright for the browser journey (G06). Live: G08 only, with declared call and spend limits. Hosted: G09. Nothing here has run; all evidence is planned.

Release bundle (G11): image or revision, prompt version, model ID, secret versions, eval-set hash. Rollback unit: previous Cloud Run revision kept ready.

## Open decisions

| ID | Question | Why it matters | Owner | Blocks |
| --- | --- | --- | --- | --- |
| O1 | OIDC issuer, audience, token type, how the token reaches us (Q10) | C1 verification details | Whoever runs the IdP | G10 (W1) |
| O2 | Existing React app location and conventions (Q5); existing PostgreSQL instance (Q11) | D1, D2, D8 | Builder, from the repo | G03 integration; G09 |
| O3 | Allowance values, user count and model spend cap | C8 | Product owner | G05 values; G08 (W3) |
| O4 | Model ID, from the dated lifecycle table in `adk-model-and-output-contracts` (not installed here) | Pinned model | Builder | G08 |
| O5 | Supported language list (Q12) | C2 allowlist | Product owner | G02 final values |
| O6 | Does partial-turn persistence in ADK match D6? | C6, C9 | Builder, at G01 | G05 |
| O7 | Pilot audience and presentation date (Q7) | W2 | Sponsor | G09 |
| O8 | Retention and backup erasure statement | C3 gap | Counsel, DPO | G12 |
