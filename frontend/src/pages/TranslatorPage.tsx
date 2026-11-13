import React, { useState, useEffect } from 'react';
import { 
  Mic, 
  UploadCloud, 
  Type, 
  Sparkles, 
  Trash2, 
  Send
} from 'lucide-react';
import { api } from '../services/api';
import { LanguageSelector } from '../components/translator/LanguageSelector';
import { MicrophoneRecorder } from '../components/translator/MicrophoneRecorder';
import { AudioUploader } from '../components/translator/AudioUploader';
import { ProcessingStatusCard } from '../components/translator/ProcessingStatusCard';
import { TranslationResultCard } from '../components/translator/TranslationResultCard';
import type { Language, TranslationRecord, ProcessingStage } from '../types';

export const TranslatorPage: React.FC = () => {
  const [languages, setLanguages] = useState<Language[]>([]);
  const [sourceLang, setSourceLang] = useState<string>('hi');
  const [targetLang, setTargetLang] = useState<string>('en');
  const [inputMode, setInputMode] = useState<'mic' | 'upload' | 'text'>('mic');

  // Input states
  const [recordedBlob, setRecordedBlob] = useState<Blob | null>(null);
  const [recordedAudioUrl, setRecordedAudioUrl] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadedAudioUrl, setUploadedAudioUrl] = useState<string | null>(null);
  const [textInput, setTextInput] = useState<string>('');
  const [applyDenoise, setApplyDenoise] = useState<boolean>(false);

  // Pipeline execution states
  const [stage, setStage] = useState<ProcessingStage>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [result, setResult] = useState<TranslationRecord | null>(null);
  const [latencies, setLatencies] = useState<{ asr_ms?: number; lid_ms?: number; nmt_ms?: number; tts_ms?: number; total_ms?: number }>({});

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const list = await api.languages.list();
        setLanguages(list);
      } catch (e) {
        console.error("Failed to load languages:", e);
        // Fallback default catalog if backend starting up
        setLanguages([
          { id: 1, code_iso_639_1: 'hi', code_iso_639_3: 'hin', name: 'Hindi', native_name: 'हिन्दी', script_name: 'Devanagari', nllb_code: 'hin_Deva', indictrans_code: 'hin_Deva', whisper_code: 'hi', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 2, code_iso_639_1: 'en', code_iso_639_3: 'eng', name: 'English', native_name: 'English', script_name: 'Latin', nllb_code: 'eng_Latn', indictrans_code: 'eng_Latn', whisper_code: 'en', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 3, code_iso_639_1: 'gu', code_iso_639_3: 'guj', name: 'Gujarati', native_name: 'ગુજરાતી', script_name: 'Gujarati', nllb_code: 'guj_Gujr', indictrans_code: 'guj_Gujr', whisper_code: 'gu', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 4, code_iso_639_1: 'mr', code_iso_639_3: 'mar', name: 'Marathi', native_name: 'मराठी', script_name: 'Devanagari', nllb_code: 'mar_Deva', indictrans_code: 'mar_Deva', whisper_code: 'mr', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 5, code_iso_639_1: 'bn', code_iso_639_3: 'ben', name: 'Bengali', native_name: 'বাংলা', script_name: 'Bengali', nllb_code: 'ben_Beng', indictrans_code: 'ben_Beng', whisper_code: 'bn', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 6, code_iso_639_1: 'ta', code_iso_639_3: 'tam', name: 'Tamil', native_name: 'தமிழ்', script_name: 'Tamil', nllb_code: 'tam_Taml', indictrans_code: 'tam_Taml', whisper_code: 'ta', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 7, code_iso_639_1: 'te', code_iso_639_3: 'tel', name: 'Telugu', native_name: 'తెలుగు', script_name: 'Telugu', nllb_code: 'tel_Telu', indictrans_code: 'tel_Telu', whisper_code: 'te', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 8, code_iso_639_1: 'kn', code_iso_639_3: 'kan', name: 'Kannada', native_name: 'ಕನ್ನಡ', script_name: 'Kannada', nllb_code: 'kan_Knda', indictrans_code: 'kan_Knda', whisper_code: 'kn', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 9, code_iso_639_1: 'ml', code_iso_639_3: 'mal', name: 'Malayalam', native_name: 'മലയാളം', script_name: 'Malayalam', nllb_code: 'mal_Mlym', indictrans_code: 'mal_Mlym', whisper_code: 'ml', supports_asr: true, supports_nmt: true, supports_tts: true },
          { id: 10, code_iso_639_1: 'pa', code_iso_639_3: 'pan', name: 'Punjabi', native_name: 'ਪੰਜਾਬੀ', script_name: 'Gurmukhi', nllb_code: 'pan_Guru', indictrans_code: 'pan_Guru', whisper_code: 'pa', supports_asr: true, supports_nmt: true, supports_tts: true }
        ]);
      }
    };
    fetchLanguages();
  }, []);

  const handleSwapLanguages = () => {
    if (sourceLang !== 'auto') {
      const prevSource = sourceLang;
      setSourceLang(targetLang);
      setTargetLang(prevSource);
    }
  };

  const handleRecordingComplete = (blob: Blob, audioUrl: string) => {
    setRecordedBlob(blob);
    setRecordedAudioUrl(audioUrl);
  };

  const handleFileSelected = (file: File) => {
    setUploadedFile(file);
    setUploadedAudioUrl(URL.createObjectURL(file));
  };

  const clearInputs = () => {
    setRecordedBlob(null);
    setRecordedAudioUrl(null);
    setUploadedFile(null);
    setUploadedAudioUrl(null);
    setTextInput('');
    setStage('idle');
    setErrorMessage(null);
    setResult(null);
  };

  const executeTranslation = async () => {
    setErrorMessage(null);

    // MODE 1: Text Translation Mode
    if (inputMode === 'text') {
      if (!textInput.trim()) {
        setErrorMessage("Please enter text to translate.");
        return;
      }

      setStage('translating');
      try {
        const payload = {
          source_text: textInput,
          target_language: targetLang,
          source_language: sourceLang === 'auto' ? undefined : sourceLang
        };
        const res = await api.translate.text(payload);
        setResult(res);
        setLatencies(res.latencies);
        setStage('completed');
      } catch (err: any) {
        console.error("Text translation failed:", err);
        setErrorMessage(err.response?.data?.detail || err.message || "Translation error occurred.");
        setStage('error');
      }
      return;
    }

    // MODE 2 & 3: Voice Translation Mode (Microphone or File Upload)
    const audioBlob = inputMode === 'mic' ? recordedBlob : uploadedFile;
    if (!audioBlob) {
      setErrorMessage("Please record speech or upload an audio file first.");
      return;
    }

    const formData = new FormData();
    const fileName = inputMode === 'mic' ? 'mic_recording.webm' : (uploadedFile?.name || 'uploaded_voice.wav');
    formData.append('file', audioBlob, fileName);
    formData.append('target_language', targetLang);
    if (sourceLang !== 'auto') {
      formData.append('source_language', sourceLang);
    }
    formData.append('apply_denoise', String(applyDenoise));

    // Progression through pipeline states
    setStage('uploading');
    setTimeout(() => setStage('recognizing'), 400);
    setTimeout(() => setStage('detecting'), 1000);
    setTimeout(() => setStage('translating'), 1400);
    setTimeout(() => setStage('synthesizing'), 1800);

    try {
      const res = await api.translate.voice(formData);
      setResult(res);
      setLatencies(res.latencies);
      setStage('completed');
    } catch (err: any) {
      console.error("Voice translation pipeline error:", err);
      const detail = err.response?.data?.detail || err.message || "Voice translation failed.";
      setErrorMessage(detail);
      setStage('error');
    }
  };

  const hasAudioReady = inputMode === 'mic' ? !!recordedBlob : !!uploadedFile;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-900">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-400" />
            AI Voice Translation Studio
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time end-to-end voice translator across 10 scheduled Indian vernacular languages.
          </p>
        </div>

        {/* Mode Selector Switch */}
        <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 self-start sm:self-auto">
          <button
            type="button"
            onClick={() => setInputMode('mic')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              inputMode === 'mic' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Mic className="w-3.5 h-3.5" />
            Microphone
          </button>
          <button
            type="button"
            onClick={() => setInputMode('upload')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              inputMode === 'upload' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <UploadCloud className="w-3.5 h-3.5" />
            Upload Audio
          </button>
          <button
            type="button"
            onClick={() => setInputMode('text')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              inputMode === 'text' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Type className="w-3.5 h-3.5" />
            Text Mode
          </button>
        </div>
      </div>

      {/* Language Selector Bar */}
      <LanguageSelector
        languages={languages}
        sourceLanguage={sourceLang}
        targetLanguage={targetLang}
        onSourceChange={setSourceLang}
        onTargetChange={setTargetLang}
        onSwap={handleSwapLanguages}
        disabled={stage !== 'idle' && stage !== 'completed' && stage !== 'error'}
      />

      {/* Input Workspace Area */}
      <div className="p-6 rounded-3xl bg-slate-900/50 border border-slate-800/80 shadow-2xl space-y-5">
        {/* Input Mode 1: Microphone Recording */}
        {inputMode === 'mic' && (
          <div className="space-y-4">
            <MicrophoneRecorder
              onRecordingComplete={handleRecordingComplete}
              disabled={stage !== 'idle' && stage !== 'completed' && stage !== 'error'}
            />

            {recordedAudioUrl && (
              <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
                  <span>Recorded Voice Input Ready</span>
                  <button
                    type="button"
                    onClick={() => { setRecordedBlob(null); setRecordedAudioUrl(null); }}
                    className="text-rose-400 hover:text-rose-300 flex items-center gap-1"
                  >
                    <Trash2 className="w-3.5 h-3.5" /> Discard
                  </button>
                </div>
                <audio controls src={recordedAudioUrl} className="w-full h-10 accent-indigo-500" />
              </div>
            )}
          </div>
        )}

        {/* Input Mode 2: Audio File Upload */}
        {inputMode === 'upload' && (
          <AudioUploader
            onFileSelected={handleFileSelected}
            onClear={() => { setUploadedFile(null); setUploadedAudioUrl(null); }}
            selectedFile={uploadedFile}
            previewUrl={uploadedAudioUrl}
            disabled={stage !== 'idle' && stage !== 'completed' && stage !== 'error'}
          />
        )}

        {/* Input Mode 3: Text Translation */}
        {inputMode === 'text' && (
          <div className="space-y-3">
            <div className="relative">
              <textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="Enter or paste text in Hindi, Tamil, Telugu, Gujarati, Marathi, English, etc..."
                rows={4}
                className="w-full p-4 rounded-2xl bg-slate-950 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 text-sm leading-relaxed"
              />
              <div className="absolute bottom-3 right-3 text-[11px] text-slate-500 font-mono">
                {textInput.length} chars
              </div>
            </div>
          </div>
        )}

        {/* Options & Action Footer */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 border-t border-slate-800/80">
          {/* DSP Denoising Switch */}
          {inputMode !== 'text' ? (
            <label className="flex items-center gap-2.5 text-xs text-slate-300 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={applyDenoise}
                onChange={(e) => setApplyDenoise(e.target.checked)}
                className="w-4 h-4 rounded bg-slate-950 border-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900"
              />
              <span>Apply Spectral Noise Reduction (Denoising)</span>
            </label>
          ) : <div />}

          {/* Action Buttons */}
          <div className="flex items-center gap-3 w-full sm:w-auto">
            {(hasAudioReady || textInput) && (
              <button
                type="button"
                onClick={clearInputs}
                className="px-4 py-2.5 rounded-xl border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-850 text-xs font-semibold transition-colors"
              >
                Clear
              </button>
            )}

            <button
              type="button"
              onClick={executeTranslation}
              disabled={
                (inputMode !== 'text' && !hasAudioReady) ||
                (inputMode === 'text' && !textInput.trim()) ||
                (stage !== 'idle' && stage !== 'completed' && stage !== 'error')
              }
              className="w-full sm:w-auto px-6 py-2.5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
              <span>Translate Speech & Text</span>
            </button>
          </div>
        </div>
      </div>

      {/* Processing Status Stepper Card */}
      <ProcessingStatusCard
        stage={stage}
        error={errorMessage}
        latencies={latencies}
      />

      {/* Final Translation Result View */}
      {result && stage === 'completed' && (
        <TranslationResultCard
          result={result}
          onClear={clearInputs}
        />
      )}
    </div>
  );
};
