# BRAIN-N173 — External Corroboration Record

## Purpose

This record is an external research input for the N173 gate. It is NOT itself a PASS receipt and does not unlock S1.

## Candidate

`https://xosothudo.com.vn`

The current canonical state identifies this domain as the official issuer-validation candidate:

- role: `OFFICIAL_ISSUER_VALIDATION_CANDIDATE`
- automated collection: `NOT_YET_ADMITTED`

## External corroboration observed on 2026-08-21

Search evidence identifies the site as the website of `Công ty TNHH một thành viên Xổ số Kiến thiết Thủ đô`, a state-owned enterprise. The site's own notice says the official website is `xosothudo.com.vn` and identifies the company, responsible director, address, telephone and email.

Independent legal-directory evidence also maps the Hanoi municipal company to the same domain.

Historical infrastructure evidence reports the domain on IP `171.244.11.104` with VNN nameservers (`vnn.vn`) and Microsoft IIS. This is a historical/third-party technical clue only; it must not be promoted to exact-current network-origin PASS until the Render probe observes fresh RDAP/network evidence.

## Security interpretation

```text
OFFICIAL_ISSUER_PROVENANCE
        !=
NETWORK_ORIGIN_PROVEN
        !=
AUTOMATED_COLLECTION_ADMITTED
        !=
FRESH_RESULT_COMPARISON
        !=
S1_PASS
```

## Required exact-current bridge

1. Render exact-current runtime probes `xosothudo.com.vn`.
2. Network owner is observed through the bounded infrastructure probe.
3. Primary `ketqua16.net` and candidate have distinct observed network owners.
4. A lawful acquisition channel is explicitly admitted.
5. Fresh result evidence for the same draw/date is captured.
6. Raw bytes are hashed.
7. Result semantics are normalized without modifying the raw artifact.
8. Excel-vs-web comparison is performed.
9. Only after all S1 V2 requirements pass may canonical quorum be considered.

No step may infer the next step's PASS.

## Source links

- Official issuer website: https://xosothudo.com.vn/
- Official company notice: https://xosothudo.com.vn/tin/tin-tuc/7228/thong-bao-thay-doi-kenh-phat-song-truc-tiep-quay-so-mo-thuong-xo-so-kien-thiet.html
- Hanoi legal directory corroboration: https://thuviennhadat.vn/van-ban-phap-luat-viet-nam/quyet-dinh-3461-qd-ubnd-2023-bo-sung-quyet-dinh-2918-qd-ubnd-ma-dinh-danh-dien-tu-ha-noi-571782.html

## Decision

`NOT_PROVEN` for S1.

The record is evidence for the candidate selection only. The exact-current Render runtime remains the authority for technical admission.
