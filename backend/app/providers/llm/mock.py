import re
from typing import List
from app.providers.llm.base import BaseLLMProvider
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    EducationEntry,
    WorkExperienceEntry,
    SkillCategory,
    ProjectEntry,
    CertificationEntry,
)


import re
from typing import List
from app.providers.llm.base import BaseLLMProvider
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    EducationEntry,
    WorkExperienceEntry,
    SkillCategory,
    ProjectEntry,
    CertificationEntry,
)

ALL_TECH_KEYWORDS = [
    # Data Analysis, BI & Viz
    "Power BI", "Tableau", "Plotly", "Streamlit", "Excel", "DAX", "Power Query",
    "EDA", "Statistical Analysis", "Data Cleaning", "Data Wrangling", "Correlation & Trend Analysis",
    "Python", "SQL", "pandas", "NumPy", "Matplotlib", "Seaborn", "scikit-learn",
    "MySQL", "MongoDB", "GitHub", "Jupyter Notebook", "VLOOKUP", "Pivot Tables",
    "R", "Tidyverse", "Spark", "Hadoop", "Airflow", "Snowflake", "BigQuery", "Looker", "ETL",
    "Data Visualization", "Data Analysis", "Machine Learning", "Deep Learning", "NLP",
    # Software Engineering & Web
    "FastAPI", "Flask", "Django", "React", "Next.js", "TypeScript", "JavaScript",
    "HTML", "CSS", "Tailwind", "PostgreSQL", "Docker", "Kubernetes", "AWS", "GCP",
    "Git", "REST API", "GraphQL", "Java", "C++", "C#", ".NET", "Go", "Rust", "Node.js"
]

SOFT_SKILLS_KEYWORDS = [
    "Leadership", "Communication", "Problem Solving", "Teamwork", "Agile", "Scrum",
    "Critical Thinking", "Analytical Mindset", "Attention to Detail", "Time Management"
]


class MockDeterministicLLMProvider(BaseLLMProvider):
    async def parse_resume_text(self, raw_text: str) -> StructuredResume:
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

        # 1. Personal Info Extraction
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
        phone_match = re.search(r"[\+\(]?[0-9\s\-\.\(\)]{8,16}", raw_text)
        linkedin_match = re.search(r"((?:https?://)?(?:www\.)?linkedin\.com/[^\s\|,\n]+)", raw_text, re.IGNORECASE)
        github_match = re.search(r"((?:https?://)?(?:www\.)?github\.com/[^\s\|,\n]+)", raw_text, re.IGNORECASE)

        # Name extraction: find first clean line that isn't email, phone, or link header
        full_name = "Candidate Name"
        for line in lines[:5]:
            clean_l = re.sub(r"(?:✉|Mail|phone|Contact|linkedin|LinkedIn|github|GitHub|OBJECTIVE|SUMMARY|PROFILE|[\d\+\(\)\-\|\/])+", "", line, flags=re.IGNORECASE).strip()
            if clean_l and len(clean_l) >= 3 and not re.search(r"@|\.(com|org|net|in)|http", clean_l, re.IGNORECASE):
                full_name = clean_l
                break

        # Summary extraction from Objective / Summary section
        summary_text = ""
        obj_match = re.search(r"(?:OBJECTIVE|SUMMARY|PROFILE)\s*\n+([^.\n]+\.[^.\n]+\.?)", raw_text, re.IGNORECASE)
        if obj_match:
            summary_text = obj_match.group(1).strip()
        elif len(lines) > 2:
            summary_text = " ".join(lines[1:3])
        else:
            summary_text = "Motivated professional with hands-on technical skills and project experience."

        personal_info = PersonalInfo(
            full_name=full_name,
            email=email_match.group(0) if email_match else None,
            phone=phone_match.group(0).strip() if phone_match else None,
            linkedin_url=linkedin_match.group(0) if linkedin_match else None,
            github_url=github_match.group(0) if github_match else None,
            summary=summary_text,
        )

        # 2. Skills Extraction (Dynamic Keyword Match + Section Parsing)
        found_tech: List[str] = []
        for kw in ALL_TECH_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", raw_text, re.IGNORECASE):
                found_tech.append(kw)

        found_soft: List[str] = []
        for kw in SOFT_SKILLS_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", raw_text, re.IGNORECASE):
                found_soft.append(kw)

        # Direct extraction from TECHNICAL SKILLS section
        skills_sec_match = re.search(r"(?:TECHNICAL SKILLS|SKILLS)\s*:?\s*\n((?:[^\n]+\n){1,8})", raw_text, re.IGNORECASE)
        if skills_sec_match:
            sec_lines = skills_sec_match.group(1).split("\n")
            for sl in sec_lines:
                sl_clean = re.sub(r"^[\bullet\-\*•\s]+", "", sl).strip()
                if sl_clean and ":" in sl_clean:
                    tools_part = sl_clean.split(":", 1)[1]
                    for t in re.split(r"[,;(/)]", tools_part):
                        t_clean = t.strip()
                        if t_clean and len(t_clean) <= 30 and t_clean not in found_tech:
                            found_tech.append(t_clean)

        tech_list = found_tech if found_tech else ["Data Analysis", "Python"]
        soft_list = found_soft if found_soft else ["Problem Solving", "Communication"]
        tools_list = [t for t in tech_list if t.lower() in ["power bi", "tableau", "excel", "git", "github", "jupyter notebook", "vscode", "docker", "dax", "power query"]]

        skills = SkillCategory(
            technical_skills=tech_list,
            soft_skills=soft_list,
            tools_and_frameworks=tools_list if tools_list else ["Git", "Excel"],
        )

        # 3. Dynamic Projects Extraction (Parse actual projects from raw_text!)
        projects: List[ProjectEntry] = []
        proj_sec_match = re.search(r"PROJECTS\s*:?\s*\n((?:[^\n]+\n){1,25})", raw_text, re.IGNORECASE)
        if proj_sec_match:
            proj_block = proj_sec_match.group(1)
            # Find project title lines (lines that don't start with bullet points)
            p_lines = [pl.strip() for pl in proj_block.split("\n") if pl.strip()]
            current_proj_title = ""
            current_bullets: List[str] = []
            for pl in p_lines:
                if re.match(r"^[\bullet\-\*•]", pl) or pl.startswith("- ") or pl.startswith("• "):
                    if current_proj_title:
                        current_bullets.append(re.sub(r"^[\bullet\-\*•\s]+", "", pl))
                else:
                    if current_proj_title:
                        proj_tech = [t for t in tech_list if re.search(r"\b" + re.escape(t) + r"\b", current_proj_title + " ".join(current_bullets), re.IGNORECASE)]
                        projects.append(
                            ProjectEntry(
                                title=current_proj_title,
                                description=" ".join(current_bullets[:2]) if current_bullets else "Featured candidate portfolio project.",
                                technologies=proj_tech[:4] if proj_tech else tech_list[:3],
                            )
                        )
                        current_bullets = []
                    # Clean project title
                    clean_title = re.sub(r"[\-—–\s]*(?:GitHub|Power BI|Tableau|Flask|Python|Link)*$", "", pl, flags=re.IGNORECASE).strip()
                    current_proj_title = clean_title or pl

            if current_proj_title:
                proj_tech = [t for t in tech_list if re.search(r"\b" + re.escape(t) + r"\b", current_proj_title + " ".join(current_bullets), re.IGNORECASE)]
                projects.append(
                    ProjectEntry(
                        title=current_proj_title,
                        description=" ".join(current_bullets[:2]) if current_bullets else "Featured candidate portfolio project.",
                        technologies=proj_tech[:4] if proj_tech else tech_list[:3],
                    )
                )

        if not projects:
            projects.append(
                ProjectEntry(
                    title=f"{full_name}'s {tech_list[0]} Portfolio Project",
                    description=f"Developed interactive data models and analytical solutions using {', '.join(tech_list[:3])}.",
                    technologies=tech_list[:3],
                )
            )

        # 4. Dynamic Work Experience Extraction
        work_experience: List[WorkExperienceEntry] = []
        exp_sec_match = re.search(r"(?:EXPERIENCE|WORK EXPERIENCE|INTERNSHIPS)\s*:?\s*\n((?:[^\n]+\n){1,20})", raw_text, re.IGNORECASE)
        if exp_sec_match:
            exp_lines = [el.strip() for el in exp_sec_match.group(1).split("\n") if el.strip()]
            if exp_lines:
                work_experience.append(
                    WorkExperienceEntry(
                        company=exp_lines[0],
                        title=exp_lines[1] if len(exp_lines) > 1 else "Data Analytics / Technical Intern",
                        location="Remote",
                        start_date="2023",
                        end_date="Present",
                        is_current=True,
                        description="Executed technical workflows, data analysis, and dashboard visualization.",
                        accomplishments=[l for l in exp_lines[2:] if len(l) > 15][:3],
                        technologies=tech_list[:3],
                    )
                )

        if not work_experience:
            work_experience.append(
                WorkExperienceEntry(
                    company=f"{full_name} Academic & Internship Portfolio",
                    title="Data Analytics & Visualization Candidate",
                    location="India",
                    start_date="2023",
                    end_date="Present",
                    is_current=True,
                    description=f"Hands-on data visualization, analytics, and software project experience.",
                    accomplishments=[
                        f"Transformed multi-source datasets into interactive dashboards using {', '.join(tech_list[:3])}.",
                        "Executed statistical data cleaning, trend analysis, and performance metrics validation."
                    ],
                    technologies=tech_list[:3],
                )
            )

        # 5. Dynamic Education Extraction
        education: List[EducationEntry] = []
        edu_sec_match = re.search(r"EDUCATION\s*:?\s*\n((?:[^\n]+\n){1,6})", raw_text, re.IGNORECASE)
        if edu_sec_match:
            e_lines = [el.strip() for el in edu_sec_match.group(1).split("\n") if el.strip()]
            degree_str = "Bachelor of Technology"
            inst_str = "Engineering Institute"
            if len(e_lines) > 0:
                first_line = e_lines[0]
                if " - " in first_line:
                    parts = first_line.split(" - ", 1)
                    degree_str = parts[0].strip()
                    inst_str = parts[1].strip()
                elif len(e_lines) > 1:
                    degree_str = e_lines[0]
                    inst_str = e_lines[1]
                else:
                    inst_str = first_line
            education.append(
                EducationEntry(
                    institution=inst_str,
                    degree=degree_str,
                    field_of_study="Computer Science & Data Science",
                    start_date="2023",
                    end_date="2027",
                )
            )
        else:
            education.append(
                EducationEntry(
                    institution="Engineering Institute",
                    degree="Bachelor of Technology",
                    field_of_study="Computer Science & Data Science",
                    start_date="2023",
                    end_date="2027",
                )
            )

        return StructuredResume(
            personal_info=personal_info,
            summary=summary_text,
            education=education,
            work_experience=work_experience,
            skills=skills,
            projects=projects,
            certifications=[],
            achievements=[],
            publications=[],
            links=[],
        )

