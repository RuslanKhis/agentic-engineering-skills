"""Keeps model requests small: trims old turns and puts a digest of them in the instruction."""
from __future__ import annotations

from google.adk.plugins.base_plugin import BasePlugin

from app.plugins.trimming import summary_line, trim_contents


class HistorySummariserPlugin(BasePlugin):
    def __init__(self, max_items: int = 24) -> None:
        super().__init__(name="history_summariser")
        self.max_items = max_items

    async def before_model_callback(self, *, callback_context, llm_request):
        kept, dropped = trim_contents(llm_request.contents, self.max_items)
        if not dropped:
            return None
        llm_request.contents = kept
        digest = summary_line(dropped)
        instruction = llm_request.config.system_instruction or ""
        llm_request.config.system_instruction = f"Earlier in this conversation: {digest}\n\n{instruction}"
        return None
