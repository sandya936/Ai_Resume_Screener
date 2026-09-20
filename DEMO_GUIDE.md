# AGENTX — Live Demonstration Script & Tech-Fest Guide

This document provides a step-by-step demonstration script for presenting **AGENTX** at national-level technical fests, hackathons, and final-year academic project vivas.

---

## 1. Core Demonstration Philosophy

> **"Chatbots answer questions. Autonomous agents perform actions. Multi-agent systems collaborate to achieve complex career goals."**

AGENTX demonstrates how specialized autonomous agents collaborate to transform static resumes into actionable career development plans.

---

## 2. Live vs. Fallback Mode Strategy (Honest Reliability Policy)

To ensure 100% presentation uptime without failing live due to external LLM vendor outages:
- **Live Mode**: Set `LLM_PROVIDER=gemini` or `LLM_PROVIDER=openai` in `.env` to execute live network LLM extraction calls.
- **Fallback Mode**: Set `LLM_PROVIDER=mock`. The system executes deterministic parsing, ATS scoring rules, and 5-category matching without external network dependencies.
- **Transparency Standard**: The UI displays provider status ("Connected: Mock Deterministic Engine (Offline Resilient)" vs "Connected: Gemini 1.5 Flash"). Zero fake results are presented as live.

---

## 3. Step-by-Step Presentation Script

### Step 1: User Login & Dashboard Overview (0:00 - 1:00)
- Navigate to `http://localhost:3000`.
- Log in with candidate credentials (`demo@agentx.ai` / `Password123!`).
- Point out the dark glassmorphic SaaS dashboard interface.

### Step 2: Resume Ingestion & Extraction Pipeline (1:00 - 2:00)
- Upload `backend/tests/sample_resumes/senior_dev.pdf`.
- Highlight instant MIME type magic bytes header validation and storage isolation.
- Show extracted raw text vs structured profile Pydantic JSON payload.

### Step 3: Job Description Ingestion & Skill Synonym Normalization (2:00 - 3:00)
- Paste a target Senior Backend Engineer Job Description containing `K8s`, `Postgres`, `AWS`.
- Demonstrate the **Skill Normalizer** translating `K8s` -> `kubernetes` and `Postgres` -> `postgresql` to prevent false negative flags.

### Step 4: 5-Category Weighted Match & Explainable ATS Breakdown (3:00 - 4:30)
- Navigate to `/match/[id]`.
- Explain the 5-category open mathematical formula:
  - Required Skills Match (40%)
  - Preferred Skills Match (15%)
  - Work Experience Match (25%)
  - Project Relevance (10%)
  - Education Match (10%)
- Show Green `+` Matched Skills vs Red `-` Missing Required Skills.

### Step 5: Multi-Agent Autonomous System Orchestration & Live Execution Trace (4:30 - 7:00)
- Click **"Run Multi-Agent Goal Orchestration"** at `/agents/orchestrate`.
- Show live progress ticks for all 6 agents:
  1. `ManagerOrchestratorAgent`: Decomposes user goal into execution graph.
  2. `ResumeAgent`: Retrieves & validates candidate profile.
  3. `JobDescriptionAgent`: Ingests & normalizes JD requirements.
  4. `SkillGapAgent`: Categorizes gaps (Critical, Medium, Low).
  5. `RecommendationAgent`: Generates 30-day curriculum (Anti-fabrication policy enforced).
  6. `InterviewAgent`: Generates 5-category tailored question bank.
- Open the **Trace Log Inspector** to show exact inputs, outputs, tool calls, and execution times for each agent.

### Step 6: Tailored Interview Practice & STAR Evaluation Studio (7:00 - 8:30)
- Navigate to `/interview/[id]`.
- Type a practice answer to a technical question.
- Click **"Evaluate Answer"** to display score (0-100), missing STAR framework elements, and an improved sample answer.
