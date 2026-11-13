from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    code_iso_639_1 = Column(String(10), unique=True, index=True, nullable=False)
    code_iso_639_3 = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    native_name = Column(String(100), nullable=False)
    script_name = Column(String(100), nullable=False)
    nllb_code = Column(String(50), nullable=False)
    indictrans_code = Column(String(50), nullable=False)
    whisper_code = Column(String(20), nullable=False)
    supports_asr = Column(Boolean, default=True, nullable=False)
    supports_nmt = Column(Boolean, default=True, nullable=False)
    supports_tts = Column(Boolean, default=True, nullable=False)

