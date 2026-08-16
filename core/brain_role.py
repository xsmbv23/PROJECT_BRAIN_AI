"""Brain foundation role: governance, not data ownership or calculation."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .foundation_hardening import CapabilityLease, GovernanceDeny, PolicyPin, validate_schema_major


class Plane(str, Enum):
    CHAT = "CHAT"
    BRAIN = "BRAIN"
    DATA = "DATA"
    ENGINE = "ENGINE"
    SECURITY = "SECURITY"


@dataclass(frozen=True)
class PlaneRequest:
    source: Plane
    destination: Plane
    corridor_id: str
    policy_version: str
    schema_version: str
    brain_state_version: str
    capability_id: str
    nonce: str


class BrainRole:
    """Deterministic governance gate between interface and execution planes.

    Brain may decide whether a request is admissible, pin policy/schema/state,
    quarantine suspicious requests, and emit audit metadata. It must not own
    source data, market calculations, network credentials, or application UI.
    Every admission must carry a scoped, expiring capability lease whose
    destination matches the requested next plane.
    """

    def __init__(self, pin: PolicyPin) -> None:
        self.pin = pin

    def authorize(
        self,
        request: PlaneRequest,
        *,
        lease: CapabilityLease,
        expected_schema_major: str,
        now: float,
        operation_count: int = 0,
    ) -> str:
        if request.destination is Plane.BRAIN:
            raise GovernanceDeny("BRAIN_SELF_SERVICE_DENY")
        self.pin.verify(
            policy_version=request.policy_version,
            schema_version=request.schema_version,
            brain_state_version=request.brain_state_version,
        )
        validate_schema_major(received=request.schema_version, expected=expected_schema_major)
        if not request.capability_id.strip() or not request.nonce.strip():
            raise GovernanceDeny("CAPABILITY_REQUIRED")
        lease.verify(
            now=now,
            corridor_id=request.corridor_id,
            capability_id=request.capability_id,
            nonce=request.nonce,
            policy_version=request.policy_version,
            operation_count=operation_count,
        )
        if lease.source_layer not in {request.source.value, "*"}:
            raise GovernanceDeny("CAPABILITY_SOURCE_LAYER_DENY")
        if lease.destination_layer not in {request.destination.value, "*"}:
            raise GovernanceDeny("CAPABILITY_DESTINATION_LAYER_DENY")
        return "ADMISSIBLE_FOR_NEXT_GATE"
