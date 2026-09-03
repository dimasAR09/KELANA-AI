'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  createConversation,
  listConversations,
  getConversation,
  sendMessage,
  renameConversation,
  deleteConversation,
} from '../../services/tripService';
import type { Conversation, Message } from '../../types';

// ─── Icons ────────────────────────────────────────────────────────────────────

const PlusIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
  </svg>
);

const SendIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
  </svg>
);

const EditIcon = () => (
  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536M9 13l6.5-6.5a2.121 2.121 0 013 3L12 16H9v-3z" />
  </svg>
);

const TrashIcon = () => (
  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2" />
  </svg>
);

const ChatBubbleIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>
);

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatTime(iso: string) {
  try {
    return new Date(iso).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  } catch {
    return '';
  }
}

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });
  } catch {
    return '';
  }
}

// ─── Typing Indicator ─────────────────────────────────────────────────────────

function TypingIndicator() {
  return (
    <div className="flex items-end gap-2 mb-4">
      <div className="w-7 h-7 rounded-full bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white shrink-0">
        K
      </div>
      <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-bl-sm px-4 py-3">
        <div className="flex gap-1 items-center h-4">
          <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}

// ─── Message Bubble ───────────────────────────────────────────────────────────

function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === 'user';
  return (
    <div className={`flex items-end gap-2 mb-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div
        className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
          isUser
            ? 'bg-linear-to-br from-emerald-500 to-teal-600 text-white'
            : 'bg-linear-to-br from-indigo-500 to-purple-600 text-white'
        }`}
      >
        {isUser ? 'U' : 'K'}
      </div>

      {/* Bubble */}
      <div className={`max-w-[78%] flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? 'bg-indigo-600 text-white rounded-br-sm whitespace-pre-wrap'
              : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-bl-sm'
          }`}
        >
          {isUser ? (
            msg.content
          ) : (
            /* AI bubble — render markdown */
            <div className="prose prose-sm prose-invert max-w-none
              prose-headings:font-bold prose-headings:text-white
              prose-h1:text-base prose-h1:mt-3 prose-h1:mb-1
              prose-h2:text-sm prose-h2:mt-3 prose-h2:mb-1
              prose-h3:text-sm prose-h3:mt-2 prose-h3:mb-1 prose-h3:text-indigo-300
              prose-p:my-1.5 prose-p:text-slate-200
              prose-strong:text-white prose-strong:font-semibold
              prose-em:text-slate-300
              prose-ul:my-1.5 prose-ul:pl-4 prose-ul:space-y-1
              prose-ol:my-1.5 prose-ol:pl-4 prose-ol:space-y-1
              prose-li:text-slate-200 prose-li:marker:text-indigo-400
              prose-code:bg-slate-700 prose-code:text-emerald-300 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-xs
              prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-700 prose-pre:rounded-xl prose-pre:p-3 prose-pre:my-2
              prose-blockquote:border-l-indigo-500 prose-blockquote:text-slate-400 prose-blockquote:pl-3 prose-blockquote:my-2
              prose-hr:border-slate-700
              prose-a:text-indigo-300 prose-a:underline
            ">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {msg.content}
              </ReactMarkdown>
            </div>
          )}
        </div>
        {/* Timestamp */}
        <span className="text-[10px] text-slate-500 px-1">{formatTime(msg.created_at)}</span>
      </div>
    </div>
  );
}

// ─── Rename Modal ─────────────────────────────────────────────────────────────

function RenameModal({
  current,
  onSave,
  onClose,
}: {
  current: string;
  onSave: (title: string) => void;
  onClose: () => void;
}) {
  const [value, setValue] = useState(current);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 w-80 space-y-4 shadow-2xl">
        <h3 className="font-bold text-white text-sm">Ganti Nama Percakapan</h3>
        <input
          autoFocus
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && value.trim() && onSave(value.trim())}
          className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-600 rounded-xl text-white outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Nama percakapan..."
        />
        <div className="flex gap-2 justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 transition"
          >
            Batal
          </button>
          <button
            onClick={() => value.trim() && onSave(value.trim())}
            className="px-4 py-2 text-xs rounded-xl bg-indigo-600 text-white hover:bg-indigo-500 transition font-semibold"
          >
            Simpan
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ChatPage() {
  // Conversations list (sidebar)
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);

  // Input
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');

  // Sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Rename modal
  const [renamingConv, setRenamingConv] = useState<Conversation | null>(null);

  // Auto-scroll ref
  const bottomRef = useRef<HTMLDivElement>(null);

  // ── Scroll to bottom on new messages ──
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // ── Load conversation list on mount ──
  const loadConversations = useCallback(async () => {
    try {
      const data = await listConversations() as Conversation[];
      setConversations(data);
    } catch {
      // user mungkin belum login — biarkan halaman menampilkan empty state
    }
  }, []);

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  // ── Load messages when active conversation changes ──
  useEffect(() => {
    if (activeConvId === null) {
      setMessages([]);
      return;
    }
    (async () => {
      try {
        const data = await getConversation(activeConvId) as Conversation;
        setMessages(data.messages ?? []);
      } catch {
        setMessages([]);
      }
    })();
  }, [activeConvId]);

  // ── Create new conversation ──
  const handleNewConversation = async () => {
    try {
      const data = await createConversation();
      await loadConversations();
      setActiveConvId(data.conversation_id);
      setMessages([]);
      setInput('');
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Gagal membuat percakapan baru');
    }
  };

  // ── Send message ──
  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    if (!activeConvId) {
      setError('Pilih atau buat percakapan terlebih dahulu.');
      return;
    }

    const userMsg: Message = {
      id: Date.now(),
      conversation_id: activeConvId,
      role: 'user',
      content: input.trim(),
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);
    setError('');

    try {
      const aiMsg = await sendMessage(activeConvId, userMsg.content) as Message;
      setMessages((prev) => [...prev, aiMsg]);
      // Refresh sidebar (title might have been set auto on first message)
      await loadConversations();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Gagal mengirim pesan');
    } finally {
      setIsTyping(false);
    }
  };

  // ── Rename ──
  const handleRename = async (title: string) => {
    if (!renamingConv) return;
    try {
      await renameConversation(renamingConv.id, title);
      await loadConversations();
      setRenamingConv(null);
    } catch {
      setError('Gagal mengganti nama percakapan');
    }
  };

  // ── Delete ──
  const handleDelete = async (convId: number) => {
    if (!confirm('Hapus percakapan ini beserta semua pesannya?')) return;
    try {
      await deleteConversation(convId);
      if (activeConvId === convId) {
        setActiveConvId(null);
        setMessages([]);
      }
      await loadConversations();
    } catch {
      setError('Gagal menghapus percakapan');
    }
  };

  const activeConv = conversations.find((c) => c.id === activeConvId);

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* ── LEFT SIDEBAR ── */}
      <aside
        className={`flex flex-col bg-slate-900 border-r border-slate-800 transition-all duration-300 shrink-0 ${
          sidebarOpen ? 'w-64' : 'w-0 overflow-hidden'
        }`}
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between px-4 py-4 border-b border-slate-800">
          <span className="font-bold text-sm text-white flex items-center gap-2">
            <ChatBubbleIcon />
            Percakapan
          </span>
          <button
            onClick={handleNewConversation}
            title="Percakapan baru"
            className="p-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition"
          >
            <PlusIcon />
          </button>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto py-2 space-y-0.5 px-2">
          {conversations.length === 0 ? (
            <p className="text-xs text-slate-500 text-center py-8 px-4">
              Belum ada percakapan.
              <br />
              Klik <strong>+</strong> untuk mulai.
            </p>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => setActiveConvId(conv.id)}
                className={`group flex items-center gap-2 px-3 py-2.5 rounded-xl cursor-pointer transition ${
                  activeConvId === conv.id
                    ? 'bg-indigo-600/20 border border-indigo-500/30'
                    : 'hover:bg-slate-800 border border-transparent'
                }`}
              >
                {/* Icon */}
                <div className="w-7 h-7 rounded-lg bg-slate-700 flex items-center justify-center shrink-0">
                  <ChatBubbleIcon />
                </div>

                {/* Title + date */}
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-semibold text-slate-200 truncate">
                    {conv.title ?? 'Percakapan baru'}
                  </p>
                  <p className="text-[10px] text-slate-500">{formatDate(conv.created_at)}</p>
                </div>

                {/* Actions — show on hover */}
                <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition shrink-0">
                  <button
                    onClick={(e) => { e.stopPropagation(); setRenamingConv(conv); }}
                    title="Ganti nama"
                    className="p-1 rounded-md hover:bg-slate-700 text-slate-400 hover:text-white transition"
                  >
                    <EditIcon />
                  </button>
                  <button
                    onClick={(e) => { e.stopPropagation(); handleDelete(conv.id); }}
                    title="Hapus"
                    className="p-1 rounded-md hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition"
                  >
                    <TrashIcon />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Back to Dashboard */}
        <div className="px-4 py-3 border-t border-slate-800">
          <Link
            href="/trips"
            className="flex items-center gap-2 text-xs text-slate-400 hover:text-white transition"
          >
            ← Dashboard
          </Link>
        </div>
      </aside>

      {/* ── MAIN CHAT PANEL ── */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Chat Header */}
        <header className="flex items-center gap-3 px-4 py-3 border-b border-slate-800 bg-slate-900/80 backdrop-blur shrink-0">
          {/* Toggle sidebar */}
          <button
            onClick={() => setSidebarOpen((v) => !v)}
            className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition"
            title="Toggle sidebar"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Title */}
          <div className="flex-1 min-w-0">
            <h1 className="text-sm font-bold text-white truncate">
              {activeConv?.title ?? (activeConvId ? 'Percakapan' : 'KelanaAI Chat')}
            </h1>
            {activeConv && (
              <p className="text-[10px] text-slate-400">
                {activeConv.messages?.length ?? 0} pesan
              </p>
            )}
          </div>

          {/* New chat button */}
          <button
            onClick={handleNewConversation}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition"
          >
            <PlusIcon />
            Baru
          </button>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-4 py-6">
          {/* Empty state — no conversation selected */}
          {activeConvId === null && (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-center">
              <div className="w-16 h-16 rounded-2xl bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-3xl shadow-lg shadow-indigo-500/20">
                ✈️
              </div>
              <div>
                <h2 className="text-lg font-bold text-white">KelanaAI Chat</h2>
                <p className="text-sm text-slate-400 mt-1 max-w-xs">
                  Asisten perjalanan cerdas yang mengingat percakapanmu.
                  Buat percakapan baru untuk mulai.
                </p>
              </div>
              <button
                onClick={handleNewConversation}
                className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-xl transition shadow-md shadow-indigo-600/20"
              >
                <PlusIcon />
                Mulai Percakapan Baru
              </button>
            </div>
          )}

          {/* Messages */}
          {activeConvId !== null && messages.length === 0 && !isTyping && (
            <div className="flex flex-col items-center justify-center h-full text-center gap-3">
              <p className="text-sm text-slate-400">
                Percakapan dimulai. Kirim pesan pertamamu!
              </p>
              {/* Quick prompts */}
              <div className="flex flex-wrap gap-2 justify-center mt-2">
                {[
                  'Rencanakan perjalanan keluarga ke Jepang 5 hari',
                  'Rekomendasi wisata kuliner di Bali',
                  'Tips backpacker ke Australia dengan budget hemat',
                ].map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => setInput(prompt)}
                    className="px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 rounded-xl transition"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <MessageBubble key={msg.id} msg={msg} />
          ))}

          {/* Part 8 Homework — Typing indicator */}
          {isTyping && <TypingIndicator />}

          {/* Auto-scroll anchor */}
          <div ref={bottomRef} />
        </div>

        {/* Error banner */}
        {error && (
          <div className="mx-4 mb-2 px-4 py-2 bg-red-500/10 border border-red-500/30 text-red-400 text-xs rounded-xl">
            {error}
          </div>
        )}

        {/* Input Bar */}
        <div className="px-4 py-4 border-t border-slate-800 bg-slate-900/80 backdrop-blur shrink-0">
          <form onSubmit={handleSend} className="flex items-center gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                activeConvId
                  ? 'Ketik pesan...'
                  : 'Buat percakapan baru terlebih dahulu...'
              }
              disabled={!activeConvId || isTyping}
              className="flex-1 px-4 py-3 text-sm bg-slate-800 border border-slate-700 rounded-xl text-white placeholder:text-slate-500 outline-none focus:ring-2 focus:ring-indigo-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              type="submit"
              disabled={!input.trim() || !activeConvId || isTyping}
              className="p-3 bg-indigo-600 enabled:hover:bg-indigo-500 text-white rounded-xl transition disabled:opacity-40 disabled:cursor-not-allowed"
              title="Kirim"
            >
              <SendIcon />
            </button>
          </form>
        </div>
      </div>

      {/* Rename Modal */}
      {renamingConv && (
        <RenameModal
          current={renamingConv.title ?? ''}
          onSave={handleRename}
          onClose={() => setRenamingConv(null)}
        />
      )}
    </div>
  );
}
