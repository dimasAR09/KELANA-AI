import { Trip } from '@/types';

// Pastikan Base URL berhenti di port 8000 ATAU sudah mencakup /api/v1
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function getTrips(): Promise<Trip[]> {
  // Cukup panggil '/trips' (JANGAN panggil '/api/v1/trips' lagi)
  const response = await fetch(`${API_BASE_URL}/trips`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    cache: 'no-store', // Mencegah caching data lama di Next.js
  });

  if (!response.ok) {
    throw new Error(`Gagal mengambil data trips: ${response.statusText}`);
  }

  return response.json();
}

export async function deleteTrip(id: number): Promise<void> {
  // Gunakan /trips/${id}
  const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error(`Gagal menghapus trip #${id}`);
  }
}

export async function getTrip(id: string | number): Promise<Trip> {
  const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`Gagal mengambil detail trip #${id}: ${response.statusText}`);
  }

  return response.json();
}