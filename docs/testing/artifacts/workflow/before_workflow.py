from typing import Awaitable, Callable
from google.adk.agents import BaseAgent

Lookup = Callable[[str], Awaitable[str]]


def build_workflow(policy_lookup: Lookup, glossary_lookup: Lookup) -> BaseAgent:
    """Build the document review workflow described in README.md."""
    raise NotImplementedError("The review workflow has not been implemented yet")
