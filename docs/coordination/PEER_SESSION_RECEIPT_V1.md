# PEER SESSION RECEIPT V1

This document makes persistent artifacts the durable coordination channel between Bot 1 (Brain) and Bot 2 (Quant).

## Authority model

- Chat is a communication convenience channel.
- Persistent state is coordination state and the authority for gated actions.
- Contracts define allowed behavior.
- Evidence records factual basis.
- Gates define authority boundaries.

Therefore: **State > Chat for authority.** A chat acknowledgement never creates PASS evidence.

## Mandatory session sequence

1. READ_PEER
2. UNDERSTAND
3. ACKNOWLEDGE
4. AGREE / CHALLENGE / UNKNOWN
5. FIND_BLOCKER
6. ACT or SAFE_NOOP
7. WRITE_EVIDENCE
8. WRITE_PEER_NEXT_ACTION
9. WRITE_OWN_NEXT_ACTION

## Decision semantics

- AGREE: peer work is aligned with policy and evidence; state the concrete dependency enabled or clarified.
- CHALLENGE: peer work conflicts with policy, ownership, architecture, or evidence; record the conflict and correction request.
- UNKNOWN: evidence is insufficient; do not manufacture agreement or disagreement.

## Parallelism

Parallel work is allowed when mutation ownership and gate dependencies are separate. A locked Brain gate does not freeze unrelated safe Quant work. Parallel work can never unlock the Brain gate or inherit PASS.

## Forensic invariants

- PASS_IS_LOCAL
- PASS_IS_PREREQUISITE_ONLY
- NO_PASS_INHERITANCE
- OWN_GATE_EVIDENCE_REQUIRED
- FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
- UNKNOWN_IS_NOT_PASS
- DEFAULT_DENY
- PEER_ACK_IS_NOT_EVIDENCE
- PEER_PRAISE_IS_NOT_VERIFICATION

## Successor requirement

A future Bot must be able to reconstruct coordination from repository artifacts without access to chat history. If a technical decision, blocker, acknowledgement, challenge, or next action matters to the system, persist it.

Corrections are new append-only receipts; history is not rewritten to manufacture continuity.
