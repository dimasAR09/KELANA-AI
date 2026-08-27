'use client';

import React from 'react';
import Link from 'next/link';
import { Trip } from '@/types';

interface TripCardProps {
  trip: Trip;
  onDelete?: (id: number) => void;
}

export default function TripCard({ trip, onDelete }: TripCardProps) {
  const getCategoryBadgeClass = (category: string) => {
    switch (category?.toLowerCase()) {
      case 'luxury':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'backpacker':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      default:
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
    }
  };

  return (
    <div className="group bg-slate-900/80 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 transition-all duration-300 hover:shadow-xl hover:shadow-indigo-500/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-600/20 to-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </div>
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-lg font-bold text-white group-hover:text-indigo-300 transition-colors">
              {trip.destination}
            </h3>
            <span className={`text-xs px-2.5 py-0.5 rounded-full border font-medium ${getCategoryBadgeClass(trip.category)}`}>
              {trip.category || 'Standard'}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            {trip.days} days &middot; USD {trip.budget?.toLocaleString()} &middot; {trip.travel_style || 'Family'}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
        {onDelete && (
          <button
            onClick={() => onDelete(trip.id)}
            title="Hapus Trip"
            className="px-3 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 text-xs font-semibold transition cursor-pointer"
          >
            🗑️
          </button>
        )}
        <Link
          href={`/trips/${trip.id}`}
          className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/20 transition cursor-pointer"
        >
          <span>View Details</span>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </Link>
      </div>
    </div>
  );
}