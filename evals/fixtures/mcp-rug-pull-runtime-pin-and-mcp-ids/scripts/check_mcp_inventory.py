"""CI: list Ledgerline's tools and fail when they differ from mcp/ledgerline.tools.json."""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.inventory import diff_inventory  # noqa: E402

RECORDED = Path(__file__).resolve().parents[1] / "mcp" / "ledgerline.tools.json"


async def list_tools(url: str) -> list[dict]:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    headers = {"Authorization": f"Bearer {os.environ['LEDGERLINE_TOKEN']}"}
    async with streamablehttp_client(url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return [t.model_dump(exclude_none=True) for t in (await session.list_tools()).tools]


def main() -> int:
    recorded = json.loads(RECORDED.read_text())
    listed = [t for t in asyncio.run(list_tools(recorded["server"])) if t["name"] in {"search_filings", "get_filing"}]
    problems = diff_inventory(recorded, listed)
    print("\n".join(problems) or "inventory unchanged")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
