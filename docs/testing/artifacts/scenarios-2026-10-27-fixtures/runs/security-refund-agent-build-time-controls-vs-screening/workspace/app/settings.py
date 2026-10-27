"""Runtime settings read from the environment."""
from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    model_id: str = "gemini-3.5-flash"
    db_path: str = "support.db"
    payments_base_url: str = "https://payments.example.invalid/v1"
    mail_base_url: str = "https://mail.example.invalid/api"
    iap_audience: str = ""
    # Refund policy limits, enforced in code by app/operations.py (the instruction only mirrors them).
    max_refund_cents: int = 15_000
    max_customer_daily_cents: int = 30_000
    max_customer_daily_count: int = 3
    max_global_daily_cents: int = 2_000_000

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model_id=os.environ.get("MODEL_ID", cls.model_id),
            db_path=os.environ.get("SUPPORT_DB_PATH", cls.db_path),
            payments_base_url=os.environ.get("PAYMENTS_BASE_URL", cls.payments_base_url),
            mail_base_url=os.environ.get("MAIL_BASE_URL", cls.mail_base_url),
            iap_audience=os.environ.get("IAP_AUDIENCE", ""),
            max_refund_cents=int(os.environ.get("MAX_REFUND_CENTS", cls.max_refund_cents)),
            max_customer_daily_cents=int(os.environ.get("MAX_CUSTOMER_DAILY_CENTS", cls.max_customer_daily_cents)),
            max_customer_daily_count=int(os.environ.get("MAX_CUSTOMER_DAILY_COUNT", cls.max_customer_daily_count)),
            max_global_daily_cents=int(os.environ.get("MAX_GLOBAL_DAILY_CENTS", cls.max_global_daily_cents)),
        )

    def refund_limits(self) -> "RefundLimits":
        from app.operations import RefundLimits
        return RefundLimits(self.max_refund_cents, self.max_customer_daily_cents,
                            self.max_customer_daily_count, self.max_global_daily_cents)
