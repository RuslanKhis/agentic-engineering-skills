from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UserScope:
    app_name: str
    user_id: str


class ProfileStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save_preferred_language(self, scope: UserScope, language: str, *, consent: bool) -> None:
        raise NotImplementedError

    def get_preferred_language(self, scope: UserScope) -> str | None:
        raise NotImplementedError

    def forget_preferred_language(self, scope: UserScope) -> None:
        raise NotImplementedError
