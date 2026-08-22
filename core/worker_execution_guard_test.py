from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from worker_execution_guard import WorkerExecutionDenied, validate_execution_input


def test_exact_lineage_and_hash_pass(tmp_path: Path) -> None:
    artifact = tmp_path / "canonical.bin"
    artifact.write_bytes(b"canonical-data")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    execution = {
        "allocation_id": "A1",
        "cycle_id": "C1",
        "task_id": "T1",
        "task_type": "QUANT",
        "worker_id": "BOT2_QUANT",
        "input_artifact": "canonical.bin",
        "input_sha256": digest,
        "model_version": "MODEL_V1",
    }
    validate_execution_input(execution, execution, tmp_path)


def test_hash_mismatch_denies(tmp_path: Path) -> None:
    (tmp_path / "canonical.bin").write_bytes(b"canonical-data")
    execution = {
        "allocation_id": "A1",
        "cycle_id": "C1",
        "task_id": "T1",
        "task_type": "QUANT",
        "worker_id": "BOT2_QUANT",
        "input_artifact": "canonical.bin",
        "input_sha256": "0" * 64,
        "model_version": "MODEL_V1",
    }
    with pytest.raises(WorkerExecutionDenied):
        validate_execution_input(execution, execution, tmp_path)


def test_lineage_mismatch_denies(tmp_path: Path) -> None:
    artifact = tmp_path / "canonical.bin"
    artifact.write_bytes(b"canonical-data")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    allocation = {
        "allocation_id": "A1",
        "cycle_id": "C1",
        "task_id": "T1",
        "task_type": "QUANT",
        "worker_id": "BOT2_QUANT",
        "input_artifact": "canonical.bin",
        "input_sha256": digest,
        "model_version": "MODEL_V1",
    }
    execution = dict(allocation, cycle_id="C2")
    with pytest.raises(WorkerExecutionDenied):
        validate_execution_input(allocation, execution, tmp_path)
