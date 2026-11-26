import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "BhashaAI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security & JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bhashaai_super_secret_jwt_key_2026_mca_project_secure_hash")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Storage Paths
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    STORAGE_DIR: str = os.path.join(BASE_DIR, "storage", "audio")
    UPLOADS_DIR: str = os.path.join(STORAGE_DIR, "uploads")
    GENERATED_DIR: str = os.path.join(STORAGE_DIR, "generated")

    # Database & Supabase Configuration
    DATABASE_URL: Optional[str] = None
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    SUPABASE_STORAGE_BUCKET: str = "bhashaai-audio"
    USE_POSTGRES: bool = False
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "bhashaai"
    POSTGRES_PORT: str = "5432"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        url = (self.DATABASE_URL or os.getenv("DATABASE_URL") or "").strip()
        if url:
            # Normalize Supabase / PostgreSQL URI for psycopg2
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+psycopg2://", 1)
            elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
                url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
            # Ensure sslmode=require for Supabase hosted connections
            if ("supabase.co" in url or "supabase.com" in url or "pooler.supabase.com" in url) and "sslmode" not in url:
                delimiter = "&" if "?" in url else "?"
                url = f"{url}{delimiter}sslmode=require"
            
            if url.startswith("postgresql"):
                return url
                
            # If it's a SQLite URL with a Windows drive (e.g. D:/...) on Linux (like Render):
            if "sqlite" in url:
                import platform
                if platform.system() != "Windows" and (":/" in url or ":\\" in url):
                    url = ""  # Discard invalid Windows drive path on Linux

        if url and url.startswith("sqlite"):
            # Check if specified SQLite path is writable
            raw_path = url.replace("sqlite:////", "/").replace("sqlite:///", "")
            target_dir = os.path.dirname(raw_path)
            if target_dir:
                try:
                    os.makedirs(target_dir, exist_ok=True)
                    test_f = os.path.join(target_dir, ".test_perm")
                    with open(test_f, "w") as f:
                        f.write("1")
                    os.remove(test_f)
                    return url
                except Exception:
                    pass
            else:
                return url

        if self.USE_POSTGRES:
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            
        # SQLite guaranteed writable fallback:
        # Check if BASE_DIR is writable (fails on Render Linux where src is read-only)
        candidate_dir = self.BASE_DIR
        try:
            os.makedirs(candidate_dir, exist_ok=True)
            test_file = os.path.join(candidate_dir, ".test_write_perm")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
        except Exception:
            import tempfile
            candidate_dir = tempfile.gettempdir()

        db_path = os.path.join(candidate_dir, "bhashaai.db").replace("\\", "/")
        if db_path.startswith("/"):
            return f"sqlite:////{db_path.lstrip('/')}"
        return f"sqlite:///{db_path}"
    
    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL and "sqlite" in self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Audio Constraints
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_AUDIO_EXTENSIONS: List[str] = [".wav", ".mp3", ".ogg", ".flac", ".m4a"]
    SAMPLE_RATE: int = 16000
    
    # AI/ML Configuration
    WHISPER_MODEL_NAME: str = os.getenv("WHISPER_MODEL_NAME", "openai/whisper-tiny")
    NMT_MODEL_NAME: str = os.getenv("NMT_MODEL_NAME", "facebook/nllb-200-distilled-600M")
    USE_GPU: bool = False
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = (
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")), ".env"),
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), ".env"),
            ".env"
        )
        extra = "allow"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
os.makedirs(settings.GENERATED_DIR, exist_ok=True)

