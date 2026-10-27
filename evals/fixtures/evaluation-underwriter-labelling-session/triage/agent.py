import os

from google.adk.agents import LlmAgent

from triage.prompts import INSTRUCTION

root_agent = LlmAgent(name="claims_triage", model=os.environ.get("MODEL_ID", "gemini-3.5-flash"),
                      instruction=INSTRUCTION)
