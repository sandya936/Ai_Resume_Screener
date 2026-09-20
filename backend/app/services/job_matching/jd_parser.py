import re
from typing import List, Dict, Set
from app.domain.schemas.job_description import ParsedJobDescription

SKILL_NORMALIZATION_MAP: Dict[str, str] = {
    "k8s": "kubernetes",
    "kube": "kubernetes",
    "kubernetes": "kubernetes",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "psql": "postgresql",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "py": "python",
    "python": "python",
    "reactjs": "react",
    "react.js": "react",
    "react": "react",
    "nextjs": "next.js",
    "next.js": "next.js",
    "node": "node.js",
    "nodejs": "node.js",
    "node.js": "node.js",
    "aws": "aws",
    "amazon web services": "aws",
    "gcp": "gcp",
    "google cloud": "gcp",
    "docker": "docker",
    "containerization": "docker",
    "fastapi": "fastapi",
    "sql": "sql",
    "nosql": "nosql",
    "mongodb": "mongodb",
    "redis": "redis",
    "git": "git",
    "github": "git",
    "ci/cd": "ci/cd",
    "cicd": "ci/cd",
    "power bi": "power bi",
    "powerbi": "power bi",
    "tableau": "tableau",
    "pandas": "pandas",
    "numpy": "numpy",
    "excel": "excel",
    "vlookup": "vlookup",
    "pivot tables": "pivot tables",
    "data visualization": "data visualization",
    "data analysis": "data analysis",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "r": "r",
    "tidyverse": "tidyverse",
}

KNOWN_TECH_KEYWORDS = [
    # Data Analysis & BI
    "Pandas", "NumPy", "Power BI", "Tableau", "Excel", "VLOOKUP", "Pivot Tables",
    "SQL", "R", "Tidyverse", "Data Visualization", "Data Analysis", "Snowflake",
    "BigQuery", "Looker", "ETL", "Statistics", "A/B Testing",
    # Data Science & Machine Learning
    "Scikit-Learn", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning",
    "NLP", "Spark", "Hadoop", "Airflow", "Data Mining",
    # Software Engineering & Languages
    "Python", "Java", "C++", "C#", ".NET", "Go", "Rust", "PHP", "Ruby", "Scala",
    "FastAPI", "Django", "Flask", "Spring Boot",
    # Frontend & Web UI
    "React", "Next.js", "TypeScript", "JavaScript", "HTML", "CSS", "Tailwind",
    "Vue", "Angular", "Node.js", "Redux", "Redux Toolkit", "Zustand", "Pinia", "Nuxt",
    "Context API", "Webpack", "Vite", "Jest", "React Testing Library", "Cypress",
    "Playwright", "WCAG", "Micro-frontend", "SSR", "SSG", "Vercel", "Netlify",
    "State Management", "Figma", "Sass", "Bootstrap",
    # Cloud, DevOps & Database
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra", "Docker", "Kubernetes",
    "AWS", "GCP", "Azure", "Git", "GitHub", "CI/CD", "Linux", "GraphQL", "REST API", "Kafka",
]


class SkillNormalizer:
    @staticmethod
    def normalize(skill: str) -> str:
        s = skill.strip().lower()
        return SKILL_NORMALIZATION_MAP.get(s, s)

    @staticmethod
    def normalize_list(skills: List[str]) -> List[str]:
        seen: Set[str] = set()
        result: List[str] = []
        for sk in skills:
            norm = SkillNormalizer.normalize(sk)
            if norm and norm not in seen:
                seen.add(norm)
                result.append(norm)
        return result


class JobDescriptionParserService:
    @staticmethod
    def parse_text(title: str, company_name: str, raw_text: str) -> ParsedJobDescription:
        # Prompt injection defense container tagging
        tagged_jd_text = f"<JOB_DESCRIPTION_DATA>\n{raw_text}\n</JOB_DESCRIPTION_DATA>"

        # Extract required vs preferred skills using regex heuristics
        required_skills: List[str] = []
        preferred_skills: List[str] = []

        # Find tech keywords present in raw_text
        found_tech = []
        for kw in KNOWN_TECH_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", raw_text, re.IGNORECASE):
                found_tech.append(kw)

        # Dynamic extraction for any comma-separated or bulleted technical tools
        pattern_tools = r"(?:tools|libraries|skills|technologies|proficient in|experience with|knowledge of)\s*[:\-\s]+([^.\n]+)"
        matches = re.findall(pattern_tools, raw_text, re.IGNORECASE)
        for m in matches:
            parts = re.split(r"[,;|\n/]|and\b|or\b", m)
            for item in parts:
                clean_item = item.strip(" ()[]*•-").title()
                if len(clean_item) >= 2 and len(clean_item) <= 30 and clean_item not in found_tech:
                    found_tech.append(clean_item)

        # Check for explicit preferred/nice-to-have section using regex DOTALL
        pref_match = re.search(r"(?:preferred|nice to have|plus|bonus|desired)([\s\S]*)$", raw_text, re.IGNORECASE)
        if pref_match:
            pref_text = pref_match.group(1)
            for kw in KNOWN_TECH_KEYWORDS:
                if re.search(r"\b" + re.escape(kw) + r"\b", pref_text, re.IGNORECASE):
                    preferred_skills.append(kw)
            required_skills = [k for k in found_tech if k not in preferred_skills]
        else:
            required_skills = found_tech
            preferred_skills = []

        # Normalize skill synonyms
        norm_required = SkillNormalizer.normalize_list(required_skills)
        norm_preferred = SkillNormalizer.normalize_list(preferred_skills)

        # Extract experience & education requirements
        exp_match = re.search(r"(\d+\+?\s*(?:-\s*\d+)?\s*(?:years?|yrs?))", raw_text, re.IGNORECASE)
        edu_match = re.search(r"(bachelor|master|phd|degree|b\.s|m\.s|computer science|data science|statistics|mathematics)", raw_text, re.IGNORECASE)

        default_domain = "Data Analysis & Business Intelligence" if any(k in raw_text.lower() for k in ["analyst", "data", "tableau", "power bi", "excel", "sql"]) else "Software Engineering"

        return ParsedJobDescription(
            title=title,
            company_name=company_name,
            required_skills=norm_required if norm_required else [title.lower() if title else "data analysis"],
            preferred_skills=norm_preferred,
            technologies=norm_required + norm_preferred,
            responsibilities=["Execute core responsibilities, engineering workflows, and system optimization."],
            experience_requirements=exp_match.group(0) if exp_match else "0-2+ years",
            education_requirements=edu_match.group(0).title() if edu_match else "Bachelor's Degree",
            domain_knowledge=[default_domain, "Domain Intelligence"],
            keywords=norm_required + norm_preferred,
        )
