# Synthetic provider adapter

Python 3.11.4; httpx 0.28.1. Preserve these pins and the `Gateway` constructor,
`lookup(reference)` and `refund(reference, amount)` async signatures. The caller
supplies and closes its authenticated `httpx.AsyncClient`, with a trusted base
URL and finite transport timeouts. No live service or ADK agent is supplied.

GET `/status` takes a `reference` query parameter. A valid success is an object
with the requested string `reference` and `state` in `ready`, `pending`.
POST `/refunds` takes `reference` and `amount`. Amount is a positive finite
decimal string with two fractional digits for this fixture's fixed USD currency.
A valid confirmed refund has a nonempty string `refund_id`, matching reference
and amount, and `status` equal to `applied`. A 2xx response alone does not prove
that contract. The provider has no protected replay facility. Once dispatched,
an invalid or lost response cannot establish that the refund was not applied.

Public results always retain `ok`, `data`, `reason`, `outcome`. Success uses the
validated provider object as `data`; failure uses `data=None` and a safe reason.
Read outcome is `read` on success and `unavailable` on error. Refund outcome is
`applied`, `unknown` after uncertain dispatch, or `not_attempted` for invalid
input. This fixture's caller handles authorisation/approval before invoking
the adapter. Do not invent a ledger or a new approval interface here.

Provider response bodies and exception messages can contain sensitive fields;
safe diagnostics must preserve error classification without disclosing them.
All tests must use a local transport double. Selected retry policy can remain
conservative; no provider error in this fixture requires automatic retry.
