"""The served route: the same stages as an ADK app. The only module that imports google.adk."""
from __future__ import annotations

import json

from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.events import Event, EventActions
from google.genai import types

from pipeline import stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies

settings = Settings.from_env()


class StageAgent(BaseAgent):
    """Runs one pipeline stage and records its result in session state."""

    stage: str
    model_name: str = ""

    async def _run_async_impl(self, ctx):
        state = ctx.session.state
        case = load_case(state["case_dir"])
        spans = case_spans(case, load_policies())
        model = ChatModel(settings.provider_base_url, self.model_name or settings.writer_model,
                          state.get("temp:provider_key", ""))
        store = CheckpointStore.from_settings(settings)
        if self.stage == "writer":
            result, usage = stages.run_writer(model, case, spans, settings.max_source_chars)
        elif self.stage == "review":
            result, usage = stages.run_review(model, state["writer"], spans, settings.max_source_chars)
        else:
            result, usage = stages.export(case, state["writer"], state["review"]), {}
        store.save(state["run_id"], self.stage, result, {"usage": usage})
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=types.Content(role="model", parts=[types.Part(text=json.dumps(result))]),
                    actions=EventActions(state_delta={self.stage: result}))


root_agent = SequentialAgent(
    name="planning_decision",
    sub_agents=[StageAgent(name="writer", stage="writer", model_name=settings.writer_model),
                StageAgent(name="review", stage="review", model_name=settings.review_model),
                StageAgent(name="export", stage="export")],
)
