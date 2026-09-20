export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: {
    code: string;
    message: string;
    details?: any[];
  } | null;
  timestamp: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'user' | 'recruiter' | 'admin';
  is_active: boolean;
  created_at: string;
}

export interface SystemHealth {
  status: string;
  service: string;
  version: string;
}
