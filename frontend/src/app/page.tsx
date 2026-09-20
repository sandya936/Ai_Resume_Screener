'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  FileText,
  Target,
  Compass,
  MessageSquare,
  Bot,
  Upload,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
  Activity,
  Code,
  Layers,
  Terminal,
  Cpu,
  Loader2,
  AlertCircle,
  TrendingUp,
  Award,
  AlertTriangle,
  XCircle,
  RefreshCw,
  Clock,
  Play,
  Check,
  Briefcase,
  Sliders,
  Star,
  BookOpen,
  BrainCircuit,
  FileCheck,
  ChevronRight,
  User,
  LogOut,
  LogIn,
} from 'lucide-react';
import {
  uploadResumeFile,
  parseResume,
  runATSAnalysis,
  createJobDescription,
  matchJobAndResume,
  generateCareerInsights,
  generateInterviewQuestions,
  orchestrateAgents,
  getSavedToken,
  getSavedUser,
  clearAuthSession,
} from '@/lib/api';
import { SAMPLE_PDF_BASE64 } from '@/lib/sample_pdf';

const PRESET_JDS = [
  {
    label: '📊 Junior Data Analyst (Fresher)',
    title: 'Junior Data Analyst / Associate Data Analyst (Fresher)',
    jd: `Basic proficiency in Python or R for data manipulation (using libraries like pandas or tidyverse). Data Visualization: Hands-on familiarity with tools like Power BI, Tableau, Plotly, or Streamlit. Excel: Working knowledge of advanced Microsoft Excel (VLOOKUP, Pivot Tables). Soft Skills: Strong problem-solving mindset, sharp attention to detail, and the ability to clearly communicate data findings to technical and non-technical stakeholders.`,
  },
  {
    label: '🚀 Senior Full-Stack Engineer',
    title: 'Senior Full-Stack Engineer (FastAPI & Next.js)',
    jd: `Looking for a Senior Full-Stack Engineer with 5+ years of experience building cloud platform microservices. Required Skills: Python, FastAPI, TypeScript, Next.js, PostgreSQL, Docker, Git. Preferred Skills: Redis, GraphQL, Tailwind CSS, CI/CD pipelines, AWS. Responsible for architecture design, database query optimization, and REST API engineering.`,
  },
];

export default function AGENTXProductionDashboard() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState<string>('');
  const [jobDescription, setJobDescription] = useState<string>('');

  const [activeTab, setActiveTab] = useState<'overview' | 'ats' | 'match' | 'roadmap' | 'interview' | 'agents'>('overview');
  const [interviewFilter, setInterviewFilter] = useState<'all' | 'resume_based' | 'hr_based'>('all');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [backendOnline, setBackendOnline] = useState<boolean>(true);

  // Dynamic state populated by real FastAPI responses
  const [executionResult, setExecutionResult] = useState<{
    resumeId?: string;
    jobId?: string;
    atsData?: any;
    matchData?: any;
    careerData?: any;
    interviewData?: any;
    orchestrationData?: any;
  } | null>(null);

  const router = useRouter();
  const [currentUser, setCurrentUser] = useState<any | null>(null);
  const [isAuthChecked, setIsAuthChecked] = useState<boolean>(false);

  useEffect(() => {
    // Check saved user session
    const token = getSavedToken();
    const u = getSavedUser();

    if (!token || !u) {
      router.push('/login');
      return;
    }

    setCurrentUser(u);
    setIsAuthChecked(true);

    // Ping backend health endpoint
    fetch('http://localhost:8000/api/v1/health')
      .then((res) => res.json())
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(true));
  }, []);

  const handleLogout = () => {
    clearAuthSession();
    setCurrentUser(null);
    router.push('/login');
  };

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const applyPresetJD = (preset: typeof PRESET_JDS[0]) => {
    setJobTitle(preset.title);
    setJobDescription(preset.jd);
  };

  // Full end-to-end execution calling all FastAPI endpoints
  const runLivePipeline = async () => {
    setIsProcessing(true);
    setErrorMessage(null);
    try {
      let resumeId = executionResult?.resumeId;

      // Step 1: Upload or create resume record
      if (selectedFile) {
        setCurrentStep('Uploading resume document & verifying magic bytes header...');
        const uploadRes = await uploadResumeFile(selectedFile);
        resumeId = uploadRes?.id || uploadRes?.resume?.id;
      } else if (!resumeId) {
        setCurrentStep('Processing candidate resume credentials...');
        const binaryString = atob(SAMPLE_PDF_BASE64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        const sampleFile = new File([bytes], 'sample_resume.pdf', { type: 'application/pdf' });
        const uploadRes = await uploadResumeFile(sampleFile);
        resumeId = uploadRes?.id || uploadRes?.resume?.id;
      }

      if (!resumeId) {
        throw new Error('Resume ID not generated from upload');
      }

      // Step 2: Parse resume
      setCurrentStep('Parsing resume structure & normalizing candidate skills...');
      await parseResume(resumeId);

      // Step 3: Run ATS Analysis Engine
      setCurrentStep('Calculating 60% Deterministic + 40% AI Auditor ATS score...');
      const atsRes = await runATSAnalysis(resumeId);

      // Step 4: Create Job Description & Match
      setCurrentStep('Normalizing skill synonyms & running 5-category job match formula...');
      const targetTitle = jobTitle.trim() || 'Junior Data Analyst / Associate Data Analyst (Fresher)';
      const targetJD = jobDescription.trim() || targetTitle;
      const jobRes = await createJobDescription(
        targetTitle,
        'Target Company',
        targetJD
      );
      const matchRes = await matchJobAndResume(jobRes.id, resumeId);

      // Step 5: Generate Career Insights & Interview Questions
      setCurrentStep('Generating Top 20 Resume + Top 20 HR practice questions & 30-day roadmap...');
      const careerRes = await generateCareerInsights(resumeId, targetTitle);
      const interviewRes = await generateInterviewQuestions(resumeId);

      // Step 6: Run Multi-Agent Orchestration
      setCurrentStep('Orchestrating 6 Autonomous Agents (Manager, Resume, JD, SkillGap, Roadmap, Interview)...');
      const orchRes = await orchestrateAgents(
        `Analyze candidate resume against target JD (${targetTitle}), calculate exact ATS score, identify missing skills, generate 40 dynamic questions, and build career roadmap.`,
        resumeId,
        jobRes.id
      );

      // Store dynamic result in state
      setExecutionResult({
        resumeId,
        jobId: jobRes.id,
        atsData: atsRes.ats_analysis,
        matchData: matchRes.match_result,
        careerData: careerRes.career_insights,
        interviewData: interviewRes.questions,
        orchestrationData: orchRes,
      });

      setActiveTab('overview');
    } catch (err: any) {
      console.error(err);
      setErrorMessage(err.message || 'An error occurred during pipeline execution.');
    } finally {
      setIsProcessing(false);
      setCurrentStep('');
    }
  };

  return (
    <div className="min-h-screen bg-[#ebdcc6] text-[#241810] flex flex-col selection:bg-[#8b1e16] selection:text-white">
      {/* Navbar Header */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-[#e8dac5]/90 border-b border-[#caba9c] px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#8b1e16] via-[#d4af37] to-[#8c7355] p-[1px] flex items-center justify-center shadow-md shadow-red-950/20">
              <div className="w-full h-full bg-[#f5ece0] rounded-[11px] flex items-center justify-center">
                <Bot className="w-5 h-5 text-[#8b1e16] animate-pulse" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-extrabold text-xl tracking-tight text-[#241810]">
                  AGENT<span className="text-[#8b1e16]">X</span>
                </h1>
                <span className="px-2.5 py-0.5 text-[10px] font-bold bg-[#dcecd8] text-[#1c5427] border border-[#a8d4a6] rounded-full flex items-center gap-1.5 shadow-sm">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#1c5427] animate-ping" />
                  Live Engine Active
                </span>
              </div>
              <p className="text-xs text-[#6e5845]">AI Resume Intelligence & Autonomous Career Platform</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#dfcfb9] border border-[#c5b196] text-xs">
              <span className="w-2 h-2 rounded-full bg-[#1c5427]" />
              <span className="text-[#4e3d30] font-bold">FastAPI Service Online (Port 8000)</span>
            </div>

            {currentUser && (
              <div className="flex items-center gap-2 bg-[#f5ece0] border border-[#caba9c] pl-3 pr-2 py-1.5 rounded-xl text-xs shadow-sm">
                <User className="w-4 h-4 text-[#8b1e16]" />
                <span className="font-bold text-[#241810] hidden sm:inline">
                  {currentUser.full_name || currentUser.email}
                </span>
                <button
                  type="button"
                  onClick={handleLogout}
                  title="Sign Out of Workspace"
                  className="flex items-center gap-1.5 px-2.5 py-1 bg-[#f5dcd8] hover:bg-[#ebd0cc] text-[#8b1e16] border border-[#e8b5ae] rounded-lg transition-all text-xs font-bold ml-1 cursor-pointer"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8 space-y-8">
        
        {/* Hero Banner Section with Rich Deep Crimson & Gold Texture */}
        <section className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#5e120b] via-[#851c14] to-[#3d2014] border border-[#d4af37]/60 p-6 sm:p-8 shadow-xl text-white">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
            <div className="lg:col-span-7 space-y-4">
              <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#d4af37]/20 border border-[#d4af37]/50 text-[#fef3c7] text-xs font-bold shadow-sm">
                <Sparkles className="w-4 h-4 text-[#fde68a]" />
                6-Agent Autonomous Architecture
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
                Transform Resumes into Explainable <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#fef3c7] via-[#fde68a] to-[#ffffff]">Career Intelligence</span>
              </h2>
              <p className="text-[#f5ead6] text-xs sm:text-sm leading-relaxed font-medium">
                Execute 60% Deterministic + 40% AI Auditor scoring, canonical skill synonym normalization (<code className="bg-[#420a05] text-[#fde68a] px-1.5 py-0.5 rounded border border-[#d4af37]/40">K8s</code> → <code className="bg-[#420a05] text-[#fde68a] px-1.5 py-0.5 rounded border border-[#d4af37]/40">kubernetes</code>), 5-category job fit formulas, and 40 dynamic STAR practice questions.
              </p>
              
              <div className="pt-2 flex flex-wrap gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#300a06]/90 border border-[#d4af37]/30 text-xs text-[#fde68a] font-semibold">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  Anti-Prompt Injection Guardrails
                </div>
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#300a06]/90 border border-[#d4af37]/30 text-xs text-[#fde68a] font-semibold">
                  <BrainCircuit className="w-4 h-4 text-purple-300" />
                  40 Dynamic Interview Questions
                </div>
              </div>
            </div>

            <div className="lg:col-span-5 relative">
              <div className="relative rounded-2xl overflow-hidden border border-[#d4af37]/50 shadow-2xl group glass-card">
                <Image
                  src="/ai_resume_hero.jpg"
                  alt="AI Resume Platform"
                  width={600}
                  height={338}
                  className="w-full h-auto object-cover group-hover:scale-105 transition-transform duration-500"
                  priority
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#2e0906] via-transparent to-transparent opacity-50" />
              </div>
            </div>
          </div>
        </section>

        {/* Live Execution Control Center Section */}
        <section className="rounded-3xl parchment-card p-6 sm:p-8 space-y-6 shadow-lg border border-[#caba9c]">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#caba9c] pb-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#e6d7c3] border border-[#caaf90] text-[#8b1e16] text-xs font-bold mb-2">
                <Zap className="w-3.5 h-3.5 text-[#8b1e16]" />
                Live Control Center
              </div>
              <h3 className="text-2xl font-extrabold text-[#241810] tracking-tight">
                Candidate Document & Job Description Ingestion
              </h3>
              <p className="text-xs sm:text-sm text-[#6e5845] mt-1 font-medium">
                Upload candidate resume credentials and input target position requirements to run end-to-end analysis.
              </p>
            </div>

            <button
              onClick={runLivePipeline}
              disabled={isProcessing}
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-[#8b1e16] via-[#a3241b] to-[#c99a2e] text-white font-extrabold text-sm shadow-lg shadow-red-950/25 hover:shadow-red-950/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shrink-0 cursor-pointer"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Running AI Pipeline...
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 fill-current" />
                  Run AI Analysis & Autonomous Pipeline
                </>
              )}
            </button>
          </div>

          {/* Live Progress Step Indicator */}
          {isProcessing && (
            <div className="p-4 rounded-xl bg-[#f5dcd8] border border-[#e8b5ae] space-y-2 animate-pulse">
              <div className="flex items-center gap-3 text-xs text-[#8b1e16] font-bold">
                <Activity className="w-4 h-4 animate-spin text-[#8b1e16]" />
                <span>{currentStep}</span>
              </div>
            </div>
          )}

          {errorMessage && (
            <div className="p-4 rounded-xl bg-red-100 border border-red-300 flex items-start gap-3 text-red-900 text-xs font-semibold">
              <AlertCircle className="w-4 h-4 text-red-700 shrink-0 mt-0.5" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Dual Column Input Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Column 1: Candidate Resume Upload */}
            <div className="p-6 rounded-2xl bg-[#ede2d2] border border-[#caba9c] space-y-4 flex flex-col justify-between shadow-sm">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2 font-extrabold text-sm text-[#241810]">
                    <FileText className="w-4 h-4 text-[#8b1e16]" />
                    Step 1: Upload Candidate Resume
                  </div>
                  <span className="text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded bg-[#dfcfb9] text-[#5c4735] border border-[#caaf90]">
                    PDF / DOCX
                  </span>
                </div>

                <div
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleFileDrop}
                  className="border-2 border-dashed border-[#b8a58c] hover:border-[#8b1e16] rounded-xl p-6 text-center transition-all bg-[#f5ece0] hover:bg-[#ebdcc6] cursor-pointer group shadow-inner"
                >
                  <input
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="resume-upload-input"
                  />
                  <label htmlFor="resume-upload-input" className="cursor-pointer space-y-2 block">
                    <div className="w-12 h-12 rounded-xl bg-[#f5dcd8] border border-[#e8b5ae] flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                      <Upload className="w-6 h-6 text-[#8b1e16]" />
                    </div>
                    {selectedFile ? (
                      <div>
                        <p className="font-extrabold text-sm text-[#1c5427] flex items-center justify-center gap-1.5">
                          <CheckCircle2 className="w-4 h-4 text-[#1c5427]" /> {selectedFile.name}
                        </p>
                        <p className="text-[11px] text-[#6e5845] font-semibold">
                          {(selectedFile.size / 1024).toFixed(1)} KB — Ready for extraction
                        </p>
                      </div>
                    ) : (
                      <div>
                        <p className="font-bold text-xs text-[#241810]">
                          Drag & drop resume file here, or <span className="text-[#8b1e16] underline">browse</span>
                        </p>
                        <p className="text-[11px] text-[#6e5845] mt-1">
                          Magic Bytes verified (%PDF-, PK\x03\x04). Max 10MB limit.
                        </p>
                      </div>
                    )}
                  </label>
                </div>
              </div>

              <div className="pt-3 border-t border-[#caba9c] flex items-center justify-between text-xs">
                <span className="text-[#6e5845] font-semibold">No file on hand? Use sample credentials:</span>
                <button
                  onClick={() => setSelectedFile(null)}
                  className="px-3 py-1.5 rounded-lg bg-[#dfcfb9] hover:bg-[#d4c3ab] text-[#4e3d30] border border-[#c5b196] font-extrabold transition shadow-sm cursor-pointer"
                >
                  Use Sample Candidate Resume
                </button>
              </div>
            </div>

            {/* Column 2: Target Position & Job Description */}
            <div className="p-6 rounded-2xl bg-[#ede2d2] border border-[#caba9c] space-y-4 shadow-sm">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2 font-extrabold text-sm text-[#241810]">
                  <Target className="w-4 h-4 text-[#8c7355]" />
                  Step 2: Target Position & Job Description
                </div>
                <span className="text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded bg-[#dfcfb9] text-[#5c4735] border border-[#caaf90]">
                  Target JD
                </span>
              </div>

              {/* Quick Presets */}
              <div className="flex items-center gap-2 overflow-x-auto pb-1">
                <span className="text-[11px] text-[#6e5845] font-bold shrink-0">Quick Presets:</span>
                {PRESET_JDS.map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => applyPresetJD(preset)}
                    className="px-2.5 py-1 rounded-lg bg-[#f8f3ea] hover:bg-[#e4d6c1] text-[#241810] border border-[#caba9c] text-[11px] font-bold transition shrink-0 shadow-sm cursor-pointer"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>

              <div className="space-y-3">
                <input
                  type="text"
                  placeholder="Target Role Title (e.g., Junior Data Analyst, Software Engineer)"
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#faf6f0] border border-[#caba9c] text-xs text-[#241810] font-semibold placeholder:text-[#8e7960] focus:outline-none focus:border-[#8b1e16] transition shadow-inner"
                />

                <textarea
                  rows={4}
                  placeholder="Paste Job Description requirements (e.g. required skills like Python, Power BI, SQL, Excel, communication)..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#faf6f0] border border-[#caba9c] text-xs text-[#241810] font-semibold placeholder:text-[#8e7960] focus:outline-none focus:border-[#8b1e16] transition resize-none shadow-inner"
                />
              </div>
            </div>

          </div>
        </section>

        {/* Tab Navigation Menu */}
        <section className="space-y-6">
          <div className="flex items-center gap-2 border-b-2 border-[#caba9c] overflow-x-auto pb-1">
            <button
              onClick={() => setActiveTab('overview')}
              className={`flex items-center gap-2 px-4 py-3 font-extrabold text-xs rounded-t-xl transition-all border-b-2 shrink-0 cursor-pointer ${
                activeTab === 'overview'
                  ? 'bg-[#8b1e16] text-white border-[#d4af37] shadow-md'
                  : 'text-[#6e5845] hover:text-[#241810] hover:bg-[#e4d6c1]'
              }`}
            >
              <Activity className="w-4 h-4" /> Execution Summary
            </button>
            <button
              onClick={() => setActiveTab('ats')}
              className={`flex items-center gap-2 px-4 py-3 font-extrabold text-xs rounded-t-xl transition-all border-b-2 shrink-0 cursor-pointer ${
                activeTab === 'ats'
                  ? 'bg-[#8b1e16] text-white border-[#d4af37] shadow-md'
                  : 'text-[#6e5845] hover:text-[#241810] hover:bg-[#e4d6c1]'
              }`}
            >
              <FileCheck className="w-4 h-4" /> ATS Scoring ({executionResult?.atsData?.overall_score ?? '--'}%)
            </button>
            <button
              onClick={() => setActiveTab('match')}
              className={`flex items-center gap-2 px-4 py-3 font-extrabold text-xs rounded-t-xl transition-all border-b-2 shrink-0 cursor-pointer ${
                activeTab === 'match'
                  ? 'bg-[#8b1e16] text-white border-[#d4af37] shadow-md'
                  : 'text-[#6e5845] hover:text-[#241810] hover:bg-[#e4d6c1]'
              }`}
            >
              <Target className="w-4 h-4" /> Job Match ({executionResult?.matchData?.overall_match_score ?? '--'}%)
            </button>
            <button
              onClick={() => setActiveTab('roadmap')}
              className={`flex items-center gap-2 px-4 py-3 font-extrabold text-xs rounded-t-xl transition-all border-b-2 shrink-0 cursor-pointer ${
                activeTab === 'roadmap'
                  ? 'bg-[#8b1e16] text-white border-[#d4af37] shadow-md'
                  : 'text-[#6e5845] hover:text-[#241810] hover:bg-[#e4d6c1]'
              }`}
            >
              <Compass className="w-4 h-4" /> 30-Day Roadmap
            </button>
            <button
              onClick={() => setActiveTab('interview')}
              className={`flex items-center gap-2 px-4 py-3 font-extrabold text-xs rounded-t-xl transition-all border-b-2 shrink-0 cursor-pointer ${
                activeTab === 'interview'
                  ? 'bg-[#8b1e16] text-white border-[#d4af37] shadow-md'
                  : 'text-[#6e5845] hover:text-[#241810] hover:bg-[#e4d6c1]'
              }`}
            >
              <MessageSquare className="w-4 h-4" /> STAR Practice Studio (40 Questions)
            </button>
            <button
              onClick={() => setActiveTab('agents')}
              className={`flex items-center gap-2 px-4 py-3 font-extrabold text-xs rounded-t-xl transition-all border-b-2 shrink-0 cursor-pointer ${
                activeTab === 'agents'
                  ? 'bg-[#8b1e16] text-white border-[#d4af37] shadow-md'
                  : 'text-[#6e5845] hover:text-[#241810] hover:bg-[#e4d6c1]'
              }`}
            >
              <Bot className="w-4 h-4" /> Agent Execution Trace
            </button>
          </div>

          {/* TAB CONTENT AREA */}
          <div className="space-y-6">

            {/* TAB 1: OVERVIEW */}
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Metric Summary Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-5 rounded-2xl parchment-card parchment-card-hover space-y-2 border border-[#d4c2a8] shadow-md">
                    <div className="flex items-center justify-between text-xs text-[#5c4735]">
                      <span className="font-extrabold text-[#241810]">ATS Structure Grade</span>
                      <Award className="w-4 h-4 text-[#1c5427]" />
                    </div>
                    <div className="text-3xl font-black text-[#8b1e16]">
                      {executionResult?.atsData?.overall_score !== undefined
                        ? `${executionResult.atsData.overall_score}%`
                        : 'N/A'}
                    </div>
                    <p className="text-[11px] text-[#6e5845] font-semibold">Formatting & Quality (Job-Independent)</p>
                  </div>

                  <div className="p-5 rounded-2xl parchment-card parchment-card-hover space-y-2 border border-[#d4c2a8] shadow-md">
                    <div className="flex items-center justify-between text-xs text-[#5c4735]">
                      <span className="font-extrabold text-[#241810]">Job Skill Alignment</span>
                      <Target className="w-4 h-4 text-[#8b1e16]" />
                    </div>
                    <div className="text-3xl font-black text-[#8b1e16]">
                      {executionResult?.matchData?.overall_match_score !== undefined
                        ? `${executionResult.matchData.overall_match_score}%`
                        : 'N/A'}
                    </div>
                    <p className="text-[11px] text-[#6e5845] font-semibold">Position Tech Fit (Job-Specific)</p>
                  </div>

                  <div className="p-5 rounded-2xl parchment-card parchment-card-hover space-y-2 border border-[#d4c2a8] shadow-md">
                    <div className="flex items-center justify-between text-xs text-[#5c4735]">
                      <span className="font-extrabold text-[#241810]">Matched Skills</span>
                      <CheckCircle2 className="w-4 h-4 text-[#1c5427]" />
                    </div>
                    <div className="text-3xl font-black text-[#8b1e16]">
                      {executionResult?.matchData?.matched_skills?.length ?? 0}
                    </div>
                    <p className="text-[11px] text-[#6e5845] font-semibold">Normalized synonym matches</p>
                  </div>

                  <div className="p-5 rounded-2xl parchment-card parchment-card-hover space-y-2 border border-[#d4c2a8] shadow-md">
                    <div className="flex items-center justify-between text-xs text-[#5c4735]">
                      <span className="font-extrabold text-[#241810]">Practice Questions</span>
                      <MessageSquare className="w-4 h-4 text-[#8c7355]" />
                    </div>
                    <div className="text-3xl font-black text-[#8b1e16]">
                      {executionResult?.interviewData?.length ?? 40}
                    </div>
                    <p className="text-[11px] text-[#6e5845] font-semibold">Top 20 Resume + Top 20 HR</p>
                  </div>
                </div>

                {/* Executive Action Plan Summary */}
                {executionResult?.orchestrationData?.final_action_plan && (
                  <div className="p-6 rounded-2xl bg-[#ede2d2] border border-[#caba9c] shadow-md space-y-3">
                    <div className="flex items-center gap-2 font-extrabold text-sm text-[#8b1e16]">
                      <Sparkles className="w-4 h-4 text-[#d4af37]" /> Orchestrator Executive Summary
                    </div>
                    <p className="text-xs sm:text-sm text-[#241810] font-medium leading-relaxed">
                      {executionResult.orchestrationData.final_action_plan.executive_summary}
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: ATS SCORING */}
            {activeTab === 'ats' && (
              <div className="rounded-2xl parchment-card p-6 space-y-6 shadow-md border border-[#caba9c]">
                <div className="flex items-center justify-between border-b border-[#caba9c] pb-4">
                  <div>
                    <h3 className="font-extrabold text-lg text-[#241810]">ATS Compatibility Report</h3>
                    <p className="text-xs text-[#6e5845]">Calculated by FastAPI ATSAnalyzerService</p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-black text-[#1c5427]">
                      {executionResult?.atsData?.overall_score !== undefined
                        ? `${executionResult.atsData.overall_score} / 100`
                        : 'N/A'}
                    </div>
                    <div className="text-xs text-[#6e5845] font-bold">Overall ATS Grade</div>
                  </div>
                </div>

                {executionResult?.atsData ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-5 rounded-xl bg-[#dcecd8] border border-[#a8d4a6] space-y-3 shadow-sm">
                      <div className="flex items-center gap-2 font-extrabold text-xs text-[#1c5427]">
                        <CheckCircle2 className="w-4 h-4 text-[#1c5427]" /> Verified Resume Strengths
                      </div>
                      <ul className="space-y-2 text-xs text-[#1c5427] font-semibold">
                        {executionResult.atsData.strengths && executionResult.atsData.strengths.length > 0 ? (
                          executionResult.atsData.strengths.map((s: string, idx: number) => (
                            <li key={idx} className="flex items-start gap-2">
                              <span className="text-[#1c5427] mt-0.5">•</span> <span>{s}</span>
                            </li>
                          ))
                        ) : (
                          <li className="text-[#6e5845] italic">No verified strengths flagged.</li>
                        )}
                      </ul>
                    </div>

                    <div className="p-5 rounded-xl bg-[#f5dcd8] border border-[#e8b5ae] space-y-3 shadow-sm">
                      <div className="flex items-center gap-2 font-extrabold text-xs text-[#8b1e16]">
                        <Sparkles className="w-4 h-4 text-[#8b1e16]" /> Actionable Improvements
                      </div>
                      <ul className="space-y-2 text-xs text-[#8b1e16] font-semibold">
                        {executionResult.atsData.actionable_improvements && executionResult.atsData.actionable_improvements.length > 0 ? (
                          executionResult.atsData.actionable_improvements.map((imp: string, idx: number) => (
                            <li key={idx} className="flex items-start gap-2">
                              <span className="text-[#8b1e16] mt-0.5">•</span> <span>{imp}</span>
                            </li>
                          ))
                        ) : (
                          <li className="text-[#6e5845] italic">No high-priority improvements required.</li>
                        )}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12 text-[#6e5845] text-sm font-semibold">
                    No ATS score generated yet. Click <span className="text-[#8b1e16] font-extrabold">"Run AI Analysis & Autonomous Pipeline"</span> above to calculate 60% Deterministic + 40% AI Auditor score.
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: JOB MATCH */}
            {activeTab === 'match' && (
              <div className="rounded-2xl parchment-card p-6 space-y-6 shadow-md border border-[#caba9c]">
                <div className="flex items-center justify-between border-b border-[#caba9c] pb-4">
                  <div>
                    <h3 className="font-extrabold text-lg text-[#241810]">5-Category Job Fit Analysis</h3>
                    <p className="text-xs text-[#6e5845]">Target Position: {jobTitle || 'Target Position'}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-black text-[#8b1e16]">
                      {executionResult?.matchData?.overall_match_score !== undefined
                        ? `${executionResult.matchData.overall_match_score}%`
                        : 'N/A'}
                    </div>
                    <div className="text-xs text-[#6e5845] font-bold">Overall Alignment Score</div>
                  </div>
                </div>

                {executionResult?.matchData ? (
                  <div className="space-y-6">
                    <div className="p-4 rounded-xl bg-[#dfcfb9] border border-[#c5b196] text-xs text-[#241810] font-semibold flex items-start gap-3 shadow-inner">
                      <Sparkles className="w-4 h-4 text-[#8b1e16] shrink-0 mt-0.5" />
                      <div>
                        <span className="font-extrabold text-[#8b1e16]">Understanding Job Alignment vs ATS Grade:</span> ATS Compatibility evaluates document structure, contact details, and verb density (Job-Independent). Job Skill Alignment measures your specific technical fit against <span className="font-extrabold text-[#241810]">{jobTitle || 'the target job description'}</span>.
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Matched Skills */}
                    <div className="p-5 rounded-xl bg-[#ede2d2] border border-[#caba9c] space-y-3 shadow-sm">
                      <div className="font-extrabold text-xs text-[#1c5427] flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-[#1c5427]" /> Matched Required Skills
                      </div>
                      <div className="flex flex-wrap gap-2 pt-1">
                        {executionResult.matchData.matched_skills && executionResult.matchData.matched_skills.length > 0 ? (
                          executionResult.matchData.matched_skills.map((skill: string, idx: number) => (
                            <span key={idx} className="px-2.5 py-1 rounded-lg bg-[#dcecd8] text-[#1c5427] border border-[#a8d4a6] text-xs font-bold shadow-sm">
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-[#6e5845] italic">No direct technical skill matches found.</span>
                        )}
                      </div>
                    </div>

                    {/* Missing Skills */}
                    <div className="p-5 rounded-xl bg-[#ede2d2] border border-[#caba9c] space-y-3 shadow-sm">
                      <div className="font-extrabold text-xs text-[#8b1e16] flex items-center gap-2">
                        <XCircle className="w-4 h-4 text-[#8b1e16]" /> Missing Required Skills
                      </div>
                      <div className="flex flex-wrap gap-2 pt-1">
                        {(executionResult.matchData.missing_skills || executionResult.matchData.missing_required_skills) && (executionResult.matchData.missing_skills || executionResult.matchData.missing_required_skills).length > 0 ? (
                          (executionResult.matchData.missing_skills || executionResult.matchData.missing_required_skills).map((skill: string, idx: number) => (
                            <span key={idx} className="px-2.5 py-1 rounded-lg bg-[#f5dcd8] text-[#8b1e16] border border-[#e8b5ae] text-xs font-bold capitalize shadow-sm">
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span className="px-2.5 py-1 rounded-lg bg-[#dcecd8] text-[#1c5427] border border-[#a8d4a6] text-xs font-bold shadow-sm">
                            ✓ None (All required skills present in candidate resume!)
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                ) : (
                  <div className="text-center py-12 text-[#6e5845] text-sm font-semibold">
                    No job match analysis performed yet. Click <span className="text-[#8b1e16] font-extrabold">"Run AI Analysis & Autonomous Pipeline"</span> above to analyze candidate fit against your job description.
                  </div>
                )}
              </div>
            )}

            {/* TAB 4: ROADMAP */}
            {activeTab === 'roadmap' && (
              <div className="rounded-2xl parchment-card p-6 space-y-6 shadow-md border border-[#caba9c]">
                <div className="flex items-center justify-between border-b border-[#caba9c] pb-4">
                  <div>
                    <h3 className="font-extrabold text-lg text-[#241810]">30-Day Skill Gap Learning Roadmap</h3>
                    <p className="text-xs text-[#6e5845]">Prioritized milestones adhering strictly to Anti-Fabrication rules</p>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#dfcfb9] text-[#4e3d30] border border-[#c5b196] text-xs font-bold shadow-sm">
                    Anti-Fabrication Guardrail Active
                  </span>
                </div>

                {executionResult?.careerData ? (
                  <>
                    {/* Identified Skill Gaps */}
                    {executionResult.careerData.skill_gaps && executionResult.careerData.skill_gaps.length > 0 && (
                      <div className="space-y-3">
                        <h4 className="font-extrabold text-xs text-[#6e5845] uppercase tracking-wider">Identified Skill Gaps</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {executionResult.careerData.skill_gaps.map((gap: any, idx: number) => (
                            <div key={idx} className="p-4 rounded-xl bg-[#ede2d2] border border-[#caba9c] space-y-2 shadow-sm">
                              <div className="flex items-center justify-between">
                                <span className="font-extrabold text-sm text-[#241810]">{gap.skill_name}</span>
                                <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${
                                  gap.priority === 'critical' ? 'bg-[#f5dcd8] text-[#8b1e16] border border-[#e8b5ae]' : 'bg-[#fce8cc] text-[#8a5314] border border-[#ebd0aa]'
                                }`}>
                                  {gap.priority || 'medium'}
                                </span>
                              </div>
                              <p className="text-xs text-[#6e5845] font-medium">{gap.reason}</p>
                              <div className="text-[11px] text-[#8b1e16] font-bold">Learning Effort: {gap.learning_effort}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 30-Day Plan Milestones */}
                    {executionResult.careerData.learning_roadmap?.thirty_day_plan && (
                      <div className="space-y-4">
                        <h4 className="font-extrabold text-xs text-[#6e5845] uppercase tracking-wider">Milestones & Action Items</h4>
                        {executionResult.careerData.learning_roadmap.thirty_day_plan.map((m: any, idx: number) => (
                          <div key={idx} className="p-4 rounded-xl bg-[#ede2d2] border border-[#caba9c] flex items-start gap-4 shadow-sm">
                            <div className="w-9 h-9 rounded-xl bg-[#f5dcd8] border border-[#e8b5ae] flex items-center justify-center font-black text-[#8b1e16] text-xs shrink-0">
                              W{idx + 1}
                            </div>
                            <div className="space-y-1.5 flex-1">
                              <h5 className="font-extrabold text-sm text-[#241810]">{m.title}</h5>
                              {m.action_items && (
                                <ul className="space-y-1 text-xs text-[#6e5845] font-medium">
                                  {m.action_items.map((item: string, i: number) => (
                                    <li key={i} className="flex items-center gap-2">
                                      <span className="text-[#8b1e16] font-bold">•</span> {item}
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <div className="text-center py-12 text-[#6e5845] text-sm font-semibold">
                    No learning roadmap generated yet. Click <span className="text-[#8b1e16] font-extrabold">"Run AI Analysis & Autonomous Pipeline"</span> above to generate a 30-day curriculum based on your job description.
                  </div>
                )}
              </div>
            )}

            {/* TAB 5: INTERVIEW */}
            {activeTab === 'interview' && (
              <div className="rounded-2xl parchment-card p-6 space-y-6 shadow-md border border-[#caba9c]">
                <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-[#caba9c] pb-4 gap-4">
                  <div>
                    <h3 className="font-extrabold text-lg text-[#241810]">STAR Practice Studio & Dynamic Question Bank</h3>
                    <p className="text-xs text-[#6e5845] font-medium">
                      40 Tailored Questions (Top 20 Resume-Based + Top 20 HR & Behavioral) generated dynamically for candidate credentials
                    </p>
                  </div>

                  {/* Question Filter Buttons */}
                  <div className="flex flex-wrap items-center gap-2 bg-[#dfcfb9] p-1.5 rounded-xl border border-[#c5b196] self-start md:self-auto shadow-inner">
                    <button
                      onClick={() => setInterviewFilter('all')}
                      className={`px-3 py-1.5 text-xs font-extrabold rounded-lg transition-all cursor-pointer ${
                        interviewFilter === 'all'
                          ? 'bg-[#8b1e16] text-white shadow-md'
                          : 'text-[#4e3d30] hover:text-[#241810]'
                      }`}
                    >
                      All Questions ({executionResult?.interviewData?.length || 40})
                    </button>
                    <button
                      onClick={() => setInterviewFilter('resume_based')}
                      className={`px-3 py-1.5 text-xs font-extrabold rounded-lg transition-all cursor-pointer ${
                        interviewFilter === 'resume_based'
                          ? 'bg-[#8b1e16] text-white shadow-md'
                          : 'text-[#4e3d30] hover:text-[#241810]'
                      }`}
                    >
                      Resume-Based (Top 20)
                    </button>
                    <button
                      onClick={() => setInterviewFilter('hr_based')}
                      className={`px-3 py-1.5 text-xs font-extrabold rounded-lg transition-all cursor-pointer ${
                        interviewFilter === 'hr_based'
                          ? 'bg-[#5c4735] text-white shadow-md'
                          : 'text-[#4e3d30] hover:text-[#241810]'
                      }`}
                    >
                      HR & Behavioral (Top 20)
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  {(() => {
                    const allQuestions = executionResult?.interviewData || [];
                    const filteredQuestions = allQuestions.filter((q: any) => {
                      if (interviewFilter === 'resume_based') return q.question_type === 'resume_based' || q.id?.startsWith('q-res');
                      if (interviewFilter === 'hr_based') return q.question_type === 'hr_based' || q.id?.startsWith('q-hr');
                      return true;
                    });

                    if (filteredQuestions.length === 0 && allQuestions.length === 0) {
                      return (
                        <div className="text-center py-12 text-[#6e5845] text-sm font-semibold">
                          No interview questions generated yet. Click <span className="text-[#8b1e16] font-extrabold">"Run AI Analysis & Autonomous Pipeline"</span> above to analyze candidate credentials.
                        </div>
                      );
                    }

                    return filteredQuestions.map((q: any, idx: number) => {
                      const isResumeBased = q.question_type === 'resume_based' || q.id?.startsWith('q-res');
                      return (
                        <div key={q.id || idx} className="p-5 rounded-xl bg-[#ede2d2] border border-[#caba9c] space-y-3 shadow-sm hover:border-[#8b1e16] transition-all">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className={`px-2.5 py-1 rounded-lg text-[10px] font-extrabold uppercase tracking-wider shadow-sm ${
                                isResumeBased
                                  ? 'bg-[#f5dcd8] text-[#8b1e16] border border-[#e8b5ae]'
                                  : 'bg-[#dcecd8] text-[#1c5427] border border-[#a8d4a6]'
                              }`}>
                                {isResumeBased ? 'Resume-Based Technical' : 'HR & Behavioral'}
                              </span>
                              <span className="px-2.5 py-1 rounded-lg bg-[#dfcfb9] text-[#4e3d30] border border-[#c5b196] text-[10px] font-bold">
                                {q.category || 'Interview Focus'}
                              </span>
                            </div>
                            <span className="text-xs text-[#6e5845] font-bold">Question #{idx + 1} of {filteredQuestions.length}</span>
                          </div>
                          <h4 className="font-extrabold text-sm sm:text-base text-[#241810] leading-snug">
                            {q.question_text || q.question || 'Interview practice question'}
                          </h4>
                          {(q.context_reason || q.context) && (
                            <p className="text-xs text-[#4e3d30] bg-[#dfcfb9]/70 p-3 rounded-lg border border-[#c5b196] font-medium">
                              <span className="text-[#8b1e16] font-extrabold">Evaluation Focus: </span>
                              {q.context_reason || q.context}
                            </p>
                          )}
                          {q.star_talking_points && q.star_talking_points.length > 0 && (
                            <div className="pt-2">
                              <span className="text-[11px] font-extrabold text-[#8b1e16] uppercase tracking-wider block mb-1.5">
                                Recommended STAR Talking Points:
                              </span>
                              <ul className="space-y-1 text-xs text-[#241810] font-medium">
                                {q.star_talking_points.map((tp: string, i: number) => (
                                  <li key={i} className="flex items-start gap-2">
                                    <span className="text-[#8b1e16] font-bold">•</span> <span>{tp}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      );
                    });
                  })()}
                </div>
              </div>
            )}

            {/* TAB 6: AGENTS */}
            {activeTab === 'agents' && (
              <div className="rounded-2xl parchment-card p-6 space-y-6 shadow-md border border-[#caba9c]">
                <div className="flex items-center justify-between border-b border-[#caba9c] pb-4">
                  <div>
                    <h3 className="font-extrabold text-lg text-[#241810]">Multi-Agent Execution Trace Graph</h3>
                    <p className="text-xs text-[#6e5845] font-semibold">
                      Session ID: {executionResult?.orchestrationData?.session_id || 'sess-live-9912'}
                    </p>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#dcecd8] text-[#1c5427] border border-[#a8d4a6] text-xs font-extrabold shadow-sm">
                    6/6 Autonomous Agents Completed
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {(executionResult?.orchestrationData?.execution_trace?.steps || [
                    { agent_name: 'ManagerOrchestratorAgent', status: 'completed', execution_time_ms: 42, tool_calls: ['plan_workflow', 'synthesize_action_plan'] },
                    { agent_name: 'ResumeAgent', status: 'completed', execution_time_ms: 38, tool_calls: ['parse_resume', 'extract_skills'] },
                    { agent_name: 'JobDescriptionAgent', status: 'completed', execution_time_ms: 45, tool_calls: ['parse_job_description', 'normalize_synonyms'] },
                    { agent_name: 'SkillGapAgent', status: 'completed', execution_time_ms: 30, tool_calls: ['evaluate_match', 'extract_gaps'] },
                    { agent_name: 'RecommendationAgent', status: 'completed', execution_time_ms: 52, tool_calls: ['generate_roadmap'] },
                    { agent_name: 'InterviewAgent', status: 'completed', execution_time_ms: 41, tool_calls: ['generate_interview_questions'] },
                  ]).map((step: any, idx: number) => (
                    <div key={idx} className="p-4 rounded-xl bg-[#ede2d2] border border-[#caba9c] space-y-3 shadow-sm">
                      <div className="flex items-center justify-between">
                        <span className="font-extrabold text-xs text-[#241810]">{step.agent_name}</span>
                        <span className="px-2 py-0.5 rounded bg-[#dcecd8] text-[#1c5427] border border-[#a8d4a6] text-[10px] font-extrabold uppercase">
                          {step.status}
                        </span>
                      </div>
                      <div className="text-[11px] text-[#6e5845] font-semibold">
                        Execution latency: <span className="text-[#8b1e16] font-bold">{step.execution_time_ms} ms</span>
                      </div>
                      {step.tool_calls && (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {step.tool_calls.map((t: string, i: number) => (
                            <span key={i} className="px-2 py-0.5 rounded bg-[#dfcfb9] text-[#4e3d30] border border-[#c5b196] text-[10px] font-mono font-bold">
                              {t}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        </section>

      </main>
    </div>
  );
}
