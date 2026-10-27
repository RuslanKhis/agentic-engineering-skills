"""Weekly refund report for team leads, added in PR #212 (October 2026)."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.workflow import Workflow, node

from app import services


@node
def collect_refunds(ctx) -> dict:
    store = services.get().store
    rows = store.conn.execute("SELECT order_id, amount_cents, created_at FROM refunds").fetchall()
    return {"refunds": [dict(r) for r in rows]}


@node
def email_report(ctx, summary: str) -> dict:
    lead = ctx.state.get("user:email", "")
    return services.get().mail.send(lead, "Weekly refunds", summary)


summariser = LlmAgent(
    name="refund_summariser",
    model="gemini-3.5-flash",
    instruction="Summarise the refunds in {refunds} for a team lead in five lines.",
)

reporting_agent = Workflow(
    name="reporting_agent",
    description="Builds and emails the weekly refund report for team leads.",
    edges=[(collect_refunds, summariser), (summariser, email_report)],
)
