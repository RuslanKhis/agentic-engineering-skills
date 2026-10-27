from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from homeline.tools import book_visit, my_visits

INSTRUCTION = """\
You are Homeline's booking assistant. Customers book plumbers, electricians and locksmiths.
Use what you remember about the customer (their address, access notes, past jobs) so they do
not have to repeat themselves, but always confirm the visit address before booking.
"""

root_agent = LlmAgent(
    name="homeline",
    model="gemini-3.5-flash",
    instruction=INSTRUCTION,
    tools=[PreloadMemoryTool(), book_visit, my_visits],
)
