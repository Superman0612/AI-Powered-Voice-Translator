import io
import os
import pytest
import numpy as np
import soundfile as sf
from unittest.mock import patch, MagicMock

from app.services.pipeline import pipeline_orchestrator

@pytest.fixture
def dummy_audio_file(tmp_path):
    file_path = tmp_path / "voice_input.wav"
    sr = 16000
    # 1 second 440Hz sine wave
    t = np.linspace(0, 1.0, sr, endpoint=False)
    wave = (np.sin(2 * np.pi * 440 * t) * 0.8).astype(np.float32)
    sf.write(str(file_path), wave, sr)
    return str(file_path)

def test_pipeline_execution_with_mocks(dummy_audio_file, tmp_path):
    mock_audio_out = tmp_path / "mock_output.wav"
    mock_audio_out.write_bytes(b"RIFF....WAVEfmt ....data....")

    with patch("app.services.asr.service.asr_service.transcribe") as mock_asr, \
         patch("app.services.translation.service.nmt_service.translate") as mock_nmt, \
         patch("app.services.tts.service.tts_service.synthesize_speech") as mock_tts:

        mock_asr.return_value = {
            "text": "Hello, welcome to India",
            "language": "en",
            "confidence": 0.98,
            "duration_ms": 120.0,
            "audio_metadata": {"is_silent": False}
        }

        mock_nmt.return_value = {
            "source_text": "Hello, welcome to India",
            "translated_text": "नमस्ते, भारत में आपका स्वागत है",
            "source_language": "en",
            "target_language": "hi",
            "duration_ms": 85.0
        }

        mock_tts.return_value = {
            "file_id": "test-mock-tts-id",
            "filename": "mock_output.wav",
            "file_path": str(mock_audio_out),
            "file_size_bytes": 28,
            "duration_seconds": 1.5,
            "sample_rate": 16000,
            "engine_used": "facebook/mms-tts",
            "duration_ms": 150.0
        }

        result = pipeline_orchestrator.execute_voice_pipeline(
            audio_file_path=dummy_audio_file,
            target_language="hi",
            source_language_hint="en"
        )

        assert result["recognized_text"] == "Hello, welcome to India"
        assert result["translated_text"] == "नमस्ते, भारत में आपका स्वागत है"
        assert result["source_language"] == "en"
        assert result["target_language"] == "hi"
        assert result["generated_audio"] is not None
        assert result["latencies"]["total_ms"] > 0

def test_pipeline_unsupported_target_language(dummy_audio_file):
    with pytest.raises(Exception) as excinfo:
        pipeline_orchestrator.execute_voice_pipeline(
            audio_file_path=dummy_audio_file,
            target_language="unsupported_lang"
        )
    assert "not supported" in str(excinfo.value)
