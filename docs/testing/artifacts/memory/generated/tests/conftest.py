import socket

import pytest

from profile_store import ProfileStore, UserScope


@pytest.fixture(autouse=True)
def offline_only(monkeypatch):
    """Guard before tests import ADK or construct agents."""
    def forbidden(*args, **kwargs):
        raise AssertionError("Network, credentials and Google clients are forbidden.")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket.socket, "connect_ex", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)

    import google.auth
    import google.genai

    monkeypatch.setattr(google.auth, "default", forbidden)
    monkeypatch.setattr(google.auth, "load_credentials_from_file", forbidden)
    monkeypatch.setattr(google.auth, "load_credentials_from_dict", forbidden)
    monkeypatch.setattr(google.genai, "Client", forbidden)


@pytest.fixture
def store(tmp_path):
    return ProfileStore(tmp_path / "profiles.sqlite3")


@pytest.fixture
def scope():
    return UserScope("synthetic-app", "synthetic-alice")
