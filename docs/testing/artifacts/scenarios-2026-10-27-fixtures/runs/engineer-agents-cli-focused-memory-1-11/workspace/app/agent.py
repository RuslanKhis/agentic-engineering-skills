import os

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.apps import App

from app.preferences import language_directive, set_response_language
from app.tools import my_tickets, raise_ticket, search_kb

MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")

INSTRUCTION = """\
You are Northbridge's IT helpdesk assistant for staff. Answer from the knowledge base
(search_kb) and cite the article ID. Use my_tickets to check the caller's open tickets and
raise_ticket when the knowledge base does not solve the problem. Never change accounts,
passwords or access; raise a ticket instead. When the caller asks to be answered in a particular
language, or to go back to the default, call set_response_language.
"""


def instruction(context: ReadonlyContext) -> str:
    """Base instruction plus the caller's saved response language, read from persisted user state."""
    return INSTRUCTION + language_directive(context.state)


root_agent = Agent(
    name="helpdesk",
    model=MODEL,
    instruction=instruction,
    tools=[search_kb, my_tickets, raise_ticket, set_response_language],
)

app = App(name="app", root_agent=root_agent)
