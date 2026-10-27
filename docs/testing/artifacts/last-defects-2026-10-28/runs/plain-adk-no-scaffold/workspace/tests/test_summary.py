import threading
import unittest
from unittest import mock

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app import summary


async def _run_readers(user_id="cust-ana"):
    """Run only the parallel reader stage (no model call) and return the final session state."""
    sessions = InMemorySessionService()
    readers = summary.build_summary_flow().sub_agents[0]
    runner = Runner(app_name="summary", agent=readers, session_service=sessions)
    session = await sessions.create_session(app_name="summary", user_id=user_id)
    async for _ in runner.run_async(user_id=user_id, session_id=session.id,
                                    new_message=types.Content(role="user", parts=[types.Part(text="x")])):
        pass
    return (await sessions.get_session(app_name="summary", user_id=user_id, session_id=session.id)).state


class ParallelReadersTests(unittest.IsolatedAsyncioTestCase):
    async def test_readers_overlap_and_both_results_are_saved(self):
        # Each tool waits for the other; sequential execution would time out the barrier.
        barrier = threading.Barrier(2, timeout=5)

        def orders(ctx):
            barrier.wait()
            return {"status": "ok", "orders": [{"order_id": "HO-1"}]}

        def tickets(ctx):
            barrier.wait()
            return {"status": "ok", "tickets": [{"ticket_id": "T-1"}]}

        with mock.patch.object(summary, "list_my_orders", orders), \
                mock.patch.object(summary, "list_open_tickets", tickets):
            state = await _run_readers()
        self.assertEqual(state["orders"], [{"order_id": "HO-1"}])
        self.assertEqual(state["tickets"], [{"ticket_id": "T-1"}])

    async def test_a_failing_reader_fails_the_run(self):
        def boom(ctx):
            raise RuntimeError("helpdesk down")

        ok = lambda ctx: {"status": "ok", "orders": []}  # noqa: E731
        with mock.patch.object(summary, "list_my_orders", ok), \
                mock.patch.object(summary, "list_open_tickets", boom):
            with self.assertRaises(BaseException):
                await _run_readers()


if __name__ == "__main__":
    unittest.main()
