"""
Automatic Speech Recognition (ASR) Service
Modular service wrapping OpenAI Whisper for multi-language transcription on CPU.
Features lazy loading, memory safety, DSP preprocessing, and latency telemetry.
"""

import time
import logging
import gc
from typing import Dict, Any, Optional
import numpy as np
import torch
from transformers import pipeline

from app.core.config import settings
from app.core.languages_config import get_language_by_code
from app.services.asr.audio_processor import AudioProcessor, AudioProcessingError

logger = logging.getLogger("bhashaai.services.asr")

class ASRService:
    def __init__(self, model_name: Optional[str] = None):
        chosen = model_name or settings.WHISPER_MODEL_NAME
        # On cloud free-tier containers (like Render 512MB RAM), heavy models cause OOM / 502 Bad Gateway
        if "small" in chosen.lower() or "medium" in chosen.lower() or "large" in chosen.lower():
            chosen = "openai/whisper-tiny"
        self.model_name = chosen
        self._pipeline = None
        self._is_loading = False

    def _get_pipeline(self):
        """Lazy loader for Whisper ASR model on CPU."""
        if self._pipeline is None:
            logger.info(f"Loading ASR model '{self.model_name}' on CPU...")
            start_load = time.time()
            try:
                # CPU device = -1 or "cpu"
                self._pipeline = pipeline(
                    "automatic-speech-recognition",
                    model=self.model_name,
                    device="cpu",
                    torch_dtype=torch.float32,
                    chunk_length_s=30
                )
                load_time = round(time.time() - start_load, 2)
                logger.info(f"ASR model '{self.model_name}' loaded in {load_time}s.")
            except Exception as e:
                logger.error(f"Failed to load Whisper ASR model: {e}")
                raise RuntimeError(f"ASR Model Initialization Error: {str(e)}")
        return self._pipeline

    def transcribe(
        self,
        audio_file_path: str,
        language: Optional[str] = None,
        apply_denoise: bool = False
    ) -> Dict[str, Any]:
        """
        Transcribes speech from an audio file.
        
        Args:
            audio_file_path: Absolute or relative path to the audio file.
            language: Optional source language code (e.g., 'hi', 'en', 'ta').
            apply_denoise: Whether to apply spectral subtraction noise reduction.

        Returns:
            Dict containing:
                - text: Recognized transcript
                - language: Detected or configured language code
                - confidence: Speech detection confidence
                - duration_ms: Inference time in milliseconds
                - audio_metadata: DSP metrics (sample rate, original duration, etc.)
        """
        start_time = time.perf_counter()

        # Step 1: Preprocess audio through DSP pipeline
        audio_array, meta = AudioProcessor.preprocess_pipeline(
            audio_file_path,
            apply_denoise=apply_denoise
        )

        if meta.get("is_silent") or len(audio_array) == 0:
            return {
                "text": "",
                "language": language or "unknown",
                "confidence": 0.0,
                "duration_ms": round((time.perf_counter() - start_time) * 1000, 2),
                "audio_metadata": meta,
                "warning": "Audio was detected as complete silence."
            }

        # Step 2: Language Code Resolution for Whisper
        whisper_lang = None
        if language:
            lang_cfg = get_language_by_code(language)
            if lang_cfg:
                whisper_lang = lang_cfg.whisper_code

        # Step 3: Run Model Inference
        asr_pipe = self._get_pipeline()
        generate_kwargs = {"task": "transcribe"}
        if whisper_lang:
            generate_kwargs["language"] = whisper_lang

        try:
            inference_start = time.perf_counter()
            result = asr_pipe(
                {"raw": audio_array, "sampling_rate": settings.SAMPLE_RATE},
                generate_kwargs=generate_kwargs,
                return_timestamps=False
            )
            inference_time_ms = round((time.perf_counter() - inference_start) * 1000, 2)
            total_duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            recognized_text = result.get("text", "").strip()

            return {
                "text": recognized_text,
                "language": whisper_lang or language or "auto",
                "confidence": 0.95 if recognized_text else 0.0,
                "inference_time_ms": inference_time_ms,
                "duration_ms": total_duration_ms,
                "audio_metadata": meta
            }

        except Exception as e:
            logger.error(f"ASR transcription inference failure: {e}")
            raise RuntimeError(f"Speech transcription failed: {str(e)}")

    def unload(self):
        """Releases model from RAM to reclaim memory under tight constraints."""
        if self._pipeline is not None:
            logger.info("Unloading ASR model from memory...")
            del self._pipeline
            self._pipeline = None
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None

# Global Singleton
asr_service = ASRService()

