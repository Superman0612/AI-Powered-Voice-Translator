# BhashaAI – Engineering Development Log

### [Entry 1: November 13, 2026 - Environment Profiling & Research]
- Conducted deep environment inspection:
  - Host OS: Windows 10 Pro x64
  - CPU: Intel 6-Core processor (Coffee Lake)
  - Memory: 8,192 MB Physical RAM (~1.1 GB free at start)
  - Storage: 150 GB total, ~51.8 GB available
  - Python: 3.14.6
  - PyTorch: 2.13.0+cpu
  - Database: PostgreSQL 18 Server running on port 5432
- Evaluated models for ASR, NMT, TTS, and LID:
  - ASR: Selected OpenAI Whisper (`whisper-small` / `base`) via HuggingFace `transformers`. Rejected NeMo IndicConformer due to Python 3.14 C++ build blockers.
  - NMT: Selected Meta NLLB-200 distilled 600M (`facebook/nllb-200-distilled-600M`) for unified many-to-many translation across all 10 target Indian languages. Architectural compatibility with IndicTrans2 also retained.
  - TTS: Selected Facebook MMS-TTS (VITS) for local offline neural synthesis, supplemented with gTTS fallback.
  - LID: Selected Unicode block boundaries + `langdetect` + Devanagari morphological disambiguation.
- Created `MODEL_SELECTION.md`, `DEVELOPMENT_PLAN.md`, `ARCHITECTURE.md`, `PROJECT_STATUS.md`.
- Successfully initialized PostgreSQL database `bhashaai`.
- Installed necessary audio and ML benchmarking libraries: `soundfile`, `gTTS`, `langdetect`, `jiwer`, `sacrebleu`, `matplotlib`, `bcrypt`, `click>=8.4.2`.
- Tested DSP signal pipeline (mono conversion, 16kHz resampling, peak normalization) successfully.

### [Entry 2: November 13, 2026 - Database & Backend Architecture]
- Designed and implemented 7 SQLAlchemy 2.0 ORM models:
  - `User`, `Language`, `AudioFile`, `Translation`, `ModelRegistry`, `EvaluationRun`, `EvaluationResult`.
- Configured Alembic database migrations:
  - Generated revision `388c8d1d9533_initial_schema_setup_for_bhashaai`.
  - Executed database stamp to `head`.
- Created database seeding script `backend/app/database/init_db.py`:
  - Seeded 10 scheduled Indian languages (`hi`, `en`, `gu`, `mr`, `bn`, `ta`, `te`, `kn`, `ml`, `pa`).
  - Seeded AI model registry entries.
  - Seeded admin user (`admin@bhashaai.org`) and test student user (`mca_student`).
- Built authentication subsystem with bcrypt password hashing and JWT access tokens.
- Implemented Pydantic request/response schemas with full type safety.

### [Entry 3: November 13, 2026 - AI/ML Modular Services & Pipeline]
- Built `LanguageDetectionService`:
  - Unicode character range segmentation.
  - Distinctive Devanagari morpheme and lexicon matching (Marathi `आहे`, `नाही`, `करणे` vs Hindi `है`, `नहीं`, `करना`).
  - Code-mixed ratio estimation.
- Built `AudioProcessor` & `ASRService`:
  - 16kHz resampling, mono conversion, peak normalization, silence trimming, spectral noise reduction.
  - Whisper transformer integration with lazy loading and CPU memory release.
- Built `NMTService`:
  - Unicode text normalization, code resolution from ISO to NLLB FLORES tokens, forced BOS token generation.
- Built `TTSService`:
  - Dual-engine architecture: Facebook MMS-TTS local neural synthesis + Google WaveNet (gTTS) fallback.
  - Audio persistence into `storage/audio/generated/` and metadata telemetry.
- Built `VoiceTranslationPipeline`:
  - Full end-to-end execution flow: Audio In -> DSP -> ASR -> LID -> NMT -> TTS -> Audio Out.

### [Entry 4: November 13, 2026 - REST API Gateway, ML Evaluation & Testing]
- Developed FastAPI controllers:
  - `/auth`, `/languages`, `/translate/text`, `/translate/voice`, `/audio`, `/evaluation`, `/health`.
- Developed `ml/` evaluation framework:
  - Parallel corpus covering 10 languages across 5 conversational domains.
  - Evaluators for WER & CER (`jiwer`), BLEU & chrF (`sacrebleu`), and latency timers.
  - Automated benchmark runner with CSV export (`ml/benchmarks/results/benchmark_metrics.csv`).
  - Matplotlib graph generator rendering publication-quality PNG charts.
- Wrote and executed automated test suite using `pytest`:
  - 40 tests covering authentication, database operations, ASR, NMT, TTS, LID, pipeline, and API endpoints.
  - **Result: 40/40 tests passed (100% pass rate in 1.45 seconds).**
- Verified live end-to-end voice translation in `verify_voice_translation_live.py`:
  - Input: Live Hindi speech audio (`नमस्ते, भाषाएआई में आपका स्वागत है।`).
  - Output: English speech audio file generated and saved with full latency profiling.
- Authored final `PHASE_1_COMPLETION_REPORT.md`.


### [Entry 5: November 13, 2026 - Phase 2 Frontend Architecture & UI Development]
- Scaffolding & Dependencies:
  - Initialized React 18 + TypeScript single-page application using Vite in `frontend/`.
  - Installed and configured Tailwind CSS v4, Lucide React icons, Recharts, Axios, and React Router DOM.
- Core Application Infrastructure:
  - Configured centralized Axios API service client with JWT token injection interceptor in `src/services/api.ts`.
  - Created authentication context (`AuthContext.tsx`) managing reactive login state, user profiles, and persistent tokens.
  - Implemented protected route guard (`ProtectedRoute.tsx`).
  - Implemented global navigation header (`Navbar.tsx`) with live backend health pulse and user profile menu.
  - Implemented responsive footer (`Footer.tsx`) detailing academic specialization and technological credits.
- Interactive Audio & Voice Studio Components:
  - Built `MicrophoneRecorder.tsx` leveraging HTML5 `MediaRecorder` API with live timer, waveform pulse, and audio preview.
  - Built `AudioUploader.tsx` supporting drag-and-drop audio file ingestion with client-side format and 25 MB size limits.
  - Built `LanguageSelector.tsx` rendering all 10 scheduled languages, native scripts, auto-detection mode, and bidirectional swap button.
  - Built `ProcessingStatusCard.tsx` providing real-time visual progress across the 5 pipeline stages (`uploading` -> `recognizing` -> `detecting` -> `translating` -> `synthesizing`).
  - Built `TranslationResultCard.tsx` displaying side-by-side source and translated text, script labels, copy button, and latency telemetry badges.
  - Built `AudioPlayer.tsx` providing custom audio playback controls, seeking scrubber, and instant audio download.
- Full Application Pages:
  - `LandingPage.tsx`: Hero section, architecture workflow, 10-language matrix, technology stack, and CTA.
  - `TranslatorPage.tsx`: Dual-mode translation studio (Microphone voice, Audio upload, Direct text) with spectral denoise toggle.
  - `HistoryPage.tsx`: Searchable and filterable table of past translations with in-line audio playback and deletion.
  - `PerformancePage.tsx`: Academic benchmarking dashboard with live Recharts visualizations (BLEU, chrF++, ASR noise WER, latency breakdown).
  - `AboutPage.tsx`: Academic abstract, problem statement, architecture overview, and future research directions.
  - `LoginPage.tsx` & `RegisterPage.tsx`: Full authentication forms with quick-fill demo buttons for seamless evaluator onboarding.
- Build Verification:
  - Addressed TypeScript compilation strictness (`noUnusedLocals: true`).
  - Executed `npm run build` (`tsc -b && vite build`) - successfully bundled production assets in `frontend/dist/` with 0 errors.

### [Entry 6: November 13, 2026 - Academic Thesis Documentation, Viva Voce & Final Deliverables]
- Authored Complete MCA Academic Thesis Chapters in `docs/academic/`:
  - `CHAPTER_1_INTRODUCTION.md`: Background, problem statement, objectives, scope, and motivation.
  - `CHAPTER_2_LITERATURE_SURVEY.md`: Deep learning ASR, NMT, TTS, LID advances, and research gaps.
  - `CHAPTER_3_SYSTEM_ANALYSIS.md`: Existing vs. proposed systems, feasibility studies (technical, operational, economic, legal), requirements.
  - `CHAPTER_4_SYSTEM_DESIGN.md`: Architecture, Use Case, DFD Levels 0 & 1, ER diagrams, Sequence diagrams, Component diagrams (all formatted with Mermaid), database tables, and API contracts.
  - `CHAPTER_5_IMPLEMENTATION.md`: Module deep-dive (DSP, ASR, LID, NMT, TTS, Pipeline, DB, Frontend) and solutions to technical challenges.
  - `CHAPTER_6_AIML_METHODOLOGY.md`: Detailed mathematical formulations (Log-Mel, Attention, VITS VAE/GAN losses, WER, CER, BLEU-4, chrF++), benchmark dataset description.
  - `CHAPTER_7_TESTING_AND_RESULTS.md`: 40/40 test suite breakdown, clean vs. noisy ASR results, multilingual BLEU/chrF++ tables, and latency analysis.
  - `CHAPTER_8_CONCLUSION_AND_FUTURE_SCOPE.md`: Project summary, objectives evaluation, limitations, and future directions.
  - `REFERENCES_AND_USER_MANUAL.md`: 19 formal academic citations in IEEE/APA format, plus end-to-end user manual and troubleshooting guide.
- Authored Comprehensive Viva Voce Examination Guide:
  - `VIVA_QUESTIONS.md`: 55 in-depth technical questions with model answers spanning AI, ML, DSP, Transformers, Whisper, NLLB, VITS, WER, BLEU, FastAPI, React, and PostgreSQL.
- Authored Presentation Deck Outline:
  - `PROJECT_PRESENTATION_OUTLINE.md`: 18-slide presentation deck structure with slide contents, presenter speaking notes, and visual asset suggestions.
- Authored Production Deployment Guide:
  - `DEPLOYMENT_GUIDE.md`: Production architecture, Vercel frontend deployment, Gunicorn/Uvicorn backend, Docker containerization, systemd service, PostgreSQL setup, NGINX SSL reverse proxy, and CORS hardening.
- Repository Hygiene & Final Artifacts:
  - Created `.gitignore` covering Python, Node, Vite dist, audio uploads, test cache, and environment secrets.
  - Re-verified automated test suite: 40/40 pytest tests passed in 1.54 seconds.
  - Authored comprehensive `FINAL_PROJECT_REPORT.md` synthesizing all project outcomes.
