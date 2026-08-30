'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getMe, getTrips } from '@/services/tripService';
import { User } from '@/types';

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [tripCount, setTripCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userData = await getMe();
        setUser(userData);
        const trips = await getTrips();
        setTripCount(trips.length);
      } catch (err) {
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('kelana_token');
    window.dispatchEvent(new Event('auth-change'));
    router.push('/login');
  };

  if (loading) return <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">Memuat profil...</div>;

  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <Link href="/" className="text-indigo-400 hover:text-indigo-300 text-sm font-bold">← Kembali ke Beranda</Link>
        
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-20 h-20 bg-gradient-to-tr from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-3xl font-bold text-white shadow-lg">
              {user?.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">{user?.name}</h1>
              <p className="text-slate-400">{user?.email}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="bg-slate-950 border border-slate-800 p-5 rounded-2xl">
              <span className="text-xs font-bold text-slate-500 block mb-1">TOTAL TRIP DIHASILKAN</span>
              <span className="text-3xl font-extrabold text-indigo-400">{tripCount}</span>
            </div>
            <div className="bg-slate-950 border border-slate-800 p-5 rounded-2xl flex flex-col justify-center">
               <Link href="/trips" className="text-sm font-bold text-emerald-400 hover:text-emerald-300 flex items-center justify-between">
                  Lihat Riwayat Perjalanan <span>→</span>
               </Link>
            </div>
          </div>
          
          <button onClick={handleLogout} className="w-full py-3 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-xl font-bold transition cursor-pointer">
            Keluar (Logout)
          </button>
        </div>
      </div>
    </div>
  );
}