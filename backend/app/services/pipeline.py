"""
Complete Multilingual Voice Translation Pipeline Orchestrator
Flow: Audio Input -> DSP Preprocessing -> ASR -> LID -> NMT -> TTS -> Audio Output
Provides individual processing times and unified error handling.
"""

import time
import logging
from typing import Dict, Any, Optional

from app.services.asr.service import asr_service
from app.services.language_detection.service import lid_service
from app.services.translation.service import nmt_service
from app.services.tts.service import tts_service
from app.core.languages_config import get_language_by_code, SUPPORTED_LANGUAGES

logger = logging.getLogger("bhashaai.services.pipeline")

class TranslationPipelineError(Exception):
    pass

class VoiceTranslationPipeline:
    def execute_voice_pipeline(
        self,
        audio_file_path: str,
        target_language: str,
        source_language_hint: Optional[str] = None,
        apply_denoise: bool = False,
        prefer_local_tts: bool = False
    ) -> Dict[str, Any]:
        """
        Executes end-to-end speech-to-speech translation:
        Audio In -> DSP -> ASR -> LID -> NMT -> TTS -> Audio Out
        """
        pipeline_start = time.perf_counter()
        latencies = {
            "asr_ms": 0.0,
            "lid_ms": 0.0,
            "nmt_ms": 0.0,
            "tts_ms": 0.0,
            "total_ms": 0.0
        }

        # Validate target language
        tgt_cfg = get_language_by_code(target_language)
        if not tgt_cfg:
            raise TranslationPipelineError(
                f"Target language '{target_language}' is not supported. Supported: {list(SUPPORTED_LANGUAGES.keys())}"
            )

        # Stage 1: Automatic Speech Recognition (ASR)
        asr_start = time.perf_counter()
        try:
            asr_res = asr_service.transcribe(
                audio_file_path=audio_file_path,
                language=source_language_hint,
                apply_denoise=apply_denoise
            )
            latencies["asr_ms"] = asr_res.get("duration_ms", round((time.perf_counter() - asr_start) * 1000, 2))
            recognized_text = asr_res.get("text", "").strip()
        except Exception as e:
            logger.error(f"Pipeline Stage 1 (ASR) failed: {e}")
            raise TranslationPipelineError(f"Speech recognition failed: {str(e)}")

        if not recognized_text:
            total_time = round((time.perf_counter() - pipeline_start) * 1000, 2)
            latencies["total_ms"] = total_time
            return {
                "recognized_text": "",
                "detected_language": source_language_hint or "unknown",
                "detection_confidence": 0.0,
                "translated_text": "",
                "source_language": source_language_hint or "unknown",
                "target_language": tgt_cfg.iso_639_1,
                "generated_audio": None,
                "latencies": latencies,
                "warning": "No speech could be recognized from the provided audio."
            }

        # Stage 2: Language Identification (LID)
        lid_start = time.perf_counter()
        try:
            lid_res = lid_service.detect_language(
                text=recognized_text,
                hint_language=source_language_hint
            )
            latencies["lid_ms"] = round((time.perf_counter() - lid_start) * 1000, 2)
            detected_lang = lid_res["detected_code"]
            confidence = lid_res["confidence"]
        except Exception as e:
            logger.warning(f"LID warning: {e}. Defaulting to source hint or 'en'")
            detected_lang = source_language_hint or "en"
            confidence = 0.5

        # Decide source language (if user provided a valid hint, check match or prioritize)
        source_lang = source_language_hint if source_language_hint else detected_lang

        # Stage 3: Neural Machine Translation (NMT)
        nmt_start = time.perf_counter()
        try:
            nmt_res = nmt_service.translate(
                text=recognized_text,
                target_language=tgt_cfg.iso_639_1,
                source_language=source_lang
            )
            latencies["nmt_ms"] = nmt_res.get("duration_ms", round((time.perf_counter() - nmt_start) * 1000, 2))
            translated_text = nmt_res.get("translated_text", "").strip()
        except Exception as e:
            logger.error(f"Pipeline Stage 3 (NMT) failed: {e}")
            raise TranslationPipelineError(f"Neural machine translation failed: {str(e)}")

        # Stage 4: Text-to-Speech (TTS)
        tts_start = time.perf_counter()
        try:
            tts_res = tts_service.synthesize_speech(
                text=translated_text,
                target_language=tgt_cfg.iso_639_1,
                prefer_local=prefer_local_tts
            )
            latencies["tts_ms"] = tts_res.get("duration_ms", round((time.perf_counter() - tts_start) * 1000, 2))
        except Exception as e:
            logger.error(f"Pipeline Stage 4 (TTS) failed: {e}")
            raise TranslationPipelineError(f"Speech synthesis failed: {str(e)}")

        latencies["total_ms"] = round((time.perf_counter() - pipeline_start) * 1000, 2)

        return {
            "recognized_text": recognized_text,
            "detected_language": detected_lang,
            "detection_confidence": confidence,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": tgt_cfg.iso_639_1,
            "generated_audio": {
                "file_id": tts_res["file_id"],
                "filename": tts_res["filename"],
                "file_path": tts_res["file_path"],
                "file_size_bytes": tts_res["file_size_bytes"],
                "duration_seconds": tts_res["duration_seconds"],
                "sample_rate": tts_res["sample_rate"],
                "engine_used": tts_res["engine_used"]
            },
            "latencies": latencies
        }

# Global Singleton
pipeline_orchestrator = VoiceTranslationPipeline()
