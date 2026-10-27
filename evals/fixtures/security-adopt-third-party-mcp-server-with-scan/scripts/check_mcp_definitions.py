"""CI: start the pinned Freightline server, list its tools, fail on any change from the manifest."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.mcp_pin import diff_manifest  # noqa: E402

MANIFEST = Path(__file__).resolve().parents[1] / "mcp" / "freightline-shipping.tools.json"


async def list_tools() -> list[dict]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    recorded = json.loads(MANIFEST.read_text())
    params = StdioServerParameters(command="npx", args=["-y", f"{recorded['server']}@{recorded['version']}"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            return [t.model_dump(exclude_none=True) for t in result.tools]


def main() -> int:
    problems = diff_manifest(json.loads(MANIFEST.read_text()), asyncio.run(list_tools()))
    for line in problems:
        print(line)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
