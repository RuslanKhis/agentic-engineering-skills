"""The served route: the same stages as an ADK app. The only module that imports google.adk."""
from __future__ import annotations

import json

from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.events import Event, EventActions
from google.genai import types

from pipeline import resume
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
        store = CheckpointStore(settings.checkpoint_dir, settings.checkpoint_limit_bytes)
        delta = {}
        if "target_run_id" not in state:
            # The first stage decides where this invocation writes: the run itself if it is new,
            # otherwise a continuation run holding only checkpoints that still qualify.
            delta["target_run_id"] = resume.prepare_continuation(case, spans, state["run_id"], settings, store)
        target = delta.get("target_run_id") or state["target_run_id"]
        if self.stage == "export":
            for stage in ("source", "constraints"):
                resume.carry_stage(stage, case, spans, target, settings, store)
            result = resume.publish(case, target, store)
        else:
            if self.stage == "writer":
                for stage in ("source", "constraints"):
                    resume.carry_stage(stage, case, spans, target, settings, store)
            result = resume.carry_stage(self.stage, case, spans, target, settings, store, model)
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=types.Content(role="model", parts=[types.Part(text=json.dumps(result))]),
                    actions=EventActions(state_delta={**delta, self.stage: result}))


root_agent = SequentialAgent(
    name="planning_decision",
    sub_agents=[StageAgent(name="writer", stage="writer", model_name=settings.writer_model),
                StageAgent(name="review", stage="review", model_name=settings.review_model),
                StageAgent(name="export", stage="export")],
)
