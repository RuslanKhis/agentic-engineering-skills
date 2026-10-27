"""Model Armor screening of the user's message before the model sees it."""
from __future__ import annotations

from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types


class ModelArmorInputPlugin(BasePlugin):
    def __init__(self, template: str) -> None:
        super().__init__(name="model_armor_input")
        self.template = template
        self._client = None

    def _armor(self):
        if self._client is None:
            from google.cloud import modelarmor_v1

            self._client = modelarmor_v1.ModelArmorClient(
                client_options={"api_endpoint": "modelarmor.europe-west4.rep.googleapis.com"})
        return self._client

    async def on_user_message_callback(self, *, invocation_context, user_message: types.Content):
        from google.cloud import modelarmor_v1

        text = " ".join(p.text for p in user_message.parts or [] if p.text)
        result = self._armor().sanitize_user_prompt(request=modelarmor_v1.SanitizeUserPromptRequest(
            name=self.template, user_prompt_data=modelarmor_v1.DataItem(text=text)))
        if result.sanitization_result.filter_match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
            return types.Content(role="user", parts=[types.Part(text="[message withheld by screening]")])
        return None
