'use client';

import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Award,
  FileText,
  BarChart3,
  TrendingUp,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
} from 'lucide-react';

interface CategoryScore {
  category_name: string;
  score: number;
  weight: number;
  description: string;
}

interface ScoringReason {
  type: 'positive' | 'negative' | 'warning';
  message: string;
  category: string;
}

interface ATSAnalysisData {
  overall_score: number;
  ats_compatibility_score: number;
  category_scores: CategoryScore[];
  reasons: ScoringReason[];
  strengths: string[];
  weaknesses: string[];
  warnings: string[];
  actionable_improvements: string[];
  scoring_formula_explanation: string;
}

export default function ResumeAnalysisDashboard() {
  // Mock data demonstration for dashboard UI preview
  const [analysis] = useState<ATSAnalysisData>({
    overall_score: 84,
    ats_compatibility_score: 88,
    category_scores: [
      { category_name: 'ATS Compatibility', score: 88, weight: 0.25, description: 'Estimates structural compatibility with standard Applicant Tracking Systems.' },
      { category_name: 'Content Quality', score: 85, weight: 0.20, description: 'Evaluates action verb usage, clarity, and readability.' },
      { category_name: 'Skills', score: 90, weight: 0.15, description: 'Evaluates diversity and categorization of technical and soft skills.' },
      { category_name: 'Experience', score: 80, weight: 0.15, description: 'Evaluates quantified metrics, bullet achievements, and career depth.' },
      { category_name: 'Projects', score: 85, weight: 0.10, description: 'Evaluates project descriptions, technologies, and URLs.' },
      { category_name: 'Education', score: 85, weight: 0.05, description: 'Evaluates degree, institution, and major completeness.' },
      { category_name: 'Completeness', score: 95, weight: 0.10, description: 'Evaluates presence of standard required resume sections.' },
    ],
    reasons: [
      { type: 'positive', message: 'Identified 6 strong action verbs in experience bullets.', category: 'Content Quality' },
      { type: 'positive', message: 'Found 3 quantified performance metrics (percentages/metrics).', category: 'Experience' },
      { type: 'warning', message: 'Contains minor formatting risks in header section.', category: 'ATS Compatibility' },
    ],
    strengths: [
      'Strong usage of high-impact action verbs (Architected, Spearheaded, Engineered, Optimized).',
      'Excellent quantified metrics and achievements (40% latency reduction, $2M ARR).',
      'Diverse technical skill presentation (Python, FastAPI, Next.js, PostgreSQL).',
      'Complete resume structure with all major professional sections.',
    ],
    weaknesses: [
      'Projects section could include explicit live demo or GitHub links.',
    ],
    warnings: [
      'Avoid using multi-column tables in header which can distort legacy ATS parsers.',
    ],
    actionable_improvements: [
      'Add customized LinkedIn and GitHub profile URLs to increase recruiter verification.',
      'Group technical skills into explicit sub-categories (Frameworks, Databases, Cloud & DevOps).',
      'Enhance project entries with bullet points detailing specific personal accomplishments.',
    ],
    scoring_formula_explanation:
      'Overall Score (0-100) is calculated as a weighted average across 7 categories: ATS Compatibility (25%), Content Quality (20%), Skills (15%), Experience (15%), Projects (10%), Education (5%), and Completeness (10%).',
  });

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#10b981'; // Green
    if (score >= 60) return '#f59e0b'; // Amber
    return '#ef4444'; // Red
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#090d16', color: '#f3f4f6', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        
        {/* Header Bar */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, background: 'linear-gradient(135deg, #60a5fa 0%, #a855f7 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                AGENTX
              </span>
              <span style={{ padding: '0.25rem 0.6rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(96, 165, 250, 0.1)', color: '#60a5fa', border: '1px solid rgba(96, 165, 250, 0.3)' }}>
                Resume Intelligence Engine
              </span>
            </div>
            <p style={{ color: '#9ca3af', fontSize: '0.95rem', margin: 0 }}>
              Explainable ATS Compatibility & Quality Audit Dashboard
            </p>
          </div>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.6rem 1.2rem', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.15)', background: 'rgba(255, 255, 255, 0.05)', color: '#fff', fontSize: '0.9rem', fontWeight: 600, cursor: 'pointer' }}>
              <FileText size={16} /> Re-parse Resume
            </button>
          </div>
        </header>

        {/* Hero Score Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
          
          {/* Overall Score Card */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '4px', background: `linear-gradient(90deg, ${getScoreColor(analysis.overall_score)}, #a855f7)` }} />
            <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1.5rem' }}>
              Overall Resume Quality
            </h3>
            <div style={{ position: 'relative', width: '140px', height: '140px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
              <svg width="140" height="140" viewBox="0 0 140 140">
                <circle cx="70" cy="70" r="58" fill="none" stroke="rgba(255, 255, 255, 0.08)" strokeWidth="12" />
                <circle
                  cx="70"
                  cy="70"
                  r="58"
                  fill="none"
                  stroke={getScoreColor(analysis.overall_score)}
                  strokeWidth="12"
                  strokeDasharray="364.4"
                  strokeDashoffset={364.4 - (364.4 * analysis.overall_score) / 100}
                  strokeLinecap="round"
                  transform="rotate(-90 70 70)"
                  style={{ transition: 'stroke-dashoffset 1s ease-out' }}
                />
              </svg>
              <div style={{ position: 'absolute', textAlign: 'center' }}>
                <span style={{ fontSize: '2.75rem', fontWeight: 800, color: '#fff' }}>{analysis.overall_score}</span>
                <span style={{ fontSize: '1.1rem', color: '#9ca3af' }}>/100</span>
              </div>
            </div>
            <p style={{ color: '#10b981', fontSize: '0.9rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.4rem', margin: 0 }}>
              <TrendingUp size={16} /> Strong Competitive Candidate Profile
            </p>
          </div>

          {/* ATS Compatibility Estimate Card */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0 }}>
                    ATS Compatibility Estimate
                  </h3>
                  <span style={{ fontSize: '0.75rem', color: '#6b7280' }}>Simulated Applicant Tracking System Parse Fit</span>
                </div>
                <ShieldCheck size={28} color="#60a5fa" />
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', marginBottom: '1rem' }}>
                <span style={{ fontSize: '3rem', fontWeight: 800, color: getScoreColor(analysis.ats_compatibility_score) }}>
                  {analysis.ats_compatibility_score}%
                </span>
                <span style={{ color: '#9ca3af', fontSize: '0.95rem', fontWeight: 600 }}>High Parse Rate</span>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#d1d5db', lineHeight: 1.5, margin: 0 }}>
                Your document structure, contact details, and heading formatting align cleanly with corporate ATS scanners (Workday, Greenhouse, Lever).
              </p>
            </div>
            <div style={{ marginTop: '1.5rem', padding: '0.75rem 1rem', background: 'rgba(96, 165, 250, 0.08)', borderRadius: '8px', border: '1px solid rgba(96, 165, 250, 0.2)', fontSize: '0.8rem', color: '#93c5fd' }}>
              ℹ Disclaimer: Scores represent an estimated benchmark, not proprietary ATS guarantee.
            </div>
          </div>
        </div>

        {/* Category Breakdown Section */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BarChart3 size={20} color="#a855f7" /> Explainable Category Scores
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
            {analysis.category_scores.map((cat, idx) => (
              <div key={idx} style={{ background: 'rgba(0, 0, 0, 0.2)', padding: '1rem 1.25rem', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.95rem', color: '#f3f4f6' }}>{cat.category_name}</span>
                  <span style={{ fontWeight: 700, color: getScoreColor(cat.score) }}>{cat.score}/100</span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '4px', overflow: 'hidden', marginBottom: '0.5rem' }}>
                  <div style={{ width: `${cat.score}%`, height: '100%', background: getScoreColor(cat.score), borderRadius: '4px', transition: 'width 0.8s ease' }} />
                </div>
                <span style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{cat.description}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Explainable Strengths, Weaknesses, Warnings Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
          
          {/* Strengths Card */}
          <div style={{ background: 'rgba(16, 185, 129, 0.04)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '16px', padding: '1.75rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#34d399', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle2 size={20} /> Key Strengths (+)
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {analysis.strengths.map((s, idx) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem', fontSize: '0.9rem', color: '#e5e7eb', lineHeight: 1.4 }}>
                  <span style={{ color: '#34d399', fontWeight: 700 }}>+</span> {s}
                </li>
              ))}
            </ul>
          </div>

          {/* Weaknesses & Warnings Card */}
          <div style={{ background: 'rgba(239, 68, 68, 0.04)', border: '1px solid rgba(239, 68, 68, 0.2)', borderRadius: '16px', padding: '1.75rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f87171', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <XCircle size={20} /> Areas to Improve (-)
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {analysis.weaknesses.map((w, idx) => (
                <li key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem', fontSize: '0.9rem', color: '#e5e7eb', lineHeight: 1.4 }}>
                  <span style={{ color: '#f87171', fontWeight: 700 }}>-</span> {w}
                </li>
              ))}
              {analysis.warnings.map((warn, idx) => (
                <li key={`warn-${idx}`} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem', fontSize: '0.9rem', color: '#fbbf24', lineHeight: 1.4 }}>
                  <AlertTriangle size={16} style={{ flexShrink: 0, marginTop: '2px' }} /> {warn}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Actionable Improvements Timeline */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Zap size={20} color="#f59e0b" /> Prioritized Actionable Improvements
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {analysis.actionable_improvements.map((item, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'rgba(255, 255, 255, 0.02)', padding: '1rem 1.25rem', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <span style={{ width: '28px', height: '28px', borderRadius: '50%', background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b', fontWeight: 700, fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  {idx + 1}
                </span>
                <span style={{ fontSize: '0.95rem', color: '#e5e7eb', flexGrow: 1 }}>{item}</span>
                <ArrowRight size={18} color="#6b7280" />
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
