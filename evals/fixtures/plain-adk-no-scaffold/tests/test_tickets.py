import unittest

from app import services
from app.clients.helpdesk import HelpdeskClient
from app.clients.http import Response
from app.tools.tickets import list_open_tickets
from tests.fakes import FakeToolContext, FakeTransport, configure_fakes


class TicketToolTests(unittest.TestCase):
    def test_lists_open_tickets_for_the_signed_in_customer(self):
        configure_fakes()
        transport = FakeTransport([Response(200, {"tickets": [
            {"ticket_id": "T-88", "subject": "Zip broken", "opened_on": "2026-10-20", "state": "open"}]})])
        services.get().helpdesk = HelpdeskClient("https://helpdesk.test/api", transport)
        result = list_open_tickets(FakeToolContext("cust-ana"))
        self.assertEqual(result["tickets"][0]["ticket_id"], "T-88")
        self.assertIn("/customers/cust-ana/tickets", transport.requests[0]["url"])


if __name__ == "__main__":
    unittest.main()
