'use client';

import React, { useState } from 'react';
import {
  Compass,
  AlertOctagon,
  AlertTriangle,
  CheckCircle,
  Calendar,
  Clock,
  ArrowRight,
  ShieldCheck,
  BookOpen,
  Zap,
} from 'lucide-react';

interface SkillGap {
  skill_name: string;
  priority: 'critical' | 'medium' | 'low';
  jd_importance: string;
  learning_effort: string;
  reason: string;
}

interface SpecificRecommendation {
  target_area: string;
  action_title: string;
  detailed_guidance: string;
}

interface Milestone {
  timeframe: string;
  title: string;
  focus_skills: string[];
  action_items: string[];
  estimated_hours: number;
}

export default function CareerInsightsDashboard() {
  const [gaps] = useState<SkillGap[]>([
    {
      skill_name: 'Kubernetes & Container Orchestration',
      priority: 'critical',
      jd_importance: 'High',
      learning_effort: '2 weeks',
      reason: 'Required for modern cloud-native backend & DevOps engineering roles.',
    },
    {
      skill_name: 'AWS Cloud Architecture (EC2, S3, IAM, ECS)',
      priority: 'critical',
      jd_importance: 'High',
      learning_effort: '3 weeks',
      reason: 'High recruiter demand for candidates with hands-on cloud deployment experience.',
    },
    {
      skill_name: 'Redis In-Memory Caching',
      priority: 'medium',
      jd_importance: 'Medium',
      learning_effort: '1 week',
      reason: 'Improves API performance and caching layer architecture.',
    },
  ]);

  const [recommendations] = useState<SpecificRecommendation[]>([
    {
      target_area: 'resume',
      action_title: 'Quantify Work Experience Impact',
      detailed_guidance:
        'Add measurable outcomes to your TechCorp work experience bullet points, such as latency reduction %, query optimization %, active users served, or deployment scale if truthful. Do not invent fake numbers; use approximate truthful metrics from your projects.',
    },
    {
      target_area: 'project',
      action_title: 'Build a Production Cloud Deployment Project',
      detailed_guidance:
        'Build an open-source demonstration project featuring FastAPI backend services, Docker containerization, PostgreSQL database, and automated GitHub Actions CI/CD pipeline.',
    },
    {
      target_area: 'job_prep',
      action_title: 'Prepare System Design & Scenario Talking Points',
      detailed_guidance:
        'Practice explaining architecture tradeoffs (SQL vs NoSQL, Caching, Event-driven architecture) using the STAR format.',
    },
  ]);

  const [milestones] = useState<Milestone[]>([
    {
      timeframe: 'week_1',
      title: 'Week 1: Advanced Docker & Containerization',
      focus_skills: ['Docker', 'Multi-stage Builds'],
      action_items: ['Build multi-container dev environment', 'Optimize Docker image size'],
      estimated_hours: 10,
    },
    {
      timeframe: 'week_2',
      title: 'Week 2: Kubernetes Fundamentals & Pod Orchestration',
      focus_skills: ['Kubernetes', 'K8s Manifests'],
      action_items: ['Set up local Minikube cluster', 'Write K8s deployment & service manifests'],
      estimated_hours: 12,
    },
    {
      timeframe: 'week_3',
      title: 'Week 3: AWS Cloud Infrastructure & IAM Security',
      focus_skills: ['AWS EC2', 'S3', 'IAM'],
      action_items: ['Deploy containerized API to AWS ECS/EC2', 'Configure S3 bucket storage & IAM policies'],
      estimated_hours: 15,
    },
    {
      timeframe: 'week_4',
      title: 'Week 4: CI/CD Automation & Production Hardening',
      focus_skills: ['GitHub Actions', 'CI/CD'],
      action_items: ['Build automated test & deploy pipeline on main branch push', 'Integrate structured logging'],
      estimated_hours: 12,
    },
  ]);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#090d16', color: '#f3f4f6', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>

        {/* Header Bar */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, background: 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                AGENTX
              </span>
              <span style={{ padding: '0.25rem 0.6rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(168, 85, 247, 0.1)', color: '#c084fc', border: '1px solid rgba(168, 85, 247, 0.3)' }}>
                Career & Skill Intelligence Engine
              </span>
            </div>
            <p style={{ color: '#9ca3af', fontSize: '0.95rem', margin: 0 }}>
              Prioritized Skill Gaps & Personalized 30-Day Learning Roadmap
            </p>
          </div>
        </header>

        {/* Skill Gap Priority Section */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Compass size={22} color="#a855f7" /> Prioritized Skill Gap Analysis
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
            {gaps.map((gap, idx) => {
              const isCritical = gap.priority === 'critical';
              return (
                <div key={idx} style={{ background: isCritical ? 'rgba(239, 68, 68, 0.04)' : 'rgba(245, 158, 11, 0.04)', border: isCritical ? '1px solid rgba(239, 68, 68, 0.2)' : '1px solid rgba(245, 158, 11, 0.2)', borderRadius: '12px', padding: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                    <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', margin: 0 }}>{gap.skill_name}</h4>
                    <span style={{ padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', backgroundColor: isCritical ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)', color: isCritical ? '#f87171' : '#fbbf24' }}>
                      {gap.priority}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: '#d1d5db', lineHeight: 1.4, marginBottom: '1rem' }}>{gap.reason}</p>
                  <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem', color: '#9ca3af' }}>
                    <span>Importance: <strong style={{ color: '#fff' }}>{gap.jd_importance}</strong></span>
                    <span>Effort: <strong style={{ color: '#fff' }}>{gap.learning_effort}</strong></span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 30-Day Learning Roadmap Timeline */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Calendar size={22} color="#60a5fa" /> Personalized 30-Day Learning Curriculum
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem' }}>
            {milestones.map((m, idx) => (
              <div key={idx} style={{ background: 'rgba(0, 0, 0, 0.25)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '1.5rem', position: 'relative' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#60a5fa', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Step {idx + 1}</span>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', margin: '0.5rem 0 0.75rem 0' }}>{m.title}</h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', marginBottom: '1rem' }}>
                  {m.focus_skills.map((s, sIdx) => (
                    <span key={sIdx} style={{ padding: '0.15rem 0.4rem', borderRadius: '4px', background: 'rgba(96, 165, 250, 0.15)', color: '#93c5fd', fontSize: '0.7rem' }}>{s}</span>
                  ))}
                </div>
                <ul style={{ paddingLeft: '1rem', margin: 0, fontSize: '0.8rem', color: '#d1d5db', lineHeight: 1.5 }}>
                  {m.action_items.map((act, aIdx) => (
                    <li key={aIdx}>{act}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Specific Non-Generic Recommendations */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Zap size={22} color="#f59e0b" /> Actionable Resume & Project Guidance
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {recommendations.map((rec, idx) => (
              <div key={idx} style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.25rem', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <span style={{ padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', backgroundColor: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24' }}>
                    {rec.target_area}
                  </span>
                  <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', margin: 0 }}>{rec.action_title}</h4>
                </div>
                <p style={{ fontSize: '0.875rem', color: '#d1d5db', lineHeight: 1.5, margin: 0 }}>{rec.detailed_guidance}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
