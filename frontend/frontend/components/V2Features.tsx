'use client';

import React, { useState } from 'react';
import { shareTripEmail, generateAiImage } from '../services/tripService'; 

export function EmailShareButton({ tripId }: { tripId: number }) {
  const [status, setStatus] = useState('');

  const handleShare = async () => {
    setStatus('Mengirim...');
    try {
      await shareTripEmail(tripId);
      setStatus('✅ Terkirim ke Email Anda!');
      setTimeout(() => setStatus(''), 3000);
    } catch (error) {
      console.error(error);
      setStatus('❌ Gagal Mengirim');
    }
  };

  return (
    <div className="mt-4">
      <button 
        onClick={handleShare} 
        className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-white font-bold text-sm transition shadow-lg"
      >
        {status || '📧 Kirim Itinerary ke Email Saya'}
      </button>
    </div>
  );
}

export function AiImageGeneratorBox() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const data = await generateAiImage(prompt);
      setImageUrl(data.image_url);
    } catch (err) {
      console.error(err);
      alert('Gagal membuat gambar dari Bedrock.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mt-6 space-y-4">
      <h3 className="text-lg font-bold text-white">🎨 AI Destination Image Generator (AWS Bedrock)</h3>
      <div className="flex gap-2">
        <input 
          type="text"
          value={prompt}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPrompt(e.target.value)}
          placeholder="Contoh: Luxury resort in Bali sunset..."
          className="flex-1 px-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-white text-sm outline-none focus:border-indigo-500"
        />
        <button 
          onClick={handleGenerate}
          disabled={loading}
          className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl text-sm transition disabled:opacity-50"
        >
          {loading ? '⏳ Generating...' : 'Generate'}
        </button>
      </div>
      {imageUrl && (
        <div className="mt-4 flex justify-center bg-slate-950 p-4 rounded-xl border border-slate-800">
          <img src={imageUrl} alt="Generated AI" className="rounded-lg max-h-80 object-contain shadow-lg" />
        </div>
      )}
    </div>
  );
}

export function VoiceAssistantButton({ onTextResult }: { onTextResult: (text: string) => void }) {
  const [isListening, setIsListening] = useState(false);

  const startListening = () => {
    // @ts-ignore
    const SpeechRecognitionWindow = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionWindow) {
      alert("Browser tidak mendukung Voice AI.");
      return;
    }
    
    const recognition = new SpeechRecognitionWindow();
    recognition.lang = 'id-ID';
    recognition.onstart = () => setIsListening(true);
    // @ts-ignore
    recognition.onresult = (event: any) => {
      onTextResult(event.results[0][0].transcript);
      setIsListening(false);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  return (
    <button 
      type="button" 
      onClick={startListening} 
      className={`p-3 rounded-full shadow-lg transition flex items-center justify-center h-12 w-12 ${isListening ? 'bg-red-500 animate-pulse' : 'bg-indigo-600 hover:bg-indigo-500'} text-white`}
      title="Bicara sekarang"
    >
      {isListening ? '🎙️' : '🎤'}
    </button>
  );
}