const getApiBase = () => {
  const envUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!envUrl) return 'https://ai-resume-screener-26ke.onrender.com/api/v1';
  const cleanUrl = envUrl.replace(/\/$/, '');
  return cleanUrl.endsWith('/api/v1') ? cleanUrl : `${cleanUrl}/api/v1`;
};

const API_BASE = getApiBase();

let cachedToken: string | null = null;

export function getSavedToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('agentx_token');
  }
  return null;
}

export function getSavedUser(): any | null {
  if (typeof window !== 'undefined') {
    const u = localStorage.getItem('agentx_user');
    if (u) {
      try { return JSON.parse(u); } catch (e) {}
    }
  }
  return null;
}

export function saveAuthSession(token: string, user: any) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('agentx_token', token);
    localStorage.setItem('agentx_user', JSON.stringify(user));
    cachedToken = token;
  }
}

export function clearAuthSession() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('agentx_token');
    localStorage.removeItem('agentx_user');
    cachedToken = null;
  }
}

export async function loginUser(email: string, pass: string) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password: pass }),
  });

  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    const errorMsg = json?.error?.message || json?.detail || 'Invalid email or password';
    throw new Error(errorMsg);
  }

  const token = json?.data?.tokens?.access_token;
  const user = json?.data?.user;
  if (token) {
    saveAuthSession(token, user);
  }
  return { token, user };
}

export async function registerUser(email: string, pass: string, fullName: string) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password: pass, full_name: fullName }),
  });

  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    const errorMsg = json?.error?.message || json?.detail || 'Registration failed';
    throw new Error(errorMsg);
  }

  const token = json?.data?.tokens?.access_token;
  const user = json?.data?.user;
  if (token) {
    saveAuthSession(token, user);
  }
  return { token, user };
}

export async function getAuthToken(): Promise<string> {
  const savedToken = getSavedToken();
  if (savedToken) {
    cachedToken = savedToken;
    return savedToken;
  }
  if (cachedToken) return cachedToken;

  const guestEmail = 'guest_demo@agentx.ai';
  const guestPass = 'GuestPassword123!';

  // 1. Try registering guest account first
  try {
    const regRes = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: guestEmail,
        password: guestPass,
        full_name: 'Guest Demo User',
      }),
    });

    if (regRes.ok) {
      const data = await regRes.json();
      if (data?.data?.tokens?.access_token) {
        cachedToken = data.data.tokens.access_token;
        return cachedToken!;
      }
    }
  } catch (e) {
    // Ignore if already registered
  }

  // 2. Fallback to login
  try {
    const loginRes = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: guestEmail,
        password: guestPass,
      }),
    });

    if (loginRes.ok) {
      const data = await loginRes.json();
      if (data?.data?.tokens?.access_token) {
        cachedToken = data.data.tokens.access_token;
        return cachedToken!;
      }
    }
  } catch (e) {
    console.error('Login error:', e);
  }

  throw new Error('Failed to establish authenticated session with backend API');
}

export async function uploadResumeFile(file: File) {
  const token = await getAuthToken();
  const formData = new FormData();
  formData.append('file', file);
  formData.append('title', file.name);

  const res = await fetch(`${API_BASE}/resumes/upload`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to upload resume file');
  }

  const json = await res.json();
  const resumeObj = json.data?.resume || json.data;
  return resumeObj; // returns object containing .id
}

export async function parseResume(resumeId: string) {
  const token = await getAuthToken();
  const res = await fetch(`${API_BASE}/resumes/${resumeId}/parse`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to parse resume');
  }
  const json = await res.json();
  return json.data;
}

export async function runATSAnalysis(resumeId: string) {
  const token = await getAuthToken();
  const res = await fetch(`${API_BASE}/analysis/ats/${resumeId}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to analyze resume ATS compatibility');
  }
  const json = await res.json();
  return json.data; // returns { resume_id, ats_analysis }
}

export async function createJobDescription(title: string, company: string, rawText: string) {
  const token = await getAuthToken();
  const res = await fetch(`${API_BASE}/jobs`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title: title || 'Target Position',
      company_name: company || 'Target Company',
      raw_text: rawText || title || 'Position details',
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to create job description');
  }
  const json = await res.json();
  return json.data.job; // returns { id, title, company_name, raw_text, parsed_jd }
}

export async function matchJobAndResume(jobId: string, resumeId: string) {
  const token = await getAuthToken();
  const res = await fetch(`${API_BASE}/jobs/${jobId}/match/${resumeId}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to match job and resume');
  }
  const json = await res.json();
  return json.data; // returns { job_id, resume_id, match_result }
}

export async function generateCareerInsights(resumeId: string, targetRole?: string) {
  const token = await getAuthToken();
  const url = targetRole
    ? `${API_BASE}/career/insights/${resumeId}?target_role=${encodeURIComponent(targetRole)}`
    : `${API_BASE}/career/insights/${resumeId}`;

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to generate career insights');
  }
  const json = await res.json();
  return json.data; // returns { resume_id, career_insights }
}

export async function generateInterviewQuestions(resumeId: string) {
  const token = await getAuthToken();
  const res = await fetch(`${API_BASE}/interview/questions/${resumeId}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to generate interview questions');
  }
  const json = await res.json();
  return json.data; // returns { resume_id, questions }
}

export async function orchestrateAgents(goal: string, resumeId: string, jobId?: string) {
  const token = await getAuthToken();
  const res = await fetch(`${API_BASE}/agents/orchestrate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      user_goal: goal || 'Analyze candidate credentials against job requirements.',
      resume_id: resumeId,
      job_id: jobId,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || err?.detail || 'Failed to orchestrate multi-agent workflow');
  }
  const json = await res.json();
  return json.data; // returns { session_id, action_plan, execution_trace }
}
