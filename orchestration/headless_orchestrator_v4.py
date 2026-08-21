#!/usr/bin/env python3
"""Headless supervisor V4: BOT2/BOT3/BOT4 health, results and reconciliation."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request,threading
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main'); BOT2=os.getenv('BOT2_URL','https://bot2-headless-worker.onrender.com'); BOT3=os.getenv('BOT3_URL','https://brain-bot3-worker.onrender.com'); BOT4=os.getenv('BOT4_URL','https://brain-bot4-worker.onrender.com'); POLL=int(os.getenv('POLL_SECONDS','60')); PORT=int(os.getenv('PORT','10000')); LAST={"status":"STARTING"}; RECEIPT={}
def raw(path):
 r=urllib.request.Request(f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}',headers={'User-Agent':'brain-headless-orchestrator-v4'}); return r.read().decode() if False else urllib.request.urlopen(r,timeout=20).read().decode()
def get(url,path):
 r=urllib.request.Request(url.rstrip('/')+path,headers={'User-Agent':'brain-headless-orchestrator-v4'}); return json.loads(urllib.request.urlopen(r,timeout=15).read().decode())
def cycle():
 text=raw('coordination/worker_allocation_v2.json'); outer=json.loads(text); return (json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer),hashlib.sha256(text.encode()).hexdigest()
def observe(url):
 try:return get(url,'/health')
 except Exception as e:return {'status':'UNREACHABLE','error':type(e).__name__}
def result(url):
 try:return get(url,'/result')
 except Exception as e:return {'result':'HOLD','error':type(e).__name__}
def tick():
 global LAST,RECEIPT
 alloc,alloc_sha=cycle(); hs=[observe(x) for x in (BOT2,BOT3,BOT4)]; rs=[result(x) for x in (BOT2,BOT3,BOT4)]; now=datetime.now(timezone.utc).isoformat()
 health_ok=all(x.get('status')=='ALLOCATION_OBSERVED' for x in hs); result_ok=all(x.get('result')=='PASS' for x in rs); identity_ok=all(x.get('allocation_id')==alloc.get('allocation_id') and x.get('cycle_id')==alloc.get('cycle_id') for x in rs)
 receipt={'schema':'headless-reconciliation-receipt/v3','receipt_type':'THREE_WORKER_RECONCILIATION','issued_at':now,'allocation_id':alloc.get('allocation_id'),'cycle_id':alloc.get('cycle_id'),'allocation_sha256':alloc_sha,'workers':rs,'checks':{'health':health_ok,'results':result_ok,'allocation_identity':identity_ok,'chat_session_execution':'CLOSED'},'result':'PASS' if health_ok and result_ok and identity_ok else 'HOLD','next_action':'BOT1_RECONCILE_AND_ALLOCATE_NEXT' if health_ok and result_ok and identity_ok else 'HOLD_AND_DIAGNOSE_WORKER_PATH','canonical_mutation':'BOT1_ONLY','promotion':'DENY','execution_authority':'HEADLESS_WORKER'}
 receipt['receipt_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest(); RECEIPT=receipt; LAST={'schema':'headless-orchestrator/v4','observed_at':now,'allocation_id':alloc.get('allocation_id'),'cycle_id':alloc.get('cycle_id'),'health_status':'PASS' if health_ok else 'HOLD','result_status':receipt['result'],'next_action':receipt['next_action'],'promotion':'DENY'}; print(json.dumps(receipt,sort_keys=True),flush=True)
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
