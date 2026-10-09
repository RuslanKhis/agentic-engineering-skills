"""Needs google-adk installed (runs in CI); checks cancel_order is confirmation-gated."""
import pytest

pytest.importorskip("google.adk")

from google.adk.tools import FunctionTool  # noqa: E402

from support_agent import tools  # noqa: E402
from support_agent.agent import root_agent  # noqa: E402


def test_cancel_order_is_only_registered_behind_confirmation():
    assert tools.cancel_order not in root_agent.tools
    wrapped = [t for t in root_agent.tools if isinstance(t, FunctionTool) and t.func is tools.cancel_order]
    assert len(wrapped) == 1
    # Private attribute name as read from ADK 2.8.0 source; unverified here.
    assert wrapped[0]._require_confirmation is True
