# CHAPTER 3 – SYSTEM ANALYSIS

## 3.1 Existing System Overview & Limitations

In the current technological landscape, automated translation is predominantly governed by multinational cloud software offerings (e.g., Google Translate, Microsoft Azure Cognitive Services, Amazon Translate). While commercially sophisticated, an in-depth analysis of these platforms within the context of Indian linguistic and academic requirements reveals critical structural bottlenecks:

1. **Monolithic Cloud-Dependent Architecture:** Existing systems require perpetual, high-bandwidth internet connectivity to remote proprietary servers. Edge deployment or disconnected on-premises operation is impossible.
2. **Proprietary Black-Box Abstraction:** Commercial APIs do not expose internal acoustic confidence, token-level attention weights, or model architecture parameters. Academic researchers cannot quantify individual module loss, intermediate representations, or architectural bottlenecks.
3. **Compound Pivoting Degradation:** Most commercial systems utilize English as an intermediate vehicular language ($\text{Source} \rightarrow \text{English} \rightarrow \text{Target}$). In translating between two structurally similar Indian languages (e.g., Marathi and Gujarati, both SOV), English pivoting forces an intermediate SOV $\rightarrow$ SVO $\rightarrow$ SOV transformation. This induces severe grammatical errors, loss of culturally specific honorifics, and awkward phrasing.
4. **Fragility to Acoustic Ambient Noise:** Consumer translation apps assume quiet speech environments with high Signal-to-Noise Ratios (SNR). In real-world Indian acoustic environments (bustling streets, public transit, railway stations), lack of dedicated spectral noise filtering leads to catastrophic ASR hallucinations or dropped phonemes.
5. **Subscription & Licensing Costs:** Commercial cloud APIs charge recurring pay-per-character and pay-per-second fees, creating financial barriers for non-profit, public sector, and educational deployments.

---

## 3.2 Proposed System: BhashaAI

**BhashaAI** addresses these limitations by introducing a completely open, modular, deep-learning-driven voice translation architecture specifically engineered for 10 scheduled Indian languages. 

### Key Innovations of the Proposed System:
- **Direct Modular Pipeline:** Decoupled microservices for Audio DSP, Speech-to-Text (ASR), Language Identification (LID), Neural Machine Translation (NMT), and Text-to-Speech (TTS).
- **Direct Multilingual Translation:** Incorporating Meta NLLB-200 and AI4Bharat IndicTrans2 representations to support direct Indic-to-Indic translation pathways without compulsory English pivoting.
- **Embedded Audio Signal Processing:** Integrated spectral noise reduction (`noisereduce`), silence trimming, and 16 kHz mono normalization prior to acoustic modeling.
- **Microsecond Latency Profiling:** Fine-grained telemetry capturing execution durations across each stage ($T_{\text{DSP}}, T_{\text{ASR}}, T_{\text{LID}}, T_{\text{NMT}}, T_{\text{TTS}}$) stored directly in the relational database.
- **Hardware-Aware CPU Optimization:** Model selection calibrated for execution on standard 8GB RAM CPU workstations via lazy loading, float32/bfloat16 precision management, and lightweight distilled checkpoints.
- **Full-Stack SaaS Implementation:** Modern responsive frontend (React, TypeScript, Tailwind CSS) communicating with an asynchronous, high-throughput backend (FastAPI, SQLAlchemy 2.0, PostgreSQL 18).

---

## 3.3 Comparative Analysis: Existing vs. Proposed System

| Feature / Dimension | Existing Commercial Systems (Google/Azure/AWS) | Proposed BhashaAI System |
|:---|:---|:---|
| **Underlying Architecture** | Proprietary cloud black-box | Open, modular, inspectable deep neural pipeline |
| **Translation Pathway** | Compulsory English Pivot ($\text{L}_1 \rightarrow \text{EN} \rightarrow \text{L}_2$) | Direct Indic-to-Indic and Indic-to-English pathways |
| **Noise Resilience** | Basic client AGC; degrades under low SNR | Embedded spectral subtraction & silence trimming |
| **Hardware Footprint** | Massive hyperscale GPU clusters required | Optimized for 8GB RAM CPU-only workstations |
| **Language Identification** | Heuristic or cloud-only | Multi-stage: Unicode block + n-gram + Devanagari morphological disambiguation |
| **Academic Observability** | No access to metrics or intermediate stages | Full observability: WER, CER, BLEU, chrF++, and stage latency metrics |
| **Cost & Licensing** | Recurring API subscription costs | 100% open-source models (MIT, CC-BY-NC 4.0, Apache 2.0) |
| **User Privacy & Governance**| Audio and transcripts uploaded to external clouds | On-premises execution; data retained within local PostgreSQL instance |

---

## 3.4 Stakeholder & User Persona Analysis

1. **Vernacular Speakers & Citizens (Primary End-Users):**
   - *Needs:* Simple, intuitive voice-driven interface; zero requirement to type complex scripts; natural audio output; instant language switching.
   - *Challenges:* Low English literacy; varied regional accents; noisy recording environments.
2. **Healthcare & Public Administration Workers (Secondary Users):**
   - *Needs:* Accurate, reliable translation of critical advisory instructions (e.g., medical dosages, civic announcements) across state linguistic boundaries.
3. **Academic Researchers & Evaluators (Tertiary Stakeholders):**
   - *Needs:* Transparent access to benchmark datasets, empirical evaluation runs, WER/BLEU telemetry, and model architectural parameters.

---

## 3.5 System Feasibility Study

### 3.5.1 Technical Feasibility
The technical feasibility is validated through the successful execution of Phase 1 and Phase 2 implementations:
- **ASR Feasibility:** OpenAI Whisper (`whisper-small` / `base`) operates seamlessly on an Intel 6-Core CPU using PyTorch, requiring ~1.2–1.5 GB RAM and transcribing 5-second utterances within 1.1–1.4 seconds.
- **NMT Feasibility:** Meta NLLB-200 (`nllb-200-distilled-600M`) requires ~2.2 GB RAM in memory. Sequence generation with beam size 2–4 produces accurate translations across all 10 target languages in ~750–850 ms.
- **TTS Feasibility:** Meta MMS-TTS (VITS) checkpoints (~140 MB on disk, ~350 MB RAM) synthesize audio in ~450–500 ms on CPU. Combined with gTTS fallback, speech generation is 100% dependable.
- **Total Memory Footprint:** The entire pipeline operates comfortably within a ~4.8 GB RAM ceiling, leaving ample margin within the physical 8 GB system budget.

### 3.5.2 Operational Feasibility
The web-based user interface leverages modern HTML5 standards (`MediaRecorder` API) to capture audio directly from mobile and desktop microphones without requiring browser plugins. The user interface provides clear visual cues (recording pulses, step progress indicators, waveform audio playback), ensuring operational feasibility for users of any technical skill level.

### 3.5.3 Economic Feasibility
BhashaAI eliminates proprietary cloud API costs. All core models and software libraries utilized (Whisper, NLLB-200, MMS-TTS, FastAPI, PostgreSQL, React, Vite) are open-source. Infrastructure costs are limited to the hosting server or local workstation hardware, yielding near-zero marginal operational cost per translation transaction.

### 3.5.4 Legal and Ethical Feasibility
All models and libraries adhere to their respective open-source licenses:
- OpenAI Whisper: MIT License.
- Meta NLLB-200: Creative Commons Attribution-NonCommercial 4.0 (CC-BY-NC 4.0).
- Meta MMS-TTS: CC-BY-NC 4.0.
- FastAPI, PostgreSQL, React: MIT / PostgreSQL Open License.
The system protects user privacy by processing audio locally without routing data to third-party ad networks or unauthorized surveillance pipelines.

---

## 3.6 Requirement Specifications

### 3.6.1 Functional Requirements (FR)
- **FR-01 (Audio Acquisition):** The system shall record live voice input via browser microphone (`audio/webm`, `audio/wav`) or accept manual audio uploads up to 25 MB.
- **FR-02 (Signal Preprocessing):** The system shall validate audio headers, resample to 16 kHz mono, normalize amplitude to $[-1.0, 1.0]$, trim silence below $-35\text{ dBFS}$, and optionally apply spectral noise reduction.
- **FR-03 (Speech-to-Text):** The system shall transcribe speech into text using an end-to-end ASR model and return word-level or sentence-level hypotheses.
- **FR-04 (Language Identification):** The system shall automatically identify the spoken or written language from audio/text across the 10 supported languages and flag unconfident detections.
- **FR-05 (Devanagari Disambiguation):** The system shall disambiguate Hindi vs. Marathi for text written in the Devanagari script using morphological heuristic token matching.
- **FR-06 (Neural Translation):** The system shall translate source text into the selected target language using Transformer sequence-to-sequence translation models.
- **FR-07 (Speech Synthesis):** The system shall synthesize translated text into intelligible acoustic waveforms, save the audio to disk, and provide an endpoint for streamable playback and download.
- **FR-08 (Orchestrated Pipeline):** The system shall execute the complete end-to-end pipeline ($\text{Audio} \rightarrow \text{DSP} \rightarrow \text{ASR} \rightarrow \text{LID} \rightarrow \text{NMT} \rightarrow \text{TTS} \rightarrow \text{Audio}$) via a single unified API endpoint.
- **FR-09 (User Authentication):** The system shall provide secure user registration, bcrypt password hashing, and JWT token-based authentication.
- **FR-10 (Translation History):** Authenticated users shall be able to browse, search, filter, play back, and delete historical translation records.
- **FR-11 (Academic Benchmarking):** The system shall provide an independent evaluation harness computing WER, CER, BLEU, and chrF++ across parallel evaluation corpora.
- **FR-12 (Performance Analytics):** The system shall expose analytical dashboards visualizing empirical metrics, latency decompositions, and noise robustness comparisons.

### 3.6.2 Non-Functional Requirements (NFR)
- **NFR-01 (Latency):** Total end-to-end translation latency on an Intel 6-Core CPU for a 5-second audio input shall not exceed 3.5 seconds.
- **NFR-02 (Memory Utilization):** The entire backend application including loaded neural models shall operate within 6.0 GB RAM.
- **NFR-03 (Reliability & Fallback):** If primary neural TTS encounters an out-of-vocabulary exception, the system shall gracefully fall back to alternative synthesis without failing the transaction.
- **NFR-04 (Security):** All user credentials must be salted and hashed using `bcrypt`. API communication must enforce Bearer token verification and strict CORS domain origins.
- **NFR-05 (Maintainability):** Codebase must maintain strict separation of concerns (FastAPI routers, Pydantic schemas, SQLAlchemy ORM models, ML service singletons).
- **NFR-06 (Portability):** System must run across modern operating systems (Windows 10/11, Ubuntu Linux 22.04+, macOS) supporting Python 3.10+ and Node.js 18+.
- **NFR-07 (Responsiveness):** The web frontend must adapt fluidly to desktop (1920x1080), tablet (768x1024), and mobile (375x667) viewports.
- **NFR-08 (Test Coverage):** Backend services must maintain 100% pass rate across automated unit, integration, and regression test suites.

---

## 3.7 Hardware and Software Specifications

### Development & Benchmarking Environment
- **Host Operating System:** Microsoft Windows 10 Pro (x64-based PC)
- **Central Processing Unit (CPU):** Intel(R) Core(TM) i5-8400 CPU @ 2.80GHz (6 Cores, 6 Logical Processors)
- **Physical Memory (RAM):** 8.00 GB DDR4 (7.87 GB Usable)
- **Storage:** 512 GB Solid State Drive (NVMe SSD)
- **Dedicated Graphics (GPU):** None (CPU execution mode strictly verified)
- **Python Runtime:** Python 3.14.6 x64
- **Node.js Runtime:** Node.js v24.15.0 / npm v11.12.1
- **Relational Database:** PostgreSQL 18.0 x64 (Port 5432)

### Target Client Environment (Web Browser)
- **Supported Browsers:** Google Chrome 90+, Mozilla Firefox 88+, Microsoft Edge 90+, Apple Safari 14.1+
- **Required Browser APIs:** Web Audio API, MediaStream Recording API (`MediaRecorder`), Fetch API, HTML5 Audio Element
- **Minimum Client RAM:** 2.0 GB RAM
- **Audio Hardware:** Any integrated or peripheral microphone and speaker/headphone hardware.
