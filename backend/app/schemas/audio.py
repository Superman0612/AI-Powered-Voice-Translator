from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AudioFileResponse(BaseModel):
    id: str
    original_filename: str
    mime_type: str
    file_size_bytes: int
    duration_seconds: Optional[float] = None
    sample_rate: int
    channels: int
    created_at: datetime
    download_url: Optional[str] = None

    class Config:
        from_attributes = True

