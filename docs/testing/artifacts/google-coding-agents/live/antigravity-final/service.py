import re
from uuid import uuid4

from provider import ProviderRejected


_OP_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_AMOUNT_RE = re.compile(r"^[0-9]+(?:\.[0-9]{1,2})?$")


def _parse_amount(amount: str) -> int:
    if not isinstance(amount, str):
        raise ValueError("Amount must be a string")
    if len(amount) == 0 or len(amount) > 32:
        raise ValueError("Amount length must be between 1 and 32 characters")
    if not _AMOUNT_RE.fullmatch(amount):
        raise ValueError(f"Invalid amount format: {amount!r}")

    if "." in amount:
        dollars_str, cents_str = amount.split(".", 1)
        if len(cents_str) == 1:
            cents_minor = int(cents_str) * 10
        else:
            cents_minor = int(cents_str)
        amount_minor = int(dollars_str) * 100 + cents_minor
    else:
        amount_minor = int(amount) * 100

    if not (1 <= amount_minor <= 1_000_000):
        raise ValueError(
            f"Amount minor units {amount_minor} out of range [1, 1000000]"
        )
    return amount_minor


def _validate_operation_id(operation_id: str) -> None:
    if not isinstance(operation_id, str):
        raise ValueError("operation_id must be a string")
    if not _OP_ID_RE.fullmatch(operation_id):
        raise ValueError(f"Invalid operation_id: {operation_id!r}")


class RefundService:
    def __init__(self, provider):
        self.provider = provider
        self.operations = {}

    def refund(self, operation_id, amount, *, confirmed=True):
        _validate_operation_id(operation_id)
        amount_minor = _parse_amount(amount)

        if operation_id in self.operations:
            record = self.operations[operation_id]
            if record["amount_minor"] != amount_minor:
                raise ValueError(
                    f"Changed amount for previously dispatched operation: {operation_id!r}"
                )
            return dict(record["result"])

        if not confirmed:
            return {
                "status": "cancelled",
                "operation_id": operation_id,
                "amount_minor": amount_minor,
                "refund_id": None,
            }

        replay_key = str(uuid4())
        try:
            receipt = self.provider.issue_refund(
                operation_id, amount_minor, replay_key=replay_key
            )
            result = {
                "status": "applied",
                "operation_id": operation_id,
                "amount_minor": amount_minor,
                "refund_id": receipt["refund_id"],
            }
        except TimeoutError:
            try:
                receipt = self.provider.issue_refund(
                    operation_id, amount_minor, replay_key=replay_key
                )
                result = {
                    "status": "applied",
                    "operation_id": operation_id,
                    "amount_minor": amount_minor,
                    "refund_id": receipt["refund_id"],
                }
            except TimeoutError:
                result = {
                    "status": "unknown",
                    "operation_id": operation_id,
                    "amount_minor": amount_minor,
                    "refund_id": None,
                }
            except ProviderRejected:
                result = {
                    "status": "unknown",
                    "operation_id": operation_id,
                    "amount_minor": amount_minor,
                    "refund_id": None,
                }
        except ProviderRejected:
            result = {
                "status": "rejected",
                "operation_id": operation_id,
                "amount_minor": amount_minor,
                "refund_id": None,
            }

        self.operations[operation_id] = {
            "amount_minor": amount_minor,
            "result": result,
        }
        return dict(result)

