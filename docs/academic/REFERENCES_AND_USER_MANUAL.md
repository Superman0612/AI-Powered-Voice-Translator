# REFERENCES AND USER MANUAL

---

# PART I: ACADEMIC REFERENCES

1. **Bahdanau, D., Cho, K., & Bengio, Y. (2014).** Neural Machine Translation by Jointly Learning to Align and Translate. *arXiv preprint arXiv:1409.0473*.
2. **Boll, S. (1979).** Suppression of Acoustic Noise in Speech Using Spectral Subtraction. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, 27(2), 113–120.
3. **Cavnar, W. B., & Trenkle, J. M. (1994).** N-Gram-Based Text Categorization. *Proceedings of the 3rd Annual Symposium on Document Analysis and Information Retrieval (SDAIR)*, 161–175.
4. **Chan, W., Jaitly, N., Le, Q., & Vinyals, O. (2016).** Listen, Attend and Spell: A Neural Network for Large Vocabulary Conversational Speech Recognition. *IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 4960–4964.
5. **Gala, J., et al. (AI4Bharat). (2023).** IndicTrans2: Towards High-Quality and Accessible Machine Translation Models for all 22 Scheduled Indian Languages. *Transactions of the Association for Computational Linguistics (TACL)*, 11, 1432–1452.
6. **Graves, A., Fernández, S., Gomez, F., & Schmidhuber, J. (2006).** Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks. *Proceedings of the 23rd International Conference on Machine Learning (ICML)*, 369–376.
7. **Gulati, A., et al. (2020).** Conformer: Convolution-augmented Transformer for Speech Recognition. *Interspeech 2020*, 5036–5040.
8. **Javed, T., et al. (AI4Bharat). (2021).** Towards Building Open-Domain Speech Systems for Indic Languages. *arXiv preprint arXiv:2111.03945*.
9. **Joulin, A., Grave, E., Bojanowski, P., & Mikolov, T. (2016).** Bag of Tricks for Efficient Text Classification. *Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics (EACL)*, 427–431.
10. **Kim, J., Kong, J., & Son, J. (2021).** Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech (VITS). *Proceedings of the 38th International Conference on Machine Learning (ICML)*, PMLR 139, 5530–5540.
11. **NLLB Team, Costa-jussà, M. R., et al. (Meta AI). (2022).** No Language Left Behind: Scaling Human-Centered Machine Translation. *arXiv preprint arXiv:2207.04672*.
12. **Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002).** BLEU: A Method for Automatic Evaluation of Machine Translation. *Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL)*, 311–318.
13. **Popović, M. (2017).** chrF++: Words Helping Character n-grams. *Proceedings of the Second Conference on Machine Translation (WMT17)*, 616–619.
14. **Post, M. (2018).** A Call for Clarity in Reporting BLEU Scores. *Proceedings of the Third Conference on Machine Translation (WMT18)*, 186–191.
15. **Pratap, V., et al. (Meta AI). (2023).** Scaling Speech Technology to 1,000+ Languages (Massively Multilingual Speech - MMS). *arXiv preprint arXiv:2305.13516*.
16. **Radford, A., et al. (OpenAI). (2022).** Robust Speech Recognition via Large-Scale Weak Supervision (Whisper). *arXiv preprint arXiv:2212.04356*.
17. **Ren, Y., et al. (2020).** FastSpeech 2: Fast and High-Quality End-to-End Text-to-Speech. *arXiv preprint arXiv:2006.04558*.
18. **Shen, J., et al. (2018).** Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions (Tacotron 2). *IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 4779–4783.
19. **Vaswani, A., et al. (2017).** Attention Is All You Need. *Advances in Neural Information Processing Systems (NeurIPS 30)*, 5998–6008.

---

# PART II: SYSTEM USER MANUAL & OPERATIONS GUIDE

## 1. System Requirements & Prerequisites

### Server & Backend Environment
- **Operating System:** Windows 10/11 x64, Ubuntu 20.04+, or macOS
- **Python:** Version 3.10 to 3.14 (Verified on Python 3.14.6)
- **Node.js & npm:** Node.js 18.0+ and npm 9.0+ (Verified on Node v24.15.0, npm 11.12.1)
- **Relational Database:** PostgreSQL 14+ (Verified on PostgreSQL 18.0 on port 5432)
- **RAM:** Minimum 8.0 GB RAM
- **Disk Space:** 5.0 GB available storage for model weights and audio cache

### Client Browser Environment
- Modern HTML5-compliant browser (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari)
- Microphone hardware peripheral with granted browser permissions

---

## 2. Installation and Setup Instructions

### Step 1: Clone and Navigate to Project
```bash
git clone <repository_url>
cd sd
```

### Step 2: Configure Environment Variables
Create or verify `.env` in the project root:
```ini
PROJECT_NAME="BhashaAI"
VERSION="2.0.0"
API_V1_STR="/api/v1"
SECRET_KEY="your-super-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# PostgreSQL Connection String
DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/bhashaai"
SYNC_DATABASE_URL="postgresql://postgres:password@localhost:5432/bhashaai"

# Audio Storage Directories
UPLOAD_DIR="storage/audio/uploads"
GENERATED_DIR="storage/audio/generated"
MAX_UPLOAD_SIZE_MB=25

# ML Model Preferences
WHISPER_MODEL_SIZE="small"
DEFAULT_NMT_MODEL="nllb"
DEFAULT_TTS_ENGINE="mms"
DEVICE="cpu"
```

### Step 3: Initialize Database Migrations
Ensure PostgreSQL service is running, then run Alembic migrations:
```bash
alembic upgrade head
```

### Step 4: Start the FastAPI Backend Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The API is available at: `http://localhost:8000`  
Interactive Swagger API documentation: `http://localhost:8000/docs`

### Step 5: Start the React Frontend Application
Open a second terminal window:
```bash
cd frontend
npm install
npm run dev
```
The web dashboard is available at: `http://localhost:5173`

---

## 3. Step-by-Step User Walkthrough

### 3.1 Registration and Authentication
1. Navigate to `http://localhost:5173/register`.
2. Fill in your Full Name, Username, Email, and Password, or click **"Quick Fill Demo Account"** for one-click onboarding.
3. Click **"Create Account"**. Upon success, you are logged in and redirected to the **Voice Translation Studio**.

### 3.2 Using the Voice Translation Studio
1. **Select Language Pair:**
   - Choose your **Source Language** (e.g., Hindi, Gujarati, Tamil, or "Auto Detect").
   - Choose your **Target Language** (e.g., English, Telugu, Marathi).
   - Use the **⇄ Swap** button to reverse language directions instantly.
2. **Input Mode - Microphone Recording:**
   - Select the **Microphone** tab.
   - Click the red microphone button to start recording. Notice the live timer and pulsing animation.
   - Speak clearly into the microphone.
   - Click the stop button to finish recording. An audio preview appears instantly.
3. **Input Mode - Audio Upload:**
   - Select the **Upload Audio** tab.
   - Drag and drop or browse for an audio file (`.wav`, `.mp3`, `.webm`).
4. **Noise Reduction Toggle:**
   - If recording in a noisy environment, toggle **"Spectral Noise Reduction"** to enable background noise filtering.
5. **Execution:**
   - Click the purple **"Translate Speech"** button.
   - Observe the live 5-stage progress indicator:
     $$\text{Uploading} \longrightarrow \text{Recognizing} \longrightarrow \text{Detecting} \longrightarrow \text{Translating} \longrightarrow \text{Synthesizing}$$
6. **Reviewing Results:**
   - View the recognized transcription in the source script alongside detected language confidence.
   - View the neural translation in the target language.
   - Click the interactive audio player to listen to synthesized speech.
   - Click **Download Audio** to save the synthesized `.wav` speech locally.
   - Click **Copy** to copy the translated text to your clipboard.
   - Inspect the latency badges showing exact execution times ($T_{\text{DSP}}, T_{\text{ASR}}, T_{\text{NMT}}, T_{\text{TTS}}$).

### 3.3 Exploring Translation History
1. Click **History** in the top navigation bar (`/history`).
2. Search past translations by keyword or filter by source/target language.
3. Play back saved audio recordings directly from the history table.
4. Delete historical records using the trash icon.

### 3.4 Reviewing AI/ML Performance Benchmarks
1. Click **Performance** in the top navigation bar (`/performance`).
2. Explore academic benchmark visualizations:
   - Multilingual BLEU and chrF++ scores across all 10 scheduled languages.
   - Word Error Rate (WER) vs. Acoustic Noise comparison (Clean vs. 20 dB vs. 10 dB).
   - Microsecond latency decomposition across all 5 pipeline stages.
   - Live Deep Learning Model Specifications table (parameters, RAM footprint, licenses).

---

## 4. Troubleshooting Guide

| Problem Observed | Probable Cause | Corrective Action |
|:---|:---|:---|
| **Microphone not recording** | Browser microphone permissions blocked. | Click the lock/tune icon in the browser address bar, set **Microphone** to "Allow", and reload the page. |
| **Backend connection refused (ERR_CONNECTION_REFUSED)** | FastAPI server is not running or running on an alternate port. | Verify terminal shows `Application startup complete` on `http://127.0.0.1:8000`. |
| **PostgreSQL connection error (`Connection refused`)** | PostgreSQL service stopped or password mismatch. | Open Windows Services, ensure `postgresql-x64-18` is running, and verify credentials in `.env`. |
| **Audio format error on upload** | Unsupported file format or file exceeds 25 MB limit. | Ensure file is WAV, MP3, WebM, FLAC, or OGG, and file size is within 25 MB. |
| **CORS blocked by browser** | Frontend origin not present in backend CORS origins. | Check `backend/app/core/config.py`; ensure `http://localhost:5173` is included in `BACKEND_CORS_ORIGINS`. |
