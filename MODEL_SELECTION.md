# BhashaAI – Model Selection & Architectural Evaluation

## 1. Executive Summary & Environment Constraints

BhashaAI is an AI-powered voice translator designed for Indian languages as part of an MCA Final Year Project (AI & Machine Learning specialization).

### Physical Environment Specification
- **Operating System:** Microsoft Windows 10 Pro (x64-based PC)
- **Processor:** Intel 6-Core (Coffee Lake Family 6 Model 158 Stepping 10)
- **GPU:** None (CPU-Only inference)
- **Total Physical Memory (RAM):** 8,192 MB (~7.98 GB detected, ~1.1 GB available at baseline)
- **Storage:** 150.33 GB total, ~51.82 GB available NVMe/SSD space
- **Python Runtime:** Python 3.14.6
- **Deep Learning Framework:** PyTorch 2.13.0+cpu, HuggingFace Transformers 5.14.1
- **Database Engine:** PostgreSQL 18 Server (Running on localhost:5432)

Given the absence of a dedicated CUDA GPU and a constrained 8 GB memory boundary, model selection must balance state-of-the-art accuracy with lightweight CPU inference, lazy loading, and robust script handling.

---

## 2. Target Language Matrix (10 Scheduled Languages)

| Language | ISO 639-1 / 639-3 | Script | IndicTrans2 Code | NLLB-200 Code | Whisper Code | MMS-TTS Code |
|---|---|---|---|---|---|---|
| **Hindi** | `hi` / `hin` | Devanagari | `hin_Deva` | `hin_Deva` | `hi` | `facebook/mms-tts-hin` |
| **English** | `en` / `eng` | Latin | `eng_Latn` | `eng_Latn` | `en` | `facebook/mms-tts-eng` |
| **Gujarati** | `gu` / `guj` | Gujarati | `guj_Gujr` | `guj_Gujr` | `gu` | `facebook/mms-tts-guj` |
| **Marathi** | `mr` / `mar` | Devanagari | `mar_Deva` | `mar_Deva` | `mr` | `facebook/mms-tts-mar` |
| **Bengali** | `bn` / `ben` | Bengali-Assamese | `ben_Beng` | `ben_Beng` | `bn` | `facebook/mms-tts-ben` |
| **Tamil** | `ta` / `tam` | Tamil | `tam_Taml` | `tam_Taml` | `ta` | `facebook/mms-tts-tam` |
| **Telugu** | `te` / `tel` | Telugu | `tel_Telu` | `tel_Telu` | `te` | `facebook/mms-tts-tel` |
| **Kannada** | `kn` / `kan` | Kannada | `kan_Knda` | `kan_Knda` | `kn` | `facebook/mms-tts-kan` |
| **Malayalam** | `ml` / `mal` | Malayalam | `mal_Mlym` | `mal_Mlym` | `ml` | `facebook/mms-tts-mal` |
| **Punjabi** | `pa` / `pan` | Gurmukhi | `pan_Guru` | `pan_Guru` | `pa` | `facebook/mms-tts-pan` |

---

## 3. Automatic Speech Recognition (ASR) Candidate Evaluation

### Evaluated Candidates
1. **OpenAI Whisper (`openai/whisper-small` / `openai/whisper-base`):**
   - *Architecture:* Sequence-to-sequence Transformer with 80-channel log Mel-filterbank encoder.
   - *Parameters:* `small` (244M params, ~480MB disk, ~1.2-1.5 GB RAM); `base` (74M params, ~145MB disk, ~500MB RAM).
   - *License:* MIT License (Permissive Open Source).
   - *Language Coverage:* Natively supports all 10 target Indian languages.
   - *CPU Viability:* Outstanding on 6-core Intel CPU when integrated with HuggingFace `pipeline("automatic-speech-recognition")`.
   - *Status:* **SELECTED (Primary: `openai/whisper-small`, Dynamic Fallback: `openai/whisper-base`)**.

2. **AI4Bharat IndicConformer (`ai4bharat/indic-conformer-600m-multilingual` / IndicWhisper):**
   - *Architecture:* Conformer CTC/RNNT.
   - *License:* MIT / CC-BY 4.0.
   - *Limitations:* Requires AI4Bharat's customized NVIDIA NeMo fork (`nemo-v2`). Heavy C++ dependencies (fairseq, hydra-core, omegaconf) which fail to compile on Python 3.14 on Windows. Inference latency on CPU is non-trivial (~4x slower without TensorRT/CUDA).
   - *Status:* **REJECTED** due to Windows/Python 3.14 NeMo incompatibilities.

3. **faster-whisper (CTranslate2 Backend):**
   - *Architecture:* 8-bit quantized Whisper via CTranslate2.
   - *Status:* Investigated; `ctranslate2` lacks prebuilt binaries for Python 3.14 on Windows x64. Standard PyTorch HuggingFace Transformers pipeline utilized as primary.

---

## 4. Neural Machine Translation (NMT) Candidate Evaluation

### Evaluated Candidates
1. **Meta AI NLLB-200 (`facebook/nllb-200-distilled-600M`):**
   - *Architecture:* Shared encoder-decoder Transformer supporting 200+ languages.
   - *Parameters:* 600 Million (distilled). Disk: ~2.4 GB. RAM footprint: ~2.2 GB.
   - *License:* CC-BY-NC 4.0 (Non-commercial, strictly permissible for MCA Academic Projects).
   - *Language Coverage:* High-fidelity representations for all 10 languages: `hin_Deva`, `eng_Latn`, `guj_Gujr`, `mar_Deva`, `ben_Beng`, `tam_Taml`, `tel_Telu`, `kan_Knda`, `mal_Mlym`, `pan_Guru`.
   - *API Compatibility:* 100% native compatibility with `AutoModelForSeq2SeqLM` and `AutoTokenizer` in `transformers>=5.0` without auxiliary Cython libraries.
   - *Status:* **SELECTED (Primary General Multilingual Engine)**.

2. **AI4Bharat IndicTrans2 (`ai4bharat/indictrans2-en-indic-dist-200M`, `indic-en-dist-200M`, `indic-indic-dist-320M`):**
   - *Parameters:* 200M (En-Indic), 200M (Indic-En), 320M (Indic-Indic).
   - *License:* MIT.
   - *Advantages:* Superior BLEU (+4 to +8 points) on Indian vernacular domain nuances.
   - *Caveats:* Requires `IndicTransToolkit` (Cython) and separate models per direction.
   - *Status:* **SUPPORTED ARCHITECTURE** with lazy loading; modular NMT service abstracts provider so IndicTrans2 weights plug in directly.

3. **Helsinki-NLP / OPUS-MT (`opus-mt-en-hi`, etc.):**
   - *Parameters:* ~75M per bilingual pair.
   - *Status:* **REJECTED** due to absence of direct Indic-to-Indic models and fragmented language coverage across Dravidian pairs.

---

## 5. Text-to-Speech (TTS) Candidate Evaluation

### Evaluated Candidates
1. **Facebook MMS-TTS (Meta Massively Multilingual Speech - VITS):**
   - *Models:* `facebook/mms-tts-hin`, `mms-tts-eng`, `mms-tts-tam`, `mms-tts-tel`, `mms-tts-ben`, `mms-tts-guj`, `mms-tts-mar`, `mms-tts-kan`, `mms-tts-mal`, `mms-tts-pan`.
   - *Architecture:* Variational Inference with Adversarial Learning (VITS), neural vocoder included.
   - *Parameters:* ~36M per language (~145 MB disk).
   - *RAM Usage:* ~350 MB per active language model.
   - *License:* CC-BY-NC 4.0.
   - *CPU Viability:* Exceptional real-time generation (~1.2s for 15-word utterance on 6 cores).
   - *Status:* **SELECTED (Primary Local Neural TTS)**.

2. **Google Text-to-Speech (`gTTS` via standard HTTP fallback):**
   - *Coverage:* All 10 languages with high-fidelity prosody.
   - *Status:* **INTEGRATED (Secondary / Robust Network Fallback)**. Explicitly tagged in API response metadata (`engine: "gtts-fallback"` vs `engine: "mms-tts-local"`).

3. **Coqui XTTS-v2 & pyttsx3:**
   - *XTTS-v2:* Only supports Hindi among Indian languages; 1.8 GB memory footprint is unsuitable for concurrent CPU tasks.
   - *pyttsx3:* Windows SAPI5 lacks native Indic voice packs by default on standard installations.

---

## 6. Language Identification (LID) Candidate Evaluation

1. **`langdetect` (N-gram statistical profile + Unicode Block Heuristics):**
   - *Memory Footprint:* <5 MB.
   - *Execution Speed:* <15 ms.
   - *Accuracy:* Near 100% on native Indic scripts because each Indian language family (Devanagari, Bengali, Gujarati, Gurmukhi, Tamil, Telugu, Kannada, Malayalam) maps to distinct, non-overlapping Unicode blocks (U+0900 to U+0D7F).
   - *Devanagari Disambiguation (Hindi vs Marathi):* Augmented with lexicon and morphological markers (e.g., Marathi auxiliary verbs `आहे`, `नाही`, `करणे` vs Hindi `है`, `नहीं`, `करना`).
   - *Status:* **SELECTED (Primary Text LID with Script Heuristic Layer)**.

2. **Speech LID:** Audio-level language classification utilizes Whisper's integrated 99-language acoustic classifier (`whisper.detect_language`) on the 30-second Mel spectrogram.

---

## 7. Memory & Concurrency Budget (8 GB System RAM)

```
+-------------------------------------------------------------+
| Total System RAM: 8,192 MB                                  |
+-------------------------------------------------------------+
| [Base OS & Background Services]              : ~2,500 MB     |
| [PostgreSQL 18 Service + Connections]         : ~  300 MB     |
| [FastAPI Uvicorn Async Worker]               : ~  250 MB     |
| [Whisper Small ASR Model (Loaded on demand)] : ~1,400 MB     |
| [NLLB-200 600M NMT Model (Loaded on demand)] : ~2,200 MB     |
| [MMS-TTS Language Model (Loaded on demand)]  : ~  350 MB     |
| [Audio Buffers & Working Memory]             : ~  300 MB     |
+-------------------------------------------------------------+
| Peak Concurrent Usage: ~7,300 MB (Leaves ~890 MB headroom)   |
+-------------------------------------------------------------+
```

### Memory Management Strategy
1. **Singleton Lazy Loading:** Models are loaded into memory on the first request, not at server startup.
2. **Explicit Garbage Collection:** `gc.collect()` and PyTorch memory cleanup invoked after heavy batch processing.
3. **Model Warmth Caching:** Frequently used models remain in RAM; inactive models can be unloaded gracefully if memory pressure thresholds (>85%) are reached.

