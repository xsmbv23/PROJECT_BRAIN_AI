import hashlib
import json
from pathlib import Path

import pytest

from tools.s1_evidence_bridge import admit_s1_evidence


def test_bridge_rejects_wrong_canonical_hash(tmp_path: Path):
    p = tmp_path / "canonical.json"
    p.write_text('{"records":[]}', encoding="utf-8")
    manifest = {
        "cycle_id": "C1",
        "canonical_sha256": "0" * 64,
    }
    with pytest.raises(ValueError, match="S1_CANONICAL_HASH_MISMATCH"):
        admit_s1_evidence(
            cycle_id="C1",
            action_id="A1",
            commit_sha="c" * 40,
            deployment_id="D1",
            canonical_path=p,
            manifest=manifest,
        )


def test_bridge_rejects_cycle_mismatch(tmp_path: Path):
    p = tmp_path / "canonical.json"
    raw = b'{"records":[]}'
    p.write_bytes(raw)
    manifest = {
        "cycle_id": "C2",
        "canonical_sha256": hashlib.sha256(raw).hexdigest(),
    }
    with pytest.raises(ValueError, match="S1_CYCLE_MISMATCH"):
        admit_s1_evidence(
            cycle_id="C1",
            action_id="A1",
            commit_sha="c" * 40,
            deployment_id="D1",
            canonical_path=p,
            manifest=manifest,
        )
