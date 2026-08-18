from brain.server import Handler
from http.server import HTTPServer
import os

from tools.runtime_boot_gate import main as run_foundation_boot_gate


if __name__ == "__main__":
    if run_foundation_boot_gate() != 0:
        raise SystemExit("FOUNDATION_BOOT_GATE_DENY")
    print(f"FOUNDATION_BOOT_GATE_PASS commit={os.environ.get('RENDER_GIT_COMMIT', 'UNKNOWN')}", flush=True)

    # Durable DB proof is an explicit external action, never an automatic
    # privilege escalation from BOUND_TLS. It is enabled only by a temporary
    # Render Secret Environment flag and keeps promotion DENY even on success.
    if os.environ.get("FORENSIC_DB_ROUND_TRIP_ONCE") == "1":
        from tools.one_time_db_round_trip import run as run_db_round_trip
        if run_db_round_trip() != 0:
            raise SystemExit("FORENSIC_DB_ROUND_TRIP_DENY")

    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler).serve_forever()
