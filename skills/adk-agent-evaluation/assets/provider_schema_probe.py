"""Offline evidence matching example; no SDK, network, budget or semantic checks.

Feed exact synthetic bytes captured after the target adapter serializes a request.
Observation outcomes must come from the named boundary, not a model's claim.
"""

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class Route:
    provider: str
    endpoint: str
    model: str
    adapter_version: str
    mode: str


@dataclass(frozen=True)
class Observation:
    route: Route
    request_sha256: str
    boundary: str
    accepted: bool


def request_hash(wire_request: bytes) -> str:
    if not isinstance(wire_request, bytes) or not wire_request:
        raise ValueError("capture a nonempty serialized request")
    return hashlib.sha256(wire_request).hexdigest()


def require_compatible(route: Route, requests: list[bytes],
                       observations: list[Observation], *, boundary: str) -> None:
    """Fail unless every exact request has one accepted record at this boundary.

    Rejected/uncertain historical observations belong to their original immutable
    experiment. Supply this gate's selected attempt records explicitly; never pick
    a later success merely to discard a failed trial.
    """
    if boundary not in {"controlled_transport", "live_provider"}:
        raise ValueError("choose controlled_transport or live_provider explicitly")
    if not all(isinstance(value, str) and value.strip() for value in (
            route.provider, route.endpoint, route.model, route.adapter_version, route.mode)):
        raise ValueError("route identity must be complete")
    expected = {request_hash(request) for request in requests}
    if not expected:
        raise ValueError("zero requests cannot establish compatibility")
    if len(observations) != len(expected):
        raise ValueError("missing or extra observations")
    seen = set()
    for observation in observations:
        if observation.route != route or observation.boundary != boundary:
            raise ValueError("route or evidence boundary mismatch")
        if observation.request_sha256 not in expected or observation.request_sha256 in seen:
            raise ValueError("unexpected or duplicate request observation")
        if observation.accepted is not True:
            raise ValueError("request was rejected or compatibility remains unverified")
        seen.add(observation.request_sha256)
