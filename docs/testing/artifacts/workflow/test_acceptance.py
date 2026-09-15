import asyncio
import uuid
import pytest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from workflow import build_workflow

async def invoke(agent, text, service=None, user="u1", session_id=None):
    service = service or InMemorySessionService()
    sid = session_id or uuid.uuid4().hex
    await service.create_session(app_name="review", user_id=user, session_id=sid)
    runner = Runner(agent=agent, app_name="review", session_service=service)
    events=[]
    error=None
    try:
        async for event in runner.run_async(user_id=user,session_id=sid,new_message=types.Content(role="user",parts=[types.Part(text=text)])):
            events.append(event)
    except Exception as exc:
        error=exc
    session=await service.get_session(app_name="review",user_id=user,session_id=sid)
    return session,events,error

@pytest.mark.asyncio
async def test_real_adk_runner_overlaps_and_combines():
    entered=[asyncio.Event(),asyncio.Event()]
    calls=[]
    async def policy(text):
        calls.append(("policy",text)); entered[0].set()
        await asyncio.wait_for(entered[1].wait(), 2)
        return "policy:"+text
    async def glossary(text):
        calls.append(("glossary",text)); entered[1].set()
        await asyncio.wait_for(entered[0].wait(), 2)
        return "glossary:"+text
    session,events,error=await invoke(build_workflow(policy,glossary), "refund terms")
    assert error is None, repr(error)
    assert sorted(calls)==[("glossary","refund terms"),("policy","refund terms")]
    assert session.state["policy_evidence"]=="policy:refund terms"
    assert session.state["glossary_evidence"]=="glossary:refund terms"
    assert session.state["review_result"]=={"policy":"policy:refund terms","glossary":"glossary:refund terms"}
    final=[e for e in events if e.is_final_response() and e.content]
    text="\n".join(p.text or "" for e in final for p in e.content.parts or [])
    assert "policy:refund terms" in text and "glossary:refund terms" in text

@pytest.mark.asyncio
async def test_lookup_failure_does_not_publish_success():
    async def policy(text): raise ValueError("synthetic lookup failure")
    async def glossary(text): return "only one source"
    session,events,error=await invoke(build_workflow(policy,glossary), "failure case")
    assert "review_result" not in session.state or session.state["review_result"] is None
    assert error is not None or any(e.error_message for e in events) or any(e.content and any("fail" in (p.text or "").lower() or "error" in (p.text or "").lower() for p in e.content.parts or []) for e in events)

@pytest.mark.asyncio
async def test_same_workflow_separate_sessions_keep_results_isolated():
    async def policy(text): return "policy:"+text
    async def glossary(text): return "glossary:"+text
    agent=build_workflow(policy,glossary)
    service=InMemorySessionService()
    a,_,err_a=await invoke(agent,"alpha",service,"alice")
    b,_,err_b=await invoke(agent,"beta",service,"bob")
    assert err_a is None and err_b is None
    assert a.state["review_result"]=={"policy":"policy:alpha","glossary":"glossary:alpha"}
    assert b.state["review_result"]=={"policy":"policy:beta","glossary":"glossary:beta"}
