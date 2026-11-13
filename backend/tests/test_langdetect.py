from app.services.language_detection.service import lid_service
from app.services.language_detection.heuristics import (
    analyze_script_distribution,
    disambiguate_devanagari,
    check_code_mixing
)

def test_script_distribution():
    hindi_text = "नमस्ते दुनिया"
    dist = analyze_script_distribution(hindi_text)
    assert "Devanagari" in dist
    assert dist["Devanagari"] == 1.0

    tamil_text = "வணக்கம் உலகம்"
    dist_ta = analyze_script_distribution(tamil_text)
    assert "Tamil" in dist_ta
    assert dist_ta["Tamil"] == 1.0

def test_devanagari_disambiguation_hindi():
    hindi_sentence = "हम आज स्कूल जा रहे हैं और खाना खाएंगे।"
    lang, conf = disambiguate_devanagari(hindi_sentence)
    assert lang == "hi"
    assert conf >= 0.70

def test_devanagari_disambiguation_marathi():
    marathi_sentence = "आम्ही आज घरी जात आहोत आणि अभ्यास करणार नाही."
    lang, conf = disambiguate_devanagari(marathi_sentence)
    assert lang == "mr"
    assert conf >= 0.70

def test_all_10_target_languages_identification():
    test_cases = [
        ("नमस्ते, आप कैसे हैं?", "hi"),
        ("Hello, how are you doing today?", "en"),
        ("નમસ્તે, તમે કેમ છો?", "gu"),
        ("नमस्कार, तुम्ही कसे आहात? आम्ही ठीक आहोत.", "mr"),
        ("নমস্কার, আপনি কেমন আছেন?", "bn"),
        ("வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?", "ta"),
        ("నమస్కారం, మీరు ఎలా ఉన్నారు?", "te"),
        ("ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?", "kn"),
        ("നമസ്കാരം, സുഖമാണോ?", "ml"),
        ("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?", "pa")
    ]
    for text, expected_code in test_cases:
        res = lid_service.detect_language(text)
        assert res["detected_code"] == expected_code, f"Failed for {text}: expected {expected_code}, got {res['detected_code']}"
        assert res["confidence"] > 0.60
        assert res["is_supported"] is True

def test_empty_string_handling():
    res = lid_service.detect_language("")
    assert res["is_supported"] is False
    assert res["confidence"] == 0.0

def test_code_mixed_text():
    code_mixed = "Hello dost, kaise ho? Main theek hoon."
    dist = analyze_script_distribution(code_mixed)
    assert "Latin" in dist  # Romanized Hindi uses Latin script

