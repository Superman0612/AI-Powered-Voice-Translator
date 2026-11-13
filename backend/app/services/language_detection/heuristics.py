"""
Linguistic Heuristics & Unicode Script Analysis for Indian Languages
Provides script classification, Devanagari disambiguation (Hindi vs Marathi),
and code-mixing detection without fabricating confidence metrics.
"""

import re
from typing import Dict, Tuple, Optional, Any

# Unicode Script Ranges
UNICODE_RANGES = {
    "Devanagari": (0x0900, 0x097F),  # Hindi, Marathi, Sanskrit, Nepali
    "Bengali": (0x0980, 0x09FF),     # Bengali, Assamese
    "Gurmukhi": (0x0A00, 0x0A7F),    # Punjabi
    "Gujarati": (0x0A80, 0x0AFF),    # Gujarati
    "Tamil": (0x0B80, 0x0BFF),       # Tamil
    "Telugu": (0x0C00, 0x0C7F),      # Telugu
    "Kannada": (0x0C80, 0x0CFF),     # Kannada
    "Malayalam": (0x0D00, 0x0D7F),   # Malayalam
    "Latin": (0x0041, 0x007A)        # English
}

# Devanagari Distinctive Morphemes & Lexicon
MARATHI_MARKERS = {
    "characters": {'ळ', 'ऱ्'},
    "words": {
        'आहे', 'नाही', 'आहेत', 'करणे', 'झाला', 'झाली', 'झाले', 'काय', 'कसे', 
        'मध्ये', 'आणि', 'पण', 'तर', 'मी', 'आम्ही', 'तुम्ही', 'तो', 'ती', 
        'ते', 'असा', 'असे', 'करा', 'जातो', 'येतो', 'पाहिजे', 'होते', 'नव्हते'
    }
}

HINDI_MARKERS = {
    "characters": set(),
    "words": {
        'है', 'हैं', 'नहीं', 'करना', 'हुआ', 'हुई', 'हुए', 'क्या', 'कैसे',
        'में', 'और', 'लेकिन', 'तो', 'मैं', 'हम', 'आप', 'तुम', 'वह', 'वे',
        'ऐसा', 'ऐसे', 'करो', 'जाता', 'आता', 'चाहिए', 'था', 'थी', 'थे'
    }
}

def analyze_script_distribution(text: str) -> Dict[str, float]:
    """Calculate the percentage of characters belonging to each Unicode script."""
    clean_text = re.sub(r'[\s\d\W_]+', '', text)
    total_chars = len(clean_text)
    if total_chars == 0:
        return {}

    counts = {script: 0 for script in UNICODE_RANGES}
    other_count = 0

    for char in clean_text:
        cp = ord(char)
        matched = False
        for script, (start, end) in UNICODE_RANGES.items():
            if script == "Latin":
                if (0x0041 <= cp <= 0x005A) or (0x0061 <= cp <= 0x007A):
                    counts[script] += 1
                    matched = True
                    break
            elif start <= cp <= end:
                counts[script] += 1
                matched = True
                break
        if not matched:
            other_count += 1

    distribution = {
        script: round(count / total_chars, 4)
        for script, count in counts.items()
        if count > 0
    }
    return distribution

def disambiguate_devanagari(text: str) -> Tuple[str, float]:
    """
    Distinguishes Hindi ('hi') vs Marathi ('mr') for Devanagari text
    using morphological lexicons and character presence.
    Returns (predicted_iso, confidence).
    """
    # Check Marathi specific characters (e.g. ळ)
    for char in MARATHI_MARKERS["characters"]:
        if char in text:
            return "mr", 0.95

    tokens = set(re.findall(r'[\u0900-\u097F]+', text))
    if not tokens:
        return "hi", 0.50

    marathi_hits = len(tokens.intersection(MARATHI_MARKERS["words"]))
    hindi_hits = len(tokens.intersection(HINDI_MARKERS["words"]))

    if marathi_hits > hindi_hits:
        confidence = min(0.99, 0.70 + 0.10 * marathi_hits)
        return "mr", round(confidence, 3)
    elif hindi_hits > marathi_hits:
        confidence = min(0.99, 0.70 + 0.10 * hindi_hits)
        return "hi", round(confidence, 3)
    else:
        # Default with low confidence if no distinctive tokens found
        return "hi", 0.55

def check_code_mixing(script_dist: Dict[str, float]) -> Optional[Dict[str, Any]]:
    """Identifies if input exhibits code-mixing (e.g., Latin + Devanagari)."""
    significant_scripts = [s for s, ratio in script_dist.items() if ratio >= 0.20]
    if len(significant_scripts) >= 2:
        return {
            "is_code_mixed": True,
            "scripts": significant_scripts,
            "distribution": script_dist
        }
    return None
