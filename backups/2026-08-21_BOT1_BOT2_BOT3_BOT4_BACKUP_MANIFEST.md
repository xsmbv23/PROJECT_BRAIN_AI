# BOT1 / BOT2 / BOT3 / BOT4 Backup Manifest

Created: 2026-08-21
Backup branch: `backup/bot1-bot2-bot3-bot4-20260821`
Source: `main`

## Purpose
Preserve a recoverable project-state boundary for the multi-Bot governance and headless worker architecture.

## Authorities
- BOT1: canonical lead / next-action authority.
- BOT2: Quant/Data reviewer and forensic continuity.
- BOT3: independent execution/reality reviewer when active.
- BOT4: independent execution/reality worker.

## Critical invariants
- Deliberation != evidence.
- Consensus != PASS.
- UNKNOWN != PASS.
- Worker != forensic authority.
- Promotion remains BOT1/local-gate controlled.
- Canonical state mutation is BOT1 controlled.
- Minority/conflict evidence must be preserved.
- ChatGPT sessions are not execution authority after handoff.
- Headless workers use persistent coordination state.

## Recovery anchors
- Latest autonomous BOT1 governance commit: `b7a318291ea4c3e43d7ff064dbc087b936281a48`
- Latest Bot3 reactivation receipt: `b5f568ae498fd0b23c77a48da5892b6871969734`
- Headless supervisor health-routing fix: `093cc4f7527baa9426d9c38b5b357e2c699c3c4c`
- Earlier worker orchestration receipt boundary: `1b75504ca5aba19197c9b2da32262f5a6d34d95c` (Bot2)
- Earlier worker orchestration receipt boundary: `bbb9846259b63d74839369f82bd3a30db5f8ac37` (Bot4)

## Recovery rule
This branch is a recovery snapshot, not a second canonical state. `main` remains authoritative. No backup snapshot may itself grant promotion authority.
