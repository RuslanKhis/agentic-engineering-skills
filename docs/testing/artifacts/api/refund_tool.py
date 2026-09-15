from provider import PayloadMismatch, PermanentRejection, ReplyLost, Unavailable


def refund(provider, operation_id, amount_cents, approved, max_attempts=3):
    """Replay one approved operation within a per-invocation attempt budget.

    The provider owns payload binding and deduplication. Upstream must retain
    the operation ID and original amount for recovery across invocations.
    Synchronous calls have no wall-clock deadline; caller cancellation escapes.
    """
    if approved is False:
        return {"status": "cancelled", "message": "Refund cancelled; no provider call made"}
    if approved is not True:
        return {"status": "rejected", "message": "Approval must be boolean True"}
    if not isinstance(operation_id, str) or not operation_id:
        return {"status": "rejected", "message": "operation_id must be a non-empty string"}
    if (
        not isinstance(amount_cents, int)
        or isinstance(amount_cents, bool)
        or amount_cents <= 0
    ):
        return {"status": "rejected", "message": "amount_cents must be a positive integer"}
    if (
        not isinstance(max_attempts, int)
        or isinstance(max_attempts, bool)
        or max_attempts <= 0
    ):
        return {"status": "rejected", "message": "max_attempts must be a positive integer"}

    uncertain = False
    error_type = None
    for attempt in range(1, max_attempts + 1):
        try:
            # Never derive this key from the amount: changed payloads must still
            # reach the provider's binding for the original logical operation.
            receipt = provider.refund(
                amount_cents=amount_cents, idempotency_key=operation_id
            )
        except ReplyLost:
            uncertain = True
        except Unavailable:
            pass
        except (PermanentRejection, PayloadMismatch) as error:
            error_type = type(error).__name__
            if not uncertain:
                return {
                    "status": "rejected",
                    "message": "Provider rejected this request",
                    "attempts": attempt,
                    "error_type": error_type,
                }
            # Rejection of this attempt cannot resolve an earlier lost reply.
            break
        except Exception as error:
            # An undocumented error has no replay or non-application guarantee.
            # Keep diagnostics, stop immediately, and do not swallow BaseException.
            uncertain = True
            error_type = type(error).__name__
            break
        else:
            return {
                "status": "succeeded",
                "message": "Refund complete",
                "receipt": receipt,
                "attempts": attempt,
            }

    if uncertain:
        result = {
            "status": "unknown",
            "message": (
                "Refund outcome is unknown. Recover using the same operation_id "
                "and original amount; do not create a new operation."
            ),
            "operation_id": operation_id,
            "attempts": attempt,
        }
        if error_type is not None:
            result["error_type"] = error_type
        return result
    return {
        "status": "rejected",
        "message": "Provider unavailable; attempt budget exhausted",
        "attempts": attempt,
    }
