import unittest

try:
    import google.adk  # noqa: F401
    HAVE_ADK = True
except ImportError:
    HAVE_ADK = False


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class PreloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_in_memory_service_starts_empty(self):
        from google.adk.memory import InMemoryMemoryService

        service = InMemoryMemoryService()
        result = await service.search_memory(app_name="fieldline", user_id="eng-ravi", query="torque")
        self.assertEqual(result.memories, [])


if __name__ == "__main__":
    unittest.main()
