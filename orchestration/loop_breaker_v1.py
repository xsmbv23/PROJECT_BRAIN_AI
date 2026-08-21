#!/usr/bin/env python3
"""Prevent completed worker handoffs from being reprocessed in the same cycle."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUS=ROOT/'coordination'/'bus.jsonl'
TARGETS={'BOT2_QUANT','BOT4_EXECUTION'}

def main():
    done=set()
    if BUS.exists():
        for line in BUS.read_text(encoding='utf-8').splitlines():
            try: e=json.loads(line)
            except Exception: continue
            if e.get('worker_id') in TARGETS and e.get('status')=='HANDOFF_READY': done.add(e['worker_id'])
    locked=sorted(done)
    out={'schema':'loop-breaker/v1','locked_workers':locked,'rule':'DO_NOT_REACTIVATE_COMPLETED_HANDOFFS','bot3_focus':True,'promotion':'DENY'}
    print(json.dumps(out,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
