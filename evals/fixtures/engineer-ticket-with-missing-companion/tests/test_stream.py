"""The /api/chat stream ends with completed, or failed after an error (G02/A1, C2).

Drives the route with a scripted event source in place of the Runner; needs fastapi and
google-adk installed, and skips without them.
"""
import importlib.util
import unittest

HAVE_STACK = all(importlib.util.find_spec(m) is not None for m in ("fastapi", "google.adk"))


class ScriptedRunner:
    def __init__(self, texts, fail_after=None):
        self.texts, self.fail_after = texts, fail_after

    async def run_async(self, **_):
        from google.genai import types

        for i, text in enumerate(self.texts):
            if self.fail_after is not None and i == self.fail_after:
                raise RuntimeError("provider error")
            yield type("Event", (), {"content": types.Content(role="model", parts=[types.Part(text=text)])})()


@unittest.skipUnless(HAVE_STACK, "fastapi and google-adk are not installed")
class StreamEndsTests(unittest.IsolatedAsyncioTestCase):
    async def _events(self, runner):
        from fastapi.testclient import TestClient

        from app import server
        from app.auth import Principal

        server.runner = runner
        server.app.dependency_overrides[server.current_principal] = lambda: Principal("u1", "u1@example.com")
        session = await server.sessions.create_session(app_name="docs", user_id="u1")
        client = TestClient(server.app)
        resp = client.post("/api/chat", json={"session_id": session.id, "message": "hi"})
        return [line.split(": ", 1)[1] for line in resp.text.splitlines() if line.startswith("event: ")]

    async def test_completed_after_text(self):
        events = await self._events(ScriptedRunner(["Hello", " there"]))
        self.assertEqual(events, ["text", "text", "completed"])

    async def test_failed_after_partial_text(self):
        events = await self._events(ScriptedRunner(["Hello", " there"], fail_after=1))
        self.assertEqual(events, ["text", "failed"])


if __name__ == "__main__":
    unittest.main()
