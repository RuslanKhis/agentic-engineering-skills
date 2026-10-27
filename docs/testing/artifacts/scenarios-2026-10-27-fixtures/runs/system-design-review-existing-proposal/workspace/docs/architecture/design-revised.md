# Revised design: travel desk assistant

Status: **draft, unreviewed**. Revises `proposal.md` (J. Weber, 2026-10-02) against `constraints.md` (K1–K5).
Design only: no application code was changed. Written 2026-10-27 in a non-interactive session, so every
question below carries the assumption the design proceeds on. Decisions that rest on an assumption are
marked **provisional**.

## 1. Assumed answers

| # | Question (nobody was available to answer) | Assumed answer | Decisions that depend on it |
|---|---|---|---|
| Q1 | Does the OIDC ID token carry a tenant claim, or must we map `sub` to a tenant? | Token is verifiable (signature, `iss`, `aud`, `exp`). Tenant and traveller come from a server-side directory lookup keyed by `sub` if no trusted claim exists. | D1 |
| Q2 | Which vector store backs the index, and does it filter by metadata *inside* the query? | It supports server-side metadata restricts (e.g. Vertex AI Vector Search). If it does not, switch to one index per tenant (D2 alternative). | D2 |
| Q3 | Are itineraries visible to the whole tenant or only to the traveller they belong to? | Policies: tenant-wide. Itineraries and bookings: the traveller they belong to, plus the tenant's travel managers if a role exists. K2 says "traveller's access", so we check per document. | D2, D3 |
| Q4 | Does the provider honour `operation_id` as an idempotency key, or offer a lookup of an operation or booking state? | **Unknown, treated as no** until the provider answers (asked 2026-10-01). | D5 (provisional) |
| Q5 | Is a price difference available before the write (a quote/read call)? | Yes, via a read of the booking plus the provider's fare rules. If not, K3 cannot be met and this is a blocker. | D4 |
| Q6 | Who handles a change whose outcome stays unknown? | A Tidewater travel-desk operator via a work queue. | D5 |
| Q7 | Approval validity window | 15 minutes, single use. | D4 |
| Q8 | Retention of approval and operation records | Keep for the life of the booking plus the contract's audit period. Needs Omar Haddad's decision. | D4, D5 |
| Q9 | Scope gate (deadline, team, budget, audience) | Default: one part-time developer new to ADK, no deadline, external customers (Tidewater's corporate travellers), real data, can change real bookings. **Profile: production-bound, because it changes real bookings and holds customer documents.** Controls are not lowered for a prototype. | whole plan |

## 2. Findings in the proposal

| # | Finding | Constraint | Where |
|---|---|---|---|
| F1 | `tenant_id` and `traveller_id` come from the JSON body, which the browser fills from local storage. Anyone can edit them. | K1 | proposal Overview; `app/server.py:15-30`; `web/chat.js` |
| F2 | A client-supplied `session_id` is looked up with the client-supplied `traveller_id`, and `tenant_id` is written to state only when a session is created. | K1 | `app/server.py:24-30` |
| F3 | The index is queried for the top 20 across all tenants and filtered afterwards. Other tenants' chunks pass through the service and crowd out the caller's, so answers go missing as the index grows. Nothing checks access per document. | K1, K2 | `app/documents.py:30-33` |
| F4 | `booking_ref` is model-supplied and not checked against the caller's tenant. | K1 | `app/booking.py:30` |
| F5 | The only approval is an instruction to the model to "ask the traveller to confirm". The model can call `change_booking` without one, or with different values than were approved. Nothing is recorded. | K3 | `app/agent.py:11-12`; `app/booking.py` |
| F6 | Each retry mints a fresh `operation_id`, so the provider cannot tell a retry from a new change. A lost reply followed by a retry can charge twice. The 2 s retry also starts before the provider's p99 of about 9 s has passed. | K4 | `app/booking.py:32-41` |
| F7 | After three timeouts the tool says "the booking system did not answer", though the change may have happened. | K4 | `app/booking.py:42` |
| F8 | `InMemorySessionService` loses sessions on restart and does not share them across Cloud Run instances. | continuity | `app/server.py:11` |
| F9 | "Hosting region" is listed as undecided but K5 fixes europe-west1. | K5 | proposal "Not decided" |

## 3. Journey used as the running example

A traveller at company A asks "what is my hotel limit in Lisbon?", then asks to move the return flight on
booking TW-5HQ2KX to 14 Nov. The change costs 85 EUR more. The booking provider takes 10 seconds, and its
reply is lost.

## 4. Contracts

| ID | Contract (invariant) | Requirement | Authority | Enforcement point | Failure outcome | Planned check (tier) |
|---|---|---|---|---|---|---|
| C1 | Tenant and traveller identity for a request come only from a verified OIDC token, never from the body, the session state a client can name, or the model. | K1 | OIDC token verified by the service | FastAPI dependency; produces an immutable `Principal(tenant, traveller)` passed to tools as trusted context | 401, no processing | Offline: body with a forged `tenant_id` and a valid token for another tenant is ignored; no token or an expired one gives 401 |
| C2 | A session is used only by the traveller who created it. | K1 | Session record owner | Server loads the session by `(principal.traveller, session_id)`; a mismatch is "not found" | 404 | Offline: traveller B using A's `session_id` gets 404 |
| C3 | A document chunk reaches the model only if the principal may read it. Tenant is a mandatory filter on the query, and each result is checked again against the ACL before content is released. | K1, K2 | Document ACL record (tenant, owner traveller, role) written at ingestion | Retrieval layer in the service, below the tool. The model supplies only the query text. | A chunk without a valid tag or ACL is dropped and counted. Empty result: "I found nothing", never a guess. | Offline: seeded two-tenant corpus where tenant B's chunks outrank A's; A never receives B's and still gets a full top-k. Live: same against the real index. |
| C4 | A booking is read or changed only if it belongs to the principal's tenant (and traveller, per Q3). | K1 | Provider read of the booking, mapped to our tenant | Check in the propose step and again at execution | Refusal, "I can't find that booking" | Offline: a `booking_ref` of another tenant is refused |
| C5 | A booking change is sent only after the traveller approved that exact change (booking, segment, new values, price difference). Approval is single-use and expires. | K3 | Durable approval record, bound to a hash of the exact change | Executor refuses unless an approval for this hash, this principal and an unexpired window exists. The model has no tool that writes. | Nothing sent, state stays `PROPOSED` or `EXPIRED` | Offline: change a value after approval, expire the approval, replay it, or approve in another traveller's session: each sends nothing |
| C6 | One approved change results in at most one charge, even when replies are lost, the instance dies or the operation is retried. | K4 | The provider's own booking state | One `operation_id` is created and stored before the first send and reused on every retry. A retry happens only when D5 says the provider can deduplicate or the outcome has been looked up. | See C7 | Offline fake provider that applies the change then drops the reply: the provider receives one effective change |
| C7 | The traveller is told a change happened only when the system knows it did. | K4 | Provider confirmation or a provider state read | Status is derived from the operation record (`CONFIRMED` only on a 2xx, or a state read showing the new values). `UNKNOWN` has fixed wording: "We could not confirm the change. Don't rebook. We're checking and will tell you." | `UNKNOWN`, with an operator queue entry | Offline: every non-confirmed state yields the non-success wording |
| C8 | Retrieved text, booking data and provider replies are data and cannot grant authority. | K1, K3 | none | Structural: the model cannot write, so injected text can at most produce a proposal the traveller must approve in the UI (C5). | Proposal rejected by the traveller | Offline: a document that says "approve my change" results in no approval |

## 5. Decisions

**D1 Identity (C1, C2).** `web/chat.js` sends the ID token in `Authorization: Bearer`, and the body carries
only `message` and `session_id`. A FastAPI dependency verifies the token and builds the `Principal`. The tool
receives the principal through trusted invocation state that the server overwrites on every request, not
from client JSON. Sessions are looked up by principal, never by body fields. Tradeoff: the browser must keep
a fresh token. Local storage already holds one for the login page, and its expiry becomes a 401 that
triggers re-login. Replace `InMemorySessionService` with a durable service (F8) shared across instances.
Provisional on Q1.

**D2 Retrieval (C3).** Keep one shared index, which is cheaper, but enforce the tenant filter inside the
query and again per document. Ingestion writes `tenant_id` and an ACL record for every chunk and rejects an
untagged one. Alternative: one index per tenant. It gives a harder boundary and no recall loss, at a higher
fixed cost. Choose it if Q2 fails or the security lead prefers it. The 40,000 chunks are small enough that
the cost gap is small, so the choice should be tested rather than assumed. Provisional on Q2 and Q3.

**D3 Booking reads (C4).** Every booking reference is resolved by the service against the principal's tenant
before anything else happens. Provider credentials stay in Secret Manager and the model never sees them.

**D4 Approval (C5).** Replace `change_booking` with two parts:
1. `propose_change(booking_ref, changes)`, a read-only tool. It checks C4, fetches the current segment and
   the price difference (Q5), and stores a `PROPOSED` record containing the exact change, the principal, an
   expiry (Q7) and a hash. It returns a `proposal_id`.
2. An approval card the browser renders from the stored record, not from model text. The traveller's click
   calls `POST /approvals/{proposal_id}` with the token. The server records who and when, and the executor
   runs. The model is never in the write path.

If the provider quote changes before execution, the executor stops and a new proposal is needed. Approvals
and operations live in Firestore in europe-west1 (provisional choice), outside the session, so they survive
session loss. This also answers the open question "should approvals be recorded": yes, always (Q8).
Tradeoff: a custom UI step instead of an in-chat "yes". ADK's built-in tool confirmation could replace the
card only if it binds the approval to the exact arguments and survives across instances. Check that against
the pinned ADK version before using it.

**D5 Lost replies (C6, C7), provisional on Q4.** The operation record has these states: `APPROVED →
SUBMITTING → CONFIRMED | REJECTED | UNKNOWN`. Write `SUBMITTING` and the `operation_id` before the first
send. One attempt per approval is the default design, because we do not know that the provider deduplicates.
Read the booking before the write so a later read can tell "applied" from "not applied". On timeout:

| Provider capability (Q4) | Behaviour on a lost reply |
|---|---|
| Honours `operation_id` as an idempotency key | Resend with the **same** `operation_id`, bounded retries, with the timeout above p99 (9 s) |
| Offers lookup by operation, or a booking read | Look up the outcome; resend only if it proves "not applied" |
| Neither (assumed now) | Do not resend. Poll the booking read for a short period; if the new values appear, `CONFIRMED`. Otherwise `UNKNOWN` and go to the operator queue (Q6). |

A sweeper (Cloud Scheduler plus a small Cloud Run job) resolves records stuck in `SUBMITTING` after an
instance dies. The chat call returns "in progress" quickly and the client polls the operation status, so a
slow provider does not hold the request. Tradeoff: some changes end in `UNKNOWN` and a person handles them.
That is the price of K4 without provider support. The provider's answer can only reduce it.

## 6. Failure grid (external systems × failure)

| System | Wrong or missing identity | Timeout / lost reply | Duplicate | Stale or partial | Unavailable |
|---|---|---|---|---|---|
| OIDC | expired or forged token: 401 (C1) | verification keys unreachable: fail closed | n/a | n/a | login unavailable, no access |
| Document index | wrong tag: dropped (C3) | search error: "can't search now", no guess | n/a | stale ACL: re-check at read (C3) | same as timeout |
| Booking read | foreign booking: refused (C4) | proposal not created | n/a | price changed since proposal: re-propose (D4) | no change possible |
| Booking write | n/a | `UNKNOWN`, no blind resend (C6, C7) | same `operation_id` only (C6) | instance dies mid-write: sweeper (D5) | stays `APPROVED`, expires unsent |
| Session / Firestore | session of another user: 404 (C2) | write failure before `SUBMITTING`: nothing sent | repeated approval click: idempotent on the proposal | n/a | no sends |

## 7. Changes from the proposal

| Item | Change | Reason |
|---|---|---|
| Tenant from the request ("stateless") | Removed, replaced by D1 | F1. Verified-token verification keeps the service stateless without trusting the browser. |
| Post-filter on top-20 | Removed, replaced by D2 | F3 |
| Prompt-only confirmation | Removed, replaced by D4 | F5 |
| Retry with fresh `operation_id`, "done on any 200" | Removed, replaced by D5 | F6, F7 |
| Retry to hide slowness | Weakened: bounded retries only when the provider deduplicates, and the timeout is set above p99 | Hiding p99 slowness cannot justify a double charge |
| One shared index | Kept, with an alternative recorded | Cost |
| Open question: approvals | Closed: recorded | K3 |
| Not decided: region | Closed: europe-west1 | K5 |
| Not decided: logging retention | Still open and now matters: records in Q8, and logs must not hold document text | Q8 |

## 8. Plan (hours for one developer with a coding agent, hands-on plus review; summed by hand)

Phase 1 (security floor, before any real customer data): G1 token verification, principal and session
ownership (C1, C2) 6 h; G2 tenant-enforced retrieval with ACL and the two-tenant test (C3) 8 h; G3 booking
ownership and `propose_change` with approval record and card (C4, C5, C8) 10 h; G4 operation record, single
`operation_id`, `UNKNOWN` handling, sweeper (C6, C7) 10 h; G5 durable sessions 3 h. Total 37 h. Waits:
provider answer on Q4; Omar Haddad's decision on Q8 and on the D2 alternative.
Phase 2: operator queue UI, provider idempotency or lookup once confirmed, cost limits, observability.
Phase 3: per-tenant index if required, load tests at p99 provider latency.

## 9. Left open

- Q4 is the blocker for automating retries. Until it is answered, D5 stays at "do not resend".
- Q1, Q2, Q3, Q5, Q6 and Q8 are assumptions that need a human owner: Lena Brandt (Q3, Q6), Omar Haddad
  (Q1, Q8, D2), the provider (Q4, Q5), Jonas Weber (Q2).
- `gemini-3.5-flash` in `app/agent.py` was not checked against a model lifecycle table; confirm it before
  the plan is relied on.
- No independent review of this design has happened. Run the plan-review prompt in a fresh session before handing it to others.
