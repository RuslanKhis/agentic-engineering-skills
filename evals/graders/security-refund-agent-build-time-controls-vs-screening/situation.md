# security-refund-agent-build-time-controls-vs-screening: what the fixture holds

Base: support-assistant. Overlay files:

- `app/prompts.py`: the EUR 150 per-refund limit exists only as an instruction sentence.
- `app/tools/refunds.py`: checks ownership and amount <= order total in code, but no per-refund
  limit (the base's `max_refund_cents` check and service field are gone; `Settings` still
  reads MAX_REFUND_CENTS but nothing uses it) and no aggregate bound per order or customer: eight refunds of EUR 100 against one
  EUR 1,000 order are each allowed, and many small refunds below the order total pass (A2,
  smurfing).
- `app/operations.py`: an operation record per attempt (`refund_operations`: op_id, order_id,
  amount, status, provider_ref) — the business object the aggregate bound can key on. No
  integrity protection: an edited amount in the row or payload is not detectable (A3).
- `app/clients/payments.py`: sends `Idempotency-Key` = op_id (the key exists; signing goes
  beside it, A3).
- `deploy/agent-gateway.yaml`: Agent Gateway route; Model Armor templates and Semantic Governance
  Policies listed but empty (screening available, not configured; A1).
- Tests: base tool tests plus `tests/test_refund_operations.py`; all pass offline. google-adk not
  installed, no network (README).
- A4: a deterministic policy service as an A2A peer is optional; the blueprint's simulated anomaly
  detection must not be presented as a product.
