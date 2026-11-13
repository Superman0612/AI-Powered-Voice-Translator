import React from 'react';
import { 
  BookOpen, 
  Target, 
  Layers, 
  Cpu, 
  Compass, 
  ShieldCheck, 
  GraduationCap,
  ChevronRight
} from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      {/* Title & Academic Banner */}
      <div className="space-y-4 pb-6 border-b border-slate-900">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 text-xs font-semibold border border-indigo-500/20">
          <GraduationCap className="w-4 h-4" />
          <span>Master of Computer Applications (MCA) Final Year Project</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          About BhashaAI
        </h1>
        <p className="text-base text-slate-400 max-w-3xl leading-relaxed">
          Full Title: <b>AI-Powered Voice Translator for Indian Languages Using Deep Learning and Neural Machine Translation</b>.
          Specialization in Artificial Intelligence and Machine Learning.
        </p>
      </div>

      {/* Abstract */}
      <section className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-3">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-indigo-400" />
          Project Abstract
        </h2>
        <p className="text-sm text-slate-300 leading-relaxed">
          India’s linguistic diversity poses a formidable communication challenge across governance, healthcare, education, and commerce. While existing translation tools predominantly cater to text-based interaction, a substantial percentage of regional speakers rely on oral communication. This project proposes and implements <b>BhashaAI</b>, an end-to-end multilingual voice translation system designed specifically for 10 scheduled Indian languages (Hindi, English, Gujarati, Marathi, Bengali, Tamil, Telugu, Kannada, Malayalam, and Punjabi).
        </p>
        <p className="text-sm text-slate-300 leading-relaxed">
          The system unites an audio signal processing pipeline (16kHz resampling, mono reduction, silence trimming, and spectral noise reduction), Automatic Speech Recognition using OpenAI Whisper, automated Language Identification combining Unicode script ranges and morphological lexicons, direct sequence-to-sequence Neural Machine Translation via Meta NLLB-200 and AI4Bharat IndicTrans2 architectures, and Text-to-Speech synthesis using Facebook MMS-TTS (VITS) and neural fallback engines. The entire system is engineered for CPU-only execution within an 8 GB RAM memory budget.
        </p>
      </section>

      {/* Problem Statement & Objectives Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-3">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-rose-400" />
            Problem Statement
          </h2>
          <ul className="space-y-2 text-xs text-slate-400 leading-relaxed list-disc list-inside">
            <li>Linguistic exclusion of non-Anglophone and non-literate speakers due to text-only translation interfaces.</li>
            <li>Semantic degradation and honorific loss caused by English pivoting in Indian-to-Indian language translation.</li>
            <li>Elevated Word Error Rates in generic speech models on colloquial regional Indian accents and dialects.</li>
            <li>Prohibitive GPU memory requirements of large multi-billion parameter foundational language models.</li>
          </ul>
        </div>

        <div className="p-6 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-3">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Core Objectives
          </h2>
          <ul className="space-y-2 text-xs text-slate-400 leading-relaxed list-disc list-inside">
            <li>Implement speech-to-text with automated audio noise reduction and silence trimming.</li>
            <li>Accurately disambiguate Devanagari languages (Hindi vs Marathi) using grammatical markers.</li>
            <li>Execute direct transformer translation without English intermediary pivoting.</li>
            <li>Generate natural regional speech waveforms with instant playback and download.</li>
            <li>Provide an independent academic benchmarking suite computing WER, CER, BLEU, and chrF.</li>
          </ul>
        </div>
      </div>

      {/* Proposed Methodology Flowchart */}
      <section className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-400" />
          System Architecture & Pipeline Flow
        </h2>
        <div className="p-4 rounded-2xl bg-slate-950 border border-slate-850 font-mono text-xs text-slate-300 space-y-2 overflow-x-auto">
          <p className="text-indigo-400 font-bold">// Sequential Voice Translation Pipeline Execution Flow</p>
          <p>1. [Voice Input]    ➔ Raw Speech captured via Web MediaRecorder or WAV/MP3 upload.</p>
          <p>2. [Audio DSP]      ➔ Signal converted to 16kHz mono; RMS silence trimmed; Spectral noise gated.</p>
          <p>3. [ASR Engine]     ➔ Whisper Sequence-to-Sequence Transformer computes log-mel spectrogram transcript.</p>
          <p>4. [LID Classifier] ➔ Unicode block boundary analysis + Devanagari morphological lexicon disambiguation.</p>
          <p>5. [NMT Engine]     ➔ NLLB-200 Distilled 600M Seq2Seq model generates target language text tokens.</p>
          <p>6. [TTS Synthesizer]➔ VITS neural vocoder transforms target text into continuous audio waveform.</p>
          <p>7. [Persistence]    ➔ Audio persisted to storage vault; metadata & latencies recorded in PostgreSQL 18.</p>
        </div>
      </section>

      {/* Deep Learning Models Used */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Cpu className="w-5 h-5 text-indigo-400" />
          AI/ML Model Suite
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <span className="font-bold text-white text-sm">OpenAI Whisper</span>
            <p className="text-slate-400">Encoder-decoder Transformer trained on 680,000 hours of multilingual audio. High acoustic robustness across Indian accents.</p>
            <div className="pt-2 text-[11px] font-mono text-indigo-400">Task: ASR (244M Params)</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <span className="font-bold text-white text-sm">Meta NLLB-200</span>
            <p className="text-slate-400">No Language Left Behind 600M distilled model supporting 200+ languages with direct many-to-many translation embeddings.</p>
            <div className="pt-2 text-[11px] font-mono text-indigo-400">Task: NMT (600M Params)</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
            <span className="font-bold text-white text-sm">Facebook MMS-TTS</span>
            <p className="text-slate-400">Variational Inference with adversarial learning (VITS) neural text-to-speech vocoder trained across 1,400+ languages.</p>
            <div className="pt-2 text-[11px] font-mono text-indigo-400">Task: TTS (36M Params/lang)</div>
          </div>
        </div>
      </section>

      {/* Future Scope */}
      <section className="p-6 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-3">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Compass className="w-5 h-5 text-indigo-400" />
          Future Enhancements & Research Scope
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-400">
          <div className="flex items-start gap-2">
            <ChevronRight className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <span>Bi-directional WebSocket streaming for simultaneous full-duplex live interpretation.</span>
          </div>
          <div className="flex items-start gap-2">
            <ChevronRight className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <span>Zero-shot Voice Cloning to preserve original speaker identity and timber across translations.</span>
          </div>
          <div className="flex items-start gap-2">
            <ChevronRight className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <span>On-device quantized deployment using ONNX Runtime mobile engines for offline edge computing.</span>
          </div>
          <div className="flex items-start gap-2">
            <ChevronRight className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <span>Expansion to remaining 12 constitutional scheduled languages (Odia, Assamese, Sanskrit, etc.).</span>
          </div>
        </div>
      </section>
    </div>
  );
};
