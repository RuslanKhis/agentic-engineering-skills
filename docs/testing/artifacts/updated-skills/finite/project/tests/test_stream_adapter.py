"""Offline contract tests through the existing public adapter."""

import asyncio
import traceback
import unittest

from stream_adapter import AnswerRejected, collect_answer


def event(text=None, *, partial=False, finish="STOP", **fields):
    value = {
        "invocation_id": "trusted-run",
        "author": "answer-agent",
        "partial": partial,
        "finish_reason": finish,
        "content": {"role": "model", "parts": [] if text is None else [{"text": text}]},
    }
    value.update(fields)
    return value


class Stream:
    def __init__(self, *items, close_error=None):
        self.items = iter(items)
        self.reads = 0
        self.exhausted = False
        self.closed = False
        self.close_calls = 0
        self.close_error = close_error

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            item = next(self.items)
        except StopIteration:
            self.exhausted = True
            raise StopAsyncIteration from None
        self.reads += 1
        if isinstance(item, BaseException):
            raise item
        return item

    async def aclose(self):
        self.close_calls += 1
        await asyncio.sleep(0)
        self.closed = True
        if self.close_error is not None:
            raise self.close_error


class AdapterTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.previews = []

    async def preview(self, text):
        self.previews.append(text)

    async def collect(self, stream, on_preview=None):
        return await collect_answer(
            stream, invocation_id="trusted-run", answer_author="answer-agent",
            on_preview=self.preview if on_preview is None else on_preview,
        )

    async def rejected(self, stream, on_preview=None):
        with self.assertRaises(AnswerRejected) as caught:
            await self.collect(stream, on_preview)
        self.assertTrue(stream.closed)
        self.assertEqual(stream.close_calls, 1)
        return caught.exception

    async def test_deltas_are_awaited_snapshots_and_final_replaces_them(self):
        stream = Stream(event("Bill", partial=True, finish=None),
                        event("ing.", partial=True, finish=None),
                        event("Billing. Corrected."), event())

        async def preview(text):
            self.assertEqual(stream.reads, len(self.previews) + 1)
            await asyncio.sleep(0)
            self.previews.append(text)

        self.assertEqual(await self.collect(stream, preview), "Billing. Corrected.")
        self.assertEqual(self.previews, ["Bill", "Billing."])
        self.assertTrue(stream.exhausted)
        self.assertTrue(stream.closed)
        self.assertEqual(stream.close_calls, 1)

    async def test_aggregate_only_with_camel_case_metadata(self):
        value = event("Complete")
        value["invocationId"] = value.pop("invocation_id")
        value["finishReason"] = value.pop("finish_reason")
        value.update(errorCode=None, errorMessage=None)
        stream = Stream(value)
        self.assertEqual(await self.collect(stream), "Complete")
        self.assertEqual(self.previews, [])
        self.assertTrue(stream.exhausted)
        self.assertTrue(stream.closed)

    async def test_partial_only_never_becomes_success(self):
        stream = Stream(event("Provisional", partial=True, finish="STOP"))
        await self.rejected(stream)
        self.assertEqual(self.previews, ["Provisional"])

    async def test_completion_is_required(self):
        for events in ([], [event()], [event("")], [event(" \n")],
                       [event("Unfinished", finish=None)]):
            with self.subTest(events=events):
                await self.rejected(Stream(*events))

    async def test_filters_authors_roles_thoughts_and_entire_tool_events(self):
        hidden = [event("other", author="helper", partial=True),
                  event("user", content={"role": "user", "parts": [{"text": "user"}]}),
                  event(content={"role": "model", "parts": [
                      {"text": "private", "thought": True}]}),
                  event(content={"role": "model", "parts": [
                      {"text": "tool narration"}, {"functionCall": {"name": "lookup"}}]})]
        visible = event(content={"role": "model", "parts": [
            {"text": "private", "thought": True}, {"text": "Public"}, {"text": " answer"}]})
        self.assertEqual(await self.collect(Stream(*hidden, visible)), "Public answer")
        self.assertEqual(self.previews, [])
        await self.rejected(Stream(*hidden))

    async def test_late_reported_errors_are_sticky_and_stream_is_drained(self):
        for name in ("error", "error_code", "errorCode", "error_message", "errorMessage"):
            with self.subTest(name=name):
                stream = Stream(event("Plausible"), event(**{name: "PRIVATE_MARKER"}),
                                event("Another plausible answer"), event())
                error = await self.rejected(stream)
                self.assertTrue(stream.exhausted)
                self.assertEqual(stream.reads, 4)
                self.assertNotIn("PRIVATE_MARKER", str(error))

    async def test_late_transport_failure_is_sanitized(self):
        stream = Stream(event("Plausible"), RuntimeError("PRIVATE_MARKER"))
        error = await self.rejected(stream)
        self.assertNotIn("PRIVATE_MARKER", "".join(traceback.format_exception(error)))
        self.assertIsNone(error.__context__)

    async def test_every_invocation_is_checked_even_on_ignored_events(self):
        for patch in ({"invocation_id": "wrong"}, {"invocation_id": None},
                      {"invocationId": "wrong"}):
            with self.subTest(patch=patch):
                stream = Stream(event("Good"), event(author="helper", **patch))
                await self.rejected(stream)

    async def test_finish_failure_and_interruption_even_after_final(self):
        for fields in ({"finish_reason": "MAX_TOKENS"}, {"finishReason": "MAX_TOKENS"},
                       {"finish_reason": "SAFETY"}, {"interrupted": True}):
            with self.subTest(fields=fields):
                await self.rejected(Stream(event("Good"), event(**fields)))

    async def test_second_complete_answer_rejects(self):
        await self.rejected(Stream(event("One"), event("Two")))

    async def test_callback_failure_is_sanitized_and_closes(self):
        async def preview(text):
            raise AnswerRejected("PRIVATE_MARKER")

        stream = Stream(event("Partial", partial=True, finish=None), event("Complete"))
        error = await self.rejected(stream, preview)
        self.assertNotIn("PRIVATE_MARKER", "".join(traceback.format_exception(error)))
        self.assertIsNone(error.__context__)

    async def test_close_failure_prevents_acceptance(self):
        stream = Stream(event("Complete"), close_error=RuntimeError("PRIVATE_MARKER"))
        error = await self.rejected(stream)
        self.assertNotIn("PRIVATE_MARKER", "".join(traceback.format_exception(error)))
        self.assertIsNone(error.__context__)

    async def test_preview_arrives_before_final_and_final_waits_for_exhaustion(self):
        preview_ready, after_final = asyncio.Event(), asyncio.Event()
        allow_final, allow_eof = asyncio.Event(), asyncio.Event()
        closed = asyncio.Event()

        async def source():
            try:
                yield event("Early", partial=True, finish=None)
                await allow_final.wait()
                yield event("Final")
                after_final.set()
                await allow_eof.wait()
                yield {"invocationId": "trusted-run"}
            finally:
                closed.set()

        async def preview(text):
            self.previews.append(text)
            preview_ready.set()

        task = asyncio.create_task(self.collect(source(), preview))
        try:
            await asyncio.wait_for(preview_ready.wait(), 1)
            self.assertEqual(self.previews, ["Early"])
            self.assertFalse(task.done())
            allow_final.set()
            await asyncio.wait_for(after_final.wait(), 1)
            self.assertFalse(task.done())
            self.assertEqual(self.previews, ["Early"])
        finally:
            allow_final.set()
            allow_eof.set()
            result = await asyncio.wait_for(task, 1)
        self.assertEqual(result, "Final")
        self.assertTrue(closed.is_set())

    async def test_whitespace_and_empty_deltas_are_preserved(self):
        stream = Stream(*(event(text, partial=True, finish=None)
                          for text in ("Hello", " ", "", "world")),
                        event("Hello world!"))
        self.assertEqual(await self.collect(stream), "Hello world!")
        self.assertEqual(self.previews, ["Hello", "Hello ", "Hello ", "Hello world"])

    async def test_partial_after_complete_answer_rejects_without_callback(self):
        await self.rejected(Stream(event("Complete"), event("Extra", partial=True)))
        self.assertEqual(self.previews, [])

    async def test_tool_payload_families_never_supply_answer_text(self):
        for field in ("function_call", "functionCall", "function_response", "functionResponse",
                      "executable_code", "executableCode", "code_execution_result",
                      "codeExecutionResult", "tool_call", "toolCall", "tool_response", "toolResponse"):
            with self.subTest(field=field):
                # The business payload is deliberately opaque to this adapter.
                tool = event(content={"role": "model", "parts": [
                    {"text": "Protocol narration"}, {field: {"error": "business failure"}}]})
                await self.rejected(Stream(tool))
                tool["partial"] = True
                stream = Stream(tool, event("Answer"), tool)
                self.assertEqual(await self.collect(stream), "Answer")
                self.assertTrue(stream.exhausted)
                self.assertEqual(self.previews, [])

    async def test_ignored_late_authors_and_thoughts_do_not_replace_answer(self):
        stream = Stream(event("Answer"), event("Other", author="helper"),
                        event(content={"role": "model", "parts": [
                            {"text": "Private", "thought": True}]}))
        self.assertEqual(await self.collect(stream), "Answer")
        self.assertTrue(stream.exhausted)

    async def test_identical_aliases_and_null_sdk_defaults_are_supported(self):
        value = event("Answer", invocationId="trusted-run", finishReason="STOP",
                      partial=None, interrupted=None, error_code=None, errorCode=None,
                      error_message="", errorMessage="")
        value["content"]["parts"][0].update(
            thought=None, function_call=None, functionCall=None,
            thought_signature=None, thoughtSignature=None, inlineData=None,
        )
        self.assertEqual(await self.collect(Stream(value)), "Answer")

    async def test_conflicting_aliases_and_malformed_markers_reject(self):
        values = [event("Answer", invocationId="wrong"),
                  event("Answer", finishReason="MAX_TOKENS"),
                  event("Answer", errorCode="", error_code="hidden"),
                  event("Answer", errorMessage="", error_message="hidden"),
                  event("Answer", partial=0), event("Answer", partial="false"),
                  event("Answer", interrupted="false"), event("Answer", finish_reason=1)]
        for value in values:
            with self.subTest(value=value):
                await self.rejected(Stream(value))
        self.assertEqual(self.previews, [])

    async def test_missing_identity_is_not_discovered_from_other_events(self):
        value = event("Untrusted", partial=True)
        del value["invocation_id"]
        await self.rejected(Stream(value, event("Complete")))
        self.assertEqual(self.previews, [])

    async def test_malformed_content_has_controlled_rejection(self):
        for value in (None, [], event(content="PRIVATE_MARKER"),
                      event(content={"role": "model", "parts": "PRIVATE_MARKER"}),
                      event(content={"role": "model", "parts": [None]}),
                      event(content={"role": "model", "parts": [{"text": 42}]}),
                      event(content={"role": "model", "parts": [{"text": "secret", "thought": "false"}]}),
                      event(content={"role": "model", "parts": [{"text": "label", "inlineData": {}}]})):
            with self.subTest(value=value):
                error = await self.rejected(Stream(value))
                self.assertNotIn("PRIVATE_MARKER", str(error))
        self.assertEqual(self.previews, [])

    async def test_closes_obtained_iterator_without_reacquiring_it(self):
        class Iterator(Stream):
            def __aiter__(self):
                raise AssertionError("Iterator must not be reacquired")

        iterator = Iterator(event("Answer"))

        class Source:
            calls = 0

            def __aiter__(self):
                self.calls += 1
                return iterator

            async def aclose(self):
                raise AssertionError("Close the obtained iterator")

        source = Source()
        self.assertEqual(await self.collect(source), "Answer")
        self.assertEqual(source.calls, 1)
        self.assertEqual(iterator.close_calls, 1)
        self.assertTrue(iterator.closed)

    async def test_iterator_without_aclose_is_supported(self):
        class Source:
            def __init__(self):
                self.items = iter([event("Answer")])

            def __aiter__(self):
                return self

            async def __anext__(self):
                try:
                    return next(self.items)
                except StopIteration:
                    raise StopAsyncIteration from None

        self.assertEqual(await self.collect(Source()), "Answer")

    async def test_iterator_acquisition_failure_is_sanitized(self):
        class Source:
            def __aiter__(self):
                raise RuntimeError("PRIVATE_MARKER")

        with self.assertRaises(AnswerRejected) as caught:
            await self.collect(Source())
        self.assertNotIn("PRIVATE_MARKER", "".join(traceback.format_exception(caught.exception)))
        self.assertIsNone(caught.exception.__context__)

    async def test_rejection_and_callback_failure_survive_close_failure(self):
        async def preview(text):
            raise RuntimeError("PRIVATE_CALLBACK")

        for stream, callback in (
            (Stream(event("Answer", interrupted=True), close_error=RuntimeError("PRIVATE_CLOSE")), None),
            (Stream(event("Preview", partial=True), close_error=RuntimeError("PRIVATE_CLOSE")), preview),
        ):
            with self.subTest(callback=callback):
                error = await self.rejected(stream, callback)
                formatted = "".join(traceback.format_exception(error))
                self.assertNotIn("PRIVATE_", formatted)
                self.assertIsNone(error.__context__)

    async def test_close_own_cancellation_is_controlled_failure(self):
        for values in ([event("Answer")], [event("Preview", partial=True)]):
            with self.subTest(values=values):
                error = await self.rejected(Stream(
                    *values, close_error=asyncio.CancelledError("PRIVATE_MARKER")))
                self.assertNotIn("PRIVATE_MARKER", "".join(traceback.format_exception(error)))

    async def test_original_cancellation_survives_close_failure(self):
        original = asyncio.CancelledError("caller cancellation")
        stream = Stream(original, close_error=RuntimeError("PRIVATE_MARKER"))
        try:
            await self.collect(stream)
        except asyncio.CancelledError as error:
            self.assertIs(error, original)
            self.assertNotIn("PRIVATE_MARKER", "".join(traceback.format_exception(error)))
        else:
            self.fail("Cancellation was not propagated")
        self.assertTrue(stream.closed)
        self.assertEqual(stream.close_calls, 1)

    async def test_task_cancellation_at_input_and_preview_closes_iterator(self):
        for phase in ("input", "preview", "after_final"):
            with self.subTest(phase=phase):
                waiting = asyncio.Event()

                class WaitingStream(Stream):
                    async def __anext__(self):
                        if phase == "input" or (phase == "after_final" and self.reads):
                            waiting.set()
                            await asyncio.Future()
                        return await super().__anext__()

                async def preview(text):
                    waiting.set()
                    await asyncio.Future()

                stream = WaitingStream(event("Text", partial=phase == "preview"))
                task = asyncio.create_task(self.collect(stream, preview))
                await asyncio.wait_for(waiting.wait(), 1)
                task.cancel("caller-marker")
                with self.assertRaises(asyncio.CancelledError) as caught:
                    await asyncio.wait_for(task, 1)
                self.assertEqual(caught.exception.args, ("caller-marker",))
                self.assertTrue(stream.closed)
                self.assertEqual(stream.close_calls, 1)

    async def test_cancellation_during_close_waits_for_owned_cleanup(self):
        for already_cancelled in (False, True):
            with self.subTest(already_cancelled=already_cancelled):
                closing, release = asyncio.Event(), asyncio.Event()
                original = asyncio.CancelledError("original-marker")

                class ClosingStream(Stream):
                    async def aclose(self):
                        self.close_calls += 1
                        closing.set()
                        await release.wait()
                        self.closed = True

                stream = ClosingStream(original if already_cancelled else event("Answer"))
                task = asyncio.create_task(self.collect(stream))
                await asyncio.wait_for(closing.wait(), 1)
                try:
                    task.cancel("during-close")
                    await asyncio.sleep(0)
                    self.assertFalse(task.done())
                    self.assertFalse(stream.closed)
                    task.cancel("second-cancellation")
                    await asyncio.sleep(0)
                    self.assertFalse(task.done())
                finally:
                    release.set()
                    with self.assertRaises(asyncio.CancelledError) as caught:
                        await asyncio.wait_for(task, 1)
                self.assertEqual(caught.exception.args,
                                 ("original-marker" if already_cancelled else "during-close",))
                self.assertTrue(stream.closed)
                self.assertEqual(stream.close_calls, 1)

    async def test_swallowed_input_cancellation_cannot_produce_success(self):
        waiting = asyncio.Event()

        class SuppressingStream(Stream):
            async def __anext__(self):
                if not self.reads:
                    waiting.set()
                    try:
                        await asyncio.Future()
                    except asyncio.CancelledError:
                        pass
                return await super().__anext__()

        stream = SuppressingStream(event("Answer"))
        task = asyncio.create_task(self.collect(stream))
        await asyncio.wait_for(waiting.wait(), 1)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, 1)
        self.assertTrue(stream.closed)
        self.assertEqual(stream.close_calls, 1)


if __name__ == "__main__":
    unittest.main()
