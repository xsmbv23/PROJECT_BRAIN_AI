"""Fail-closed validator for worker runtime receipts.

This module validates evidence shape only. It never promotes state and never
turns a receipt into a PASS unless the receipt itself is structurally valid.
"""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED = {
    "receipt_type", "allocation_id", "cycle_id", "task_id", "worker_id",
    "input_artifact", "input_sha256", "model_version",
    "execution_started_at", "execution_finished_at", "status",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_receipt(receipt: dict[str, Any], base_dir: str | Path = ".") -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not REQUIRED.issubset(receipt):
        errors.append("missing_required_fields")
        return False, errors
    if receipt.get("receipt_type") != "WORKER_RUNTIME_RECEIPT":
        errors.append("invalid_receipt_type")
    if receipt.get("status") not in {"PASS", "FAIL", "BLOCKED"}:
        errors.append("invalid_status")
    try:
        start = datetime.fromisoformat(receipt["execution_started_at"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(receipt["execution_finished_at"].replace("Z", "+00:00"))
        if end < start:
            errors.append("execution_time_reversed")
    except (TypeError, ValueError):
        errors.append("invalid_execution_time")

    inp = Path(base_dir) / receipt["input_artifact"]
    if not inp.is_file():
        errors.append("input_artifact_missing")
    else:
        actual = _sha256(inp)
        if actual != receipt["input_sha256"]:
            errors.append("input_sha256_mismatch")

    if receipt["status"] == "PASS":
        if not receipt.get("output_artifact") or not receipt.get("output_sha256"):
            errors.append("pass_missing_output")
        else:
            out = Path(base_dir) / receipt["output_artifact"]
            if not out.is_file():
                errors.append("output_artifact_missing")
            elif _sha256(out) != receipt["output_sha256"]:
                errors.append("output_sha256_mismatch")
    if receipt["status"] == "FAIL" and not receipt.get("error_code"):
        errors.append("fail_missing_error_code")
    return not errors, errors


def validate_file(path: str | Path, base_dir: str | Path = ".") -> tuple[bool, list[str]]:
    with Path(path).open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, dict):
        return False, ["receipt_not_object"]
    return validate_receipt(payload, base_dir)
