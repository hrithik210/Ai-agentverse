// API Types
export interface User {
  id: string;
  username: string;
  email: string;
}

export interface AuthResponse {
  message: string;
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface UserStats {
  current_level: number;
  total_xp: number;
  todays_xp: number;
  xp_breakdown: Record<string, number>;
}

export interface MoodLog {
  id: string;
  mood_rating: number;
  energy_level: number;
  stress_level: number;
  notes?: string;
  date: string;
}

export interface HealthLog {
  id: string;
  type: 'meal' | 'exercise' | 'sleep' | 'water';
  value: number;
  notes?: string;
  date: string;
}

export interface CodeLog {
  id: string;
  lines_added: number;
  lines_removed: number;
  total_time_minutes: number;
  date: string;
  processed: boolean;
}

export interface DailyReport {
  report: string;
}
