"""Deliberately incomplete evaluation input; not a production template."""


async def execute_refund(store, provider, approval):
    if not approval["confirmed"]:
        return {"ok": False, "reason": "cancelled", "data": None}
    action = await store.current(approval["operation_id"])
    data = await provider.refund(action)
    return {"ok": True, "reason": None, "data": data}
