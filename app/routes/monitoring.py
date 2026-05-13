from fastapi import APIRouter, Depends
from app.core.dependencies import require_admin
from app.core.logger import logger
import time
import os

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

# In-memory stats (populated by middleware in main.py)
stats = {
    "total_requests": 0,
    "total_errors": 0,
    "total_response_time_ms": 0,
    "recent_logs": []
}


def record_request(status_code: int, response_time_ms: float, log_line: str):
    """Called by middleware in main.py to update stats."""
    stats["total_requests"] += 1
    stats["total_response_time_ms"] += response_time_ms
    if status_code >= 400:
        stats["total_errors"] += 1
    stats["recent_logs"].append(log_line)
    if len(stats["recent_logs"]) > 100:
        stats["recent_logs"].pop(0)


@router.get("/stats")
def get_stats(current_user=Depends(require_admin)):
    total = stats["total_requests"]
    errors = stats["total_errors"]
    avg_time = round(stats["total_response_time_ms"] / total, 2) if total > 0 else 0
    error_rate = f"{round((errors / total) * 100, 1)}%" if total > 0 else "0.0%"

    return {
        "status": "Running",
        "total_requests": total,
        "total_errors": errors,
        "error_rate": error_rate,
        "avg_response_time_ms": avg_time,
    }


@router.get("/logs")
def get_logs(current_user=Depends(require_admin)):
    return {
        "recent_logs": stats["recent_logs"][-50:]
    }