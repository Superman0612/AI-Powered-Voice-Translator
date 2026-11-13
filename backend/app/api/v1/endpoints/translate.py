import os
import time
from typing import List, Optional, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user, get_current_user
from app.models.user import User
from app.models.translation import Translation
from app.models.audio import AudioFile
from app.schemas.translation import TextTranslateRequest, TranslationResponse, LatencyMetrics
from app.services.translation.service import nmt_service
from app.services.language_detection.service import lid_service
from app.services.pipeline import pipeline_orchestrator
from app.utils.audio_utils import save_upload_audio
from app.core.config import settings
from app.core.languages_config import get_language_by_code, SUPPORTED_LANGUAGES

router = APIRouter()

def _format_translation_response(t: Translation) -> Dict[str, Any]:
    input_url = f"/api/v1/audio/{t.input_audio_id}/download" if t.input_audio_id else None
    output_url = f"/api/v1/audio/{t.output_audio_id}/download" if t.output_audio_id else None

    return {
        "id": t.id,
        "source_text": t.source_text,
        "translated_text": t.translated_text,
        "source_language": t.source_lang_code,
        "target_language": t.target_lang_code,
        "detected_language": t.detected_language,
        "detection_confidence": t.detection_confidence,
        "input_audio_url": input_url,
        "output_audio_url": output_url,
        "latencies": {
            "asr_ms": t.asr_duration_ms,
            "nmt_ms": t.nmt_duration_ms,
            "tts_ms": t.tts_duration_ms,
            "total_ms": t.total_duration_ms
        },
        "status": t.status,
        "created_at": t.created_at
    }

@router.post("/text", response_model=TranslationResponse)
def translate_text(
    payload: TextTranslateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """Neural Machine Translation of text between Indian languages."""
    start_total = time.perf_counter()

    # Verify target language
    tgt_cfg = get_language_by_code(payload.target_language)
    if not tgt_cfg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Target language '{payload.target_language}' not supported. Supported: {list(SUPPORTED_LANGUAGES.keys())}"
        )

    # Detect source language if omitted
    detected_lang = None
    detection_conf = None
    src_lang = payload.source_language

    if not src_lang:
        lid_res = lid_service.detect_language(payload.source_text)
        detected_lang = lid_res["detected_code"]
        detection_conf = lid_res["confidence"]
        src_lang = detected_lang

    src_cfg = get_language_by_code(src_lang)
    if not src_cfg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Source language '{src_lang}' is not supported."
        )

    try:
        nmt_res = nmt_service.translate(
            text=payload.source_text,
            target_language=tgt_cfg.iso_639_1,
            source_language=src_cfg.iso_639_1
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation engine error: {str(e)}"
        )

    total_duration_ms = round((time.perf_counter() - start_total) * 1000, 2)

    # Persist translation record
    record = Translation(
        user_id=current_user.id if current_user else None,
        source_lang_code=src_cfg.iso_639_1,
        target_lang_code=tgt_cfg.iso_639_1,
        source_text=payload.source_text,
        translated_text=nmt_res["translated_text"],
        detected_language=detected_lang,
        detection_confidence=detection_conf,
        asr_duration_ms=0.0,
        nmt_duration_ms=nmt_res["duration_ms"],
        tts_duration_ms=0.0,
        total_duration_ms=total_duration_ms,
        status="completed"
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return _format_translation_response(record)

@router.post("/voice", response_model=TranslationResponse)
async def translate_voice(
    file: UploadFile = File(..., description="Speech audio file (wav, mp3, ogg, flac)"),
    target_language: str = Form(..., description="Target language code (e.g., 'hi', 'ta', 'bn')"),
    source_language: Optional[str] = Form(None, description="Optional source language code hint"),
    apply_denoise: bool = Form(False, description="Apply spectral noise reduction"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """
    End-to-End Voice Translation:
    Audio In -> Preprocessing -> ASR -> LID -> NMT -> TTS -> Audio Out
    """
    # 1. Save uploaded audio safely
    saved_path = await save_upload_audio(file)
    file_size = os.path.getsize(saved_path)

    # Create input audio DB record
    input_audio_rec = AudioFile(
        user_id=current_user.id if current_user else None,
        original_filename=file.filename or "uploaded_voice.wav",
        storage_path=saved_path,
        mime_type=file.content_type or "audio/wav",
        file_size_bytes=file_size,
        sample_rate=settings.SAMPLE_RATE,
        channels=1
    )
    db.add(input_audio_rec)
    db.commit()
    db.refresh(input_audio_rec)

    # 2. Execute full translation pipeline
    try:
        pipeline_result = pipeline_orchestrator.execute_voice_pipeline(
            audio_file_path=saved_path,
            target_language=target_language,
            source_language_hint=source_language,
            apply_denoise=apply_denoise
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice translation pipeline failure: {str(e)}"
        )

    # 3. Create output audio DB record if generated
    output_audio_rec = None
    gen_audio = pipeline_result.get("generated_audio")
    if gen_audio:
        output_audio_rec = AudioFile(
            user_id=current_user.id if current_user else None,
            original_filename=gen_audio["filename"],
            storage_path=gen_audio["file_path"],
            mime_type="audio/wav" if gen_audio["filename"].endswith(".wav") else "audio/mpeg",
            file_size_bytes=gen_audio["file_size_bytes"],
            duration_seconds=gen_audio["duration_seconds"],
            sample_rate=gen_audio["sample_rate"],
            channels=1
        )
        db.add(output_audio_rec)
        db.commit()
        db.refresh(output_audio_rec)

    # 4. Save Translation record
    latencies = pipeline_result["latencies"]
    translation_rec = Translation(
        user_id=current_user.id if current_user else None,
        source_lang_code=pipeline_result["source_language"],
        target_lang_code=pipeline_result["target_language"],
        source_text=pipeline_result["recognized_text"],
        translated_text=pipeline_result["translated_text"],
        detected_language=pipeline_result["detected_language"],
        detection_confidence=pipeline_result["detection_confidence"],
        input_audio_id=input_audio_rec.id,
        output_audio_id=output_audio_rec.id if output_audio_rec else None,
        asr_duration_ms=latencies["asr_ms"],
        nmt_duration_ms=latencies["nmt_ms"],
        tts_duration_ms=latencies["tts_ms"],
        total_duration_ms=latencies["total_ms"],
        status="completed"
    )
    db.add(translation_rec)
    db.commit()
    db.refresh(translation_rec)

    return _format_translation_response(translation_rec)

@router.get("/history", response_model=List[TranslationResponse])
def get_translation_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve translation history for authenticated user."""
    query = db.query(Translation).filter(Translation.user_id == current_user.id)
    translations = query.order_by(Translation.created_at.desc()).offset(skip).limit(limit).all()
    return [_format_translation_response(t) for t in translations]

@router.get("/{id}", response_model=TranslationResponse)
def get_translation_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """Retrieve specific translation record by ID."""
    t = db.query(Translation).filter(Translation.id == id).first()
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation record not found."
        )
    return _format_translation_response(t)

@router.delete("/{id}")
def delete_translation(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Delete a translation record and clean up its associated audio files."""
    t = db.query(Translation).filter(Translation.id == id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found.")

    if not current_user.is_admin and t.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    db.delete(t)
    db.commit()
    return {"status": "success", "message": f"Translation {id} deleted successfully."}
