# Review campaign runner

Runs our ADK document-review route over a fixed cohort of planning cases against the
model provider, inside a spending allowance agreed with finance. Each case goes through
`generation` (the writer stage) and `review`; a stage call is one paid provider request.

- `campaign/ledger.py`: the persistent ledger (SQLite) of attempts, reservations,
  provider receipts and the provider balance we last observed.
- `campaign/admission.py`: decides whether a request (a first attempt or a
  continuation of an earlier one) may go out.
- `campaign/dispatch.py`: admission, reservation, send, settlement.
- `campaign/transport.py`: the provider transport interface; production wraps the
  provider SDK, tests use `tests/fake_provider.py`, which counts sends.
- `config/campaign.json`: the campaign envelope (sends, wall-clock minutes, spend) and the
  per-stage allocations.
- `approvals/`: approvals from the campaign owner for anything outside the planned run.
- `data/ledger-seed.json`: the ledger as exported after the 25 October session;
  `data/receipts-inbox.jsonl`: provider receipts that arrived after that export.

Amounts are integer cents. A reservation is the conservative cost estimate held before a
request is sent; the provider's receipt settles it with the actual charge.

Tests: `python -m unittest discover -s tests -t .` (stdlib only, no provider access).
