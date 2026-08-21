#!/usr/bin/env python3
"""Headless supervisor: observes canonical allocation and all declared workers."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request,threading
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main')
BOT_URLS={'BOT2_QUANT':os.getenv('BOT2_URL','https://bot2-headless-worker.onrender.com'),'BOT3_REALITY':os.getenv('BOT3_URL',''),'BOT4_EXECUTION':os.getenv('BOT4_URL','https://brain-bot4-worker.onrender.com')}
POLL=int(os.getenv('POLL_SECONDS','60')); RETRIES=int(os.getenv('HEALTH_RETRIES','4')); DELAY=float(os.getenv('HEALTH_RETRY_DELAY','2')); PORT=int(os.getenv('PORT','10000')); LAST={'status':'STARTING'}; RECEIPT={}
def raw(path):
 r=urllib.request.Request(f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}',headers={'User-Agent':'brain-headless-orchestrator'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def get(url,path):
 r=urllib.request.Request(url.rstrip('/')+path,headers={'User-Agent':'brain-headless-orchestrator'}); return json.loads(urllib.request.urlopen(r,timeout=15).read().decode())
def probe(url,path):
 if not url:return {'status':'UNCONFIGURED'}
 last={'status':'UNREACHABLE'}
 for i in range(1,RETRIES+1):
  try:
   v=get(url,path); v['probe_attempt']=i; return v
  except Exception as e:
   last={'status':'UNREACHABLE','error':type(e).__name__,'probe_attempt':i}
   if i<RETRIES:time.sleep(DELAY*i)
 return last
def alloc():
 r=raw('coordination/worker_allocation_v2.json'); o=json.loads(r); return (json.loads(o['content']) if isinstance(o.get('content'),str) else o),hashlib.sha256(r.encode()).hexdigest()
def prior():
 try:return json.loads(raw('coordination/worker_runtime_receipt.json'))
 except Exception:return {}
def tick():
 global LAST,RECEIPT
 a,ash=alloc(); obs={}
 for wid in a.get('workers',{}):obs[wid]={'health':probe(BOT_URLS.get(wid),'/health'),'result':probe(BOT_URLS.get(wid),'/result')}
 configured=all(BOT_URLS.get(wid) for wid in a.get('workers',{}))
 health_ok=configured and all(x['health'].get('status')=='ALLOCATION_OBSERVED' for x in obs.values())
 result_ok=configured and all(x['result'].get('result')=='PASS' for x in obs.values())
 identity_ok=configured and all(x['result'].get('allocation_id')==a.get('allocation_id') and x['result'].get('cycle_id')==a.get('cycle_id') for x in obs.values())
 p=prior(); prior_ok=p.get('result')=='PASS' and p.get('allocation_id')==a.get('allocation_id') and p.get('cycle_id')==a.get('cycle_id') and bool(p.get('receipt_sha256'))
 overall='PASS' if health_ok and result_ok and identity_ok and prior_ok else 'HOLD'; now=datetime.now(timezone.utc).isoformat()
 r={'schema':'headless-reconciliation-receipt/v4','receipt_type':'WORKER_RECONCILIATION','issued_at':now,'allocation_id':a.get('allocation_id'),'cycle_id':a.get('cycle_id'),'allocation_sha256':ash,'workers':obs,'checks':{'declared_workers_configured':configured,'health':health_ok,'results':result_ok,'allocation_identity':identity_ok,'prior_receipt_anchor':prior_ok},'result':overall,'next_action':'BOT1_RECONCILE_AND_ALLOCATE_NEXT' if overall=='PASS' else 'HOLD_AND_DIAGNOSE_WORKER_PATH','canonical_mutation':'BOT1_ONLY','promotion':'DENY','chat_session_execution':'CLOSED','execution_authority':'HEADLESS_WORKER'}
 r['receipt_sha256']=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest(); RECEIPT=r; LAST={'schema':'headless-orchestrator/v5','observed_at':now,'allocation_id':a.get('allocation_id'),'cycle_id':a.get('cycle_id'),'workers':obs,'health_status':'PASS' if health_ok else 'HOLD','result_status':overall,'next_action':r['next_action'],'promotion':'DENY'}; print(json.dumps(LAST,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path in ('/health','/receipt'):
   b=json.dumps(LAST if self.path=='/health' else RECEIPT,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a):pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H)
 def loop():
  while True:
   try:tick()
   except Exception as e:print(json.dumps({'status':'SUPERVISOR_ERROR','error':type(e).__name__}),flush=True)
   time.sleep(POLL)
 threading.Thread(target=loop,daemon=True).start(); s.serve_forever()
