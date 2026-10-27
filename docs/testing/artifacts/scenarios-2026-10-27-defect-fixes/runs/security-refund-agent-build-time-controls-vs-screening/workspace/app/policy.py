"""Refund policy limits. Enforced in the tool body and the operation store, not by the prompt."""
from __future__ import annotations

# EUR 150.00 per refund, as the instruction has always told the model. The aggregate bound
# (everything pending or succeeded on one order <= the order total) lives in OperationStore.reserve.
MAX_REFUND_CENTS = 15_000
