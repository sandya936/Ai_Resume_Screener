'use client';

import React, { useState, useEffect } from 'react';
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
  Moon,
  Sun,
  Palette,
} from 'lucide-react';
import { loginUser, registerUser } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [showPassword, setShowPassword] = useState(false);
  const [theme, setTheme] = useState<'parchment' | 'dark'>('parchment');

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

  useEffect(() => {
    const savedTheme = localStorage.getItem('agentx_theme') as 'parchment' | 'dark' | null;
    if (savedTheme === 'dark' || savedTheme === 'parchment') {
      setTheme(savedTheme);
      document.body.className = `theme-${savedTheme}`;
    } else {
      document.body.className = 'theme-parchment';
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === 'parchment' ? 'dark' : 'parchment';
    setTheme(nextTheme);
    localStorage.setItem('agentx_theme', nextTheme);
    document.body.className = `theme-${nextTheme}`;
  };

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

  const isDark = theme === 'dark';

  return (
    <div className={`min-h-screen flex flex-col justify-between relative overflow-hidden font-sans ${
      isDark ? 'bg-[#030712] text-slate-100 selection:bg-indigo-500' : 'bg-[#ebdcc6] text-[#241810] selection:bg-[#8b1e16]'
    } selection:text-white`}>
      {/* Background Glows */}
      {isDark ? (
        <>
          <div className="absolute top-0 -left-4 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none animate-pulse" />
          <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-cyan-600/15 rounded-full blur-3xl pointer-events-none" />
        </>
      ) : (
        <>
          <div className="absolute top-0 -left-4 w-96 h-96 bg-[#f5dcd8]/50 rounded-full blur-3xl pointer-events-none animate-pulse" />
          <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-[#dfcfb9]/60 rounded-full blur-3xl pointer-events-none" />
        </>
      )}

      {/* Navigation Header */}
      <header className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className={`w-11 h-11 rounded-2xl p-[2px] shadow-md group-hover:scale-105 transition-transform duration-300 ${
            isDark
              ? 'bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-400 shadow-indigo-500/25'
              : 'bg-gradient-to-br from-[#8b1e16] via-[#d4af37] to-[#8c7355] shadow-red-950/20'
          }`}>
            <div className={`w-full h-full rounded-[14px] flex items-center justify-center ${
              isDark ? 'bg-slate-950' : 'bg-[#f5ece0]'
            }`}>
              <Bot className={`w-6 h-6 ${isDark ? 'text-cyan-400' : 'text-[#8b1e16]'}`} />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className={`font-extrabold text-2xl tracking-tight ${isDark ? 'text-white' : 'text-[#241810]'}`}>
                AGENT<span className={isDark ? 'text-cyan-400' : 'text-[#8b1e16]'}>X</span>
              </span>
              <span className={`text-[10px] uppercase font-extrabold tracking-widest px-2 py-0.5 rounded-full shadow-sm ${
                isDark
                  ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                  : 'bg-[#dfcfb9] text-[#4e3d30] border border-[#c5b196]'
              }`}>
                AI 2.0
              </span>
            </div>
            <span className={`text-xs font-semibold hidden sm:block ${isDark ? 'text-slate-400' : 'text-[#6e5845]'}`}>
              Enterprise AI Resume & Career Intelligence
            </span>
          </div>
        </Link>

        {/* Theme Toggle Button */}
        <button
          onClick={toggleTheme}
          type="button"
          className={`px-3.5 py-2 rounded-xl text-xs font-extrabold flex items-center gap-2 border shadow-sm transition-all cursor-pointer ${
            isDark
              ? 'bg-slate-900 hover:bg-slate-800 text-cyan-300 border-slate-700'
              : 'bg-[#dfcfb9] hover:bg-[#d4c3ab] text-[#4e3d30] border-[#c5b196]'
          }`}
        >
          {isDark ? (
            <>
              <Moon className="w-4 h-4 text-cyan-400" />
              <span>🌙 Dark Slate UI</span>
            </>
          ) : (
            <>
              <Sun className="w-4 h-4 text-[#8b1e16]" />
              <span>📜 Warm Crimson Theme</span>
            </>
          )}
        </button>
      </header>

      {/* Main Container */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex items-center justify-center">
        <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Hero Brand Panel (Desktop) */}
          <div className="lg:col-span-6 space-y-6 lg:pr-8 text-center lg:text-left">
            <div className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-bold shadow-sm ${
              isDark
                ? 'bg-indigo-500/10 border border-indigo-500/20 text-indigo-300'
                : 'bg-[#dfcfb9] border border-[#c5b196] text-[#4e3d30]'
            }`}>
              <ShieldCheck className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-[#8b1e16]'}`} />
              <span>Next-Gen Enterprise Career Intelligence</span>
            </div>

            <h1 className={`text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight ${
              isDark ? 'text-white' : 'text-[#241810]'
            }`}>
              Transform Your Resume into a{' '}
              <span className={`text-transparent bg-clip-text ${
                isDark
                  ? 'bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400'
                  : 'bg-gradient-to-r from-[#8b1e16] via-[#a3241b] to-[#8c7355]'
              }`}>
                High-Impact
              </span>{' '}
              Career Asset.
            </h1>

            <p className={`text-base sm:text-lg leading-relaxed max-w-xl mx-auto lg:mx-0 font-medium ${
              isDark ? 'text-slate-400' : 'text-[#6e5845]'
            }`}>
              Unlock real-time ATS compatibility scoring, Job Description keyword matching, 40-question dynamic interview preparation, and autonomous Multi-Agent AI career roadmap guidance.
            </p>

            {/* Feature Highlights Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
              <div className={`rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left transition-colors ${
                isDark
                  ? 'bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40'
                  : 'bg-[#ede2d2] border border-[#caba9c] hover:border-[#8b1e16]'
              }`}>
                <div className={`p-2.5 rounded-xl ${isDark ? 'bg-cyan-500/10 text-cyan-400' : 'bg-[#f5dcd8] text-[#8b1e16]'}`}>
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <h4 className={`text-sm font-extrabold ${isDark ? 'text-white' : 'text-[#241810]'}`}>Instant ATS Audit</h4>
                  <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-[#6e5845]'}`}>
                    99.8% precision score across 7 core structural criteria.
                  </p>
                </div>
              </div>

              <div className={`rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left transition-colors ${
                isDark
                  ? 'bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40'
                  : 'bg-[#ede2d2] border border-[#caba9c] hover:border-[#8b1e16]'
              }`}>
                <div className={`p-2.5 rounded-xl ${isDark ? 'bg-violet-500/10 text-violet-400' : 'bg-[#dfcfb9] text-[#4e3d30]'}`}>
                  <BrainCircuit className="w-5 h-5" />
                </div>
                <div>
                  <h4 className={`text-sm font-extrabold ${isDark ? 'text-white' : 'text-[#241810]'}`}>40 Interview Questions</h4>
                  <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-[#6e5845]'}`}>
                    Top 20 Technical Deep Dives + 20 Behavioral STAR practice questions.
                  </p>
                </div>
              </div>

              <div className={`rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left transition-colors ${
                isDark
                  ? 'bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40'
                  : 'bg-[#ede2d2] border border-[#caba9c] hover:border-[#8b1e16]'
              }`}>
                <div className={`p-2.5 rounded-xl ${isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-[#dcecd8] text-[#1c5427]'}`}>
                  <Briefcase className="w-5 h-5" />
                </div>
                <div>
                  <h4 className={`text-sm font-extrabold ${isDark ? 'text-white' : 'text-[#241810]'}`}>1-Click Job Match</h4>
                  <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-[#6e5845]'}`}>
                    Pinpoint required skill gaps and actionable candidate keywords.
                  </p>
                </div>
              </div>

              <div className={`rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left transition-colors ${
                isDark
                  ? 'bg-slate-900/60 border border-slate-800 hover:border-indigo-500/40'
                  : 'bg-[#ede2d2] border border-[#caba9c] hover:border-[#8b1e16]'
              }`}>
                <div className={`p-2.5 rounded-xl ${isDark ? 'bg-amber-500/10 text-amber-400' : 'bg-[#f5dcd8] text-[#8b1e16]'}`}>
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h4 className={`text-sm font-extrabold ${isDark ? 'text-white' : 'text-[#241810]'}`}>Multi-Agent Swarm</h4>
                  <p className={`text-xs font-medium ${isDark ? 'text-slate-400' : 'text-[#6e5845]'}`}>
                    Autonomous LLM workflow executing parallel career tasks.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Login / Sign Up Card Form */}
          <div className="lg:col-span-6 flex justify-center">
            <div className={`w-full max-w-md rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden ${
              isDark
                ? 'bg-slate-900/90 border border-slate-800'
                : 'bg-[#f5ece0] border border-[#caba9c]'
            }`}>
              <div className={`absolute top-0 left-0 right-0 h-1.5 ${
                isDark
                  ? 'bg-gradient-to-r from-cyan-400 via-indigo-500 to-violet-500'
                  : 'bg-gradient-to-r from-[#8b1e16] via-[#d4af37] to-[#8c7355]'
              }`} />

              {/* Mode Toggle Tabs */}
              <div className={`flex p-1.5 rounded-2xl border mb-6 shadow-inner ${
                isDark ? 'bg-slate-950/80 border-slate-800' : 'bg-[#dfcfb9] border-[#c5b196]'
              }`}>
                <button
                  type="button"
                  onClick={() => { setMode('login'); setErrorMsg(null); setSuccessMsg(null); }}
                  className={`flex-1 py-2.5 text-xs sm:text-sm font-extrabold rounded-xl transition-all cursor-pointer ${
                    mode === 'login'
                      ? isDark
                        ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md'
                        : 'bg-[#8b1e16] text-white shadow-md'
                      : isDark
                        ? 'text-slate-400 hover:text-white'
                        : 'text-[#4e3d30] hover:text-[#241810]'
                  }`}
                >
                  Sign In
                </button>
                <button
                  type="button"
                  onClick={() => { setMode('register'); setErrorMsg(null); setSuccessMsg(null); }}
                  className={`flex-1 py-2.5 text-xs sm:text-sm font-extrabold rounded-xl transition-all cursor-pointer ${
                    mode === 'register'
                      ? isDark
                        ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md'
                        : 'bg-[#8b1e16] text-white shadow-md'
                      : isDark
                        ? 'text-slate-400 hover:text-white'
                        : 'text-[#4e3d30] hover:text-[#241810]'
                  }`}
                >
                  Create Account
                </button>
              </div>

              {/* Title & Subtitle */}
              <div className="text-center mb-6">
                <h2 className={`text-xl sm:text-2xl font-extrabold ${isDark ? 'text-white' : 'text-[#241810]'}`}>
                  {mode === 'login' ? 'Welcome Back to AGENTX' : 'Create Your Free Account'}
                </h2>
                <p className={`text-xs sm:text-sm mt-1 font-medium ${isDark ? 'text-slate-400' : 'text-[#6e5845]'}`}>
                  {mode === 'login'
                    ? 'Enter your credentials to access your AI Career Intelligence workspace.'
                    : 'Start auditing resumes, analyzing ATS scores, and generating interview questions.'}
                </p>
              </div>

              {/* Error & Success Feedback Alerts */}
              {errorMsg && (
                <div className={`mb-5 p-3.5 rounded-2xl flex items-start gap-3 text-xs sm:text-sm font-semibold ${
                  isDark
                    ? 'bg-rose-500/10 border border-rose-500/30 text-rose-300'
                    : 'bg-red-100 border border-red-300 text-red-900'
                }`}>
                  <AlertCircle className={`w-5 h-5 shrink-0 mt-0.5 ${isDark ? 'text-rose-400' : 'text-red-700'}`} />
                  <div>{errorMsg}</div>
                </div>
              )}

              {successMsg && (
                <div className={`mb-5 p-3.5 rounded-2xl flex items-start gap-3 text-xs sm:text-sm font-extrabold ${
                  isDark
                    ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300'
                    : 'bg-[#dcecd8] border border-[#a8d4a6] text-[#1c5427]'
                }`}>
                  <CheckCircle2 className={`w-5 h-5 shrink-0 mt-0.5 ${isDark ? 'text-emerald-400' : 'text-[#1c5427]'}`} />
                  <div>{successMsg}</div>
                </div>
              )}

              {/* Auth Form */}
              <form onSubmit={handleAuthSubmit} className="space-y-4">
                {mode === 'register' && (
                  <div>
                    <label className={`block text-xs font-extrabold mb-1.5 ${isDark ? 'text-slate-300' : 'text-[#241810]'}`}>
                      Full Name
                    </label>
                    <div className="relative">
                      <User className={`absolute left-3.5 top-3.5 w-4 h-4 ${isDark ? 'text-slate-400' : 'text-[#8c7355]'}`} />
                      <input
                        type="text"
                        required
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="e.g. Sandy Smith"
                        className={`w-full rounded-xl pl-10 pr-4 py-3 text-sm font-semibold transition-all shadow-inner ${
                          isDark
                            ? 'bg-slate-950/80 border border-slate-800 text-white placeholder-slate-500 focus:border-indigo-500'
                            : 'bg-[#faf6f0] border border-[#caba9c] text-[#241810] placeholder-[#8e7960] focus:border-[#8b1e16]'
                        }`}
                      />
                    </div>
                  </div>
                )}

                <div>
                  <label className={`block text-xs font-extrabold mb-1.5 ${isDark ? 'text-slate-300' : 'text-[#241810]'}`}>
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className={`absolute left-3.5 top-3.5 w-4 h-4 ${isDark ? 'text-slate-400' : 'text-[#8c7355]'}`} />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@example.com"
                      className={`w-full rounded-xl pl-10 pr-4 py-3 text-sm font-semibold transition-all shadow-inner ${
                        isDark
                          ? 'bg-slate-950/80 border border-slate-800 text-white placeholder-slate-500 focus:border-indigo-500'
                          : 'bg-[#faf6f0] border border-[#caba9c] text-[#241810] placeholder-[#8e7960] focus:border-[#8b1e16]'
                      }`}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className={`block text-xs font-extrabold ${isDark ? 'text-slate-300' : 'text-[#241810]'}`}>
                      Password
                    </label>
                    {mode === 'login' && (
                      <button
                        type="button"
                        onClick={() => alert('Password reset link sent to your registered email.')}
                        className={`text-xs font-bold hover:underline transition-colors cursor-pointer ${
                          isDark ? 'text-indigo-400' : 'text-[#8b1e16]'
                        }`}
                      >
                        Forgot password?
                      </button>
                    )}
                  </div>
                  <div className="relative">
                    <Lock className={`absolute left-3.5 top-3.5 w-4 h-4 ${isDark ? 'text-slate-400' : 'text-[#8c7355]'}`} />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className={`w-full rounded-xl pl-10 pr-10 py-3 text-sm font-semibold transition-all shadow-inner ${
                        isDark
                          ? 'bg-slate-950/80 border border-slate-800 text-white placeholder-slate-500 focus:border-indigo-500'
                          : 'bg-[#faf6f0] border border-[#caba9c] text-[#241810] placeholder-[#8e7960] focus:border-[#8b1e16]'
                      }`}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className={`absolute right-3.5 top-3.5 cursor-pointer ${isDark ? 'text-slate-400 hover:text-white' : 'text-[#8c7355] hover:text-[#241810]'}`}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {mode === 'register' && (
                  <div>
                    <label className={`block text-xs font-extrabold mb-1.5 ${isDark ? 'text-slate-300' : 'text-[#241810]'}`}>
                      Confirm Password
                    </label>
                    <div className="relative">
                      <Lock className={`absolute left-3.5 top-3.5 w-4 h-4 ${isDark ? 'text-slate-400' : 'text-[#8c7355]'}`} />
                      <input
                        type={showPassword ? 'text' : 'password'}
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="••••••••"
                        className={`w-full rounded-xl pl-10 pr-4 py-3 text-sm font-semibold transition-all shadow-inner ${
                          isDark
                            ? 'bg-slate-950/80 border border-slate-800 text-white placeholder-slate-500 focus:border-indigo-500'
                            : 'bg-[#faf6f0] border border-[#caba9c] text-[#241810] placeholder-[#8e7960] focus:border-[#8b1e16]'
                        }`}
                      />
                    </div>
                  </div>
                )}

                {/* Checkbox Options */}
                <div className="flex items-center justify-between pt-1">
                  <label className={`flex items-center gap-2 cursor-pointer text-xs font-semibold select-none ${
                    isDark ? 'text-slate-400' : 'text-[#6e5845]'
                  }`}>
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className={`w-4 h-4 rounded ${
                        isDark
                          ? 'bg-slate-950 border-slate-800 text-indigo-600 focus:ring-indigo-500'
                          : 'bg-[#faf6f0] border-[#caba9c] text-[#8b1e16] focus:ring-[#8b1e16]'
                      }`}
                    />
                    <span>{mode === 'login' ? 'Keep me logged in' : 'I agree to Terms of Service & Privacy Policy'}</span>
                  </label>
                </div>

                {/* Primary Action Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className={`w-full py-3.5 px-4 text-white font-extrabold text-sm rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 group mt-2 cursor-pointer ${
                    isDark
                      ? 'bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 shadow-indigo-600/25'
                      : 'bg-gradient-to-r from-[#8b1e16] via-[#a3241b] to-[#c99a2e] shadow-red-950/25'
                  }`}
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
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
                    className={`w-full py-3 px-4 font-extrabold text-xs rounded-xl transition-all flex items-center justify-center gap-2 shadow-sm mt-3 cursor-pointer ${
                      isDark
                        ? 'bg-slate-950 hover:bg-slate-800 border border-indigo-500/30 text-indigo-300'
                        : 'bg-[#dfcfb9] hover:bg-[#d4c3ab] border border-[#c5b196] text-[#4e3d30]'
                    }`}
                  >
                    <Zap className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-[#8b1e16]'}`} />
                    <span>⚡ 1-Click Instant Guest Demo Sign In</span>
                  </button>
                )}
              </form>

              {/* Social Login Separator */}
              <div className="relative my-6 text-center">
                <div className="absolute inset-0 flex items-center">
                  <div className={`w-full border-t ${isDark ? 'border-slate-800' : 'border-[#caba9c]'}`} />
                </div>
                <span className={`relative px-3 text-xs uppercase tracking-wider font-extrabold ${
                  isDark ? 'bg-slate-900 text-slate-500' : 'bg-[#f5ece0] text-[#6e5845]'
                }`}>
                  Or continue with
                </span>
              </div>

              {/* Social SSO Buttons */}
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => handleQuickDemoLogin()}
                  className={`py-2.5 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 shadow-sm cursor-pointer ${
                    isDark
                      ? 'bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300'
                      : 'bg-[#ede2d2] hover:bg-[#ebdcc6] border border-[#caba9c] text-[#241810]'
                  }`}
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
                  className={`py-2.5 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 shadow-sm cursor-pointer ${
                    isDark
                      ? 'bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300'
                      : 'bg-[#ede2d2] hover:bg-[#ebdcc6] border border-[#caba9c] text-[#241810]'
                  }`}
                >
                  <svg className={`w-4 h-4 fill-current ${isDark ? 'text-white' : 'text-[#241810]'}`} viewBox="0 0 24 24">
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
      <footer className={`relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-xs font-semibold flex flex-col sm:flex-row items-center justify-between gap-4 ${
        isDark ? 'text-slate-500 border-t border-slate-900' : 'text-[#6e5845] border-t border-[#caba9c]'
      }`}>
        <div>
          © 2026 AGENTX AI Platform. All rights reserved. Powered by Sandya Kaki & FastAPI Architecture.
        </div>
        <div className="flex items-center gap-6 font-bold">
          <a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-300' : 'hover:text-[#8b1e16]'}`}>Privacy Policy</a>
          <a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-300' : 'hover:text-[#8b1e16]'}`}>Terms of Service</a>
          <a href="#" className={`transition-colors ${isDark ? 'hover:text-slate-300' : 'hover:text-[#8b1e16]'}`}>Documentation</a>
        </div>
      </footer>
    </div>
  );
}
