# REALITY-N010 — Forensic Reality-Validation Lock

Current state: FOUNDATION STABLE / REALITY EVIDENCE INSUFFICIENT. This is a valid forensic state, not a broken pipeline.

## One admission chain

DB_EXISTENCE -> DB_BINDING -> SECRET_RESOLUTION -> DB_TLS_ADMISSION -> NETWORK_ORIGIN_PROOF -> DB_ROUND_TRIP -> PROMOTION

Rules: one FSM only; no shortcut; PASS is only a prerequisite; no PASS inheritance; UNKNOWN is not PASS; UNREACHED is not PASS; DEFAULT DENY.

## Receipt doctrine

RECEIPT_1 tests the system against reality. RECEIPT_2 tests repeatability. A receipt is an observation, not domain truth.

SINGLE_RECEIPT != DOMAIN_UNDERSTANDING
TWO_RECEIPTS != CANONICAL_TRUTH
VALID != TRUE
STRUCTURALLY_VALID != DOMAIN_TRUE
ROUNDTRIP_VALID != DOMAIN_UNDERSTANDING

No canonicalization from one observation.

## Current evidence

RECEIPT_1: ketqua16.net, HTTP 200, raw hash recorded, transport classification ROUNDTRIP_VALID, domain truth UNREACHED, no parsing/normalization/mapping.

RECEIPT_2: NOT_CAPTURED. Exact raw bytes plus complete transport metadata were not available through the current execution boundary. Never fabricate a hash.

## Next action

REALITY-N010-RECEIPT-2: capture the second receipt through the same source path and method; preserve raw bytes before parsing; hash SHA-256; persist compact metadata; compare only HTTP status, content type, final URL, raw byte count, SHA-256 and observed time; then STOP.

Forbidden in this action: parsing, 27-field extraction, normalization, business-date inference, domain mapping, cross-source merge, canonical schema, domain-truth claims.

If capture fails, the failure is valid forensic evidence and the system stops with the reason.

## Architecture

COLLECTION -> RAW RECEIPT -> TRANSPORT CLASSIFICATION -> STABILITY/VARIANCE/DRIFT -> QUORUM -> CANONICAL CONTRACT

Brain = governance/control plane. Chat = communication interface only. Data owns source truth. Quant Engine owns calculations. Sensors observe only. Layer 1 and staircase remain locked. Render Free 512 MB is a hard boundary; 320 MiB guard remains mandatory.

Successor rule: when the system is correct but reality has not supplied the next evidence, STOP rather than invent another hardening task.
