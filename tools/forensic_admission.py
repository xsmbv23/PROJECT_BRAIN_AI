"""Fail-closed admission helpers for the Brain foundation.

This module is deliberately small and dependency-free. It does not calculate
Expected Value; Quant Engine owns EV. Brain only admits or denies a downstream
action based on an explicit EV observation and an explicit graph edge.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Admission:
    allowed: bool
    reason: str


def admit_edge(source: str, target: str, observable_evidence: bool) -> Admission:
    if not source or not target:
        return Admission(False, "EDGE_ENDPOINT_MISSING")
    if not observable_evidence:
        return Admission(False, "EDGE_EVIDENCE_UNKNOWN")
    return Admission(True, "EDGE_ADMITTED")


def admit_ev(ev: float | int | None) -> Admission:
    if ev is None:
        return Admission(False, "EV_UNKNOWN")
    try:
        value = float(ev)
    except (TypeError, ValueError):
        return Admission(False, "EV_INVALID")
    if not math.isfinite(value):
        return Admission(False, "EV_NONFINITE")
    if value < 0.0:
        return Admission(False, "EV_NEGATIVE")
    return Admission(True, "EV_NONNEGATIVE")
