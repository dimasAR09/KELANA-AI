'use client';
import React, { useState } from 'react';
import Image from "next/image";
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
  <svg className="w-5 h-5 text-emerald-500 inline mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);
const QUICK_DESTINATIONS = ['Japan 🇯🇵', 'Bali 🏝️', 'Australia 🇦🇺'];
// Spot wisata bawaan sesuai lokasi pilihan
const DESTINATION_SPOTS: Record<string, string[]> = {
  japan: ["Tokyo Tower", "Shibuya", "Mount Fuji"],
  jepang: ["Tokyo Tower", "Shibuya", "Mount Fuji"],
  bali: ["Ubud", "Kuta Beach", "Pandawa Beach"],
  australia: ["Sydney", "Melbourne", "Queensland"],
};
const TRAVEL_STYLES = [
  { id: 'family', name: 'Keluarga', icon: '👨‍👩‍👧‍👦', desc: 'Nyaman & santai' },
  { id: 'backpacker', name: 'Hemat / Backpacker', icon: '🎒', desc: 'Efisien & terjangkau' },
  { id: 'luxury', name: 'Mewah', icon: '✨', desc: 'Eksklusif & premium' },
  { id: 'solo', name: 'Solo Adventure', icon: '🧗', desc: 'Bebas & eksploratif' },
  { id: 'romantic', name: 'Pasangan', icon: '👩‍❤️‍👨', desc: 'Romantis & intim' },
  { id: 'culinary', name: 'Kuliner', icon: '🍜', desc: 'Eksplor makanan lokal' },
];
export default function Home() {
  const [destination, setDestination] = useState('');
  const [budget, setBudget] = useState('2000');
  const [days, setDays] = useState(3);
  const [travelStyle, setTravelStyle] = useState('family');
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [generatedResult, setGeneratedResult] = useState<any>(null);
  React.useEffect(() => {
    try {
      const saved = localStorage.getItem('kelana_ai_trip');
      if (saved) {
        setGeneratedResult(JSON.parse(saved));
      }
    } catch (e) {
      console.error('Gagal membaca dari localStorage:', e);
    }
  }, []);
  // Helper untuk menyimpan hasil ke state & localStorage
  const saveResult = (result: any) => {
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
  const formatUSD = (val: string) => {
    const num = parseInt(val.replace(/\D/g, ''), 10);
    if (isNaN(num)) return '';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
  };
  const parseAiText = (text: string) => {
    if (!text) return { highlights: [], itinerary: [], rawMarkdown: '' };
    const trimmed = text.trim();
    // 1. Coba parse HANYA jika string diawali karakter JSON valid ('{' atau '[')
    if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
      try {
        const parsed = JSON.parse(trimmed);
        if (parsed && (parsed.itinerary || parsed.highlights)) {
          return {
            highlights: parsed.highlights || [],
            itinerary: parsed.itinerary || [],
            rawMarkdown: ''
          };
        }
      } catch (e) {
        // Abaikan jika ternyata bukan JSON valid
      }
    }
    // 2. Parse format Teks Markdown jika dari AWS Bedrock
    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);
    const highlights: string[] = [];
    const itinerary: { day: number; title: string; activities: string[] }[] = [];
    let currentDay: { day: number; title: string; activities: string[] } | null = null;
    let inOverview = false;
    let inTips = false;
    for (const line of lines) {
      if (line.includes('Trip Overview')) {
        inOverview = true;
        continue;
      }
      if (line.includes('Daily Itinerary') || line.includes('Day 1')) {
        inOverview = false;
      }
      if (line.includes('Essential Tips') || line.includes('Top 5 Insider Tips')) {
        inTips = true;
        inOverview = false;
        if (currentDay) {
          itinerary.push(currentDay);
          currentDay = null;
        }
        continue;
      }
      // Lewati baris metadata overview agar tidak masuk ke sorotan/highlights
      if (inOverview && (line.includes('Destination:') || line.includes('Duration:') || line.includes('Budget:') || line.includes('Travel Style:'))) {
        continue;
      }
      // Deteksi header hari (misal: "## Day 1", "Hari 1", "**Day 1**")
      const dayMatch = line.match(/^(?:#+\s*|\*\*|)(?:🌅\s*)?(Day|Hari)\s*(\d+)\s*[:\-\|]?\s*(.*?)(?:\*\*|)$/i);
      if (dayMatch) {
        if (currentDay) itinerary.push(currentDay);
        const dayNum = parseInt(dayMatch[2], 10);
        const titleText = dayMatch[3] ? dayMatch[3].replace(/^\*+|\*+$/g, '').trim() : `Eksplorasi Hari ${dayNum}`;
        currentDay = {
          day: dayNum,
          title: `Hari ke-${dayNum}: ${titleText || 'Aktivitas Wisata'}`,
          activities: []
        };
        inOverview = false;
        inTips = false;
        continue;
      }
      // Deteksi poin aktivitas / bullet point
      if (line.startsWith('-') || line.startsWith('*') || line.match(/^\d+\./)) {
        const cleanLine = line.replace(/^[\-\*\d\.]+\s*/, '').replace(/\*\*/g, '').trim();
        if (currentDay) {
          currentDay.activities.push(cleanLine);
        } else if (inTips && highlights.length < 4) {
          highlights.push(cleanLine);
        }
      } else if (!line.startsWith('#') && !currentDay && !inOverview && highlights.length < 3) {
        const cleanLine = line.replace(/^[#\*\s]+/, '').trim();
        if (cleanLine && !cleanLine.includes('Destination') && !cleanLine.includes('Budget')) highlights.push(cleanLine);
      }
    }
    if (currentDay) itinerary.push(currentDay);
    return {
      highlights: highlights.length ? highlights : [
        'Eksplorasi destinasi pilihan dengan rute optimal',
        'Rekomendasi kuliner & aktivitas harian terbaik'
      ],
      itinerary,
      rawMarkdown: text
    };
  };
  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!destination.trim()) return;
    setIsGenerating(true);
    setGeneratedResult(null);
    setLoadingStep('Mengirim data ke server backend Python (:8000)...');
    
    const parsedBudget = parseFloat(budget) || 2000;
    try {
      // Panggil REST API backend Python (FastAPI + SQLAlchemy)
      const res = await fetch('http://localhost:8000/api/v1/trips', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          destination: destination.trim(),
          days: days,
          budget: parsedBudget,
          travel_style: travelStyle,
        })
      });
      if (!res.ok) {
        throw new Error(`Server backend merespons error status: ${res.status}`);
      }
      setLoadingStep('Memproses rekomendasi AI dari database...');
      const data = await res.json();
      
      // Mengurai rekomendasi tanpa memicu SyntaxError JSON parse
      const parsedAi = parseAiText(data.ai_recommendation || '');
      setIsGenerating(false);
      const newResult = {
        id: data.id,
        destination: data.destination,
        days: data.days,
        budget: formatUSD(data.budget.toString()),
        dailyBudget: formatUSD(data.daily_budget.toString()),
        style: TRAVEL_STYLES.find(s => s.id === data.category)?.name || data.category,
        highlights: parsedAi.highlights,
        itinerary: parsedAi.itinerary,
        rawMarkdown: parsedAi.rawMarkdown
      };
      saveResult(newResult);
      return;
    } catch (error) {
      console.log('Backend offline / error, menjalankan simulasi fallback di frontend...', error);
    }
    // Fallback jika server backend belum dinyalakan atau error
    setLoadingStep('Menganalisis karakteristik destinasi...');
    setTimeout(() => setLoadingStep('Menghitung estimasi biaya & akomodasi...'), 1000);
    setTimeout(() => setLoadingStep('Menyusun itinerary harian yang optimal...'), 2000);
    setTimeout(() => {
      setIsGenerating(false);
      
      const destLower = destination.trim().toLowerCase();
      const matchedSpots = DESTINATION_SPOTS[destLower] || [
        `Destinasi utama di ${destination}`,
        `Spot foto populer & pusat kota`,
        `Kawasan wisata favorit`
      ];
      const fallbackResult = {
        destination,
        days,
        budget: formatUSD(budget),
        dailyBudget: formatUSD((parsedBudget / days).toFixed(0)),
        style: TRAVEL_STYLES.find(s => s.id === travelStyle)?.name || travelStyle,
        highlights: [
          `Mengunjungi spot ikonik: ${matchedSpots.join(', ')}`,
          `Rekomendasi akomodasi efisien untuk ${days} hari`,
          `Rute perjalanan harian yang efektif & hemat waktu`,
        ],
        itinerary: Array.from({ length: Math.min(days, 5) }, (_, i) => {
          const spotName = matchedSpots[i % matchedSpots.length];
          return {
            day: i + 1,
            title: `Hari ke-${i + 1}: Eksplorasi ${spotName}`,
            activities: [
              `08:00 - Penjemputan / Sarapan lokal di ${destination}`,
              `10:00 - Kunjungan utama & aktivitas di ${spotName}`,
              `13:00 - Makan siang kuliner lokal khas setempat`,
              `16:00 - Santai & eksplorasi area sekitar ${spotName}`,
              `19:00 - Makan malam & berburu suvenir`,
            ]
          };
        })
      };
      saveResult(fallbackResult);
    }, 3200);
  };
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.25),rgba(255,255,255,0))] relative">
      
      {/* FULLSCREEN LOADING STAGE OVERLAY */}
      {isGenerating && (
        <div className="fixed inset-0 z-[100] bg-slate-950/90 backdrop-blur-xl flex flex-col items-center justify-center p-4 transition-all duration-300">
          <div className="relative max-w-lg w-full bg-slate-900/90 border border-indigo-500/30 rounded-3xl p-8 text-center shadow-2xl shadow-indigo-500/20 space-y-6 overflow-hidden">
            
            {/* Ambient Background Glow Effect */}
            <div className="absolute -top-24 -left-24 w-48 h-48 bg-indigo-500/20 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-700"></div>
            {/* Travel & AI Animated Badge */}
            <div className="relative mx-auto w-24 h-24 flex items-center justify-center">
              <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-blue-600 via-indigo-500 to-purple-600 animate-spin opacity-80 blur-sm"></div>
              <div className="relative w-20 h-20 rounded-full bg-slate-950 flex items-center justify-center text-4xl shadow-inner border border-indigo-400/30">
                ✈️
              </div>
            </div>
            {/* Title & Tagline Branding */}
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
            {/* Loading Indicator & Status Bar */}
            <div className="space-y-3 pt-2 relative z-10">
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 h-full w-full animate-pulse rounded-full"></div>
              </div>
              <p className="text-xs sm:text-sm text-slate-300 font-medium min-h-[20px] animate-fade-in">
                {loadingStep || 'Sedang menyusun petualangan impianmu...'}
              </p>
            </div>
            <div className="text-[11px] text-slate-500 italic pt-2 border-t border-slate-800/80">
              Menghubungkan ke server backend FastAPI & AI Bedrock...
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
          <span className="text-xs font-medium px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
            v2.0 Beta
          </span>
        </div>
      </header>

      {/* Hero Banner collage containing iconic landmarks */}
      <div className="w-full h-48 sm:h-72 md:h-[360px] relative overflow-hidden flex select-none pointer-events-none z-0">
        <img
          src="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80"
          alt="Landmark Jepang"
          className="w-1/3 h-full object-cover border-r border-slate-900/50"
        />
        <img
          src="https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80"
          alt="Landmark Bali"
          className="w-1/3 h-full object-cover border-r border-slate-900/50"
        />
        <img
          src="https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=800&q=80"
          alt="Landmark Australia"
          className="w-1/3 h-full object-cover"
        />
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
        {/* Input Form Card */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl shadow-2xl backdrop-blur-xl p-6 sm:p-8">
          <form onSubmit={handleGenerate} className="space-y-6">
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                <MapPinIcon />
                <span>DESTINASI TUJUAN</span>
              </label>
              <input
                type="text"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                placeholder="Misal: Jepang, Bali, Yogyakarta, Swiss..."
                className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-white placeholder-slate-500 text-base"
                required
              />
              <div className="flex flex-wrap items-center gap-2 pt-1">
                <span className="text-xs text-slate-400">Pilihan populer:</span>
                {QUICK_DESTINATIONS.map((dest) => (
                  <button
                    key={dest}
                    type="button"
                    onClick={() => setDestination(dest.split(' ')[0])}
                    className="text-xs px-2.5 py-1 rounded-lg bg-slate-800/60 hover:bg-slate-800 text-slate-300 border border-slate-700/50 transition"
                  >
                    {dest}
                  </button>
                ))}
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Budget Input */}
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
                  className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-white placeholder-slate-500 text-base"
                />
                <p className="text-xs text-emerald-400 font-medium pt-0.5">
                  Estimasi: {formatUSD(budget) || '$0'}
                </p>
              </div>
              {/* Days Counter */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                  <CalendarIcon />
                  <span>DURASI PERJALANAN (HARI)</span>
                </label>
                <div className="flex items-center gap-3">
                  <button
                    type="button"
                    onClick={() => setDays(Math.max(1, days - 1))}
                    className="w-12 h-12 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xl font-bold flex items-center justify-center transition border border-slate-700"
                  >
                    -
                  </button>
                  <div className="flex-1 text-center py-2.5 bg-slate-950/80 border border-slate-800 rounded-xl font-bold text-lg text-indigo-400">
                    {days} Hari
                  </div>
                  <button
                    type="button"
                    onClick={() => setDays(days + 1)}
                    className="w-12 h-12 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xl font-bold flex items-center justify-center transition border border-slate-700"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>
            {/* Travel Style Selection */}
            <div className="space-y-3">
              <label className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                <CompassIcon />
                <span>GAYA PERJALANAN</span>
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {TRAVEL_STYLES.map((style) => (
                  <button
                    key={style.id}
                    type="button"
                    onClick={() => setTravelStyle(style.id)}
                    className={`p-3.5 rounded-xl border text-left transition flex flex-col justify-between gap-2 ${
                      travelStyle === style.id
                        ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg shadow-indigo-500/10'
                        : 'bg-slate-950/40 border-slate-800 hover:border-slate-700 text-slate-400'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-2xl">{style.icon}</span>
                      {travelStyle === style.id && (
                        <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
                      )}
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-slate-200">{style.name}</p>
                      <p className="text-xs text-slate-400 font-normal">{style.desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
            {/* Submit Button */}
            <button
              type="submit"
              disabled={isGenerating}
              className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:via-indigo-500 hover:to-purple-500 text-white font-bold text-base shadow-xl shadow-indigo-500/20 flex items-center justify-center gap-2 transition disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {isGenerating ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{loadingStep || 'Menyusun Rencana AI...'}</span>
                </>
              ) : (
                <>
                  <SparklesIcon />
                  <span>Buat Rencana Liburan dengan AI</span>
                </>
              )}
            </button>
          </form>
        </div>
        {/* AI Result Cards */}
        {generatedResult && (
          <div className="bg-slate-900 border border-indigo-500/30 rounded-2xl p-6 sm:p-8 space-y-6 shadow-2xl">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
              <div>
                <span className="text-xs uppercase tracking-wider text-indigo-400 font-bold">Rencana Perjalanan AI</span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">
                  Itinerary {generatedResult.destination}
                </h2>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-3 py-1 rounded-full bg-slate-800 text-slate-300 text-xs font-medium border border-slate-700">
                  ⏱️ {generatedResult.days} Hari
                </span>
                <span className="px-3 py-1 rounded-full bg-slate-800 text-emerald-400 text-xs font-medium border border-slate-700">
                  💵 {generatedResult.budget}
                </span>
                <span className="px-3 py-1 rounded-full bg-slate-800 text-purple-400 text-xs font-medium border border-slate-700">
                  ✨ {generatedResult.style}
                </span>
                <button
                  type="button"
                  onClick={handleClearResult}
                  className="px-3 py-1 rounded-full bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-medium border border-red-500/20 transition cursor-pointer"
                  title="Hapus Rencana Tersimpan"
                >
                  🗑️ Hapus
                </button>
              </div>
            </div>
            <div className="bg-indigo-950/30 border border-indigo-500/20 rounded-xl p-4">
              <h4 className="text-sm font-semibold text-indigo-300 mb-2">💡 Sorotan Rencana Ini:</h4>
              <ul className="space-y-1.5 text-xs sm:text-sm text-slate-300">
                {generatedResult.highlights.map((h: string, idx: number) => (
                  <li key={idx} className="flex items-center">
                    <CheckCircleIcon /> {h}
                  </li>
                ))}
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="text-base sm:text-lg font-bold text-white">Jadwal Harian:</h3>
              
              {generatedResult.itinerary && generatedResult.itinerary.length > 0 ? (
                <div className="grid grid-cols-1 gap-4">
                  {generatedResult.itinerary.map((item: any) => (
                    <div key={item.day} className="bg-slate-950/60 border border-slate-800 rounded-xl p-5 space-y-3">
                      <h4 className="text-sm sm:text-base font-bold text-blue-400">{item.title}</h4>
                      <ul className="space-y-2">
                        {item.activities.map((act: string, aIdx: number) => (
                          <li key={aIdx} className="text-xs sm:text-sm text-slate-300 flex items-start gap-2">
                            <span className="text-indigo-400 text-xs mt-0.5">●</span>
                            <span>{act}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              ) : generatedResult.rawMarkdown ? (
                <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-5 text-sm text-slate-300 whitespace-pre-line leading-relaxed">
                  {generatedResult.rawMarkdown}
                </div>
              ) : null}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}