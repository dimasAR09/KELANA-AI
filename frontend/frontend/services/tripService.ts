const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const getToken = () => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    return token ? token.trim() : '';
  }
  return '';
};

export async function registerUser(data: { name?: string; email: string; password: string }) {
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
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');

  const response = await fetch(`${API_BASE_URL}/trips`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
    },
  });

  if (!response.ok) {
    throw new Error('Gagal memuat data perjalanan');
  }

  return response.json();
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

export async function createTrip(data: { destination: string; days: number; budget: number; travel_style: string }) {
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

export async function askAssistant(question: string) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/assistant`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  });
  
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Gagal terhubung ke Asisten AI');
  }
  return res.json();
}

// ─── Conversation Memory API (Session 10) ────────────────────────────────────

/**
 * POST /api/v1/conversations
 * Buat conversation baru, kembalikan { conversation_id, title, created_at }
 */
export async function createConversation(title?: string) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/conversations`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title: title ?? null }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail || 'Gagal membuat conversation');
  }
  return res.json() as Promise<{ conversation_id: number; title: string | null; created_at: string }>;
}

/**
 * GET /api/v1/conversations
 * Daftar semua conversation milik user yang sedang login.
 */
export async function listConversations() {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/conversations`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Gagal memuat daftar conversation');
  return res.json();
}

/**
 * GET /api/v1/conversations/{id}
 * Ambil detail conversation beserta semua messages-nya.
 */
export async function getConversation(conversationId: number) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Gagal memuat conversation');
  return res.json();
}

/**
 * POST /api/v1/conversations/{id}/messages
 * Kirim pesan ke conversation, terima AI response.
 */
export async function sendMessage(conversationId: number, content: string) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail || 'Gagal mengirim pesan');
  }
  return res.json();
}

/**
 * PATCH /api/v1/conversations/{id}
 * Challenge: rename conversation title.
 */
export async function renameConversation(conversationId: number, title: string) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail || 'Gagal mengganti nama conversation');
  }
  return res.json();
}

/**
 * DELETE /api/v1/conversations/{id}
 * Hapus conversation beserta semua messages-nya.
 */
export async function deleteConversation(conversationId: number) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Gagal menghapus conversation');
  // 204 No Content — tidak ada body
  return true;
}
