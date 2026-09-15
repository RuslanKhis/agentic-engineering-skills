import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types

Lookup = Callable[[str], Awaitable[str]]


async def _lookup(lookup: Lookup, document: str) -> str:
    result = await lookup(document)
    if not isinstance(result, str):
        raise TypeError("Document review lookups must return strings")
    return result


class _DocumentReviewAgent(BaseAgent):
    policy_lookup: Lookup
    glossary_lookup: Lookup

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Invalidate earlier results through the Runner's persisted event path.
        # ADK state deltas support assignment, so None means no current result.
        stale = {
            key: None
            for key in ("policy_evidence", "glossary_evidence", "review_result")
            if key in ctx.session.state
        }
        if stale:
            yield Event(
                author=self.name,
                actions=EventActions(state_delta=stale),
            )

        parts = ctx.user_content.parts if ctx.user_content else None
        texts = [part.text for part in parts or [] if part.text is not None]
        if not texts:
            raise ValueError("Document review requires a text document")
        document = "".join(texts)

        tasks = [
            asyncio.create_task(_lookup(self.policy_lookup, document)),
            asyncio.create_task(_lookup(self.glossary_lookup, document)),
        ]
        try:
            policy, glossary = await asyncio.gather(*tasks)
        finally:
            # gather alone leaves siblings running when a lookup raises.
            # Cancel and drain them on failure or cancellation before returning.
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

        result = {"policy": policy, "glossary": glossary}
        yield Event(
            author=self.name,
            content=types.Content(
                role="model",
                parts=[types.Part(text=f"Policy:\n{policy}\n\nGlossary:\n{glossary}")],
            ),
            actions=EventActions(
                state_delta={
                    "policy_evidence": policy,
                    "glossary_evidence": glossary,
                    "review_result": result,
                }
            ),
        )


def build_workflow(policy_lookup: Lookup, glossary_lookup: Lookup) -> BaseAgent:
    """Run injected lookups concurrently and publish a review only on success.

    Lookups receive the current message's text, run once each without retries,
    and must cooperate with asyncio cancellation. Exceptions propagate through
    the Runner; a failed or cancelled run does not publish a combined result.
    """
    return _DocumentReviewAgent(
        name="document_review",
        policy_lookup=policy_lookup,
        glossary_lookup=glossary_lookup,
    )
