I added code-level refund limits and tests for them, but I couldn't run anything. Bash is disabled in this session, so the new and existing tests are all unrun. Please run `python -m unittest discover -s tests -t .` before relying on any of it.

**What was wrong**
- The EUR 150 per-refund limit existed only in the prompt. The tool allowed any amount up to the order total.
- `Settings.max_refund_cents` was unused and said 20,000, against 15,000 in the prompt.
- The order-total check ran per call, so repeated refunds on one order could exceed the total. Nothing bounded refunds per customer or overall.
- Concurrent calls could both pass the same headroom check.

**What I built**
- `OperationStore.reserve()` in `app/operations.py` checks every limit and records the pending refund in one locked SQLite transaction. `issue_refund` calls it before the payments client, so a denial never reaches the provider. Identity still comes from `tool_context.user_id`.
- Limits, all in cents and overridable by environment variable:

| Limit | Default |
|---|---|
| Per refund | 15,000 (the prompt's stated policy) |
| Per order, cumulative | The order total |
| Per customer per 24h, amount | 30,000 |
| Per customer per 24h, count | 3 |
| Global per 24h | 2,000,000 |

- Pending and succeeded refunds count against the limits; declined ones release their headroom. A provider timeout keeps its reservation, which is the conservative choice.
- The tool now also rejects amounts that aren't plain integers (bool, float, string).
- `Settings` and `Services` carry the limits, and `app/agent.py` passes them in.
- `tests/test_refund_limits.py` covers each limit and asserts the fake payments transport saw no request on a denial.
- `docs/refund-hardening.md` has the findings, the limits table and the proof plan.

**What to prove for the review**
- The limits hold with the model fully compromised. The 24-hour loss is bounded by the global cap, and any one order by its total.
- Model Armor and the semantic policies are an extra detection layer, not the boundary. Run them inspect-only first and report their results separately from the limits.
- Still to add once `google-adk` is installed: a scripted-model Runner test in which the model attempts an over-limit refund and the payments fake sees nothing.

**Questions I couldn't ask, and the assumptions I used**
- I assumed 15,000 is the right per-refund limit, matching the prompt rather than settings. Please confirm.
- The customer and global caps (30,000, 3 per day, 2,000,000) are my guesses. They need an owner's sign-off.
- Refusing is the assumed behaviour above the cap. Queueing for human approval is an alternative.

**Left undone**
- Model Armor and semantic policies are not configured in `deploy/agent-gateway.yaml`. I have no template names, and applying them is a cloud change.
- Gift-card exclusion is still prompt-only. The order data has no field to enforce it on.
- Which order statuses are refundable is not enforced.
- The lock only serialises writes on one database. If Cloud Run runs several instances, each with its own SQLite file, the global cap applies per instance. That needs a shared database.
- I didn't edit the prompt text.