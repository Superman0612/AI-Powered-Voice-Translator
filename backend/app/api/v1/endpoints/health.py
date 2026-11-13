import os
import psutil
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db
from app.core.config import settings

router = APIRouter()

@router.get("")
def health_check(db: Session = Depends(get_db)) -> Any:
    """Full system diagnostics: Database, CPU, Memory, and AI Models."""
    # Check Database Connectivity
    db_status = "unhealthy"
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy ({str(e)})"

    # Memory and CPU stats
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\" if os.name == "nt" else "/")

    return {
        "status": "operational",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": {
            "status": db_status,
            "engine": "PostgreSQL 18"
        },
        "system": {
            "cpu_cores": os.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "ram_total_mb": round(mem.total / (1024 * 1024), 2),
            "ram_available_mb": round(mem.available / (1024 * 1024), 2),
            "ram_percent_used": mem.percent,
            "disk_free_gb": round(disk.free / (1024 * 1024 * 1024), 2)
        },
        "ai_models_configured": {
            "asr_model": settings.WHISPER_MODEL_NAME,
            "nmt_model": settings.NMT_MODEL_NAME,
            "tts_engine": "facebook/mms-tts + gtts fallback",
            "lid_engine": "langdetect + Unicode heuristic classifier"
        }
    }

