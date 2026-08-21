# Recovery Backups

`backup/bot1-bot2-bot3-bot4-20260821` is a recovery snapshot of the multi-Bot orchestration state.

## Rule
`main` remains canonical. Backup branches are recovery snapshots only and never grant forensic promotion authority.

## What is preserved
- BOT1 autonomous governance context
- BOT2 Quant/Data role and handoff boundary
- BOT3 execution/reality role and reactivation state
- BOT4 execution/reality role and handoff boundary
- worker allocation protocol
- headless worker architecture
- critical forensic invariants
- recovery commit anchors

Before destructive migrations or architectural changes, create a new dated backup branch from `main`.
