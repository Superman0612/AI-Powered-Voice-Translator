"""
Automatic Speech Recognition (ASR) Metric Evaluator
Computes Word Error Rate (WER) and Character Error Rate (CER) using jiwer.
"""

from typing import List, Dict, Any
import jiwer

class ASREvaluator:
    @staticmethod
    def compute_metrics(hypotheses: List[str], references: List[str]) -> Dict[str, float]:
        """
        Computes corpus-level WER and CER between model hypotheses and ground-truth references.
        """
        if not hypotheses or not references or len(hypotheses) != len(references):
            raise ValueError("Hypotheses and references must be non-empty and of identical length.")

        # Clean whitespace and strip
        hyps = [h.strip() for h in hypotheses]
        refs = [r.strip() for r in references]

        wer = jiwer.wer(reference=refs, hypothesis=hyps)
        cer = jiwer.cer(reference=refs, hypothesis=hyps)

        return {
            "wer": round(float(wer), 4),
            "cer": round(float(cer), 4),
            "wer_percent": round(float(wer) * 100, 2),
            "cer_percent": round(float(cer) * 100, 2),
            "sample_count": len(hypotheses)
        }

