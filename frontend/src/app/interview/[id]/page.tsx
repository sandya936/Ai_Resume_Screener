'use client';

import React, { useState } from 'react';
import {
  MessageSquare,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Send,
  Star,
  BookOpen,
  Award,
} from 'lucide-react';

interface Question {
  id: string;
  category: 'technical' | 'project' | 'behavioral' | 'hr' | 'jd_specific';
  question_text: string;
  context_reason: string;
  star_talking_points: string[];
}

interface EvaluationResult {
  score: number;
  strengths: string[];
  missing_elements: string[];
  improved_sample_answer: string;
  explainable_feedback: string;
}

export default function InterviewPracticeStudio() {
  const [activeTab, setActiveTab] = useState<string>('all');
  const [userAnswer, setUserAnswer] = useState<string>('');
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>({
    score: 82,
    strengths: [
      'Clear description of technical action taken (FastAPI & SQLAlchemy 2.0 async connections).',
      'Includes quantifiable outcomes (45% latency reduction and 99.9% uptime).',
    ],
    missing_elements: [
      'Briefly state the team size or project deadline context in the Situation phase.',
    ],
    improved_sample_answer:
      'Situation: While engineering backend microservices for high concurrency workloads at TechCorp, Task: I was responsible for optimizing API response latency and database query bottlenecks under 10M daily requests. Action: I architected async database connections using SQLAlchemy 2.0 and integrated Redis caching for hot read paths. Result: This reduced database query latency by 45% and maintained 99.9% uptime during peak traffic.',
    explainable_feedback:
      'Answer Score: 82/100. Excellent technical detail and quantitative metric impact. Structuring your answer using the STAR methodology (Situation, Task, Action, Result) will make it top-tier for senior tech interviews.',
  });

  const [questions] = useState<Question[]>([
    {
      id: 'q1',
      category: 'technical',
      question_text: 'How do you optimize API performance and handle database concurrency using Python and PostgreSQL?',
      context_reason: 'Targets your core technical skill in Python backend engineering.',
      star_talking_points: [
        'Explain indexing strategies and connection pooling.',
        'Discuss async I/O handlers and query caching using Redis.',
        'Mention metric monitoring for latency (p95, p99).',
      ],
    },
    {
      id: 'q2',
      category: 'project',
      question_text: "Walk me through the architecture of 'AGENTX Platform'. What was your specific role and key technical challenges?",
      context_reason: "Focuses on your primary listed project 'AGENTX Platform'.",
      star_talking_points: [
        'Situation: Define problem statement and project objective.',
        'Task: Explain your individual design responsibility.',
        'Action: Detail system architecture, tech stack, and API design.',
        'Result: State quantifiable outcomes (users, latency, uptime).',
      ],
    },
    {
      id: 'q3',
      category: 'behavioral',
      question_text: 'Tell me about a time you encountered an unexpected system failure or API outage in production. How did you diagnose and resolve it?',
      context_reason: 'Evaluates production incident handling and engineering problem-solving.',
      star_talking_points: [
        'Describe log inspection and root cause analysis.',
        'Explain emergency mitigation vs long-term fix.',
        'Highlight post-mortem review and automated testing.',
      ],
    },
  ]);

  const [selectedQuestion, setSelectedQuestion] = useState<Question>(questions[0]);

  const handleEvaluate = () => {
    if (!userAnswer.trim()) return;
    setIsEvaluating(true);
    setTimeout(() => {
      setIsEvaluating(false);
    }, 600);
  };

  const filteredQuestions = activeTab === 'all' ? questions : questions.filter(q => q.category === activeTab);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#090d16', color: '#f3f4f6', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>

        {/* Header Bar */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1.5rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, background: 'linear-gradient(135deg, #3b82f6 0%, #a855f7 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                AGENTX
              </span>
              <span style={{ padding: '0.25rem 0.6rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 700, backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#60a5fa', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                Interview Practice & Evaluation Studio
              </span>
            </div>
            <p style={{ color: '#9ca3af', fontSize: '0.95rem', margin: 0 }}>
              Tailored Technical, Project, and STAR Behavioral Mock Interview Studio
            </p>
          </div>
        </header>

        {/* Main 2-Column Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) minmax(400px, 1.5fr)', gap: '1.5rem' }}>

          {/* Left Column: Question Bank */}
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <MessageSquare size={18} color="#60a5fa" /> Tailored Questions Bank
            </h3>

            {/* Filter Tabs */}
            <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '1.25rem', overflowX: 'auto', paddingBottom: '0.25rem' }}>
              {['all', 'technical', 'project', 'behavioral'].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  style={{
                    padding: '0.35rem 0.75rem',
                    borderRadius: '6px',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    textTransform: 'capitalize',
                    border: 'none',
                    cursor: 'pointer',
                    backgroundColor: activeTab === tab ? '#3b82f6' : 'rgba(255, 255, 255, 0.05)',
                    color: activeTab === tab ? '#fff' : '#9ca3af',
                  }}
                >
                  {tab}
                </button>
              ))}
            </div>

            {/* Question Cards List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {filteredQuestions.map(q => {
                const isSelected = q.id === selectedQuestion.id;
                return (
                  <div
                    key={q.id}
                    onClick={() => setSelectedQuestion(q)}
                    style={{
                      padding: '1rem',
                      borderRadius: '10px',
                      border: isSelected ? '1px solid #3b82f6' : '1px solid rgba(255, 255, 255, 0.08)',
                      background: isSelected ? 'rgba(59, 130, 246, 0.1)' : 'rgba(0, 0, 0, 0.2)',
                      cursor: 'pointer',
                    }}
                  >
                    <span style={{ fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', color: '#60a5fa' }}>{q.category}</span>
                    <p style={{ fontSize: '0.875rem', color: '#fff', fontWeight: 600, margin: '0.4rem 0 0 0', lineHeight: 1.4 }}>{q.question_text}</p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Column: Practice & Evaluation Studio */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            
            {/* Selected Question Detail Card */}
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '1.75rem' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', color: '#a855f7' }}>Selected Question</span>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff', margin: '0.5rem 0 0.75rem 0', lineHeight: 1.4 }}>
                {selectedQuestion.question_text}
              </h3>
              <p style={{ fontSize: '0.85rem', color: '#9ca3af', marginBottom: '1rem' }}>{selectedQuestion.context_reason}</p>
              
              {/* STAR Talking Points */}
              <div style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '1rem', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '0.3rem', marginBottom: '0.5rem' }}>
                  <Star size={14} /> Recommended STAR Talking Points
                </span>
                <ul style={{ paddingLeft: '1.25rem', margin: 0, fontSize: '0.8rem', color: '#d1d5db', lineHeight: 1.5 }}>
                  {selectedQuestion.star_talking_points.map((pt, idx) => (
                    <li key={idx}>{pt}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Practice Textarea Box */}
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '1.75rem' }}>
              <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>Practice Your Answer</h4>
              <textarea
                rows={5}
                value={userAnswer}
                onChange={e => setUserAnswer(e.target.value)}
                placeholder="Type your practice response here... (Describe your Situation, Task, Action, and Result)"
                style={{ width: '100%', backgroundColor: 'rgba(0, 0, 0, 0.4)', border: '1px solid rgba(255, 255, 255, 0.15)', borderRadius: '10px', padding: '1rem', color: '#fff', fontSize: '0.9rem', outline: 'none', resize: 'vertical', marginBottom: '1rem' }}
              />
              <button
                onClick={handleEvaluate}
                disabled={isEvaluating}
                style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem 1.5rem', borderRadius: '8px', border: 'none', background: 'linear-gradient(135deg, #3b82f6 0%, #a855f7 100%)', color: '#fff', fontSize: '0.9rem', fontWeight: 700, cursor: 'pointer' }}
              >
                <Sparkles size={16} /> {isEvaluating ? 'Evaluating Answer...' : 'Evaluate My Answer'}
              </button>
            </div>

            {/* Answer Evaluation Feedback Result */}
            {evaluation && (
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '16px', padding: '1.75rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', margin: 0 }}>Answer Feedback Report</h4>
                  <span style={{ fontSize: '1.25rem', fontWeight: 800, color: evaluation.score >= 75 ? '#34d399' : '#fbbf24' }}>
                    Score: {evaluation.score}/100
                  </span>
                </div>
                <p style={{ fontSize: '0.875rem', color: '#d1d5db', lineHeight: 1.5, marginBottom: '1.25rem' }}>{evaluation.explainable_feedback}</p>

                {/* Improved Exemplar Answer */}
                <div style={{ background: 'rgba(59, 130, 246, 0.06)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: '10px', padding: '1rem' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#60a5fa', display: 'block', marginBottom: '0.4rem' }}>Improved Exemplar Answer</span>
                  <p style={{ fontSize: '0.85rem', color: '#e5e7eb', lineHeight: 1.5, margin: 0 }}>{evaluation.improved_sample_answer}</p>
                </div>
              </div>
            )}

          </div>

        </div>

      </div>
    </div>
  );
}
