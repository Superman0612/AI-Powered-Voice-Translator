from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.language import Language
from app.schemas.language import LanguageResponse, LanguageDetectRequest, LanguageDetectResponse
from app.core.languages_config import SUPPORTED_LANGUAGES, get_language_by_code
from app.services.language_detection.service import lid_service

router = APIRouter()

@router.get("", response_model=List[LanguageResponse])
def list_supported_languages(db: Session = Depends(get_db)) -> Any:
    """Retrieve full catalog of supported Indian languages with capabilities."""
    langs = db.query(Language).order_by(Language.name).all()
    return langs

@router.get("/{code}", response_model=LanguageResponse)
def get_language_details(code: str, db: Session = Depends(get_db)) -> Any:
    """Get metadata and model mappings for a specific language code."""
    lang_cfg = get_language_by_code(code)
    if not lang_cfg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language '{code}' is not in the supported catalog."
        )
    lang = db.query(Language).filter(Language.code_iso_639_1 == lang_cfg.iso_639_1).first()
    return lang

@router.post("/detect", response_model=LanguageDetectResponse)
def detect_language(request: LanguageDetectRequest) -> Any:
    """
    Detect the language and script of input text using
    Unicode script boundary analysis, morphological heuristics, and n-gram models.
    """
    res = lid_service.detect_language(request.text)
    lang_cfg = get_language_by_code(res["detected_code"])

    supported_models = []
    if lang_cfg:
        supported_models = [
            f"ASR: {lang_cfg.whisper_code}",
            f"NMT: {lang_cfg.nllb_code}",
            f"TTS: {lang_cfg.mms_tts_code}"
        ]

    return {
        "detected_language": res["detected_code"],
        "language_name": res["language_name"],
        "script": res["script"],
        "confidence": res["confidence"],
        "is_supported": res["is_supported"],
        "supported_models": supported_models
    }

