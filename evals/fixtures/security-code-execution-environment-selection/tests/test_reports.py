import unittest
from unittest import mock

from app.tools import reports


class EmailReportTests(unittest.TestCase):
    def test_sends_one_message(self):
        with mock.patch("smtplib.SMTP") as smtp:
            result = reports.email_report("uw-lead@fjord.example", "Loss ratios", "Q3 up 4 %")
        self.assertEqual(result, {"status": "sent"})
        sent = smtp.return_value.__enter__.return_value.send_message.call_args[0][0]
        self.assertEqual(sent["To"], "uw-lead@fjord.example")


if __name__ == "__main__":
    unittest.main()
