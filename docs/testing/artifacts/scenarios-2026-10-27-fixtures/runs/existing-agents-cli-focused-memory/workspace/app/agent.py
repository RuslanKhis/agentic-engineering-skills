import os

from google.adk.agents import Agent
from google.adk.apps import App

from app import preferences
from app.tools import (
    delete_language_preference,
    get_language_preference,
    my_tickets,
    raise_ticket,
    search_kb,
    set_language_preference,
)

MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")

INSTRUCTION = """\
You are Northbridge's IT helpdesk assistant for staff. Answer from the knowledge base
(search_kb) and cite the article ID. Use my_tickets to check the caller's open tickets and
raise_ticket when the knowledge base does not solve the problem. Never change accounts,
passwords or access; raise a ticket instead.
"""

LANGUAGE_INSTRUCTION = """\
Users can save a response language (set_language_preference), check it
(get_language_preference) and delete it (delete_language_preference). Use these only when the
user asks. A language saved by the user is applied automatically.
"""


def instruction_provider(ctx) -> str:
    """Base instruction plus the caller's saved language, read fresh on every invocation."""
    text = INSTRUCTION + LANGUAGE_INSTRUCTION
    code = preferences.get_language(ctx.user_id)
    if code:
        text += f"\nReply in {preferences.LANGUAGES[code]}. Keep article IDs unchanged.\n"
    return text


root_agent = Agent(
    name="helpdesk",
    model=MODEL,
    instruction=instruction_provider,
    tools=[search_kb, my_tickets, raise_ticket, set_language_preference,
           get_language_preference, delete_language_preference],
)

app = App(name="app", root_agent=root_agent)
