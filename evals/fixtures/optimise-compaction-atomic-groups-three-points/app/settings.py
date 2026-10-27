"""Runtime settings read from the environment."""
from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    model_id: str = "gemini-3.5-flash"
    db_path: str = "support.db"
    database_url: str = "sqlite+aiosqlite:///sessions-dev.db"
    payments_base_url: str = "https://payments.example.invalid/v1"
    mail_base_url: str = "https://mail.example.invalid/api"
    iap_audience: str = ""
    max_refund_cents: int = 20_000

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model_id=os.environ.get("MODEL_ID", cls.model_id),
            db_path=os.environ.get("SUPPORT_DB_PATH", cls.db_path),
            database_url=os.environ.get("DATABASE_URL", cls.database_url),
            payments_base_url=os.environ.get("PAYMENTS_BASE_URL", cls.payments_base_url),
            mail_base_url=os.environ.get("MAIL_BASE_URL", cls.mail_base_url),
            iap_audience=os.environ.get("IAP_AUDIENCE", ""),
            max_refund_cents=int(os.environ.get("MAX_REFUND_CENTS", cls.max_refund_cents)),
        )
