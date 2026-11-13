# CHAPTER 4 – SYSTEM DESIGN

## 4.1 High-Level Architectural Design

BhashaAI is designed as a decoupled, multi-tier software architecture comprising five core layers:
1. **Presentation Layer (Client SPA):** React 18, TypeScript, Tailwind CSS, Vite single-page application providing responsive UI components, audio recording via the HTML5 `MediaRecorder` API, real-time waveform playback, and telemetry charts.
2. **API Gateway & Routing Layer:** FastAPI asynchronous ASGI application enforcing CORS security policies, JWT authentication validation, request rate limiting, and multipart form-data handling.
3. **Business Logic & Service Layer:** Independent singletons for audio signal processing, ASR orchestration, language identification, neural translation, speech synthesis, and pipeline aggregation.
4. **Deep Learning Inference Engine:** Deep neural networks running on PyTorch and Hugging Face Transformers (`Whisper`, `NLLB-200`, `MMS-TTS`, `gTTS`).
5. **Persistence & Storage Layer:** PostgreSQL 18 relational database engine managed via SQLAlchemy 2.0 ORM and Alembic schema migrations, alongside local disk storage for audio artifacts.

```mermaid
flowchart TD
    subgraph ClientLayer["Presentation Layer (Client SPA)"]
        UI["React 18 + TypeScript + Vite SPA"]
        Rec["HTML5 MediaRecorder API"]
        Audio["Web Audio Player"]
    end

    subgraph APILayer["API Gateway & Routing Layer (FastAPI)"]
        Router["FastAPI Application Router"]
        AuthMiddleware["JWT Authentication Guard"]
        CORSMiddleware["CORS Origin Validator"]
    end

    subgraph ServiceLayer["Service Layer (Decoupled Python Microservices)"]
        DSP["AudioProcessor (DSP / Denoise)"]
        ASR_Svc["ASRService (Whisper)"]
        LID_Svc["LanguageDetector (Script / n-gram)"]
        NMT_Svc["TranslationService (NLLB / IndicTrans)"]
        TTS_Svc["TTSService (VITS / MMS / gTTS)"]
        Pipe_Svc["VoiceTranslationPipeline (Orchestrator)"]
    end

    subgraph ModelLayer["Deep Learning Engine (PyTorch / Transformers)"]
        WhisperModel["OpenAI Whisper"]
        NLLBModel["Meta NLLB-200"]
        MMSModel["Meta MMS-TTS (VITS)"]
    end

    subgraph StorageLayer["Data & Persistence Layer"]
        PG["PostgreSQL 18 Relational DB"]
        Disk["Local Storage (WAV / WebM)"]
    end

    Rec -->|audio/webm stream| Router
    UI -->|JSON REST Requests| Router
    Router --> AuthMiddleware
    AuthMiddleware --> CORSMiddleware
    CORSMiddleware --> Pipe_Svc

    Pipe_Svc --> DSP
    DSP --> ASR_Svc
    ASR_Svc --> WhisperModel
    ASR_Svc --> LID_Svc
    LID_Svc --> NMT_Svc
    NMT_Svc --> NLLBModel
    NMT_Svc --> TTS_Svc
    TTS_Svc --> MMSModel
    TTS_Svc --> Disk

    Pipe_Svc --> PG
    Audio <-->|stream audio| Disk
```

---

## 4.2 Use Case Modeling

The system interacts with three primary actors:
- **Guest / Unregistered User:** Explores landing page, reviews supported language matrix, registers a new account, logs in.
- **Authenticated User:** Performs real-time speech recording, uploads audio files, triggers voice and text translations, reviews stage-by-stage latencies, listens to translated audio, downloads generated speech, and searches/filters translation history.
- **Academic Evaluator / Admin:** Executes automated evaluation harnesses, inspects WER/CER/BLEU metrics, reviews model registry specifications, and inspects database records.

```mermaid
flowchart LR
    User["Authenticated User"]
    Evaluator["Academic Evaluator"]
    SystemAdmin["System Admin"]

    UC1["UC-01: Record / Upload Speech"]
    UC2["UC-02: Execute Voice Translation"]
    UC3["UC-03: View Stage Latencies"]
    UC4["UC-04: Playback / Download Audio"]
    UC5["UC-05: Browse / Filter History"]
    UC6["UC-06: Run ML Evaluation Suite"]
    UC7["UC-07: Inspect Model Registry"]

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5

    Evaluator --> UC6
    Evaluator --> UC7
    SystemAdmin --> UC7
```

---

## 4.3 Data Flow Modeling

### 4.3.1 DFD Level 0 (Context Diagram)
The Context Diagram depicts the system boundary and fundamental data exchanges between external entities and BhashaAI.

```mermaid
flowchart LR
    User["End User (Browser)"]
    BhashaAI["BhashaAI System Gateway"]
    DB[("PostgreSQL 18 DB")]
    FS[("Local File Storage")]

    User -->|"Raw Audio / Text + Target Lang"| BhashaAI
    BhashaAI -->|"Translated Text + Audio Stream + Latency"| User
    BhashaAI -->|"Metadata & History Logs"| DB
    DB -->|"User Profile & Translation Records"| BhashaAI
    BhashaAI -->|"Write WAV / WebM Files"| FS
    FS -->|"Read Audio Stream"| BhashaAI
```

### 4.3.2 DFD Level 1 (Detailed Voice Pipeline Flow)
The Level 1 diagram decomposes the voice translation pipeline into its discrete transformation processes.

```mermaid
flowchart TD
    P1["1.0 Audio Acquisition & Validation"]
    P2["2.0 DSP Preprocessing & Denoise"]
    P3["3.0 Acoustic Speech Recognition (ASR)"]
    P4["4.0 Language Identification & Disambiguation"]
    P5["5.0 Neural Machine Translation (NMT)"]
    P6["6.0 Speech Synthesis (TTS)"]
    P7["7.0 Telemetry & History Logging"]

    InputAudio["Input Audio (WebM/WAV)"] --> P1
    P1 -->|"Validated Buffer"| P2
    P2 -->|"16kHz Float32 Mono Array"| P3
    P3 -->|"Recognized Text Hypothesis"| P4
    P4 -->|"Source Language Code"| P5
    P5 -->|"Translated Target Text"| P6
    P6 -->|"Synthesized WAV Audio"| P7
    P7 --> Output["Client JSON Response + Audio Stream URL"]
```

---

## 4.4 Entity-Relationship (ER) Design

The relational database model comprises 7 normalized tables designed to ensure referential integrity, eliminate data redundancy, and index search queries:

```mermaid
erDiagram
    USERS ||--o{ TRANSLATION_RECORDS : "initiates"
    USERS ||--o{ AUDIO_FILES : "uploads"
    LANGUAGES ||--o{ TRANSLATION_RECORDS : "source_lang"
    LANGUAGES ||--o{ TRANSLATION_RECORDS : "target_lang"
    AUDIO_FILES ||--o{ TRANSLATION_RECORDS : "input_audio"
    AUDIO_FILES ||--o{ TRANSLATION_RECORDS : "output_audio"
    EVALUATION_RUNS ||--o{ EVALUATION_RESULTS : "contains"
    MODEL_REGISTRY ||--o{ EVALUATION_RESULTS : "evaluated_in"

    USERS {
        int id PK
        string email UK
        string username UK
        string hashed_password
        string full_name
        boolean is_active
        datetime created_at
    }

    LANGUAGES {
        int id PK
        string code_iso_639_1 UK
        string code_iso_639_3 UK
        string name
        string native_name
        string script_name
        string nllb_code
        string indictrans_code
        string whisper_code
        boolean supports_asr
        boolean supports_nmt
        boolean supports_tts
    }

    AUDIO_FILES {
        int id PK
        int user_id FK
        string file_path
        string original_filename
        string format
        float duration_seconds
        int sample_rate
        int channels
        int file_size_bytes
        datetime created_at
    }

    TRANSLATION_RECORDS {
        int id PK
        int user_id FK
        string source_language
        string target_language
        string original_text
        string translated_text
        int input_audio_id FK
        int output_audio_id FK
        float asr_duration_ms
        float nmt_duration_ms
        float tts_duration_ms
        float total_duration_ms
        datetime created_at
    }

    MODEL_REGISTRY {
        int id PK
        string task_type
        string model_name UK
        string huggingface_id
        string architecture
        int parameter_count
        string license
        boolean is_active
    }

    EVALUATION_RUNS {
        int id PK
        string run_name
        string description
        string dataset_name
        int total_samples
        datetime created_at
    }

    EVALUATION_RESULTS {
        int id PK
        int run_id FK
        int model_id FK
        string language_pair
        float metric_value
        string metric_name
        json details
    }
```

---

## 4.5 Sequence Modeling: End-to-End Voice Translation

The sequence diagram illustrates the synchronous and asynchronous messaging flow between the client application, API gateway, and internal ML processing components.

```mermaid
sequenceDiagram
    autonumber
    actor User as Client Browser
    participant API as FastAPI Gateway
    participant DSP as AudioProcessor
    participant ASR as ASRService (Whisper)
    participant LID as LanguageDetector
    participant NMT as TranslationService (NLLB)
    participant TTS as TTSService (MMS/gTTS)
    participant DB as PostgreSQL 18

    User->>API: POST /api/v1/translate/voice (Multipart audio file, target_lang)
    API->>DSP: validate_and_resample(file_bytes, target_sr=16000)
    DSP-->>API: normalized_pcm_array (float32, 16kHz)
    
    API->>ASR: transcribe(pcm_array)
    ASR-->>API: recognized_text, asr_latency_ms
    
    API->>LID: detect_language(recognized_text)
    LID-->>API: detected_source_lang, lid_confidence
    
    API->>NMT: translate(text, source_lang, target_lang)
    NMT-->>API: translated_text, nmt_latency_ms
    
    API->>TTS: synthesize(translated_text, target_lang)
    TTS-->>API: audio_file_path, tts_latency_ms
    
    API->>DB: INSERT INTO translation_records (latencies, texts, file_paths)
    DB-->>API: record_id
    
    API-->>User: 200 OK JSON (recognized_text, translated_text, audio_url, latencies)
    User->>API: GET /api/v1/audio/stream/{audio_id}
    API-->>User: 206 Partial Content / 200 OK Audio Stream (WAV)
```

---

## 4.6 Component & Package Architecture

The system is decomposed into cleanly isolated Python modules and React component hierarchies:

```mermaid
flowchart TD
    subgraph FrontendApp["Frontend Application (React + Vite)"]
        F1["App.tsx & Router"]
        F2["AuthContext.tsx"]
        F3["TranslatorPage.tsx"]
        F4["MicrophoneRecorder.tsx"]
        F5["AudioPlayer.tsx"]
        F6["PerformancePage.tsx"]
        F7["HistoryPage.tsx"]
        F8["api.ts (Axios Client)"]
    end

    subgraph BackendApp["Backend Application (FastAPI)"]
        B1["main.py (ASGI Entrypoint)"]
        B2["api/v1/endpoints/"]
        B3["core/ (config, security, languages)"]
        B4["db/ (session, base, models)"]
        B5["services/ (ASR, NMT, TTS, LID, Pipeline)"]
    end

    subgraph MLPackages["ML Framework & Benchmarks"]
        M1["ml/evaluation/ (asr_evaluator, nmt_evaluator)"]
        M2["ml/experiments/ (benchmark_runner)"]
        M3["ml/datasets/ (test_multilingual_corpus.json)"]
    end

    F8 <-->|REST over HTTP/JSON| B2
    B2 --> B5
    B5 --> B3
    B5 --> B4
    M2 --> B5
    M1 --> M3
```

---

## 4.7 API Contract Specifications

### 1. Voice Translation Endpoint
- **Route:** `POST /api/v1/translate/voice`
- **Content-Type:** `multipart/form-data`
- **Request Parameters:**
  - `file`: Binary audio file (`audio/wav`, `audio/webm`, `audio/mpeg`). Required.
  - `target_language`: ISO 639-1 target language code (e.g., `'en'`, `'hi'`, `'ta'`). Required.
  - `source_language`: ISO 639-1 source language code (optional, defaults to automatic detection).
  - `apply_denoise`: Boolean flag indicating whether spectral noise subtraction should be applied.
- **Success Response (200 OK):**
```json
{
  "id": 42,
  "source_language": "hi",
  "target_language": "en",
  "recognized_text": "नमस्ते, आप कैसे हैं?",
  "detected_language": "hi",
  "translated_text": "Hello, how are you?",
  "output_audio_url": "/api/v1/audio/stream/84",
  "latencies": {
    "dsp_ms": 42.1,
    "asr_ms": 1148.5,
    "lid_ms": 14.2,
    "nmt_ms": 782.9,
    "tts_ms": 479.3,
    "total_ms": 2467.0
  },
  "created_at": "2026-11-13T10:15:30.123456"
}
```

### 2. Text Translation Endpoint
- **Route:** `POST /api/v1/translate/text`
- **Content-Type:** `application/json`
- **Request Body:**
```json
{
  "source_text": "भारत एक महान और सुंदर देश है।",
  "target_language": "gu",
  "source_language": "hi"
}
```
- **Success Response (200 OK):**
```json
{
  "id": 43,
  "source_language": "hi",
  "target_language": "gu",
  "original_text": "भारत एक महान और सुंदर देश है।",
  "translated_text": "ભારત એક મહાન અને સુંદર દેશ છે.",
  "latencies": {
    "lid_ms": 12.0,
    "nmt_ms": 745.2,
    "total_ms": 757.2
  }
}
```

### 3. Audio Streaming Endpoint
- **Route:** `GET /api/v1/audio/stream/{audio_id}`
- **Response:** Binary audio stream (`audio/wav` or `audio/webm`), supporting HTTP range headers (`206 Partial Content`) for instant browser seeking and waveform scrubbing.
