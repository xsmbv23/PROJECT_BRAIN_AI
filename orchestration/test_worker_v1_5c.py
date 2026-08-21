#!/usr/bin/env python3
"""Compatibility contract checks for the canonical BOT1 triple-worker path."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):
    v=json.loads(p.read_text(encoding='utf-8'))
    if isinstance(v,dict) and isinstance(v.get('content'),str): return json.loads(v['content'])
    return v
def main():
    m=load(ROOT/'coordination/worker_allocation_v2.json')
    assert m['issued_by']=='BOT1_LEAD' and m['authority']=='BOT1_ONLY'
    assert m['parallel'] is True
    assert m['shared_mutation']=='FORBIDDEN'
    assert m['canonical_state_mutation']=='BOT1_ONLY'
    assert m['promotion']=='DENY'
    assert set(m['workers'])=={'BOT2_QUANT','BOT3_REALITY','BOT4_EXECUTION'}
    assert set(m['active_workers'])==set(m['workers'])
    for wid,a in m['workers'].items():
        assert a['enabled'] is True
        assert a['write_scope'].startswith('coordination/inbox/')
        assert 'fresh' in a['deliverable'].lower()
    print('TRIPLE_WORKER_CONTRACT_PASS')
if __name__=='__main__': main()
