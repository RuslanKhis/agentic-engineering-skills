"""Duck-typed tool context for calling tool functions directly (not an ADK ToolContext)."""
from dataclasses import dataclass, field


@dataclass
class FakeToolContext:
    user_id: str
    state: dict = field(default_factory=dict)
