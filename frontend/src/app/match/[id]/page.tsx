'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Target,
  ArrowLeft,
  Briefcase,
  Layers,
  ArrowRight,
  TrendingUp,
  Cpu,
  BookOpen,
} from 'lucide-react';

interface JobMatchData {
  overall_match_score: number;
  required_skills_match_score: number;
  preferred_skills_match_score: number;
  experience_match_score: number;
  education_match_score: number;
  project_relevance_score: number;
  matched_skills: string[];
  missing_skills: string[];
  weak_skills: string[];
  keyword_gaps: string[];
  actionable_gap_recommendations: string[];
  matching_formula_explanation: string;
}

export default function JobMatchDashboard() {
  const [match, setMatch] = useState<JobMatchData>({
    overall_match_score: 78,
    required_skills_match_score: 80,
    preferred_skills_match_score: 70,
    experience_match_score: 85,
    education_match_score: 90,
    project_relevance_score: 80,
    matched_skills: ['python', 'fastapi', 'postgresql', 'docker', 'git'],
    missing_skills: ['kubernetes', 'aws'],
    weak_skills: ['redis', 'agile'],
    keyword_gaps: ['kubernetes', 'aws'],
    actionable_gap_recommendations: [
      "Acquire or explicitly list proficiency in 'Kubernetes' to fulfill key JD requirements.",
      "Acquire or explicitly list proficiency in 'Aws' to fulfill key JD requirements.",
    ],
    matching_formula_explanation:
      'Overall Match Score (0-100) is calculated using a weighted formula: Required Skills Match (40%), Preferred Skills Match (15%), Work Experience (25%), Project Relevance (10%), and Education (10%).',
  });

  const getScoreColor = (score: number) => {
    if (score >= 75) return '#10b981'; // Green
    if (score >= 50) return '#f59e0b'; // Amber
    return '#ef4444'; // Red
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#090d16', color: '#f3f4f6', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>

        {/* Back Navigation Bar */}
        <div style={{ marginBottom: '1.5rem' }}>
          <Link
            href="/"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              color: '#38bdf8',
              fontSize: '0.9rem',
              fontWeight: 600,
              textDecoration: 'none',
              padding: '0.5rem 1rem',
              background: 'rgba(56, 189, 248, 0.1)',
              borderRadius: '8px',
              border: '1px solid rgba(56, 189, 248, 0.2)',
            }}
          >
            ← Back to Live Application Dashboard
          </Link>
        </div>

        {/* Header Bar */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                AGENTX
              </span>
              <span style={{ padding: '0.25rem 0.6rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(16, 185, 129, 0.1)', color: '#10b981', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                Job-Fit Intelligence Platform
              </span>
            </div>
            <p style={{ color: '#9ca3af', fontSize: '0.95rem', margin: 0 }}>
              Job Description Match Analysis Engine
            </p>
          </div>
        </header>

        {/* Hero Score Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
          
          {/* Overall Match Score Card */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#9ca3af', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1.5rem' }}>
              OVERALL JOB-FIT MATCH
            </h3>
            <div style={{ position: 'relative', width: '140px', height: '140px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
              <svg width="140" height="140" viewBox="0 0 140 140">
                <circle cx="70" cy="70" r="58" fill="none" stroke="rgba(255, 255, 255, 0.08)" strokeWidth="12" />
                <circle
                  cx="70"
                  cy="70"
                  r="58"
                  fill="none"
                  stroke={getScoreColor(match.overall_match_score)}
                  strokeWidth="12"
                  strokeDasharray="364.4"
                  strokeDashoffset={364.4 - (364.4 * match.overall_match_score) / 100}
                  strokeLinecap="round"
                  transform="rotate(-90 70 70)"
                />
              </svg>
              <div style={{ position: 'absolute', fontSize: '2rem', fontWeight: 800, color: getScoreColor(match.overall_match_score) }}>
                {match.overall_match_score}%
              </div>
            </div>
            <p style={{ color: '#10b981', fontSize: '0.85rem', fontWeight: 600, margin: 0 }}>
              Strong Alignment with Candidate Credentials
            </p>
          </div>

          {/* Category Scores Breakdown */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem' }}>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers style={{ width: '18px', height: '18px', color: '#60a5fa' }} />
              Match Category Breakdown
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                  <span style={{ color: '#d1d5db' }}>Required Skills (40%)</span>
                  <span style={{ fontWeight: 700, color: '#10b981' }}>{match.required_skills_match_score}%</span>
                </div>
                <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${match.required_skills_match_score}%`, background: '#10b981', borderRadius: '4px' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                  <span style={{ color: '#d1d5db' }}>Work Experience (25%)</span>
                  <span style={{ fontWeight: 700, color: '#10b981' }}>{match.experience_match_score}%</span>
                </div>
                <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${match.experience_match_score}%`, background: '#10b981', borderRadius: '4px' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                  <span style={{ color: '#d1d5db' }}>Preferred Skills (15%)</span>
                  <span style={{ fontWeight: 700, color: '#f59e0b' }}>{match.preferred_skills_match_score}%</span>
                </div>
                <div style={{ height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${match.preferred_skills_match_score}%`, background: '#f59e0b', borderRadius: '4px' }} />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Explainable Skill Comparison */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Target style={{ width: '20px', height: '20px', color: '#10b981' }} />
            Explainable Skill Comparison
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
            {/* Matched */}
            <div style={{ background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '12px', padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', fontWeight: 700, fontSize: '0.9rem', marginBottom: '1rem' }}>
                <CheckCircle2 style={{ width: '18px', height: '18px' }} />
                Matched Skills ({match.matched_skills.length})
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {match.matched_skills.map((s, idx) => (
                  <span key={idx} style={{ padding: '0.35rem 0.75rem', borderRadius: '6px', background: 'rgba(16, 185, 129, 0.15)', color: '#6ee7b7', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    + {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Missing */}
            <div style={{ background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.2)', borderRadius: '12px', padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ef4444', fontWeight: 700, fontSize: '0.9rem', marginBottom: '1rem' }}>
                <XCircle style={{ width: '18px', height: '18px' }} />
                Missing Required Skills ({match.missing_skills.length})
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {match.missing_skills.map((s, idx) => (
                  <span key={idx} style={{ padding: '0.35rem 0.75rem', borderRadius: '6px', background: 'rgba(239, 68, 68, 0.15)', color: '#fca5a5', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    - {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Weak / Preferred */}
            <div style={{ background: 'rgba(245, 158, 11, 0.05)', border: '1px solid rgba(245, 158, 11, 0.2)', borderRadius: '12px', padding: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', fontWeight: 700, fontSize: '0.9rem', marginBottom: '1rem' }}>
                <AlertTriangle style={{ width: '18px', height: '18px' }} />
                Weak / Preferred Gaps ({match.weak_skills.length})
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {match.weak_skills.map((s, idx) => (
                  <span key={idx} style={{ padding: '0.35rem 0.75rem', borderRadius: '6px', background: 'rgba(245, 158, 11, 0.15)', color: '#fde047', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
                    ! {s}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Actionable Recommendations */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <TrendingUp style={{ width: '20px', height: '20px', color: '#60a5fa' }} />
            Actionable Gap Recommendations
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {match.actionable_gap_recommendations.map((rec, idx) => (
              <div key={idx} style={{ padding: '1rem', background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.05)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.9rem', color: '#d1d5db' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <span style={{ width: '24px', height: '24px', borderRadius: '50%', background: 'rgba(96, 165, 250, 0.15)', color: '#60a5fa', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 800 }}>
                    {idx + 1}
                  </span>
                  <span>{rec}</span>
                </div>
                <ArrowRight style={{ width: '16px', height: '16px', color: '#60a5fa' }} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
