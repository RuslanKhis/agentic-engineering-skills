"""Served qualification route as an ADK agent (imports google.adk; not used by the unit tests)."""
from __future__ import annotations

import json

from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions
from google.genai import types

from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.qualification import load_pack, run_qualification

settings = Settings.from_env()


class QualificationAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        state = ctx.session.state
        pack = load_pack(state["pack_path"])
        model = ChatModel(settings.provider_base_url, settings.writer_model, state.get("temp:provider_key", ""))
        store = CheckpointStore(settings.checkpoint_dir, settings.checkpoint_limit_bytes)
        result = run_qualification(pack, model, store, state["run_id"])
        yield Event(author=self.name, invocation_id=ctx.invocation_id,
                    content=types.Content(role="model", parts=[types.Part(text=json.dumps(result))]),
                    actions=EventActions(state_delta={"qualification": result}))


root_agent = QualificationAgent(name="policy_qualification")
