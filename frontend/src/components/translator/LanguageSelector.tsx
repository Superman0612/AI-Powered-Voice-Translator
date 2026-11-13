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

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  languages,
  sourceLanguage,
  targetLanguage,
  onSourceChange,
  onTargetChange,
  onSwap,
  disabled = false
}) => {
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
            {languages.map((lang) => (
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
            {languages.map((lang) => (
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
