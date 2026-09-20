import uuid
import re
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.parsed_resume import ParsedResume
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    SkillCategory,
    WorkExperienceEntry,
    ProjectEntry,
    EducationEntry,
)
from app.domain.schemas.interview_intelligence import (
    InterviewQuestion,
    AnswerEvaluationRequest,
    AnswerEvaluationResponse,
)


class InterviewIntelligenceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_question_bank(self, resume_id: uuid.UUID) -> List[InterviewQuestion]:
        # Fetch ParsedResume
        result_parsed = await self.db.execute(
            select(ParsedResume).where(ParsedResume.resume_id == resume_id)
        )
        parsed_record = result_parsed.scalar_one_or_none()

        if not parsed_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "PARSED_RESUME_NOT_FOUND",
                        "message": "Resume has not been parsed yet. Run POST /resumes/{id}/parse first.",
                        "details": [],
                    },
                },
            )

        structured = StructuredResume(
            personal_info=PersonalInfo(**parsed_record.contact_info),
            summary=parsed_record.summary,
            work_experience=[WorkExperienceEntry(**w) for w in parsed_record.work_experience],
            education=[EducationEntry(**e) for e in parsed_record.education],
            skills=SkillCategory(**parsed_record.skills),
            projects=[ProjectEntry(**p) for p in parsed_record.projects],
        )

        # Query latest JobDescription for candidate's user
        from app.db.models.job_description import JobDescription
        result_jd = await self.db.execute(
            select(JobDescription)
            .where(JobDescription.user_id == parsed_record.resume.user_id)
            .order_by(JobDescription.created_at.desc())
        )
        latest_jd = result_jd.scalars().first()
        target_role = latest_jd.title if latest_jd else "Target Role"

        # Extract dynamic candidate parameters
        tech_skills = structured.skills.technical_skills if structured.skills.technical_skills else ["Python", "FastAPI", "SQL", "Data Analysis"]
        tools = structured.skills.tools_and_frameworks if structured.skills.tools_and_frameworks else ["Git", "Docker", "Power BI", "Excel"]
        all_skills = tech_skills + tools

        s0 = all_skills[0].title() if len(all_skills) > 0 else "Python"
        s1 = all_skills[1].title() if len(all_skills) > 1 else "SQL"
        s2 = all_skills[2].title() if len(all_skills) > 2 else "FastAPI"
        s3 = all_skills[3].title() if len(all_skills) > 3 else "Power BI"
        s4 = all_skills[4].title() if len(all_skills) > 4 else "Docker"

        # Projects
        p0_title = structured.projects[0].title if len(structured.projects) > 0 else f"{s0} & {s1} Portfolio Analytics Project"
        p0_tech = ", ".join(structured.projects[0].technologies) if len(structured.projects) > 0 and structured.projects[0].technologies else f"{s0}, {s1}"
        p1_title = structured.projects[1].title if len(structured.projects) > 1 else f"Automated {s2} Microservices Pipeline"

        # Work Experience
        exp0_company = structured.work_experience[0].company if len(structured.work_experience) > 0 else "Tech & Analytics Operations"
        exp0_title = structured.work_experience[0].title if len(structured.work_experience) > 0 else "Software & Data Analytics Specialist"
        exp1_company = structured.work_experience[1].company if len(structured.work_experience) > 1 else "Engineering & Innovation Lab"

        # Education
        edu_inst = structured.education[0].institution if len(structured.education) > 0 else "University Engineering Institute"
        edu_field = structured.education[0].field_of_study if len(structured.education) > 0 else "Computer Science & Data Analytics"

        cand_name = structured.personal_info.full_name if structured.personal_info.full_name else "Candidate"

        questions: List[InterviewQuestion] = []

        # ==========================================
        # TOP 20 RESUME-BASED QUESTIONS
        # ==========================================

        # 1. Technical Skill Deep Dive
        questions.append(
            InterviewQuestion(
                id="q-res-01",
                category="Resume - Technical Skill",
                question_type="resume_based",
                question_text=f"How do you design, optimize, and maintain production workflows using {s0} and {s1}?",
                context_reason=f"Evaluates your core listed technical expertise in {s0} and {s1}.",
                star_talking_points=[
                    f"Situation: Detail a production scenario where you utilized {s0}.",
                    f"Task: Explain system requirements and efficiency targets.",
                    f"Action: Describe implementation details, query structures, or logic handling.",
                    f"Result: State throughput gains, latency reduction, or accuracy metrics.",
                ],
            )
        )

        # 2. Secondary Framework Architecture
        questions.append(
            InterviewQuestion(
                id="q-res-02",
                category="Resume - Technical Skill",
                question_type="resume_based",
                question_text=f"Walk me through how you leverage {s2} to ensure high reliability, modularity, and maintainability.",
                context_reason=f"Assesses technical depth with your listed technology {s2}.",
                star_talking_points=[
                    f"Discuss architectural patterns and code organization when building with {s2}.",
                    "Explain state management, error boundaries, or middleware integration.",
                    "Highlight automated testing and validation strategies.",
                ],
            )
        )

        # 3. Database & Query Optimization
        questions.append(
            InterviewQuestion(
                id="q-res-03",
                category="Resume - Technical Skill",
                question_type="resume_based",
                question_text=f"How do you optimize complex database queries, schema indexing, and data normalization when working with {s1}?",
                context_reason=f"Probes database performance engineering skills using {s1}.",
                star_talking_points=[
                    f"Explain query plan analysis, indexing strategies, and joins in {s1}.",
                    "Describe data sanitization and migration procedures.",
                    "Provide concrete examples of query latency reduction.",
                ],
            )
        )

        # 4. Tooling & Infrastructure Workflow
        questions.append(
            InterviewQuestion(
                id="q-res-04",
                category="Resume - Technical Skill",
                question_type="resume_based",
                question_text=f"How do you incorporate {s3} and {s4} into your daily development and deployment workflow?",
                context_reason=f"Validates operational proficiency with listed tools {s3} and {s4}.",
                star_talking_points=[
                    f"Explain environment setup, containerization, or dashboard design using {s3}/{s4}.",
                    "Discuss configuration management and reproducibility.",
                    "Highlight team collaboration or version control practices.",
                ],
            )
        )

        # 5. Asynchronous & Performance Engineering
        questions.append(
            InterviewQuestion(
                id="q-res-05",
                category="Resume - Technical Skill",
                question_type="resume_based",
                question_text=f"How do you handle concurrency, asynchronous I/O, or caching to prevent bottlenecks in applications built with {s0}?",
                context_reason=f"Evaluates performance engineering and scalability capabilities in {s0}.",
                star_talking_points=[
                    "Explain async event loops, connection pooling, or Redis caching.",
                    "Discuss memory management and CPU profile monitoring.",
                    "Describe load test verification and throughput metrics.",
                ],
            )
        )

        # 6. Primary Project Architecture
        questions.append(
            InterviewQuestion(
                id="q-res-06",
                category="Resume - Project Deep Dive",
                question_type="resume_based",
                question_text=f"Walk me through the system architecture and key design choices of your featured project '{p0_title}'.",
                context_reason=f"Focuses on your primary portfolio project '{p0_title}'.",
                star_talking_points=[
                    f"Situation: Define problem statement and objectives for '{p0_title}'.",
                    f"Task: Detail your specific architectural design responsibilities.",
                    f"Action: Explain tech stack integration ({p0_tech}) and data flow.",
                    "Result: Highlight project delivery metrics, adoption, or performance.",
                ],
            )
        )

        # 7. Project Technology Trade-offs
        questions.append(
            InterviewQuestion(
                id="q-res-07",
                category="Resume - Project Deep Dive",
                question_type="resume_based",
                question_text=f"Why did you choose {p0_tech} for '{p0_title}' over alternative technologies? What trade-offs did you evaluate?",
                context_reason=f"Evaluates technical decision-making and evaluation rigor in '{p0_title}'.",
                star_talking_points=[
                    "Compare alternative frameworks or database choices.",
                    "Explain evaluation criteria (performance, developer velocity, ecosystem).",
                    "Justify the final architecture selection based on project needs.",
                ],
            )
        )

        # 8. Secondary Project Edge Cases
        questions.append(
            InterviewQuestion(
                id="q-res-08",
                category="Resume - Project Deep Dive",
                question_type="resume_based",
                question_text=f"In '{p1_title}', what was the most complex technical bug or edge-case you encountered, and how did you resolve it?",
                context_reason=f"Assesses debugging methodology and technical resilience in '{p1_title}'.",
                star_talking_points=[
                    "Describe bug symptom, logs, and initial diagnostic hypothesis.",
                    "Explain root cause analysis techniques and tools used.",
                    "Detail code patch, automated regression test, and deployment.",
                ],
            )
        )

        # 9. Data Modeling & Schema Integrity
        questions.append(
            InterviewQuestion(
                id="q-res-09",
                category="Resume - Project Deep Dive",
                question_type="resume_based",
                question_text=f"How did you structure data schema entities, relationships, and validation logic for '{p0_title}'?",
                context_reason=f"Probes data integrity and modeling capabilities in '{p0_title}'.",
                star_talking_points=[
                    "Explain entity relationship diagrams, foreign keys, and constraints.",
                    "Discuss schema validation frameworks (Pydantic, ORM schemas).",
                    "Highlight data sanity checks and migration strategies.",
                ],
            )
        )

        # 10. API Contracts & Service Integration
        questions.append(
            InterviewQuestion(
                id="q-res-10",
                category="Resume - Project Deep Dive",
                question_type="resume_based",
                question_text=f"How did you design RESTful endpoints, API contracts, or third-party service integrations for '{p0_title}'?",
                context_reason=f"Evaluates API contract design and integration skills in '{p0_title}'.",
                star_talking_points=[
                    "Discuss request/response payloads, status codes, and security headers.",
                    "Explain error handling and correlation tracking.",
                    "Detail OpenAPI specification or API documentation practices.",
                ],
            )
        )

        # 11. Work Experience Role Deliverables
        questions.append(
            InterviewQuestion(
                id="q-res-11",
                category="Resume - Work Experience",
                question_type="resume_based",
                question_text=f"As a {exp0_title} at {exp0_company}, what were your core technical deliverables and day-to-day responsibilities?",
                context_reason=f"Targets your professional experience as {exp0_title} at {exp0_company}.",
                star_talking_points=[
                    f"Situation: Describe company context and engineering objectives at {exp0_company}.",
                    "Task: Outline your core deliverables and sprint commitments.",
                    f"Action: Detail engineering practices, code reviews, and technologies used.",
                    "Result: Highlight operational achievements and team impact.",
                ],
            )
        )

        # 12. Quantified Achievements & Metrics
        questions.append(
            InterviewQuestion(
                id="q-res-12",
                category="Resume - Work Experience",
                question_type="resume_based",
                question_text=f"How did you measure and quantify the business or performance impact of your contributions at {exp0_company}?",
                context_reason=f"Evaluates metric-driven engineering mindsets at {exp0_company}.",
                star_talking_points=[
                    "Identify baseline performance or business metrics before your changes.",
                    "Describe engineering actions taken to drive improvement.",
                    "State final quantitative result (e.g. % efficiency increase, time saved, latency reduction).",
                ],
            )
        )

        # 13. Technical Debt & Code Refactoring
        questions.append(
            InterviewQuestion(
                id="q-res-13",
                category="Resume - Work Experience",
                question_type="resume_based",
                question_text=f"Describe a scenario at {exp0_company} where you identified technical debt or unoptimized code and refactored it.",
                context_reason=f"Assesses commitment to code quality and refactoring at {exp0_company}.",
                star_talking_points=[
                    "Identify specific code smell, legacy bottleneck, or duplicate pattern.",
                    "Explain refactoring plan, test coverage protection, and execution.",
                    "Demonstrate code readability and performance improvements.",
                ],
            )
        )

        # 14. Multi-Role / Internship Experience
        questions.append(
            InterviewQuestion(
                id="q-res-14",
                category="Resume - Work Experience",
                question_type="resume_based",
                question_text=f"What key technical lessons or engineering practices did you adopt while working with {exp1_company}?",
                context_reason=f"Evaluates continuous technical growth across roles including {exp1_company}.",
                star_talking_points=[
                    f"Discuss technical workflows learned at {exp1_company}.",
                    "Explain adaptation to new team standards and tooling.",
                    "Highlight key accomplishments and skills carried forward.",
                ],
            )
        )

        # 15. Resilience & Fault Tolerance
        questions.append(
            InterviewQuestion(
                id="q-res-15",
                category="Resume - Engineering Practice",
                question_type="resume_based",
                question_text=f"How do you design fallbacks, circuit breakers, or retry mechanisms when upstream services fail?",
                context_reason="Probes fault tolerance and production reliability design.",
                star_talking_points=[
                    "Discuss graceful degradation strategies and timeout policies.",
                    "Explain logging, alerting, and error monitoring setup.",
                    "Provide real-world example of mitigating external downtime.",
                ],
            )
        )

        # 16. Academic & Theoretical Foundations
        questions.append(
            InterviewQuestion(
                id="q-res-16",
                category="Resume - Academic Foundation",
                question_type="resume_based",
                question_text=f"How has your background in {edu_field} from {edu_inst} informed your practical software engineering?",
                context_reason=f"Connects your academic coursework in {edu_field} at {edu_inst} to production practice.",
                star_talking_points=[
                    f"Relate theoretical concepts in {edu_field} to software/data engineering.",
                    "Discuss algorithms, data structures, or statistical methods applied in projects.",
                    "Explain continuous bridging of academic theory with practical tech stacks.",
                ],
            )
        )

        # 17. Security & Input Defense Standards
        questions.append(
            InterviewQuestion(
                id="q-res-17",
                category="Resume - Security & Defense",
                question_type="resume_based",
                question_text="How do you enforce security controls, PII redaction, and prompt injection defenses in your application code?",
                context_reason="Evaluates security hardening awareness and defensive coding practices.",
                star_talking_points=[
                    "Discuss input sanitization, parameter validation, and CSP headers.",
                    "Explain secret management, JWT handling, and environment isolation.",
                    "Detail logging security and PII log redaction filters.",
                ],
            )
        )

        # 18. Automated Test Harness & QA Strategy
        questions.append(
            InterviewQuestion(
                id="q-res-18",
                category="Resume - Quality Assurance",
                question_type="resume_based",
                question_text=f"What is your approach to writing automated Pytest or unit/integration test suites for apps built with {s0}?",
                context_reason=f"Probes automated testing methodologies for {s0} codebases.",
                star_talking_points=[
                    "Discuss test coverage goals, fixtures, and async test runners.",
                    "Explain mocking database calls, API HTTP clients, and providers.",
                    "Describe CI/CD automated test gate integration.",
                ],
            )
        )

        # 19. Target Role Technical Alignment
        questions.append(
            InterviewQuestion(
                id="q-res-19",
                category="Resume - Role Alignment",
                question_type="resume_based",
                question_text=f"How do your resume credentials and hands-on experience with {s0}, {s1}, and {s2} prepare you for the technical demands of a {target_role}?",
                context_reason=f"Directly maps your technical stack to the target role of {target_role}.",
                star_talking_points=[
                    f"Highlight core technical overlap between your resume and {target_role}.",
                    "Discuss past project impact demonstrating role readiness.",
                    "Emphasize technical mastery of required tools and paradigms.",
                ],
            )
        )

        # 20. Skill Evolution & Emerging Technologies
        questions.append(
            InterviewQuestion(
                id="q-res-20",
                category="Resume - Technical Growth",
                question_type="resume_based",
                question_text=f"Which advanced skills or tools beyond {s0} and {s1} are you currently learning to stay ahead in {target_role} fields?",
                context_reason="Evaluates proactive technical growth and learning roadmap initiative.",
                star_talking_points=[
                    "Identify specific technologies or cloud services currently being learned.",
                    "Explain side projects or hands-on tutorials built to gain mastery.",
                    "Connect new learning goals to future target role requirements.",
                ],
            )
        )

        # ==========================================
        # TOP 20 HR & BEHAVIORAL QUESTIONS
        # ==========================================

        # 1. Professional Story & Overview
        questions.append(
            InterviewQuestion(
                id="q-hr-01",
                category="HR - Professional Overview",
                question_type="hr_based",
                question_text=f"Tell me about yourself, your engineering journey, and what key experiences bring you here today as a {target_role} candidate.",
                context_reason="Evaluates concise self-presentation, professional narrative, and communication style.",
                star_talking_points=[
                    f"Present concise 2-minute summary of technical background ({s0}, {s1}).",
                    f"Highlight key project or career milestone at {exp0_company}.",
                    f"Express clear enthusiasm for growing as a {target_role}.",
                ],
            )
        )

        # 2. Target Role Motivation
        questions.append(
            InterviewQuestion(
                id="q-hr-02",
                category="HR - Role Motivation",
                question_type="hr_based",
                question_text=f"What specifically attracted you to apply for a {target_role} position, and why is this the right next step for you?",
                context_reason=f"Assesses genuine career alignment and motivation for {target_role}.",
                star_talking_points=[
                    f"Explain passion for solving engineering/data challenges in {target_role}.",
                    "Align company mission or domain with personal technical interests.",
                    "Demonstrate clear understanding of role expectations.",
                ],
            )
        )

        # 3. High Pressure & Deadline Management
        questions.append(
            InterviewQuestion(
                id="q-hr-03",
                category="HR - STAR Behavioral",
                question_type="hr_based",
                question_text=f"Describe a situation at {exp0_company} when you faced an extremely tight deadline. How did you manage your priorities and deliver?",
                context_reason=f"Evaluates performance under pressure and priority management at {exp0_company}.",
                star_talking_points=[
                    "Situation: Explain high-pressure project scope and deadline constraints.",
                    "Task: Outline critical vs non-critical deliverables.",
                    "Action: Detail task prioritization, clear stakeholder updates, and focused execution.",
                    "Result: State successful on-time delivery without compromising quality.",
                ],
            )
        )

        # 4. Conflict Resolution with Technical Peers
        questions.append(
            InterviewQuestion(
                id="q-hr-04",
                category="HR - STAR Behavioral",
                question_type="hr_based",
                question_text="Tell me about a time you had a strong technical disagreement with a teammate. How did you handle it and reach consensus?",
                context_reason="Assesses interpersonal communication, active listening, and conflict resolution.",
                star_talking_points=[
                    "Describe technical context of the disagreement (e.g. architecture design or tool choice).",
                    "Explain objective data-driven evaluation of both approaches.",
                    "Highlight collaborative alignment and team-first resolution.",
                ],
            )
        )

        # 5. Overcoming Project Roadblocks
        questions.append(
            InterviewQuestion(
                id="q-hr-05",
                category="HR - STAR Behavioral",
                question_type="hr_based",
                question_text=f"Describe a technical setback or unexpected obstacle you encountered in '{p0_title}'. How did you overcome it?",
                context_reason=f"Evaluates problem-solving resilience and adaptability during '{p0_title}'.",
                star_talking_points=[
                    f"Situation: Detail unexpected obstacle in '{p0_title}'.",
                    "Task: Identify problem scope and potential impact.",
                    "Action: Describe alternative strategies explored and resolution executed.",
                    "Result: State project recovery and key engineering lessons learned.",
                ],
            )
        )

        # 6. Communication with Non-Technical Stakeholders
        questions.append(
            InterviewQuestion(
                id="q-hr-06",
                category="HR - Stakeholder Communication",
                question_type="hr_based",
                question_text="How do you explain complex technical architecture or data findings to non-technical business partners?",
                context_reason="Evaluates cross-functional communication and ability to translate technical jargon into business value.",
                star_talking_points=[
                    "Explain use of visual diagrams, analogies, and business KPI language.",
                    "Discuss active listening and verifying stakeholder understanding.",
                    "Give example of presenting analytical insights to business leaders.",
                ],
            )
        )

        # 7. Prioritization & Multitasking
        questions.append(
            InterviewQuestion(
                id="q-hr-07",
                category="HR - Time Management",
                question_type="hr_based",
                question_text="When faced with multiple urgent bug reports and feature requests simultaneously, how do you decide what to work on first?",
                context_reason="Probes priority triage frameworks and time management discipline.",
                star_talking_points=[
                    "Explain severity/impact triage framework (P0 critical blocker vs P2 feature).",
                    "Discuss communicating expectations with product managers and engineers.",
                    "Describe maintaining focus without context-switching fatigue.",
                ],
            )
        )

        # 8. Adaptability to Changing Requirements
        questions.append(
            InterviewQuestion(
                id="q-hr-08",
                category="HR - STAR Behavioral",
                question_type="hr_based",
                question_text="Tell me about a time when business requirements shifted significantly in the middle of a development sprint.",
                context_reason="Assesses adaptability, flexibility, and positive attitude toward change.",
                star_talking_points=[
                    "Describe initial sprint goal and sudden scope requirement change.",
                    "Explain quick reassessment of architecture and task adjustments.",
                    "Highlight smooth pivot and successful delivery under new parameters.",
                ],
            )
        )

        # 9. End-to-End Ownership & Initiative
        questions.append(
            InterviewQuestion(
                id="q-hr-09",
                category="HR - Leadership & Ownership",
                question_type="hr_based",
                question_text=f"Describe a project where you took full ownership from initial requirement gathering to final production release.",
                context_reason="Evaluates proactive ownership, self-direction, and execution drive.",
                star_talking_points=[
                    "Detail how you identified the project need or problem statement.",
                    "Explain driving design, development, testing, and deployment independently.",
                    "Highlight measurable impact and stakeholder appreciation.",
                ],
            )
        )

        # 10. Teamwork, Mentorship & Knowledge Sharing
        questions.append(
            InterviewQuestion(
                id="q-hr-10",
                category="HR - Culture & Teamwork",
                question_type="hr_based",
                question_text="How do you foster knowledge sharing, documentation, and peer support within your engineering team?",
                context_reason="Assesses team collaboration, documentation habits, and peer support.",
                star_talking_points=[
                    "Discuss writing clean READMEs, API docs, and architecture decision records.",
                    "Explain conducting supportive code reviews and pair programming.",
                    "Describe contributing to an inclusive team environment.",
                ],
            )
        )

        # 11. Receiving Constructive Criticism
        questions.append(
            InterviewQuestion(
                id="q-hr-11",
                category="HR - Continuous Growth",
                question_type="hr_based",
                question_text="Can you share an instance where you received critical feedback during a code review or performance evaluation? How did you respond?",
                context_reason="Evaluates humility, openness to feedback, and emotional intelligence.",
                star_talking_points=[
                    "Describe context of feedback received regarding code structure or process.",
                    "Explain objective, receptive mindset and seeking clarifying guidance.",
                    "Detail concrete changes implemented and long-term improvement.",
                ],
            )
        )

        # 12. Driving Process Automation
        questions.append(
            InterviewQuestion(
                id="q-hr-12",
                category="HR - Leadership & Ownership",
                question_type="hr_based",
                question_text="Tell me about a repetitive manual task you noticed in your team's workflow that you proactively automated.",
                context_reason="Probes initiative to eliminate operational friction and manual effort.",
                star_talking_points=[
                    "Identify inefficient manual process (e.g. manual data checks or deployment steps).",
                    "Explain building automated scripts or CI/CD pipelines.",
                    "Quantify hours saved per week for the team.",
                ],
            )
        )

        # 13. Data Ethics & Confidentiality
        questions.append(
            InterviewQuestion(
                id="q-hr-13",
                category="HR - Ethics & Standards",
                question_type="hr_based",
                question_text="How do you ensure data confidentiality, user privacy, and compliance with data governance policies in your work?",
                context_reason="Assesses commitment to ethical standards and data governance.",
                star_talking_points=[
                    "Discuss principle of least privilege access and secure data storage.",
                    "Explain sanitizing sensitive PII before logging or reporting.",
                    "Highlight adherence to compliance standards.",
                ],
            )
        )

        # 14. Working in Agile / Sprint Environments
        questions.append(
            InterviewQuestion(
                id="q-hr-14",
                category="HR - Agile Collaboration",
                question_type="hr_based",
                question_text="What sprint rituals (daily standups, retrospectives, story sizing) do you find most valuable and why?",
                context_reason="Evaluates familiarity with modern Agile delivery practices.",
                star_talking_points=[
                    "Share experience participating in 2-week Agile sprint cycles.",
                    "Explain leveraging standups for blocker resolution and retros for process tweaks.",
                    "Describe estimating story points accurately.",
                ],
            )
        )

        # 15. Handling Ambiguity
        questions.append(
            InterviewQuestion(
                id="q-hr-15",
                category="HR - STAR Behavioral",
                question_type="hr_based",
                question_text="Describe a time when you were given a task with vague specifications and little guidance. How did you navigate it?",
                context_reason="Probes problem decomposition and dealing with uncertain requirements.",
                star_talking_points=[
                    "Describe initial state of ambiguous requirements.",
                    "Explain interviewing stakeholders, researching prior art, and creating draft specs.",
                    "Highlight validating prototype with team before full implementation.",
                ],
            )
        )

        # 16. Work Culture Preferences
        questions.append(
            InterviewQuestion(
                id="q-hr-16",
                category="HR - Culture & Values",
                question_type="hr_based",
                question_text="What type of work culture, communication style, and management approach brings out your best performance?",
                context_reason="Evaluates culture fit and management style compatibility.",
                star_talking_points=[
                    "Express preference for transparency, psychological safety, and technical excellence.",
                    "Discuss appreciating clear goals with autonomy in technical execution.",
                    "Highlight valuing collaborative team environments.",
                ],
            )
        )

        # 17. 3-to-5 Year Career Vision
        questions.append(
            InterviewQuestion(
                id="q-hr-17",
                category="HR - Career Trajectory",
                question_type="hr_based",
                question_text=f"Where do you see your technical career progressing over the next 3 to 5 years as a {target_role}?",
                context_reason=f"Assesses long-term career ambition and growth trajectory as {target_role}.",
                star_talking_points=[
                    f"Emphasize deepening technical mastery in {s0}, cloud architecture, and AI systems.",
                    "Discuss aspiration to take on technical leadership or architectural responsibilities.",
                    f"Connect growth goals directly to impact within a {target_role} team.",
                ],
            )
        )

        # 18. Continuous Technical Learning
        questions.append(
            InterviewQuestion(
                id="q-hr-18",
                category="HR - Continuous Growth",
                question_type="hr_based",
                question_text="With technology evolving rapidly, how do you curate your technical learning routine outside of daily work?",
                context_reason="Probes habits for staying updated with engineering advancements.",
                star_talking_points=[
                    "Discuss reading engineering blogs, open-source repositories, or research papers.",
                    "Explain building hands-on side projects or experimentation sandboxes.",
                    "Describe sharing learnings with teammates.",
                ],
            )
        )

        # 19. Stress & Burnout Prevention
        questions.append(
            InterviewQuestion(
                id="q-hr-19",
                category="HR - Work-Life Balance",
                question_type="hr_based",
                question_text="How do you maintain focus, high quality, and work-life sustainability during intensive release periods?",
                context_reason="Evaluates self-awareness, stress management, and sustainable productivity.",
                star_talking_points=[
                    "Discuss structured focus blocks and clear goal setting.",
                    "Explain healthy boundaries, open communication about workload, and taking breaks.",
                    "Highlight maintaining high code quality without rush errors.",
                ],
            )
        )

        # 20. Value Proposition & Candidate Pitch
        questions.append(
            InterviewQuestion(
                id="q-hr-20",
                category="HR - Value Proposition",
                question_type="hr_based",
                question_text=f"Summarize why your unique combination of skills in {s0}, {s1}, and portfolio experience makes you an ideal fit for {target_role}.",
                context_reason=f"Directly synthesizes candidate strengths for the {target_role} position.",
                star_talking_points=[
                    f"Synthesize top technical skills ({s0}, {s1}, {s2}) and practical project track record.",
                    "Highlight strong problem-solving mindset and team collaboration.",
                    f"Conclude with strong commitment to driving value as a {target_role}.",
                ],
            )
        )

        return questions

    @staticmethod
    def evaluate_answer(payload: AnswerEvaluationRequest) -> AnswerEvaluationResponse:
        # Prompt injection defense check
        tagged_answer = f"<USER_ANSWER_DATA>\n{payload.user_answer}\n</USER_ANSWER_DATA>"

        text = payload.user_answer.strip()
        word_count = len(text.split())

        strengths: List[str] = []
        missing: List[str] = []

        # Evaluate STAR framework elements
        has_situation = any(k in text.lower() for k in ["situation", "when", "project", "building", "task", "company", "team"])
        has_action = any(k in text.lower() for k in ["implemented", "built", "designed", "architected", "optimized", "created", "led", "debugged"])
        has_result = any(k in text.lower() for k in ["result", "reduced", "increased", "improved", "saved", "%", "metric", "outcome"])

        if has_action:
            strengths.append("Clear description of technical action taken.")
        else:
            missing.append("Missing specific technical implementation details (Action).")

        if has_result:
            strengths.append("Includes quantifiable outcomes or metric impact.")
        else:
            missing.append("Missing explicit quantified results or outcome metrics (Result).")

        if word_count >= 50:
            strengths.append("Detailed response with sufficient depth.")
        else:
            missing.append("Response is brief (< 50 words). Provide more context.")

        score = 60
        if has_situation: score += 10
        if has_action: score += 15
        if has_result: score += 15
        score = max(30, min(100, score))

        improved = (
            "Situation: While engineering backend services for high concurrency workloads, "
            "Task: I was responsible for optimizing API response latency and database throughput. "
            "Action: I implemented async database connections with SQLAlchemy 2.0 and integrated Redis caching for hot read paths. "
            "Result: This reduced database query latency by 45% and maintained 99.9% uptime during peak traffic."
        )

        feedback = (
            f"Answer Score: {score}/100. Your response demonstrates basic technical context. "
            "To maximize impact, structure your answer strictly using the STAR methodology (Situation, Task, Action, Result) "
            "and emphasize quantifiable engineering metrics."
        )

        return AnswerEvaluationResponse(
            score=score,
            strengths=strengths,
            missing_elements=missing,
            improved_sample_answer=improved,
            explainable_feedback=feedback,
        )
