const API_BASE_URL = 'http://localhost:8000/api/v1';

const getToken = () => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    return token ? token.trim() : '';
  }
  return '';
};

export async function registerUser(data: any) {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Gagal mendaftar');
  }
  return res.json();
}

export async function loginUser(data: { email: string; password: string }) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Gagal login');
  }
  return res.json();
}

export async function getMe() {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/auth/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) throw new Error('Gagal memuat profil');
  return res.json();
}

export async function getTrips() {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/trips`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) {
    throw new Error('Gagal mengambil data trips. Silakan login kembali.');
  }
  return res.json();
}

export async function getTrip(id: string) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/trips/${id}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) throw new Error('Gagal mengambil detail trip');
  return res.json();
}

export async function createTrip(data: any) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/trips`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Gagal membuat trip');
  }
  return res.json();
}

export async function deleteTrip(id: number) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/trips/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!res.ok) throw new Error('Gagal menghapus trip');
  return res.json();
}