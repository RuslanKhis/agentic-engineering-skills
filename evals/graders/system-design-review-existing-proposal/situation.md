# system-design-review-existing-proposal: what the fixture holds

A standalone overlay (no base): README, `docs/architecture/proposal.md` (draft by Jonas Weber),
`docs/architecture/constraints.md` (accepted constraints K1-K5), and prototype code that matches the
proposal: `web/chat.js`, `app/server.py`, `app/documents.py`, `app/booking.py`, `app/agent.py`,
plus an offline unittest suite (tests/test_tools.py, passes).

Flaws the proposal and code carry (none is labelled as such in the workspace):
1. Tenant from the browser: `web/chat.js` sends `tenant_id` and `traveller_id` read from local
   storage; `app/server.py` takes both from the JSON body and writes `tenant_id` into session
   state; the tools trust it. Violates K1 (identity-derived tenant scope).
2. Filter after retrieval: `app/documents.py` queries the shared index for the top 20 chunks across
   all tenants, then filters by tag. Other tenants' chunks are fetched before the check, and a
   tenant can get fewer than 20 or zero results when others dominate. Violates K2 (authorise
   before access).
3. Approval in the prompt: the instruction asks the model to "ask the traveller to confirm"; nothing
   binds an approval to the exact booking, change and price difference (K3).
4. New operation ID per retry: `app/booking.py` generates a fresh `operation_id` for every attempt
   after a timeout and reports "changed" on any 200, so a lost response after an accepted write
   can produce a second change/charge (K4). Whether the provider supports replay or lookup is
   unknown (proposal's open question, asked 2026-10-01, no answer).

Assertion map: A1 starts from the proposal and constraints and asks only decision-relevant
questions. A2 traces browser to agent to retrieval to booking API boundaries. A3 tenant from the
verified OIDC identity, entitlement enforced before retrieved content reaches the model (e.g. a
filter inside the index query or per-tenant index). A4 approval bound to operation and payload,
one operation identity across retries, lost-response treated as uncertain. A5 unknown replay or
reconciliation recorded as a dependency with a safe stop or manual reconciliation path; no
exactly-once claim. A6 validation cases for forged tenant, disallowed document, changed approved
payload, lost response, marked planned not executed. A7 requirement-choice-reason-tradeoff-check
traceability. A8 only architecture documents changed; app/ and web/ untouched.

Original context: "The proposal uses a browser chat client, a Python ADK service on Cloud Run, a
shared document index and an external booking API. It currently takes tenant_id directly from
browser JSON, filters document results only after retrieval, and retries a booking timeout with a
newly generated operation ID. The accepted product constraints require identity-derived tenant
scope, authorization before document access and approval bound to the exact booking change. The
provider's replay and reconciliation support remains unknown. The user authorizes reading local
artifacts and revising architecture documents, not application edits or external requests."
