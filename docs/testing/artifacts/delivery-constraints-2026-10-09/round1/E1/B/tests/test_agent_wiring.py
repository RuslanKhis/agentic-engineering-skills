"""Needs google-adk: checks cancel_order is only exposed behind confirmation."""
import pytest

pytest.importorskip("google.adk")

from google.adk.tools import FunctionTool  # noqa: E402

from support_agent import tools  # noqa: E402
from support_agent.agent import root_agent  # noqa: E402


def test_cancel_order_requires_confirmation():
    wrapped = [t for t in root_agent.tools if isinstance(t, FunctionTool) and t.func is tools.cancel_order]
    assert len(wrapped) == 1
    assert wrapped[0]._require_confirmation is True
    assert tools.cancel_order not in root_agent.tools
