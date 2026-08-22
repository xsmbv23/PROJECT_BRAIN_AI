"""Fail-closed binding between an S1 admission and its exact evidence set."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def canonical_manifest(manifest: dict[str, Any]) -> bytes:
    return json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_binding(binding: dict[str, Any], manifest: dict[str, Any], canonical_path: str | Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if binding.get("schema") != "s1-admission-binding/v1": errors.append("invalid_schema")
    if binding.get("status") != "PASS": errors.append("binding_not_pass")
    manifest_hash = sha256_bytes(canonical_manifest(manifest))
    if binding.get("evidence_manifest_sha256") != manifest_hash: errors.append("manifest_hash_mismatch")
    actual_canonical = sha256_file(canonical_path)
    if binding.get("canonical_sha256") != actual_canonical: errors.append("canonical_hash_mismatch")
    if manifest.get("canonical_sha256") != actual_canonical: errors.append("manifest_canonical_hash_mismatch")
    if manifest.get("cycle_id") != binding.get("cycle_id"): errors.append("cycle_id_mismatch")
    if manifest.get("business_date_start") != binding.get("business_date_start"): errors.append("start_date_mismatch")
    if manifest.get("business_date_end") != binding.get("business_date_end"): errors.append("end_date_mismatch")
    return not errors, errors
