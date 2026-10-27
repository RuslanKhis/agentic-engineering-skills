I fixed the admission logic and added tests that use the fake provider, but I couldn't run any of them. Bash is disabled in this session, so the code and tests are only traced by hand. Please run `python -m unittest discover -s tests -t .` before relying on this.

**What was letting a second paid request out**
- **Approval:** any approval for the campaign allowed any continuation. It now has to match the stage and case, and it stops after `max_requests` and `max_spend_cents`. APR-0031 therefore allows exactly one `case-07` review request and nothing else. A second attempt after another lost response is refused.
- **Lost responses:** a `no_response` attempt released its reservation, so the money looked free again. It now stays held until a receipt settles it. It also counts as a send, where before only successes did.
- **Late receipts:** the inbox has `rc-9005` delivered twice, and settling inserted it twice. Settling is now idempotent on `receipt_id` and rejects receipts for unknown reservations. A case with any receipt, such as `case-05` generation after the late receipt, is treated as already charged and refused.
- **Reserve estimate:** it was lowered to the cheapest past charge, which isn't a safe upper bound. It now always uses the configured reserve.
- **Allowance:** it now counts settled charges plus open holds. The provider balance (read 25 Oct 08:00, before every attempt in the export) is reduced by everything committed since then. The per-stage send limits and spend allocations in the config are now enforced too.

The envelope and the approval file are unchanged. The edits are in `campaign/ledger.py`, `campaign/admission.py` and `campaign/dispatch.py`. I added a `load_receipts` helper to `dispatch.py` and nine tests to `tests/test_dispatch.py`.

**Questions I couldn't ask, and what I assumed**
- **Tied-up money:** is the open hold on `case-05` generation (110) and `case-07` review (60) real money? I assumed yes and kept it counted. The `case-05` one is replaced by its 102-cent receipt once you apply the inbox.
- **Provider balance:** the figure is stale. I subtracted spend since it was read rather than waiting for a fresh reading, so please refresh it from the billing page.
- **Provider side:** I assumed a late receipt means the provider did the work. Whether the `case-05` output survived the worker restart is a human decision, and no approval covers redoing it.

**Not done**
- I haven't run the tests.
- Inbox receipts are not applied automatically at startup. Call `apply_late_receipts(ledger, load_receipts("data/receipts-inbox.jsonl"))` first.
- Admission and the send aren't atomic across processes. That's fine for one runner but not for concurrent ones.
- `max_minutes` is still not enforced.
- I didn't touch real provider calls.