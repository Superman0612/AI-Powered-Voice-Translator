import pytest
from unittest.mock import MagicMock
from app.services.translation.normalizer import TextNormalizer
from app.services.translation.service import NMTService

def test_text_normalizer():
    raw_text = "  नमस्ते    दुनिया ।  यह   परीक्षण  है।  "
    normalized = TextNormalizer.normalize_text(raw_text)
    assert "  " not in normalized
    assert normalized.startswith("नमस्ते")
    assert "।" in normalized

def test_resolve_codes():
    service = NMTService()
    src_iso, tgt_iso, src_nllb, tgt_nllb = service._resolve_codes("hi", "ta")
    assert src_iso == "hi"
    assert tgt_iso == "ta"
    assert src_nllb == "hin_Deva"
    assert tgt_nllb == "tam_Taml"

def test_unsupported_language_raises_error():
    service = NMTService()
    with pytest.raises(ValueError) as excinfo:
        service.translate("Hello", target_language="klingon", source_language="en")
    assert "not supported" in str(excinfo.value)

def test_identity_translation():
    service = NMTService()
    result = service.translate("Hello world", target_language="en", source_language="en")
    assert result["translated_text"] == "Hello world"
    assert result["source_language"] == "en"
    assert result["target_language"] == "en"

def test_nmt_service_mocked_inference():
    service = NMTService(model_name="facebook/nllb-test-mock")

    mock_tokenizer = MagicMock()
    mock_model = MagicMock()

    mock_tokenizer.unk_token_id = -1
    mock_tokenizer.convert_tokens_to_ids.return_value = 12345
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.return_value = {"input_ids": MagicMock()}
    mock_model.generate.return_value = MagicMock()
    mock_tokenizer.batch_decode.return_value = ["भारत में आपका स्वागत है"]

    service._tokenizer = mock_tokenizer
    service._model = mock_model

    res = service.translate("Welcome to India", target_language="hi", source_language="en")
    assert res["translated_text"] == "भारत में आपका स्वागत है"
    assert res["target_language"] == "hi"
    assert res["src_nllb_code"] == "eng_Latn"
    assert res["tgt_nllb_code"] == "hin_Deva"

