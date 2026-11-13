from typing import Optional, List
from pydantic import BaseModel

class LanguageResponse(BaseModel):
    id: int
    code_iso_639_1: str
    code_iso_639_3: str
    name: str
    native_name: str
    script_name: str
    nllb_code: str
    indictrans_code: str
    whisper_code: str
    supports_asr: bool
    supports_nmt: bool
    supports_tts: bool

    class Config:
        from_attributes = True

class LanguageDetectRequest(BaseModel):
    text: str

class LanguageDetectResponse(BaseModel):
    detected_language: str
    language_name: str
    script: str
    confidence: float
    is_supported: bool
    supported_models: List[str]

