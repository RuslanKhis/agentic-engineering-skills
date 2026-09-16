"""Deterministic synthetic provider; never performs I/O."""


class ProviderRejected(Exception):
    pass


class SyntheticProvider:
    def __init__(self, outcomes=()):
        self.outcomes = list(outcomes)
        self.calls = []
        self.effects = []
        self.receipts = {}

    def issue_refund(self, operation_id, amount_minor, *, replay_key):
        payload = (operation_id, amount_minor)
        self.calls.append((operation_id, amount_minor, replay_key))
        outcome = self.outcomes.pop(0) if self.outcomes else "success"
        if outcome == "reject":
            raise ProviderRejected("synthetic terminal rejection")
        if outcome == "timeout_before_commit":
            raise TimeoutError("synthetic response unavailable")
        if replay_key in self.receipts:
            old_payload, receipt = self.receipts[replay_key]
            if old_payload != payload:
                raise ProviderRejected("synthetic replay payload conflict")
        else:
            receipt = {
                "status": "applied", "operation_id": operation_id,
                "amount_minor": amount_minor,
                "refund_id": f"refund-{len(self.effects) + 1}",
            }
            self.receipts[replay_key] = (payload, receipt)
            self.effects.append(payload)
        if outcome == "commit_then_timeout":
            raise TimeoutError("synthetic response lost after commit")
        return dict(receipt)
