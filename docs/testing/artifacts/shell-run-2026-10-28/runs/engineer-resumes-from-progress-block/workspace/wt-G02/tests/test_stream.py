import asyncio
import unittest

from app.stream import relay


async def scripted(*events):
    for event in events:
        yield event


async def collect(gen):
    return [frame async for frame in gen]


class StreamTests(unittest.TestCase):
    def test_completed_after_text(self):
        frames = asyncio.run(collect(relay(scripted({"text": "Hallo"}, {"text": " Ana"}))))
        self.assertTrue(frames[0].startswith("event: delta"))
        self.assertTrue(frames[-1].startswith("event: completed"))
        self.assertEqual(sum(f.startswith("event: completed") for f in frames), 1)

    def test_failed_after_partial_text_has_no_completed(self):
        async def broken():
            yield {"text": "Hal"}
            raise RuntimeError("model down")

        frames = asyncio.run(collect(relay(broken())))
        self.assertTrue(frames[0].startswith("event: delta"))
        self.assertTrue(frames[-1].startswith("event: failed"))
        self.assertFalse(any(f.startswith("event: completed") for f in frames))
        self.assertNotIn("model down", frames[-1])

    def test_disconnect_stops_run_and_records_interrupted(self):
        state = {"closed": False, "interrupted": 0}

        async def slow():
            try:
                yield {"text": "Hal"}
                await asyncio.sleep(60)
                yield {"text": "lo"}
            finally:
                state["closed"] = True

        async def client():
            gen = relay(slow(), on_interrupted=lambda: state.update(interrupted=state["interrupted"] + 1))
            self.assertTrue((await gen.__anext__()).startswith("event: delta"))
            task = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0.01)
            task.cancel()  # what the server does when the client disconnects
            with self.assertRaises(asyncio.CancelledError):
                await task

        asyncio.run(client())
        self.assertTrue(state["closed"])
        self.assertEqual(state["interrupted"], 1)


if __name__ == "__main__":
    unittest.main()
