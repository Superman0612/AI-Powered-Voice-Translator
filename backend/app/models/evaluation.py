import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.base import Base

class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    model_id = Column(String(100), unique=True, nullable=False, index=True)
    task_type = Column(String(50), nullable=False)  # ASR, NMT, TTS, LID
    architecture = Column(String(100), nullable=False)
    parameter_count = Column(String(50), nullable=False)
    license = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    registered_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    evaluation_runs = relationship("EvaluationRun", back_populates="model")

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    run_name = Column(String(255), nullable=False)
    task_type = Column(String(50), nullable=False)
    dataset_name = Column(String(255), nullable=False)
    model_id = Column(Integer, ForeignKey("model_registry.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="evaluation_runs")
    model = relationship("ModelRegistry", back_populates="evaluation_runs")
    results = relationship("EvaluationResult", back_populates="run", cascade="all, delete-orphan")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    run_id = Column(String(36), ForeignKey("evaluation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    language_pair = Column(String(20), nullable=False)
    metric_wer = Column(Float, nullable=True)
    metric_cer = Column(Float, nullable=True)
    metric_bleu = Column(Float, nullable=True)
    metric_chrf = Column(Float, nullable=True)
    avg_latency_ms = Column(Float, nullable=False)
    sample_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    run = relationship("EvaluationRun", back_populates="results")

