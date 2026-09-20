from typing import List, Dict, Any
from app.domain.schemas.structured_resume import StructuredResume


class AIAuditorService:
    @staticmethod
    def generate_recommendations(
        structured_resume: StructuredResume,
        deterministic_res: Dict[str, Any]
    ) -> List[str]:
        recommendations: List[str] = []

        # Check contact details
        info = structured_resume.personal_info
        if not info.email or not info.phone:
            recommendations.append("Ensure phone number and professional email are prominently displayed at the top of your resume.")
        if not info.linkedin_url:
            recommendations.append("Add a customized LinkedIn profile URL to increase recruiter trust and ATS verification.")
        if not info.summary and not structured_resume.summary:
            recommendations.append("Add a concise 2-3 sentence Professional Summary highlighting your core technical expertise and target role.")

        # Check experience & metrics
        if deterministic_res["experience_score"] < 75:
            recommendations.append("Enhance work experience bullet points with quantified results (e.g. 'Increased throughput by 35%', 'Managed $50k budget').")

        # Check action verbs
        if deterministic_res["content_quality_score"] < 75:
            recommendations.append("Start every bullet point in your Work Experience section with strong action verbs (e.g., 'Architected', 'Engineered', 'Optimized').")

        # Check skills
        if len(structured_resume.skills.technical_skills) < 5:
            recommendations.append("Group your technical skills into explicit categories (Languages, Frameworks, Databases, Cloud & DevOps).")

        # Check projects
        if len(structured_resume.projects) == 0:
            recommendations.append("Add a Projects section featuring 1-2 key technical projects with repository or live demo links.")

        if len(recommendations) == 0:
            recommendations.append("Maintain resume alignment with target job descriptions by tailoring skill keywords for each application.")

        return recommendations
