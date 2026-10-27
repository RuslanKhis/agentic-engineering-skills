"""In-memory flight API and mailer for tests; records every call."""


class FlightDouble:
    def __init__(self):
        self.calls = []
        self.bookings = {}

    def __call__(self, method, path, json):
        self.calls.append((method, path, dict(json)))
        if path == "/flights":
            return 200, {"flights": [{"flight_id": "BA0303", "departs": "08:10", "arrives": "10:25", "price_eur": 182},
                                     {"flight_id": "AF1681", "departs": "12:40", "arrives": "15:05", "price_eur": 149}]}
        key = json["idempotency_key"]
        if key not in self.bookings:
            self.bookings[key] = {"booking_id": f"BK-{len(self.bookings) + 1:04d}", **json}
        return 201, self.bookings[key]


class MailerDouble:
    def __init__(self):
        self.sent = []

    def send(self, to, body):
        self.sent.append((to, body))
