from uuid import uuid4

def refund(provider, operation_id, amount_cents, approved, max_attempts=3):
    """Create a refund using a provider client."""
    for attempt in range(max_attempts):
        try:
            receipt = provider.refund(amount_cents=amount_cents, idempotency_key=str(uuid4()))
            return {"status": "succeeded", "message": "Refund complete", "receipt": receipt}
        except Exception:
            continue
    return {"status": "rejected", "message": "Refund failed"}
