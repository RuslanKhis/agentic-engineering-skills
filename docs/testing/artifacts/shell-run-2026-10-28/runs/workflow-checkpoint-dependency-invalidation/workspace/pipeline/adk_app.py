"""The served route: the same stages as an ADK app. The only module that imports google.adk."""
from __future__ import annotations

import json

from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.events import Event, EventActions
from google.genai import types

from pipeline import stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.constraints import site_constraints
from pipeline.model import ChatModel
from pipeline.resume import Continuation
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
        writer = ChatModel(settings.provider_base_url, settings.writer_model, state.get("temp:provider_key", ""))
        reviewer = ChatModel(settings.provider_base_url, settings.review_model, state.get("temp:provider_key", ""))
        store = CheckpointStore(settings.checkpoint_dir, settings.checkpoint_limit_bytes)
        # Saved stages are reused only while their inputs still match; results go to a new continuation
        # run, never into the retained run named by run_id.
        cont = Continuation(store, state["run_id"], case, spans, settings, writer, reviewer,
                            run_id=state.get("continuation_run_id"))
        if self.stage == "writer":
            result = cont.obtain_draft(lambda: stages.run_writer(writer, case, spans, settings.max_source_chars))
        elif self.stage == "review":
            cont.draft = state["writer"]
            result = cont.obtain("review", lambda: stages.run_review(reviewer, state["writer"], spans,
                                                                     settings.max_source_chars))
        else:
            cont.draft = state["writer"]
            cont.obtain("source", lambda: ({"span_ids": [sp.span_id for sp in spans]}, {}))
            cont.obtain("constraints", lambda: (site_constraints(case["address"]), {}))
            cont.lookup("writer")
            cont.lookup("review")
            result = cont.publish(state["writer"], state["review"])
        delta = {self.stage: result}
        if cont.run_id:
            delta["continuation_run_id"] = cont.run_id
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=types.Content(role="model", parts=[types.Part(text=json.dumps(result))]),
                    actions=EventActions(state_delta=delta))


root_agent = SequentialAgent(
    name="planning_decision",
    sub_agents=[StageAgent(name="writer", stage="writer", model_name=settings.writer_model),
                StageAgent(name="review", stage="review", model_name=settings.review_model),
                StageAgent(name="export", stage="export")],
)
