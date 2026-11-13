import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.base import Base

class Translation(Base):
    __tablename__ = "translations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    source_lang_code = Column(String(10), nullable=False, index=True)
    target_lang_code = Column(String(10), nullable=False, index=True)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    detected_language = Column(String(10), nullable=True)
    detection_confidence = Column(Float, nullable=True)
    
    input_audio_id = Column(String(36), ForeignKey("audio_files.id", ondelete="SET NULL"), nullable=True)
    output_audio_id = Column(String(36), ForeignKey("audio_files.id", ondelete="SET NULL"), nullable=True)
    
    asr_duration_ms = Column(Float, default=0.0, nullable=False)
    nmt_duration_ms = Column(Float, default=0.0, nullable=False)
    tts_duration_ms = Column(Float, default=0.0, nullable=False)
    total_duration_ms = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), default="completed", nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="translations")
    input_audio = relationship("AudioFile", foreign_keys=[input_audio_id])
    output_audio = relationship("AudioFile", foreign_keys=[output_audio_id])

    __table_args__ = (
        Index("idx_translations_user_created", "user_id", "created_at"),
    )

