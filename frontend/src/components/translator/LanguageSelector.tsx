import React from 'react';
import { ArrowLeftRight } from 'lucide-react';
import type { Language } from '../../types';

interface LanguageSelectorProps {
  languages: Language[];
  sourceLanguage: string;
  targetLanguage: string;
  onSourceChange: (code: string) => void;
  onTargetChange: (code: string) => void;
  onSwap: () => void;
  disabled?: boolean;
}

const FALLBACK_LANGUAGES: Language[] = [
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
];

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  languages,
  sourceLanguage,
  targetLanguage,
  onSourceChange,
  onTargetChange,
  onSwap,
  disabled = false
}) => {
  const activeLanguages = languages && languages.length > 0 ? languages : FALLBACK_LANGUAGES;
  return (
    <div className="flex flex-col sm:flex-row items-center gap-3 p-3 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-lg">
      {/* Source Language */}
      <div className="flex-1 w-full">
        <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1 px-1">
          Source Language
        </label>
        <div className="relative">
          <select
            value={sourceLanguage}
            onChange={(e) => onSourceChange(e.target.value)}
            disabled={disabled}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm font-medium text-white appearance-none cursor-pointer hover:border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 transition-colors disabled:opacity-50"
          >
            <option value="auto">✨ Auto Detect Language</option>
            {activeLanguages.map((lang) => (
              <option key={`src-${lang.code_iso_639_1}`} value={lang.code_iso_639_1}>
                {lang.name} ({lang.native_name})
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400 text-xs">
            ▼
          </div>
        </div>
      </div>

      {/* Swap Button */}
      <div className="sm:pt-5 shrink-0">
        <button
          type="button"
          onClick={onSwap}
          disabled={disabled || sourceLanguage === 'auto'}
          className={`p-2.5 rounded-xl border transition-all ${
            sourceLanguage === 'auto'
              ? 'opacity-40 cursor-not-allowed bg-slate-950 border-slate-850 text-slate-600'
              : 'bg-slate-950 border-slate-800 text-slate-300 hover:text-white hover:border-indigo-500/50 hover:bg-indigo-950/20 active:scale-95'
          }`}
          title={sourceLanguage === 'auto' ? "Cannot swap with Auto Detect" : "Swap Source & Target Languages"}
        >
          <ArrowLeftRight className="w-4 h-4" />
        </button>
      </div>

      {/* Target Language */}
      <div className="flex-1 w-full">
        <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1 px-1">
          Target Language
        </label>
        <div className="relative">
          <select
            value={targetLanguage}
            onChange={(e) => onTargetChange(e.target.value)}
            disabled={disabled}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-sm font-medium text-white appearance-none cursor-pointer hover:border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 transition-colors disabled:opacity-50"
          >
            {activeLanguages.map((lang) => (
              <option key={`tgt-${lang.code_iso_639_1}`} value={lang.code_iso_639_1}>
                {lang.name} ({lang.native_name})
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400 text-xs">
            ▼
          </div>
        </div>
      </div>
    </div>
  );
};
