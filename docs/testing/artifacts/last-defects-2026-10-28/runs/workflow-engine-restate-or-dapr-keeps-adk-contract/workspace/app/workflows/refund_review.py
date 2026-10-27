"""Restate workflow: wait for a manager's decision on a refund operation, then pay once.

Run as its own process (`hypercorn app.workflows.refund_review:asgi`), registered with the Restate
server. UNVERIFIED against the real SDK: written from the restate-sdk 1.x API as documented and
never imported in this session (no packages, no network). Before relying on it, run the
"Before you trust it" list in docs/refund-durability.md against a real Restate server.

Why this is not the ADK plugin: `RestatePlugin` accepts only an LlmAgent root, bypasses the
agent's before/after-model callbacks (the token budget) and RunConfig.max_llm_calls, and cannot
resume an ADK confirmation. The chat turn stays plain ADK with all of that intact; only the wait
and the payment are durable, and they live here.

The workflow acts on the stored operation, never on anything the wake-up carries: the ingress has
no caller authentication, so a stray wake-up must at worst find the operation still pending.
"""
from __future__ import annotations

from datetime import timedelta

import restate

from app import refund_ops
from app.settings import Settings
from app.wiring import configure_services

PAY_ATTEMPTS = 6  # then outcome_unknown; the provider's key window is 7 days, so stay well inside it

refund_review = restate.Workflow("RefundReview")


@refund_review.main()
async def run(ctx: restate.WorkflowContext, req: dict) -> dict:
    op_id = req["op_id"]
    remaining = await ctx.run("expiry", lambda: refund_ops.seconds_until_expiry(op_id))
    decided = ctx.promise("decision").value()
    winner, _ = await restate.select(decision=decided, timeout=ctx.sleep(timedelta(seconds=remaining)))
    # Known gap: a wake-up while the operation is still pending (only possible by calling the
    # ingress directly) ends this run with nothing paid and the operation left pending.
    if winner == "timeout":
        # Wins only if the operation is still pending; an approval that landed first stands.
        await ctx.run("expire", lambda: refund_ops.expire(op_id))
    try:
        return await ctx.run("pay", lambda: refund_ops.execute(op_id),
                             max_attempts=PAY_ATTEMPTS)
    except restate.TerminalError:
        return await ctx.run("unknown", lambda: refund_ops.mark_outcome_unknown(op_id))


@refund_review.handler()
async def decided(ctx: restate.WorkflowSharedContext) -> None:
    await ctx.promise("decision").resolve("decided")


configure_services(Settings.from_env())
asgi = restate.app([refund_review])
