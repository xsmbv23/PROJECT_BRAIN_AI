"""Deterministic, dataset-free classifier for result transport discovery.

N104C must identify *how* a source exposes result data before any candidate is
admitted. This module never performs network access and never creates a
candidate. It only classifies supplied raw response text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class TransportEvidence:
    raw_html_result: bool
    embedded_json: bool
    js_generated_hint: bool
    secondary_endpoint_hint: bool
    candidate_numbers: int
    status: str


def inspect_response(raw: str) -> TransportEvidence:
    text = raw or ""
    lower = text.lower()
    numbers = re.findall(r"(?<!\d)\d{2,6}(?!\d)", text)

    raw_html_result = bool(
        re.search(r"<(?:td|span|div|li)[^>]*>\s*\d{2,6}\s*</", text, re.I)
    )
    embedded_json = bool(
        re.search(r"(?:application/json|__next_data__|window\.__|\"(?:result|results|draw|db)\")", text, re.I)
    )
    js_generated_hint = bool(
        re.search(r"(?:fetch\(|XMLHttpRequest|axios|jquery|\.ajax\(|document\.createElement|innerHTML)", text, re.I)
    )
    secondary_endpoint_hint = bool(
        re.search(r"(?:/api/|/ajax/|/data/|\.json(?:\?|\"|')|\.php\?(?:[^\"']*))(?:[^\s<]+)", text, re.I)
    )

    if raw_html_result:
        status = "RAW_HTML_RESULT"
    elif embedded_json:
        status = "EMBEDDED_JSON"
    elif js_generated_hint or secondary_endpoint_hint:
        status = "SECONDARY_TRANSPORT_HINT"
    else:
        status = "NO_RESULT_TRANSPORT_PROVEN"

    return TransportEvidence(
        raw_html_result=raw_html_result,
        embedded_json=embedded_json,
        js_generated_hint=js_generated_hint,
        secondary_endpoint_hint=secondary_endpoint_hint,
        candidate_numbers=len(numbers) if status != "NO_RESULT_TRANSPORT_PROVEN" else 0,
        status=status,
    )


def classify(raw: str) -> dict[str, object]:
    return asdict(inspect_response(raw))
