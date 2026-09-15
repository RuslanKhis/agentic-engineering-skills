from collections import deque

class Unavailable(Exception): pass
class ReplyLost(Exception): pass
class PermanentRejection(Exception): pass
class PayloadMismatch(Exception): pass

class MockProvider:
    def __init__(self, actions=()):
        self.actions = deque(actions)
        self.calls = []
        self.payloads = {}
        self.receipts = {}
        self.effects = 0

    def refund(self, *, amount_cents, idempotency_key):
        self.calls.append((idempotency_key, amount_cents))
        if idempotency_key in self.payloads and self.payloads[idempotency_key] != amount_cents:
            raise PayloadMismatch("Operation already bound to another amount")
        self.payloads[idempotency_key] = amount_cents
        action = self.actions.popleft() if self.actions else "success"
        if action == "unavailable":
            raise Unavailable("Temporarily unavailable before committing")
        if action == "permanent":
            raise PermanentRejection("Request rejected before this attempt commits")
        if idempotency_key not in self.receipts:
            self.effects += 1
            self.receipts[idempotency_key] = {"refund_id": f"refund-{self.effects}", "amount_cents": amount_cents}
        if action == "commit_then_lose":
            raise ReplyLost("Reply lost; operation may have committed")
        return dict(self.receipts[idempotency_key])
