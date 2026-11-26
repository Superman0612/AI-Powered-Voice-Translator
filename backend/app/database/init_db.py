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

        # 3. Seed Master Administrator User
        admin_email = "shubhamdevatwal2121@gmail.com"
        admin = db.query(User).filter(
            (User.email == admin_email) | (User.username == "Superman0612") | (User.username == "shubhamdevatwal")
        ).first()
        if not admin:
            admin = User(
                email=admin_email,
                username="Superman0612",
                hashed_password=get_password_hash("Shubham@404"),
                full_name="Shubham Devatwal",
                is_active=True,
                is_admin=True
            )
            db.add(admin)
            db.commit()
            logger.info("Master Admin user created (Superman0612 / shubhamdevatwal2121@gmail.com).")
        else:
            admin.email = admin_email
            admin.username = "Superman0612"
            admin.hashed_password = get_password_hash("Shubham@404")
            admin.is_admin = True
            db.commit()
            logger.info("Master Admin user updated (Superman0612 / shubhamdevatwal2121@gmail.com).")

        # 4. Seed Standard 'admin' user alias
        std_admin = db.query(User).filter((User.username == "admin") | (User.email == "admin@bhashaai.org")).first()
        if not std_admin:
            std_admin = User(
                email="admin@bhashaai.org",
                username="admin",
                hashed_password=get_password_hash("Shubham@404"),
                full_name="BhashaAI Administrator",
                is_active=True,
                is_admin=True
            )
            db.add(std_admin)
            db.commit()
            logger.info("Standard Admin account created (admin / Shubham@404).")
        else:
            std_admin.hashed_password = get_password_hash("Shubham@404")
            std_admin.is_admin = True
            db.commit()
            logger.info("Standard Admin account updated (admin / Shubham@404).")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during init_db: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

