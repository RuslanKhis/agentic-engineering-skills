"""LlamaFirewall Prompt Guard 2 adapter. Imports llamafirewall lazily; not exercised in this repo's tests.

Unverified against an installed llamafirewall (not available when this was written): the
`PromptGuardScanner` import path and its `.tokenizer` attribute follow the PurpleLlama source.
"""
from __future__ import annotations

import os
from pathlib import Path

from contracts.screen import ResultScreen

WEIGHTS_DIR = "meta-llama--Llama-Prompt-Guard-2-86M"


def load_prompt_guard_screen() -> ResultScreen:
    """Build the screen once at startup from weights already on disk; refuse to start without them.

    A missing directory would otherwise trigger a download and an interactive Hugging Face login.
    """
    hf_home = os.environ.get("HF_HOME")
    if not hf_home or not (Path(hf_home) / WEIGHTS_DIR).is_dir():
        raise RuntimeError(f"Prompt Guard 2 weights not found under $HF_HOME/{WEIGHTS_DIR}")
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from llamafirewall import ToolMessage
    from llamafirewall.scanners.promptguard_scanner import PromptGuardScanner

    scanner = PromptGuardScanner()
    return ResultScreen(scanner, scanner.tokenizer, make_message=lambda text: ToolMessage(content=text))
