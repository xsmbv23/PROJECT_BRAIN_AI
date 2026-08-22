import hashlib
import json
from pathlib import Path
from core.s1_admission_binding import verify_binding, canonical_manifest


def test_binding_requires_exact_manifest_and_canonical(tmp_path: Path):
    canonical = tmp_path / "canonical.json"
    canonical.write_text('{"records":[{"business_date":"2026-08-20","full_27":["00"]}]}', encoding="utf-8")
    manifest = {
        "cycle_id":"C-S1-001",
        "business_date_start":"2026-08-20",
        "business_date_end":"2026-08-20",
        "canonical_sha256":hashlib.sha256(canonical.read_bytes()).hexdigest(),
    }
    binding = {
        "schema":"s1-admission-binding/v1","status":"PASS",
        "cycle_id":"C-S1-001","business_date_start":"2026-08-20","business_date_end":"2026-08-20",
        "evidence_manifest_sha256":hashlib.sha256(canonical_manifest(manifest)).hexdigest(),
        "canonical_sha256":manifest["canonical_sha256"],
        "verifier_version":"s1-verifier/v1","issued_at_utc":"2026-08-22T00:00:00+00:00"
    }
    assert verify_binding(binding, manifest, canonical) == (True, [])


def test_binding_rejects_tampered_canonical(tmp_path: Path):
    canonical = tmp_path / "canonical.json"
    canonical.write_text('{"records":[]}', encoding="utf-8")
    manifest = {"cycle_id":"C1","business_date_start":"2026-08-20","business_date_end":"2026-08-20","canonical_sha256":"0"*64}
    binding = {"schema":"s1-admission-binding/v1","status":"PASS","cycle_id":"C1","business_date_start":"2026-08-20","business_date_end":"2026-08-20","evidence_manifest_sha256":hashlib.sha256(canonical_manifest(manifest)).hexdigest(),"canonical_sha256":"0"*64,"verifier_version":"v1","issued_at_utc":"2026-08-22T00:00:00+00:00"}
    ok, errors = verify_binding(binding, manifest, canonical)
    assert not ok and "canonical_hash_mismatch" in errors
