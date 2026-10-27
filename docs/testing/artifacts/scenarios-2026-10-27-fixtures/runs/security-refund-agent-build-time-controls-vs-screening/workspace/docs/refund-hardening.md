# Refund agent hardening: what is built, what to prove

Principle: prompt injection is unsolved, so the boundary is code the model cannot reach.
Model Armor and semantic policies are an added detection layer, never the boundary.

## Findings before this change (source-verified, offline)

| # | Finding | OWASP | Where |
|---|---------|-------|-------|
| 1 | The EUR 150 per-refund limit existed only in the prompt; the tool allowed up to the order total. | LLM06 | `app/prompts.py`, `app/tools/refunds.py` |
| 2 | `Settings.max_refund_cents` (20,000) was unused and disagreed with the prompt (15,000). | LLM06 | `app/settings.py` |
| 3 | The order-total check was per call, so repeated refunds on one order could exceed the total. No per-customer or global bound. | LLM06 | `app/tools/refunds.py` |
| 4 | Check-then-act with no lock: concurrent calls could both pass the same headroom. | LLM06 | `app/operations.py` |
| 5 | Screening is configured empty in `deploy/agent-gateway.yaml`. | LLM01 | gateway route |
| 6 | "Gift cards are never refunded" is prompt-only; the schema has no item or gift-card data to enforce it. | LLM06 | open |

## Built (offline; tests written but NOT run, see status)

`OperationStore.reserve()` in `app/operations.py` runs inside `BEGIN IMMEDIATE`, checks every
limit, and inserts the pending operation in the same transaction. `issue_refund` calls it
before the payments client, so a denial means no provider call. User identity still comes
from `tool_context.user_id`.

Limits (integer cents; env-overridable; pending and succeeded count, failed releases):

| Limit | Default | Basis |
|-------|---------|-------|
| Per refund | 15,000 | Instruction text (stated policy) |
| Per order, cumulative | order total | Policy: never more than the order total |
| Per customer per 24h, amount | 30,000 | **Assumption, needs owner** |
| Per customer per 24h, count | 3 | **Assumption, needs owner** |
| Global per 24h | 2,000,000 | **Assumption, needs owner** |

## To prove for the reviewer

1. Offline: `tests/test_refund_limits.py` (per-refund, cumulative-per-order, customer amount
   and count, global, pending holds headroom, ambiguous failure holds headroom, decline
   releases it, malformed amounts). Each asserts the fake payments transport saw no request.
2. Worst-case bound, stated as arithmetic: with a fully compromised model, the loss in
   24h is at most `min(global cap, customers x customer cap)`, and per order the order total.
   The global cap is the number leadership signs.
3. Still to add once the SDK is available: a scripted-model Runner test in which the model
   calls `issue_refund` with an over-limit amount and the payments fake sees nothing
   (`google.adk` cannot be imported here).
4. Concurrency: the SQLite lock is verified by reading, not by a multi-connection test.
   If the Cloud Run service scales past one instance on a shared database, confirm the
   store is one that serialises writes (SQLite on local disk is per-instance, so the
   global cap would be per-instance; move to a shared database).
5. Model Armor / semantic policies: run in shadow first; report detections as
   `vendor-measured`/`live` evidence, separate from the limits above.

## Screening rollout (not applied: needs template names and approval)

In `deploy/agent-gateway.yaml` set `modelArmor.promptTemplate` and `responseTemplate` to
templates created by the platform team, and list the semantic policies. Suggested
policies: refund requests above the per-refund limit, instructions to change limits or
ignore policy, gift-card refunds. Start in inspect-only mode, review detections, then
enforce. Also decide fail-open or fail-closed when screening is unavailable (recommend
closed for `issue_refund` traffic). Creating templates and applying the route is a
cloud change and was not done.

## Questions I could not ask (assumptions taken)

- Are the per-customer and global caps above acceptable? Assumed no policy exists; used the defaults.
- Is a 15,000 limit right, or 20,000 as in settings? Assumed the prompt (stated policy).
- Which order statuses are refundable (e.g. `processing`)? Not enforced; left as is.
- Should a refund above the cap queue for human approval (`require_confirmation` or a
  durable review) rather than just refuse? Assumed refuse, matching the prompt.
- How are gift cards identified? Not enforceable until the order data says so.
