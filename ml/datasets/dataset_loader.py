"""
Dataset Loader for BhashaAI ML Benchmarking Framework
Loads multi-parallel parallel sentences across Indian languages.
"""

import os
import json
from typing import List, Dict, Tuple, Optional

DEFAULT_DATASET_PATH = os.path.join(os.path.dirname(__file__), "test_multilingual_corpus.json")

class DatasetLoader:
    def __init__(self, dataset_path: str = DEFAULT_DATASET_PATH):
        self.dataset_path = dataset_path
        self._data = None
        self._load()

    def _load(self):
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Benchmark dataset not found at: {self.dataset_path}")
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    @property
    def total_samples(self) -> int:
        return len(self._data.get("samples", []))

    def get_parallel_pairs(self, src_lang: str, tgt_lang: str) -> List[Tuple[str, str]]:
        """
        Extracts source and target text tuples for a language pair.
        Returns: [(src_sentence, ref_sentence), ...]
        """
        pairs = []
        for sample in self._data.get("samples", []):
            if src_lang in sample and tgt_lang in sample:
                pairs.append((sample[src_lang], sample[tgt_lang]))
        return pairs

    def get_all_sentences(self, lang: str) -> List[str]:
        return [s[lang] for s in self._data.get("samples", []) if lang in s]

