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

### Independent candidate C — not admitted for automated collection

`https://xskt.com.vn/`

This site publishes XSMB result tables and is technically observed on infrastructure distinct from the Cloudflare-fronted sources. However, its published terms explicitly prohibit automated robots/spiders or automated collection without prior written permission. Therefore it is a **validation candidate only**, not an automatically scraped production source unless lawful permission is obtained.

## External evidence captured 2026-08-21

- ketqua16.net current XSMB page: current result tables observed. citeturn0search1turn0search2
- ketqua16.net domain-change notice: Ketqua.net announced the move to ketqua16.net in July 2026. citeturn1search1
- xsmb.com.vn current XSMB pages: current and historical result tables observed. citeturn1search10turn0search11
- xskt.com.vn technical evidence: observed direct IPv4 `210.245.72.221` with Vietnam hosting; historical technical evidence also associates it with FPT infrastructure. citeturn4search0turn4search1
- xskt.com.vn terms: automated robots/spiders/automated collection are prohibited without prior written permission. citeturn4search6

## Forensic interpretation

Hostname diversity is NOT ownership independence.

Two sites can publish identical tables and still derive from the same upstream result feed, operator, CDN, hosting group, or copied dataset.

Likewise, two different IP addresses do not by themselves prove independent ownership.

Therefore the current evidence is sufficient to say:

```text
RESULT_CONTENT_AVAILABLE       = YES
MULTIPLE_HOSTNAMES              = YES
CROSS-OWNER_INDEPENDENCE        = NOT_PROVEN
AUTOMATED_SOURCE_C_ALLOWED      = NO (permission absent)
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

`BRAIN-N171` — establish an explicitly permitted independent-source path (preferably a source with independently provable ownership/upstream provenance) and run a fresh same-date comparison against `ketqua16.net` and `xsmb.com.vn`. If no lawful and independently attributable source is available, preserve `DENY` and move the architecture toward a manual/authorized evidence-ingestion boundary rather than scraping a prohibited source.
