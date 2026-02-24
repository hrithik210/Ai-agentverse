const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

export class ApiClient {
  private static getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  private static async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const url = `${API_BASE_URL}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    console.log('API Request:', { url, method: options.method || 'GET', headers, body: options.body });

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      console.log('API Response:', { status: response.status, statusText: response.statusText });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.log('API Error Data:', errorData);
        throw new APIError(response.status, errorData.detail || 'An error occurred');
      }

      const data = await response.json();
      console.log('API Success Data:', data);
      return data;
    } catch (error) {
      console.error('API Request Failed:', error);
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(500, 'Network error occurred');
    }
  }

  // Auth methods
  static async login(email: string, password: string) {
    return this.request('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  static async register(username: string, email: string, password: string) {
    return this.request('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  // User stats
  static async getUserStats() {
    return this.request('/stats');
  }

  // Daily report
  static async getDailyReport() {
    return this.request('/daily-report');
  }

  // Mood logging
  static async logMood(moodData: any) {
    return this.request('/mood', {
      method: 'POST',
      body: JSON.stringify(moodData),
    });
  }

  // Health logging
  static async logMeal(mealData: any) {
    return this.request('/health/meal', {
      method: 'POST',
      body: JSON.stringify(mealData),
    });
  }

  static async logExercise(exerciseData: any) {
    return this.request('/health/exercise', {
      method: 'POST',
      body: JSON.stringify(exerciseData),
    });
  }

  static async logSleep(sleepData: any) {
    return this.request('/health/sleep', {
      method: 'POST',
      body: JSON.stringify(sleepData),
    });
  }

  static async logWater(waterData: any) {
    return this.request('/health/water', {
      method: 'POST',
      body: JSON.stringify(waterData),
    });
  }

  // Code activity
  static async getCodeActivity() {
    return this.request('/get-code-activity');
  }

  static async createCodeActivity() {
    return this.request('/create-code-activity', {
      method: 'POST',
    });
  }
}

export { APIError };
