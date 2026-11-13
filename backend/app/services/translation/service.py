"""
Neural Machine Translation (NMT) Service
Orchestrates transformer-based sequence-to-sequence translation for Indian languages.
Primary Engine: Meta NLLB-200 Distilled 600M with full ISO-to-FLORES code mappings.
"""

import time
import logging
import gc
from typing import Dict, Any, List, Optional
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.core.config import settings
from app.core.languages_config import get_language_by_code, SUPPORTED_LANGUAGES
from app.services.translation.normalizer import TextNormalizer

logger = logging.getLogger("bhashaai.services.nmt")

class NMTService:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.NMT_MODEL_NAME
        self._tokenizer = None
        self._model = None

    def _load_model(self):
        """Lazy load NMT model and tokenizer."""
        if self._model is None or self._tokenizer is None:
            logger.info(f"Loading NMT model '{self.model_name}' on CPU...")
            load_start = time.perf_counter()
            try:
                self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self._model = AutoModelForSeq2SeqLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True
                )
                self._model.eval()
                elapsed = round(time.perf_counter() - load_start, 2)
                logger.info(f"NMT model '{self.model_name}' successfully loaded in {elapsed}s.")
            except Exception as e:
                logger.error(f"Failed to load NMT model: {e}")
                raise RuntimeError(f"NMT Model Initialization Error: {str(e)}")

    def _resolve_codes(self, src_lang: str, tgt_lang: str) -> tuple[str, str, str, str]:
        """Resolves input language codes to both ISO and NLLB FLORES tokens."""
        src_cfg = get_language_by_code(src_lang)
        tgt_cfg = get_language_by_code(tgt_lang)

        if not src_cfg:
            raise ValueError(f"Source language '{src_lang}' is not supported. Supported: {list(SUPPORTED_LANGUAGES.keys())}")
        if not tgt_cfg:
            raise ValueError(f"Target language '{tgt_lang}' is not supported. Supported: {list(SUPPORTED_LANGUAGES.keys())}")

        return src_cfg.iso_639_1, tgt_cfg.iso_639_1, src_cfg.nllb_code, tgt_cfg.nllb_code

    def translate(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = "en"
    ) -> Dict[str, Any]:
        """
        Translates text from source_language to target_language.
        
        Args:
            text: Input string to translate.
            target_language: ISO code (e.g., 'hi', 'ta', 'bn').
            source_language: ISO code (e.g., 'en', 'gu').
            
        Returns:
            Dict containing translated_text, resolved codes, and duration_ms.
        """
        start_time = time.perf_counter()

        if not text or not text.strip():
            return {
                "source_text": text,
                "translated_text": "",
                "source_language": source_language,
                "target_language": target_language,
                "duration_ms": 0.0
            }

        # Step 1: Normalize and resolve codes
        normalized_text = TextNormalizer.normalize_text(text)
        src_iso, tgt_iso, src_nllb, tgt_nllb = self._resolve_codes(source_language, target_language)

        # Identity translation shortcut
        if src_iso == tgt_iso:
            return {
                "source_text": normalized_text,
                "translated_text": normalized_text,
                "source_language": src_iso,
                "target_language": tgt_iso,
                "duration_ms": 0.1
            }

        # Step 2: Ensure model is loaded
        self._load_model()

        # Step 3: Tokenize & Generate with forced BOS target language
        try:
            self._tokenizer.src_lang = src_nllb
            inputs = self._tokenizer(
                normalized_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )

            target_token_id = self._tokenizer.convert_tokens_to_ids(tgt_nllb)
            if target_token_id == self._tokenizer.unk_token_id:
                raise ValueError(f"Target language token '{tgt_nllb}' not found in NLLB tokenizer vocabulary.")

            with torch.no_grad():
                generated_tokens = self._model.generate(
                    **inputs,
                    forced_bos_token_id=target_token_id,
                    max_length=512,
                    num_beams=2,
                    early_stopping=True
                )

            translated_text = self._tokenizer.batch_decode(
                generated_tokens,
                skip_special_tokens=True
            )[0].strip()

            total_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return {
                "source_text": normalized_text,
                "translated_text": translated_text,
                "source_language": src_iso,
                "target_language": tgt_iso,
                "src_nllb_code": src_nllb,
                "tgt_nllb_code": tgt_nllb,
                "duration_ms": total_ms
            }

        except Exception as e:
            logger.error(f"Translation inference failed for '{src_iso}' -> '{tgt_iso}': {e}")
            raise RuntimeError(f"Translation inference error: {str(e)}")

    def translate_batch(
        self,
        texts: List[str],
        target_language: str,
        source_language: str
    ) -> List[Dict[str, Any]]:
        """Batch translation for evaluation and experimentation."""
        results = []
        for t in texts:
            results.append(self.translate(t, target_language=target_language, source_language=source_language))
        return results

    def unload(self):
        """Unload NMT model to free RAM."""
        if self._model is not None or self._tokenizer is not None:
            logger.info("Unloading NMT model from memory...")
            del self._model
            del self._tokenizer
            self._model = None
            self._tokenizer = None
            gc.collect()

# Global Singleton
nmt_service = NMTService()

