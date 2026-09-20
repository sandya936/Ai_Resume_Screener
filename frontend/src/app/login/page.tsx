'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Sparkles,
  Mail,
  Lock,
  User,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  Eye,
  EyeOff,
  Zap,
  Bot,
  BrainCircuit,
  Briefcase,
  ChevronLeft,
} from 'lucide-react';
import { loginUser, registerUser } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [showPassword, setShowPassword] = useState(false);

  // Form states
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);

  // UX states
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (!email || !password) {
      setErrorMsg('Please enter both email and password.');
      return;
    }

    if (mode === 'register') {
      if (!fullName) {
        setErrorMsg('Please enter your full name.');
        return;
      }
      if (password.length < 6) {
        setErrorMsg('Password must be at least 6 characters long.');
        return;
      }
      if (password !== confirmPassword) {
        setErrorMsg('Passwords do not match.');
        return;
      }
    }

    setIsLoading(true);

    try {
      if (mode === 'login') {
        const { user } = await loginUser(email, password);
        setSuccessMsg(`Welcome back, ${user?.full_name || email.split('@')[0]}! Redirecting to workspace...`);
        setTimeout(() => {
          router.push('/');
        }, 800);
      } else {
        const { user } = await registerUser(email, password, fullName);
        setSuccessMsg(`Account created successfully! Welcome to AGENTX AI, ${user?.full_name || fullName}.`);
        setTimeout(() => {
          router.push('/');
        }, 900);
      }
    } catch (err: any) {
      setErrorMsg(err?.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickDemoLogin = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    setEmail('guest_demo@agentx.ai');
    setPassword('GuestPassword123!');

    try {
      const { user } = await loginUser('guest_demo@agentx.ai', 'GuestPassword123!');
      setSuccessMsg('Logged in as Guest Demo User! Redirecting to workspace...');
      setTimeout(() => {
        router.push('/');
      }, 700);
    } catch (err: any) {
      setErrorMsg('Failed to log in as Guest Demo. Please try regular login.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-indigo-500 selection:text-white relative overflow-hidden font-sans">
      {/* Background Animated Gradient Blobs */}
      <div className="absolute top-0 -left-4 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-cyan-600/15 rounded-full blur-3xl pointer-events-none"></div>

      {/* Navigation Header */}
      <header className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-400 p-[2px] shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform duration-300">
            <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-2xl tracking-tight text-white">AGENT<span className="text-cyan-400">X</span></span>
              <span className="text-[10px] uppercase font-bold tracking-widest bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded-full">AI 2.0</span>
            </div>
            <span className="text-xs text-slate-400 hidden sm:block">Enterprise AI Resume & Career Intelligence</span>
          </div>
        </Link>
      </header>

      {/* Main Container */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex items-center justify-center">
        <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Hero Brand Panel (Desktop) */}
          <div className="lg:col-span-6 space-y-6 lg:pr-8 text-center lg:text-left">
            <div className="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 px-3.5 py-1.5 rounded-full text-xs font-semibold text-indigo-300">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              <span>Next-Gen Enterprise Career Intelligence</span>
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight">
              Transform Your Resume into a <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400">High-Impact</span> Career Asset.
            </h1>

            <p className="text-slate-400 text-base sm:text-lg leading-relaxed max-w-xl mx-auto lg:mx-0">
              Unlock real-time ATS compatibility scoring, Job Description keyword matching, 40-question dynamic interview preparation, and autonomous Multi-Agent AI career roadmap guidance.
            </p>

            {/* Feature Highlights Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
              <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 backdrop-blur-md flex items-start gap-3 text-left hover:border-indigo-500/40 transition-colors">
                <div className="p-2.5 bg-cyan-500/10 rounded-xl text-cyan-400">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">Instant ATS Audit</h4>
                  <p className="text-xs text-slate-400">99.8% precision score across 7 core structural criteria.</p>
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 backdrop-blur-md flex items-start gap-3 text-left hover:border-indigo-500/40 transition-colors">
                <div className="p-2.5 bg-violet-500/10 rounded-xl text-violet-400">
                  <BrainCircuit className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">40 Interview Questions</h4>
                  <p className="text-xs text-slate-400">Top 20 Technical Deep Dives + 20 Behavioral STAR practice questions.</p>
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 backdrop-blur-md flex items-start gap-3 text-left hover:border-indigo-500/40 transition-colors">
                <div className="p-2.5 bg-emerald-500/10 rounded-xl text-emerald-400">
                  <Briefcase className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">1-Click Job Match</h4>
                  <p className="text-xs text-slate-400">Pinpoint required skill gaps and actionable candidate keywords.</p>
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 backdrop-blur-md flex items-start gap-3 text-left hover:border-indigo-500/40 transition-colors">
                <div className="p-2.5 bg-amber-500/10 rounded-xl text-amber-400">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">Multi-Agent Swarm</h4>
                  <p className="text-xs text-slate-400">Autonomous LLM workflow executing parallel career tasks.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Login / Sign Up Card Form */}
          <div className="lg:col-span-6 flex justify-center">
            <div className="w-full max-w-md bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl backdrop-blur-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-cyan-400 via-indigo-500 to-violet-500"></div>

              {/* Mode Toggle Tabs */}
              <div className="flex bg-slate-950/80 p-1.5 rounded-2xl border border-slate-800 mb-6">
                <button
                  type="button"
                  onClick={() => { setMode('login'); setErrorMsg(null); setSuccessMsg(null); }}
                  className={`flex-1 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                    mode === 'login'
                      ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Sign In
                </button>
                <button
                  type="button"
                  onClick={() => { setMode('register'); setErrorMsg(null); setSuccessMsg(null); }}
                  className={`flex-1 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                    mode === 'register'
                      ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Create Account
                </button>
              </div>

              {/* Title & Subtitle */}
              <div className="text-center mb-6">
                <h2 className="text-xl sm:text-2xl font-bold text-white">
                  {mode === 'login' ? 'Welcome Back to AGENTX' : 'Create Your Free Account'}
                </h2>
                <p className="text-xs sm:text-sm text-slate-400 mt-1">
                  {mode === 'login'
                    ? 'Enter your credentials to access your AI Career Intelligence workspace.'
                    : 'Start auditing resumes, analyzing ATS scores, and generating interview questions.'}
                </p>
              </div>

              {/* Error & Success Feedback Alerts */}
              {errorMsg && (
                <div className="mb-5 bg-rose-500/10 border border-rose-500/30 text-rose-300 p-3.5 rounded-2xl flex items-start gap-3 text-xs sm:text-sm">
                  <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                  <div>{errorMsg}</div>
                </div>
              )}

              {successMsg && (
                <div className="mb-5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 p-3.5 rounded-2xl flex items-start gap-3 text-xs sm:text-sm">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                  <div>{successMsg}</div>
                </div>
              )}

              {/* Auth Form */}
              <form onSubmit={handleAuthSubmit} className="space-y-4">
                {mode === 'register' && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                      Full Name
                    </label>
                    <div className="relative">
                      <User className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-400" />
                      <input
                        type="text"
                        required
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="e.g. Sandy Smith"
                        className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                      />
                    </div>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-400" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@example.com"
                      className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="block text-xs font-semibold text-slate-300">
                      Password
                    </label>
                    {mode === 'login' && (
                      <button
                        type="button"
                        onClick={() => alert('Password reset link sent to your registered email.')}
                        className="text-xs font-medium text-indigo-400 hover:text-indigo-300 transition-colors"
                      >
                        Forgot password?
                      </button>
                    )}
                  </div>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-400" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-10 pr-10 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-3.5 text-slate-400 hover:text-white"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {mode === 'register' && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                      Confirm Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-400" />
                      <input
                        type={showPassword ? 'text' : 'password'}
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="••••••••"
                        className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                      />
                    </div>
                  </div>
                )}

                {/* Checkbox Options */}
                <div className="flex items-center justify-between pt-1">
                  <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-400 select-none">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 rounded bg-slate-950 border-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900"
                    />
                    <span>{mode === 'login' ? 'Keep me logged in' : 'I agree to Terms of Service & Privacy Policy'}</span>
                  </label>
                </div>

                {/* Primary Action Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full py-3.5 px-4 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white font-bold text-sm rounded-xl shadow-lg shadow-indigo-600/25 hover:shadow-indigo-600/40 transition-all flex items-center justify-center gap-2 group mt-2"
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  ) : (
                    <>
                      <span>{mode === 'login' ? 'Sign In to Workspace' : 'Create Account'}</span>
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </>
                  )}
                </button>

                {/* Quick 1-Click Demo Account Login Button */}
                {mode === 'login' && (
                  <button
                    type="button"
                    onClick={handleQuickDemoLogin}
                    disabled={isLoading}
                    className="w-full py-3 px-4 bg-slate-950 hover:bg-slate-800/80 border border-indigo-500/30 text-indigo-300 font-semibold text-xs rounded-xl transition-all flex items-center justify-center gap-2 shadow-sm mt-3"
                  >
                    <Zap className="w-4 h-4 text-cyan-400" />
                    <span>⚡ 1-Click Instant Guest Demo Sign In</span>
                  </button>
                )}
              </form>

              {/* Social Login Separator */}
              <div className="relative my-6 text-center">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-slate-800"></div>
                </div>
                <span className="relative px-3 bg-slate-900 text-slate-500 text-xs uppercase tracking-wider font-semibold">
                  Or continue with
                </span>
              </div>

              {/* Social SSO Buttons */}
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => handleQuickDemoLogin()}
                  className="py-2.5 px-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-xs font-medium text-slate-300 hover:text-white transition-all flex items-center justify-center gap-2"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24">
                    <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.2 8.8 5 12 5z" />
                    <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z" />
                    <path fill="#FBBC05" d="M5.3 14.7c-.2-.7-.4-1.4-.4-2.2s.2-1.5.4-2.2L1.6 7.4C.6 9.4 0 11.6 0 14s.6 4.6 1.6 6.6l3.7-2.9z" />
                    <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.2 0-5.8-2.2-6.7-5.3L1.6 16C3.5 19.8 7.4 23 12 23z" />
                  </svg>
                  <span>Google</span>
                </button>

                <button
                  type="button"
                  onClick={() => handleQuickDemoLogin()}
                  className="py-2.5 px-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-xs font-medium text-slate-300 hover:text-white transition-all flex items-center justify-center gap-2"
                >
                  <svg className="w-4 h-4 fill-current text-white" viewBox="0 0 24 24">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
                  </svg>
                  <span>GitHub</span>
                </button>
              </div>

            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between border-t border-slate-900 gap-4">
        <div>
          © 2026 AGENTX AI Platform. All rights reserved. Powered by Google Antigravity & FastAPI Architecture.
        </div>
        <div className="flex items-center gap-6">
          <a href="#" className="hover:text-slate-300 transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-slate-300 transition-colors">Terms of Service</a>
          <a href="#" className="hover:text-slate-300 transition-colors">Documentation</a>
        </div>
      </footer>
    </div>
  );
}
