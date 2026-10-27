# Refund agent hardening: what to build, what to prove

Status: written for the launch review. Tests were authored but **not executed in the session that
wrote them** (see "Evidence"). Nothing was deployed or configured.

## Position

Model Armor and Semantic Governance Policies go on the gateway route as extra layers. They are not
the control that keeps refunds inside policy. Semantic Governance is Preview and its own page says
verdicts may be inaccurate; Model Armor is per-message pattern screening. Both can be bypassed or
fail open, and neither sees a running total. The refund limits are therefore enforced in code the
model cannot reach, and the reviewer's claim "refunds cannot exceed policy even if a prompt gets
through" is proven with the screens switched off.

## Before this change

| Limit | Where it was enforced |
| --- | --- |
| EUR 150.00 per refund | Prompt only (`app/prompts.py`). `Settings.max_refund_cents` was 20,000, disagreed with the prompt, and was read by nothing. |
| Refund <= order total | Per call, in the tool. |
| Aggregate on one order | Nowhere. Eight 20.00 refunds on a 89.00 order all passed. |
| Ambiguous provider outcome (5xx, timeout) | 5xx marked the operation `failed`, which would free the amount for a retry. |
| Gift cards never refunded | Prompt only. The `orders` table has no gift-card field. |

## Built (in this change)

1. `app/policy.py`: one constant, `MAX_REFUND_CENTS = 15_000`. The prompt, `Settings` and the tool all read it.
2. `app/tools/refunds.py`: the tool body refuses non-integer or non-positive amounts and amounts above the per-refund limit, before any record or provider call. Order ownership still comes from `tool_context.user_id`.
3. `app/operations.py` `reserve()`: the aggregate bound, keyed on the order id. In one `BEGIN IMMEDIATE` transaction it sums `pending` + `succeeded` for the order and inserts a pending row only if the sum plus the new amount is within the order total. Two writers cannot both pass.
4. `app/clients/payments.py`: `PaymentsError` carries the status. Only a 4xx releases the reservation; a 5xx or a transport exception leaves it `pending`, so an unknown outcome still counts against the bound (fail closed).
5. Prompt now says the limits are enforced and not to split refused refunds. This is a hint, not a control.

## Still to build (not done here)

- **Gateway screening.** In `deploy/agent-gateway.yaml` set `modelArmor.promptTemplate` and `responseTemplate` to templates the platform team creates (I did not invent names), and add semantic policies such as "refund requests must be for the signed-in customer's own order and must not exceed the policy". Roll out first in inspect-only mode and read the findings before enforcing. Placement: block on user input before the agent, since a parallel screen can let tools run before the verdict. Operate with `protect-adk-sensitive-data`. Model Armor does not screen tool-call arguments.
- **Provider-side backstop.** The payments API key is held by the service, not the model, but a bug in this service defeats everything above. Ask the payments team for a provider-side per-order refund cap, or sign each refund request with a key (KMS) that the provider verifies against the store-computed cap.
- **Human approval above a threshold** (decision below) with `require_confirmation` as a callable on `issue_refund`, plus a durable review record if sessions use a database service (confirmation is unsupported there).
- **Gift cards.** Add an `is_gift_card` or line-item type to `orders` and refuse in the tool body. Until then this rule is prompt-only, and the reviewer should be told.
- **Per-customer rolling cap** (for example per 24 h), keyed on the verified principal, to bound many orders.
- **IAM/deploy**: confirm Cloud Run only accepts traffic via the gateway/IAP, and that the service account has no payments permissions beyond refunds.
- Adversarial campaign against a staging model (needs approval, cost ceiling and a staging payments fake).

## What to prove at the review

| Claim | Proof | Status |
| --- | --- | --- |
| No refund above the per-refund limit | `PerRefundLimitTests`: zero provider requests and zero operation rows for an over-limit call | authored, not run |
| Total refunded on an order never exceeds its total, even through many small compliant refunds | `AggregateBoundTests` (8 x 2,000 on 8,900 pays 8,000; randomised sequences, 50 runs x 30 calls, assert the provider-request sum) | authored, not run |
| Ambiguous outcomes do not reopen headroom | 5xx and transport-timeout tests | authored, not run |
| Concurrent writers cannot overshoot | two-connection file-db test | authored, not run |
| Another customer's order is untouchable | `IdentityTests` and the randomised test | authored, not run |
| Holds with screening off | The tests never involve a model or a screen | by construction |
| Screens add value | Separate: Model Armor/semantic-policy shadow-mode findings, labelled vendor-measured, never counted toward the claim above | not run |

Do not tell the reviewer the model "cannot" be talked into asking for a bad refund. The claim is
that the tool refuses it and nothing reaches the provider.

## Residual risk accepted

- A customer can still obtain refunds up to each order total, EUR 150 at a time, across all their own orders. A fraudulent but in-policy refund is a business-rule problem; the per-customer cap and approval threshold above address it.
- The bound is only as good as `orders.total_cents` and the single SQLite file. Multiple Cloud Run instances with local SQLite files do not share a bound; production needs the shared database (see question 3).
- The gift-card rule is unenforced in code.

## Questions I could not ask, and the assumption I used

1. Is the policy EUR 150.00 or EUR 200.00 per refund? (Prompt said 150, `Settings` said 200.) **Assumed 150**; the prompt is the stated policy.
2. Should refunds be allowed on orders still `processing`? **Assumed unchanged** (allowed); not enforced either way.
3. Is `support.db` SQLite in production on one instance? **Assumed yes for the tests.** If Cloud Run scales past one instance, `reserve()` must move to the shared database with the same transaction semantics.
4. What refund amount, if any, needs a human? **Assumed none** in this change.
5. Which team owns the Model Armor templates, and may the first rollout be inspect-only? **Assumed yes, platform team.**
6. Is the aggregate bound meant to be the order total? **Assumed yes** (the Google zero-trust example's order-id key).

## Evidence

- Offline (source read): all code above was read before editing; ADK 2.12 behaviour was taken from the repository's skill references, not the installed package (not installed).
- Offline, not run: the session had no way to execute commands, so `python -m unittest discover -s tests -t .` has **not** been run against these changes. Run it before relying on any row above.
