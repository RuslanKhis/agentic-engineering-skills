import asyncio
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.sessions import InMemorySessionService, Session
from agent import make_agent
from profile_store import ProfileStore, UserScope


def resolve(agent, session_id):
    context = ReadonlyContext(InvocationContext(
        session_service=InMemorySessionService(),
        invocation_id=f"invoke-{session_id}",
        session=Session(id=session_id, app_name="support", user_id="alice"),
    ))
    text, uses_provider = asyncio.run(agent.canonical_instruction(context))
    assert uses_provider
    return text


def test_new_adk_sessions_read_persisted_profile(tmp_path):
    path = tmp_path / "profiles.sqlite3"
    scope = UserScope("support", "alice")
    first = ProfileStore(path)
    first.save_preferred_language(scope, "French", consent=True)
    assert "French" in resolve(make_agent(first, scope), "conversation-1")
    second = ProfileStore(path)
    assert "French" in resolve(make_agent(second, scope), "conversation-2")


def test_adk_instruction_resolution_rechecks_after_forgetting(tmp_path):
    store = ProfileStore(tmp_path / "profiles.sqlite3")
    scope = UserScope("support", "alice")
    agent = make_agent(store, scope)
    store.save_preferred_language(scope, "Japanese", consent=True)
    assert "Japanese" in resolve(agent, "conversation-1")
    store.forget_preferred_language(scope)
    assert "Japanese" not in resolve(agent, "conversation-1")
