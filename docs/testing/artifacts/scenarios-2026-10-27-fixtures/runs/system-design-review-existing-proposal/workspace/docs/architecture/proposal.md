# Proposal: travel desk assistant

Author: Jonas Weber, 2026-10-02. Status: draft for review. **Superseded in part: see `design-revised.md`**
(tenant identity, retrieval, approval and lost-reply handling do not meet K1–K4 as written below).

## Overview

```text
browser (web/chat.js) --HTTPS JSON--> Cloud Run: FastAPI + ADK agent --+--> shared document index
                                                                        +--> booking provider API
```

- **Browser chat client.** A small JavaScript client posts each message as JSON:
  `{"tenant_id": "...", "traveller_id": "...", "message": "..."}`. The client reads `tenant_id` and
  `traveller_id` from the profile the OIDC login page stores in local storage.
- **Agent service.** One FastAPI app on Cloud Run with an in-process ADK Runner. The request's
  `tenant_id` is written to session state (`tenant_id`) and the tools read it from there.
- **Document index.** One shared vector index holds every customer's travel policies and
  itineraries (about 40,000 chunks), each chunk tagged with `tenant_id`. `search_documents`
  queries the index for the top 20 chunks, then keeps the chunks whose tag matches the session's
  `tenant_id` and returns them to the model.
- **Booking changes.** The model calls `change_booking(booking_ref, changes)`. Before calling it,
  the instruction tells the model to "ask the traveller to confirm". The tool generates a new
  `operation_id` (UUID4) for the provider call; on a timeout it waits two seconds and calls again
  with a fresh `operation_id`, up to three attempts, and tells the traveller the change is done
  when any attempt returns 200.

## Why this shape

- One index is cheaper than one per customer.
- Taking the tenant from the request keeps the service stateless.
- Retrying on timeout hides the provider's occasional slowness (p99 around 9 s).

## Open questions

- Does the booking provider offer an idempotency key or a way to look up an operation? (Asked
  the provider on 2026-10-01; no answer yet.)
- Should approvals be recorded anywhere?

## Not decided

Hosting region, logging retention.
