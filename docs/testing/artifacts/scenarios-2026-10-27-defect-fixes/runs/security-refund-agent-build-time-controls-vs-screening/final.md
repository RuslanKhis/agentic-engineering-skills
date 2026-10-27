I've put the refund limits into code and written tests for them. I couldn't run anything in this session, so **none of it has been executed**, including the existing tests. Run `python -m unittest discover -s tests -t .` before the review.

**What was wrong**
- The EUR 150 per-refund limit existed only in the prompt.
- `Settings.max_refund_cents` said 20,000, disagreed with the prompt, and nothing read it.
- Nothing capped the total refunded on one order. Eight small refunds could pass one at a time and add up to more than the order.
- A 5xx from the payments API marked the refund `failed`, which freed that amount for a retry even though the provider may have processed it.

**What I built**
- **Per-refund limit:** `app/policy.py` holds one constant, 15,000 cents. The prompt, settings and tool all read it, and the tool refuses larger or malformed amounts before touching the payments API.
- **Order total bound:** `OperationStore.reserve()` in `app/operations.py` checks the order's pending plus succeeded refunds in one write transaction. Two concurrent requests can't both claim the last cents.
- **Unclear outcomes still count:** only a 4xx releases the reserved amount. A 5xx or a timeout keeps it counted against the order.
- **Tests:** `tests/test_refund_policy.py` includes the eight-small-refunds case, randomised attack sequences, 5xx and timeout, two database connections, and another customer's order.
- **Write-up:** `docs/refund-hardening.md` has the build list, the proof table for the reviewer, residual risk and the open questions.

**What to prove at the review:** that no more than the order total, and no single refund above the limit, ever reaches the provider, with screening switched off. The tests check exactly that, and they involve no model or screen.

**Not done**
- Model Armor and the semantic policies are not configured. I didn't invent template names in `deploy/agent-gateway.yaml`, and the doc lists the rollout steps. They go on as extra layers only: the semantic policies are in Preview and the vendor says their verdicts may be wrong.
- Not built: a payments-side cap or signed refund requests, human approval above a threshold, a per-customer daily cap, and a staging adversarial run.
- The gift-card rule is still prompt-only, because `orders` has no field to check it against.

**Questions I couldn't ask, and what I assumed**
- **Limit:** EUR 150 (the prompt) rather than 200 (the settings default).
- **`processing` orders:** refunds on them stay allowed.
- **Database:** `support.db` is a single instance. If Cloud Run scales past one, `reserve()` has to move to a shared database.
- **Order total:** it is the aggregate cap.