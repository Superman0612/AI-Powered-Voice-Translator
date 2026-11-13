import os
import pytest
from app.services.tts.service import tts_service

def test_tts_empty_text_raises_error():
    with pytest.raises(ValueError) as excinfo:
        tts_service.synthesize_speech("", target_language="hi")
    assert "empty or whitespace" in str(excinfo.value)

def test_tts_unsupported_language_raises_error():
    with pytest.raises(ValueError) as excinfo:
        tts_service.synthesize_speech("Hello", target_language="klingon")
    assert "not supported" in str(excinfo.value)

def test_tts_synthesis_generation():
    # Test real synthesis with Hindi text
    res = tts_service.synthesize_speech(
        text="नमस्ते, यह परीक्षण है",
        target_language="hi",
        prefer_local=False  # test reliable synthesis pipeline
    )
    assert res["file_id"] is not None
    assert os.path.exists(res["file_path"])
    assert res["file_size_bytes"] > 0
    assert res["duration_seconds"] > 0.0
    assert res["language"] == "hi"

    # Cleanup generated test audio
    if os.path.exists(res["file_path"]):
        os.remove(res["file_path"])

