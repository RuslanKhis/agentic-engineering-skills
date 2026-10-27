import os

from google.adk.agents import Agent
from google.adk.apps import App

from app.preferences import language_instruction
from app.tools import my_tickets, raise_ticket, search_kb, set_response_language

MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")

INSTRUCTION = """\
You are Northbridge's IT helpdesk assistant for staff. Answer from the knowledge base
(search_kb) and cite the article ID. Use my_tickets to check the caller's open tickets and
raise_ticket when the knowledge base does not solve the problem. Never change accounts,
passwords or access; raise a ticket instead.
"""



def instruction_provider(context) -> str:
    """Base instruction plus the caller's saved response language, read per invocation."""
    return INSTRUCTION + language_instruction(context.state)


root_agent = Agent(
    name="helpdesk",
    model=MODEL,
    instruction=instruction_provider,
    tools=[search_kb, my_tickets, raise_ticket, set_response_language],
)

app = App(name="app", root_agent=root_agent)
