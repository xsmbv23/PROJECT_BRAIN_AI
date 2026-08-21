#!/usr/bin/env python3
"""Headless supervisor: observes workers, collects execution receipts, and reconciles them."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request,threading
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main'); BOT2=os.getenv('BOT2_URL','https://bot2-headless-worker.onrender.com'); BOT4=os.getenv('BOT4_URL','https://brain-bot4-worker.onrender.com'); POLL=int(os.getenv('POLL_SECONDS','60')); HEALTH_RETRIES=int(os.getenv('HEALTH_RETRIES','4')); RETRY_DELAY=float(os.getenv('HEALTH_RETRY_DELAY','2')); PORT=int(os.getenv('PORT','10000')); LAST={"status":"STARTING"}; RECEIPT={}
def get_json(url,path):
 r=urllib.request.Request(url.rstrip('/')+path,headers={'User-Agent':'brain-headless-orchestrator'}); return json.loads(urllib.request.urlopen(r,timeout=15).read().decode())
def get_raw(path):
 u=f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}'; r=urllib.request.Request(u,headers={'User-Agent':'brain-headless-orchestrator'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def health(url):
 last={"status":"UNREACHABLE","error":"UNKNOWN"}
 for attempt in range(1,HEALTH_RETRIES+1):
  try:
   value=get_json(url,'/health'); value['health_attempt']=attempt; return value
  except Exception as e:
   last={"status":"UNREACHABLE","error":type(e).__name__,"health_attempt":attempt}
   if attempt<HEALTH_RETRIES: time.sleep(RETRY_DELAY*attempt)
 return last
def result(url):
 try:return get_json(url,'/result')
 except Exception as e:return {"result":"HOLD","error":type(e).__name__}
def cycle():
 raw=get_raw('coordination/worker_allocation_v1.json'); outer=json.loads(raw); alloc=json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer; return alloc,hashlib.sha256(raw.encode()).hexdigest()
def tick():
 global LAST,RECEIPT
 alloc,alloc_sha=cycle(); h2=health(BOT2); h4=health(BOT4); r2=result(BOT2); r4=result(BOT4); now=datetime.now(timezone.utc).isoformat()
 health_ok=h2.get('status')=='ALLOCATION_OBSERVED' and h4.get('status')=='ALLOCATION_OBSERVED'; result_ok=r2.get('result')=='PASS' and r4.get('result')=='PASS'; identity_ok=all(x.get('allocation_id')==alloc.get('allocation_id') and x.get('cycle_id')==alloc.get('cycle_id') for x in (r2,r4)); overall='PASS' if health_ok and result_ok and identity_ok else 'HOLD'
 receipt={"schema":"headless-reconciliation-receipt/v1","receipt_type":"WORKER_RECONCILIATION","issued_at":now,"allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"allocation_sha256":alloc_sha,"bot2_result":r2,"bot4_result":r4,"checks":{"health":health_ok,"results":result_ok,"allocation_identity":identity_ok},"result":overall,"next_action":"BOT1_RECONCILE_AND_ALLOCATE_NEXT" if overall=='PASS' else "HOLD_AND_DIAGNOSE_WORKER_PATH","canonical_mutation":"BOT1_ONLY","promotion":"DENY","chat_session_execution":"CLOSED","execution_authority":"HEADLESS_WORKER"}
 receipt['receipt_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest(); RECEIPT=receipt; LAST={"schema":"headless-orchestrator/v2","observed_at":now,"allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"health_status":"PASS" if health_ok else "HOLD","result_status":overall,"next_action":receipt['next_action'],"promotion":"DENY"}; print(json.dumps(receipt,sort_keys=True),flush=True); print(json.dumps(LAST,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path in ('/health','/receipt'):
   b=json.dumps(LAST if self.path=='/health' else RECEIPT,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a):pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H)
 def loop():
  global LAST
  while True:
   try: tick()
   except Exception as e:
    LAST={"status":"SUPERVISOR_ERROR","error":type(e).__name__}; print(json.dumps(LAST,sort_keys=True),flush=True)
   time.sleep(POLL)
 threading.Thread(target=loop,daemon=True).start(); print(json.dumps({"status":"HTTP_READY","component":"HEADLESS_SUPERVISOR","port":PORT}),flush=True); s.serve_forever()
