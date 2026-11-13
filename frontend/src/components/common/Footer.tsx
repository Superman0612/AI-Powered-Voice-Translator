import React from 'react';
import { Link } from 'react-router-dom';
import { Languages, Shield, Terminal, BookOpen, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-900 bg-slate-950/90 text-slate-400 text-sm mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Info */}
          <div className="md:col-span-1 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                <Languages className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-white tracking-tight">Bhasha<span className="text-indigo-400">AI</span></span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              AI-Powered Voice Translator for Indian Languages using Deep Learning, Transformer ASR, and Neural Machine Translation.
            </p>
            <div className="text-[11px] text-slate-500 pt-1">
              MCA Final Year AI & ML Capstone Project
            </div>
          </div>

          {/* Supported Languages */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">Supported Languages (10)</h4>
            <div className="flex flex-wrap gap-1.5 text-xs">
              {['Hindi', 'English', 'Gujarati', 'Marathi', 'Bengali', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Punjabi'].map((lang) => (
                <span key={lang} className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-slate-300 text-[11px]">
                  {lang}
                </span>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">Application</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/translate" className="hover:text-white transition-colors">Voice Translator</Link>
              </li>
              <li>
                <Link to="/history" className="hover:text-white transition-colors">Translation History</Link>
              </li>
              <li>
                <Link to="/performance" className="hover:text-white transition-colors">AI/ML Benchmark Metrics</Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-white transition-colors">Academic Documentation</Link>
              </li>
              <li>
                <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors flex items-center gap-1">
                  <Terminal className="w-3 h-3 text-indigo-400" /> Swagger OpenAPI Docs
                </a>
              </li>
            </ul>
          </div>

          {/* Academic & AI Stack */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">AI & Engineering Stack</h4>
            <div className="space-y-1.5 text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                <span>OpenAI Whisper (ASR)</span>
              </div>
              <div className="flex items-center gap-2">
                <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
                <span>Meta NLLB-200 / IndicTrans2 (NMT)</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="w-3.5 h-3.5 text-indigo-400" />
                <span>Facebook MMS-TTS (VITS)</span>
              </div>
              <div className="flex items-center gap-2 text-[11px] text-slate-500 pt-2 border-t border-slate-900">
                <span>FastAPI • PostgreSQL 18 • PyTorch 2.13</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-900 mt-8 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© 2026 BhashaAI Research Project. Developed for MCA Final Year Specialization in AI & Machine Learning.</p>
          <div className="flex items-center gap-4 text-slate-400">
            <span>Non-Commercial Academic Research</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

