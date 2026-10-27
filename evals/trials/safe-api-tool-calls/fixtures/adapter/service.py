"""Deliberately incomplete evaluation input; not a production template."""


class Gateway:
    def __init__(self, client):
        self.client = client

    async def lookup(self, reference):
        response = await self.client.get("/status", params={"reference": reference})
        return {"ok": True, "data": response.json(), "reason": None, "outcome": "read"}

    async def refund(self, reference, amount):
        for attempt in range(2):
            try:
                response = await self.client.post(
                    "/refunds", json={"reference": reference, "amount": amount}
                )
                return {"ok": True, "data": response.json(), "reason": None,
                        "outcome": "applied"}
            except Exception as error:
                if attempt == 1:
                    return {"ok": False, "data": None, "reason": str(error),
                            "outcome": "not_attempted"}
