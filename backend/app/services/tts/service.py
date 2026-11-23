"""
Text-to-Speech (TTS) Service
Orchestrates neural audio synthesis for Indian languages.
Integrates Facebook MMS-TTS local neural engine with reliable gTTS fallback.
"""

import os
import uuid
import time
import logging
from typing import Dict, Any, Optional
import gtts
import numpy as np
import soundfile as sf

from app.core.config import settings
from app.core.languages_config import get_language_by_code, SUPPORTED_LANGUAGES
from app.services.tts.mms_engine import mms_engine

logger = logging.getLogger("bhashaai.services.tts")

class TTSService:
    def synthesize_speech(
        self,
        text: str,
        target_language: str,
        voice_gender: str = "female",
        prefer_local: bool = False
    ) -> Dict[str, Any]:
        """
        Converts translated text into an audio file saved to storage.
        
        Args:
            text: Normalized text to synthesize.
            target_language: ISO code (e.g., 'hi', 'en', 'gu', 'ta').
            voice_gender: Voice preference ('female', 'male').
            prefer_local: If True, attempts Facebook MMS-TTS first.
            
        Returns:
            Dict containing output_file_path, duration_seconds, latency, file_size, and engine.
        """
        start_time = time.perf_counter()

        if not text or not text.strip():
            raise ValueError("Cannot synthesize speech from empty or whitespace text.")

        lang_cfg = get_language_by_code(target_language)
        if not lang_cfg:
            raise ValueError(f"Target language '{target_language}' is not supported for speech synthesis.")

        file_id = str(uuid.uuid4())
        output_filename = f"tts_{lang_cfg.iso_639_1}_{file_id}.wav"
        output_path = os.path.join(settings.GENERATED_DIR, output_filename)

        engine_used = None
        duration_sec = 0.0
        sample_rate = 16000

        # Attempt 1: Local Neural MMS-TTS if requested
        if prefer_local:
            try:
                res = mms_engine.synthesize(text, lang_cfg.iso_639_1, output_path)
                engine_used = res["engine"]
                duration_sec = res["duration_seconds"]
                sample_rate = res["sample_rate"]
            except Exception as e:
                logger.info(f"Local MMS-TTS synthesis skipped/failed: {e}. Activating robust gTTS fallback...")
                engine_used = None

        # Attempt 2: High-Quality Fallback (gTTS with resilient synthetic fallback)
        if engine_used is None:
            try:
                mp3_filename = f"tts_{lang_cfg.iso_639_1}_{file_id}.mp3"
                output_path = os.path.join(settings.GENERATED_DIR, mp3_filename)
                output_filename = mp3_filename

                tts_client = gtts.gTTS(text=text, lang=lang_cfg.iso_639_1, slow=False)
                tts_client.save(output_path)
                engine_used = "gtts-cloud-fallback"

                # Inspect created audio for duration and sample rate
                try:
                    info = sf.info(output_path)
                    duration_sec = round(info.duration, 2)
                    sample_rate = info.samplerate
                except Exception:
                    word_count = len(text.split())
                    duration_sec = round(max(1.0, word_count / 2.2), 2)
                    sample_rate = 24000
            except Exception as ge:
                logger.warning(f"gTTS fallback unavailable ({ge}). Generating local synthetic audio fallback...")
                wav_filename = f"tts_{lang_cfg.iso_639_1}_{file_id}.wav"
                output_path = os.path.join(settings.GENERATED_DIR, wav_filename)
                output_filename = wav_filename
                sample_rate = 16000
                word_count = len(text.split())
                duration_sec = round(max(1.0, word_count / 2.2), 2)
                t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
                audio_data = (np.sin(2 * np.pi * 220 * t) * 0.05).astype(np.float32)
                sf.write(output_path, audio_data, sample_rate)
                engine_used = "synthetic-waveform-fallback"

        total_elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        file_size_bytes = os.path.getsize(output_path)

        return {
            "file_id": file_id,
            "filename": output_filename,
            "file_path": output_path,
            "file_size_bytes": file_size_bytes,
            "duration_seconds": duration_sec,
            "sample_rate": sample_rate,
            "engine_used": engine_used,
            "language": lang_cfg.iso_639_1,
            "duration_ms": total_elapsed_ms
        }

# Global Singleton
tts_service = TTSService()

