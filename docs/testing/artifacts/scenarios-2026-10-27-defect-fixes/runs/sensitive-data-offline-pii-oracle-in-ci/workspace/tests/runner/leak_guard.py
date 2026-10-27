"""Offline leak detector for test runs: no Google Cloud, no ADK import, no network.

It scans the text of every sink a Runner test touches (model requests, session events and
state, log records, provider-bound tool calls) with detectors that do NOT depend on the
screening fakes, so a fake that is too lenient cannot hide a leak.

Coverage is what the detectors below match and nothing more: the synthetic canaries, our
credential formats, and email, card (Luhn) and E.164-style phone shapes. Names, addresses,
free-text identifiers and re-encoded values (base64, spelled-out digits) are NOT detected.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from tests.runner import canaries

_UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
_CREDENTIALS = {
    "payments_key": re.compile(r"hpk_(?:live|test)_[0-9a-fA-F]{32}"),
    "mail_relay_token": re.compile(r"hmr-[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"),
    "jwt": re.compile(r"eyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}"),
}
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_PHONE = re.compile(r"(?<![\w.])\+\d[\d ()-]{7,16}\d")
_CARD = re.compile(r"(?<![\w.-])\d(?:[ -]?\d){12,18}(?![\w.])")


def _luhn(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2:
            n = n * 2 - 9 if n > 4 else n * 2
        total += n
    return total % 10 == 0


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value)


@dataclass(frozen=True)
class Finding:
    sink: str
    kind: str
    sample: str  # masked: never print the value that leaked

    def __str__(self) -> str:
        return f"{self.sink}: {self.kind} {self.sample}"


def _mask(value: str) -> str:
    return f"{value[:2]}…({len(value)} chars)"


def scan_text(text: str, sink: str, *, shapes: bool = True) -> list[Finding]:
    """Return findings in `text`. `shapes=False` limits it to canaries, credentials and cards,
    for provider-bound requests where an email recipient or API auth is legitimate."""
    found: list[Finding] = []
    lowered = text.lower()
    digits_only = _digits(text)
    for value in canaries.ALL:
        if value.lower() in lowered or (_digits(value) and len(_digits(value)) >= 10
                                        and _digits(value) in digits_only):
            found.append(Finding(sink, "canary", _mask(value)))
    for kind, pattern in _CREDENTIALS.items():
        found += [Finding(sink, kind, _mask(m.group())) for m in pattern.finditer(text)]
    scrubbed = _UUID.sub(" ", text)
    for m in _CARD.finditer(scrubbed):
        d = _digits(m.group())
        if 13 <= len(d) <= 19 and _luhn(d):
            found.append(Finding(sink, "card_number", _mask(m.group())))
    if shapes:
        found += [Finding(sink, "email", _mask(m.group())) for m in _EMAIL.finditer(text)]
        found += [Finding(sink, "phone", _mask(m.group())) for m in _PHONE.finditer(scrubbed)]
    return sorted(set(found), key=lambda f: (f.sink, f.kind, f.sample))


def dump(obj) -> str:
    """Serialise a pydantic model, dict or anything else to text without dropping fields."""
    for name in ("model_dump_json",):
        fn = getattr(obj, name, None)
        if fn:
            try:
                return fn()
            except Exception:
                pass
    return repr(obj)


class _Capture(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.texts: list[str] = []

    def emit(self, record):
        try:
            extras = {k: v for k, v in record.__dict__.items() if k not in logging.makeLogRecord({}).__dict__
                      and k not in ("message", "asctime")}
            self.texts.append(" ".join([record.getMessage(), str(record.args), record.exc_text or "", repr(extras)]))
        except Exception as exc:  # a record that cannot be rendered must not pass unscanned
            self.texts.append(f"<unrenderable log record: {exc!r}> {record.msg!r}")


class LeakGuard:
    """Collects sink text during a test and fails it at the end if any detector matched.

    Logs are captured from the root logger at DEBUG, which includes ADK's own debug logging of
    requests. Loggers with propagate=False are not seen.
    """

    def __init__(self):
        self._capture = _Capture()
        self._root = logging.getLogger()
        self._prior_level = self._root.level
        self.model_requests: list = []
        self.events: list = []
        self.sessions: list = []
        self.provider_transports: dict[str, object] = {}

    def start(self):
        self._root.addHandler(self._capture)
        self._root.setLevel(logging.DEBUG)

    def stop(self):
        self._root.removeHandler(self._capture)
        self._root.setLevel(self._prior_level)

    def findings(self) -> list[Finding]:
        out: list[Finding] = []
        for i, req in enumerate(self.model_requests):
            out += scan_text(dump(req), f"model_request[{i}]")
        for i, ev in enumerate(self.events):
            out += scan_text(dump(ev), f"event[{i}]")
        for i, sess in enumerate(self.sessions):
            out += scan_text(dump(sess), f"session[{i}]")  # includes stored events and state
        for i, text in enumerate(self._capture.texts):
            out += scan_text(text, f"log[{i}]")
        for name, transport in self.provider_transports.items():
            for i, req in enumerate(getattr(transport, "requests", [])):
                headers = {k: v for k, v in (req.get("headers") or {}).items()
                           if k.lower() not in ("authorization", "x-api-key")}
                out += scan_text(repr({**req, "headers": headers}), f"tool_call:{name}[{i}]", shapes=False)
        return out

    def report(self) -> str:
        return "\n".join(str(f) for f in self.findings())
