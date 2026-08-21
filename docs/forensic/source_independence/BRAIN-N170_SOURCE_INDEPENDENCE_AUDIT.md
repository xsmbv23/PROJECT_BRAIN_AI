# BRAIN-N170 — Source Independence Admission Audit

## Decision

`SOURCE_INDEPENDENCE = DENY`

This is a deliberate forensic decision. The quorum rule is NOT weakened merely because multiple hostnames publish matching XSMB tables.

## Observed sources

### Primary target A

`https://ketqua16.net/xo-so-mien-bac`

The site publishes XSMB result tables and explicitly describes itself as the current destination for the former Ketqua.net service. Its own site contains a July 2026 domain-change notice referring to the move to `ketqua16.net`.

### Identity source B

`https://www.xsmb.com.vn/`

The site publishes XSMB result tables with the same prize structure and historical result presentation.

### Preferred independent candidate C — official issuer source

`https://xosothudo.com.vn/`

This is the website identified by the Công ty TNHH một thành viên Xổ số Kiến thiết Thủ Đô as its own website and as a place where its lottery results can be viewed. The first-party company page identifies the company, website, headquarters, and its role in issuing Xổ số kiến thiết Miền Bắc. This gives substantially stronger ownership provenance than another generic result aggregator.

Automated collection is **not yet admitted** because the current evidence set has not established a complete technical automation permission/network-origin record. The source can be used as an external validation reference while the technical admission boundary is completed.

### Rejected/blocked candidate

`https://xskt.com.vn/`

Its published terms explicitly prohibit automated robots/spiders or automated collection without prior written permission. It therefore remains outside the production automated source set unless written permission is obtained.

## External evidence captured 2026-08-21

- ketqua16.net current XSMB page: current result tables observed. citeturn0search1turn0search2
- ketqua16.net domain-change notice: Ketqua.net announced the move to ketqua16.net in July 2026. citeturn1search1
- xsmb.com.vn current XSMB pages: current and historical result tables observed. citeturn1search10turn0search11
- xosothudo.com.vn first-party company page: the issuer identifies its own website and states that Xổ số kiến thiết Thủ Đô results are available there. citeturn7search0turn7search1
- xskt.com.vn technical evidence and terms remain recorded as a blocked automated candidate. citeturn4search0turn4search6

## Forensic interpretation

Hostname diversity is NOT ownership independence.

Two sites can publish identical tables and still derive from the same upstream result feed, operator, CDN, hosting group, or copied dataset.

Likewise, two different IP addresses do not by themselves prove independent ownership.

Therefore the current evidence is sufficient to say:

```text
RESULT_CONTENT_AVAILABLE       = YES
MULTIPLE_HOSTNAMES              = YES
OFFICIAL_ISSUER_PROVENANCE     = YES (xosothudo.com.vn)
CROSS-OWNER_TECHNICAL_PROOF    = NOT_COMPLETELY_PROVEN
AUTOMATED_SOURCE_C_ALLOWED     = NOT_YET_ADMITTED
CANONICAL_QUORUM                = DENY
```

## Advertising rule

Advertisements, affiliate blocks, navigation widgets, prediction articles, comments, promotional text, SMS offers, and unrelated embedded content are **non-truth content**.

They must never participate in:

- result parsing;
- source quorum;
- raw truth hash;
- semantic result hash;
- conflict resolution;
- canonical admission.

The scraper/parser may encounter advertisements, but the Forensic truth layer must classify them as `NON_TRUTH_CONTENT` and exclude them from the evidence object without modifying the original raw artifact.

## Immutable rule

Raw bytes remain immutable.

Filtering advertisements happens only in a derived interpretation layer:

```text
RAW_BYTES
   |
   +--> BYTE_SHA256 (immutable identity)
   |
   v
STRUCTURAL PARSER
   |
   +--> RESULT_FIELDS
   +--> NON_TRUTH_CONTENT
   +--> NAVIGATION
   +--> ADVERTISING
   |
   v
SEMANTIC HASH (derived meaning)
```

Never rewrite the raw artifact to remove ads.

## Gate result

```text
SOURCE_INDEPENDENCE = DENY
CANONICAL_QUORUM    = DENY
S1                  = LOCKED
S2                  = LOCKED
S3+                 = UNREACHED
```

This DENY is immutable history. A future Bot may add fresh evidence, but it must not edit this decision into PASS.

## Next action

`BRAIN-N171` — establish a permitted technical path to the official issuer source, capture fresh network-origin evidence, and perform a same-real-date comparison against `ketqua16.net` and `xsmb.com.vn`. If automated access is not explicitly admissible, keep the official source as validation-only and preserve `DENY` for automated canonical quorum.
