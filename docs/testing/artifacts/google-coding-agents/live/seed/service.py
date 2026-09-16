"""Existing refund adapter. Keep its public API and improve its behavior."""
from uuid import uuid4

from provider import ProviderRejected


class RefundService:
    def __init__(self, provider):
        self.provider = provider
        self.operations = {}

    def refund(self, operation_id, amount, *, confirmed=True):
        amount_minor = round(float(amount) * 100)
        for _ in range(2):
            try:
                return self.provider.issue_refund(
                    operation_id, amount_minor, replay_key=str(uuid4())
                )
            except (TimeoutError, ProviderRejected):
                pass
        return {
            "status": "rejected", "operation_id": operation_id,
            "amount_minor": amount_minor, "refund_id": None,
        }
