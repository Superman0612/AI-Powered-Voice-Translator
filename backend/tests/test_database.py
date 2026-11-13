import uuid
from app.models.user import User
from app.models.language import Language
from app.models.translation import Translation
from app.models.audio import AudioFile
from app.models.evaluation import ModelRegistry

def test_language_catalog_seeded(db_session):
    languages = db_session.query(Language).all()
    assert len(languages) >= 10
    iso_codes = [l.code_iso_639_1 for l in languages]
    for required in ["hi", "en", "gu", "mr", "bn", "ta", "te", "kn", "ml", "pa"]:
        assert required in iso_codes

def test_model_registry_seeded(db_session):
    models = db_session.query(ModelRegistry).all()
    assert len(models) >= 4
    model_ids = [m.model_id for m in models]
    assert "openai/whisper-small" in model_ids
    assert "facebook/nllb-200-distilled-600M" in model_ids

def test_translation_record_creation(db_session):
    user = db_session.query(User).first()
    t = Translation(
        user_id=user.id,
        source_lang_code="en",
        target_lang_code="hi",
        source_text="Welcome to India",
        translated_text="भारत में आपका स्वागत है",
        detected_language="en",
        detection_confidence=0.99,
        asr_duration_ms=0.0,
        nmt_duration_ms=45.2,
        tts_duration_ms=0.0,
        total_duration_ms=45.2,
        status="completed"
    )
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)

    assert t.id is not None
    assert t.translated_text == "भारत में आपका स्वागत है"

    # Query back
    fetched = db_session.query(Translation).filter(Translation.id == t.id).first()
    assert fetched is not None
    assert fetched.user_id == user.id

    # Cleanup
    db_session.delete(fetched)
    db_session.commit()

