"""The tool-free SQL author: sees one domain's metadata, writes one BigQuery SELECT."""
from __future__ import annotations

import json

from google.adk.agents import LlmAgent

AUTHOR_INSTRUCTION = """\
You write one BigQuery Standard SQL SELECT statement that answers the question, using only the
tables, columns, joins and derived tables in the domain context below. Use fully qualified table
names. If the question cannot be answered from this context, reply exactly CANNOT_ANSWER.

Domain context:
{domain_context}
"""


def build_author(model: str, context: dict) -> LlmAgent:
    return LlmAgent(
        name="sql_author",
        model=model,
        instruction=AUTHOR_INSTRUCTION.replace("{domain_context}", json.dumps(context, indent=1)),
        tools=[],
        output_key="candidate_sql",
    )
