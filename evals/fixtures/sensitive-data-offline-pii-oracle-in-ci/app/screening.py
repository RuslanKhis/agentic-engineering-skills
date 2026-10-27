"""Production screening: Model Armor on customer input, SDP de-identification on replies and logs.

Clients are created lazily so tests and local runs can pass fakes.
"""
from __future__ import annotations

import os

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "harbour-support-prod")
LOCATION = os.environ.get("SECURITY_LOCATION", "europe-west2")
ARMOR_TEMPLATE = f"projects/{PROJECT}/locations/{LOCATION}/templates/support-input"
DEID_TEMPLATE = f"projects/{PROJECT}/locations/{LOCATION}/deidentifyTemplates/support-replies"


class Screening:
    def __init__(self, armor=None, dlp=None):
        self._armor, self._dlp = armor, dlp

    def armor(self):
        if self._armor is None:
            from google.api_core.client_options import ClientOptions
            from google.cloud import modelarmor_v1

            self._armor = modelarmor_v1.ModelArmorClient(
                client_options=ClientOptions(api_endpoint=f"modelarmor.{LOCATION}.rep.googleapis.com"))
        return self._armor

    def dlp(self):
        if self._dlp is None:
            from google.api_core.client_options import ClientOptions
            from google.cloud import dlp_v2

            self._dlp = dlp_v2.DlpServiceClient(
                client_options=ClientOptions(api_endpoint=f"dlp.{LOCATION}.rep.googleapis.com"))
        return self._dlp

    def input_allowed(self, text: str) -> bool:
        response = self.armor().sanitize_user_prompt(
            request={"name": ARMOR_TEMPLATE, "user_prompt_data": {"text": text}})
        return response.sanitization_result.filter_match_state.name == "NO_MATCH_FOUND"

    def deidentify(self, text: str) -> str:
        response = self.dlp().deidentify_content(request={
            "parent": f"projects/{PROJECT}/locations/{LOCATION}",
            "deidentify_template_name": DEID_TEMPLATE,
            "item": {"value": text},
        })
        return response.item.value


screening = Screening()
