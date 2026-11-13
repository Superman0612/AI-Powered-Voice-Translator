# BhashaAI ML Datasets & Benchmark Methodology

## 1. Dataset Identification & Research

For the Indian multilingual voice translation task, the following academic corpora were evaluated:

### 1. AI4Bharat IndicVoices / IndicSUPERB / IN22
- **Source:** AI4Bharat (IIT Madras / EkStep Foundation)
- **License:** CC-BY 4.0 / MIT
- **Coverage:** 22 scheduled Indian languages.
- **Role in BhashaAI:** Ground truth parallel evaluation sets and acoustic evaluation references.

### 2. Meta FLORES-200 / NLLB Benchmark
- **Source:** Meta AI Research
- **License:** CC-BY-SA 4.0
- **Coverage:** All 10 BhashaAI target languages (`hin_Deva`, `eng_Latn`, `guj_Gujr`, `mar_Deva`, `ben_Beng`, `tam_Taml`, `tel_Telu`, `kan_Knda`, `mal_Mlym`, `pan_Guru`).
- **Role in BhashaAI:** Machine translation quality assessment using standardized professional human translations.

### 3. OpenSLR & Google FLEURS
- **Source:** OpenSLR (Open Speech and Language Resources) / Google Research
- **License:** Apache 2.0 / CC-BY 4.0
- **Coverage:** Multilingual speech recordings across major Indic languages.

---

## 2. Benchmark Corpus Details (`ml/datasets/test_multilingual_corpus.json`)

To prevent storage exhaustion on the target system (leaving ~51 GB intact), BhashaAI packages a verified, multi-parallel gold test set covering all 10 languages across key conversational domains:
1. **General Greetings & Introductions**
2. **Technology & Artificial Intelligence**
3. **Travel & Transit Assistance**
4. **Education & National Development**
5. **Healthcare & Wellness Advisories**

### Preprocessing & Text Normalization Steps
1. **Unicode NFC Canonical Normalization:** Converts decomposed Unicode code points into precomposed representations.
2. **Punctuation Alignment:** Standardizes western periods `.` and Indic danda `।` (Purna Viram) to prevent tokenization penalties.
3. **Whitespace Pruning:** Strips non-breaking spaces and zero-width joiners (ZWJ) where appropriate.

---

## 3. Evaluation Metrics Formulation

### A. Automatic Speech Recognition (ASR)
$$\text{WER} = \frac{S + D + I}{N} = \frac{\text{Substitutions} + \text{Deletions} + \text{Insertions}}{\text{Reference Word Count}}$$

$$\text{CER} = \frac{S_c + D_c + I_c}{N_c} = \frac{\text{Character Errors}}{\text{Reference Character Count}}$$

### B. Neural Machine Translation (NMT)
- **BLEU (Bilingual Evaluation Understudy):** Geometric mean of modified n-gram precisions multiplied by brevity penalty (BP).
- **chrF++ (Character n-gram F-score):** Balances character precision and recall, especially vital for Indic languages with complex agglutinative morphology (e.g., Tamil, Telugu, Malayalam).

### C. Latency Profiling
- **End-to-End Latency:** $T_{\text{total}} = T_{\text{DSP}} + T_{\text{ASR}} + T_{\text{LID}} + T_{\text{NMT}} + T_{\text{TTS}}$
- Measured with microsecond resolution using `time.perf_counter()`.

