'use client';
import React, { useState, useMemo, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { getMe } from '@/services/tripService';
import { User } from '@/types';

// ─── Icon Components ──────────────────────────────────────────────────────────

const SparklesIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);
const MapPinIcon = () => (
  <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);
const WalletIcon = () => (
  <svg className="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>
);
const CalendarIcon = () => (
  <svg className="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);
const CompassIcon = () => (
  <svg className="w-5 h-5 text-sky-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 4a1 1 0 012 0v1a1 1 0 01-2 0V4zm0 14a1 1 0 012 0v1a1 1 0 01-2 0v-1zM4 11a1 1 0 010-2h1a1 1 0 010 2H4zm14 0a1 1 0 010-2h1a1 1 0 010 2h-1zM8.05 8.05a1 1 0 011.414 0l.707.707a1 1 0 01-1.414 1.414l-.707-.707a1 1 0 010-1.414zm7.778 7.778a1 1 0 011.414 0l.707.707a1 1 0 01-1.414 1.414l-.707-.707a1 1 0 010-1.414zM8.05 15.95a1 1 0 010 1.414l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 0zm7.778-7.778a1 1 0 010 1.414l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 0z" />
  </svg>
);
const CheckCircleIcon = () => (
  <svg className="w-5 h-5 text-emerald-500 inline mr-2 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

// ─── Constants ────────────────────────────────────────────────────────────────

const QUICK_DESTINATIONS = ['Japan 🏯', 'Bali 🏝️', 'Australia 🐨'];

const DESTINATION_SPOTS: Record<string, string[]> = {
  japan: ["Tokyo Tower", "Shibuya Crossing", "Mount Fuji", "Kyoto Arashiyama", "Osaka Dotonbori", "Nara Park", "Akihabara"],
  jepang: ["Tokyo Tower", "Shibuya Crossing", "Mount Fuji", "Kyoto Arashiyama", "Osaka Dotonbori", "Nara Park", "Akihabara"],
  bali: ["Ubud Monkey Forest", "Kuta Beach", "Pandawa Beach", "Tanah Lot", "Nusa Penida", "Seminyak", "Ulun Danu Beratan"],
  australia: ["Sydney Opera House", "Melbourne Laneways", "Great Barrier Reef", "Bondi Beach", "Blue Mountains", "Gold Coast"],
};

const TRAVEL_STYLES = [
  { id: 'family',      name: 'Keluarga',             icon: '👨‍👩‍👧‍👦', desc: 'Nyaman & santai' },
  { id: 'backpacker',  name: 'Hemat / Backpacker',   icon: '🎒', desc: 'Efisien & terjangkau' },
  { id: 'luxury',      name: 'Mewah',                icon: '✨', desc: 'Eksklusif & premium' },
  { id: 'solo',        name: 'Solo Adventure',       icon: '🧗', desc: 'Bebas & eksploratif' },
  { id: 'romantic',    name: 'Pasangan',             icon: '👩‍❤️‍👨', desc: 'Romantis & intim' },
  { id: 'culinary',    name: 'Kuliner',              icon: '🍜', desc: 'Eksplor makanan lokal' },
];

// ─── Types ────────────────────────────────────────────────────────────────────

interface DayPlan {
  day: number;
  title: string;
  activities: string[];
}

interface TripResult {
  id?: number;
  destination: string;
  days: number;
  budget: string;
  dailyBudget: string;
  style: string;
  highlights: string[];
  itinerary: DayPlan[];
  rawMarkdown?: string;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const formatUSD = (val: string) => {
  const num = parseInt(val.toString().replace(/\D/g, ''), 10);
  if (isNaN(num)) return '';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
};

const parseAiText = (text: string): { highlights: string[]; itinerary: DayPlan[]; rawMarkdown: string } => {
  if (!text) return { highlights: [], itinerary: [], rawMarkdown: '' };

  const trimmed = text.trim();
  if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
    try {
      const parsed = JSON.parse(trimmed) as { itinerary?: DayPlan[]; highlights?: string[] };
      if (parsed && (parsed.itinerary || parsed.highlights)) {
        return {
          highlights: parsed.highlights || [],
          itinerary: parsed.itinerary || [],
          rawMarkdown: '',
        };
      }
    } catch {
      // not valid JSON — fall through to line-by-line parsing
    }
  }

  const lines = text.split('\n').map((l) => l.trim()).filter(Boolean);
  const highlights: string[] = [];
  const itinerary: DayPlan[] = [];
  let currentDay: DayPlan | null = null;
  let inOverview = false;
  let inTips = false;

  for (const line of lines) {
    if (line.includes('Trip Overview')) { inOverview = true; continue; }
    if (line.includes('Daily Itinerary') || line.includes('Day 1')) { inOverview = false; }
    if (line.includes('Essential Tips') || line.includes('Top 5 Insider Tips')) {
      inTips = true;
      inOverview = false;
      if (currentDay) { itinerary.push(currentDay); currentDay = null; }
      continue;
    }
    if (inOverview && (line.includes('Destination:') || line.includes('Duration:') || line.includes('Budget:') || line.includes('Travel Style:'))) {
      continue;
    }

    const dayMatch = line.match(/^(?:#+\s*|\*\*|)(?:🌅\s*)?(Day|Hari)\s*(\d+)\s*[:\-|]?\s*(.*?)(?:\*\*|)$/i);
    if (dayMatch) {
      if (currentDay) itinerary.push(currentDay);
      const dayNum = parseInt(dayMatch[2], 10);
      const titleText = dayMatch[3] ? dayMatch[3].replace(/^\*+|\*+$/g, '').trim() : `Eksplorasi Hari ${dayNum}`;
      currentDay = {
        day: dayNum,
        title: `Hari ke-${dayNum}: ${titleText || 'Aktivitas Wisata'}`,
        activities: [],
      };
      inOverview = false;
      inTips = false;
      continue;
    }

    if (line.startsWith('-') || line.startsWith('*') || line.match(/^\d+\./)) {
      const cleanLine = line.replace(/^[-*\d.]+\s*/, '').replace(/\*\*/g, '').trim();
      if (currentDay) {
        currentDay.activities.push(cleanLine);
      } else if (inTips && highlights.length < 4) {
        highlights.push(cleanLine);
      }
    } else if (!line.startsWith('#') && !currentDay && !inOverview && highlights.length < 3) {
      const cleanLine = line.replace(/^[#*\s]+/, '').trim();
      if (cleanLine && !cleanLine.includes('Destination') && !cleanLine.includes('Budget')) {
        highlights.push(cleanLine);
      }
    }
  }

  if (currentDay) itinerary.push(currentDay);

  return {
    highlights: highlights.length
      ? highlights
      : ['Eksplorasi destinasi pilihan dengan rute optimal', 'Rekomendasi kuliner & aktivitas harian terbaik'],
    itinerary,
    rawMarkdown: text,
  };
};

const getStyleActivities = (style: string, destination: string, spotName: string, dailyBudStr: string): string[] => {
  switch (style) {
    case 'luxury':
      return [
        `08:30 - Sarapan buffet eksklusif & Penjemputan Private Car (Estimasi harian ~${dailyBudStr})`,
        `10:30 - Kunjungan VIP & tur privat berpemandu di ${spotName}`,
        `13:00 - Makan siang Fine Dining kuliner berbintang khas ${destination}`,
        `16:00 - Sesi relaksasi Spa / Lounge pemandangan premium`,
        `19:30 - Candlelight Dinner romantis & pengalaman malam eksklusif`,
      ];
    case 'backpacker':
      return [
        `08:00 - Sarapan hemat lokal & berangkat naik transportasi umum`,
        `09:30 - Eksplorasi spot foto populer & jalan santai di ${spotName}`,
        `12:30 - Makan siang street food / kedai lokal favorit warga setempat`,
        `15:00 - Tur budaya mandiri & eksplorasi kawasan bersejarah ${destination}`,
        `18:30 - Berburu kuliner malam terjangkau di Night Market`,
      ];
    case 'culinary':
      return [
        `08:30 - Wisata kuliner sarapan legendaris khas ${destination}`,
        `10:30 - Mengunjungi pasar tradisional & cooking class masakan lokal`,
        `13:00 - Santap siang hidangan paling ikonik di ${spotName}`,
        `16:00 - Tasting dessert, kafe estetik & camilan manis khas setempat`,
        `19:00 - Wisata kuliner malam & eksplorasi rekomendasi resto terbaik`,
      ];
    case 'romantic':
      return [
        `09:00 - Sarapan santai dengan pemandangan indah bersama pasangan`,
        `11:00 - Jalan-jalan romantis & momen berfoto di ${spotName}`,
        `13:30 - Makan siang di kafe berkonsep intim & estetik`,
        `16:30 - Menikmati sunset di spot pemandangan terbaik ${destination}`,
        `19:30 - Dinner romantis spesial & menikmati suasana malam`,
      ];
    case 'solo':
      return [
        `08:00 - Morning walk & eksplor hidden gem di sekitar ${destination}`,
        `10:00 - Mengunjungi galeri/museum & tur mandiri di ${spotName}`,
        `12:30 - Makan siang santai di kafe lokal`,
        `15:00 - Photography walk & sosialisasi dengan warga lokal`,
        `18:30 - Santai malam di tempat musik lokal & eksplorasi bebas`,
      ];
    default: // family
      return [
        `08:30 - Penjemputan keluarga & sarapan ramah anak/semua usia`,
        `10:00 - Kunjungan ke wahana/area wisata keluarga di ${spotName}`,
        `13:00 - Makan siang bersama di restoran keluarga yang nyaman`,
        `15:30 - Aktivitas santai & berburu suvenir khas ${destination}`,
        `18:30 - Makan malam keluarga & kembali istirahat di hotel`,
      ];
  }
};

// ─── Main Component ───────────────────────────────────────────────────────────

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [destination, setDestination] = useState('');
  const [budget, setBudget] = useState('2000');
  const [days, setDays] = useState(3);
  const [travelStyle, setTravelStyle] = useState('family');
  const [styleSearchQuery, setStyleSearchQuery] = useState('');

  const [isGenerating, setIsGenerating] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [generatedResult, setGeneratedResult] = useState<TripResult | null>(null);

  useEffect(() => {
    // Load persisted result from localStorage
    try {
      const saved = localStorage.getItem('kelana_ai_trip');
      if (saved) {
        setGeneratedResult(JSON.parse(saved) as TripResult);
      }
    } catch (e) {
      console.error('Gagal membaca dari localStorage:', e);
    }

    // Check auth
    const checkAuth = async () => {
      try {
        const userData = await getMe();
        setUser(userData as User);
      } catch {
        setUser(null);
      }
    };

    checkAuth();
    window.addEventListener('auth-change', checkAuth);
    return () => window.removeEventListener('auth-change', checkAuth);
  }, []);

  const saveResult = (result: TripResult) => {
    setGeneratedResult(result);
    try {
      localStorage.setItem('kelana_ai_trip', JSON.stringify(result));
    } catch (e) {
      console.error('Gagal menyimpan ke localStorage:', e);
    }
  };

  const handleClearResult = () => {
    setGeneratedResult(null);
    localStorage.removeItem('kelana_ai_trip');
  };

  const handleResetForm = () => {
    setDestination('');
    setBudget('2000');
    setDays(3);
    setTravelStyle('family');
    setStyleSearchQuery('');
  };

  const handlePrint = () => {
    window.print();
  };

  const filteredTravelStyles = useMemo(() => {
    if (!styleSearchQuery.trim()) return TRAVEL_STYLES;
    const query = styleSearchQuery.toLowerCase();
    return TRAVEL_STYLES.filter(
      (style) =>
        style.name.toLowerCase().includes(query) ||
        style.desc.toLowerCase().includes(query)
    );
  }, [styleSearchQuery]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!destination.trim()) return;

    setIsGenerating(true);
    setGeneratedResult(null);

    const parsedBudget = parseFloat(budget) || 2000;
    const selectedStyleObj = TRAVEL_STYLES.find((s) => s.id === travelStyle);
    const styleLabel = selectedStyleObj ? selectedStyleObj.name : travelStyle;

    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') || '' : '';

      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const res = await fetch(`${API_BASE_URL}/trips`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          destination: destination.trim(),
          days,
          budget: parsedBudget,
          travel_style: travelStyle,
        }),
      });

      if (res.ok) {
        setLoadingStep('Memproses rekomendasi AI dari database...');
        const data = await res.json() as {
          id: number;
          destination: string;
          days: number;
          budget: number;
          ai_recommendation?: string;
        };
        const parsedAi = parseAiText(data.ai_recommendation || '');
        setIsGenerating(false);

        saveResult({
          id: data.id,
          destination: data.destination,
          days: data.days,
          budget: formatUSD(data.budget.toString()),
          dailyBudget: formatUSD((data.budget / data.days).toFixed(0)),
          style: styleLabel,
          highlights: parsedAi.highlights.length
            ? parsedAi.highlights
            : [
                `Pengalaman perjalanan ${styleLabel} selama ${data.days} hari`,
                `Alokasi total budget ${formatUSD(data.budget.toString())} (${formatUSD((data.budget / data.days).toFixed(0))}/hari)`,
              ],
          itinerary: parsedAi.itinerary,
          rawMarkdown: parsedAi.rawMarkdown,
        });
        return;
      }
    } catch (error: unknown) {
      console.log('Backend offline / error 500, menjalankan simulasi fallback presisi...', error);
    }

    // Fallback simulation
    setLoadingStep('Menganalisis karakteristik destinasi & gaya perjalanan...');
    setTimeout(() => setLoadingStep('Menghitung alokasi budget harian efisien...'), 1000);
    setTimeout(() => setLoadingStep(`Menyusun ${days} hari itinerary presisi...`), 2000);
    setTimeout(() => {
      setIsGenerating(false);

      const destLower = destination.trim().toLowerCase();
      const matchedSpots = DESTINATION_SPOTS[destLower] || [
        `Pusat Kota & Landmark Ikonik ${destination}`,
        `Kawasan Wisata & Spot Foto Populer`,
        `Kawasan Kuliner Khas ${destination}`,
        `Taman & Area Rekreasi Terkenal`,
        `Pusat Seni & Kebudayaan Lokal`,
      ];

      const dailyBudVal = formatUSD((parsedBudget / days).toFixed(0));
      const budgetTotalStr = formatUSD(budget);

      saveResult({
        destination,
        days,
        budget: budgetTotalStr,
        dailyBudget: dailyBudVal,
        style: styleLabel,
        highlights: [
          `Rute ${days} hari ${styleLabel} yang dirancang khusus untuk destinasi ${destination}`,
          `Total Anggaran: ${budgetTotalStr} dengan rata-rata estimasi ${dailyBudVal} per hari`,
          `Rekomendasi spot ikonik: ${matchedSpots.slice(0, 3).join(', ')}`,
          `Rangkaian aktivitas yang fleksibel & dioptimalkan sesuai preferensi ${styleLabel}`,
        ],
        itinerary: Array.from({ length: days }, (_, i) => {
          const spotName = matchedSpots[i % matchedSpots.length];
          return {
            day: i + 1,
            title: `Hari ke-${i + 1}: Eksplorasi ${spotName}`,
            activities: getStyleActivities(travelStyle, destination, spotName, dailyBudVal),
          };
        }),
      });
    }, 3200);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.25),rgba(255,255,255,0))] relative">

      {/* FULLSCREEN LOADING OVERLAY */}
      {isGenerating && (
        <div className="fixed inset-0 z-[100] bg-slate-950/90 backdrop-blur-xl flex flex-col items-center justify-center p-4 transition-all duration-300">
          <div className="relative max-w-lg w-full bg-slate-900/90 border border-indigo-500/30 rounded-3xl p-8 text-center shadow-2xl shadow-indigo-500/20 space-y-6 overflow-hidden">
            <div className="absolute -top-24 -left-24 w-48 h-48 bg-indigo-500/20 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-700"></div>
            <div className="relative mx-auto w-24 h-24 flex items-center justify-center">
              <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-blue-600 via-indigo-500 to-purple-600 animate-spin opacity-80 blur-sm"></div>
              <div className="relative w-20 h-20 rounded-full bg-slate-950 flex items-center justify-center text-4xl shadow-inner border border-indigo-400/30">
                ✈️
              </div>
            </div>
            <div className="space-y-2 relative z-10">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold uppercase tracking-wider">
                <SparklesIcon /> AI Trip Engine Active
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
                KELANA AI
              </h2>
              <p className="text-xs sm:text-sm font-bold tracking-widest text-indigo-400 uppercase">
                TRAVELING ASIK PAKE AI
              </p>
            </div>
            <div className="space-y-3 pt-2 relative z-10">
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 h-full w-full animate-pulse rounded-full"></div>
              </div>
              <p className="text-xs sm:text-sm text-slate-300 font-medium min-h-5 animate-fade-in">
                {loadingStep || 'Sedang menyusun petualangan impianmu...'}
              </p>
            </div>
            <div className="text-[11px] text-slate-500 italic pt-2 border-t border-slate-800/80">
              Menghubungkan ke server Kelana AI...
            </div>
          </div>
        </div>
      )}

      {/* Header Bar */}
      <header className="border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-gradient-to-tr from-blue-600 to-indigo-500 rounded-xl shadow-lg shadow-blue-500/30 text-white">
              <SparklesIcon />
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
              KelanaAI
            </span>
          </div>
          <div className="flex items-center gap-3">
            {user ? (
              <>
                <span className="text-sm text-slate-300 hidden sm:inline-block">
                  Halo, <span className="font-bold text-white">{user.name}</span>
                </span>
                <Link href="/profile" className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md transition">
                  👤 Profil
                </Link>
                <Link href="/chat" className="px-3 py-1.5 rounded-xl bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 text-xs font-semibold border border-indigo-500/30 transition">
                  💬 Chat AI
                </Link>
                <Link href="/trips" className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition">
                  📜 Riwayat
                </Link>
              </>
            ) : (
              <>
                <Link href="/login" className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition">
                  Login
                </Link>
                <Link href="/register" className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
                  Daftar
                </Link>
              </>
            )}
            <span className="text-xs font-medium px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              v2.0 Beta
            </span>
          </div>
        </div>
      </header>

      {/* Hero Banner */}
      <div className="w-full h-48 sm:h-72 relative overflow-hidden flex select-none pointer-events-none z-0">
        <div className="relative w-1/3 h-full border-r border-slate-900/50">
          <Image
            src="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80"
            alt="Landmark Jepang"
            fill
            className="object-cover"
            unoptimized
            priority
          />
        </div>
        <div className="relative w-1/3 h-full border-r border-slate-900/50">
          <Image
            src="https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80"
            alt="Landmark Bali"
            fill
            className="object-cover"
            unoptimized
            priority
          />
        </div>
        <div className="relative w-1/3 h-full">
          <Image
            src="https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=800&q=80"
            alt="Landmark Australia"
            fill
            className="object-cover"
            unoptimized
            priority
          />
        </div>
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent pointer-events-none"></div>
        <div className="absolute inset-0 bg-slate-900/20 mix-blend-multiply pointer-events-none"></div>
      </div>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 py-10 space-y-10">
        <div className="text-center space-y-3 max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs sm:text-sm font-medium">
            <SparklesIcon /> AI-Powered Travel Planner
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Plan Your Next Adventure with KelanaAI
          </h1>
          <p className="text-slate-400 text-sm sm:text-base">
            Atur anggaran, durasi, dan gaya liburanmu. Biarkan kecerdasan buatan menyusun jadwal perjalanan terbaik secara personal.
          </p>
        </div>

        {/* Form Input Card */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl shadow-2xl backdrop-blur-xl p-6 sm:p-8">
          <div className="flex justify-between items-center mb-6 pb-2 border-b border-slate-800">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              ✏️ Isi Form Perjalanan
            </h2>
            <button
              type="button"
              onClick={handleResetForm}
              className="text-xs px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center gap-1 cursor-pointer"
            >
              🔄 Reset Form
            </button>
          </div>

          <form onSubmit={handleGenerate} className="space-y-6">
            {/* Destinasi */}
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                <MapPinIcon />
                <span>DESTINASI TUJUAN (Pencarian Teks)</span>
              </label>
              <input
                type="text"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                placeholder="Cari atau ketik destinasi: Jepang, Bali, Yogyakarta, Swiss..."
                className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-white placeholder:text-slate-500 text-base"
                required
              />
              <div className="flex flex-wrap items-center gap-2 pt-1">
                <span className="text-xs text-slate-400">Pilihan populer:</span>
                {QUICK_DESTINATIONS.map((dest) => (
                  <button
                    key={dest}
                    type="button"
                    onClick={() => setDestination(dest.split(' ')[0])}
                    className="text-xs px-2.5 py-1 rounded-lg bg-slate-800/60 hover:bg-slate-800 text-slate-300 border border-slate-700/50 transition cursor-pointer"
                  >
                    {dest}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Budget */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                  <WalletIcon />
                  <span>ANGGARAN (USD)</span>
                </label>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  placeholder="2000"
                  step="100"
                  min="50"
                  className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-white placeholder:text-slate-500 text-base"
                />
                <p className="text-xs text-emerald-400 font-medium pt-0.5">
                  Estimasi: {formatUSD(budget) || '$0'}
                </p>
              </div>

              {/* Days */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                  <CalendarIcon />
                  <span>DURASI PERJALANAN (HARI)</span>
                </label>
                <div className="flex items-center gap-3">
                  <button
                    type="button"
                    onClick={() => setDays(Math.max(1, days - 1))}
                    className="w-12 h-12 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xl font-bold flex items-center justify-center transition border border-slate-700 cursor-pointer"
                  >
                    -
                  </button>
                  <div className="flex-1 text-center py-2.5 bg-slate-950/80 border border-slate-800 rounded-xl font-bold text-lg text-indigo-400">
                    {days} Hari
                  </div>
                  <button
                    type="button"
                    onClick={() => setDays(days + 1)}
                    className="w-12 h-12 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xl font-bold flex items-center justify-center transition border border-slate-700 cursor-pointer"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            {/* Travel Style */}
            <div className="space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                  <CompassIcon />
                  <span>GAYA PERJALANAN (Travel Style)</span>
                </label>
                <input
                  type="text"
                  value={styleSearchQuery}
                  onChange={(e) => setStyleSearchQuery(e.target.value)}
                  placeholder="🔍 Cari gaya (misal: Mewah, Backpacker)..."
                  className="px-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-lg text-white placeholder:text-slate-500 focus:ring-1 focus:ring-indigo-500 outline-none w-full sm:w-64"
                />
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {filteredTravelStyles.length > 0 ? (
                  filteredTravelStyles.map((style) => (
                    <button
                      key={style.id}
                      type="button"
                      onClick={() => setTravelStyle(style.id)}
                      className={`p-3.5 rounded-xl border text-left transition flex flex-col justify-between gap-2 cursor-pointer ${
                        travelStyle === style.id
                          ? 'bg-indigo-600 border-indigo-500'
                          : 'bg-slate-800/50 border-slate-700 hover:border-slate-600'
                      }`}
                    >
                      <span className="text-2xl">{style.icon}</span>
                      <div>
                        <h4 className="text-sm font-bold text-white">{style.name}</h4>
                        <p className="text-xs text-slate-400">{style.desc}</p>
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="col-span-2 sm:col-span-3 text-center py-4 text-xs text-slate-400 bg-slate-950/50 rounded-xl border border-slate-800">
                    Gaya liburan &ldquo;{styleSearchQuery}&rdquo; tidak ditemukan.
                  </div>
                )}
              </div>
            </div>

            <button
              type="submit"
              disabled={isGenerating}
              className="w-full py-4 bg-gradient-to-r from-blue-600 hover:from-blue-500 to-indigo-600 hover:to-indigo-500 text-white rounded-xl font-bold text-lg shadow-lg shadow-blue-500/30 transition disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer"
            >
              Generate Itinerary
            </button>
          </form>
        </div>

        {/* Results Section */}
        {generatedResult && (
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 mt-10">
            <div className="flex flex-wrap justify-between items-center gap-3 pb-4 border-b border-slate-800">
              <h3 className="text-2xl font-bold text-white">🎉 Itinerary Anda Sudah Siap!</h3>
              <div className="flex items-center gap-3">
                <button
                  onClick={handlePrint}
                  className="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition flex items-center gap-1.5 cursor-pointer shadow-md shadow-indigo-600/20"
                >
                  🖨️ Print / Simpan PDF
                </button>
                <button
                  onClick={handleClearResult}
                  className="px-3.5 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 text-xs font-bold transition cursor-pointer"
                >
                  🗑️ Hapus
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Destinasi</span>
                <span className="text-lg font-bold text-indigo-400">{generatedResult.destination}</span>
              </div>
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Total Budget</span>
                <span className="text-lg font-bold text-emerald-400">{generatedResult.budget}</span>
              </div>
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Durasi</span>
                <span className="text-lg font-bold text-amber-400">{generatedResult.days} Hari</span>
              </div>
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-xs text-slate-400 block mb-1">Gaya Perjalanan</span>
                <span className="text-lg font-bold text-sky-400">{generatedResult.style}</span>
              </div>
            </div>

            {generatedResult.highlights.length > 0 && (
              <div className="space-y-3">
                <h4 className="font-bold text-white">✨ Sorotan Perjalanan</h4>
                <ul className="space-y-2">
                  {generatedResult.highlights.map((highlight, idx) => (
                    <li key={idx} className="flex items-start text-sm text-slate-300">
                      <CheckCircleIcon />
                      <span>{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {generatedResult.itinerary.length > 0 && (
              <div className="space-y-4 pt-4 border-t border-slate-800">
                <h4 className="font-bold text-white text-lg">📅 Jadwal Harian ({generatedResult.days} Hari)</h4>
                <div className="space-y-4">
                  {generatedResult.itinerary.map((dayPlan, idx) => (
                    <div key={idx} className="bg-slate-800/30 rounded-xl p-4 border border-slate-700/50">
                      <h5 className="font-bold text-indigo-300 mb-3">{dayPlan.title}</h5>
                      <ul className="space-y-2 pl-2 border-l-2 border-indigo-500/30">
                        {dayPlan.activities.map((act, actIdx) => (
                          <li key={actIdx} className="text-sm text-slate-300 pl-4 relative">
                            <span className="absolute -left-[5px] top-1.5 w-2 h-2 rounded-full bg-indigo-400"></span>
                            {act}
                          </li>
                        ))}
                      </ul>
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
