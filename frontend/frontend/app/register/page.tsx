'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { registerUser } from '@/services/tripService';

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await registerUser({ name, email, password });
      alert('Registrasi berhasil! Silakan login.');
      router.push('/login');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-2 text-center">Buat Akun KelanaAI</h2>
        <p className="text-slate-400 text-sm text-center mb-6">Mulai rencanakan liburan Anda dengan AI</p>
        
        {error && <div className="bg-red-500/10 text-red-400 p-3 rounded-lg text-sm mb-4">{error}</div>}
        
        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-400 mb-1">NAMA LENGKAP</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} required 
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 mb-1">EMAIL</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required 
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 mb-1">PASSWORD</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required 
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none" />
          </div>
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-xl transition cursor-pointer">
            Daftar Sekarang
          </button>
        </form>
        <p className="text-center text-sm text-slate-400 mt-6">
          Sudah punya akun? <Link href="/login" className="text-indigo-400 hover:text-indigo-300">Login</Link>
        </p>
      </div>
    </div>
  );
}