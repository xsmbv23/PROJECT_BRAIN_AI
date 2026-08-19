"""Single admission path for evaluating Forensic gates."""
from __future__ import annotations

from collections.abc import Sequence

from tools.gate_invariant import GateDefinition, GateResult, assert_gate_admitted


class BaseGate:
    """Gate implementation surface.

    Subclasses implement _evaluate. Callers must use GateRunner.run_gate; the
    private naming is intentional and the repository verifier checks for direct
    external calls.
    """

    definition: GateDefinition

    def _evaluate(self, history: Sequence[GateResult]) -> GateResult:
        raise NotImplementedError


class GateRunner:
    """Only authorized path for moving from one gate to the next."""

    def __init__(self, *, ttl_seconds: float = 300.0) -> None:
        self.ttl_seconds = ttl_seconds

    def run_gate(self, gate: BaseGate, history: Sequence[GateResult]) -> GateResult:
        assert_gate_admitted(gate.definition, history, ttl_seconds=self.ttl_seconds)
        result = gate._evaluate(history)
        if result.gate_id != gate.definition.gate_id:
            raise RuntimeError("DENY:GATE_ID_RESULT_MISMATCH")
        if result.status not in {"PASS", "FAIL", "UNKNOWN", "UNREACHED"}:
            raise RuntimeError("DENY:INVALID_GATE_STATUS")
        # The result must have fresh identity. A gate is not allowed to clone a
        # predecessor's evidence hash or cycle identity.
        if history and result.evidence_hash == history[-1].evidence_hash:
            raise RuntimeError("DENY:EVIDENCE_REUSE")
        if history and result.cycle_id != history[-1].cycle_id:
            raise RuntimeError("DENY:CYCLE_MISMATCH")
        return result
