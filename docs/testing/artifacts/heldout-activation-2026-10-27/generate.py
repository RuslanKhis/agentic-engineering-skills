#!/usr/bin/env python3
"""Generate held-out activation requests from neutral briefs (27 October 2026).

Each brief goes to its own fresh, isolated ``claude -p`` session through the
repository's claude-cli backend (scripts/model_backends.py): an empty temporary
working directory, no tools, safe mode, no slash commands or skills, no MCP
servers, no setting sources (so no CLAUDE.md or user settings) and no saved
session. The session sees GENERATOR_SYSTEM and the prompt built from one brief,
nothing else: not the skill name, SKILL.md, any description, existing case or
the repository. Raw replies are written to raw/<short>.json beside this file.

    .venv/bin/python docs/testing/artifacts/heldout-activation-2026-10-27/generate.py [--only short,...] [--round N]
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from model_backends import BackendError, call_claude_cli, claude_cli_command  # noqa: E402

MODEL = "claude-opus-5-5"

GENERATOR_SYSTEM = (
    "You write realistic test requests that software developers type to an AI coding "
    "assistant. Answer with JSON only."
)

PROMPT = """\
The coding assistant is used by developers who build AI agents in Python with \
Google's Agent Development Kit, usually hosted on Google Cloud. Their requests may \
or may not mention that stack.

Here is one kind of help the assistant can give:

<brief>
{brief}
</brief>

Write three requests a developer might type to the assistant:
- two that need exactly this kind of help;
- one that sounds related but actually needs a different kind of help.

Write as real developers do: vary the tone (terse, chatty, frustrated, formal); make \
some vague and some full of detail that does not matter; mention their own project, \
code or deadline where natural. Do not reuse the wording of the brief. For the third \
request, say in plain words what kind of help it actually needs instead.

Answer with JSON only, in exactly this shape:
{{"requests": [
 {{"kind": "fits", "text": "..."}},
 {{"kind": "fits", "text": "..."}},
 {{"kind": "elsewhere", "text": "...", "needs_instead": "..."}}
]}}"""


def generate(entry: dict, round_no: int) -> dict:
    prompt = PROMPT.format(brief=entry["brief"])
    record = {"short": entry["short"], "round": round_no, "model": MODEL,
              "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "command": claude_cli_command(MODEL, GENERATOR_SYSTEM) + ["(prompt on stdin)"],
              "cwd": "fresh empty temporary directory (tempfile.TemporaryDirectory)",
              "system": GENERATOR_SYSTEM, "prompt": prompt}
    try:
        reply = call_claude_cli(prompt, GENERATOR_SYSTEM, MODEL, timeout=600)
        record.update(reply_text=reply.text, reply_model=reply.model, usage=reply.usage,
                      cost_usd=reply.cost_usd, duration_s=reply.duration_s)
    except BackendError as exc:
        record["error"] = str(exc)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="comma-separated short names")
    parser.add_argument("--round", type=int, default=1)
    args = parser.parse_args()
    briefs = json.loads((HERE / "briefs.json").read_text(encoding="utf-8"))["briefs"]
    if args.only:
        wanted = set(args.only.split(","))
        briefs = [b for b in briefs if b["short"] in wanted]
    (HERE / "raw").mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for record in pool.map(lambda b: generate(b, args.round), briefs):
            suffix = "" if args.round == 1 else f"-round{args.round}"
            path = HERE / "raw" / f"{record['short']}{suffix}.json"
            path.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(record["short"], "error: " + record["error"] if "error" in record else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
