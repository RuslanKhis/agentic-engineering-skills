import unittest

from app import stream


class ScriptedRun:
    """Stands in for the runner: yields scripted chunks, optionally raising after them."""

    def __init__(self, chunks, raises=None):
        self.chunks = chunks
        self.raises = raises
        self.closed = False

    def __aiter__(self):
        return self._run()

    async def _run(self):
        try:
            for chunk in self.chunks:
                yield chunk
            if self.raises:
                raise self.raises
        finally:
            self.closed = True


def connected():
    async def check():
        return False
    return check


def disconnects_after(n):
    calls = 0

    async def check():
        nonlocal calls
        calls += 1
        return calls > n
    return check


async def collect(source, is_disconnected):
    recorded = []
    frames = [f async for f in stream.relay(source._run(), is_disconnected, recorded.append)]
    return frames, recorded


class StreamTests(unittest.IsolatedAsyncioTestCase):
    async def test_finished_run_ends_with_completed_after_text(self):
        frames, recorded = await collect(ScriptedRun(["Hel", "lo"]), connected())
        self.assertEqual([f.split("\n")[0] for f in frames],
                         ["event: text", "event: text", "event: completed"])
        self.assertEqual(recorded, ["completed"])

    async def test_failure_after_partial_text_ends_with_failed_not_completed(self):
        run = ScriptedRun(["Hel"], raises=RuntimeError("provider down"))
        frames, recorded = await collect(run, connected())
        self.assertEqual([f.split("\n")[0] for f in frames], ["event: text", "event: failed"])
        self.assertEqual(recorded, ["failed"])

    async def test_client_disconnect_stops_the_run_and_records_interrupted(self):
        run = ScriptedRun(["a", "b", "c"])
        frames, recorded = await collect(run, disconnects_after(1))
        self.assertEqual([f.split("\n")[0] for f in frames], ["event: text"])
        self.assertEqual(recorded, ["interrupted"])
        self.assertTrue(run.closed)

    async def test_closing_the_response_records_interrupted(self):
        run = ScriptedRun(["a", "b"])
        recorded = []
        gen = stream.relay(run._run(), connected(), recorded.append)
        await gen.__anext__()
        await gen.aclose()
        self.assertEqual(recorded, ["interrupted"])
        self.assertTrue(run.closed)


if __name__ == "__main__":
    unittest.main()
