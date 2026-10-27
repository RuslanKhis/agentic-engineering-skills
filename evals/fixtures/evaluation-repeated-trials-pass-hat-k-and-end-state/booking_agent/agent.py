"""Builds the booking agent."""
import os

from google.adk.agents import LlmAgent

from booking_agent import tools

root_agent = LlmAgent(
    name="booking_agent",
    model=os.environ.get("MODEL_ID", "gemini-3.5-flash"),
    instruction="You book, move and cancel physiotherapy appointments for the signed-in patient.",
    tools=[tools.search_slots, tools.get_my_bookings, tools.book_slot, tools.cancel_booking],
)
