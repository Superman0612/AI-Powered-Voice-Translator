from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.evaluation import ModelRegistry, EvaluationRun, EvaluationResult
from app.models.user import User
from app.schemas.evaluation import ModelRegistryResponse, EvaluationRunResponse, EvaluationResultResponse

router = APIRouter()

@router.get("/models", response_model=List[ModelRegistryResponse])
def get_registered_models(db: Session = Depends(get_db)) -> Any:
    """Lists all AI/ML models registered in the BhashaAI model registry."""
    models = db.query(ModelRegistry).all()
    return models

@router.get("/runs", response_model=List[EvaluationRunResponse])
def get_evaluation_runs(db: Session = Depends(get_db)) -> Any:
    """Lists past ML evaluation and benchmark runs."""
    runs = db.query(EvaluationRun).order_by(EvaluationRun.created_at.desc()).all()
    return runs

@router.get("/runs/{run_id}/results", response_model=List[EvaluationResultResponse])
def get_evaluation_results(run_id: str, db: Session = Depends(get_db)) -> Any:
    """Retrieves detailed WER, CER, BLEU, and chrF metrics for a specific benchmark run."""
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation run '{run_id}' not found."
        )
    return run.results

@router.get("/summary")
def get_evaluation_summary(db: Session = Depends(get_db)) -> Any:
    """Summarizes overall model benchmarks across ASR and NMT tasks."""
    total_models = db.query(ModelRegistry).count()
    total_runs = db.query(EvaluationRun).count()
    total_results = db.query(EvaluationResult).count()

    recent_results = db.query(EvaluationResult).order_by(EvaluationResult.created_at.desc()).limit(10).all()

    return {
        "total_registered_models": total_models,
        "total_evaluation_runs": total_runs,
        "total_evaluated_language_pairs": total_results,
        "recent_benchmarks": [
            {
                "language_pair": r.language_pair,
                "wer": r.metric_wer,
                "cer": r.metric_cer,
                "bleu": r.metric_bleu,
                "chrf": r.metric_chrf,
                "avg_latency_ms": r.avg_latency_ms,
                "sample_count": r.sample_count,
                "recorded_at": r.created_at
            }
            for r in recent_results
        ]
    }

