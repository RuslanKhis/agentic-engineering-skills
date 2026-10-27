import unittest
from unittest import mock

from app import booking, documents


class Ctx:
    def __init__(self, tenant_id):
        self.state = {"tenant_id": tenant_id}


class FakeIndex:
    def __init__(self, hits):
        self.hits = hits

    def query(self, text, top_k):
        return self.hits[:top_k]


class DocumentTests(unittest.TestCase):
    def test_only_the_sessions_tenant_chunks_are_returned(self):
        documents.set_index(FakeIndex([
            {"doc_id": "p1", "title": "Acme travel policy", "text": "Economy under 6 h", "tenant_id": "acme"},
            {"doc_id": "p2", "title": "Globex travel policy", "text": "Business always", "tenant_id": "globex"},
        ]))
        result = documents.search_documents("flight class", Ctx("acme"))
        self.assertEqual([c["doc_id"] for c in result["chunks"]], ["p1"])


class BookingTests(unittest.TestCase):
    def test_change_returns_confirmation(self):
        booking.set_sender(lambda payload: (200, {"confirmation": "C-77"}))
        result = booking.change_booking("TW-5HQ2KX", {"return_date": "2026-11-14"}, Ctx("acme"))
        self.assertEqual(result, {"status": "changed", "confirmation": "C-77"})

    def test_timeout_is_retried(self):
        calls = []

        def send(payload):
            calls.append(dict(payload))
            if len(calls) == 1:
                raise TimeoutError()
            return 200, {"confirmation": "C-78"}

        booking.set_sender(send)
        with mock.patch.object(booking.time, "sleep"):
            result = booking.change_booking("TW-5HQ2KX", {"seat": "14C"}, Ctx("acme"))
        self.assertEqual(result["status"], "changed")
        self.assertEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
