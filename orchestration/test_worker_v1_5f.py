#!/usr/bin/env python3
"""V1.5F fail-closed headless execution contract."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 x=json.loads(p.read_text()); return json.loads(x['content']) if isinstance(x.get('content'),str) else x
def main():
 a=read(ROOT/'coordination/worker_allocation_v1.json')
 assert a['authority']=='BOT1_ONLY'
 assert a['canonical_state_mutation']=='BOT1_ONLY'
 assert a['promotion']=='DENY'
 assert a['parallel'] is True
 for wid,v in a['workers'].items():
  assert v['write_scope'] and wid in v['write_scope']
 print('V1.5F_EXECUTION_CONTRACT=PASS')
if __name__=='__main__': main()
