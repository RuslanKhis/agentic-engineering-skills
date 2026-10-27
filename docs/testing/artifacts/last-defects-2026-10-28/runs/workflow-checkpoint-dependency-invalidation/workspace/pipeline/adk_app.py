"""The served route: the same stages as an ADK app. The only module that imports google.adk."""
from __future__ import annotations

import json

from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.events import Event, EventActions
from google.genai import types

from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.resume import Resumption

settings = Settings.from_env()


class StageAgent(BaseAgent):
    """Runs one pipeline stage, or loads it from the checkpoint store when what it depended on is unchanged,
    and records its result in session state. New records go to a continuation of state["run_id"]; the
    continuation's name travels in state["resume_run"] so the three stages write to the same directory."""

    stage: str
    model_name: str = ""

    async def _run_async_impl(self, ctx):
        state = ctx.session.state
        model = ChatModel(settings.provider_base_url, self.model_name or settings.writer_model,
                          state.get("temp:provider_key", ""))
        store = CheckpointStore(settings.checkpoint_dir, settings.checkpoint_limit_bytes)
        resumption = Resumption(state["case_dir"], state["run_id"], settings, model, model, store,
                                continuation=state.get("resume_run"))
        draft, revision = resumption.draft()
        if self.stage == "writer":
            result = draft
        else:
            review = resumption.review(draft, revision)
            result = review if self.stage == "review" else resumption.export(draft, revision, review, None)
        resumption.finish()
        delta = {self.stage: result}
        if resumption.run_id:
            delta["resume_run"] = resumption.run_id
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=types.Content(role="model", parts=[types.Part(text=json.dumps(result))]),
                    actions=EventActions(state_delta=delta))


root_agent = SequentialAgent(
    name="planning_decision",
    sub_agents=[StageAgent(name="writer", stage="writer", model_name=settings.writer_model),
                StageAgent(name="review", stage="review", model_name=settings.review_model),
                StageAgent(name="export", stage="export")],
)
