import os

from google.adk.agents import Agent
from google.adk.apps import App

from app.tools import my_tickets, raise_ticket, search_kb

MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")

INSTRUCTION = """\
You are Northbridge's IT helpdesk assistant for staff. Answer from the knowledge base
(search_kb) and cite the article ID. Use my_tickets to check the caller's open tickets and
raise_ticket when the knowledge base does not solve the problem. Never change accounts,
passwords or access; raise a ticket instead.
"""

root_agent = Agent(
    name="helpdesk",
    model=MODEL,
    instruction=INSTRUCTION,
    tools=[search_kb, my_tickets, raise_ticket],
)

app = App(name="app", root_agent=root_agent)
