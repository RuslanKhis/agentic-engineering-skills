import os

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.plugins.bigquery_agent_analytics_plugin import (BigQueryAgentAnalyticsPlugin,
                                                               BigQueryLoggerConfig)

from app.app_utils.analytics_privacy import CONTENT_EVENTS, drop_content
from app.tools import draft_booking_request, search_travel_policy

root_agent = Agent(
    name="travel_desk",
    model="gemini-3.5-flash",
    instruction=(
        "You are Oakmere's travel desk assistant. Answer questions from the travel policy using "
        "search_travel_policy and cite the section. When an employee wants to book, collect the "
        "traveller's name, dates, route and passport expiry and call draft_booking_request. The "
        "travel team approves every booking; you never book anything yourself."
    ),
    tools=[search_travel_policy, draft_booking_request],
)

analytics = BigQueryAgentAnalyticsPlugin(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", "oakmere-travel-dev"),
    dataset_id=os.environ.get("ANALYTICS_DATASET", "travel_desk_analytics"),
    config=BigQueryLoggerConfig(
        batch_size=20,
        enable_otel_correlation=True,
        event_denylist=CONTENT_EVENTS,
        content_formatter=drop_content,
        log_multi_modal_content=False,
    ),
)

app = App(name="app", root_agent=root_agent, plugins=[analytics])
