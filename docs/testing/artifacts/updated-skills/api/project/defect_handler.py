"""Local transport-double handler whose source line holds a literal canary."""

import httpx


async def raising_handler(request: httpx.Request) -> httpx.Response:
    raise RuntimeError("PRIVATE_EXCEPTION_PAYLOAD_CANARY")
