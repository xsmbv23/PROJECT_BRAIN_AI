"""Brain foundation role: governance, not data ownership or calculation."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .foundation_hardening import GovernanceDeny, PolicyPin, validate_schema_major


class Plane(str, Enum):
    CHAT = "CHAT"
    BRAIN = "BRAIN"
    DATA = "DATA"
    ENGINE = "ENGINE"


@dataclass(frozen=True)
class PlaneRequest:
    source: Plane
    destination: Plane
    policy_version: str
    schema_version: str
    brain_state_version: str
    capability_id: str


class BrainRole:
    """Deterministic governance gate between interface and execution planes.

    Brain may decide whether a request is admissible, pin policy/schema/state,
    quarantine suspicious requests, and emit audit metadata. It must not own
    source data, market calculations, network credentials, or application UI.
    """

    def __init__(self, pin: PolicyPin) -> None:
        self.pin = pin

    def authorize(self, request: PlaneRequest, *, expected_schema_major: str) -> str:
        if request.destination is Plane.BRAIN:
            raise GovernanceDeny("BRAIN_SELF_SERVICE_DENY")
        self.pin.verify(
            policy_version=request.policy_version,
            schema_version=request.schema_version,
            brain_state_version=request.brain_state_version,
        )
        validate_schema_major(received=request.schema_version, expected=expected_schema_major)
        if not request.capability_id.strip():
            raise GovernanceDeny("CAPABILITY_REQUIRED")
        return "ADMISSIBLE_FOR_NEXT_GATE"
