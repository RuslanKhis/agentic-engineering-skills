# Payments provider: refund API (excerpt we rely on)

Copied from the provider's integration guide, v3 (2026-08), section 4.

## POST /refunds

Body: `{"order_id": str, "amount_cents": int, "reason": str}`.
Success: `201 {"id": "re_...", "order_id": ..., "amount_cents": ..., "status": "accepted"}`.

Errors: `400` invalid body; `402` refund not allowed for this payment (do not retry);
`409 replay_key_mismatch`; `429`, `500`, `502`, `503`, `504` transient.

## Replay keys

Send a `Replay-Key` header (1-64 characters) on every refund request.

- A request with a key the provider has already accepted, and the same body, is not
  processed again: the provider returns `200` with the original refund and
  `"replayed": true`.
- The same key with a different body returns `409 replay_key_mismatch` and changes
  nothing.
- Keys are remembered for 72 hours.
- `GET /refunds?replay_key=<key>` returns the refund created under that key, or `404`
  if the provider never accepted a request with it.

A request can be accepted even when the client sees a timeout: the provider commits the
refund before the response is sent.
