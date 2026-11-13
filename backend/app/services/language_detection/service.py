"""
Language Identification Service
Integrates Unicode script detection, morphological heuristic disambiguation,
and langdetect statistical models to accurately identify Indic languages.
"""

import logging
from typing import Dict, Any, Optional
from langdetect import DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException

from app.core.languages_config import SUPPORTED_LANGUAGES, get_language_by_code
from app.services.language_detection.heuristics import (
    analyze_script_distribution,
    disambiguate_devanagari,
    check_code_mixing
)

# Seed langdetect for deterministic inference
DetectorFactory.seed = 42
logger = logging.getLogger("bhashaai.services.lid")

SCRIPT_TO_ISO = {
    "Bengali": "bn",
    "Gurmukhi": "pa",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Latin": "en"
}

class LanguageDetectionService:
    def detect_language(self, text: str, hint_language: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect language of provided text.
        Returns:
            {
                "detected_code": "hi",
                "language_name": "Hindi",
                "script": "Devanagari",
                "confidence": 0.98,
                "is_supported": True,
                "is_code_mixed": False,
                "matches_hint": True/False,
                "details": {...}
            }
        """
        if not text or not text.strip():
            return {
                "detected_code": "en",
                "language_name": "Unknown",
                "script": "Unknown",
                "confidence": 0.0,
                "is_supported": False,
                "is_code_mixed": False,
                "matches_hint": False,
                "details": {"reason": "Empty input"}
            }

        # Step 1: Script Distribution
        script_dist = analyze_script_distribution(text)
        code_mix_info = check_code_mixing(script_dist)

        # Primary script determination
        if script_dist:
            primary_script = max(script_dist, key=script_dist.get)
            script_confidence = script_dist[primary_script]
        else:
            primary_script = "Latin"
            script_confidence = 0.5

        detected_code = "en"
        confidence = script_confidence

        if primary_script == "Devanagari":
            # Disambiguate Hindi vs Marathi
            detected_code, confidence = disambiguate_devanagari(text)
        elif primary_script in SCRIPT_TO_ISO:
            detected_code = SCRIPT_TO_ISO[primary_script]
            # Boost confidence when script matches unambiguously
            confidence = max(confidence, 0.92)
        else:
            # Fallback to langdetect statistical analyzer
            try:
                predictions = detect_langs(text)
                if predictions:
                    top_pred = predictions[0]
                    detected_code = top_pred.lang
                    confidence = round(top_pred.prob, 3)
            except LangDetectException:
                detected_code = "en"
                confidence = 0.30

        # Validate against supported catalog
        lang_config = get_language_by_code(detected_code)
        is_supported = lang_config is not None
        lang_name = lang_config.name if lang_config else f"Unrecognized ({detected_code})"
        script_name = lang_config.script if lang_config else primary_script

        matches_hint = None
        if hint_language:
            hint_cfg = get_language_by_code(hint_language)
            if hint_cfg:
                matches_hint = (hint_cfg.iso_639_1 == detected_code)

        return {
            "detected_code": detected_code,
            "language_name": lang_name,
            "script": script_name,
            "confidence": round(min(1.0, float(confidence)), 3),
            "is_supported": is_supported,
            "is_code_mixed": bool(code_mix_info),
            "matches_hint": matches_hint,
            "details": {
                "script_distribution": script_dist,
                "code_mixing": code_mix_info
            }
        }

# Global Singleton
lid_service = LanguageDetectionService()

