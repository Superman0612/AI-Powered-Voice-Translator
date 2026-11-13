"""
Database Initialization & Seeding Script for BhashaAI
Creates schema and seeds initial data (Languages, Models, Admin User).
"""

import logging
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models import User, Language, ModelRegistry
from app.core.languages_config import SUPPORTED_LANGUAGES
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bhashaai.init_db")

def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")

    db = SessionLocal()
    try:
        # 1. Seed Languages
        logger.info("Checking and seeding language catalog...")
        for code, lang in SUPPORTED_LANGUAGES.items():
            existing = db.query(Language).filter(Language.code_iso_639_1 == code).first()
            if not existing:
                db_lang = Language(
                    code_iso_639_1=lang.iso_639_1,
                    code_iso_639_3=lang.iso_639_3,
                    name=lang.name,
                    native_name=lang.native_name,
                    script_name=lang.script,
                    nllb_code=lang.nllb_code,
                    indictrans_code=lang.indictrans_code,
                    whisper_code=lang.whisper_code,
                    supports_asr=lang.supports_asr,
                    supports_nmt=lang.supports_nmt,
                    supports_tts=lang.supports_tts,
                )
                db.add(db_lang)
        db.commit()
        logger.info("Languages verified/seeded.")

        # 2. Seed Model Registry
        models = [
            {
                "model_id": "openai/whisper-small",
                "task_type": "ASR",
                "architecture": "Encoder-Decoder Transformer",
                "parameter_count": "244M",
                "license": "MIT",
                "is_active": True
            },
            {
                "model_id": "openai/whisper-base",
                "task_type": "ASR",
                "architecture": "Encoder-Decoder Transformer",
                "parameter_count": "74M",
                "license": "MIT",
                "is_active": False
            },
            {
                "model_id": "facebook/nllb-200-distilled-600M",
                "task_type": "NMT",
                "architecture": "Shared Seq2Seq Transformer",
                "parameter_count": "600M",
                "license": "CC-BY-NC 4.0",
                "is_active": True
            },
            {
                "model_id": "ai4bharat/indictrans2-en-indic-dist-200M",
                "task_type": "NMT",
                "architecture": "Seq2Seq Transformer",
                "parameter_count": "200M",
                "license": "MIT",
                "is_active": False
            },
            {
                "model_id": "facebook/mms-tts",
                "task_type": "TTS",
                "architecture": "VITS (Variational Autoencoder + GAN)",
                "parameter_count": "36M per language",
                "license": "CC-BY-NC 4.0",
                "is_active": True
            },
            {
                "model_id": "gtts-neural-service",
                "task_type": "TTS",
                "architecture": "Google Neural WaveNet TTS (Cloud Fallback)",
                "parameter_count": "Cloud API",
                "license": "Cloud Fallback",
                "is_active": True
            },
            {
                "model_id": "langdetect-statistical-ngram",
                "task_type": "LID",
                "architecture": "N-gram Profile & Unicode Range Classifier",
                "parameter_count": "Heuristic Rule-based",
                "license": "Apache 2.0",
                "is_active": True
            }
        ]

        logger.info("Seeding Model Registry...")
        for m in models:
            reg = db.query(ModelRegistry).filter(ModelRegistry.model_id == m["model_id"]).first()
            if not reg:
                db.add(ModelRegistry(**m))
        db.commit()
        logger.info("Model Registry seeded.")

        # 3. Seed Default Test/Admin User
        admin_email = "admin@bhashaai.org"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                username="admin",
                hashed_password=get_password_hash("Admin@BhashaAI2026"),
                full_name="BhashaAI System Administrator",
                is_active=True,
                is_admin=True
            )
            db.add(admin)
            db.commit()
            logger.info("Admin user created (admin@bhashaai.org / Admin@BhashaAI2026).")
        
        # Test regular user
        test_email = "user@bhashaai.org"
        test_user = db.query(User).filter(User.email == test_email).first()
        if not test_user:
            test_user = User(
                email=test_email,
                username="mca_student",
                hashed_password=get_password_hash("Student@123"),
                full_name="MCA Researcher",
                is_active=True,
                is_admin=False
            )
            db.add(test_user)
            db.commit()
            logger.info("Student test user created (user@bhashaai.org / Student@123).")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during init_db: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

