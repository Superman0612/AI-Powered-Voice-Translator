"""
Facebook MMS-TTS (Meta Massively Multilingual Speech) Local Engine
Uses VITS (Variational Inference with adversarial learning for end-to-end TTS).
Each language is an independent lightweight (~36M parameter) model.
"""

import os
import time
import logging
import gc
from typing import Dict, Any, Optional
import torch
import soundfile as sf
from transformers import VitsModel, AutoTokenizer

from app.core.config import settings
from app.core.languages_config import get_language_by_code

logger = logging.getLogger("bhashaai.services.tts.mms")

class MMSTTSEngine:
    def __init__(self):
        self._current_lang: Optional[str] = None
        self._model: Optional[VitsModel] = None
        self._tokenizer: Optional[AutoTokenizer] = None

    def _load_model_for_lang(self, iso_code: str):
        """Loads language-specific VITS model into memory."""
        lang_cfg = get_language_by_code(iso_code)
        if not lang_cfg:
            raise ValueError(f"Unsupported language code '{iso_code}' for MMS-TTS.")

        mms_model_id = lang_cfg.mms_tts_code

        # If already loaded for this language, reuse
        if self._current_lang == iso_code and self._model is not None:
            return

        logger.info(f"Loading MMS-TTS model '{mms_model_id}' on CPU...")
        load_start = time.perf_counter()
        
        # Release previous language model to maintain strict RAM budget (<8GB)
        self.unload()

        try:
            self._tokenizer = AutoTokenizer.from_pretrained(mms_model_id)
            self._model = VitsModel.from_pretrained(mms_model_id)
            self._model.eval()
            self._current_lang = iso_code
            elapsed = round(time.perf_counter() - load_start, 2)
            logger.info(f"MMS-TTS model '{mms_model_id}' loaded in {elapsed}s.")
        except Exception as e:
            logger.error(f"Failed to load MMS-TTS model '{mms_model_id}': {e}")
            self.unload()
            raise RuntimeError(f"MMS-TTS Model Initialization Error: {str(e)}")

    def synthesize(self, text: str, iso_code: str, output_path: str) -> Dict[str, Any]:
        """Synthesizes text into a WAV audio file on disk."""
        start_time = time.perf_counter()
        self._load_model_for_lang(iso_code)

        try:
            inputs = self._tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                output = self._model(**inputs).waveform

            waveform = output.squeeze().cpu().numpy()
            sample_rate = self._model.config.sampling_rate

            # Write WAV file using soundfile
            sf.write(output_path, waveform, samplerate=sample_rate)

            duration_sec = len(waveform) / float(sample_rate)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return {
                "success": True,
                "engine": "facebook/mms-tts",
                "sample_rate": sample_rate,
                "duration_seconds": round(duration_sec, 2),
                "duration_ms": elapsed_ms,
                "output_path": output_path
            }

        except Exception as e:
            logger.warning(f"MMS-TTS local synthesis encountered exception: {e}")
            raise e

    def unload(self):
        """Frees model from RAM."""
        if self._model is not None or self._tokenizer is not None:
            del self._model
            del self._tokenizer
            self._model = None
            self._tokenizer = None
            self._current_lang = None
            gc.collect()

# Global MMS instance
mms_engine = MMSTTSEngine()

