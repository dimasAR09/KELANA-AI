'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import TripCard from '@/components/TripCard';
import { getTrips, deleteTrip } from '@/services/tripService';
import { Trip, SortOption } from '@/types';

// Batas maksimal trip per halaman
const ITEMS_PER_PAGE = 100;

export default function TripHistoryPage() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('latest');
  const [currentPage, setCurrentPage] = useState(1);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  // Ambil data trip dari backend PostgreSQL
  const fetchTripsData = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getTrips();
      if (Array.isArray(data)) {
        setTrips(data);
      } else {
        setTrips([]);
        console.error('Format data dari backend bukan array:', data);
      }
    } catch (err: any) {
      console.error('Error fetching trips:', err);
      setError(
        err?.message || 'Gagal memuat data perjalanan dari database PostgreSQL.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTripsData();
  }, []);

  // Filter berdasarkan pencarian teks (Destination atau Travel Style/Category)
  const filteredTrips = useMemo(() => {
    return trips.filter((t) => {
      const query = searchQuery.toLowerCase();
      const matchDest = t.destination?.toLowerCase().includes(query);
      const matchStyle =
        t.travel_style?.toLowerCase().includes(query) ||
        t.category?.toLowerCase().includes(query);
      return matchDest || matchStyle;
    });
  }, [trips, searchQuery]);

  // Pengurutan data (Latest, Oldest, Highest Budget)
  const sortedTrips = useMemo(() => {
    const list = [...filteredTrips];
    if (sortBy === 'latest') {
      return list.sort((a, b) => b.id - a.id);
    } else if (sortBy === 'oldest') {
      return list.sort((a, b) => a.id - b.id);
    } else if (sortBy === 'highest_budget') {
      return list.sort((a, b) => (b.budget || 0) - (a.budget || 0));
    }
    return list;
  }, [filteredTrips, sortBy]);

  // Kalkulasi Pagination
  const totalPages = Math.ceil(sortedTrips.length / ITEMS_PER_PAGE) || 1;
  const paginatedTrips = useMemo(() => {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    return sortedTrips.slice(start, start + ITEMS_PER_PAGE);
  }, [sortedTrips, currentPage]);

  // Fungsi memicu modal konfirmasi hapus
  const handleDelete = (id: number) => {
    setDeletingId(id);
  };

  // Fungsi mengeksekusi penghapusan trip
  const confirmDelete = async () => {
    if (!deletingId) return;
    const targetId = deletingId;
    setDeletingId(null);
    try {
      await deleteTrip(targetId);
      setTrips((prev) => prev.filter((item) => item.id !== targetId));
    } catch (err: any) {
      alert(err?.message || 'Gagal menghapus trip');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-4 sm:p-8">
      <main className="max-w-4xl mx-auto space-y-6">
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Link
                href="/"
                className="text-indigo-400 hover:text-indigo-300 font-bold text-xl transition"
              >
                KelanaAI
              </Link>
              <span className="text-slate-600">/</span>
              <span className="text-slate-400 text-sm">My Trips</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">
              Trip History
            </h1>
            <p className="text-xs text-slate-400">
              {filteredTrips.length} saved itineraries in PostgreSQL
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={fetchTripsData}
              className="px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer"
            >
              🔄 Refresh
            </button>
            <Link
              href="/"
              className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-md shadow-indigo-600/20"
            >
              + Create New Trip
            </Link>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="sm:col-span-2 relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
              placeholder="🔍 Search by Destination or Travel Style (e.g. Japan, Backpacker)..."
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm text-white placeholder-slate-500"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-3 text-xs text-slate-400 hover:text-white"
              >
                ✕
              </button>
            )}
          </div>

          <div>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm text-slate-300 cursor-pointer"
            >
              <option value="latest">Sort: Latest (Newest)</option>
              <option value="oldest">Sort: Oldest</option>
              <option value="highest_budget">Sort: Highest Budget</option>
            </select>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-16 text-slate-400 animate-pulse">
            Memuat daftar rute liburan dari database PostgreSQL...
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 p-4 rounded-xl text-red-400 text-sm">
            ⚠️ {error}
          </div>
        )}

        {/* List Content */}
        {!loading && !error && (
          <div className="space-y-4">
            {paginatedTrips.length > 0 ? (
              paginatedTrips.map((t) => (
                <TripCard key={t.id} trip={t} onDelete={handleDelete} />
              ))
            ) : (
              <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-12 text-center text-slate-400">
                {searchQuery
                  ? `Tidak ada data trip yang cocok dengan pencarian "${searchQuery}".`
                  : 'Belum ada data trip yang tersimpan.'}
              </div>
            )}
          </div>
        )}

        {/* Navigasi Pagination (Selalu Muncul) */}
        {!loading && !error && (
          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold disabled:opacity-40 disabled:cursor-not-allowed hover:border-slate-700 cursor-pointer transition"
            >
              ← Previous
            </button>

            <span className="text-xs text-slate-400">
              Page {currentPage} of {totalPages}
            </span>

            <button
              disabled={currentPage >= totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold disabled:opacity-40 disabled:cursor-not-allowed hover:border-slate-700 cursor-pointer transition"
            >
              Next →
            </button>
          </div>
        )}
      </main>

      {/* Modal Dialog Hapus */}
      {deletingId !== null && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl max-w-sm w-full space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">Konfirmasi Hapus</h3>
            <p className="text-sm text-slate-400">
              Apakah Anda yakin ingin menghapus trip ID #{deletingId}? Tindakan ini tidak dapat dibatalkan.
            </p>
            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setDeletingId(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
              >
                Batal
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-semibold transition shadow-md shadow-red-600/20"
              >
                Hapus
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}