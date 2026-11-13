export interface Language {
  id: number;
  code_iso_639_1: string;
  code_iso_639_3: string;
  name: string;
  native_name: string;
  script_name: string;
  nllb_code: string;
  indictrans_code: string;
  whisper_code: string;
  supports_asr: boolean;
  supports_nmt: boolean;
  supports_tts: boolean;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

export interface LatencyMetrics {
  asr_ms: number;
  nmt_ms: number;
  tts_ms: number;
  total_ms: number;
}

export interface TranslationRecord {
  id: string;
  source_text: string;
  translated_text: string;
  source_language: string;
  target_language: string;
  detected_language?: string;
  detection_confidence?: number;
  input_audio_url?: string;
  output_audio_url?: string;
  latencies: LatencyMetrics;
  status: string;
  created_at: string;
}

export interface LanguageDetectResponse {
  detected_language: string;
  language_name: string;
  script: string;
  confidence: number;
  is_supported: boolean;
  supported_models: string[];
}

export interface ModelRegistryItem {
  id: number;
  model_id: string;
  task_type: string;
  architecture: string;
  parameter_count: string;
  license: string;
  is_active: boolean;
  registered_at: string;
}

export interface BenchmarkResult {
  language_pair: string;
  wer?: number;
  cer?: number;
  bleu?: number;
  chrf?: number;
  avg_latency_ms: number;
  sample_count: number;
  recorded_at: string;
}

export interface EvaluationSummary {
  total_registered_models: number;
  total_evaluation_runs: number;
  total_evaluated_language_pairs: number;
  recent_benchmarks: BenchmarkResult[];
}

export type ProcessingStage =
  | 'idle'
  | 'recording'
  | 'uploading'
  | 'recognizing'
  | 'detecting'
  | 'translating'
  | 'synthesizing'
  | 'completed'
  | 'error';

