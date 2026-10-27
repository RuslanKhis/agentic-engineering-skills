"""Settings, from the environment with the defaults the team runs with."""
from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    provider_base_url: str = "https://gateway.example.invalid/v1"
    writer_model: str = "gemini-3.5-flash"
    review_model: str = "gemini-3.5-flash"
    temperature: float = 1.0
    max_output_tokens: int = 8192
    request_timeout_s: float = 120.0
    checkpoint_dir: str = "runs"
    # The store sits on a document database whose single-record limit is 1 MiB.
    checkpoint_limit_bytes: int = 1_048_576
    # Raised from 60,000 on 2026-10-09: major applications were being cut mid-document.
    max_source_chars: int = 700_000
    ledger_path: str = "campaign/ledger.json"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            provider_base_url=os.environ.get("PROVIDER_BASE_URL", cls.provider_base_url),
            writer_model=os.environ.get("WRITER_MODEL", cls.writer_model),
            review_model=os.environ.get("REVIEW_MODEL", cls.review_model),
            checkpoint_dir=os.environ.get("CHECKPOINT_DIR", cls.checkpoint_dir),
        )
