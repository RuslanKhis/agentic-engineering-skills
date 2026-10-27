import unittest

from travel_agent import tools
from travel_agent.flight_api import FlightApi
from tests.flight_double import FlightDouble, MailerDouble


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.double = FlightDouble()
        tools.api = FlightApi(self.double)
        tools.mailer = MailerDouble()

    def test_search_returns_flights(self):
        self.assertEqual(len(tools.search_flights("LHR", "CDG", "2026-11-03")["flights"]), 2)

    def test_retried_booking_with_same_key_books_once(self):
        a = tools.book_flight("AF1681", "Ana Ruiz", "k-1")
        b = tools.book_flight("AF1681", "Ana Ruiz", "k-1")
        self.assertEqual(a["booking_id"], b["booking_id"])
        self.assertEqual(len(self.double.bookings), 1)


if __name__ == "__main__":
    unittest.main()
