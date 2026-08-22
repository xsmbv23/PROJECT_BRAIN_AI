import hashlib
import json
from pathlib import Path
from core.worker_runtime_receipt import validate_file


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_valid_pass_receipt(tmp_path: Path):
    inp = tmp_path / "input.bin"
    out = tmp_path / "output.json"
    inp.write_bytes(b"canonical-input")
    out.write_text('{"ok":true}', encoding="utf-8")
    receipt = {
        "receipt_type":"WORKER_RUNTIME_RECEIPT","allocation_id":"A1","cycle_id":"C1",
        "task_id":"T1","worker_id":"BOT2_QUANT","input_artifact":"input.bin",
        "input_sha256":_sha(inp),"model_version":"v1","execution_started_at":"2026-08-22T00:00:00+00:00",
        "execution_finished_at":"2026-08-22T00:01:00+00:00","status":"PASS",
        "output_artifact":"output.json","output_sha256":_sha(out)
    }
    p = tmp_path / "receipt.json"; p.write_text(json.dumps(receipt), encoding="utf-8")
    assert validate_file(p, tmp_path) == (True, [])


def test_reject_input_hash_mismatch(tmp_path: Path):
    inp = tmp_path / "input.bin"; inp.write_bytes(b"real")
    receipt = {
        "receipt_type":"WORKER_RUNTIME_RECEIPT","allocation_id":"A1","cycle_id":"C1",
        "task_id":"T1","worker_id":"BOT2_QUANT","input_artifact":"input.bin",
        "input_sha256":"0"*64,"model_version":"v1","execution_started_at":"2026-08-22T00:00:00+00:00",
        "execution_finished_at":"2026-08-22T00:01:00+00:00","status":"BLOCKED"
    }
    p = tmp_path / "receipt.json"; p.write_text(json.dumps(receipt), encoding="utf-8")
    ok, errors = validate_file(p, tmp_path)
    assert not ok and "input_sha256_mismatch" in errors
