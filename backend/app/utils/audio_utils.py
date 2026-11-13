import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

async def save_upload_audio(file: UploadFile) -> str:
    """Safely saves uploaded audio file to storage/audio/uploads/ directory."""
    ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".wav"
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid audio format '{ext}'. Allowed formats: {', '.join(settings.ALLOWED_AUDIO_EXTENSIONS)}"
        )

    unique_filename = f"upload_{uuid.uuid4()}{ext}"
    destination_path = os.path.join(settings.UPLOADS_DIR, unique_filename)

    file_size = 0
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    async with aiofiles.open(destination_path, "wb") as buffer:
        while chunk := await file.read(1024 * 64):  # 64 KB chunks
            file_size += len(chunk)
            if file_size > max_bytes:
                # Remove partially written file
                await buffer.close()
                if os.path.exists(destination_path):
                    os.remove(destination_path)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File exceeds maximum upload size limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
                )
            await buffer.write(chunk)

    if file_size == 0:
        if os.path.exists(destination_path):
            os.remove(destination_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty (0 bytes)."
        )

    return destination_path

