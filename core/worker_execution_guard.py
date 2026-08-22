"""Fail-closed guard for exact worker execution identity and input lineage."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


class WorkerExecutionDenied(ValueError):
    pass


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_execution_input(
    allocation: dict[str, Any],
    execution: dict[str, Any],
    artifact_root: Path,
) -> None:
    required = (
        "allocation_id",
        "cycle_id",
        "task_id",
        "task_type",
        "worker_id",
        "input_artifact",
        "input_sha256",
        "model_version",
    )
    for field in required:
        if not execution.get(field):
            raise WorkerExecutionDenied(f"missing execution field: {field}")

    for field in required:
        expected = allocation.get(field)
        if expected is not None and execution.get(field) != expected:
            raise WorkerExecutionDenied(f"lineage mismatch: {field}")

    if len(str(execution["input_sha256"])) != 64:
        raise WorkerExecutionDenied("input_sha256: expected SHA-256")

    root = artifact_root.resolve()
    candidate = (root / str(execution["input_artifact"])).resolve()
    if candidate != root and root not in candidate.parents:
        raise WorkerExecutionDenied("input_artifact: path escapes artifact root")
    if not candidate.is_file():
        raise WorkerExecutionDenied("input_artifact: file not found")

    actual = _sha256(candidate)
    if actual.lower() != str(execution["input_sha256"]).lower():
        raise WorkerExecutionDenied("input_sha256: artifact bytes do not match")
