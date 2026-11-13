from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field

class TextTranslateRequest(BaseModel):
    source_text: str = Field(..., min_length=1)
    target_language: str = Field(..., description="Target ISO 639-1 code (e.g. 'hi', 'en', 'ta')")
    source_language: Optional[str] = Field(None, description="Optional source ISO 639-1 code. If omitted, auto-detected.")

class VoiceTranslateMetadata(BaseModel):
    target_language: str
    source_language: Optional[str] = None

class LatencyMetrics(BaseModel):
    asr_ms: float = 0.0
    nmt_ms: float = 0.0
    tts_ms: float = 0.0
    total_ms: float = 0.0

class TranslationResponse(BaseModel):
    id: str
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    detected_language: Optional[str] = None
    detection_confidence: Optional[float] = None
    input_audio_url: Optional[str] = None
    output_audio_url: Optional[str] = None
    latencies: LatencyMetrics
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

