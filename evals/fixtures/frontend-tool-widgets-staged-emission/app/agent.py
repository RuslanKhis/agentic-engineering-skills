"""Builds the ADK shopping agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent

from app.callbacks import refresh_cards_after_preference_change
from app.prompts import ROOT_INSTRUCTION
from app.settings import Settings
from app.tools.shopping import compare_products, recommend_products, search_products


def build_agent(settings: Settings | None = None) -> LlmAgent:
    settings = settings or Settings.from_env()
    return LlmAgent(
        name="shopping_assistant",
        model=settings.model_id,
        description="Helps Harbour Outfitters customers find and compare products.",
        instruction=ROOT_INSTRUCTION,
        tools=[search_products, recommend_products, compare_products],
        after_agent_callback=refresh_cards_after_preference_change,
    )


root_agent = build_agent()
