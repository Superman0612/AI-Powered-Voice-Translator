import React, { useState } from 'react';
import { Copy, Check, Sparkles, Languages } from 'lucide-react';
import { AudioPlayer } from '../common/AudioPlayer';
import type { TranslationRecord } from '../../types';

interface TranslationResultCardProps {
  result: TranslationRecord;
  onClear: () => void;
}

export const TranslationResultCard: React.FC<TranslationResultCardProps> = ({
  result,
  onClear
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(result.translated_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getAudioUrl = (partialUrl?: string) => {
    if (!partialUrl) return '';
    if (partialUrl.startsWith('http')) return partialUrl;
    // Map relative url to backend base
    const base = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').trim().replace(/\/+$/, '');
    const cleanBase = base.endsWith('/api/v1') ? base.replace('/api/v1', '') : base;
    const cleanPartial = partialUrl.startsWith('/') ? partialUrl : `/${partialUrl}`;
    return `${cleanBase}${cleanPartial}`;
  };

  return (
    <div className="rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl overflow-hidden divide-y divide-slate-800/80">
      {/* Top Header with Latency Telemetry */}
      <div className="px-5 py-3.5 bg-slate-950/60 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1 font-semibold text-indigo-400">
            <Sparkles className="w-3.5 h-3.5" />
            Verified Pipeline Output
          </span>
          <span className="text-slate-600">•</span>
          <span className="text-slate-400 font-mono text-[11px]">
            ID: {result.id.slice(0, 8)}...
          </span>
        </div>

        {/* Latency Breakdown Badges */}
        <div className="flex items-center gap-2 text-[11px] font-mono">
          {result.latencies?.asr_ms > 0 && (
            <span className="px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/50" title="ASR Processing Time">
              ASR: {result.latencies.asr_ms.toFixed(0)}ms
            </span>
          )}
          {result.latencies?.nmt_ms > 0 && (
            <span className="px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/50" title="NMT Translation Time">
              NMT: {result.latencies.nmt_ms.toFixed(0)}ms
            </span>
          )}
          {result.latencies?.tts_ms > 0 && (
            <span className="px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/50" title="TTS Generation Time">
              TTS: {result.latencies.tts_ms.toFixed(0)}ms
            </span>
          )}
          <span className="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-bold" title="Total End-to-End Latency">
            ⚡ {result.latencies?.total_ms?.toFixed(0) || '0'}ms
          </span>
        </div>
      </div>

      {/* Main Content Panels: Dual-Pane Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-800">
        {/* Left: Source Text & ASR Output */}
        <div className="p-5 flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                Source Speech / Text ({result.source_language.toUpperCase()})
              </span>
              {result.detected_language && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <Languages className="w-3 h-3" />
                  Detected: {result.detected_language.toUpperCase()} ({Math.round((result.detection_confidence || 1) * 100)}%)
                </span>
              )}
            </div>
            <p className="text-base text-slate-100 font-medium leading-relaxed whitespace-pre-wrap">
              {result.source_text}
            </p>
          </div>

          {result.input_audio_url && (
            <div className="pt-2">
              <AudioPlayer 
                src={getAudioUrl(result.input_audio_url)} 
                title="Recorded User Input Audio" 
                className="bg-slate-950 border-slate-850" 
              />
            </div>
          )}
        </div>

        {/* Right: Translated Text & TTS Audio */}
        <div className="p-5 flex flex-col justify-between space-y-4 bg-slate-950/30">
          <div>
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-400 flex items-center gap-1">
                <Sparkles className="w-3 h-3" /> Translated ({result.target_language.toUpperCase()})
              </span>
              <button
                type="button"
                onClick={handleCopy}
                className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 transition-colors"
                title="Copy translated text"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>
            <p className="text-base text-white font-medium leading-relaxed whitespace-pre-wrap">
              {result.translated_text}
            </p>
          </div>

          {/* Generated Audio Player */}
          {result.output_audio_url && (
            <div className="pt-2">
              <AudioPlayer 
                src={getAudioUrl(result.output_audio_url)} 
                title={`Neural Speech Synthesis (${result.target_language.toUpperCase()})`} 
                autoPlay={false}
                className="bg-indigo-950/20 border-indigo-900/30" 
              />
            </div>
          )}
        </div>
      </div>

      {/* Bottom Actions Bar */}
      <div className="px-5 py-3 bg-slate-950 flex items-center justify-between">
        <span className="text-xs text-slate-400">
          Completed at {new Date(result.created_at).toLocaleTimeString()}
        </span>
        <button
          type="button"
          onClick={onClear}
          className="text-xs text-slate-400 hover:text-slate-200 transition-colors"
        >
          Clear Workspace
        </button>
      </div>
    </div>
  );
};
