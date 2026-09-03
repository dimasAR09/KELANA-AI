export interface User {
  id: number;
  name: string;
  email: string;
}

export interface TripRequest {
  destination: string;
  days: number;
  budget: number;
  travel_style: string;
}

export interface Trip {
  id: number;
  destination: string;
  days: number;
  budget: number;
  category: string;
  daily_budget: number;
  travel_style?: string;
  recommended_transport?: string;
  ai_recommendation?: string;
  user_id?: number;
  created_at?: string;
}

export type SortOption = 'latest' | 'oldest' | 'highest_budget';

// ─── Conversation Memory (Session 10) ────────────────────────────────────────

export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface Conversation {
  id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  messages: Message[];
}

export interface ConversationSummary {
  id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  messages: Message[];
}
