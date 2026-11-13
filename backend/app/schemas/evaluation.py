from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class ModelRegistryResponse(BaseModel):
    id: int
    model_id: str
    task_type: str
    architecture: str
    parameter_count: str
    license: str
    is_active: bool
    registered_at: datetime

    class Config:
        from_attributes = True

class EvaluationResultResponse(BaseModel):
    id: str
    language_pair: str
    metric_wer: Optional[float] = None
    metric_cer: Optional[float] = None
    metric_bleu: Optional[float] = None
    metric_chrf: Optional[float] = None
    avg_latency_ms: float
    sample_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class EvaluationRunResponse(BaseModel):
    id: str
    run_name: str
    task_type: str
    dataset_name: str
    model_id: int
    created_at: datetime
    results: List[EvaluationResultResponse] = []

    class Config:
        from_attributes = True

