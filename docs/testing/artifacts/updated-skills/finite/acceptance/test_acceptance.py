"""Independent checks of the published task contract; no external services.

Run with the evaluated project's root on PYTHONPATH. These tests live outside
that project so the coding agent does not use them as its implementation recipe.
"""

import asyncio
import unittest

from stream_adapter import AnswerRejected, collect_answer


INVOCATION = "trusted-invocation-41"
AUTHOR = "warehouse_answer"
PRIVATE = "SYNTHETIC_PRIVATE_PROVIDER_DETAIL_41"


def event(text=None, *, partial=False, finish=None, author=AUTHOR,
          invocation=INVOCATION, thought=False, camel=False, **extra):
    value = {
        "author": author,
        "invocationId" if camel else "invocation_id": invocation,
        "partial": partial,
        "content": {"role": "model", "parts": []},
        **extra,
    }
    if text is not None:
        value["content"]["parts"].append({"text": text, "thought": thought})
    if finish is not None:
        value["finishReason" if camel else "finish_reason"] = finish
    return value


class Stream:
    def __init__(self, items, *, failure=None, close_failure=None):
        self.items = list(items)
        self.failure = failure
        self.close_failure = close_failure
        self.reads = 0
        self.exhausted = False
        self.closed = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.reads += 1
        if self.items:
            return self.items.pop(0)
        if self.failure is not None:
            raise self.failure
        self.exhausted = True
        raise StopAsyncIteration

    async def aclose(self):
        self.closed += 1
        if self.close_failure is not None:
            raise self.close_failure


class Acceptance(unittest.IsolatedAsyncioTestCase):
    async def invoke(self, source, previews=None, callback=None):
        async def record(snapshot):
            if previews is not None:
                previews.append(snapshot)

        return await collect_answer(
            source, invocation_id=INVOCATION, answer_author=AUTHOR,
            on_preview=callback or record,
        )

    async def reject(self, source, *, callback=None):
        with self.assertRaises(AnswerRejected) as raised:
            await self.invoke(source, callback=callback)
        self.assertNotIn(PRIVATE, str(raised.exception))
        self.assertEqual(source.closed, 1)
        return raised.exception

    async def test_complete_answer_replaces_delta_preview_and_waits_for_exhaustion(self):
        for camel in (False, True):
            with self.subTest(camel=camel):
                source = Stream([
                    event("Hello ", partial=True, camel=camel),
                    event("world.", partial=True, camel=camel),
                    event("Hello world.", finish="STOP", camel=camel),
                    event(camel=camel),  # Content-free metadata may follow.
                ])
                previews = []
                self.assertEqual(await self.invoke(source, previews), "Hello world.")
                self.assertEqual(previews, ["Hello ", "Hello world."])
                self.assertTrue(source.exhausted)
                self.assertEqual(source.closed, 1)

    async def test_only_designated_public_model_text_is_displayed(self):
        protocol = event("Do not display tool narration.")
        protocol["content"]["parts"].append({"function_call": {
            "id": "call-41", "name": "lookup_stock", "args": {},
        }})
        source = Stream([
            event("Hidden reasoning.", partial=True, thought=True),
            event("Other agent's work.", partial=True, author="inventory_worker"),
            protocol,
            event("In stock.", partial=True),
            event("In stock.", finish="STOP"),
        ])
        previews = []
        self.assertEqual(await self.invoke(source, previews), "In stock.")
        self.assertEqual(previews, ["In stock."])
        self.assertEqual(source.closed, 1)

    async def test_late_reported_error_invalidates_the_candidate(self):
        for camel in (False, True):
            with self.subTest(camel=camel):
                error_fields = {
                    "errorCode" if camel else "error_code": "PROVIDER_FAILED",
                    "errorMessage" if camel else "error_message": PRIVATE,
                }
                source = Stream([
                    event("Looks complete.", finish="STOP", camel=camel),
                    event(camel=camel, **error_fields),
                ])
                await self.reject(source)
                self.assertEqual(source.items, [])

    async def test_late_transport_failure_invalidates_the_candidate(self):
        await self.reject(Stream(
            [event("Looks complete.", finish="STOP")],
            failure=RuntimeError(PRIVATE),
        ))

    async def test_incomplete_or_unaccepted_outcomes_are_rejected(self):
        cases = [
            [],
            [event("Only a partial", partial=True)],
            [event("No finish reason")],
            [event("Truncated", finish="MAX_TOKENS")],
            [event("Interrupted", finish="STOP", interrupted=True)],
            [event("Hidden", finish="STOP", thought=True)],
            [event("Wrong speaker", finish="STOP", author="inventory_worker")],
            [event("First", finish="STOP"), event("Second", finish="STOP")],
        ]
        for index, items in enumerate(cases):
            with self.subTest(case=index):
                await self.reject(Stream(items))

    async def test_wrong_invocation_is_rejected_before_its_preview(self):
        source = Stream([
            event("Wrong invocation", partial=True, invocation="other-invocation"),
            event("Otherwise complete", finish="STOP"),
        ])
        previews = []
        with self.assertRaises(AnswerRejected):
            await self.invoke(source, previews)
        self.assertEqual(previews, [])
        self.assertEqual(source.closed, 1)

    async def test_callback_failure_rejects_without_disclosing_content(self):
        async def failed_callback(snapshot):
            raise RuntimeError(PRIVATE)

        await self.reject(Stream([
            event("Preview", partial=True), event("Answer", finish="STOP"),
        ]), callback=failed_callback)

    async def test_close_failure_prevents_returning_a_success(self):
        await self.reject(Stream(
            [event("Answer", finish="STOP")], close_failure=RuntimeError(PRIVATE),
        ))

    async def test_caller_cancellation_propagates_and_closes_owned_iterator(self):
        entered = asyncio.Event()
        never = asyncio.Event()

        class StalledStream(Stream):
            async def __anext__(self):
                entered.set()
                await never.wait()
                raise AssertionError("The fixture should remain stalled")

        source = StalledStream([])
        task = asyncio.create_task(self.invoke(source))
        try:
            await asyncio.wait_for(entered.wait(), timeout=2)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, timeout=2)
            self.assertEqual(source.closed, 1)
        finally:
            if not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

    def test_unrelated_configuration_is_preserved(self):
        from application_config import APPLICATION_NAME, PUBLIC_ROUTE

        self.assertEqual(APPLICATION_NAME, "warehouse-support")
        self.assertEqual(PUBLIC_ROUTE, "/v2/assist")


if __name__ == "__main__":
    unittest.main()
