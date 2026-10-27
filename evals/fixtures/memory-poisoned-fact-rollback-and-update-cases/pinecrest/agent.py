from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from pinecrest.tools import book_slot, order_status

INSTRUCTION = """\
You are Pinecrest Grocers' delivery assistant. Use what you remember about the customer
(address, access notes, substitutions, dietary needs, account benefits) so they do not
repeat themselves. Book slots with book_slot and check orders with order_status.
"""

root_agent = LlmAgent(
    name="pinecrest_delivery",
    model="gemini-3.5-flash",
    instruction=INSTRUCTION,
    tools=[PreloadMemoryTool(), book_slot, order_status],
)
