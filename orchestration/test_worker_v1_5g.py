#!/usr/bin/env python3
"""V1.5G receipt/recovery contract."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=ROOT/'coordination'/'bus.jsonl'
 lines=p.read_text(encoding='utf-8').splitlines() if p.exists() else []
 records=[json.loads(x) for x in lines if x.strip()]
 handoffs=[r for r in records if r.get('status')=='HANDOFF_READY' or r.get('event')=='HANDOFF_READY']
 assert handoffs, 'HANDOFF_RECEIPT_MISSING'
 assert all(r.get('CHAT_SESSION_EXECUTION')=='CLOSED' for r in handoffs if 'CHAT_SESSION_EXECUTION' in r)
 # deterministic receipt identity check for append-only records
 for r in records:
  if r.get('receipt_id'):
   body=json.dumps({k:v for k,v in r.items() if k!='receipt_sha'},sort_keys=True,separators=(',',':'))
   expected=hashlib.sha256(body.encode()).hexdigest()
   if r.get('receipt_sha'): assert r['receipt_sha']==expected, 'RECEIPT_HASH_MISMATCH'
 print('V1.5G_RECEIPT_RECOVERY_CONTRACT=PASS')
if __name__=='__main__': main()
