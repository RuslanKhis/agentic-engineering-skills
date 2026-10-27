"""Where model-written code may run: one named sandbox in the EU project, or nowhere."""
from __future__ import annotations

import os
import re

PROJECT = "fjord-uw-prod"
REGION = "europe-west4"

_SANDBOX_NAME = re.compile(
    rf"projects/{re.escape(PROJECT)}/locations/{re.escape(REGION)}"
    r"/reasoningEngines/\d+/sandboxEnvironments/\d+"
)


def sandbox_resource_name() -> str:
    """Return SANDBOX_RESOURCE_NAME if it names a sandbox in the EU project, else raise.

    The executor's lazy path would create an engine in GOOGLE_CLOUD_LOCATION, whose library default
    is a US region, so the name is mandatory and validated at start-up: the service fails closed.
    """
    name = os.environ.get("SANDBOX_RESOURCE_NAME", "")
    if not _SANDBOX_NAME.fullmatch(name):
        raise RuntimeError(
            f"SANDBOX_RESOURCE_NAME must match projects/{PROJECT}/locations/{REGION}"
            "/reasoningEngines/<id>/sandboxEnvironments/<id>"
        )
    return name
