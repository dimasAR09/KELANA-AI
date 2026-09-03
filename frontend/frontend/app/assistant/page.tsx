'use client';

import { useState } from 'react';
import Link from 'next/link';
import { askAssistant } from '../../services/tripService';

interface AssistantResponse {
  answer: string;
  sources?: string[];
}

export default function AssistantPage() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');
    setSources([]);

    try {
      const data = (await askAssistant(question)) as AssistantResponse;
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : 'Terjadi kesalahan saat memproses pertanyaan.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-4 sm:p-8">
      <main className="max-w-3xl mx-auto space-y-8 mt-10">

        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-linear-to-r from-indigo-400 to-cyan-400">
              KelanaAI Assistant
            </h1>
            <p className="text-slate-400 text-sm mt-1">Travel Assistant (KelanaAI)</p>
          </div>
          <Link
            href="/trips"
            className="text-sm font-bold text-slate-400 hover:text-white transition"
          >
            ← Back to Dashboard
          </Link>
          <Link
            href="/chat"
            className="px-3 py-1.5 rounded-xl bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 text-xs font-semibold border border-indigo-500/30 transition"
          >
            💬 Chat AI
          </Link>
        </div>

        {/* Input Form */}
        <form
          onSubmit={handleAsk}
          className="flex items-center gap-3 bg-slate-900 border border-slate-700 p-2 rounded-2xl shadow-xl"
        >
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Contoh: Apa aturan Travel terbaru?"
            className="flex-1 bg-transparent px-4 py-2 outline-none text-sm text-white placeholder:opacity-50"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="px-6 py-2.5 enabled:bg-indigo-600 enabled:hover:bg-indigo-500 enabled:text-white disabled:bg-slate-800 disabled:text-slate-500 text-sm font-bold rounded-xl transition cursor-pointer"
          >
            {loading ? 'Thinking...' : 'Ask AI'}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl text-sm">
            {error}
          </div>
        )}

        {/* Answer & Citations Box */}
        {answer && (
          <div className="bg-emerald-900/20 border border-emerald-500/30 rounded-2xl p-6 space-y-6">
            <div>
              <span className="text-[10px] font-extrabold uppercase text-emerald-400 tracking-wider">
                AI ANSWER
              </span>
              <p className="text-slate-200 mt-2 leading-relaxed text-sm whitespace-pre-wrap">
                {answer}
              </p>
            </div>

            {/* Source / Citations */}
            {sources.length > 0 && (
              <div className="border-t border-emerald-500/20 pt-4">
                <span className="text-[10px] font-extrabold uppercase text-slate-400 tracking-wider">
                  SOURCE / CITATIONS
                </span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {sources.map((src, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-1.5 bg-slate-900 border border-slate-700 px-3 py-1.5 rounded-lg text-xs font-mono text-slate-300"
                    >
                      📄 {src}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

      </main>
    </div>
  );
}
