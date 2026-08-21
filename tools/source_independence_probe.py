"""Bounded infrastructure comparison for source independence admission.

No credentials, no application actions, no bulk content. IPs are hashed.
Network ownership is queried through bounded RDAP metadata; absence of an
explicit owner signal is DENY. The candidate is the canonical first-party
issuer candidate selected by the current Forensic state. This proves only the
infrastructure leg; fresh result comparison remains a separate gate.
"""
from __future__ import annotations

import hashlib
import json
import socket
import ssl
import time
from dataclasses import asdict, dataclass
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

PRIMARY_SOURCE = "https://ketqua16.net"
IDENTITY_SOURCE_B = "https://xsmb.com.vn"
CANDIDATE_SOURCE_C = "https://xosothudo.com.vn"
DECLARED_SOURCES = (PRIMARY_SOURCE, IDENTITY_SOURCE_B, CANDIDATE_SOURCE_C)
RDAP_MAX_BYTES = 16_384


@dataclass(frozen=True)
class InfrastructureReceipt:
    requested_host: str
    resolved_ip_sha256_16: tuple[str, ...]
    tls_version: str | None
    tls_cipher: str | None
    certificate_subject: str | None
    certificate_issuer: str | None
    certificate_san_sha256_16: str | None
    server_hint: str | None
    network_owner: str
    network_owner_observed: bool
    decision: str
    reason: str
    transfer_ms: float


def _raw_addresses(host: str, port: int) -> list[str]:
    return sorted({item[4][0] for item in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)})


def _flatten_name(value) -> str | None:
    if not value:
        return None
    parts = []
    for section in value:
        for key, item in section:
            parts.append(f"{key}={item}")
    return ";".join(parts)[:512] or None


def _rdap_owner(ip: str, timeout: float = 5.0) -> str | None:
    req = Request(f"https://rdap.org/ip/{ip}", headers={"User-Agent": "XSMB-Forensic-IndependenceProbe/1.3", "Accept": "application/rdap+json"})
    with urlopen(req, timeout=timeout) as response:
        raw = response.read(RDAP_MAX_BYTES)
    doc = json.loads(raw.decode("utf-8", errors="ignore"))
    for key in ("name", "handle"):
        value = doc.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:256]
    for entity in doc.get("entities", [])[:8]:
        roles = entity.get("roles", [])
        if "registrant" in roles or "administrative" in roles:
            handle = entity.get("handle")
            if isinstance(handle, str) and handle.strip():
                return handle.strip()[:256]
    return None


def probe_infrastructure(url: str, timeout: float = 8.0) -> InfrastructureReceipt:
    parsed = urlsplit(url)
    started = time.perf_counter()
    host = parsed.hostname or ""
    port = parsed.port or 443
    ips_hash: tuple[str, ...] = ()
    tls_version = None
    tls_cipher = None
    subject = None
    issuer = None
    san_hash = None
    owner = None
    owner_observed = False
    try:
        ips = _raw_addresses(host, port)
        ips_hash = tuple(hashlib.sha256(ip.encode()).hexdigest()[:16] for ip in ips)
        if ips:
            try:
                owner = _rdap_owner(ips[0])
                owner_observed = bool(owner)
            except (OSError, ValueError, json.JSONDecodeError):
                owner = None
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as sock:
                tls_version = sock.version()
                cipher = sock.cipher()
                tls_cipher = cipher[0] if cipher else None
                cert = sock.getpeercert()
                subject = _flatten_name(cert.get("subject"))
                issuer = _flatten_name(cert.get("issuer"))
                sans = tuple(v for key, v in cert.get("subjectAltName", ()) if key == "DNS")
                san_hash = hashlib.sha256("|".join(sorted(sans)).encode()).hexdigest()[:16] if sans else None
        decision = "DENY"
        reason = "NETWORK_OWNER_NOT_OBSERVED" if not owner_observed else "INDEPENDENCE_REQUIRES_CROSS_OWNER_AND_FRESH_COMPARISON"
    except (OSError, ssl.SSLError, ValueError):
        decision = "DENY"
        reason = "INFRASTRUCTURE_METADATA_NOT_PROVEN"

    return InfrastructureReceipt(
        requested_host=host,
        resolved_ip_sha256_16=ips_hash,
        tls_version=tls_version,
        tls_cipher=tls_cipher,
        certificate_subject=subject,
        certificate_issuer=issuer,
        certificate_san_sha256_16=san_hash,
        server_hint=None,
        network_owner=owner or "NOT_OBSERVED",
        network_owner_observed=owner_observed,
        decision=decision,
        reason=reason,
        transfer_ms=round((time.perf_counter() - started) * 1000, 3),
    )


def run_probe() -> dict[str, object]:
    receipts = [asdict(probe_infrastructure(url)) for url in DECLARED_SOURCES]
    owners = {r["requested_host"]: r["network_owner"] for r in receipts if r["network_owner_observed"]}

    independent_pairs: list[dict[str, str]] = []
    primary_owner = owners.get(urlsplit(PRIMARY_SOURCE).hostname or "")
    if primary_owner:
        for url in (IDENTITY_SOURCE_B, CANDIDATE_SOURCE_C):
            host = urlsplit(url).hostname or ""
            owner = owners.get(host)
            if owner and owner != primary_owner:
                independent_pairs.append({"primary": PRIMARY_SOURCE, "independent": url, "primary_owner": primary_owner, "independent_owner": owner})

    independence = "PASS_LOCAL" if independent_pairs else "DENY"
    return {
        "probe": "BRAIN-N103_SOURCE_INDEPENDENCE_PROOF",
        "mode": "DATA_ADMISSION",
        "source_count": len(receipts),
        "primary_source": PRIMARY_SOURCE,
        "identity_source_b": IDENTITY_SOURCE_B,
        "candidate_source_c": CANDIDATE_SOURCE_C,
        "candidate_role": "OFFICIAL_ISSUER_VALIDATION_CANDIDATE",
        "receipts": receipts,
        "distinct_network_owners": len(set(owners.values())),
        "independent_pairs": independent_pairs,
        "independence": independence,
        "canonical_quorum": "PASS_LOCAL" if independence == "PASS_LOCAL" else "DENY",
        "promotion": "DENY",
        "policy": "HOSTNAME_DIFFERENCE_IS_NOT_INDEPENDENCE_PROOF;PRIMARY_PLUS_CROSS_OWNER_REQUIRED;FRESH_RESULT_COMPARISON_REQUIRED",
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), ensure_ascii=False, sort_keys=True))
