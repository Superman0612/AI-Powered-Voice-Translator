# BhashaAI – System Architecture & Technical Design

## 1. High-Level Architecture Overview

BhashaAI implements a decoupled, service-oriented architecture specifically designed for low-resource CPU inference on Indian languages.

```mermaid
graph TD
    Client["Client / API Consumer (Phase 2 UI / Postman / SDK)"]
    
    subgraph FastAPI_Backend ["FastAPI Application Gateway"]
        AuthMiddleware["JWT Auth & Security Guard"]
        Router["API Route Controllers"]
        
        subgraph Services_Layer ["Modular Services Layer"]
            ASR["ASR Service (Whisper)"]
            LID["Language Identification Service"]
            NMT["NMT Service (NLLB-200 / IndicTrans2)"]
            TTS["TTS Service (MMS-TTS / gTTS)"]
            DSP["Audio DSP Engine (Resample / Normalize)"]
            Orchestrator["End-to-End Pipeline Orchestrator"]
        end
        
        subgraph Data_Layer ["Data & Persistence Layer"]
            ORM["SQLAlchemy 2.0 Async/Sync ORM"]
            PG[(PostgreSQL 18 Database)]
            Storage["Local Secure Audio Vault (/storage/audio)"]
        end
    end
    
    subgraph ML_Framework ["Independent ML Evaluation Framework (ml/)"]
        Benchmarks["Benchmarking Scripts"]
        EvalEngine["Metrics Evaluator (WER, CER, BLEU, chrF)"]
        Plots["Matplotlib Performance Visualizer"]
    end
    
    Client -->|HTTPS / Multipart| AuthMiddleware
    AuthMiddleware --> Router
    Router --> Orchestrator
    Orchestrator --> DSP
    DSP --> ASR
    ASR --> LID
    LID --> NMT
    NMT --> TTS
    TTS --> Storage
    Router --> ORM
    ORM --> PG
    ML_Framework --> Services_Layer
```

---

## 2. Voice Translation Pipeline Dataflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Client
    participant API as FastAPI Router
    participant Pipe as Pipeline Orchestrator
    participant DSP as Audio DSP
    participant ASR as Whisper ASR
    participant LID as Lang Identification
    participant NMT as NLLB NMT
    participant TTS as MMS/gTTS Engine
    participant DB as PostgreSQL DB
    participant FS as Audio File System

    User->>API: POST /api/v1/translate/voice (Audio File + Target Lang)
    API->>DSP: Validate format & Resample to 16kHz Mono
    DSP-->>Pipe: Preprocessed Audio Buffer (16kHz float32)
    Pipe->>ASR: Run Whisper Inference
    ASR-->>Pipe: Transcribed Text + Audio LID confidence
    Pipe->>LID: Verify Source Language (Devanagari/Dravidian disambiguation)
    LID-->>Pipe: Confirmed Source Language Code
    Pipe->>NMT: Translate(Source Text, Source Code, Target Code)
    NMT-->>Pipe: Translated Output Text
    Pipe->>TTS: Synthesize(Translated Text, Target Language)
    TTS->>FS: Save Output Audio (WAV/MP3)
    FS-->>TTS: File Path & Duration
    TTS-->>Pipe: Audio File Metadata
    Pipe->>DB: Persist Translation Record & Latencies
    DB-->>Pipe: Translation ID
    Pipe-->>API: Full Response JSON (Texts, Audios, Latencies)
    API-->>User: 200 OK + Payload
```

---

## 3. Database Schema Design (Entity-Relationship)

```mermaid
erDiagram
    USERS ||--o{ TRANSLATIONS : creates
    USERS ||--o{ AUDIO_FILES : uploads
    USERS ||--o{ EVALUATION_RUNS : conducts
    
    LANGUAGES ||--o{ TRANSLATIONS : "source language"
    LANGUAGES ||--o{ TRANSLATIONS : "target language"
    
    TRANSLATIONS ||--o| AUDIO_FILES : "input audio"
    TRANSLATIONS ||--o| AUDIO_FILES : "output audio"
    
    MODEL_REGISTRY ||--o{ EVALUATION_RUNS : evaluates
    EVALUATION_RUNS ||--o{ EVALUATION_RESULTS : yields

    USERS {
        uuid id PK
        string email UK
        string username UK
        string hashed_password
        string full_name
        boolean is_active
        boolean is_admin
        datetime created_at
        datetime updated_at
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
        uuid id PK
        uuid user_id FK
        string original_filename
        string storage_path
        string mime_type
        int file_size_bytes
        float duration_seconds
        int sample_rate
        int channels
        datetime created_at
    }

    TRANSLATIONS {
        uuid id PK
        uuid user_id FK
        string source_lang_code FK
        string target_lang_code FK
        text source_text
        text translated_text
        string detected_language
        float detection_confidence
        uuid input_audio_id FK
        uuid output_audio_id FK
        float asr_duration_ms
        float nmt_duration_ms
        float tts_duration_ms
        float total_duration_ms
        string status
        datetime created_at
    }

    MODEL_REGISTRY {
        int id PK
        string model_id UK
        string task_type
        string architecture
        string parameter_count
        string license
        boolean is_active
        datetime registered_at
    }

    EVALUATION_RUNS {
        uuid id PK
        uuid user_id FK
        string run_name
        string task_type
        string dataset_name
        int model_id FK
        datetime created_at
    }

    EVALUATION_RESULTS {
        uuid id PK
        uuid run_id FK
        string language_pair
        float metric_wer
        float metric_cer
        float metric_bleu
        float metric_chrf
        float avg_latency_ms
        int sample_count
        datetime created_at
    }
```

---

## 4. Backend Directory Structure

```
sd/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── translate.py
│   │   │   │   │   ├── languages.py
│   │   │   │   │   ├── audio.py
│   │   │   │   │   ├── evaluation.py
│   │   │   │   │   └── health.py
│   │   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── languages_config.py
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── language.py
│   │   │   ├── translation.py
│   │   │   ├── audio.py
│   │   │   └── evaluation.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── translation.py
│   │   │   ├── language.py
│   │   │   ├── audio.py
│   │   │   └── evaluation.py
│   │   ├── services/
│   │   │   ├── asr/
│   │   │   │   ├── service.py
│   │   │   │   └── audio_processor.py
│   │   │   ├── translation/
│   │   │   │   ├── service.py
│   │   │   │   └── normalizer.py
│   │   │   ├── tts/
│   │   │   │   ├── service.py
│   │   │   │   └── mms_engine.py
│   │   │   ├── language_detection/
│   │   │   │   ├── service.py
│   │   │   │   └── heuristics.py
│   │   │   └── pipeline.py
│   │   ├── utils/
│   │   │   ├── audio_utils.py
│   │   │   └── logger.py
│   │   └── main.py
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_database.py
│   │   ├── test_asr.py
│   │   ├── test_nmt.py
│   │   ├── test_tts.py
│   │   ├── test_langdetect.py
│   │   ├── test_endpoints.py
│   │   └── test_pipeline.py
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
├── ml/
│   ├── datasets/
│   │   ├── test_sentences.json
│   │   └── test_audio_manifest.json
│   ├── preprocessing/
│   │   └── audio_cleaner.py
│   ├── evaluation/
│   │   ├── asr_evaluator.py
│   │   └── nmt_evaluator.py
│   ├── experiments/
│   │   └── benchmark_runner.py
│   ├── benchmarks/
│   │   └── results/
│   └── scripts/
│       └── generate_plots.py
├── storage/
│   └── audio/
│       ├── uploads/
│       └── generated/
├── MODEL_SELECTION.md
├── ARCHITECTURE.md
├── DEVELOPMENT_PLAN.md
├── PROJECT_STATUS.md
├── DEVELOPMENT_LOG.md
└── PHASE_1_COMPLETION_REPORT.md
```

