"""Tools for the invoice hold agent (fixture: the payments ledger is not reachable here)."""


def find_paid_invoice(invoice_number: str) -> dict:
    """Look up an earlier payment for this exact invoice number.

    Returns {"payment_id": "<id>"} when one exists, or {"payment_id": None}.
    """
    raise NotImplementedError("the payments ledger is not available in this workspace")
