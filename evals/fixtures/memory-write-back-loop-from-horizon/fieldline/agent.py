from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from fieldline.tools import get_site, log_visit

INSTRUCTION = """\
You help Fieldline maintenance engineers on site visits. Look sites up with get_site and log
finished work with log_visit. Use what you remember about the engineer's way of working
(units, checklist style, kit they carry) to keep answers short and relevant. Safety hazards
from get_site always come first.
"""

root_agent = LlmAgent(
    name="fieldline",
    model="gemini-2.5-flash",
    instruction=INSTRUCTION,
    tools=[PreloadMemoryTool(), get_site, log_visit],
)
