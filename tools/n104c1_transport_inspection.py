"""N104C.1 exact-current transport inspection.

Network access belongs to the collector layer. This one-shot probe fetches the
allowlisted source, streams the body in bounded chunks, then applies the
network-free transport classifier and a narrow official-result-panel detector.
It never admits candidates, never declares canonical truth, and never stores
credentials or bulk payloads.
"""
from __future__ import annotations

import hashlib
import json
import re
from urllib.request import Request, urlopen

from tools.network_evidence_collector import CHUNK_SIZE, collect
from tools.result_transport_probe import inspect_response

SOURCE = "https://ketqua16.net/"
MAX_CAPTURE_BYTES = 512 * 1024


def _bounded_capture(url: str) -> tuple[str, int, str, str]:
    request = Request(url, headers={"User-Agent": "XSMB-Forensic-EvidenceCollector/1.0"})
    digest = hashlib.sha256()
    chunks: list[bytes] = []
    total = 0
    with urlopen(request, timeout=20.0) as response:
        final_url = response.geturl()
        status = int(getattr(response, "status", 0) or 0)
        while total < MAX_CAPTURE_BYTES:
            chunk = response.read(min(CHUNK_SIZE, MAX_CAPTURE_BYTES - total))
            if not chunk:
                break
            digest.update(chunk)
            chunks.append(chunk)
            total += len(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace"), status, final_url, digest.hexdigest()


def _official_panel(html: str) -> dict[str, object]:
    # Narrow structural proof: a result-bearing table-like region containing
    # the official prize labels. Advertisement/side-panel text is not accepted.
    compact = re.sub(r"\s+", " ", html)
    match = re.search(
        r"Xổ số Truyền Thống.{0,30000}?Đặc biệt.{0,3000}?Giải nhất.{0,3000}?Giải nhì.{0,3000}?Giải ba.{0,3000}?Giải tư.{0,3000}?Giải năm.{0,3000}?Giải sáu.{0,3000}?Giải bảy",
        compact,
        re.I,
    )
    if not match:
        return {"proven": False, "reason": "OFFICIAL_RESULT_PANEL_NOT_IDENTIFIED"}
    snippet = match.group(0)
    return {
        "proven": True,
        "panel_marker_sha256": hashlib.sha256(snippet.encode("utf-8")).hexdigest(),
        "panel_snippet_bytes": len(snippet.encode("utf-8")),
        "numeric_token_count": len(re.findall(r"(?<!\d)\d{2,6}(?!\d)", snippet)),
        "advertisement_domain_excluded": True,
    }


def run() -> dict[str, object]:
    receipt = collect(SOURCE)
    html, status, final_url, bounded_hash = _bounded_capture(SOURCE)
    transport = inspect_response(html)
    panel = _official_panel(html)
    return {
        "action_id": "BRAIN-N104C.1",
        "source": SOURCE,
        "final_url": final_url,
        "network_origin": receipt.as_dict(),
        "transport": transport.__dict__,
        "bounded_capture_bytes": len(html.encode("utf-8")),
        "bounded_capture_sha256": bounded_hash,
        "official_result_panel": panel,
        "candidate_admission": "DENY",
        "excel_vs_web_match": "DENY",
        "canonical_quorum": "DENY",
        "truth_admission": "DENY",
        "completion": "PASS" if transport.status == "RAW_HTML_RESULT" and panel["proven"] else "DENY",
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, separators=(",", ":")), flush=True)
