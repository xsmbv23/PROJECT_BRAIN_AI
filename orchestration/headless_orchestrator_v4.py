#!/usr/bin/env python3
"""V1.5D headless supervisor: active-worker health, result, identity and fail-closed reconciliation."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request,threading
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main')
BOT_URLS={'BOT2_QUANT':os.getenv('BOT2_URL','https://brain-bot2-worker-v2.onrender.com'),'BOT3_REALITY':os.getenv('BOT3_URL','https://brain-bot3-worker.onrender.com'),'BOT4_EXECUTION':os.getenv('BOT4_URL','https://brain-bot4-worker-v2.onrender.com')}
POLL=int(os.getenv('POLL_SECONDS','60')); RETRIES=int(os.getenv('HEALTH_RETRIES','3')); DELAY=float(os.getenv('HEALTH_RETRY_DELAY','2')); PORT=int(os.getenv('PORT','10000'))
LAST={'status':'STARTING'}; RECEIPT={}
def raw(path):
 r=urllib.request.Request(f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}',headers={'User-Agent':'brain-headless-orchestrator-v1.5d'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def get(url,path):
 r=urllib.request.Request(url.rstrip('/')+path,headers={'User-Agent':'brain-headless-orchestrator-v1.5d'}); return json.loads(urllib.request.urlopen(r,timeout=15).read().decode())
def probe(url,path):
 if not url:return {'status':'UNCONFIGURED'}
 last={'status':'UNREACHABLE'}
 for attempt in range(1,RETRIES+1):
  try:
   v=get(url,path); v['probe_attempt']=attempt; return v
  except Exception as e:
   last={'status':'UNREACHABLE','error':type(e).__name__,'probe_attempt':attempt}
   if attempt<RETRIES: time.sleep(DELAY*attempt)
 return last
def allocation():
 text=raw('coordination/worker_allocation_v2.json'); outer=json.loads(text); alloc=json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer
 active=alloc.get('active_workers') or [w for w,v in alloc.get('workers',{}).items() if v.get('enabled',True)]
 return alloc,active,hashlib.sha256(text.encode()).hexdigest()
def tick():
 global LAST,RECEIPT
 alloc,active,alloc_sha=allocation(); observations={}
 for wid in alloc.get('workers',{}):
  if wid not in active:
   observations[wid]={'status':'PAUSED','execution_required':False}; continue
  url=BOT_URLS.get(wid,''); observations[wid]={'health':probe(url,'/health'),'result':probe(url,'/result')}
 configured=all(BOT_URLS.get(w) for w in active)
 health_ok=configured and all(observations[w]['health'].get('status')=='ALLOCATION_OBSERVED' for w in active)
 result_ok=configured and all(observations[w]['result'].get('result')=='PASS' for w in active)
 identity_ok=configured and all(observations[w]['result'].get('allocation_id')==alloc.get('allocation_id') and observations[w]['result'].get('cycle_id')==alloc.get('cycle_id') for w in active)
 authority_ok=configured and all(observations[w]['result'].get('promotion')=='DENY' and observations[w]['result'].get('canonical_mutation')=='FORBIDDEN' for w in active)
 overall='PASS' if health_ok and result_ok and identity_ok and authority_ok else 'HOLD'
 now=datetime.now(timezone.utc).isoformat()
 receipt={'schema':'headless-reconciliation-receipt/v4','receipt_type':'ACTIVE_WORKER_RECONCILIATION','issued_at':now,'allocation_id':alloc.get('allocation_id'),'cycle_id':alloc.get('cycle_id'),'allocation_sha256':alloc_sha,'active_workers':active,'workers':observations,'checks':{'active_workers_configured':configured,'health':health_ok,'results':result_ok,'allocation_identity':identity_ok,'authority_boundary':authority_ok},'result':overall,'next_action':'BOT1_RECONCILE_AND_ALLOCATE_NEXT' if overall=='PASS' else 'HOLD_AND_DIAGNOSE_WORKER_PATH','canonical_mutation':'BOT1_ONLY','promotion':'DENY','chat_session_execution':'CLOSED','execution_authority':'HEADLESS_WORKER'}
 receipt['receipt_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest(); RECEIPT=receipt
 LAST={'schema':'headless-orchestrator/v1.5d','observed_at':now,'allocation_id':alloc.get('allocation_id'),'cycle_id':alloc.get('cycle_id'),'active_workers':active,'workers':observations,'health_status':'PASS' if health_ok else 'HOLD','result_status':overall,'next_action':receipt['next_action'],'promotion':'DENY','chat_session_execution':'CLOSED'}
 print(json.dumps(receipt,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path in ('/health','/receipt'):
   payload=LAST if self.path=='/health' else RECEIPT; b=json.dumps(payload,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a):pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H)
 def loop():
  while True:
   try: tick()
   except Exception as e:
    global LAST
    LAST={'status':'SUPERVISOR_ERROR','error':type(e).__name__}; print(json.dumps(LAST),flush=True)
   time.sleep(POLL)
 threading.Thread(target=loop,daemon=True).start(); s.serve_forever()
