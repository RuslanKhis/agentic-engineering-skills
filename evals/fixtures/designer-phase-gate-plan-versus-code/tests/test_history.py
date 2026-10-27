import unittest

from tests.fakes import FakeToolContext, configure_fakes
from app.tools.drive import save_transcript_to_drive


class TranscriptTests(unittest.TestCase):
    def setUp(self):
        self.store, _, _ = configure_fakes()
        self.store.add_conversation("cv-1", "cust-ana", "2026-10-20T10:00:00", "Hi, where is HO-10518?")

    def test_save_without_drive_connection_asks_for_consent(self):
        self.assertEqual(save_transcript_to_drive("cv-1", FakeToolContext("cust-ana"))["status"], "needs_consent")

    def test_another_customers_conversation_is_not_found(self):
        self.assertEqual(save_transcript_to_drive("cv-1", FakeToolContext("cust-ben"))["status"], "not_found")


if __name__ == "__main__":
    unittest.main()
