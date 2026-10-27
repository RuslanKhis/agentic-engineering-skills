# Situation (judge only): evaluation-incident-regression-fail-to-pass

Context (unchanged): ADK 2.12 refund agent with issue_refund and lookup_order, in-memory backend
fixture, scripted-model Runner tests for eligible refund and foreign-order denial, fix merged as
one commit on top of a known base commit, no model access.

Workspace: support-assistant base plus this overlay (the post-fix tree). There is no `.git`
directory: the base commit `4e1d2a7` and fix commit `b93c0f5` are named in
`docs/incidents/INC-0412.md`, so running the tests on the base commit is impossible in the
session; the agent can only specify those two recorded runs.

- Fix: `app/tools/refunds.py` (propose_refund stores a pending proposal in state; issue_refund
  takes no arguments and consumes it once). Before the fix, issue_refund(order_id, amount_cents,
  reason) refunded on every call.
- Existing Runner tests: `tests/test_runner_refunds.py` (eligible refund paid once; foreign order
  denied), using `tests/scripted_model.py`; they skip without google-adk (not installed).
- In-memory backend: `tests/fakes.py` (FakeTransport records provider requests; Store in memory).

## Assertion map

A1 new scripted-model Runner test: two confirmations ("yes", "yes") with the model calling
issue_refund twice → exactly one stored refund / one provider request; listed under fail_to_pass,
existing two Runner tests under pass_to_pass; A2 two recorded runs required (base commit: f2p
fails, p2p pass; fix: all pass); A3 grading rule exactly: resolved only if f2p non-empty and every
listed test passed; skipped/missing f2p fails the case; skipped p2p → NOT RUN; no partial credit;
A4 metadata with base_ref 4e1d2a7, reference_fix b93c0f5, both lists, and the new test reported as
not run (SDK absent, no shell).
