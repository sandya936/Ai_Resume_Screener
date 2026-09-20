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
    <div className="min-h-screen bg-[#f7f4ee] text-[#2c221a] flex flex-col justify-between selection:bg-[#b83227] selection:text-white relative overflow-hidden font-sans">
      {/* Subtle Background Glows */}
      <div className="absolute top-0 -left-4 w-96 h-96 bg-[#fee2e2]/40 rounded-full blur-3xl pointer-events-none animate-pulse" />
      <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-[#f2ede4]/60 rounded-full blur-3xl pointer-events-none" />

      {/* Navigation Header */}
      <header className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-[#b83227] via-[#d4af37] to-[#8c7355] p-[2px] shadow-md shadow-red-900/10 group-hover:scale-105 transition-transform duration-300">
            <div className="w-full h-full bg-[#faf7f2] rounded-[14px] flex items-center justify-center">
              <Bot className="w-6 h-6 text-[#b83227]" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-2xl tracking-tight text-[#2c221a]">
                AGENT<span className="text-[#b83227]">X</span>
              </span>
              <span className="text-[10px] uppercase font-bold tracking-widest bg-[#f2ede4] text-[#8c7355] border border-[#d8c8b0] px-2 py-0.5 rounded-full">
                AI 2.0
              </span>
            </div>
            <span className="text-xs text-[#6b5a4b] hidden sm:block">Enterprise AI Resume & Career Intelligence</span>
          </div>
        </Link>
      </header>

      {/* Main Container */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex items-center justify-center">
        <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Hero Brand Panel (Desktop) */}
          <div className="lg:col-span-6 space-y-6 lg:pr-8 text-center lg:text-left">
            <div className="inline-flex items-center gap-2 bg-[#f2ede4] border border-[#d8c8b0] px-3.5 py-1.5 rounded-full text-xs font-semibold text-[#8c7355]">
              <ShieldCheck className="w-4 h-4 text-[#b83227]" />
              <span>Next-Gen Enterprise Career Intelligence</span>
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-[#2c221a] tracking-tight leading-tight">
              Transform Your Resume into a <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#b83227] via-[#9e2419] to-[#8c7355]">High-Impact</span> Career Asset.
            </h1>

            <p className="text-[#6b5a4b] text-base sm:text-lg leading-relaxed max-w-xl mx-auto lg:mx-0">
              Unlock real-time ATS compatibility scoring, Job Description keyword matching, 40-question dynamic interview preparation, and autonomous Multi-Agent AI career roadmap guidance.
            </p>

            {/* Feature Highlights Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
              <div className="bg-[#faf7f2] border border-[#e2d5c3] rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left hover:border-[#b83227] transition-colors">
                <div className="p-2.5 bg-[#fee2e2]/60 rounded-xl text-[#b83227]">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-[#2c221a]">Instant ATS Audit</h4>
                  <p className="text-xs text-[#6b5a4b]">99.8% precision score across 7 core structural criteria.</p>
                </div>
              </div>

              <div className="bg-[#faf7f2] border border-[#e2d5c3] rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left hover:border-[#b83227] transition-colors">
                <div className="p-2.5 bg-[#f2ede4] rounded-xl text-[#8c7355]">
                  <BrainCircuit className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-[#2c221a]">40 Interview Questions</h4>
                  <p className="text-xs text-[#6b5a4b]">Top 20 Technical Deep Dives + 20 Behavioral STAR practice questions.</p>
                </div>
              </div>

              <div className="bg-[#faf7f2] border border-[#e2d5c3] rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left hover:border-[#b83227] transition-colors">
                <div className="p-2.5 bg-emerald-100/80 rounded-xl text-emerald-800">
                  <Briefcase className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-[#2c221a]">1-Click Job Match</h4>
                  <p className="text-xs text-[#6b5a4b]">Pinpoint required skill gaps and actionable candidate keywords.</p>
                </div>
              </div>

              <div className="bg-[#faf7f2] border border-[#e2d5c3] rounded-2xl p-4 shadow-sm flex items-start gap-3 text-left hover:border-[#b83227] transition-colors">
                <div className="p-2.5 bg-[#fee2e2]/60 rounded-xl text-[#b83227]">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-[#2c221a]">Multi-Agent Swarm</h4>
                  <p className="text-xs text-[#6b5a4b]">Autonomous LLM workflow executing parallel career tasks.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Login / Sign Up Card Form */}
          <div className="lg:col-span-6 flex justify-center">
            <div className="w-full max-w-md bg-[#faf7f2] border border-[#e2d5c3] rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-[#b83227] via-[#d4af37] to-[#8c7355]" />

              {/* Mode Toggle Tabs */}
              <div className="flex bg-[#f2ede4] p-1.5 rounded-2xl border border-[#d8c8b0] mb-6">
                <button
                  type="button"
                  onClick={() => { setMode('login'); setErrorMsg(null); setSuccessMsg(null); }}
                  className={`flex-1 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                    mode === 'login'
                      ? 'bg-gradient-to-r from-[#b83227] to-[#9e2419] text-white shadow-md'
                      : 'text-[#6b5a4b] hover:text-[#2c221a]'
                  }`}
                >
                  Sign In
                </button>
                <button
                  type="button"
                  onClick={() => { setMode('register'); setErrorMsg(null); setSuccessMsg(null); }}
                  className={`flex-1 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                    mode === 'register'
                      ? 'bg-gradient-to-r from-[#b83227] to-[#9e2419] text-white shadow-md'
                      : 'text-[#6b5a4b] hover:text-[#2c221a]'
                  }`}
                >
                  Create Account
                </button>
              </div>

              {/* Title & Subtitle */}
              <div className="text-center mb-6">
                <h2 className="text-xl sm:text-2xl font-bold text-[#2c221a]">
                  {mode === 'login' ? 'Welcome Back to AGENTX' : 'Create Your Free Account'}
                </h2>
                <p className="text-xs sm:text-sm text-[#6b5a4b] mt-1">
                  {mode === 'login'
                    ? 'Enter your credentials to access your AI Career Intelligence workspace.'
                    : 'Start auditing resumes, analyzing ATS scores, and generating interview questions.'}
                </p>
              </div>

              {/* Error & Success Feedback Alerts */}
              {errorMsg && (
                <div className="mb-5 bg-red-50 border border-red-200 text-red-800 p-3.5 rounded-2xl flex items-start gap-3 text-xs sm:text-sm font-medium">
                  <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                  <div>{errorMsg}</div>
                </div>
              )}

              {successMsg && (
                <div className="mb-5 bg-emerald-50 border border-emerald-200 text-emerald-900 p-3.5 rounded-2xl flex items-start gap-3 text-xs sm:text-sm font-medium">
                  <CheckCircle2 className="w-5 h-5 text-emerald-700 shrink-0 mt-0.5" />
                  <div>{successMsg}</div>
                </div>
              )}

              {/* Auth Form */}
              <form onSubmit={handleAuthSubmit} className="space-y-4">
                {mode === 'register' && (
                  <div>
                    <label className="block text-xs font-semibold text-[#2c221a] mb-1.5">
                      Full Name
                    </label>
                    <div className="relative">
                      <User className="absolute left-3.5 top-3.5 w-4 h-4 text-[#8c7355]" />
                      <input
                        type="text"
                        required
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="e.g. Sandy Smith"
                        className="w-full bg-white border border-[#d8c8b0] rounded-xl pl-10 pr-4 py-3 text-sm text-[#2c221a] placeholder-[#a0907c] focus:outline-none focus:border-[#b83227] transition-all"
                      />
                    </div>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-semibold text-[#2c221a] mb-1.5">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-3.5 w-4 h-4 text-[#8c7355]" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@example.com"
                      className="w-full bg-white border border-[#d8c8b0] rounded-xl pl-10 pr-4 py-3 text-sm text-[#2c221a] placeholder-[#a0907c] focus:outline-none focus:border-[#b83227] transition-all"
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="block text-xs font-semibold text-[#2c221a]">
                      Password
                    </label>
                    {mode === 'login' && (
                      <button
                        type="button"
                        onClick={() => alert('Password reset link sent to your registered email.')}
                        className="text-xs font-medium text-[#b83227] hover:underline transition-colors"
                      >
                        Forgot password?
                      </button>
                    )}
                  </div>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-3.5 w-4 h-4 text-[#8c7355]" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full bg-white border border-[#d8c8b0] rounded-xl pl-10 pr-10 py-3 text-sm text-[#2c221a] placeholder-[#a0907c] focus:outline-none focus:border-[#b83227] transition-all"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-3.5 text-[#8c7355] hover:text-[#2c221a]"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {mode === 'register' && (
                  <div>
                    <label className="block text-xs font-semibold text-[#2c221a] mb-1.5">
                      Confirm Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3.5 top-3.5 w-4 h-4 text-[#8c7355]" />
                      <input
                        type={showPassword ? 'text' : 'password'}
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="••••••••"
                        className="w-full bg-white border border-[#d8c8b0] rounded-xl pl-10 pr-4 py-3 text-sm text-[#2c221a] placeholder-[#a0907c] focus:outline-none focus:border-[#b83227] transition-all"
                      />
                    </div>
                  </div>
                )}

                {/* Checkbox Options */}
                <div className="flex items-center justify-between pt-1">
                  <label className="flex items-center gap-2 cursor-pointer text-xs text-[#6b5a4b] select-none">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 rounded bg-white border-[#d8c8b0] text-[#b83227] focus:ring-[#b83227]"
                    />
                    <span>{mode === 'login' ? 'Keep me logged in' : 'I agree to Terms of Service & Privacy Policy'}</span>
                  </label>
                </div>

                {/* Primary Action Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full py-3.5 px-4 bg-gradient-to-r from-[#b83227] via-[#9e2419] to-[#d4af37] hover:scale-[1.01] text-white font-bold text-sm rounded-xl shadow-lg shadow-red-900/15 hover:shadow-red-900/30 transition-all flex items-center justify-center gap-2 group mt-2"
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
                    className="w-full py-3 px-4 bg-[#f2ede4] hover:bg-[#e8decb] border border-[#d8c8b0] text-[#5c4936] font-semibold text-xs rounded-xl transition-all flex items-center justify-center gap-2 shadow-sm mt-3"
                  >
                    <Zap className="w-4 h-4 text-[#b83227]" />
                    <span>⚡ 1-Click Instant Guest Demo Sign In</span>
                  </button>
                )}
              </form>

              {/* Social Login Separator */}
              <div className="relative my-6 text-center">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-[#e2d5c3]" />
                </div>
                <span className="relative px-3 bg-[#faf7f2] text-[#6b5a4b] text-xs uppercase tracking-wider font-semibold">
                  Or continue with
                </span>
              </div>

              {/* Social SSO Buttons */}
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => handleQuickDemoLogin()}
                  className="py-2.5 px-3 bg-white hover:bg-[#f7f4ee] border border-[#d8c8b0] rounded-xl text-xs font-semibold text-[#2c221a] transition-all flex items-center justify-center gap-2 shadow-sm"
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
                  className="py-2.5 px-3 bg-white hover:bg-[#f7f4ee] border border-[#d8c8b0] rounded-xl text-xs font-semibold text-[#2c221a] transition-all flex items-center justify-center gap-2 shadow-sm"
                >
                  <svg className="w-4 h-4 fill-current text-[#2c221a]" viewBox="0 0 24 24">
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
      <footer className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-xs text-[#6b5a4b] flex flex-col sm:flex-row items-center justify-between border-t border-[#e2d5c3] gap-4">
        <div>
          © 2026 AGENTX AI Platform. All rights reserved. Powered by Google Antigravity & FastAPI Architecture.
        </div>
        <div className="flex items-center gap-6 font-medium">
          <a href="#" className="hover:text-[#b83227] transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-[#b83227] transition-colors">Terms of Service</a>
          <a href="#" className="hover:text-[#b83227] transition-colors">Documentation</a>
        </div>
      </footer>
    </div>
  );
}
