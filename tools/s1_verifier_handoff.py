"""Independent S1 verifier handoff.

The verifier is deliberately separate from BOT3. A worker review can be PASS
while this handoff remains DENY. Only an independently validated canonical
artifact may enter durable evidence persistence.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.s1_evidence_bridge import admit_s1_evidence


def verify_and_persist_s1(*, verifier_result: str, cycle_id: str, action_id: str,
                          commit_sha: str, deployment_id: str,
                          canonical_path: str | Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if verifier_result != "PASS":
        return {"s1_admission": "DENY", "reason": "INDEPENDENT_VERIFIER_NOT_PASS"}
    return admit_s1_evidence(
        cycle_id=cycle_id,
        action_id=action_id,
        commit_sha=commit_sha,
        deployment_id=deployment_id,
        canonical_path=canonical_path,
        manifest=manifest,
    )
