from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import secrets
from typing import Any


class Denied(Exception):
    pass


def sha256_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Corridor:
    corridor_id: str
    source_room: str
    destination_room: str
    source_layer: str
    destination_layer: str
    capability: str
    mutation: bool = False


@dataclass(frozen=True)
class Envelope:
    message_id: str
    project_id: str
    source_room: str
    destination_room: str
    source_layer: str
    destination_layer: str
    corridor_id: str
    capability: str
    nonce: str
    issued_at: str
    expires_at: str
    lineage: tuple[str, ...]
    payload_sha256: str
    payload: dict[str, Any]


class BrainGate:
    """Default-deny, replay-protected, lineage-aware communication gate."""

    def __init__(self, corridors: list[Corridor]) -> None:
        self._corridors = {c.corridor_id: c for c in corridors}
        self._used_nonces: set[tuple[str, str]] = set()
        self.audit: list[dict[str, Any]] = []

    def issue_envelope(
        self,
        *,
        project_id: str,
        source_room: str,
        destination_room: str,
        source_layer: str,
        destination_layer: str,
        corridor_id: str,
        capability: str,
        payload: dict[str, Any],
        lineage: list[str],
        ttl_seconds: int = 300,
    ) -> Envelope:
        corridor = self._corridors.get(corridor_id)
        if corridor is None:
            raise Denied("UNKNOWN_CORRIDOR")
        if (corridor.source_room, corridor.destination_room) != (source_room, destination_room):
            raise Denied("CORRIDOR_ENDPOINT_MISMATCH")
        if (corridor.source_layer, corridor.destination_layer) != (source_layer, destination_layer):
            raise Denied("CORRIDOR_LAYER_MISMATCH")
        if corridor.capability != capability:
            raise Denied("CAPABILITY_SCOPE_MISMATCH")
        if not lineage:
            raise Denied("MISSING_LINEAGE")

        now = datetime.now(timezone.utc)
        nonce = secrets.token_urlsafe(24)
        return Envelope(
            message_id=secrets.token_urlsafe(18),
            project_id=project_id,
            source_room=source_room,
            destination_room=destination_room,
            source_layer=source_layer,
            destination_layer=destination_layer,
            corridor_id=corridor_id,
            capability=capability,
            nonce=nonce,
            issued_at=now.isoformat(),
            expires_at=(now.timestamp() + ttl_seconds).__str__(),
            lineage=tuple(lineage),
            payload_sha256=sha256_json(payload),
            payload=payload,
        )

    def accept(self, envelope: Envelope) -> dict[str, Any]:
        corridor = self._corridors.get(envelope.corridor_id)
        try:
            if corridor is None:
                raise Denied("UNKNOWN_CORRIDOR")
            if corridor.source_room != envelope.source_room or corridor.destination_room != envelope.destination_room:
                raise Denied("CORRIDOR_ENDPOINT_MISMATCH")
            if corridor.source_layer != envelope.source_layer or corridor.destination_layer != envelope.destination_layer:
                raise Denied("CORRIDOR_LAYER_MISMATCH")
            if corridor.capability != envelope.capability:
                raise Denied("CAPABILITY_SCOPE_MISMATCH")
            if not envelope.lineage:
                raise Denied("MISSING_LINEAGE")
            if sha256_json(envelope.payload) != envelope.payload_sha256:
                raise Denied("PAYLOAD_HASH_MISMATCH")
            nonce_key = (envelope.corridor_id, envelope.nonce)
            if nonce_key in self._used_nonces:
                raise Denied("REPLAY_DENIED")
            expiry = float(envelope.expires_at)
            if datetime.now(timezone.utc).timestamp() > expiry:
                raise Denied("STALE_MESSAGE")
            self._used_nonces.add(nonce_key)
            result = {"status": "ACCEPT", "promotion": "DENY", "message_id": envelope.message_id}
            self.audit.append({"event": "ACCEPT", "message_id": envelope.message_id, "corridor_id": envelope.corridor_id})
            return result
        except Denied as exc:
            self.audit.append({"event": "DENY", "message_id": envelope.message_id, "reason": str(exc)})
            raise


def default_gate() -> BrainGate:
    return BrainGate([
        Corridor(
            "DATA_EVIDENCE_EXPORT_V1",
            "XSMB_DATA",
            "BRAIN_GOVERNANCE",
            "L0_DATA",
            "L0_GOVERNANCE",
            "EVIDENCE_WRITE",
            False,
        ),
        Corridor(
            "GOVERNANCE_DECISION_READ_V1",
            "BRAIN_GOVERNANCE",
            "XSMB_BUILD_RUNTIME",
            "L0_GOVERNANCE",
            "L0_BUILD",
            "GOVERNANCE_READ",
            False,
        ),
    ])
