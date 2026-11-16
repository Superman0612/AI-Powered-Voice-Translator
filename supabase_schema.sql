-- ==============================================================================
-- BhashaAI - Supabase PostgreSQL Schema & Seeding Script
-- Paste this entire SQL into your Supabase SQL Editor and click 'Run'.
-- ==============================================================================

-- 1. Languages Table
CREATE TABLE IF NOT EXISTS languages (
    id SERIAL PRIMARY KEY,
    code_iso_639_1 VARCHAR(10) UNIQUE NOT NULL,
    code_iso_639_3 VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100) NOT NULL,
    script_name VARCHAR(100) NOT NULL,
    nllb_code VARCHAR(50) NOT NULL,
    indictrans_code VARCHAR(50) NOT NULL,
    whisper_code VARCHAR(20) NOT NULL,
    supports_asr BOOLEAN DEFAULT TRUE NOT NULL,
    supports_nmt BOOLEAN DEFAULT TRUE NOT NULL,
    supports_tts BOOLEAN DEFAULT TRUE NOT NULL
);

-- 2. Model Registry Table
CREATE TABLE IF NOT EXISTS model_registry (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(100) UNIQUE NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    architecture VARCHAR(100) NOT NULL,
    parameter_count VARCHAR(50) NOT NULL,
    license VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    registered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 3. Users Table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 4. Audio Files Table
CREATE TABLE IF NOT EXISTS audio_files (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    original_filename VARCHAR(255) NOT NULL,
    storage_path VARCHAR(512) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    duration_seconds FLOAT,
    sample_rate INTEGER DEFAULT 16000 NOT NULL,
    channels INTEGER DEFAULT 1 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 5. Evaluation Runs Table
CREATE TABLE IF NOT EXISTS evaluation_runs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    run_name VARCHAR(255) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    dataset_name VARCHAR(255) NOT NULL,
    model_id INTEGER REFERENCES model_registry(id) ON DELETE RESTRICT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 6. Evaluation Results Table
CREATE TABLE IF NOT EXISTS evaluation_results (
    id VARCHAR(36) PRIMARY KEY,
    run_id VARCHAR(36) REFERENCES evaluation_runs(id) ON DELETE CASCADE NOT NULL,
    language_pair VARCHAR(20) NOT NULL,
    metric_wer FLOAT,
    metric_cer FLOAT,
    metric_bleu FLOAT,
    metric_chrf FLOAT,
    avg_latency_ms FLOAT NOT NULL,
    sample_count INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 7. Translations Table
CREATE TABLE IF NOT EXISTS translations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    source_lang_code VARCHAR(10) NOT NULL,
    target_lang_code VARCHAR(10) NOT NULL,
    source_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    detected_language VARCHAR(10),
    detection_confidence FLOAT,
    input_audio_id VARCHAR(36) REFERENCES audio_files(id) ON DELETE SET NULL,
    output_audio_id VARCHAR(36) REFERENCES audio_files(id) ON DELETE SET NULL,
    asr_duration_ms FLOAT DEFAULT 0.0 NOT NULL,
    nmt_duration_ms FLOAT DEFAULT 0.0 NOT NULL,
    tts_duration_ms FLOAT DEFAULT 0.0 NOT NULL,
    total_duration_ms FLOAT DEFAULT 0.0 NOT NULL,
    status VARCHAR(50) DEFAULT 'completed' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_translations_user_created ON translations(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_translations_source ON translations(source_lang_code);
CREATE INDEX IF NOT EXISTS idx_translations_target ON translations(target_lang_code);
CREATE INDEX IF NOT EXISTS idx_audio_files_user ON audio_files(user_id);

-- ==============================================================================
-- SEED DATA: 10 Supported Indian Languages
-- ==============================================================================
INSERT INTO languages (code_iso_639_1, code_iso_639_3, name, native_name, script_name, nllb_code, indictrans_code, whisper_code, supports_asr, supports_nmt, supports_tts)
VALUES
('hi', 'hin', 'Hindi', 'हिन्दी', 'Devanagari', 'hin_Deva', 'hin_Deva', 'hi', TRUE, TRUE, TRUE),
('en', 'eng', 'English', 'English', 'Latin', 'eng_Latn', 'eng_Latn', 'en', TRUE, TRUE, TRUE),
('gu', 'guj', 'Gujarati', 'ગુજરાતી', 'Gujarati', 'guj_Gujr', 'guj_Gujr', 'gu', TRUE, TRUE, TRUE),
('mr', 'mar', 'Marathi', 'मराठी', 'Devanagari', 'mar_Deva', 'mar_Deva', 'mr', TRUE, TRUE, TRUE),
('bn', 'ben', 'Bengali', 'বাংলা', 'Bengali', 'ben_Beng', 'ben_Beng', 'bn', TRUE, TRUE, TRUE),
('ta', 'tam', 'Tamil', 'தமிழ்', 'Tamil', 'tam_Taml', 'tam_Taml', 'ta', TRUE, TRUE, TRUE),
('te', 'tel', 'Telugu', 'తెలుగు', 'Telugu', 'tel_Telu', 'tel_Telu', 'te', TRUE, TRUE, TRUE),
('kn', 'kan', 'Kannada', 'ಕನ್ನಡ', 'Kannada', 'kan_Knda', 'kan_Knda', 'kn', TRUE, TRUE, TRUE),
('ml', 'mal', 'Malayalam', 'മലയാളം', 'Malayalam', 'mal_Mlym', 'mal_Mlym', 'ml', TRUE, TRUE, TRUE),
('pa', 'pan', 'Punjabi', 'ਪੰਜਾਬੀ', 'Gurmukhi', 'pan_Guru', 'pan_Guru', 'pa', TRUE, TRUE, TRUE)
ON CONFLICT (code_iso_639_1) DO NOTHING;

-- ==============================================================================
-- SEED DATA: Model Registry
-- ==============================================================================
INSERT INTO model_registry (model_id, task_type, architecture, parameter_count, license, is_active)
VALUES
('openai/whisper-small', 'ASR', 'Encoder-Decoder Transformer', '244M', 'MIT', TRUE),
('openai/whisper-base', 'ASR', 'Encoder-Decoder Transformer', '74M', 'MIT', FALSE),
('facebook/nllb-200-distilled-600M', 'NMT', 'Shared Seq2Seq Transformer', '600M', 'CC-BY-NC 4.0', TRUE),
('ai4bharat/indictrans2-en-indic-dist-200M', 'NMT', 'Seq2Seq Transformer', '200M', 'MIT', FALSE),
('facebook/mms-tts', 'TTS', 'VITS (Variational Autoencoder + GAN)', '36M per language', 'CC-BY-NC 4.0', TRUE),
('gtts-neural-service', 'TTS', 'Google Neural WaveNet TTS (Cloud Fallback)', 'Cloud API', 'Cloud Fallback', TRUE),
('langdetect-statistical-ngram', 'LID', 'N-gram Profile & Unicode Range Classifier', 'Heuristic Rule-based', 'Apache 2.0', TRUE)
ON CONFLICT (model_id) DO NOTHING;

-- ==============================================================================
-- SEED DATA: Master Admin Account (shubhamdevatwal2121@gmail.com / Shubham@404)
-- ==============================================================================
INSERT INTO users (id, email, username, hashed_password, full_name, is_active, is_admin)
VALUES
('00000000-0000-0000-0000-000000000001', 'shubhamdevatwal2121@gmail.com', 'shubhamdevatwal', '$2b$12$55fgV84ztdKtZLIhLbUr2eb7m3mnNb6Chtf/cOLXUICWp53pmFz2.', 'Shubham Devatwal', TRUE, TRUE)
ON CONFLICT (email) DO UPDATE SET hashed_password = EXCLUDED.hashed_password, is_admin = TRUE;
