'use client';

import React, { useState } from 'react';
import {
  Bot,
  CheckCircle2,
  Clock,
  Play,
  Layers,
  ChevronDown,
  ChevronRight,
  ShieldCheck,
  Zap,
  Code,
  Target,
  Calendar,
  MessageSquare,
} from 'lucide-react';

interface StepTrace {
  agent_name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  tool_calls: string[];
  execution_time_ms: number;
  input_payload: any;
  output_payload: any;
}

interface ActionPlan {
  user_goal: string;
  candidate_name: string;
  job_title: string;
  overall_match_score: number;
  ats_compatibility_score: number;
  matched_skills: string[];
  missing_skills: string[];
  executive_summary: string;
}

export default function MultiAgentOrchestratorDashboard() {
  const [expandedStep, setExpandedStep] = useState<number | null>(0);
  const [isRunning, setIsRunning] = useState<boolean>(false);

  const [traces] = useState<StepTrace[]>([
    {
      agent_name: 'ManagerOrchestrator',
      status: 'completed',
      tool_calls: ['plan_workflow', 'delegate_tasks'],
      execution_time_ms: 12,
      input_payload: { goal: 'Analyze resume against JD, identify gaps, build roadmap & prep interview' },
      output_payload: { plan: ['ResumeAgent', 'JobDescriptionAgent', 'SkillGapAgent', 'RecommendationAgent', 'InterviewAgent'] },
    },
    {
      agent_name: 'ResumeAgent',
      status: 'completed',
      tool_calls: ['tool_fetch_resume'],
      execution_time_ms: 45,
      input_payload: { resume_id: 'res-9912' },
      output_payload: { candidate_name: 'Alice Johnson', email: 'alice@example.com', skills: ['Python', 'FastAPI', 'Docker'] },
    },
    {
      agent_name: 'JobDescriptionAgent',
      status: 'completed',
      tool_calls: ['tool_parse_job'],
      execution_time_ms: 38,
      input_payload: { title: 'Senior Backend Engineer', has_raw_text: true },
      output_payload: { required_skills: ['python', 'fastapi', 'postgresql', 'kubernetes', 'aws'] },
    },
    {
      agent_name: 'SkillGapAgent',
      status: 'completed',
      tool_calls: ['tool_evaluate_match'],
      execution_time_ms: 52,
      input_payload: { resume_id: 'res-9912', job_id: 'job-4410' },
      output_payload: { overall_match_score: 78, matched_skills: ['python', 'fastapi'], missing_skills: ['kubernetes', 'aws'] },
    },
    {
      agent_name: 'RecommendationAgent',
      status: 'completed',
      tool_calls: ['tool_generate_roadmap'],
      execution_time_ms: 60,
      input_payload: { gaps: ['kubernetes', 'aws'] },
      output_payload: { thirty_day_plan_milestones: 4 },
    },
    {
      agent_name: 'InterviewAgent',
      status: 'completed',
      tool_calls: ['tool_generate_interview_questions'],
      execution_time_ms: 40,
      input_payload: { resume_id: 'res-9912' },
      output_payload: { questions_count: 5 },
    },
  ]);

  const [actionPlan] = useState<ActionPlan>({
    user_goal: 'Analyze my resume against this job, identify my gaps, create a learning plan, and prepare me for the interview.',
    candidate_name: 'Alice Johnson',
    job_title: 'Senior Backend Engineer',
    overall_match_score: 78,
    ats_compatibility_score: 88,
    matched_skills: ['python', 'fastapi', 'postgresql', 'docker'],
    missing_skills: ['kubernetes', 'aws'],
    executive_summary:
      'Multi-Agent Orchestration complete for candidate Alice Johnson targeting Senior Backend Engineer. Achieved 78% overall job match with 4 matched skills and 2 missing required skills. Personalized 30-day learning curriculum and 5-category interview question bank generated.',
  });

  const handleRunOrchestration = () => {
    setIsRunning(true);
    setTimeout(() => {
      setIsRunning(false);
    }, 800);
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#090d16', color: '#f3f4f6', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>

        {/* Header Bar */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, background: 'linear-gradient(135deg, #10b981 0%, #a855f7 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                AGENTX
              </span>
              <span style={{ padding: '0.25rem 0.6rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(16, 185, 129, 0.1)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                Multi-Agent Autonomous Orchestrator
              </span>
            </div>
            <p style={{ color: '#9ca3af', fontSize: '0.95rem', margin: 0 }}>
              Observable Agent Execution Graph & Integrated Final Career Action Plan
            </p>
          </div>
          <button
            onClick={handleRunOrchestration}
            disabled={isRunning}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem 1.5rem', borderRadius: '8px', border: 'none', background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)', color: '#fff', fontSize: '0.9rem', fontWeight: 700, cursor: 'pointer' }}
          >
            <Play size={16} /> {isRunning ? 'Orchestrating Agents...' : 'Run Goal Orchestration'}
          </button>
        </header>

        {/* User Goal Prompt Banner */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '1.5rem', marginBottom: '2.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(168, 85, 247, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            <Bot size={24} color="#c084fc" />
          </div>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', color: '#c084fc' }}>Active Goal</span>
            <p style={{ fontSize: '1rem', fontWeight: 600, color: '#fff', margin: 0 }}>"{actionPlan.user_goal}"</p>
          </div>
        </div>

        {/* Multi-Agent Pipeline Trace Graph */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem', marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Layers size={20} color="#60a5fa" /> Observable Execution Trace Graph
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {traces.map((trace, idx) => {
              const isExpanded = expandedStep === idx;
              return (
                <div key={idx} style={{ background: 'rgba(0, 0, 0, 0.25)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.08)', overflow: 'hidden' }}>
                  <div
                    onClick={() => setExpandedStep(isExpanded ? null : idx)}
                    style={{ padding: '1rem 1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <CheckCircle2 size={20} color="#34d399" />
                      <span style={{ fontWeight: 700, fontSize: '0.95rem', color: '#fff' }}>{trace.agent_name}</span>
                      <span style={{ fontSize: '0.75rem', color: '#9ca3af', background: 'rgba(255, 255, 255, 0.05)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                        {trace.execution_time_ms} ms
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 700, textTransform: 'uppercase' }}>{trace.status}</span>
                      {isExpanded ? <ChevronDown size={18} color="#9ca3af" /> : <ChevronRight size={18} color="#9ca3af" />}
                    </div>
                  </div>

                  {/* Trace Log Inspector Drawer */}
                  {isExpanded && (
                    <div style={{ padding: '1rem 1.25rem', borderTop: '1px solid rgba(255, 255, 255, 0.05)', background: 'rgba(0, 0, 0, 0.4)', fontSize: '0.85rem' }}>
                      <div style={{ marginBottom: '0.75rem' }}>
                        <strong style={{ color: '#60a5fa' }}>Executed Tools: </strong>
                        <span style={{ color: '#e5e7eb' }}>{trace.tool_calls.join(', ')}</span>
                      </div>
                      <div style={{ marginBottom: '0.75rem' }}>
                        <strong style={{ color: '#c084fc' }}>Input Payload: </strong>
                        <pre style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '0.5rem', borderRadius: '6px', color: '#9ca3af', margin: '0.25rem 0 0 0', fontSize: '0.75rem', overflowX: 'auto' }}>
                          {JSON.stringify(trace.input_payload, null, 2)}
                        </pre>
                      </div>
                      <div>
                        <strong style={{ color: '#34d399' }}>Output Payload: </strong>
                        <pre style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '0.5rem', borderRadius: '6px', color: '#9ca3af', margin: '0.25rem 0 0 0', fontSize: '0.75rem', overflowX: 'auto' }}>
                          {JSON.stringify(trace.output_payload, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Integrated Final Action Plan */}
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '2rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Zap size={20} color="#f59e0b" /> Integrated Final Career Action Plan
          </h3>
          <p style={{ fontSize: '0.9rem', color: '#d1d5db', lineHeight: 1.5, marginBottom: '1.5rem' }}>
            {actionPlan.executive_summary}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
            <div style={{ background: 'rgba(16, 185, 129, 0.05)', padding: '1.25rem', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
              <span style={{ fontSize: '0.8rem', color: '#34d399', fontWeight: 700 }}>Overall Job Match</span>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: '#fff', margin: '0.25rem 0' }}>{actionPlan.overall_match_score}%</div>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{actionPlan.matched_skills.length} Matched Skills</span>
            </div>

            <div style={{ background: 'rgba(239, 68, 68, 0.05)', padding: '1.25rem', borderRadius: '12px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
              <span style={{ fontSize: '0.8rem', color: '#f87171', fontWeight: 700 }}>Critical Skill Gaps</span>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: '#fff', margin: '0.25rem 0' }}>{actionPlan.missing_skills.length}</div>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af' }}>{actionPlan.missing_skills.join(', ')}</span>
            </div>

            <div style={{ background: 'rgba(168, 85, 247, 0.05)', padding: '1.25rem', borderRadius: '12px', border: '1px solid rgba(168, 85, 247, 0.2)' }}>
              <span style={{ fontSize: '0.8rem', color: '#c084fc', fontWeight: 700 }}>30-Day Learning Plan</span>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: '#fff', margin: '0.25rem 0' }}>4 Weeks</div>
              <span style={{ fontSize: '0.75rem', color: '#9ca3af' }}>Targeting Docker, K8s, AWS</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
