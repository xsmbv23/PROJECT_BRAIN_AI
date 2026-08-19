"""Room 01 — DATA_ADMISSION.

This room admits an evidence-bearing source artifact into the Brain governance
plane. It does NOT declare canonical truth and does NOT unlock research.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

EXPECTED = (1, 1, 2, 6, 4, 6, 3, 4)
TOTAL = sum(EXPECTED)
DOMAIN_LENGTHS = [5] * 10 + [4] * 10 + [3] * 3 + [2] * 4


def _sha(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def admit_manifest(manifest: dict) -> dict:
    prizes = [str(x) for x in manifest.get("source_prizes", [])]
    lengths = [int(x) for x in manifest.get("semantic_lengths", [])]
    draw_date = manifest.get("source_row_date")
    source_count = int(manifest.get("source_count", 0))

    if manifest.get("fixture_status") != "VERIFICATION_ONLY":
        raise ValueError("ROOM01_SOURCE_STATUS_DENY")
    if len(prizes) != TOTAL:
        raise ValueError("ROOM01_CARDINALITY_DENY")
    if lengths != DOMAIN_LENGTHS:
        raise ValueError("ROOM01_DOMAIN_LENGTH_DENY")
    if not isinstance(draw_date, str):
        raise ValueError("ROOM01_DATE_DENY")
    try:
        d, m, y = map(int, draw_date.split("/"))
        parsed = date(y, m, d)
    except Exception as exc:
        raise ValueError("ROOM01_DATE_DENY") from exc
    if parsed > date.today():
        raise ValueError("ROOM01_FUTURE_DATE_DENY")

    tails = [p[-2:] for p in prizes]
    receipt = {
        "receipt_version": "ROOM01-DATA-ADMISSION-V1",
        "room": "ROOM_01_DATA_ADMISSION",
        "admission": "PASS",
        "fixture_id": manifest.get("fixture_id"),
        "source_file": manifest.get("source_file"),
        "source_file_sha256": manifest.get("source_file_sha256"),
        "fixture_payload_sha256": manifest.get("fixture_payload_sha256"),
        "draw_date": parsed.isoformat(),
        "full27_count": len(prizes),
        "domain_lengths": lengths,
        "tail27": tails,
        "tail_derivation": "source_prize[-2:]",
        "missing_day_policy": "UNKNOWN_GAP;NEVER_INFER_NON_DRAW",
        "source_count": source_count,
        "quorum_required": 2,
        "canonical_eligibility": "DENY_QUORUM_LT_2" if source_count < 2 else "ELIGIBLE_PENDING_RECONCILIATION",
        "research_admission": "LOCKED",
        "evidence_analysis": "LOCKED",
        "reporting": "LOCKED",
        "staircase": "LOCKED",
        "forensic": "INVARIANT",
    }
    receipt["receipt_sha256"] = _sha(receipt)
    return receipt


def load_manifest(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
