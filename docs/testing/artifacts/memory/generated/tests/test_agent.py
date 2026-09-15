import asyncio
import sqlite3
from contextlib import closing

import pytest

from profile_store import ProfileStore, UserScope


def make_context(agent, scope, session_id="conversation-one", state=None):
    from google.adk.agents.invocation_context import InvocationContext
    from google.adk.agents.readonly_context import ReadonlyContext
    from google.adk.sessions.in_memory_session_service import InMemorySessionService
    from google.adk.sessions.session import Session

    return ReadonlyContext(
        InvocationContext(
            invocation_id=f"invocation-{session_id}",
            agent=agent,
            session_service=InMemorySessionService(),
            session=Session(
                id=session_id,
                app_name=scope.app_name,
                user_id=scope.user_id,
                state=state or {},
            ),
        )
    )


def instructions(agent, context):
    text, bypass_state_injection = asyncio.run(agent.canonical_instruction(context))
    assert bypass_state_injection is True
    return text


def test_existing_agent_reads_latest_preference_in_each_conversation(store, scope):
    from google.adk.agents import LlmAgent

    from agent import make_agent

    agent = make_agent(store, scope)
    assert isinstance(agent, LlmAgent)
    assert callable(agent.instruction)
    first = make_context(agent, scope)
    baseline = instructions(agent, first)
    assert baseline
    for language in ("English", "French", "Spanish", "Japanese"):
        assert language not in baseline

    writer = ProfileStore(store.path)
    writer.save_preferred_language(scope, "French", consent=True)
    assert "Answer in French" in instructions(agent, first)
    second = make_context(agent, scope, "conversation-two")
    assert "Answer in French" in instructions(agent, second)

    writer.save_preferred_language(scope, "Japanese", consent=True)
    changed = instructions(agent, first)
    assert "Answer in Japanese" in changed
    assert "French" not in changed
    rebuilt = make_agent(ProfileStore(store.path), scope)
    assert "Answer in Japanese" in instructions(rebuilt, make_context(rebuilt, scope))

    writer.forget_preferred_language(scope)
    assert instructions(agent, first) == baseline
    assert instructions(agent, second) == baseline
    assert instructions(rebuilt, make_context(rebuilt, scope)) == baseline


def test_instruction_scope_is_trusted_and_users_can_forget_independently(store, scope):
    from agent import make_agent

    bob = UserScope(scope.app_name, "synthetic-bob")
    other_app = UserScope("different-app", scope.user_id)
    owners = [scope, bob, other_app]
    languages = ["French", "Japanese", "Spanish"]
    agents = [make_agent(store, owner) for owner in owners]
    # Session identity and model-visible state cannot redirect a bound agent.
    contexts = [
        make_context(
            agent,
            bob,
            state={
                "app_name": other_app.app_name,
                "user_id": bob.user_id,
                "preferred_language": "English",
                "user:preferred_language": "English",
                "conversation": "SYNTHETIC_PRIVATE_CONVERSATION",
            },
        )
        for agent in agents
    ]
    for owner, language in zip(owners, languages):
        store.save_preferred_language(owner, language, consent=True)

    for index, (agent, context) in enumerate(zip(agents, contexts)):
        text = instructions(agent, context)
        assert f"Answer in {languages[index]}" in text
        for other in set(languages + ["English"]) - {languages[index]}:
            assert other not in text
        for owner in owners:
            assert owner.app_name not in text
            assert owner.user_id not in text
        assert "SYNTHETIC_PRIVATE_CONVERSATION" not in text

    # Check before forgetting, while all preferences are still stored.
    with closing(sqlite3.connect(store.path)) as connection:
        dump = "\n".join(connection.iterdump())
    assert "SYNTHETIC_PRIVATE_CONVERSATION" not in dump

    for index, owner in enumerate(owners):
        store.forget_preferred_language(owner)
        for other_index, (agent, context) in enumerate(zip(agents, contexts)):
            text = instructions(agent, context)
            if other_index <= index:
                assert all(language not in text for language in languages)
                assert "English" not in text
            else:
                assert f"Answer in {languages[other_index]}" in text


def test_instruction_read_failure_propagates_without_cached_language(store, scope):
    from agent import make_agent

    store.save_preferred_language(scope, "French", consent=True)
    agent = make_agent(store, scope)
    context = make_context(agent, scope)
    assert "French" in instructions(agent, context)
    with closing(sqlite3.connect(store.path)) as connection, connection:
        connection.execute("DROP TABLE preferred_languages")
    with pytest.raises(sqlite3.OperationalError):
        instructions(agent, context)
