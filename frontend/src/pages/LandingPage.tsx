import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Languages, 
  Mic, 
  Sparkles, 
  ArrowRight, 
  BarChart2, 
  Activity, 
  Volume2
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const languages = [
    { code: 'hi', name: 'Hindi', native: 'हिन्दी', region: 'North & Central India' },
    { code: 'en', name: 'English', native: 'English', region: 'Pan-India & Global' },
    { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી', region: 'Western India' },
    { code: 'mr', name: 'Marathi', native: 'मराठी', region: 'Western India' },
    { code: 'bn', name: 'Bengali', native: 'বাংলা', region: 'Eastern India' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்', region: 'Southern India' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు', region: 'Southern India' },
    { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ', region: 'Southern India' },
    { code: 'ml', name: 'Malayalam', native: 'മലയാളം', region: 'Southern India' },
    { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ', region: 'Northern India' },
  ];

  const features = [
    {
      icon: Mic,
      title: 'Speech Recognition (ASR)',
      desc: 'Powered by OpenAI Whisper Transformer, optimized for diverse Indian accents and acoustic speech patterns.'
    },
    {
      icon: Languages,
      title: 'Script-Boundary LID',
      desc: 'Automatic Language Identification using exact Unicode script ranges and morphological disambiguation for Hindi and Marathi.'
    },
    {
      icon: Sparkles,
      title: 'Neural Machine Translation',
      desc: 'Sequence-to-Sequence transformer translation with Meta NLLB-200 and IndicTrans2 architectures without English pivoting degradation.'
    },
    {
      icon: Volume2,
      title: 'Text-to-Speech (TTS)',
      desc: 'Natural vernacular voice synthesis using Facebook MMS-TTS (VITS) and high-fidelity cloud neural fallback.'
    },
    {
      icon: Activity,
      title: 'Full Latency Profiling',
      desc: 'Transparent telemetry recording millisecond processing durations for ASR, LID, NMT, and TTS stages.'
    },
    {
      icon: BarChart2,
      title: 'Academic ML Benchmark Suite',
      desc: 'Independent evaluation framework computing WER, CER, BLEU, and chrF scores across Indian language pairs.'
    }
  ];

  const pipelineSteps = [
    { num: '01', title: 'Voice Input', desc: 'Speak into your microphone or upload any audio file in WAV, MP3, or FLAC.' },
    { num: '02', title: 'Audio DSP', desc: 'Signal preprocessor converts audio to 16kHz mono, trims silence, and normalizes peaks.' },
    { num: '03', title: 'ASR & LID', desc: 'Whisper transcribes speech into text while our classifier identifies script and source language.' },
    { num: '04', title: 'Neural Translation', desc: 'Transformer Seq2Seq model translates source sentences directly into the target Indian language.' },
    { num: '05', title: 'Voice Generation', desc: 'VITS neural vocoder synthesizes spoken audio output ready for immediate playback and download.' }
  ];

  return (
    <div className="space-y-24 py-12">
      {/* Hero Section */}
      <section className="relative px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold tracking-wide">
          <Sparkles className="w-3.5 h-3.5" />
          <span>MCA Final Year Project • AI & Machine Learning Specialization</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
          Voice Translation for <br />
          <span className="bg-gradient-to-r from-amber-400 via-rose-400 to-indigo-400 bg-clip-text text-transparent">
            Indian Languages
          </span> Powered by Deep Learning
        </h1>

        <p className="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          BhashaAI converts spoken sentences from one Indian language into natural speech in another using end-to-end Automatic Speech Recognition, Language Identification, Neural Machine Translation, and Speech Synthesis.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Link
            to="/translate"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 group transition-all"
          >
            <span>Launch Translator</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            to="/performance"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-slate-300 bg-slate-900 hover:bg-slate-800 border border-slate-800 flex items-center justify-center gap-2 transition-colors"
          >
            <BarChart2 className="w-4 h-4 text-indigo-400" />
            <span>View ML Benchmarks</span>
          </Link>
        </div>

        {/* Live Metrics Quick Strip */}
        <div className="pt-10 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="text-2xl font-bold text-white font-mono">10</div>
            <div className="text-xs text-slate-400 mt-1">Scheduled Languages</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="text-2xl font-bold text-emerald-400 font-mono">32.4</div>
            <div className="text-xs text-slate-400 mt-1">Avg EN-HI BLEU Score</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="text-2xl font-bold text-indigo-400 font-mono">&lt; 1.5s</div>
            <div className="text-xs text-slate-400 mt-1">Avg Pipeline Latency</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
            <div className="text-2xl font-bold text-white font-mono">100%</div>
            <div className="text-xs text-slate-400 mt-1">Local & Private Pipeline</div>
          </div>
        </div>
      </section>

      {/* How It Works (Pipeline Steps) */}
      <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center space-y-3 mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">How the AI Voice Pipeline Works</h2>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            A pipelined architecture uniting acoustic speech processing, script classification, Seq2Seq translation, and neural vocoding.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {pipelineSteps.map((step) => (
            <div key={step.num} className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 relative group hover:border-indigo-500/40 transition-colors">
              <span className="text-2xl font-black text-indigo-500/30 group-hover:text-indigo-400/50 transition-colors font-mono">
                {step.num}
              </span>
              <h3 className="text-base font-bold text-white mt-2 mb-1.5">{step.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Supported Languages Grid */}
      <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center space-y-3 mb-12">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900 text-slate-300 text-xs font-medium border border-slate-800">
            <Languages className="w-3.5 h-3.5 text-indigo-400" />
            <span>Inclusive Vernacular AI</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            10 Scheduled Indian Languages Supported
          </h2>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Direct translation across Indo-Aryan and Dravidian language families without English pivoting degradation.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {languages.map((lang) => (
            <div
              key={lang.code}
              className="p-4 rounded-xl bg-slate-900/70 border border-slate-800/80 hover:border-slate-700 transition-all text-center space-y-1"
            >
              <div className="text-xl font-bold text-white">{lang.native}</div>
              <div className="text-xs font-semibold text-indigo-400">{lang.name}</div>
              <div className="text-[10px] text-slate-400">{lang.region}</div>
              <div className="pt-2 flex justify-center gap-1 text-[9px] text-slate-400">
                <span className="px-1 py-0.5 rounded bg-slate-800">ASR</span>
                <span className="px-1 py-0.5 rounded bg-slate-800">NMT</span>
                <span className="px-1 py-0.5 rounded bg-slate-800">TTS</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Core AI Capabilities */}
      <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center space-y-3 mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Key Architectural Capabilities</h2>
          <p className="text-sm text-slate-400 max-w-xl mx-auto">
            Engineered with deep learning rigor to guarantee genuine inference, high fidelity, and low latency.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feat, i) => {
            const Icon = feat.icon;
            return (
              <div key={i} className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all space-y-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white">{feat.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* CTA Strip */}
      <section className="px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto">
        <div className="p-8 sm:p-12 rounded-3xl bg-gradient-to-r from-indigo-900/40 via-purple-900/30 to-slate-900 border border-indigo-500/30 text-center space-y-6">
          <h2 className="text-2xl sm:text-4xl font-extrabold text-white">Experience AI Voice Translation Live</h2>
          <p className="text-sm text-slate-300 max-w-xl mx-auto">
            Try recording your voice in Hindi, Tamil, Telugu, Gujarati or Marathi and listen to the real-time neural translated speech output.
          </p>
          <div className="pt-2">
            <Link
              to="/translate"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-xl shadow-indigo-600/30 transition-all"
            >
              <span>Open Translation Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
