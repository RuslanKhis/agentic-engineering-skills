import unittest
from types import SimpleNamespace

from homeline import tools


class BookingToolTests(unittest.TestCase):
    def setUp(self):
        tools.BOOKINGS.visits.clear()

    def test_book_visit(self):
        result = tools.book_visit("plumber", "12 Alder Close", "2026-11-03", SimpleNamespace(user_id="u-1"))
        self.assertEqual(result["status"], "booked")

    def test_unknown_trade(self):
        result = tools.book_visit("roofer", "12 Alder Close", "2026-11-03", SimpleNamespace(user_id="u-1"))
        self.assertEqual(result["status"], "error")

    def test_visits_are_per_customer(self):
        tools.book_visit("plumber", "12 Alder Close", "2026-11-03", SimpleNamespace(user_id="u-1"))
        self.assertEqual(tools.my_visits(SimpleNamespace(user_id="u-2"))["visits"], [])


if __name__ == "__main__":
    unittest.main()
