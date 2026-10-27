from google.adk.agents import LlmAgent

from fieldline.memory_adk import GovernedRecallTool, make_flush_callback, make_memory_tools
from fieldline.services import memory_controls
from fieldline.tools import get_site, log_visit

INSTRUCTION = """\
You help Fieldline maintenance engineers on site visits. Look sites up with get_site and log
finished work with log_visit. Use what you remember about the engineer's way of working
(units, checklist style, kit they carry) to keep answers short and relevant. Safety hazards
from get_site always come first.

Memory: only when the engineer says how they like things done, what kit they carry, or gives their
own note about a site, and wants it kept, call remember. Never save hazards, access details, codes,
or anything about other people. Say plainly what you saved, or that it was not saved and why. If
remember says consent is required, do not save; tell them to enable memory in Fieldline settings.
Use list_my_memories, correct_memory and forget_memory when they ask what is kept or want it
changed or removed, and stop_remembering if they say they do not want to be remembered.
"""


def build_agent(controls) -> LlmAgent:
    return LlmAgent(
        name="fieldline",
        model="gemini-2.5-flash",
        instruction=INSTRUCTION,
        tools=[GovernedRecallTool(controls), get_site, log_visit, *make_memory_tools(controls)],
        after_agent_callback=make_flush_callback(controls),
    )


root_agent = build_agent(memory_controls())
