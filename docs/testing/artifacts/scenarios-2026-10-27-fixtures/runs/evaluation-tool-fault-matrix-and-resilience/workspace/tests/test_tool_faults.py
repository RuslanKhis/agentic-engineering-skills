"""Faults behind the real tool bodies: the transport times out, or returns empty, garbage or errors.

Unlike Environment Simulation (which short-circuits before the tool runs), these drive the real
tools.py / flight_api.py code. A tool must never raise into the agent and must never report
"booked" or "ok" for a response it could not validate.

Tests marked `known_defect` fail on the current code (read from tools.py and flight_api.py; not
yet run, see the report). expectedFailure keeps the default run green while recording the gap; when
a defect is fixed the test reports an unexpected success, which is the cue to remove the marker.
"""
import unittest

from travel_agent import tools
from travel_agent.flight_api import FlightApi
from tests.flight_double import FlightDouble, MailerDouble

known_defect = unittest.expectedFailure


class RaisingTransport:
    """Like FlightDouble but a chosen call raises, optionally after committing the booking."""

    def __init__(self, exc, commit_first=False):
        self.inner = FlightDouble()
        self.exc = exc
        self.commit_first = commit_first

    def __call__(self, method, path, json):
        if self.commit_first:
            self.inner(method, path, json)   # the server stored it, the acknowledgement is lost
        raise self.exc


def fixed(status, body):
    return lambda method, path, json: (status, body)


class FaultyMailer:
    def send(self, to, body):
        raise TimeoutError("smtp timed out")


class SearchFaultTests(unittest.TestCase):
    def use(self, transport):
        tools.api = FlightApi(transport)
        tools.mailer = MailerDouble()

    def test_503_with_json_body_is_an_error_result(self):
        self.use(fixed(503, {"error": "Service Unavailable"}))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    def test_empty_result_is_ok_with_no_flights(self):
        self.use(fixed(200, {"flights": []}))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03"), {"status": "ok", "flights": []})

    @known_defect
    def test_timeout_is_an_error_result_not_an_exception(self):
        self.use(RaisingTransport(TimeoutError("read timed out")))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    @known_defect
    def test_connection_error_is_an_error_result(self):
        self.use(RaisingTransport(ConnectionError("reset")))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    @known_defect
    def test_html_error_page_is_an_error_result(self):
        self.use(fixed(502, "<html>Bad Gateway</html>"))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    @known_defect
    def test_200_with_missing_flights_key_is_an_error_result(self):
        self.use(fixed(200, {}))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    @known_defect
    def test_200_with_non_json_body_is_an_error_result(self):
        self.use(fixed(200, "OK"))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    @known_defect
    def test_200_with_wrong_flights_type_is_an_error_result(self):
        self.use(fixed(200, {"flights": "none"}))
        self.assertEqual(tools.search_flights("LHR", "CDG", "2026-11-03")["status"], "error")

    @known_defect
    def test_flight_without_id_is_not_offered(self):
        self.use(fixed(200, {"flights": [{"flight_id": None, "price_eur": "ZX-SENTINEL-7Q3"}]}))
        result = tools.search_flights("LHR", "CDG", "2026-11-03")
        self.assertTrue(result["status"] == "error" or result["flights"] == [])


class BookFaultTests(unittest.TestCase):
    def use(self, transport):
        tools.api = FlightApi(transport)
        tools.mailer = MailerDouble()

    def test_503_is_an_error_result(self):
        self.use(fixed(503, {"error": "Service Unavailable"}))
        self.assertEqual(tools.book_flight("AF1681", "Ana Ruiz", "k-1")["status"], "error")

    @known_defect
    def test_timeout_is_not_reported_as_booked_and_does_not_raise(self):
        self.use(RaisingTransport(TimeoutError("read timed out")))
        self.assertNotEqual(tools.book_flight("AF1681", "Ana Ruiz", "k-1")["status"], "booked")

    @known_defect
    def test_201_without_booking_id_is_not_booked(self):
        self.use(fixed(201, {}))
        self.assertNotEqual(tools.book_flight("AF1681", "Ana Ruiz", "k-1")["status"], "booked")

    @known_defect
    def test_201_with_empty_booking_id_is_not_booked(self):
        self.use(fixed(201, {"booking_id": None}))
        self.assertNotEqual(tools.book_flight("AF1681", "Ana Ruiz", "k-1")["status"], "booked")

    @known_defect
    def test_html_error_page_is_an_error_result(self):
        self.use(fixed(500, "<html>boom</html>"))
        self.assertEqual(tools.book_flight("AF1681", "Ana Ruiz", "k-1")["status"], "error")

    @known_defect
    def test_lost_acknowledgement_is_reported_as_unknown_not_booked(self):
        """The server stored the booking, the reply timed out. The tool must not raise or say "booked",
        and a retry with the same key must find the one stored booking, not make a second."""
        transport = RaisingTransport(TimeoutError("read timed out"), commit_first=True)
        self.use(transport)
        first = tools.book_flight("AF1681", "Ana Ruiz", "k-1")
        self.assertNotEqual(first["status"], "booked")
        self.assertEqual(len(transport.inner.bookings), 1)
        self.use(transport.inner)
        retry = tools.book_flight("AF1681", "Ana Ruiz", "k-1")
        self.assertEqual(retry["status"], "booked")
        self.assertEqual(len(transport.inner.bookings), 1)


class ConfirmationFaultTests(unittest.TestCase):
    @known_defect
    def test_mailer_timeout_is_an_error_result_not_an_exception(self):
        tools.api = FlightApi(FlightDouble())
        tools.mailer = FaultyMailer()
        self.assertEqual(tools.send_confirmation("BK-0001", "ana@example.com")["status"], "error")


if __name__ == "__main__":
    unittest.main()
