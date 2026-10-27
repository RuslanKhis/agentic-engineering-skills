"""The ADK App: root agent, plugins and context compaction."""
from __future__ import annotations

from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig

from app.agent import root_agent
from app.plugins.summariser import HistorySummariserPlugin

support_app = App(
    name="support",
    root_agent=root_agent,
    plugins=[HistorySummariserPlugin(max_items=24)],
    events_compaction_config=EventsCompactionConfig(compaction_interval=6, overlap_size=1),
)
