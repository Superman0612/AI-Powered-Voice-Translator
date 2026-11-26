from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Standard sync engine for FastAPI endpoints
db_uri = settings.SQLALCHEMY_DATABASE_URI
if "sqlite" in db_uri:
    import os
    clean_path = db_uri.replace("sqlite:////", "/").replace("sqlite:///", "")
    target_dir = os.path.dirname(clean_path)
    if target_dir:
        try:
            os.makedirs(target_dir, exist_ok=True)
        except Exception:
            pass
    engine = create_engine(
        db_uri,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        db_uri,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency that yields a database session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

