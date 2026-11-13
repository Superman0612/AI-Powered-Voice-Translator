import React from 'react';
import { 
  Upload, 
  Cpu, 
  Languages, 
  Sparkles, 
  Volume2, 
  CheckCircle2, 
  AlertTriangle,
  Loader2
} from 'lucide-react';
import type { ProcessingStage } from '../../types';

interface ProcessingStatusCardProps {
  stage: ProcessingStage;
  error?: string | null;
  latencies?: {
    asr_ms?: number;
    lid_ms?: number;
    nmt_ms?: number;
    tts_ms?: number;
    total_ms?: number;
  };
}

export const ProcessingStatusCard: React.FC<ProcessingStatusCardProps> = ({
  stage,
  error,
  latencies
}) => {
  if (stage === 'idle') return null;

  const stages = [
    { key: 'uploading', label: 'Audio Ingestion & DSP', desc: 'Resampling to 16kHz & mono normalization', icon: Upload },
    { key: 'recognizing', label: 'Speech Recognition (ASR)', desc: 'OpenAI Whisper transformer inference', icon: Cpu, latency: latencies?.asr_ms },
    { key: 'detecting', label: 'Language Identification', desc: 'Script boundary & morphological analysis', icon: Languages, latency: latencies?.lid_ms },
    { key: 'translating', label: 'Neural Machine Translation', desc: 'Meta NLLB-200 Seq2Seq model', icon: Sparkles, latency: latencies?.nmt_ms },
    { key: 'synthesizing', label: 'Text-to-Speech Synthesis', desc: 'VITS neural vocoder synthesis', icon: Volume2, latency: latencies?.tts_ms },
  ];

  const getStageStatus = (stepKey: string) => {
    if (stage === 'error') {
      return 'error';
    }
    if (stage === 'completed') {
      return 'completed';
    }
    const order = ['uploading', 'recognizing', 'detecting', 'translating', 'synthesizing'];
    const currentIndex = order.indexOf(stage);
    const stepIndex = order.indexOf(stepKey);

    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'active';
    return 'pending';
  };

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {stage === 'error' ? (
            <AlertTriangle className="w-5 h-5 text-rose-400" />
          ) : stage === 'completed' ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          ) : (
            <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
          )}
          <span className="text-sm font-semibold text-white">
            {stage === 'error' ? 'Pipeline Failure' : stage === 'completed' ? 'Translation Complete' : 'AI Pipeline Processing...'}
          </span>
        </div>
        {latencies?.total_ms && (
          <span className="text-xs font-mono font-semibold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20">
            Total: {latencies.total_ms.toFixed(0)} ms
          </span>
        )}
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs">
          <p className="font-semibold mb-0.5">Backend Error Notice:</p>
          <p className="font-mono">{error}</p>
        </div>
      )}

      {/* Step Sequence */}
      <div className="space-y-2">
        {stages.map((step) => {
          const status = getStageStatus(step.key);
          const Icon = step.icon;
          return (
            <div
              key={step.key}
              className={`flex items-center justify-between p-2.5 rounded-xl border transition-all text-xs ${
                status === 'completed'
                  ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-300'
                  : status === 'active'
                  ? 'bg-indigo-500/10 border-indigo-500/30 text-white shadow-inner'
                  : status === 'error'
                  ? 'bg-slate-950/60 border-slate-850 text-slate-500'
                  : 'bg-slate-950/40 border-slate-850 text-slate-500'
              }`}
            >
              <div className="flex items-center gap-2.5 truncate">
                <div className={`p-1.5 rounded-lg ${
                  status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                  status === 'active' ? 'bg-indigo-500/20 text-indigo-400 animate-pulse' :
                  'bg-slate-800 text-slate-600'
                }`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="truncate">
                  <p className="font-medium truncate">{step.label}</p>
                  <p className="text-[10px] text-slate-400 opacity-80">{step.desc}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                {step.latency !== undefined && (
                  <span className="font-mono text-[11px] text-slate-400">
                    {step.latency.toFixed(0)}ms
                  </span>
                )}
                {status === 'completed' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                {status === 'active' && <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

