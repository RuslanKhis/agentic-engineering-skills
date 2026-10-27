from dataclasses import dataclass
import unittest

from booking_agent import tools
from booking_agent.backend import Backend


@dataclass
class Ctx:
    user_id: str


class ToolTests(unittest.TestCase):
    def setUp(self):
        tools.backend = Backend()

    def test_book_then_cancel_frees_the_slot(self):
        booked = tools.book_slot("S-0901", Ctx("p-1"))
        tools.cancel_booking(booked["booking_id"], Ctx("p-1"))
        self.assertTrue(tools.backend.slots["S-0901"]["free"])

    def test_taken_slot_is_refused(self):
        self.assertEqual(tools.book_slot("S-0904", Ctx("p-1"))["status"], "error")

    def test_cannot_cancel_someone_elses_booking(self):
        booked = tools.book_slot("S-0902", Ctx("p-1"))
        self.assertEqual(tools.cancel_booking(booked["booking_id"], Ctx("p-2"))["status"], "error")


if __name__ == "__main__":
    unittest.main()
