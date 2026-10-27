"""Occurrence labels for policy passages: what findings cite."""
from __future__ import annotations


def occurrence_label(p: dict) -> str:
    base = f"{p['document']}-{p['version']}/p{p['page']}"
    if p["kind"] == "cell":
        return f"{base}/{p['table']}/c{p['col']}"
    if p["kind"] == "clause":
        return f"{base}/{p['clause']}"
    return f"{base}/{p['kind']}"


def label_index(passages: list[dict]) -> dict[str, dict]:
    """label -> passage. Later passages with the same label replace earlier ones."""
    return {occurrence_label(p): p for p in passages}
