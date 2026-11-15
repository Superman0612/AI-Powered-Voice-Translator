"""
Supabase Integration Module for BhashaAI
Provides client initialization and optional storage helper for audio files.
"""

import logging
from typing import Optional
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger("bhashaai.supabase")

_supabase_client: Optional[Client] = None

def get_supabase_client() -> Optional[Client]:
    """Returns singleton Supabase client if configured in settings."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY
    if settings.SUPABASE_URL and key:
        try:
            _supabase_client = create_client(
                supabase_url=settings.SUPABASE_URL,
                supabase_key=key
            )
            logger.info("Supabase client initialized successfully.")
            return _supabase_client
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            return None
    return None

def is_supabase_configured() -> bool:
    """Checks if Supabase credentials or database URI are configured."""
    return bool(
        (settings.SUPABASE_URL and settings.SUPABASE_KEY) or
        ("supabase" in settings.SQLALCHEMY_DATABASE_URI.lower())
    )
