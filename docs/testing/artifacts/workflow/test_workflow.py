"""Offline acceptance through the actual ADK Runner with synthetic lookups."""

import asyncio
import socket

import google.auth
from google import genai
from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import pytest

from workflow import build_workflow


APP = "document_review"
USER = "synthetic-user"
TIMEOUT = 3  # Deadlock guard, never an overlap/latency acceptance threshold.


@pytest.fixture(autouse=True)
def offline_only(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Network, Google clients and credentials are forbidden")

    for name in ("connect", "connect_ex", "sendto"):
        monkeypatch.setattr(socket.socket, name, forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    monkeypatch.setattr(genai, "Client", forbidden)
    monkeypatch.setattr(google.auth, "default", forbidden)


@pytest.fixture
async def runner_factory():
    runners = []

    def make(policy, glossary):
        agent = build_workflow(policy, glossary)
        assert isinstance(agent, BaseAgent)
        runner = Runner(
            app_name=APP,
            agent=agent,
            session_service=InMemorySessionService(),
        )
        runners.append(runner)
        return runner

    yield make
    for runner in runners:
        await runner.close()


async def create_session(runner, session_id="review", state=None):
    return await runner.session_service.create_session(
        app_name=APP, user_id=USER, session_id=session_id, state=state
    )


async def stored_state(runner, session_id="review"):
    session = await runner.session_service.get_session(
        app_name=APP, user_id=USER, session_id=session_id
    )
    assert session is not None
    return session.state


async def consume(runner, events, document="Synthetic document", session_id="review"):
    message = (
        types.Content(role="user", parts=[types.Part(text=document)])
        if isinstance(document, str)
        else document
    )
    async for event in runner.run_async(
        user_id=USER, session_id=session_id, new_message=message
    ):
        events.append(event)


def final_texts(events):
    # ADK also classifies contentless state events as final; they are not reviews.
    return [
        "".join(part.text for part in event.content.parts or [] if part.text is not None)
        for event in events
        if event.is_final_response() and event.content is not None
    ]


def assert_no_review(events):
    assert final_texts(events) == []
    assert all(event.actions.state_delta.get("review_result") is None for event in events)


@pytest.mark.parametrize("first", ["policy", "glossary"])
async def test_lookups_overlap_and_merge_waits_for_both(runner_factory, first):
    started = {name: asyncio.Event() for name in ("policy", "glossary")}
    release = {name: asyncio.Event() for name in started}
    completed = {name: asyncio.Event() for name in started}
    calls = []
    outputs = {"policy": "  synthetic policy\nα  ", "glossary": "synthetic terms\nβ"}
    document = "Synthetic document\nwith terminology."

    def lookup(name, other):
        async def run(text):
            calls.append((name, text))
            started[name].set()
            await started[other].wait()
            await release[name].wait()
            completed[name].set()
            return outputs[name]

        return run

    runner = runner_factory(lookup("policy", "glossary"), lookup("glossary", "policy"))
    await create_session(runner, state={"unrelated": "preserved"})
    events = []
    message = types.Content(
        role="user",
        parts=[types.Part(text="Synthetic document\n"), types.Part(text="with terminology.")],
    )
    task = asyncio.create_task(consume(runner, events, message))
    try:
        async with asyncio.timeout(TIMEOUT):
            await asyncio.gather(*(event.wait() for event in started.values()))
            assert sorted(calls) == [("glossary", document), ("policy", document)]
            assert_no_review(events)
            assert "review_result" not in await stored_state(runner)

            release[first].set()
            await completed[first].wait()
            assert not task.done()
            assert_no_review(events)
            assert "review_result" not in await stored_state(runner)

            release["glossary" if first == "policy" else "policy"].set()
            await task
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

    assert await stored_state(runner) == {
        "unrelated": "preserved",
        "policy_evidence": outputs["policy"],
        "glossary_evidence": outputs["glossary"],
        "review_result": outputs,
    }
    assert final_texts(events) == [
        f"Policy:\n{outputs['policy']}\n\nGlossary:\n{outputs['glossary']}"
    ]
    commits = [event for event in events if event.actions.state_delta.get("review_result")]
    assert len(commits) == 1
    assert commits[0].is_final_response()
    assert len(calls) == 2


@pytest.mark.parametrize("failed_branch", ["policy", "glossary"])
@pytest.mark.parametrize("sibling_completes", [False, True])
async def test_failure_propagates_and_drains_sibling(
    runner_factory, failed_branch, sibling_completes
):
    failing_started = asyncio.Event()
    sibling_started = asyncio.Event()
    sibling_finished = asyncio.Event()
    calls = []
    failure = RuntimeError(f"Synthetic {failed_branch} lookup failure")

    async def failing(document):
        calls.append(("failing", document))
        failing_started.set()
        await sibling_started.wait()
        if sibling_completes:
            await sibling_finished.wait()
        raise failure

    async def sibling(document):
        calls.append(("sibling", document))
        sibling_started.set()
        try:
            await failing_started.wait()
            if sibling_completes:
                return "Synthetic completed evidence"
            await asyncio.Event().wait()
        finally:
            sibling_finished.set()

    lookups = (failing, sibling) if failed_branch == "policy" else (sibling, failing)
    runner = runner_factory(*lookups)
    await create_session(runner)
    events = []
    async with asyncio.timeout(TIMEOUT):
        with pytest.raises(RuntimeError) as caught:
            await consume(runner, events)
    assert caught.value is failure
    assert sibling_finished.is_set()
    assert len(calls) == 2
    assert_no_review(events)
    assert "review_result" not in await stored_state(runner)


@pytest.mark.parametrize("invalid", [None, 42, {"policy": "synthetic"}])
@pytest.mark.parametrize("failed_branch", ["policy", "glossary"])
async def test_non_string_lookup_result_is_a_failure(runner_factory, invalid, failed_branch):
    async def invalid_lookup(document):
        return invalid

    async def valid_lookup(document):
        return "Synthetic evidence"

    lookups = (
        (invalid_lookup, valid_lookup)
        if failed_branch == "policy"
        else (valid_lookup, invalid_lookup)
    )
    runner = runner_factory(*lookups)
    await create_session(runner)
    events = []
    with pytest.raises(TypeError, match="must return strings"):
        await consume(runner, events)
    assert_no_review(events)
    assert "review_result" not in await stored_state(runner)


async def test_cancellation_drains_both_lookups_without_success(runner_factory):
    started = [asyncio.Event(), asyncio.Event()]
    finished = [asyncio.Event(), asyncio.Event()]

    def lookup(index):
        async def run(document):
            started[index].set()
            try:
                await asyncio.Event().wait()
            finally:
                finished[index].set()

        return run

    runner = runner_factory(lookup(0), lookup(1))
    await create_session(runner)
    events = []
    task = asyncio.create_task(consume(runner, events))
    try:
        async with asyncio.timeout(TIMEOUT):
            await asyncio.gather(*(event.wait() for event in started))
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
    assert all(event.is_set() for event in finished)
    assert_no_review(events)
    assert "review_result" not in await stored_state(runner)


async def test_sessions_are_isolated_and_failed_repeat_invalidates_old_result(runner_factory):
    async def policy(document):
        if document == "Synthetic failure":
            raise RuntimeError("Synthetic failure")
        return f"Policy for {document}"

    async def glossary(document):
        return f"Glossary for {document}"

    runner = runner_factory(policy, glossary)
    await create_session(runner, "first", {"unrelated": "preserved"})
    await create_session(runner, "second")
    await create_session(runner, "failed")
    await consume(runner, [], "Synthetic first", "first")
    first_state = await stored_state(runner, "first")
    assert first_state["review_result"] == {
        "policy": "Policy for Synthetic first", "glossary": "Glossary for Synthetic first"
    }
    assert "review_result" not in await stored_state(runner, "second")
    await consume(runner, [], "Synthetic second", "second")
    second_state = await stored_state(runner, "second")
    assert second_state["review_result"] == {
        "policy": "Policy for Synthetic second", "glossary": "Glossary for Synthetic second"
    }
    assert await stored_state(runner, "first") == first_state

    for session_id in ("failed", "first"):
        events = []
        with pytest.raises(RuntimeError, match="Synthetic failure"):
            await consume(runner, events, "Synthetic failure", session_id)
        assert_no_review(events)
        state = await stored_state(runner, session_id)
        assert state.get("review_result") is None
        assert state.get("policy_evidence") is None
        assert state.get("glossary_evidence") is None

    assert (await stored_state(runner, "first"))["unrelated"] == "preserved"
    assert await stored_state(runner, "second") == second_state
    # The same session can recover, using the new message rather than its history.
    events = []
    await consume(runner, events, "Synthetic recovery", "first")
    assert (await stored_state(runner, "first"))["review_result"] == {
        "policy": "Policy for Synthetic recovery", "glossary": "Glossary for Synthetic recovery"
    }
    assert len(final_texts(events)) == 1


async def test_empty_strings_are_preserved(runner_factory):
    async def lookup(document):
        assert document == ""
        return ""

    runner = runner_factory(lookup, lookup)
    await create_session(runner)
    events = []
    await consume(runner, events, "")
    assert (await stored_state(runner))["review_result"] == {"policy": "", "glossary": ""}
    assert final_texts(events) == ["Policy:\n\n\nGlossary:\n"]


async def test_non_text_message_invalidates_previous_review(runner_factory):
    async def lookup(document):
        pytest.fail("A non-text message must not reach a lookup")

    runner = runner_factory(lookup, lookup)
    await create_session(runner, state={"review_result": {"policy": "old", "glossary": "old"}})
    events = []
    with pytest.raises(ValueError, match="requires a text document"):
        await consume(
            runner,
            events,
            types.Content(role="user", parts=[types.Part(inline_data=types.Blob(
                mime_type="application/octet-stream", data=b"synthetic"
            ))]),
        )
    assert_no_review(events)
    assert (await stored_state(runner))["review_result"] is None
