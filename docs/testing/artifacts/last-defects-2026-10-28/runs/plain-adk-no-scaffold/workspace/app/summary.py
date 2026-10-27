"""Account summary flow: read orders, read open tickets, then summarise for the customer.

The two readers are plain agents that call the tool functions directly and put their result in
session state; they run in parallel and either one failing fails the run. The summary agent's
instruction reads both.
"""
from __future__ import annotations

import asyncio
from typing import AsyncGenerator

from google.adk.agents import BaseAgent, LlmAgent, ParallelAgent, SequentialAgent
from google.adk.events import Event, EventActions

from app.tools.orders import list_my_orders
from app.tools.tickets import list_open_tickets

SUMMARY_INSTRUCTION = """\
Summarise the customer's account in three or four sentences: their recent orders and any open
support tickets. Recent orders: {orders}. Open tickets: {tickets}.
"""


class _Ctx:
    def __init__(self, user_id):
        self.user_id = user_id


class OrdersReader(BaseAgent):
    async def _run_async_impl(self, ctx) -> AsyncGenerator[Event, None]:
        # The tools are synchronous; a worker thread lets the two readers overlap. A failure
        # propagates: the summary must not be written from a missing read.
        orders = (await asyncio.to_thread(list_my_orders, _Ctx(ctx.session.user_id)))["orders"]
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    actions=EventActions(state_delta={"orders": orders}))


class TicketsReader(BaseAgent):
    async def _run_async_impl(self, ctx) -> AsyncGenerator[Event, None]:
        tickets = (await asyncio.to_thread(list_open_tickets, _Ctx(ctx.session.user_id)))["tickets"]
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    actions=EventActions(state_delta={"tickets": tickets}))


def build_summary_flow(model: str = "gemini-3.5-flash") -> SequentialAgent:
    return SequentialAgent(name="account_summary", sub_agents=[
        ParallelAgent(name="readers", sub_agents=[
            OrdersReader(name="orders_reader"),
            TicketsReader(name="tickets_reader"),
        ]),
        LlmAgent(name="summary", model=model, instruction=SUMMARY_INSTRUCTION),
    ])
