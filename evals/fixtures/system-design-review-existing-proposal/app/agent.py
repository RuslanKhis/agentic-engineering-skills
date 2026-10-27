"""The travel desk agent."""
from google.adk.agents import LlmAgent

from app.booking import change_booking
from app.documents import search_documents

INSTRUCTION = """\
You are Tidewater Travel's travel desk assistant for corporate travellers.
Answer questions about the traveller's company travel policy and itineraries using
search_documents, and quote the document title you used.
When the traveller wants to change a booking, ask the traveller to confirm the change,
then call change_booking.
"""

root_agent = LlmAgent(
    name="travel_desk",
    model="gemini-3.5-flash",
    instruction=INSTRUCTION,
    tools=[search_documents, change_booking],
)
