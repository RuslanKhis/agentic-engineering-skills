I haven't run anything yet. I'm still editing, and I can't find a shell tool in this session to run the tests with.

The fix is written but not run. I'll finish with a summary.

## What I did

I fixed the continuation decision in `campaign/admission.py`, `campaign/dispatch.py` and `campaign/ledger.py`, and added tests in `tests/test_dispatch.py`. The tests use the counting fake, so no real provider is involved.

**Causes of the double payment**
- **Lost response released the hold.** A no-response attempt was released as if nothing had been charged, even though the provider may still bill it. Its reservation now stays open until a receipt settles it. The allowance and the approval stay spent.
- **Approval matched too loosely.** Any approval for the campaign allowed any continuation, and the approval's own stage, case, request-count and spend limits were never checked. APR-0031 now covers only `case-07` `review`, one request, up to 60 cents. Each use is recorded in a new `approval_uses` table, so a second continuation is refused even after another lost response.
- **Paid attempts were treated as unpaid.** An attempt that was interrupted but later got a receipt could be sent again. Admission now refuses an identity that has any receipt, so `case-05` generation is refused because `rc-9005` arrived late.
- **Duplicate receipts.** `rc-9005` appears twice in the inbox and would have been counted twice. Settling is now once per receipt ID, and a conflicting redelivery or an unknown reservation raises an error.

**Spending allowance, kept and tightened**
- The envelope check now subtracts open holds as well as settled charges.
- The provider balance is only an upper bound. It was read before the last session, so I subtract everything committed since that reading.
- The per-attempt hold is now at least the configured reserve. It was previously cut to the cheapest charge seen, which understated the cost.
- The send count now includes unanswered attempts, not only successful ones.
- Admission, attempt creation and approval use now happen under one lock, so two concurrent requests can't both pass.

## What I left undone
- **Tests not run.** I traced the new test numbers by hand, but that is not a test result. Please run `python -m unittest discover -s tests -t .`.
- **Per-stage limits.** The per-stage spend and send limits in `config/campaign.json` are still not enforced.
- **Single process only.** The lock covers one process. Several runners sharing one SQLite file would need a database-level transaction.
- **Other failures still release.** A generic exception still releases the hold. That is right for a definite rejection like the 400 error, but a timeout reported as a plain exception would be under-counted.
- **Stale balance.** Please refresh the provider balance. Other spending on the account since that reading is invisible to us.
- **Late receipts.** Applying `receipts-inbox.jsonl` is left to the caller of `apply_late_receipts`. The tests apply it.

## Questions I couldn't ask, and what I assumed
- **Does an approval cover a first attempt for an out-of-cohort case?** I assumed it does when the approval names that case and stage and still has requests left.
- **What counts as an approval's spend?** I assumed receipt amounts where they exist, otherwise the held reservation.