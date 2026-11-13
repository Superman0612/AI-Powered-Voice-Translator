import React, { useState, useEffect } from 'react';
import { 
  History, 
  Search, 
  Trash2, 
  Loader2 
} from 'lucide-react';
import { api } from '../services/api';
import { AudioPlayer } from '../components/common/AudioPlayer';
import type { TranslationRecord } from '../types';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<TranslationRecord[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedLanguage, setSelectedLanguage] = useState<string>('all');
  const [deleteId, setDeleteId] = useState<string | null>(null);

  const fetchHistory = async () => {
    setIsLoading(true);
    try {
      const records = await api.translate.getHistory(0, 50);
      setHistory(records);
    } catch (err) {
      console.error("Failed to load translation history:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this translation record and its audio files?")) return;
    setDeleteId(id);
    try {
      await api.translate.delete(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error("Failed to delete translation:", err);
      alert("Failed to delete record. Please check backend connection.");
    } finally {
      setDeleteId(null);
    }
  };

  const getAudioUrl = (partialUrl?: string) => {
    if (!partialUrl) return '';
    if (partialUrl.startsWith('http')) return partialUrl;
    const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    const cleanBase = base.endsWith('/api/v1') ? base.replace('/api/v1', '') : base;
    return `${cleanBase}${partialUrl}`;
  };

  const filteredHistory = history.filter((item) => {
    const matchesSearch = 
      item.source_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.translated_text.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesLanguage = 
      selectedLanguage === 'all' || 
      item.source_language === selectedLanguage || 
      item.target_language === selectedLanguage;
    return matchesSearch && matchesLanguage;
  });

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-900">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <History className="w-6 h-6 text-indigo-400" />
            Translation History
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Browse, search, and replay past voice and text translations saved in your database.
          </p>
        </div>
        <button
          onClick={fetchHistory}
          disabled={isLoading}
          className="px-3.5 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-white transition-colors self-start sm:self-auto"
        >
          Refresh History
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
        {/* Search Input */}
        <div className="sm:col-span-2 relative">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search transcripts, keywords, or translations..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs font-medium text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
          />
        </div>

        {/* Language Filter */}
        <div className="relative">
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs font-medium text-white appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
          >
            <option value="all">All Languages</option>
            <option value="hi">Hindi (hi)</option>
            <option value="en">English (en)</option>
            <option value="gu">Gujarati (gu)</option>
            <option value="mr">Marathi (mr)</option>
            <option value="bn">Bengali (bn)</option>
            <option value="ta">Tamil (ta)</option>
            <option value="te">Telugu (te)</option>
            <option value="kn">Kannada (kn)</option>
            <option value="ml">Malayalam (ml)</option>
            <option value="pa">Punjabi (pa)</option>
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400 text-xs">
            ▼
          </div>
        </div>
      </div>

      {/* History Items List */}
      {isLoading ? (
        <div className="min-h-[40vh] flex flex-col items-center justify-center gap-3">
          <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
          <p className="text-xs text-slate-400">Loading translation records...</p>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="p-12 text-center rounded-3xl bg-slate-900/40 border border-slate-800/80 space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-slate-800/80 text-slate-500 flex items-center justify-center mx-auto">
            <History className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-300">No translation records found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            {searchQuery || selectedLanguage !== 'all'
              ? 'No translations matched your filter criteria.'
              : 'Perform voice or text translations on the studio page to populate your history.'}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredHistory.map((item) => (
            <div
              key={item.id}
              className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-slate-750 transition-all space-y-4 shadow-lg"
            >
              <div className="flex flex-wrap items-center justify-between gap-3 text-xs border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded font-bold uppercase text-[10px] bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                    {item.source_language} ➔ {item.target_language}
                  </span>
                  {item.detected_language && (
                    <span className="text-slate-400 text-[11px]">
                      Detected: <b className="text-slate-200">{item.detected_language}</b>
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-slate-500 text-[11px] font-mono">
                    {new Date(item.created_at).toLocaleString()}
                  </span>
                  <span className="text-indigo-400 font-mono text-[11px]">
                    ⚡ {item.latencies?.total_ms?.toFixed(0) || '0'}ms
                  </span>
                  <button
                    onClick={() => handleDelete(item.id)}
                    disabled={deleteId === item.id}
                    className="p-1 rounded text-slate-500 hover:text-rose-400 transition-colors"
                    title="Delete record"
                  >
                    {deleteId === item.id ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Trash2 className="w-3.5 h-3.5" />
                    )}
                  </button>
                </div>
              </div>

              {/* Text Translation Content */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Original</span>
                  <p className="text-sm text-slate-200 leading-relaxed font-medium">{item.source_text}</p>
                </div>
                <div className="space-y-1">
                  <span className="text-[10px] font-semibold text-indigo-400 uppercase tracking-wider">Translated</span>
                  <p className="text-sm text-white leading-relaxed font-medium">{item.translated_text}</p>
                </div>
              </div>

              {/* Playback strip if audio available */}
              {item.output_audio_url && (
                <div className="pt-2">
                  <AudioPlayer 
                    src={getAudioUrl(item.output_audio_url)} 
                    title={`Translated Speech Audio (${item.target_language.toUpperCase()})`} 
                    className="bg-slate-950 border-slate-850" 
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
