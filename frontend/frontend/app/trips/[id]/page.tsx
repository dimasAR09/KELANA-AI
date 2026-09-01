'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { getTrip, deleteTrip } from '@/services/tripService';
import { Trip } from '@/types';

export default function TripDetailPage() {
  const router = useRouter();
  const params = useParams();
  const id = params?.id as string;

  const [trip, setTrip] = useState<Trip | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    async function loadDetail() {
      try {
        const data = await getTrip(id);
        setTrip(data);
      } catch (err: unknown) {
        console.error(err);
        setError(`Trip dengan ID #${id} tidak ditemukan.`);
      } finally {
        setLoading(false);
      }
    }
    loadDetail();
  }, [id]);

  const handleDelete = async () => {
    if (!trip) return;
    if (confirm(`Apakah Anda yakin ingin menghapus itinerary ke ${trip.destination}?`)) {
      try {
        await deleteTrip(trip.id);
        router.push('/trips');
      } catch (err: unknown) {
        alert(err instanceof Error ? err.message : 'Gagal menghapus trip');
      }
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-300 flex items-center justify-center">
        Memuat detail trip dari PostgreSQL...
      </div>
    );
  }

  if (error || !trip) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-300 p-8 flex flex-col items-center justify-center space-y-4">
        <p className="text-red-400">⚠️ {error}</p>
        <Link href="/trips" className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold">
          ← Back to Trips
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-4 sm:p-8">
      <main className="max-w-4xl mx-auto space-y-8">
        <div className="flex flex-wrap items-center justify-between gap-4 print:hidden">
          <Link
            href="/trips"
            className="inline-flex items-center gap-2 text-slate-400 hover:text-white text-sm font-semibold transition"
          >
            ← Back to Trips
          </Link>

          <div className="flex items-center gap-3">
        <button
          onClick={handlePrint}
          className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-200 text-xs font-bold transition flex items-center gap-1.5 cursor-pointer"
        >
          🖨️ Save / Print
        </button>
        <button
          onClick={handleDelete}
          className="px-4 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 text-xs font-bold transition cursor-pointer"
        >
          🗑️ Delete Trip
        </button>
      </div>
    </div>

    <div>
      <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
        {trip.destination}
      </h1>
      <p className="text-xs text-slate-400 mt-1">Trip ID: #{trip.id}</p>
    </div>

    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
        <span className="text-[10px] font-extrabold uppercase text-slate-400 tracking-wider">
          DESTINATION
        </span>
        <p className="text-lg font-bold text-white mt-1">{trip.destination}</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
        <span className="text-[10px] font-extrabold uppercase text-slate-400 tracking-wider">
          BUDGET
        </span>
        <p className="text-lg font-bold text-emerald-400 mt-1">
          USD {trip.budget?.toLocaleString()}
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
        <span className="text-[10px] font-extrabold uppercase text-slate-400 tracking-wider">
          CATEGORY
        </span>
        <div className="mt-1">
          <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 font-bold">
            {trip.category || 'Standard'}
          </span>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl">
        <span className="text-[10px] font-extrabold uppercase text-slate-400 tracking-wider">
          DAYS
        </span>
        <p className="text-lg font-bold text-white mt-1">{trip.days} days</p>
      </div>
    </div>

    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-4">
      <div className="flex items-center gap-2 border-b border-slate-800 pb-4">
        <span className="text-xl">✨</span>
        <h2 className="text-sm font-extrabold uppercase tracking-wider text-indigo-400">
          AI RECOMMENDATION (AWS Bedrock)
        </h2>
      </div>

      {trip.ai_recommendation ? (
        <div className="prose prose-invert max-w-none text-sm text-slate-300 leading-relaxed whitespace-pre-line">
          {trip.ai_recommendation}
        </div>
      ) : (
        <p className="text-sm text-slate-500 italic">
          Belum ada AI recommendation tersimpan untuk trip ini.
        </p>
      )}
    </div>
  </main>
</div>
  );
}