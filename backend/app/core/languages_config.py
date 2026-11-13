"""
BhashaAI Centralized Language Configuration & Capability Matrix
Defines all supported languages, script types, code mappings, and model support.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class LanguageConfig(BaseModel):
    name: str
    native_name: str
    iso_639_1: str
    iso_639_3: str
    script: str
    unicode_range: Optional[tuple] = None  # (start, end) hex range
    nllb_code: str
    indictrans_code: str
    whisper_code: str
    mms_tts_code: str
    supports_asr: bool = True
    supports_nmt: bool = True
    supports_tts: bool = True
    supports_lid: bool = True
    sample_text: str

SUPPORTED_LANGUAGES: Dict[str, LanguageConfig] = {
    "hi": LanguageConfig(
        name="Hindi",
        native_name="हिन्दी",
        iso_639_1="hi",
        iso_639_3="hin",
        script="Devanagari",
        unicode_range=(0x0900, 0x097F),
        nllb_code="hin_Deva",
        indictrans_code="hin_Deva",
        whisper_code="hi",
        mms_tts_code="facebook/mms-tts-hin",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="नमस्ते, आप कैसे हैं? भाषाएआई में आपका स्वागत है।"
    ),
    "en": LanguageConfig(
        name="English",
        native_name="English",
        iso_639_1="en",
        iso_639_3="eng",
        script="Latin",
        unicode_range=(0x0020, 0x007F),
        nllb_code="eng_Latn",
        indictrans_code="eng_Latn",
        whisper_code="en",
        mms_tts_code="facebook/mms-tts-eng",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="Hello, how are you? Welcome to BhashaAI."
    ),
    "gu": LanguageConfig(
        name="Gujarati",
        native_name="ગુજરાતી",
        iso_639_1="gu",
        iso_639_3="guj",
        script="Gujarati",
        unicode_range=(0x0A80, 0x0AFF),
        nllb_code="guj_Gujr",
        indictrans_code="guj_Gujr",
        whisper_code="gu",
        mms_tts_code="facebook/mms-tts-guj",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="નમસ્તે, તમે કેમ છો? ભાષાએઆઈમાં આપનું સ્વાગત છે."
    ),
    "mr": LanguageConfig(
        name="Marathi",
        native_name="मराठी",
        iso_639_1="mr",
        iso_639_3="mar",
        script="Devanagari",
        unicode_range=(0x0900, 0x097F),
        nllb_code="mar_Deva",
        indictrans_code="mar_Deva",
        whisper_code="mr",
        mms_tts_code="facebook/mms-tts-mar",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="नमस्कार, तुम्ही कसे आहात? भाषाएआय मध्ये आपले स्वागत आहे."
    ),
    "bn": LanguageConfig(
        name="Bengali",
        native_name="বাংলা",
        iso_639_1="bn",
        iso_639_3="ben",
        script="Bengali",
        unicode_range=(0x0980, 0x09FF),
        nllb_code="ben_Beng",
        indictrans_code="ben_Beng",
        whisper_code="bn",
        mms_tts_code="facebook/mms-tts-ben",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="নমস্কার, আপনি কেমন আছেন? ভাষাএআই-তে আপনাকে স্বাগতম।"
    ),
    "ta": LanguageConfig(
        name="Tamil",
        native_name="தமிழ்",
        iso_639_1="ta",
        iso_639_3="tam",
        script="Tamil",
        unicode_range=(0x0B80, 0x0BFF),
        nllb_code="tam_Taml",
        indictrans_code="tam_Taml",
        whisper_code="ta",
        mms_tts_code="facebook/mms-tts-tam",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்? பாஷா ஏஐக்கு வரவேற்கிறோம்."
    ),
    "te": LanguageConfig(
        name="Telugu",
        native_name="తెలుగు",
        iso_639_1="te",
        iso_639_3="tel",
        script="Telugu",
        unicode_range=(0x0C00, 0x0C7F),
        nllb_code="tel_Telu",
        indictrans_code="tel_Telu",
        whisper_code="te",
        mms_tts_code="facebook/mms-tts-tel",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="నమస్కారం, మీరు ఎలా ఉన్నారు? భాషా ఏఐకి స్వాగతం."
    ),
    "kn": LanguageConfig(
        name="Kannada",
        native_name="ಕನ್ನಡ",
        iso_639_1="kn",
        iso_639_3="kan",
        script="Kannada",
        unicode_range=(0x0C80, 0x0CFF),
        nllb_code="kan_Knda",
        indictrans_code="kan_Knda",
        whisper_code="kn",
        mms_tts_code="facebook/mms-tts-kan",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ? ಭಾಷಾ ಎಐಗೆ ಸ್ವಾಗತ."
    ),
    "ml": LanguageConfig(
        name="Malayalam",
        native_name="മലയാളം",
        iso_639_1="ml",
        iso_639_3="mal",
        script="Malayalam",
        unicode_range=(0x0D00, 0x0D7F),
        nllb_code="mal_Mlym",
        indictrans_code="mal_Mlym",
        whisper_code="ml",
        mms_tts_code="facebook/mms-tts-mal",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="നമസ്കാരം, സുഖമാണോ? ഭാഷാ എഐലേക്ക് സ്വാഗതം."
    ),
    "pa": LanguageConfig(
        name="Punjabi",
        native_name="ਪੰਜਾਬੀ",
        iso_639_1="pa",
        iso_639_3="pan",
        script="Gurmukhi",
        unicode_range=(0x0A00, 0x0A7F),
        nllb_code="pan_Guru",
        indictrans_code="pan_Guru",
        whisper_code="pa",
        mms_tts_code="facebook/mms-tts-pan",
        supports_asr=True,
        supports_nmt=True,
        supports_tts=True,
        supports_lid=True,
        sample_text="ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ? ਭਾਸ਼ਾ ਏਆਈ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ।"
    )
}

def get_language_by_code(code: str) -> Optional[LanguageConfig]:
    """Retrieve LanguageConfig by ISO 639-1 or ISO 639-3 or NLLB code."""
    normalized = code.strip().lower()
    if normalized in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[normalized]
    for lang in SUPPORTED_LANGUAGES.values():
        if normalized in [lang.iso_639_3.lower(), lang.nllb_code.lower(), lang.name.lower()]:
            return lang
    return None

def is_language_supported(code: str) -> bool:
    return get_language_by_code(code) is not None

def list_all_languages() -> List[Dict[str, Any]]:
    return [lang.model_dump() for lang in SUPPORTED_LANGUAGES.values()]

