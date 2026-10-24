#!/usr/bin/env python3
"""Fetch or load an A2A agent card and check its contract before an ADK agent trusts it.

Reads ``/.well-known/agent-card.json`` from ``--url BASE`` (falling back to the
legacy ``/.well-known/agent.json``, which is flagged) or a local file with
``--file``. Validates the fields the A2A specification and Gemini Enterprise
registration require, that every RPC URL is https (plain http only on a
loopback host) and shares the origin the card was fetched from, that a
non-loopback endpoint declares ``securitySchemes``, parses ``protocolVersion``
and compares it with an optional ``--installed-a2a-sdk`` version, reports
capabilities (streaming, push notifications, extensions, extended card) and
flags long or instruction-like descriptions. For a signed card it checks the
JWS structure the specification requires (``protected`` and ``signature``; an
asymmetric ``alg``, ``kid`` and ``typ`` in the protected header; a ``jku`` on
https at the card's origin or a ``--key-host``), flags unprotected header
values and, on a 1.0 card, the fields an a2a-sdk 1.x verifier drops before
checking, which the signature therefore does not cover. It does not verify the
signature cryptographically. Accepts the a2a-sdk 0.3 card shape (``url``, ``preferredTransport``) and the 1.0 shape
(``supportedInterfaces``), with camelCase or snake_case keys.

Read-only: one GET per candidate path, no RPC call. Non-loopback hosts are
refused unless ``--allow-remote`` is given. Exit 0 when a card was obtained and
checked (findings are in the JSON), 1 when no card could be read, 2 for bad
arguments, 3 when ``--fail-on`` is given and a finding at that level or above
was reported (the JSON is still printed).
"""

from __future__ import annotations

import argparse
import base64
import binascii
import ipaddress
import json
from pathlib import Path
import re
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import urlsplit, urlunsplit


WELL_KNOWN_PATH = "/.well-known/agent-card.json"
LEGACY_PATH = "/.well-known/agent.json"
ADK_EXTENSION_URI = "https://google.github.io/adk-docs/a2a/a2a-extension/"
SPEC_CORE_FIELDS = ("name", "description", "version", "capabilities", "skills",
                    "defaultInputModes", "defaultOutputModes")
GEMINI_ENTERPRISE_FIELDS = ("protocolVersion", "name", "description", "url", "version",
                            "defaultInputModes", "defaultOutputModes", "capabilities", "skills")
DESCRIPTION_LONG = 500
# Field names an a2a-sdk 1.x verifier keeps: it parses the card into the proto
# with ignore_unknown_fields=True before canonicalising, so any other field is
# not covered by the signature (a2a-sdk 1.2.3 a2a.types descriptors and
# a2a/utils/signing.py, read 2026-10-24).
SIGNED_FIELDS = {
    "": {"name", "description", "supportedInterfaces", "provider", "version", "documentationUrl",
         "capabilities", "securitySchemes", "securityRequirements", "defaultInputModes",
         "defaultOutputModes", "skills", "signatures", "iconUrl"},
    "skills": {"id", "name", "description", "tags", "examples", "inputModes", "outputModes",
               "securityRequirements"},
    "capabilities": {"streaming", "pushNotifications", "extensions", "extendedAgentCard"},
    "provider": {"url", "organization"},
    "supportedInterfaces": {"url", "protocolBinding", "tenant", "protocolVersion"},
}
ASYMMETRIC_ALGS = {"RS256", "RS384", "RS512", "PS256", "PS384", "PS512",
                   "ES256", "ES384", "ES512", "ES256K", "EdDSA"}
VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?")
INSTRUCTION_PATTERNS = [
    (re.compile(r"\byou are (a|an|the)\b", re.I), "persona instruction"),
    (re.compile(r"\b(you must|you should|always|never) (call|use|invoke|run|respond|answer|include|pass)\b", re.I),
     "directive aimed at the model"),
    (re.compile(r"\bignore (all |any )?(previous|prior|above|earlier) (instructions|messages|rules)", re.I),
     "ignore previous instructions"),
    (re.compile(r"\b(do not|don't|never) (tell|mention|reveal|show|inform) (the )?user\b", re.I),
     "concealment instruction"),
    (re.compile(r"</?(important|system|instructions?|hidden|secret)>", re.I), "pseudo-markup marker"),
    (re.compile(r"\b(IMPORTANT|SYSTEM|NOTE TO (THE )?(MODEL|ASSISTANT|AI))\s*:", re.I), "attention marker"),
    (re.compile(r"\bsystem prompt\b", re.I), "system prompt reference"),
    (re.compile(r"(^|\n)\s*\d+\.\s+\S+.*\n\s*\d+\.\s+\S+", re.M), "numbered step list"),
    (re.compile(r"\b(call|invoke) the \w+ tool\b", re.I), "tool-call instruction"),
    (re.compile(r"[​‌‍⁠﻿­]"), "zero-width or invisible character"),
]


class CardError(Exception):
    """Raised when no usable card could be obtained."""


class NoRedirect(urlrequest.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        raise CardError(f"refusing to follow redirect ({code}) to {newurl}")


def positive(value):
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive number") from None
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive number")
    return number


def is_loopback_host(hostname: str | None) -> bool:
    if not hostname:
        return False
    host = hostname.strip("[]").lower()
    if host == "localhost" or host.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def to_camel(key: str) -> str:
    parts = key.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


_NAME_MAPS = {"securitySchemes", "schemes", "scopes"}


def normalise(value, keep_keys=False):
    """Return a copy with every mapping key in camelCase so both SDK spellings compare alike.

    Keys that name things the author chose (security scheme names, requirement
    scheme names, scope names) are kept as written, so the report shows the
    card's own names.
    """
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            key = str(k) if keep_keys else to_camel(str(k))
            out[key] = normalise(v, keep_keys=(key in _NAME_MAPS) or (keep_keys and key not in _NAME_MAPS and False))
        return out
    if isinstance(value, list):
        return [normalise(v, keep_keys=keep_keys) for v in value]
    return value


def _normalise_card(raw):
    """normalise() plus the two places where a 0.3 card keys by author-chosen name."""
    card = normalise(raw)
    if isinstance(raw, dict):
        for key in ("security", "security_requirements", "securityRequirements"):
            if isinstance(raw.get(key), list):
                card[to_camel(key)] = [{str(k): normalise(v, keep_keys=True) for k, v in entry.items()}
                                       if isinstance(entry, dict) else normalise(entry) for entry in raw[key]]
    return card


def origin(url: str) -> tuple[str, str, int | None]:
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    default = {"http": 80, "https": 443}.get(scheme)
    try:
        port = parts.port or default
    except ValueError:
        port = None
    return scheme, (parts.hostname or "").lower(), port


def fetch(url: str, timeout: float, max_bytes: int, headers: dict[str, str] | None = None) -> tuple[int, str]:
    opener = urlrequest.build_opener(NoRedirect)
    request_headers = {"Accept": "application/json"}
    request_headers.update(headers or {})
    req = urlrequest.Request(url, headers=request_headers, method="GET")
    try:
        with opener.open(req, timeout=timeout) as response:
            raw = response.read(max_bytes + 1)
            status = response.status
    except urlerror.HTTPError as exc:
        return exc.code, ""
    except (urlerror.URLError, OSError, ValueError) as exc:
        raise CardError(f"cannot reach {url}: {exc}") from exc
    if len(raw) > max_bytes:
        raise CardError(f"{url} returned more than {max_bytes} bytes")
    return status, raw.decode("utf-8", "replace")


def load_card_from_url(base: str, card_path: str | None, timeout: float, max_bytes: int,
                       headers: dict[str, str] | None = None) -> tuple[dict, str, bool]:
    parts = urlsplit(base)
    root = urlunsplit((parts.scheme, parts.netloc, parts.path.rstrip("/"), "", ""))
    candidates = [(card_path, False)] if card_path else [(WELL_KNOWN_PATH, False), (LEGACY_PATH, True)]
    attempts = []
    for path, legacy in candidates:
        url = root + (path if path.startswith("/") else "/" + path)
        status, text = fetch(url, timeout, max_bytes, headers)
        if status == 404:
            attempts.append(f"{url} -> 404")
            continue
        if status in {401, 403}:
            raise CardError(f"{url} returned HTTP {status}; an authenticated card (for example Agent Runtime's"
                            " /v1/card) needs --header Authorization=Bearer ... and usually --card-path")
        if status != 200:
            raise CardError(f"{url} returned HTTP {status}")
        try:
            data = json.loads(text)
        except ValueError as exc:
            raise CardError(f"{url} did not return JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise CardError(f"{url} returned a JSON value that is not an object")
        return data, url, legacy
    raise CardError("no agent card found: " + "; ".join(attempts))


def load_card_from_file(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CardError(f"cannot read agent card {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CardError(f"{path} does not hold a JSON object")
    return data


def rpc_urls(card: dict) -> list[str]:
    urls = []
    top = card.get("url")
    if isinstance(top, str) and top:
        urls.append(top)
    for key in ("supportedInterfaces", "additionalInterfaces"):
        for iface in card.get(key) or []:
            if isinstance(iface, dict) and isinstance(iface.get("url"), str) and iface["url"]:
                urls.append(iface["url"])
    deduped = []
    for url in urls:
        if url not in deduped:
            deduped.append(url)
    return deduped


def card_protocol_version(card: dict) -> str | None:
    version = card.get("protocolVersion")
    if isinstance(version, str) and version:
        return version
    for iface in card.get("supportedInterfaces") or []:
        if isinstance(iface, dict) and isinstance(iface.get("protocolVersion"), str) and iface["protocolVersion"]:
            return iface["protocolVersion"]
    return None


def parse_version(text: str | None):
    if not isinstance(text, str):
        return None
    match = VERSION_PATTERN.match(text.strip().lstrip("v"))
    if not match:
        return None
    return tuple(int(part) for part in match.groups(default="0"))


def text_findings(where: str, text: str, checks: list[dict]) -> None:
    if len(text) > DESCRIPTION_LONG:
        checks.append({"code": "description_long", "level": "review", "heuristic": True,
                       "message": f"{where} is {len(text)} characters; ADK main caps relayed card descriptions at 1024 and quotes them, 2.8.0 relays them unmodified"})
    for pattern, label in INSTRUCTION_PATTERNS:
        match = pattern.search(text)
        if match:
            checks.append({"code": "description_instruction_like", "level": "review", "heuristic": True,
                           "message": f"{where} contains {label}: {match.group(0).strip()[:60]!r}; a card describes capability, it does not instruct the caller's model"})


def _decode_protected(value: str) -> dict | None:
    try:
        raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
        header = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, binascii.Error):
        return None
    return header if isinstance(header, dict) else None


def unsigned_fields(card: dict) -> list[str]:
    paths = sorted(f for f in card if f not in SIGNED_FIELDS[""])
    for key in ("skills", "supportedInterfaces"):
        for index, item in enumerate(card.get(key) or []):
            if isinstance(item, dict):
                paths += [f"{key}[{index}].{f}" for f in sorted(item) if f not in SIGNED_FIELDS[key]]
    for key in ("capabilities", "provider"):
        if isinstance(card.get(key), dict):
            paths += [f"{key}.{f}" for f in sorted(card[key]) if f not in SIGNED_FIELDS[key]]
    return paths


def signature_checks(card: dict, *, shape: str, fetched_from: str | None, key_hosts: list[str],
                     require: bool, checks: list[dict]) -> list[str]:
    """Structural JWS checks on card signatures; returns the algorithms seen."""
    signatures = card.get("signatures")
    if signatures is None:
        if require:
            checks.append({"code": "signature_missing", "level": "error", "heuristic": False,
                           "message": "card carries no signatures and --require-signature was given"})
        return []
    if not isinstance(signatures, list) or not signatures:
        checks.append({"code": "signatures_malformed", "level": "error", "heuristic": False,
                       "message": "signatures must be a nonempty list of AgentCardSignature objects"})
        return []
    card_host = origin(fetched_from)[1] if fetched_from else None
    allowed_hosts = {h.lower() for h in key_hosts} | ({card_host} if card_host else set())
    algs = []
    for index, sig in enumerate(signatures):
        where = f"signatures[{index}]"
        if not isinstance(sig, dict):
            checks.append({"code": "signatures_malformed", "level": "error", "heuristic": False,
                           "message": f"{where} is not an object"})
            continue
        missing = [f for f in ("protected", "signature") if not isinstance(sig.get(f), str) or not sig.get(f)]
        if missing:
            checks.append({"code": "signature_field_missing", "level": "error", "heuristic": False,
                           "message": f"{where} has no {' or '.join(missing)}; both are required JWS components"})
        if sig.get("header"):
            checks.append({"code": "signature_unprotected_header", "level": "review", "heuristic": False,
                           "message": f"{where}.header values are not integrity-protected; trust only what is in the protected header"})
        if "protected" in missing:
            continue
        header = _decode_protected(sig["protected"])
        if header is None:
            checks.append({"code": "signature_protected_invalid", "level": "error", "heuristic": False,
                           "message": f"{where}.protected is not base64url-encoded JSON"})
            continue
        alg = header.get("alg")
        algs.append(alg if isinstance(alg, str) else None)
        if not isinstance(alg, str) or not alg:
            checks.append({"code": "signature_alg_missing", "level": "error", "heuristic": False,
                           "message": f"{where} protected header has no alg (a2a-sdk's signer then defaults to HS256)"})
        elif alg.lower() == "none" or alg.upper().startswith("HS"):
            checks.append({"code": "signature_alg_not_asymmetric", "level": "error", "heuristic": False,
                           "message": f"{where} uses {alg}; a card signature must use an asymmetric algorithm a verifier can pin"})
        elif alg not in ASYMMETRIC_ALGS:
            checks.append({"code": "signature_alg_unknown", "level": "review", "heuristic": False,
                           "message": f"{where} uses {alg}; confirm the verifier's algorithm allowlist includes it"})
        if not isinstance(header.get("kid"), str) or not header.get("kid"):
            checks.append({"code": "signature_kid_missing", "level": "error", "heuristic": False,
                           "message": f"{where} protected header has no kid, which the specification requires"})
        if header.get("typ") != "JOSE":
            checks.append({"code": "signature_typ_not_jose", "level": "review", "heuristic": False,
                           "message": f"{where} protected header typ is {header.get('typ')!r}; the specification says it SHOULD be 'JOSE'"})
        jku = header.get("jku")
        if jku is not None:
            scheme, host, _ = origin(jku) if isinstance(jku, str) else ("", "", None)
            if scheme != "https":
                checks.append({"code": "signature_jku_not_https", "level": "error", "heuristic": False,
                               "message": f"{where} jku is not an https URL: {jku!r}"})
            elif not allowed_hosts:
                checks.append({"code": "signature_jku_unchecked", "level": "review", "heuristic": False,
                               "message": f"{where} jku {jku} cannot be checked against an origin for a local file; pass --key-host"})
            elif host not in allowed_hosts:
                checks.append({"code": "signature_jku_off_origin", "level": "error", "heuristic": False,
                               "message": f"{where} jku host {host} is neither the card's origin nor a --key-host"})
            checks.append({"code": "signature_jku_present", "level": "info", "heuristic": False,
                           "message": f"{where} names a jku; a verifier must take keys from a key set agreed out of band, never from the card it is verifying"})
    if shape.startswith("a2a-1.0"):
        uncovered = unsigned_fields(card)
        if uncovered:
            checks.append({"code": "signature_fields_uncovered", "level": "review", "heuristic": False,
                           "message": "fields outside the a2a-sdk 1.x card schema are dropped before verification, so the signature does not cover them: " + ", ".join(uncovered)})
    else:
        checks.append({"code": "signature_shape_unchecked", "level": "review", "heuristic": False,
                       "message": "signed card in the 0.3 shape; which fields the signature covers depends on the pinned a2a-sdk's verifier"})
    return algs


def check_card(card: dict, *, fetched_from: str | None, legacy_path: bool, installed_sdk: str | None,
               key_hosts: list[str] | None = None, require_signature: bool = False) -> dict:
    checks: list[dict] = []
    shape = "unknown"
    if isinstance(card.get("supportedInterfaces"), list):
        shape = "a2a-1.0 (supportedInterfaces)"
    elif isinstance(card.get("url"), str):
        shape = "a2a-0.3 (url, preferredTransport)"
    if legacy_path:
        checks.append({"code": "legacy_card_path", "level": "review", "heuristic": False,
                       "message": f"card served only at {LEGACY_PATH}; the specification renamed the well-known path to {WELL_KNOWN_PATH} in 0.3"})

    missing_core = [f for f in SPEC_CORE_FIELDS if f not in card]
    for name in missing_core:
        checks.append({"code": "required_field_missing", "level": "error", "heuristic": False,
                       "message": f"card has no {name!r}"})
    urls = rpc_urls(card)
    if not urls:
        checks.append({"code": "rpc_url_missing", "level": "error", "heuristic": False,
                       "message": "no RPC url (top-level url or supportedInterfaces[].url); RemoteA2aAgent raises AgentCardResolutionError"})
    if not isinstance(card.get("skills"), list) or not card.get("skills"):
        if "skills" in card:
            checks.append({"code": "skills_empty", "level": "review", "heuristic": False,
                           "message": "skills is empty; callers and registries select agents by skills"})
    else:
        for index, skill in enumerate(card["skills"]):
            if not isinstance(skill, dict):
                checks.append({"code": "skill_malformed", "level": "error", "heuristic": False,
                               "message": f"skills[{index}] is not an object"})
                continue
            for name in ("id", "name", "description"):
                if not isinstance(skill.get(name), str) or not skill.get(name):
                    checks.append({"code": "skill_field_missing", "level": "error", "heuristic": False,
                                   "message": f"skills[{index}] has no {name!r}"})
            if isinstance(skill.get("description"), str):
                text_findings(f"skills[{index}].description", skill["description"], checks)

    ge_missing = [f for f in GEMINI_ENTERPRISE_FIELDS if f not in card]
    for name in ge_missing:
        if name == "url" and urls:
            message = "no top-level url; Gemini Enterprise registration reads url and supports A2A v0.3 cards (1.0 needs the compatibility packages)"
        elif name == "protocolVersion":
            message = ("no top-level protocolVersion; this 1.0 card declares it per interface, but Gemini"
                       " Enterprise registration reads the top-level field (0.3 card shape)"
                       if card_protocol_version(card) else
                       "no protocolVersion; ADK's AgentCardBuilder writes one, a hand-written agent.json must add it")
        else:
            message = f"Gemini Enterprise registration requires {name!r}"
        checks.append({"code": "gemini_enterprise_field_missing", "level": "review", "heuristic": False,
                       "message": message})

    source_origin = origin(fetched_from) if fetched_from else None
    any_remote_rpc = False
    for url in urls:
        scheme, host, _ = origin(url)
        if scheme not in {"http", "https"} or not host:
            checks.append({"code": "rpc_url_invalid", "level": "error", "heuristic": False,
                           "message": f"RPC url is not an http(s) URL with a host: {url}"})
            continue
        loopback = is_loopback_host(host)
        if not loopback:
            any_remote_rpc = True
        if url.endswith("/") and urlsplit(url).path not in {"", "/"}:
            checks.append({"code": "rpc_url_trailing_slash", "level": "review", "heuristic": False,
                           "message": f"RPC url ends with '/'; ADK's card builder strips it and registries have rejected trailing slashes: {url}"})
        if scheme != "https" and not loopback:
            checks.append({"code": "rpc_url_not_https", "level": "error", "heuristic": False,
                           "message": f"RPC url uses plain http on a non-loopback host; RemoteA2aAgent (2.8.0 to 2.12.0) refuses it for a fetched card: {url}"})
        if source_origin and origin(url) != source_origin:
            checks.append({"code": "rpc_url_origin_mismatch", "level": "error", "heuristic": False,
                           "message": f"RPC url origin differs from where the card was fetched ({fetched_from}); RemoteA2aAgent (2.8.0 to 2.12.0) refuses it: {url}"})

    schemes = card.get("securitySchemes")
    requirements = card.get("security") or card.get("securityRequirements")
    has_schemes = isinstance(schemes, dict) and bool(schemes)
    if any_remote_rpc and not has_schemes:
        checks.append({"code": "no_security_schemes", "level": "error", "heuristic": False,
                       "message": "non-loopback endpoint declares no securitySchemes; the A2A enterprise baseline carries auth in HTTP headers declared by the card"})
    if has_schemes and not requirements:
        checks.append({"code": "security_requirements_missing", "level": "review", "heuristic": False,
                       "message": "securitySchemes declared but no security requirement list says which scheme a caller must satisfy"})
    for scheme_name, scheme in (schemes or {}).items() if has_schemes else []:
        if not isinstance(scheme, dict):
            continue
        inner = scheme.get("apiKeySecurityScheme") or scheme
        location = inner.get("in") or inner.get("location")
        if isinstance(location, str) and location.lower() not in {"header", "api_key_location_header"} and "name" in inner:
            checks.append({"code": "api_key_not_in_header", "level": "review", "heuristic": False,
                           "message": f"securitySchemes[{scheme_name!r}] puts the API key in {location!r}; the enterprise baseline carries credentials in headers"})

    protocol_version = card_protocol_version(card)
    parsed = parse_version(protocol_version)
    if protocol_version is None:
        checks.append({"code": "protocol_version_missing", "level": "review", "heuristic": False,
                       "message": "no protocolVersion anywhere on the card; a2a-sdk 1.x clients send A2A-Version and treat an empty value as 0.3"})
    elif parsed is None:
        checks.append({"code": "protocol_version_unparsable", "level": "error", "heuristic": False,
                       "message": f"protocolVersion {protocol_version!r} is not Major.Minor[.Patch]"})
    sdk_parsed = parse_version(installed_sdk)
    if installed_sdk and sdk_parsed is None:
        checks.append({"code": "installed_sdk_unparsable", "level": "error", "heuristic": False,
                       "message": f"--installed-a2a-sdk {installed_sdk!r} is not a version"})
    if parsed and sdk_parsed:
        card_major = parsed[0]
        sdk_major = sdk_parsed[0]
        if card_major >= 1 and sdk_major == 0:
            checks.append({"code": "protocol_version_sdk_mismatch", "level": "review", "heuristic": False,
                           "message": f"card speaks A2A {protocol_version} but the installed a2a-sdk is {installed_sdk} (0.3 wire format); confirm the server keeps a 0.3-compatible route"})
        elif card_major == 0 and sdk_major >= 1:
            checks.append({"code": "protocol_version_sdk_mismatch", "level": "info", "heuristic": False,
                           "message": f"card speaks A2A {protocol_version}; a2a-sdk {installed_sdk} sends A2A-Version 1.x and ADK's _compat parses 0.3 cards, so test the exchange on the pinned versions"})

    capabilities = card.get("capabilities") if isinstance(card.get("capabilities"), dict) else {}
    extensions = capabilities.get("extensions") if isinstance(capabilities.get("extensions"), list) else []
    extension_uris = [e.get("uri") for e in extensions if isinstance(e, dict) and isinstance(e.get("uri"), str)]
    adk_extension = ADK_EXTENSION_URI in extension_uris
    if "capabilities" in card and not isinstance(card.get("capabilities"), dict):
        checks.append({"code": "capabilities_not_object", "level": "error", "heuristic": False,
                       "message": "capabilities must be an object"})

    signature_algs = signature_checks(card, shape=shape, fetched_from=fetched_from,
                                      key_hosts=key_hosts or [], require=require_signature, checks=checks)

    description = card.get("description")
    if isinstance(description, str):
        text_findings("description", description, checks)
    elif "description" in card:
        checks.append({"code": "description_not_string", "level": "error", "heuristic": False,
                       "message": "description must be a string"})
    if isinstance(card.get("name"), str) and not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_ .-]{0,127}", card["name"]):
        checks.append({"code": "name_unusual", "level": "review", "heuristic": True,
                       "message": "name has unusual characters; ADK uses the RemoteA2aAgent name, not the card name, for transfer targets"})
    if isinstance(card.get("provider"), dict) is False and "provider" in card:
        checks.append({"code": "provider_not_object", "level": "error", "heuristic": False,
                       "message": "provider must be an object"})

    return {
        "shape": shape,
        "summary": {
            "name": card.get("name"), "version": card.get("version"), "protocol_version": protocol_version,
            "rpc_urls": urls, "preferred_transport": card.get("preferredTransport"),
            "protocol_bindings": sorted({i.get("protocolBinding") for i in card.get("supportedInterfaces") or []
                                         if isinstance(i, dict) and isinstance(i.get("protocolBinding"), str)}),
            "streaming": bool(capabilities.get("streaming")),
            "push_notifications": bool(capabilities.get("pushNotifications")),
            "state_transition_history": bool(capabilities.get("stateTransitionHistory")),
            "extended_card": bool(capabilities.get("extendedAgentCard")) or bool(card.get("supportsAuthenticatedExtendedCard")),
            "extensions": extension_uris, "adk_a2a_extension": adk_extension,
            "security_schemes": sorted(schemes.keys()) if has_schemes else [],
            "signatures": len(card["signatures"]) if isinstance(card.get("signatures"), list) else 0,
            "signature_algs": signature_algs,
            "skills": len(card["skills"]) if isinstance(card.get("skills"), list) else 0,
            "description_length": len(description) if isinstance(description, str) else None,
        },
        "gemini_enterprise": {"required_present": [f for f in GEMINI_ENTERPRISE_FIELDS if f in card],
                              "missing": ge_missing},
        "checks": checks,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Fetches the card only; sends no A2A message. Description findings are heuristics.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", metavar="BASE", help="agent base URL; the well-known card path is appended")
    source.add_argument("--file", type=Path, metavar="CARD.json", help="local agent card file")
    parser.add_argument("--card-path", metavar="PATH",
                        help="override the well-known card path for --url (Agent Runtime serves /v1/card)")
    parser.add_argument("--header", action="append", default=[], metavar="K=V",
                        help="HTTP header for the card GET (repeatable); values are not printed")
    parser.add_argument("--allow-remote", action="store_true", help="permit a non-loopback --url host")
    parser.add_argument("--installed-a2a-sdk", metavar="VERSION",
                        help="installed a2a-sdk version to compare with the card's protocolVersion")
    parser.add_argument("--require-signature", action="store_true",
                        help="report an unsigned card as an error")
    parser.add_argument("--key-host", action="append", default=[], metavar="HOST",
                        help="host besides the card's origin that may serve its jku key set (repeatable)")
    parser.add_argument("--fail-on", choices=("error", "review"),
                        help="exit 3 when a finding at this level or above is reported (for CI)")
    parser.add_argument("--timeout", type=positive, default=10.0, help="seconds per request (default: 10)")
    parser.add_argument("--max-bytes", type=int, default=1_000_000, help="maximum card size (default: 1000000)")
    args = parser.parse_args(argv)
    if args.max_bytes < 1024:
        parser.error("--max-bytes must be at least 1024")
    if (args.card_path or args.header) and not args.url:
        parser.error("--card-path and --header require --url")
    headers = {}
    for item in args.header:
        if "=" not in item or not item.split("=", 1)[0].strip():
            parser.error(f"--header expects KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        headers[key.strip()] = value
    if args.url:
        parts = urlsplit(args.url)
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            parser.error(f"--url must be an http(s) URL with a host: {args.url!r}")
        if not is_loopback_host(parts.hostname) and not args.allow_remote:
            parser.error(f"{args.url!r} is not a loopback host; pass --allow-remote after the owner approves the fetch")

    result = {"source": args.url or str(args.file), "card_url": None, "legacy_path": False,
              "installed_a2a_sdk": args.installed_a2a_sdk, "partial": False, "error": None}
    try:
        if args.url:
            raw, card_url, legacy = load_card_from_url(args.url, args.card_path, args.timeout, args.max_bytes,
                                                       headers)
            result["card_url"] = card_url
            result["legacy_path"] = legacy
            fetched_from = card_url
        else:
            raw = load_card_from_file(args.file)
            legacy = False
            fetched_from = None
        card = _normalise_card(raw)
        result.update(check_card(card, fetched_from=fetched_from, legacy_path=legacy,
                                 installed_sdk=args.installed_a2a_sdk, key_hosts=args.key_host,
                                 require_signature=args.require_signature))
    except CardError as exc:
        result["partial"] = True
        result["error"] = str(exc)
        result["checks"] = []
    checks = result.get("checks", [])
    result["counts"] = {"checks": len(checks),
                        "errors": sum(1 for c in checks if c["level"] == "error"),
                        "review": sum(1 for c in checks if c["level"] == "review"),
                        "info": sum(1 for c in checks if c["level"] == "info"),
                        "by_code": {code: sum(1 for c in checks if c["code"] == code)
                                    for code in sorted({c["code"] for c in checks})}}
    result["notes"] = [
        "Checks mirror RemoteA2aAgent 2.8.0 to 2.12.0 card validation (https or loopback, same origin) plus specification and registration requirements.",
        "description_instruction_like, description_long and name_unusual are heuristics; the owner reads the text.",
        "Signature checks are structural; verify the signature itself with a2a-sdk's create_signature_verifier against a key set agreed out of band.",
    ]
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["partial"]:
        return 1
    failing = {"error": ("error",), "review": ("error", "review")}.get(args.fail_on, ())
    return 3 if any(result["counts"][{"error": "errors", "review": "review"}[level]] for level in failing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
