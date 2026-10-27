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


if __name__ == "__main__":
    unittest.main()
