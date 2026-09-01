'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { loginUser } from '@/services/tripService';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const data = await loginUser({
        email: email.trim(),
        password: password
      });
      
      console.log("Respon Login dari Backend:", data);
      
      const tokenToSave = data.access_token || data.token;
      
      if (tokenToSave) {
        localStorage.setItem('token', tokenToSave);
      } else {
        alert("Token tidak ditemukan di respon server!");
        return;
      }
      
      router.push('/trips');
      
    } catch (error: unknown) {
      setError(error instanceof Error ? error.message : 'Login gagal');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-2 text-center">Selamat Datang Kembali</h2>
        <p className="text-slate-400 text-sm text-center mb-6">Login untuk melanjutkan ke KelanaAI</p>
        
        {error && <div className="bg-red-500/10 text-red-400 p-3 rounded-lg text-sm mb-4">{error}</div>}
        
        <form onSubmit={handleLogin} className="space-y-4">
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
            Login
          </button>
        </form>
        <p className="text-center text-sm text-slate-400 mt-6">
          Belum punya akun? <Link href="/register" className="text-indigo-400 hover:text-indigo-300">Daftar</Link>
        </p>
      </div>
    </div>
  );
}