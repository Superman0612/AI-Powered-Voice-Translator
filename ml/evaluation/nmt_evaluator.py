"""
Neural Machine Translation (NMT) Metric Evaluator
Computes corpus BLEU and character n-gram F-score (chrF++) using sacrebleu.
"""

from typing import List, Dict, Any
import sacrebleu

class NMTEvaluator:
    @staticmethod
    def compute_metrics(hypotheses: List[str], references: List[str]) -> Dict[str, float]:
        """
        Computes BLEU and chrF scores.
        sacrebleu expects references as a list of lists: [[ref1, ref2, ...]]
        """
        if not hypotheses or not references or len(hypotheses) != len(references):
            raise ValueError("Hypotheses and references must be non-empty and of identical length.")

        hyps = [h.strip() for h in hypotheses]
        refs = [[r.strip() for r in references]]

        # Compute BLEU
        bleu = sacrebleu.corpus_bleu(hyps, refs)
        # Compute chrF (Character n-gram F-score, very effective for agglutinative Indian languages)
        chrf = sacrebleu.corpus_chrf(hyps, refs)

        return {
            "bleu": round(float(bleu.score), 2),
            "chrf": round(float(chrf.score), 2),
            "sample_count": len(hypotheses)
        }

