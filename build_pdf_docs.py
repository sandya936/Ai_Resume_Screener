import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf():
    pdf_path = os.path.join(os.getcwd(), "PROJECT_DOCUMENTATION.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2C221E'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#8B0000'),
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=3
    )

    story = []

    # Header
    story.append(Paragraph("AGENTX — AI Resume Intelligence & Autonomous Career Platform", title_style))
    story.append(Paragraph("<b>Comprehensive Project Documentation & Technical Specification</b><br/>Project Author & Architecture: Sandya Kaki & FastAPI Architecture | Version 1.0 Live", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#8B0000'), spaceAfter=12))

    # URLs Table
    url_data = [
        [Paragraph("<b>Resource</b>", body_style), Paragraph("<b>Production URL / Reference</b>", body_style)],
        [Paragraph("<b>Frontend Live URL</b>", body_style), Paragraph("<a href='https://frontend-pi-lime-21.vercel.app'>https://frontend-pi-lime-21.vercel.app</a>", body_style)],
        [Paragraph("<b>Backend Live URL</b>", body_style), Paragraph("<a href='https://ai-resume-screener-26ke.onrender.com'>https://ai-resume-screener-26ke.onrender.com</a>", body_style)],
        [Paragraph("<b>GitHub Repository</b>", body_style), Paragraph("<a href='https://github.com/sandya936/Ai_Resume_Screener'>https://github.com/sandya936/Ai_Resume_Screener</a>", body_style)],
        [Paragraph("<b>Pytest Harness</b>", body_style), Paragraph("<b>44 / 44 Passing Automated Unit Tests (100%)</b>", body_style)],
    ]
    t = Table(url_data, colWidths=[140, 400])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F4EFEB')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#8B0000')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Planning", h1_style))
    story.append(Paragraph("<b>AGENTX</b> is a production-oriented AI Resume Intelligence SaaS platform designed to transform static resumes into actionable, explainable career development plans. Built on a high-performance Modular Monolith architecture in FastAPI (Async Python 3.11) and Next.js 14+ (App Router), AGENTX replaces arbitrary black-box LLM scoring with an explainable <b>60% Deterministic + 40% AI Auditor Engine</b>, a Skill Normalizer, a 5-Category Open Mathematical Matching Formula, and an observable 6-Agent Autonomous System.", body_style))
    
    story.append(Paragraph("<b>Development Planning Methodology:</b>", h2_style))
    story.append(Paragraph("• <b>Phase 1: Foundation & Domain Engine</b> — Pydantic domain models, magic-byte document validation, async ORM storage layer.", bullet_style))
    story.append(Paragraph("• <b>Phase 2: ATS Scoring & Skill Normalization</b> — 100+ Action verb registry, canonical keyword normalizer (K8s -&gt; kubernetes), 5-category match score equation.", bullet_style))
    story.append(Paragraph("• <b>Phase 3: Multi-Agent Swarm Orchestration</b> — Built 6 specialized agents executing sandboxed tools with execution trace logs.", bullet_style))
    story.append(Paragraph("• <b>Phase 4: Dual-Theme Frontend UI</b> — Next.js 14 App Router UI with Warm Crimson Parchment vs Dark Cyber Slate theme switcher, guest demo login, and 40-question STAR interview generator.", bullet_style))
    story.append(Paragraph("• <b>Phase 5: Cloud Deployment & Testing</b> — 44/44 passing automated pytest suite, Vercel frontend deployment, Render backend deployment.", bullet_style))

    story.append(Spacer(1, 8))

    # Section 2
    story.append(Paragraph("2. Technical Stack Specification", h1_style))
    stack_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Purpose / Details</b>", body_style)],
        [Paragraph("<b>Backend Core</b>", body_style), Paragraph("FastAPI (Python 3.11+)", body_style), Paragraph("Async ASGI Web Framework for high concurrency", body_style)],
        [Paragraph("<b>Frontend Core</b>", body_style), Paragraph("Next.js 14 App Router", body_style), Paragraph("React Framework with TypeScript & Server Components", body_style)],
        [Paragraph("<b>Styling & CSS</b>", body_style), Paragraph("Vanilla CSS3 & Tokens", body_style), Paragraph("Dynamic CSS variables, glassmorphism, responsive grids", body_style)],
        [Paragraph("<b>Database</b>", body_style), Paragraph("SQLAlchemy 2.0 Async", body_style), Paragraph("SQLite / PostgreSQL with Alembic migration support", body_style)],
        [Paragraph("<b>AI Providers</b>", body_style), Paragraph("Gemini 2.0 / OpenAI", body_style), Paragraph("LLM Provider Abstraction (BaseLLMProvider) & fallback", body_style)],
        [Paragraph("<b>Security</b>", body_style), Paragraph("PII Redactor & Headers", body_style), Paragraph("PII Log Redaction Filter, HSTS, CSP, X-Request-ID", body_style)],
        [Paragraph("<b>Test Suite</b>", body_style), Paragraph("Pytest Asyncio", body_style), Paragraph("44 Automated Tests covering APIs, models, agents", body_style)],
    ]
    t_stack = Table(stack_data, colWidths=[100, 140, 300])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stack)

    story.append(Spacer(1, 8))

    # Section 3
    story.append(Paragraph("3. System Architecture & Autonomous Multi-Agent Swarm", h1_style))
    story.append(Paragraph("The system uses a modular monolith backend architecture communicating with a 6-Agent Manager-Worker Swarm System executing sandboxed tools:", body_style))
    story.append(Paragraph("• <b>ManagerOrchestratorAgent</b>: Plan decomposition, state aggregation, and trace graph management.", bullet_style))
    story.append(Paragraph("• <b>ResumeAgent</b>: Executes <i>tool_fetch_resume</i> for section extraction and candidate profile building.", bullet_style))
    story.append(Paragraph("• <b>JobDescriptionAgent</b>: Executes <i>tool_parse_job</i> for requirements, preferred skills, and experience extraction.", bullet_style))
    story.append(Paragraph("• <b>SkillGapAgent</b>: Executes <i>tool_evaluate_match</i> using canonical skill normalization and 5-category scoring.", bullet_style))
    story.append(Paragraph("• <b>RecommendationAgent</b>: Executes <i>tool_generate_roadmap</i> for prioritized 30-day learning curriculum.", bullet_style))
    story.append(Paragraph("• <b>InterviewAgent</b>: Executes <i>tool_generate_interview_questions</i> for 40-question STAR practice generator.", bullet_style))

    story.append(Spacer(1, 8))

    # Section 4
    story.append(Paragraph("4. UI Design & Aesthetic Architecture", h1_style))
    story.append(Paragraph("AGENTX features a dual-theme switcher (persisted via <i>localStorage</i> key <b>agentx_theme</b>):", body_style))
    story.append(Paragraph("1. <b>Warm Crimson Parchment Theme</b>: Background <i>#F4EFEB</i>, Crimson Accent <i>#8B0000</i>, Warm Sandstone Cards, Dark Espresso Typography <i>#2C221E</i>.", bullet_style))
    story.append(Paragraph("2. <b>Dark Cyber Slate Theme</b>: Background <i>#0B0F17</i>, Electric Emerald Accent <i>#10B981</i>, Obsidian Cards, Crisp Slate Typography <i>#F9FAFB</i>.", bullet_style))

    story.append(Spacer(1, 8))

    # Section 5
    story.append(Paragraph("5. Implementation Features & Mathematical Matching", h1_style))
    story.append(Paragraph("<b>5-Category Weighted Match Formula:</b>", h2_style))
    story.append(Paragraph("Match Score = (Required Skills × 0.40) + (Preferred Skills × 0.15) + (Experience × 0.25) + (Projects × 0.10) + (Education × 0.10)", body_style))
    
    story.append(Paragraph("<b>40-Question STAR Interview Practice Studio:</b>", h2_style))
    story.append(Paragraph("Generates 10 Technical Deep Dives, 10 Behavioral STAR Scenarios, 8 Project Experience Dives, 6 HR & Fit Questions, and 6 Job Description Specific questions with real-time answer scoring.", body_style))

    story.append(Spacer(1, 8))

    # Section 6
    story.append(Paragraph("6. Verification Test Suite & Cloud Deployment", h1_style))
    story.append(Paragraph("<b>Automated Test Suite Results: 44 / 44 PASSED (100%)</b> across 12 test modules including ATS analysis, authentication, career intelligence, job matching, multi-agent execution, and PII security headers.", body_style))
    story.append(Paragraph("<b>Cloud Deployment Topology:</b>", body_style))
    story.append(Paragraph("• <b>Backend</b>: Deployed on Render (Python 3.11 ASGI Uvicorn Server).", bullet_style))
    story.append(Paragraph("• <b>Frontend</b>: Deployed on Vercel (Next.js 14 App Router with edge optimization).", bullet_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
    story.append(Paragraph("<font color='#64748B' size=8><b>© 2026 AGENTX AI Platform. All rights reserved.</b><br/>Powered by Sandya Kaki &amp; FastAPI Architecture.</font>", ParagraphStyle('Footer', parent=styles['Normal'], alignment=1)))

    doc.build(story)
    print(f"Successfully generated PDF at: {pdf_path}")

def generate_html():
    html_path = os.path.join(os.getcwd(), "PROJECT_DOCUMENTATION.html")
    with open("PROJECT_DOCUMENTATION.md", "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AGENTX — Project Documentation</title>
    <style>
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background-color: #F4EFEB;
            color: #2C221E;
            line-height: 1.6;
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 50px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            border: 1px solid #E2D9D0;
        }}
        h1 {{
            color: #8B0000;
            font-size: 28px;
            border-bottom: 2px solid #8B0000;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #8B0000;
            font-size: 20px;
            margin-top: 30px;
            border-bottom: 1px solid #E2D9D0;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #1E293B;
            font-size: 16px;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        th, td {{
            padding: 10px 14px;
            border: 1px solid #CBD5E1;
            text-align: left;
        }}
        th {{
            background-color: #F4EFEB;
            color: #8B0000;
            font-weight: bold;
        }}
        code {{
            background: #F1F5F9;
            color: #0F172A;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Consolas, monospace;
            font-size: 13px;
        }}
        pre {{
            background: #0F172A;
            color: #F8FAFC;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: Consolas, monospace;
        }}
        .badge {{
            display: inline-block;
            background: #8B0000;
            color: #FFF;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #E2D9D0;
            font-size: 13px;
            color: #64748B;
            text-align: center;
        }}
        @media print {{
            body {{ background: #FFF; padding: 0; }}
            .container {{ box-shadow: none; border: none; padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">PRODUCTION LIVE v1.0</span>
        <h1>AGENTX — AI Resume Intelligence & Autonomous Career Platform</h1>
        <p><strong>Author & Architecture:</strong> Sandya Kaki & FastAPI Architecture</p>
        
        <table>
            <tr><th>Resource</th><th>Link / Detail</th></tr>
            <tr><td><strong>Frontend Live Website</strong></td><td><a href="https://frontend-pi-lime-21.vercel.app" target="_blank">https://frontend-pi-lime-21.vercel.app</a></td></tr>
            <tr><td><strong>Backend Live API</strong></td><td><a href="https://ai-resume-screener-26ke.onrender.com" target="_blank">https://ai-resume-screener-26ke.onrender.com</a></td></tr>
            <tr><td><strong>GitHub Repository</strong></td><td><a href="https://github.com/sandya936/Ai_Resume_Screener" target="_blank">https://github.com/sandya936/Ai_Resume_Screener</a></td></tr>
            <tr><td><strong>Automated Pytest Suite</strong></td><td><strong>44 / 44 PASSED (100% Pass Rate)</strong></td></tr>
        </table>

        <h2>1. Executive Summary & Planning</h2>
        <p>AGENTX is a production-oriented AI Resume Intelligence & Autonomous Career SaaS platform. It transforms static resume documents (PDF / DOCX) into explainable, actionable, and quantifiable career growth assets using a <strong>60% Deterministic + 40% AI Auditor Engine</strong>.</p>

        <h2>2. Technical Stack</h2>
        <ul>
            <li><strong>Backend Core:</strong> FastAPI (Python 3.11 Async), Uvicorn ASGI</li>
            <li><strong>Frontend Core:</strong> Next.js 14 App Router, TypeScript, Responsive CSS Variables</li>
            <li><strong>Database:</strong> SQLAlchemy 2.0 Async ORM (SQLite / PostgreSQL)</li>
            <li><strong>AI LLM Engine:</strong> Google Gemini 2.0 / OpenAI / Fallback Engine</li>
            <li><strong>Security:</strong> PII Redaction Filter, HSTS, CSP, Correlation <code>X-Request-ID</code></li>
            <li><strong>Cloud Deployment:</strong> Vercel (Frontend) + Render (Backend)</li>
        </ul>

        <h2>3. 6-Agent Autonomous System Architecture</h2>
        <pre>
ManagerOrchestratorAgent (Decomposes goal into plan)
  ├─> 1. ResumeAgent (Tool: tool_fetch_resume)
  ├─> 2. JobDescriptionAgent (Tool: tool_parse_job)
  ├─> 3. SkillGapAgent (Tool: tool_evaluate_match)
  ├─> 4. RecommendationAgent (Tool: tool_generate_roadmap)
  └─> 5. InterviewAgent (Tool: tool_generate_interview_questions)
        </pre>

        <h2>4. Dual-Theme Architecture</h2>
        <ul>
            <li><strong>Warm Crimson Parchment Theme:</strong> Sandstone background (<code>#F4EFEB</code>), Crimson accents (<code>#8B0000</code>), Espresso typography (<code>#2C221E</code>).</li>
            <li><strong>Dark Cyber Slate Theme:</strong> Deep obsidian background (<code>#0B0F17</code>), Electric emerald accents (<code>#10B981</code>).</li>
        </ul>

        <h2>5. 40-Question STAR Interview Practice Studio</h2>
        <p>Generates 40 custom interview practice questions (10 Technical, 10 Behavioral, 8 Project, 6 HR, 6 JD-Specific) with interactive STAR scoring.</p>

        <div class="footer">
            © 2026 AGENTX AI Platform. All rights reserved.<br>
            <em>Powered by Sandya Kaki & FastAPI Architecture.</em>
        </div>
    </div>
</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated HTML at: {html_path}")

if __name__ == "__main__":
    generate_pdf()
    generate_html()
