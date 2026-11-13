import os
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user, get_current_user
from app.models.user import User
from app.models.audio import AudioFile
from app.schemas.audio import AudioFileResponse
from app.utils.audio_utils import save_upload_audio
from app.services.asr.audio_processor import AudioProcessor
from app.core.config import settings

router = APIRouter()

@router.post("/upload", response_model=AudioFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_audio_file(
    file: UploadFile = File(..., description="Audio file to upload (wav, mp3, ogg, flac)"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Any:
    """Uploads, validates, and stores an audio file."""
    saved_path = await save_upload_audio(file)
    file_size = os.path.getsize(saved_path)

    # Validate audio DSP properties
    try:
        raw, sr = AudioProcessor.load_audio(saved_path)
        duration_sec = round(len(raw) / float(sr), 2)
        channels = 2 if raw.ndim > 1 else 1
    except Exception:
        duration_sec = None
        sr = 16000
        channels = 1

    audio_rec = AudioFile(
        user_id=current_user.id if current_user else None,
        original_filename=file.filename or "uploaded_audio.wav",
        storage_path=saved_path,
        mime_type=file.content_type or "audio/wav",
        file_size_bytes=file_size,
        duration_seconds=duration_sec,
        sample_rate=sr,
        channels=channels
    )
    db.add(audio_rec)
    db.commit()
    db.refresh(audio_rec)

    return {
        "id": audio_rec.id,
        "original_filename": audio_rec.original_filename,
        "mime_type": audio_rec.mime_type,
        "file_size_bytes": audio_rec.file_size_bytes,
        "duration_seconds": audio_rec.duration_seconds,
        "sample_rate": audio_rec.sample_rate,
        "channels": audio_rec.channels,
        "created_at": audio_rec.created_at,
        "download_url": f"/api/v1/audio/{audio_rec.id}/download"
    }

@router.get("/{id}", response_model=AudioFileResponse)
def get_audio_metadata(id: str, db: Session = Depends(get_db)) -> Any:
    """Retrieve metadata of a stored audio file."""
    audio_rec = db.query(AudioFile).filter(AudioFile.id == id).first()
    if not audio_rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio record not found."
        )

    return {
        "id": audio_rec.id,
        "original_filename": audio_rec.original_filename,
        "mime_type": audio_rec.mime_type,
        "file_size_bytes": audio_rec.file_size_bytes,
        "duration_seconds": audio_rec.duration_seconds,
        "sample_rate": audio_rec.sample_rate,
        "channels": audio_rec.channels,
        "created_at": audio_rec.created_at,
        "download_url": f"/api/v1/audio/{audio_rec.id}/download"
    }

@router.get("/{id}/download")
def download_audio_file(id: str, db: Session = Depends(get_db)) -> Any:
    """Download audio file with appropriate streaming headers."""
    audio_rec = db.query(AudioFile).filter(AudioFile.id == id).first()
    if not audio_rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file does not exist on storage vault."
        )

    storage_path = str(audio_rec.storage_path)
    if not os.path.exists(storage_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file does not exist on storage vault."
        )

    media_type = str(audio_rec.mime_type) if audio_rec.mime_type else "audio/wav"
    download_filename = str(audio_rec.original_filename) if audio_rec.original_filename else "audio.wav"

    return FileResponse(
        path=storage_path,
        media_type=media_type,
        filename=download_filename
    )

