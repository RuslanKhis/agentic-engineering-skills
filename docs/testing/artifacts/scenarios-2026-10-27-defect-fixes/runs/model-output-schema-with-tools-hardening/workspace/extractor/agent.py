"""The extraction agent: a tool-using gatherer followed by a tool-free formatter.

On the API-key backend ADK 2.8.0 does not send a response schema when an agent has tools; it adds a
`set_model_response` tool instead and the model may answer in prose or fenced JSON. So the schema
lives on a second agent with no tools, which always takes the native response_schema path.
"""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent, SequentialAgent
from google.genai import types

from extractor.probe import request_probe
from extractor.schema import ClaimExtraction
from extractor.tools import lookup_policy, lookup_repairer

MODEL = os.environ.get("EXTRACTOR_MODEL", "gemini-3.5-flash")

GATHER_INSTRUCTION = """\
You prepare motor-insurance claim facts for the claims queue.

Read the claim email and any attachment text in the user's message. Check the policy number
with lookup_policy and, if the customer names a garage, find it with lookup_repairer.
Then write plain notes: every fact the email supports (claim reference copied exactly from the
subject, policy number, claimant, vehicle, incident, third party, injuries, repairer, fault, claim
type, urgency), the exact lookup results, and a list of what the email does not say.
Do not guess missing facts.
"""

FORMAT_INSTRUCTION = """\
Turn the claim notes below into the ClaimExtraction record. Use only the notes and the original
claim email. Leave unsupported fields empty and list what is missing in missing_information.
Copy the claim reference exactly.

Notes:
{claim_notes}
"""

gather_agent = LlmAgent(
    name="claim_gatherer",
    model=MODEL,
    instruction=GATHER_INSTRUCTION,
    tools=[lookup_policy, lookup_repairer],
    output_key="claim_notes",
    # Gemini 3: thinking_level only, default temperature. No planner, so there is one thinking config.
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
    before_model_callback=request_probe,
)

format_agent = LlmAgent(
    name="claim_formatter",
    model=MODEL,
    instruction=FORMAT_INSTRUCTION,
    output_schema=ClaimExtraction,
    output_key="extraction",
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
    before_model_callback=request_probe,
)

extraction_agent = SequentialAgent(name="claim_extractor", sub_agents=[gather_agent, format_agent])

root_agent = extraction_agent
