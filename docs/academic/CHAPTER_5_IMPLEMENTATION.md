# CHAPTER 5 – IMPLEMENTATION

## 5.1 Technology Stack Justification

The implementation of BhashaAI was engineered around high computational efficiency, low CPU memory consumption, strict modularity, and rapid user responsiveness:

| Component | Selected Technology | Technical Justification |
|:---|:---|:---|
| **Programming Language** | Python 3.14.6 | Standard scientific computing ecosystem, mature bindings for PyTorch, Hugging Face, SciPy, and Librosa. |
| **Backend Framework** | FastAPI (ASGI) | Native asynchronous coroutines (`async/await`), high throughput, automatic OpenAPI documentation, strict Pydantic V2 data validation. |
| **Deep Learning Framework** | PyTorch 2.1+ / Transformers 4.40+ | Industry-standard neural network framework supporting lazy checkpoint loading, bfloat16/float32 precision, and CPU vectorized tensor operations. |
| **Relational Database** | PostgreSQL 18.0 | ACID compliance, rock-solid referential integrity, performant text searching, and native JSON storage support. |
| **Database ORM & Migrations** | SQLAlchemy 2.0 & Alembic | Explicit declarative data models, connection pooling, and version-controlled migration tracking. |
| **Frontend Framework** | React 18 + TypeScript | Component-based reactivity, compile-time type safety preventing runtime null pointer dereferences. |
| **Build Tooling & Bundler** | Vite 8 | Instant Hot Module Replacement (HMR), lightning-fast Rollup-based tree-shaking and production compilation. |
| **Styling Architecture** | Tailwind CSS v4 | Zero runtime CSS overhead, utility-first responsiveness, and cohesive design tokens. |
| **Data Visualization** | Recharts 2 | SVG-based responsive charting for ML empirical distributions and latency telemetry. |

---

## 5.2 Backend Core Module Implementation

### 5.2.1 Audio Signal Processing (`AudioProcessor`)
Located in `backend/app/services/asr/audio_processor.py`, the `AudioProcessor` class executes critical digital signal processing transformations prior to feeding audio to neural networks:
- **Format Validation:** Inspects raw file magic bytes and MIME types, verifying compatibility across WAV, WebM, MP3, FLAC, and OGG formats.
- **Resampling via Sinc Interpolation:** Resamples variable input frequencies (e.g., 44.1 kHz, 48 kHz browser streams) to a strict 16,000 Hz sample rate required by Whisper:

$$y[n] = \sum_{k} x[k] \cdot \text{sinc}\left(\frac{t_n - t_k}{T}\right)$$

- **Mono Channel Conversion:** Averages multi-channel stereo or quad-channel audio into a single-channel array: $x_{\text{mono}}[n] = \frac{1}{C}\sum_{c=1}^C x_c[n]$.
- **Peak Amplitude Normalization:** Normalizes signals to $[-1.0, 1.0]$ using maximum absolute scaling: $x_{\text{norm}}[n] = \frac{x[n]}{\max(|x|) + \epsilon}$.
- **Silence Energy Trimming:** Computes short-term Root-Mean-Square (RMS) frame energies:

$$\text{RMS}_i = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} x_i[n]^2}$$

Frames below $-35\text{ dBFS}$ are trimmed to eliminate unvoiced padding.
- **Spectral Noise Subtraction:** Implements non-stationary spectral noise subtraction via the `noisereduce` algorithm, estimating stationary noise spectral profiles from the initial 200 ms of audio and subtracting them from the STFT magnitude spectrum.

### 5.2.2 Automatic Speech Recognition (`ASRService`)
Located in `backend/app/services/asr/service.py`, `ASRService` manages the speech-to-text inference pipeline:
- **Lazy Singleton Instantiation:** Avoids loading large neural weights during server boot. The model is initialized into memory upon the first transcription request.
- **Quantized CPU Inference:** Loads `openai/whisper-small` (or `base`) via Hugging Face `transformers.pipeline`, configured with float32 computation on CPU.
- **Chunked Processing:** Employs 30-second sliding audio window chunks with 2-second cross-fading, ensuring arbitrary-length speech files can be transcribed without out-of-memory exceptions.

### 5.2.3 Language Identification & Script Disambiguation (`LanguageDetector`)
Located in `backend/app/services/language_detection/service.py`, the language detection module operates as a three-stage hierarchical classifier:
1. **Unicode Script Range Matching:** Analyzes character frequency distributions against distinct Brahmic script blocks:
   - Bengali (`0x0980` - `0x09FF`)
   - Gurmukhi (`0x0A00` - `0x0A7F`)
   - Gujarati (`0x0A80` - `0x0AFF`)
   - Tamil (`0x0B80` - `0x0BFF`)
   - Telugu (`0x0C00` - `0x0C7F`)
   - Kannada (`0x0C80` - `0x0CFF`)
   - Malayalam (`0x0D00` - `0x0D7F`)
2. **Devanagari Morphological Disambiguation:** When text falls within the Devanagari range (`0x0900` - `0x097F`), it may represent either Hindi or Marathi. The engine performs token-level matching against Marathi-specific functional tokens (e.g., आहे, नाही, च्या, साठी, करतो, जातो, होतो). If threshold frequency $\theta_{\text{marathi}} \ge 0.15$, the text is classified as Marathi (`mr`); otherwise, it defaults to Hindi (`hi`).
3. **Statistical n-gram Fallback:** For Latin script or ambiguous inputs, the engine queries the `langdetect` library, computing posterior n-gram probabilities over character tri-grams.

### 5.2.4 Neural Machine Translation (`TranslationService`)
Located in `backend/app/services/translation/service.py`:
- **Model Checkpoint:** Meta's `facebook/nllb-200-distilled-600M` serves as the primary direct translation engine, backed by architecture support for `ai4bharat/indictrans2-indic-indic-dist-320M`.
- **Language Code Resolution:** Translates standard ISO 639-1 language codes (`hi`, `ta`, `gu`) to BCP-47 / Flores-200 script tags (`hin_Deva`, `tam_Taml`, `guj_Gujr`, `eng_Latn`).
- **Generation Parameters:** Configured with beam search ($k=3$), length penalty ($\alpha=1.0$), and maximum new tokens ($T_{\max}=256$), producing syntactically coherent translations with minimal repetition.

### 5.2.5 Text-to-Speech Synthesis (`TTSService`)
Located in `backend/app/services/tts/service.py`:
- **Neural Architecture:** Deploys Meta MMS-TTS checkpoints based on VITS (Conditional VAE with Adversarial Learning).
- **Phonemization & Waveform Synthesis:** The text is mapped to language-specific phoneme representations, passed through normalizing flow layers, and rendered directly into a 16 kHz time-domain floating-point waveform.
- **Fail-Safe Fallback:** If a target language checkpoint experiences an unsupported character exception, execution gracefully transitions to `gTTS` synthesis, ensuring 100% synthesis uptime.
- **Persistence:** Generated speech arrays are written to `storage/audio/generated/{uuid}.wav` with full metadata recorded in PostgreSQL.

### 5.2.6 End-to-End Orchestrator (`VoiceTranslationPipeline`)
Located in `backend/app/services/pipeline.py`, this master orchestrator executes the complete pipeline:

```python
# Conceptual execution flow in VoiceTranslationPipeline
t_start = time.perf_counter()
pcm_audio, dsp_time = audio_processor.process(raw_bytes, denoise=apply_denoise)
recognized_text, asr_time = asr_service.transcribe(pcm_audio)
source_lang, lid_time = language_detector.identify(recognized_text, fallback=source_hint)
translated_text, nmt_time = translation_service.translate(recognized_text, source_lang, target_lang)
audio_path, tts_time = tts_service.synthesize(translated_text, target_lang)
t_total = (time.perf_counter() - t_start) * 1000.0
```

---

## 5.3 Database Schema & Migration Implementation

Database state is governed through SQLAlchemy 2.0 models and Alembic version tracking:
- **Connection Engine:** Initialized in `backend/app/db/session.py` with thread-safe pooling (`pool_pre_ping=True`, `pool_size=10`).
- **Alembic Version `388c8d1d9533`:** Migration scripts explicitly create indices on `users.email`, `translation_records.user_id`, and `languages.code_iso_639_1`.
- **Cascade Rules:** Foreign keys between `users` and `translation_records` enforce `ON DELETE CASCADE`, preventing orphaned translation records.

---

## 5.4 Frontend Implementation Architecture

The frontend application (`frontend/src/`) delivers a responsive, single-page application experience:
- **Microphone Capture:** Uses `navigator.mediaDevices.getUserMedia({ audio: true })` and `MediaRecorder` API to stream audio into an in-memory `Blob` array of type `audio/webm;codecs=opus`.
- **Dual-Pane Translation Studio:** `TranslatorPage.tsx` manages language selection dropdowns, recording timers, drag-and-drop file uploaders, and progressive status steppers (`uploading` $\rightarrow$ `recognizing` $\rightarrow$ `detecting` $\rightarrow$ `translating` $\rightarrow$ `synthesizing` $\rightarrow$ `completed`).
- **Real-Time Telemetry Display:** `TranslationResultCard.tsx` renders decomposed millisecond latency badges alongside copy-to-clipboard buttons and interactive audio players.
- **Interactive Benchmarking Dashboard:** `PerformancePage.tsx` integrates Recharts to visualize multilingual BLEU scores, chrF++ evaluations, SNR-dependent Word Error Rates, and stage latency distributions.

---

## 5.5 Challenges Encountered & Technical Solutions

1. **Python 3.14 Compatibility with PyTorch JIT:**
   - *Challenge:* Python 3.14 deprecated `torch.jit.script` in favor of `torch.compile` / `torch.export`, throwing deprecation warnings.
   - *Solution:* Standardized neural forward passes on standard PyTorch eager module evaluation, avoiding deprecated JIT script annotations.
2. **`jiwer` 3+ API Signature Changes:**
   - *Challenge:* `jiwer.wer()` changed parameter names from `references` and `hypotheses` (plural) to `reference` and `hypothesis` (singular).
   - *Solution:* Refactored `ml/evaluation/asr_evaluator.py` to match the singular parameter interface, ensuring seamless evaluation runs.
3. **TypeScript Strict Type Checks on Node Timers:**
   - *Challenge:* Under Vite's browser TypeScript compilation (`noUnusedLocals: true`), referencing `NodeJS.Timeout` failed because Node ambient types are omitted in browser environments.
   - *Solution:* Refactored timer references to `useRef<any>(null)` and cleaned up unused lucide icons across all component files.
4. **Devanagari Script Ambiguity:**
   - *Challenge:* Standard language detectors frequently misclassified Marathi input as Hindi due to identical Unicode character blocks.
   - *Solution:* Formulated a custom Marathi morphological heuristic module checking high-frequency verbal and postpositional Marathi markers.
