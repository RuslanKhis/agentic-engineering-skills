"""The extraction agent."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from extractor.schema import ClaimExtraction
from extractor.tools import lookup_policy, lookup_repairer

INSTRUCTION = """\
You extract motor-insurance claims for the claims queue.

Read the claim email and any attachment text in the user's message. Check the policy number
with lookup_policy and, if the customer names a garage, find it with lookup_repairer.
Fill every field of the ClaimExtraction you can support from the email; leave the rest empty and
list what is missing in missing_information. Copy the claim reference exactly from the subject.

Return ONLY the JSON object. Do not add any explanation.
"""

extraction_agent = LlmAgent(
    name="claim_extractor",
    model=os.environ.get("EXTRACTOR_MODEL", "gemini-3.5-flash"),
    instruction=INSTRUCTION,
    tools=[lookup_policy, lookup_repairer],
    output_schema=ClaimExtraction,
    output_key="extraction",
    planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(thinking_budget=1024)),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)

root_agent = extraction_agent
