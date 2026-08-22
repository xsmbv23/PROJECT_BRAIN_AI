#!/usr/bin/env python3
"""Claim, execute and reconcile worker tasks without mutating canonical state."""
from __future__ import annotations

import hashlib
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path
from llm_provider import invoke

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "current_state.json"
NEXT = ROOT / "state" / "next_action.json"
OUTBOX = ROOT / "coordination" / "worker_outbox"
RESULTS = ROOT / "coordination" / "worker_results"
RECON = ROOT / "coordination" / "reconciliation"
WORKERS = tuple(x.strip() for x in os.environ.get("WORKERS", "BOT2_QUANT,BOT3_REALITY,BOT4_EXECUTION").split(",") if x.strip())

def now(): return datetime.now(timezone.utc).isoformat()
def unwrap(v):
    if isinstance(v, dict) and isinstance(v.get("content"), str):
        try: return json.loads(v["content"])
        except json.JSONDecodeError: pass
    return v
def load(p): return unwrap(json.loads(p.read_text(encoding="utf-8")))
def digest(v): return hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()
def append_jsonl(p, r):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f: f.write(json.dumps(r, sort_keys=True) + "\n")
def latest_result(p, task_id):
    if not p.exists(): return None
    found = None
    for line in p.read_text(encoding="utf-8").splitlines():
        try: r=json.loads(line)
        except json.JSONDecodeError: continue
        if r.get("task_id") == task_id: found=r
    return found
def prompt_for(task):
    return json.dumps({"worker_id":task.get("worker_id"),"role":task.get("role"),"objective":task.get("objective"),"task":task.get("task"),"deliverable":task.get("deliverable"),"authority":"execution-only; no canonical state mutation; no forensic promotion"}, sort_keys=True)
def execute(task):
    result=invoke(prompt_for(task))
    if result.get("status") == "LLM_COMPLETED":
        result.update({"reasoning_classification":"ADVISORY_ONLY","evidence_refs":[],"forensic_gate":"NONE","promotion":"DENY"})
    return result
def process(task_path, current_cycle):
    task=json.loads(task_path.read_text(encoding="utf-8")); worker=task.get("worker_id"); cycle=task.get("cycle_id"); task_id=task.get("task_id")
    if worker not in WORKERS: return None
    result_path=RESULTS/str(cycle)/f"{worker}.jsonl"
    if cycle != current_cycle: return {"status":"STALE_REJECTED","worker_id":worker,"cycle_id":cycle,"task_id":task_id,"reason":"task cycle differs from current canonical cycle","canonical_mutation":"FORBIDDEN"}
    prior=latest_result(result_path, task_id)
    if prior is not None: return {"status":"DUPLICATE_IGNORED","worker_id":worker,"cycle_id":cycle,"task_id":task_id,"lease_id":prior.get("lease_id")}
    lease=task.get("lease",{}); lease_id=lease.get("lease_id") or f"LEASE-{digest(task)[:20]}"; attempt=int(lease.get("attempt",1))
    append_jsonl(RESULTS/str(cycle)/f"{worker}.claims.jsonl", {"schema":"forensic-worker-claim/v2","recorded_at":now(),"worker_id":worker,"cycle_id":cycle,"task_id":task_id,"lease_id":lease_id,"attempt":attempt,"state":"CLAIMED","runner":socket.gethostname(),"task_sha256":digest(task)})
    result=execute(task)
    record={"schema":"forensic-worker-result/v4","recorded_at":now(),"worker_id":worker,"cycle_id":cycle,"task_id":task_id,"task_sha256":digest(task),"lease_id":lease_id,"attempt":attempt,"result":result,"evidence_refs":result.get("evidence_refs",[]),"canonical_mutation":"FORBIDDEN","forensic_gate":"NONE","promotion":"DENY"}
    append_jsonl(result_path,record); return record
def reconcile(cycle, results):
    active=[r for r in results if r.get("status") not in {"STALE_REJECTED","DUPLICATE_IGNORED"}]
    workers_observed=sorted({r.get("worker_id") for r in active if r.get("worker_id")}); missing=sorted(set(WORKERS)-set(workers_observed)); statuses=[r.get("result",{}).get("status") for r in active]
    if any(r.get("status")=="STALE_REJECTED" for r in results): decision,reason="HOLD","stale task/result detected"
    elif any(s in {"FAIL","CONFLICT"} for s in statuses): decision,reason="HOLD","blocking worker failure/conflict preserved"
    elif any(s=="BLOCKED_PROVIDER_NOT_CONFIGURED" for s in statuses): decision,reason="HOLD","background reasoning provider unavailable"
    elif len(workers_observed) >= 3 and not missing:
        decision,reason="REVIEW_REQUIRED","full three-worker reconciliation; BOT1 forensic synthesis required"
    elif len(workers_observed) == 2:
        decision,reason="PROVISIONAL","two-worker degraded reconciliation; missing worker recorded; S1 promotion remains denied"
    else:
        decision,reason="INSUFFICIENT_QUORUM","fewer than two worker results; operational deliberation quorum not met"
    return {"schema":"forensic-worker-reconciliation/v4","recorded_at":now(),"cycle_id":cycle,"worker_results":results,"workers_expected":list(WORKERS),"workers_observed":workers_observed,"missing_workers":missing,"worker_count":len(workers_observed),"decision":decision,"reason":reason,"minority_preserved":True,"canonical_next_action_mutation":"FORBIDDEN","promotion":"DENY"}
def main():
    current_state=load(STATE); current_next=load(NEXT); current_cycle=current_next.get("action_id","UNKNOWN-CYCLE")
    matrix_path=ROOT/"coordination"/"next_action_matrix_v1.json"
    if matrix_path.exists(): current_cycle=load(matrix_path).get("cycle_id",current_cycle)
    produced=[]
    if OUTBOX.exists():
        for cycle_dir in sorted(OUTBOX.iterdir()):
            if not cycle_dir.is_dir(): continue
            for worker in WORKERS:
                path=cycle_dir/f"{worker}.json"
                if path.exists():
                    result=process(path,current_cycle)
                    if result is not None: produced.append(result)
    ledger=reconcile(current_cycle,produced); ledger["canonical_state_digest"]=digest(current_state); ledger["canonical_next_action_digest"]=digest(current_next)
    append_jsonl(RECON/f"{current_cycle}.jsonl",ledger); print(json.dumps({"event":"RECONCILIATION",**ledger},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
