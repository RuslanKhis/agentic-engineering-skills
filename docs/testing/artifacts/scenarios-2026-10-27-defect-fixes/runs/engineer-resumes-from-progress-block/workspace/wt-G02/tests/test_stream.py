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
        async def raising():
            yield {"text": "Hal"}
            raise RuntimeError("runner broke")

        states = []
        frames = asyncio.run(collect(relay(raising(), states.append)))
        self.assertTrue(frames[0].startswith("event: delta"))
        self.assertTrue(frames[-1].startswith("event: failed"))
        self.assertFalse(any(f.startswith("event: completed") for f in frames))
        self.assertEqual(states, ["failed"])

    def test_disconnect_stops_run_and_records_interrupted(self):
        closed = []

        async def source():
            try:
                yield {"text": "Hal"}
                yield {"text": "lo"}
            finally:
                closed.append(True)

        states = []

        async def disconnect_after_first_frame():
            gen = relay(source(), states.append)
            await gen.__anext__()
            await gen.aclose()  # what the server does when the client goes away

        asyncio.run(disconnect_after_first_frame())
        self.assertEqual(states, ["interrupted"])
        self.assertEqual(closed, [True])


if __name__ == "__main__":
    unittest.main()
