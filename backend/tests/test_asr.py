import os
import pytest
import numpy as np
import soundfile as sf
from unittest.mock import MagicMock, patch

from app.services.asr.audio_processor import AudioProcessor, AudioProcessingError
from app.services.asr.service import ASRService

@pytest.fixture
def sample_wav_file(tmp_path):
    """Generates a synthetic 1-second 44.1kHz stereo WAV file for testing."""
    file_path = tmp_path / "test_stereo.wav"
    sr = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # Sine wave tone
    tone1 = np.sin(2 * np.pi * 440 * t)
    tone2 = np.sin(2 * np.pi * 880 * t)
    stereo = np.column_stack([tone1, tone2]).astype(np.float32)

    sf.write(str(file_path), stereo, sr)
    return str(file_path)

@pytest.fixture
def silent_wav_file(tmp_path):
    """Generates a synthetic 1-second pure silent WAV file."""
    file_path = tmp_path / "test_silent.wav"
    sr = 16000
    silent = np.zeros(sr, dtype=np.float32)
    sf.write(str(file_path), silent, sr)
    return str(file_path)

def test_audio_format_validation(sample_wav_file, tmp_path):
    # Valid file
    res = AudioProcessor.validate_file(sample_wav_file)
    assert res["valid"] is True
    assert res["extension"] == ".wav"

    # Unsupported extension
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("not audio")
    with pytest.raises(AudioProcessingError) as excinfo:
        AudioProcessor.validate_file(str(invalid_file))
    assert "Unsupported audio format" in str(excinfo.value)

    # Missing file
    with pytest.raises(AudioProcessingError) as excinfo:
        AudioProcessor.validate_file(str(tmp_path / "nonexistent.wav"))
    assert "not found" in str(excinfo.value)

def test_mono_conversion():
    stereo = np.array([[1.0, 3.0], [2.0, 4.0]], dtype=np.float32)
    mono = AudioProcessor.to_mono(stereo)
    assert mono.ndim == 1
    assert mono[0] == 2.0
    assert mono[1] == 3.0

def test_resampling():
    orig_sr = 44100
    target_sr = 16000
    audio = np.random.randn(orig_sr).astype(np.float32)
    resampled = AudioProcessor.resample(audio, orig_sr, target_sr)
    assert len(resampled) == target_sr

def test_amplitude_normalization():
    audio = np.array([0.1, -0.5, 0.4], dtype=np.float32)
    norm = AudioProcessor.normalize_amplitude(audio, target_peak=0.95)
    assert np.isclose(np.max(np.abs(norm)), 0.95)

def test_silence_detection(silent_wav_file):
    audio, sr = AudioProcessor.load_audio(silent_wav_file)
    silence = AudioProcessor.detect_silence(audio, sr=sr)
    assert silence["is_silent"] is True

def test_spectral_noise_reduction(sample_wav_file):
    audio, sr = AudioProcessor.load_audio(sample_wav_file)
    mono = AudioProcessor.to_mono(audio)
    resampled = AudioProcessor.resample(mono, sr, 16000)
    denoised = AudioProcessor.apply_spectral_noise_reduction(resampled, sr=16000)
    assert len(denoised) > 0

def test_asr_service_mocked_transcription(sample_wav_file):
    service = ASRService(model_name="openai/whisper-test-mock")

    # Mock the internal pipeline
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = {"text": "नमस्ते भारत"}
    service._pipeline = mock_pipeline

    result = service.transcribe(sample_wav_file, language="hi")
    assert result["text"] == "नमस्ते भारत"
    assert result["language"] == "hi"
    assert result["confidence"] == 0.95
    assert result["duration_ms"] > 0

