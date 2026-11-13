"""
Text Normalization & Preprocessing for Indian Language Machine Translation
Handles Unicode canonical decomposition/composition, punctuation mapping,
and whitespace cleanup prior to Seq2Seq tokenization.
"""

import unicodedata
import re

class TextNormalizer:
    @staticmethod
    def normalize_text(text: str, script: str = "Devanagari") -> str:
        """Applies Unicode NFC normalization and punctuation standardizations."""
        if not text:
            return ""

        # Step 1: Unicode NFC Normalization
        text = unicodedata.normalize("NFC", text)

        # Step 2: Normalize multiple whitespaces and control characters
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r' +', ' ', text).strip()

        # Step 3: Normalize quotes and dashes
        text = re.sub(r'[“”„‟"]', '"', text)
        text = re.sub(r"[‘’‚‛']", "'", text)
        text = re.sub(r'[—–]', '-', text)

        # Step 4: Danda normalization for Indic scripts
        # Ensure proper spacing around Purna Viram (।) and Deergh Viram (॥)
        text = re.sub(r'\s*([।॥])\s*', r' \1 ', text)
        text = re.sub(r' +', ' ', text).strip()

        return text

