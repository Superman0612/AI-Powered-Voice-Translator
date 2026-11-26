"""
BhashaAI – AI-Powered Voice Translator for Indian Languages
FastAPI Application Entry Point & Core Gateway
"""

import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.router import api_router
from app.database.session import engine
from app.database.base import Base
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern lifespan event handler replacing deprecated @app.on_event('startup')
    and @app.on_event('shutdown').
    """
    import asyncio
    from app.database.init_db import init_db
    try:
        init_db()
        logger.info("Database schema and core seed catalogs verified at application startup.")
    except Exception as e:
        logger.warning(f"Database startup initialization notice: {e}")

    # Non-blocking async background warm-up of ASR to prevent first-request 502 timeout
    async def warmup_asr():
        try:
            from app.services.asr.service import asr_service
            logger.info("Background warming up ASR engine...")
            asr_service._get_pipeline()
            logger.info("ASR engine warm and ready.")
        except Exception as e:
            logger.warning(f"ASR warmup notice: {e}")

    asyncio.create_task(warmup_asr())
    yield

app = FastAPI(
    title="BhashaAI API",
    description="""
# BhashaAI – AI-Powered Voice Translator for Indian Languages
### MCA Final Year Project (AI & Machine Learning Specialization)

BhashaAI provides deep learning-based multilingual speech and neural machine translation 
for 10 scheduled Indian languages:
* Hindi (`hi`)
* English (`en`)
* Gujarati (`gu`)
* Marathi (`mr`)
* Bengali (`bn`)
* Tamil (`ta`)
* Telugu (`te`)
* Kannada (`kn`)
* Malayalam (`ml`)
* Punjabi (`pa`)

### AI/ML Capabilities:
* **ASR**: Automatic Speech Recognition using OpenAI Whisper Transformer.
* **LID**: Language Identification using Unicode character block boundaries and n-gram statistics.
* **NMT**: Neural Machine Translation using Meta NLLB-200 600M Seq2Seq model.
* **TTS**: Text-to-Speech using Facebook MMS-TTS (VITS) and high-fidelity cloud fallback.
* **Evaluation**: Automated WER, CER, BLEU, and chrF benchmark scoring.
    """,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

# CORS Middleware: Permissive configuration supporting Vercel deployments, localhost, and preview domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Global Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = round((time.perf_counter() - start_time) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(process_time)
    return response

# Mount API V1 Router (primary with prefix, secondary without prefix for flexible cloud deployments)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router)

# Global Exception Handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error processing {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred while processing the request.",
            "details": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else None
        }
    )

@app.get("/", tags=["Root"])
def root_status():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "documentation": "/docs",
        "health": f"{settings.API_V1_STR}/health",
        "description": "AI-Powered Voice Translator for Indian Languages"
    }

@app.get("/health", tags=["Root"])
def health_redirect():
    from app.api.v1.endpoints.health import health_check
    from app.database.session import SessionLocal
    db = SessionLocal()
    try:
        return health_check(db=db)
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
