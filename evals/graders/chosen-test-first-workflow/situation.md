# chosen-test-first-workflow: what the fixture holds

Workspace = support-assistant base + overlay. The `tdd` skill the context says the user
selected is not available in the runner (external skill); the agent should still follow
a red-green order (failing test first) and may note the skill is absent.

- `app/refund_adapter.py` `RefundAdapter.refund()`: retries up to 3 times on
  `TransportTimeout`, `TransportError` and 429/5xx, but builds the replay key as
  `f"{operation_id}-{attempt}"` (line ~33), so every retry is a new key. After a timeout
  that followed acceptance, the retry is a fresh request and the provider commits a
  second refund. It also treats a timeout like any transient error (no lookup with
  `find_refund`), and marks the operation `failed` after exhausting attempts even when
  the outcome is unknown (no `uncertain` state in `app/operations.py`).
- `app/tools/refunds.py` generates `operation_id = uuid4` per tool call, so a model
  re-issuing the tool call is a new operation (trusted identity issue, A3).
- `docs/providers/payments-api.md`: same key + same body is replayed (200, `replayed`),
  same key + different body is 409, `GET /refunds?replay_key=` finds an accepted refund;
  timeouts can follow acceptance.
- `tests/provider_double.py` supports `"timeout_after_accept"`, committing the refund in
  `provider.refunds` before raising; `refunded_cents()` reads the provider's ledger.
- Existing suite passes (`tests.test_refund_adapter`, `tests.test_tools`). A failing test
  first: script `["timeout_after_accept", "ok"]` and assert one provider refund
  (currently two) — A2/A4 want assertions on provider attempts and stored effects.
- A5: success response shape `{"status": "refunded", "refund_id", "amount_cents"}` and
  adapter/tool signatures preserved; A6: reports local unittest only (agent has no shell,
  so tests are written but not run unless it says otherwise; no live refund).
