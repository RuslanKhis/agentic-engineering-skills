"""Shared offline helpers: repo paths, source scanning and a socket guard."""
from __future__ import annotations

import ast
import socket
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"


def app_sources() -> dict[Path, str]:
    return {p: p.read_text() for p in sorted(APP.rglob("*.py"))}


def imported_and_named(source: str) -> set[str]:
    """Every imported module/name and every identifier or attribute used in the source."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            found.add(node.module or "")
            found.update(a.name for a in node.names)
        elif isinstance(node, ast.Name):
            found.add(node.id)
        elif isinstance(node, ast.Attribute):
            found.add(node.attr)
    return found


class NoNetworkTestCase(unittest.TestCase):
    """Any socket connection attempt fails the test, so a tool that dials out is caught."""

    def setUp(self):
        self.attempts: list[object] = []

        def refuse(sock, address, *a, **k):
            self.attempts.append(address)
            raise AssertionError(f"outbound connection attempted: {address!r}")

        for target in ("socket.socket.connect", "socket.socket.connect_ex"):
            p = mock.patch(target, refuse)
            p.start()
            self.addCleanup(p.stop)
        p = mock.patch("socket.getaddrinfo", lambda *a, **k: self.attempts.append(a[:2]) or
                       (_ for _ in ()).throw(AssertionError(f"DNS lookup attempted: {a[:2]!r}")))
        p.start()
        self.addCleanup(p.stop)
