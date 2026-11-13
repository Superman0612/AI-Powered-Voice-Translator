from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    languages,
    translate,
    audio,
    evaluation,
    health
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(languages.router, prefix="/languages", tags=["Languages"])
api_router.include_router(translate.router, prefix="/translate", tags=["Translation"])
api_router.include_router(audio.router, prefix="/audio", tags=["Audio Management"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["ML Evaluation & Benchmarking"])
api_router.include_router(health.router, prefix="/health", tags=["Health & Diagnostics"])

