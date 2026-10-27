"""Stream relay tests (C3). Scripted event source; duck-typed events, not ADK Events."""
import json
import unittest
from types import SimpleNamespace

from app import stream


def ev(text, partial):
    return SimpleNamespace(partial=partial, content=SimpleNamespace(parts=[SimpleNamespace(text=text)]))


async def scripted(*events):
    for e in events:
        yield e


async def collect(source):
    return [frame async for frame in stream.relay(source, "s1")]


def names(frames):
    return [f.split("\n", 1)[0].removeprefix("event: ") for f in frames]


class StreamTests(unittest.IsolatedAsyncioTestCase):
    async def test_completed_follows_the_text(self):  # A1
        frames = await collect(scripted(ev("Hal", True), ev("lo", True), ev("Hallo", False)))
        self.assertEqual(names(frames), ["session", "text", "text", "completed"])
        texts = [json.loads(f.split("data: ", 1)[1])["text"] for f in frames if f.startswith("event: text")]
        self.assertEqual("".join(texts), "Hallo")
        self.assertEqual(names(frames).count("completed"), 1)

    async def test_non_streaming_reply_is_sent_once(self):  # A1
        frames = await collect(scripted(ev("Hallo", False)))
        self.assertEqual(names(frames), ["session", "text", "completed"])


if __name__ == "__main__":
    unittest.main()
