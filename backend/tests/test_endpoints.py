import io
import numpy as np
import soundfile as sf
from fastapi import status
from unittest.mock import patch

def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "operational"
    assert data["database"]["status"] == "healthy"
    assert "ram_available_mb" in data["system"]

def test_list_languages_endpoint(client):
    response = client.get("/api/v1/languages")
    assert response.status_code == status.HTTP_200_OK
    langs = response.json()
    assert len(langs) >= 10
    codes = [l["code_iso_639_1"] for l in langs]
    assert "hi" in codes
    assert "ta" in codes
    assert "en" in codes

def test_get_single_language_details(client):
    response = client.get("/api/v1/languages/hi")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Hindi"
    assert data["script_name"] == "Devanagari"
    assert data["nllb_code"] == "hin_Deva"

def test_detect_language_endpoint(client):
    response = client.post("/api/v1/languages/detect", json={"text": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["detected_language"] == "ta"
    assert data["language_name"] == "Tamil"
    assert data["is_supported"] is True

def test_audio_upload_endpoint(client, auth_headers):
    # Create synthetic wav in-memory buffer
    sr = 16000
    audio_data = (np.sin(2 * np.pi * 440 * np.linspace(0, 0.5, sr // 2)) * 32767).astype(np.int16)
    buf = io.BytesIO()
    sf.write(buf, audio_data, sr, format='WAV')
    buf.seek(0)

    files = {"file": ("test_upload.wav", buf, "audio/wav")}
    response = client.post("/api/v1/audio/upload", files=files, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["original_filename"] == "test_upload.wav"
    assert data["file_size_bytes"] > 0

    # Retrieve uploaded audio metadata
    audio_id = data["id"]
    get_res = client.get(f"/api/v1/audio/{audio_id}")
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["id"] == audio_id

def test_text_translate_endpoint_with_mock_nmt(client, auth_headers):
    with patch("app.services.translation.service.nmt_service.translate") as mock_nmt:
        mock_nmt.return_value = {
            "source_text": "Hello world",
            "translated_text": "नमस्ते दुनिया",
            "source_language": "en",
            "target_language": "hi",
            "duration_ms": 32.5
        }

        payload = {
            "source_text": "Hello world",
            "source_language": "en",
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate/text", json=payload, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["translated_text"] == "नमस्ते दुनिया"
        assert data["target_language"] == "hi"
        assert "latencies" in data

def test_translation_history_endpoint(client, auth_headers):
    response = client.get("/api/v1/translate/history", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_evaluation_endpoints(client):
    models_res = client.get("/api/v1/evaluation/models")
    assert models_res.status_code == status.HTTP_200_OK
    assert len(models_res.json()) >= 4

    summary_res = client.get("/api/v1/evaluation/summary")
    assert summary_res.status_code == status.HTTP_200_OK
    assert "total_registered_models" in summary_res.json()

