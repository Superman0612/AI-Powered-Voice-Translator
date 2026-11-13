import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.core.config import settings
from app.core.security import get_password_hash, create_access_token
from app.models.user import User
from app.database.init_db import init_db

# Use test database or shared connection
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database tables and seed data exist."""
    init_db()

@pytest.fixture
def db_session():
    """Provides a fresh database session for a test."""
    from app.database.session import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    """FastAPI TestClient fixture."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(db_session):
    """Provides Authorization Bearer headers for the test student user."""
    user = db_session.query(User).filter(User.username == "mca_student").first()
    if not user:
        user = User(
            email="mca_test@bhashaai.org",
            username="mca_student",
            hashed_password=get_password_hash("Student@123"),
            full_name="MCA Researcher",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    token = create_access_token(user.id)
    return {"Authorization": f"Bearer {token}"}

