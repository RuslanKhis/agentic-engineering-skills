"""Adversarial finite-stream acceptance tests; no provider or transport calls."""

import asyncio
import copy
from dataclasses import replace
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import sys
import traceback
import unittest
from unittest.mock import patch


def event(text="complete", *, partial=False, **updates):
    value = {
        "author": "answer", "invocationId": "synthetic-invocation",
        "partial": partial,
        "content": {"role": "model", "parts": [{"text": text}]},
    }
    if not partial:
        value["finishReason"] = "STOP"
    value.update(updates)
    return value


def compact_size(value):
    return len(json.dumps(value, ensure_ascii=False, allow_nan=False,
                          separators=(",", ":")).encode("utf-8"))


class TrackedStream:
    def __init__(self, values, *, close_error=None):
        self.values = iter(values)
        self.closed = 0
        self.close_error = close_error
        self.pulls = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.pulls += 1
        try:
            value = next(self.values)
        except StopIteration:
            raise StopAsyncIteration
        if isinstance(value, BaseException):
            raise value
        return value

    async def aclose(self):
        self.closed += 1
        if self.close_error:
            raise self.close_error


class FiniteAnswerStream(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        for target in ("socket.socket.connect", "socket.socket.connect_ex",
                       "socket.create_connection", "socket.getaddrinfo"):
            guard = patch(target, side_effect=AssertionError("Network is prohibited"))
            guard.start()
            self.addCleanup(guard.stop)
        name = "finite_answer_stream_under_test"
        source = Path(__file__).resolve().parents[1] / "assets/finite_answer_stream.py"
        spec = importlib.util.spec_from_file_location(name, source)
        self.asset = importlib.util.module_from_spec(spec)
        previous = sys.modules.get(name)
        sys.modules[name] = self.asset
        self.addCleanup(self.restore_module, name, previous)
        spec.loader.exec_module(self.asset)
        self.previews = []

    @staticmethod
    def restore_module(name, previous):
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous

    async def consume(self, stream, **overrides):
        async def display(text):
            self.previews.append(text)
        options = dict(answer_author="answer", invocation_id="synthetic-invocation",
                       preview_mode="delta", send_preview=display)
        options.update(overrides)
        return await self.asset.consume_answer(stream, **options)

    async def reject(self, values, code=None, **options):
        stream = values if hasattr(values, "__aiter__") else TrackedStream(values)
        with self.assertRaises(self.asset.StreamRejected) as caught:
            await self.consume(stream, **options)
        if code is not None:
            self.assertEqual(str(caught.exception), code)
        self.assertIsNone(caught.exception.__context__)
        self.assertIsNone(caught.exception.__cause__)
        if hasattr(stream, "closed"):
            self.assertEqual(stream.closed, 1)
        return caught.exception

    async def test_delta_preserves_whitespace_and_final_is_not_callback(self):
        values = [event("Hello", partial=True), event(" ", partial=True),
                  event("world", partial=True), event("Hello world.")]
        original = copy.deepcopy(values)
        stream = TrackedStream(values)
        result = await self.consume(stream, min_partials=2)
        self.assertEqual(self.previews, ["Hello", "Hello ", "Hello world"])
        self.assertEqual((result.text, result.event_count, result.partial_count),
                         ("Hello world.", 4, 2))
        self.assertEqual(stream.closed, 1)
        self.assertEqual(values, original)

    async def test_snapshot_replaces_and_can_clear_preview(self):
        result = await self.consume(TrackedStream([
            event("ab", partial=True), event("", partial=True),
            event("corrected", partial=True), event("Corrected final."),
        ]), preview_mode="snapshot", min_partials=2)
        self.assertEqual(self.previews, ["ab", "", "corrected"])
        self.assertEqual(result.text, "Corrected final.")

    async def test_candidate_waits_for_exhaustion_and_accepts_metadata_only_tail(self):
        reached_tail, release = asyncio.Event(), asyncio.Event()
        async def source():
            yield event()
            reached_tail.set()
            await release.wait()
            yield event("", content=None, finishReason=None)
        task = asyncio.create_task(self.consume(source()))
        await reached_tail.wait()
        self.assertFalse(task.done())
        self.assertEqual(self.previews, [])
        release.set()
        result = await task
        self.assertEqual(result.event_count, 2)

    async def test_thought_tool_and_other_author_text_are_not_answers(self):
        values = [
            event("", content={"role": "model", "parts": [{"text": "private", "thought": True}]}),
            event("", content={"role": "model", "parts": [
                {"text": "tool narration"}, {"functionCall": {"id": "c", "name": "lookup"}},
            ]}),
            event("other agent", author="helper"),
            event("valid"),
        ]
        result = await self.consume(TrackedStream(values))
        self.assertEqual(result.text, "valid")
        self.assertEqual(self.previews, [])
        await self.reject(values[:3], "missing_completion")

    async def test_thought_only_partial_and_metadata_do_not_clear_snapshot_preview(self):
        await self.consume(TrackedStream([
            event("visible", partial=True),
            event("", partial=True, content={"role": "model", "parts": [
                {"text": "private thought", "thought": True},
            ]}),
            event("", partial=True, content=None),
            event("final"),
        ]), preview_mode="snapshot", min_partials=1)
        self.assertEqual(self.previews, ["visible"])

    async def test_global_failures_reject_even_from_another_author(self):
        cases = (
            ({"errorCode": "MODEL_SECRET"}, "stream_error"),
            ({"error_message": "private error"}, "stream_error"),
            ({"error": {"detail": "private"}}, "stream_error"),
            ({"finishReason": "MAX_TOKENS"}, "unaccepted_finish"),
            ({"interrupted": True}, "interrupted"),
        )
        for fields, code in cases:
            with self.subTest(fields=fields):
                await self.reject([event(author="helper", **fields)], code)

    async def test_late_error_text_tool_or_second_answer_invalidates_candidate(self):
        tails = [event(error_code="private"), event("second"),
                 event(" ", partial=True), event("helper continuation", author="helper"),
                 event("", content={"role": "user", "parts": [
                     {"function_response": {"id": "late", "name": "lookup", "response": {}}},
                 ]})]
        for tail in tails:
            with self.subTest(tail=tail):
                await self.reject([event(), tail])

    async def test_missing_completion_and_partial_evidence_are_separate(self):
        for values in ([], [event("", finishReason="STOP")],
                       [event(finishReason=None)], [event("preview", partial=True)]):
            await self.reject(values, "missing_completion")
        result = await self.consume(TrackedStream([event()]))
        self.assertEqual(result.partial_count, 0)
        await self.reject([event()], "missing_completion", min_partials=1)

    async def test_tool_payload_families_never_display_narration_or_finish_an_answer(self):
        for aliases in (("function_call", "functionCall"),
                        ("function_response", "functionResponse"),
                        ("executable_code", "executableCode"),
                        ("code_execution_result", "codeExecutionResult"),
                        ("tool_call", "toolCall"),
                        ("tool_response", "toolResponse")):
            for field in aliases:
                with self.subTest(field=field):
                    payload = {field: {"synthetic": "tool payload"}}
                    tool_event = event("", partial=True, content={
                        "role": "model", "parts": [{"text": "private tool narration"}, payload],
                    })
                    result = await self.consume(TrackedStream([tool_event, event("final")]))
                    self.assertEqual(result.text, "final")
                    self.assertEqual(self.previews, [])
                    tool_event["partial"] = False
                    tool_event["finishReason"] = "STOP"
                    await self.reject([tool_event], "missing_completion")
                    await self.reject([event(), tool_event], "activity_after_answer")
                    malformed = event(content={"role": "model", "parts": [{field: "bad"}]})
                    await self.reject([malformed], "invalid_event")

    async def test_nontext_payloads_and_unknown_part_fields_fail_closed(self):
        for field in ("inline_data", "inlineData", "file_data", "fileData",
                      "video_metadata", "videoMetadata", "media_resolution", "mediaResolution",
                      "audio_transcription", "audioTranscription", "part_metadata", "partMetadata",
                      "futurePayload"):
            with self.subTest(field=field):
                value = event(content={"role": "model", "parts": [
                    {"text": "incomplete narration"}, {field: {"synthetic": "data"}},
                ]})
                await self.reject([value], "unsupported_content")
                await self.reject([event(), value], "unsupported_content")
        result = await self.consume(TrackedStream([event(content={"role": "model", "parts": [
            {"text": "complete", "inlineData": None, "thoughtSignature": "opaque"},
        ]})]))
        self.assertEqual(result.text, "complete")
        for part in ({"thoughtSignature": {}},
                     {"thought_signature": "a", "thoughtSignature": "b"},
                     {"executable_code": {"code": "a"}, "executableCode": {"code": "b"}}):
            await self.reject([event(content={"role": "model", "parts": [part]})], "invalid_event")

    async def test_invocation_is_required_exact_and_aliases_must_agree(self):
        for identity in (None, "stale", 123, True):
            await self.reject([event(invocationId=identity)], "invocation_mismatch")
        await self.reject([event(invocation_id="other")], "invalid_event")
        await self.reject([event(finish_reason="MAX_TOKENS")], "invalid_event")
        await self.reject([event(error_code="different", errorCode="error")], "invalid_event")
        result = await self.consume(TrackedStream([event(
            invocation_id="synthetic-invocation", finish_reason="STOP")]))
        self.assertEqual(result.text, "complete")

    async def test_malformed_protocol_types_and_plain_json_are_rejected(self):
        cases = [
            event(partial=1), event(interrupted="false"), event(author=None),
            event(finishReason=1), event(content=[]),
            event(content={"role": 1, "parts": []}),
            event(content={"role": "model", "parts": {}}),
            event(content={"role": "model", "parts": [None]}),
            event(content={"role": "model", "parts": [{"text": 17}]}),
            event(content={"role": "model", "parts": [{"thought": "false"}]}),
            event(content={"role": "model", "parts": [{"functionCall": "call"}]}),
            event(metadata={1: "integer key"}), event(metadata=("tuple",)),
            event(metadata=float("nan")), event("\ud800"), [event()],
        ]
        cyclic = event()
        cyclic["cycle"] = cyclic
        cases.append(cyclic)
        for index, value in enumerate(cases):
            with self.subTest(index=index):
                await self.reject([value])

    async def test_event_count_and_utf8_limits_are_inclusive(self):
        value = event("é🙂")
        byte_count = compact_size(value)
        limits = self.asset.StreamLimits(max_events=1, max_event_bytes=byte_count,
                                        max_total_bytes=byte_count, max_visible_bytes=6)
        self.assertEqual((await self.consume(TrackedStream([value]), limits=limits)).text, "é🙂")
        await self.reject([value], "event_bytes_limit", limits=replace(limits, max_event_bytes=byte_count-1))
        await self.reject([value], "event_bytes_limit", limits=replace(limits, max_total_bytes=byte_count-1))
        await self.reject([value], "visible_bytes_limit", limits=replace(limits, max_visible_bytes=5))
        await self.reject([event("p", partial=True), value], "event_limit", limits=limits)

    async def test_total_and_visible_bounds_include_previews_and_snapshots(self):
        values = [event("é", partial=True), event("éé", partial=True), event("éé")]
        limits = self.asset.StreamLimits(max_visible_bytes=10,
                                        max_total_bytes=sum(map(compact_size, values)))
        await self.consume(TrackedStream(values), limits=limits, preview_mode="snapshot")
        await self.reject(values, "visible_bytes_limit", limits=replace(limits, max_visible_bytes=9), preview_mode="snapshot")
        await self.reject(values, "event_bytes_limit", limits=replace(limits, max_total_bytes=limits.max_total_bytes-1))

    async def test_provider_and_callback_errors_are_fixed_without_exception_chains(self):
        sentinel = "DO_NOT_EXPOSE_PRIVATE_PROVIDER_TEXT"
        failure = await self.reject([RuntimeError(sentinel)], "stream_failed")
        self.assertNotIn(sentinel, "".join(traceback.format_exception(failure)))
        async def bad_preview(text):
            raise ValueError(sentinel)
        failure = await self.reject([event("p", partial=True)], "stream_failed", send_preview=bad_preview)
        self.assertNotIn(sentinel, "".join(traceback.format_exception(failure)))
        async def timeout_preview(text):
            raise TimeoutError(sentinel)
        await self.reject([event("p", partial=True)], "stream_failed", send_preview=timeout_preview)
        await self.reject([self.asset.StreamRejected(sentinel)], "stream_failed")

    async def test_stalled_iterator_deadline_closes_generator(self):
        closed = asyncio.Event()
        async def source():
            try:
                yield event("preview", partial=True)
                await asyncio.Event().wait()
            finally:
                closed.set()
        limits = self.asset.StreamLimits(overall_seconds=0.01)
        await self.reject(source(), "deadline_exceeded", limits=limits)
        self.assertTrue(closed.is_set())

    async def test_stalled_preview_is_inside_overall_deadline(self):
        async def stalled(text):
            await asyncio.Event().wait()
        await self.reject([event("p", partial=True)], "deadline_exceeded",
                          send_preview=stalled, limits=self.asset.StreamLimits(overall_seconds=0.01))

    async def test_suppressed_overall_timeout_still_rejects_late_answer(self):
        closed = asyncio.Event()
        async def source():
            try:
                try:
                    await asyncio.Event().wait()
                except asyncio.CancelledError:
                    pass
                yield event("late")
            finally:
                closed.set()
        await self.reject(source(), "deadline_exceeded",
                          limits=self.asset.StreamLimits(overall_seconds=0.01))
        self.assertTrue(closed.is_set())

    async def test_suppressed_preview_timeout_stops_before_next_pull(self):
        async def display(text):
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                pass
        stream = TrackedStream([event("p", partial=True), event("late")])
        await self.reject(stream, "deadline_exceeded", send_preview=display,
                          limits=self.asset.StreamLimits(overall_seconds=0.01))
        self.assertEqual(stream.pulls, 1)

    async def test_synchronous_iterator_cannot_starve_deadline_check(self):
        loop = asyncio.get_running_loop()
        for delayed_pull in (1, 2):
            with self.subTest(delayed_pull=delayed_pull):
                clock = [loop.time()]
                class FastStream(TrackedStream):
                    async def __anext__(self):
                        if self.pulls + 1 == delayed_pull:
                            clock[0] += 2
                        return await super().__anext__()
                stream = FastStream([event()])
                # No suspension lets asyncio's scheduled timeout callback run;
                # advance only the injected clock, including at final exhaustion.
                with patch.object(loop, "time", side_effect=lambda: clock[0]):
                    await self.reject(stream, "deadline_exceeded",
                                      limits=self.asset.StreamLimits(overall_seconds=1))

    async def test_iterator_acquisition_is_inside_overall_deadline(self):
        loop = asyncio.get_running_loop()
        clock = [loop.time()]
        class SlowAcquisition(TrackedStream):
            def __aiter__(self):
                clock[0] += 2
                return self
        stream = SlowAcquisition([event()])
        with patch.object(loop, "time", side_effect=lambda: clock[0]):
            await self.reject(stream, "deadline_exceeded",
                              limits=self.asset.StreamLimits(overall_seconds=1))
        self.assertEqual(stream.pulls, 0)

    async def test_caller_cancellation_propagates_and_closes_owned_iterator(self):
        waiting, closed = asyncio.Event(), asyncio.Event()
        async def source():
            try:
                waiting.set()
                await asyncio.Event().wait()
                yield event()
            finally:
                closed.set()
        task = asyncio.create_task(self.consume(source()))
        await waiting.wait()
        task.cancel("cancel-marker")
        with self.assertRaises(asyncio.CancelledError) as caught:
            await task
        self.assertEqual(caught.exception.args, ("cancel-marker",))
        self.assertTrue(closed.is_set())

    async def test_swallowed_caller_cancellation_cannot_return_success(self):
        waiting, closed = asyncio.Event(), asyncio.Event()
        async def source():
            try:
                waiting.set()
                try:
                    await asyncio.Event().wait()
                except asyncio.CancelledError:
                    pass
                yield event("must not be accepted")
            finally:
                closed.set()
        task = asyncio.create_task(self.consume(source()))
        await waiting.wait()
        task.cancel("swallowed-by-adapter")
        with self.assertRaises(asyncio.CancelledError) as caught:
            await task
        self.assertIn("stream_cancellation_was_suppressed", caught.exception.__notes__)
        self.assertTrue(closed.is_set())

    async def test_primary_failure_survives_cleanup_failure_safely(self):
        stream = TrackedStream([event(finishReason="MAX_TOKENS")],
                               close_error=RuntimeError("private cleanup error"))
        failure = await self.reject(stream, "unaccepted_finish")
        self.assertTrue(failure.cleanup_failed)
        self.assertNotIn("private", "".join(traceback.format_exception(failure)))
        stream = TrackedStream([event()], close_error=RuntimeError("private"))
        failure = await self.reject(stream, "cleanup_failed")
        self.assertTrue(failure.cleanup_failed)

    async def test_cancellation_identity_survives_cleanup_failure(self):
        cancellation = asyncio.CancelledError("original-cancellation")
        stream = TrackedStream([cancellation], close_error=RuntimeError("private"))
        with self.assertRaises(asyncio.CancelledError) as caught:
            await self.consume(stream)
        self.assertIs(caught.exception, cancellation)
        self.assertEqual(caught.exception.__notes__, ["stream_cleanup_failed"])
        self.assertEqual(stream.closed, 1)

    async def test_close_own_cancellation_does_not_replace_primary_failure(self):
        stream = TrackedStream([event(finishReason="MAX_TOKENS")],
                               close_error=asyncio.CancelledError("private close cancellation"))
        failure = await self.reject(stream, "unaccepted_finish")
        self.assertTrue(failure.cleanup_failed)
        self.assertNotIn("private", "".join(traceback.format_exception(failure)))
        stream = TrackedStream([event()], close_error=asyncio.CancelledError("private"))
        await self.reject(stream, "cleanup_failed")

    async def test_new_caller_cancellation_during_close_propagates(self):
        closing = asyncio.Event()
        class AwaitingClose(TrackedStream):
            async def aclose(self):
                self.closed += 1
                closing.set()
                await asyncio.Event().wait()
        stream = AwaitingClose([event(finishReason="MAX_TOKENS")])
        task = asyncio.create_task(self.consume(stream))
        await closing.wait()
        task.cancel("caller-during-close")
        with self.assertRaises(asyncio.CancelledError) as caught:
            await task
        self.assertEqual(caught.exception.args, ("caller-during-close",))
        self.assertEqual(caught.exception.__notes__, [
            "stream_cleanup_failed", "stream_rejected_before_cancellation",
        ])
        self.assertEqual(stream.closed, 1)

    async def test_original_cancellation_survives_close_own_cancellation(self):
        original = asyncio.CancelledError("original")
        stream = TrackedStream([original], close_error=asyncio.CancelledError("close-only"))
        with self.assertRaises(asyncio.CancelledError) as caught:
            await self.consume(stream)
        self.assertIs(caught.exception, original)
        self.assertEqual(caught.exception.__notes__, ["stream_cleanup_failed"])

    async def test_closure_has_its_own_cooperative_deadline(self):
        class SlowClose(TrackedStream):
            async def aclose(self):
                self.closed += 1
                await asyncio.Event().wait()
        stream = SlowClose([event()])
        failure = await self.reject(stream, "cleanup_failed",
                                    limits=self.asset.StreamLimits(close_seconds=0.01))
        self.assertTrue(failure.cleanup_failed)

    async def test_suppressed_closure_timeout_marks_cleanup_failed(self):
        class SuppressingClose(TrackedStream):
            async def aclose(self):
                self.closed += 1
                try:
                    await asyncio.Event().wait()
                except asyncio.CancelledError:
                    pass
        for values, code in (([event()], "cleanup_failed"),
                             ([event(finishReason="MAX_TOKENS")], "unaccepted_finish")):
            with self.subTest(code=code):
                failure = await self.reject(SuppressingClose(values), code,
                                            limits=self.asset.StreamLimits(close_seconds=0.01))
                self.assertTrue(failure.cleanup_failed)

    async def test_synchronous_closure_cannot_starve_its_deadline_check(self):
        loop = asyncio.get_running_loop()
        clock = [loop.time()]
        class FastClose(TrackedStream):
            async def aclose(self):
                self.closed += 1
                clock[0] += 2
        with patch.object(loop, "time", side_effect=lambda: clock[0]):
            failure = await self.reject(FastClose([event()]), "cleanup_failed",
                                        limits=self.asset.StreamLimits(close_seconds=1))
        self.assertTrue(failure.cleanup_failed)

    async def test_closure_lookup_is_inside_cleanup_deadline(self):
        loop = asyncio.get_running_loop()
        clock = [loop.time()]
        class SlowCloseLookup(TrackedStream):
            @property
            def aclose(self):
                clock[0] += 2
                return super().aclose
        stream = SlowCloseLookup([event()])
        with patch.object(loop, "time", side_effect=lambda: clock[0]):
            failure = await self.reject(stream, "cleanup_failed",
                                        limits=self.asset.StreamLimits(close_seconds=1))
        self.assertTrue(failure.cleanup_failed)

    async def test_swallowed_caller_cancellation_during_close_cannot_return_success(self):
        closing = asyncio.Event()
        class SuppressingClose(TrackedStream):
            async def aclose(self):
                self.closed += 1
                closing.set()
                try:
                    await asyncio.Event().wait()
                except asyncio.CancelledError:
                    pass
        stream = SuppressingClose([event()])
        task = asyncio.create_task(self.consume(stream))
        await closing.wait()
        task.cancel("swallowed-during-close")
        with self.assertRaises(asyncio.CancelledError) as caught:
            await task
        self.assertEqual(caught.exception.__notes__, [
            "stream_cancellation_was_suppressed", "stream_cleanup_failed",
        ])
        self.assertEqual(stream.closed, 1)

    async def test_configuration_rejects_coercions_and_nonfinite_deadlines(self):
        for values in ({"max_events": True}, {"max_event_bytes": 1.5},
                       {"max_total_bytes": 0}, {"max_visible_bytes": -1},
                       {"overall_seconds": float("inf")}, {"close_seconds": float("nan")},
                       {"close_seconds": True}, {"overall_seconds": 10**1000}):
            with self.assertRaises(self.asset.StreamRejected):
                self.asset.StreamLimits(**values)
        for options in ({"min_partials": True}, {"min_partials": -1},
                        {"preview_mode": "auto"}, {"invocation_id": ""},
                        {"answer_author": None}):
            stream = TrackedStream([event()])
            with self.assertRaises(self.asset.StreamRejected) as caught:
                await self.consume(stream, **options)
            self.assertEqual(str(caught.exception), "invalid_configuration")
            self.assertEqual(stream.pulls, 0)
            self.assertEqual(stream.closed, 0)

    async def test_real_adk_event_json_serialization_interoperability(self):
        try:
            installed = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; preserve target dependencies")
        if installed != "2.8.0":
            self.skipTest("Recorded JSON interoperability requires ADK 2.8.0")
        from google.adk.events import Event
        from google.genai import types
        values = [Event(
            author="answer", invocation_id="synthetic-invocation", partial=partial,
            content=types.Content(role="model", parts=[types.Part(text=text)]),
            finish_reason=None if partial else types.FinishReason.STOP,
        ).model_dump(mode="json", by_alias=alias, exclude_none=exclude)
            for partial, text, alias, exclude in (
                (True, "First ", True, True),
                (True, "preview", False, False),
                (False, "Accepted complete answer.", True, False),
            )]
        result = await self.consume(TrackedStream(values), min_partials=2)
        self.assertEqual(result.text, "Accepted complete answer.")
        self.assertEqual(self.previews, ["First ", "First preview"])

    async def test_real_adk_code_execution_parts_do_not_become_final_answers(self):
        try:
            installed = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; preserve target dependencies")
        if installed != "2.8.0":
            self.skipTest("Recorded code serialization requires ADK 2.8.0")
        from google.adk.events import Event
        from google.genai import types
        parts = [
            types.Part.from_executable_code(language="PYTHON", code="print(2)"),
            types.Part.from_code_execution_result(outcome="OUTCOME_OK", output="2"),
            types.Part(tool_call=types.ToolCall(id="synthetic-tool", args={"input": 2})),
            types.Part(tool_response=types.ToolResponse(id="synthetic-tool", response={"output": 2})),
        ]
        for tool_part in parts:
            for alias in (True, False):
                with self.subTest(part=tool_part, by_alias=alias):
                    sdk_event = Event(
                        author="answer", invocation_id="synthetic-invocation", partial=False,
                        finish_reason=types.FinishReason.STOP,
                        content=types.Content(role="model", parts=[
                            types.Part(text="About to calculate."), tool_part,
                        ]),
                    )
                    if tool_part.code_execution_result:
                        self.assertFalse(sdk_event.is_final_response())
                    value = sdk_event.model_dump(mode="json", by_alias=alias, exclude_none=False)
                    await self.reject([value], "missing_completion")
                    result = await self.consume(TrackedStream([value, event("Complete calculation.")]))
                    self.assertEqual(result.text, "Complete calculation.")
                    self.assertEqual(self.previews, [])
                    await self.reject([event(), value], "activity_after_answer")


if __name__ == "__main__":
    unittest.main()
