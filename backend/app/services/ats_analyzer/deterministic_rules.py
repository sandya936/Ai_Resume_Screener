import re
from typing import List, Dict, Any, Tuple
from app.domain.schemas.structured_resume import StructuredResume
from app.domain.schemas.ats_analysis import ScoringReason

STRONG_ACTION_VERBS = {
    "architected", "spearheaded", "engineered", "optimized", "implemented",
    "designed", "led", "developed", "managed", "accelerated", "reduced",
    "increased", "built", "automated", "delivered", "formulated",
    "orchestrated", "scaled", "transformed", "established", "created",
    "launched", "deployed", "refactored", "migrated", "pioneered",
    "analyzed", "visualized", "calculated", "performed", "executed",
    "maintained", "collaborated", "extracted", "cleansed", "modeled",
    "modelled", "reported", "presented", "structured", "configured",
}

QUANTIFIED_METRIC_PATTERNS = [
    r"\d+%",                         # Percentages e.g. 40%
    r"\$\d+(?:\.\d+)?[kKmMbB]?",    # Dollar amounts e.g. $100k, $2M
    r"\d+x",                         # Multipliers e.g. 3x
    r"\b\d+[kKmMbB]\b",              # Abbreviated numbers e.g. 10M, 50k
    r"\b(?:reduced|decreased|improved|increased|boosted|grew|saved|cut|processed|analyzed|visualized|built|created)\b.*?\b\d+", # Action + Number
    r"\b\d+\+?\s+(?:users|customers|clients|requests|transactions|services|projects|teams|million|thousand|k|m|dashboards|reports|datasets|records|rows)\b",
]


class DeterministicRulesEngine:
    @staticmethod
    def evaluate(structured_resume: StructuredResume, raw_text: str) -> Dict[str, Any]:
        reasons: List[ScoringReason] = []
        strengths: List[str] = []
        weaknesses: List[str] = []
        warnings: List[str] = []

        # 1. Completeness Check
        info = structured_resume.personal_info
        has_email = bool(info.email)
        has_phone = bool(info.phone)
        has_name = bool(info.full_name and info.full_name != "Candidate Name")
        has_summary = bool(structured_resume.summary or info.summary)
        has_work = len(structured_resume.work_experience) > 0
        has_edu = len(structured_resume.education) > 0
        has_skills = (
            len(structured_resume.skills.technical_skills) > 0
            or len(structured_resume.skills.tools_and_frameworks) > 0
            or len(structured_resume.skills.soft_skills) > 0
        )

        completeness_score = 0
        if has_name: completeness_score += 10
        if has_email: completeness_score += 20
        if has_phone: completeness_score += 10
        if has_summary: completeness_score += 15
        if has_work: completeness_score += 25
        if has_edu: completeness_score += 10
        if has_skills: completeness_score += 10

        if completeness_score >= 85:
            strengths.append("Complete resume structure with all major professional sections.")
            reasons.append(ScoringReason(type="positive", message="Resume includes all core standard sections.", category="Completeness"))
        else:
            if not has_email or not has_phone:
                weaknesses.append("Missing complete contact details (email/phone).")
                warnings.append("Contact information incomplete. ATS parsers need phone and email.")
                reasons.append(ScoringReason(type="negative", message="Missing email or phone number in contact info.", category="Completeness"))
            if not has_work:
                weaknesses.append("No work experience entries detected.")
                reasons.append(ScoringReason(type="negative", message="Missing Work Experience section.", category="Completeness"))

        # 2. Action Verbs & Experience Quality Check
        all_bullet_text = []
        for exp in structured_resume.work_experience:
            all_bullet_text.extend(exp.accomplishments)
            if exp.description:
                all_bullet_text.append(exp.description)
        for proj in structured_resume.projects:
            if proj.description:
                all_bullet_text.append(proj.description)

        combined_text = " ".join(all_bullet_text) + " " + raw_text
        words_in_text = set(re.findall(r"\b[a-zA-Z]+\b", combined_text.lower()))

        action_verbs_found = words_in_text.intersection(STRONG_ACTION_VERBS)
        verb_count = len(action_verbs_found)

        if verb_count >= 4:
            action_verb_score = 90
            strengths.append(f"Strong usage of high-impact action verbs ({', '.join(list(action_verbs_found)[:4]).title()}).")
            reasons.append(ScoringReason(type="positive", message=f"Identified {verb_count} strong action verbs in experience bullets.", category="Content Quality"))
        elif verb_count >= 2:
            action_verb_score = 75
            reasons.append(ScoringReason(type="positive", message="Contains basic action verbs.", category="Content Quality"))
        else:
            action_verb_score = 50
            weaknesses.append("Low density of active impact action verbs.")
            reasons.append(ScoringReason(type="negative", message="Weak action verb density in job accomplishments.", category="Content Quality"))

        # 3. Quantified Impact Metrics Check
        metrics_found = []
        for pattern in QUANTIFIED_METRIC_PATTERNS:
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            metrics_found.extend(matches)

        metric_count = len(metrics_found)
        if metric_count >= 2:
            impact_score = 90
            strengths.append(f"Quantified metrics and achievements ({', '.join(metrics_found[:3])}).")
            reasons.append(ScoringReason(type="positive", message=f"Found {metric_count} quantified performance metrics.", category="Experience"))
        elif metric_count >= 1:
            impact_score = 75
            reasons.append(ScoringReason(type="positive", message="Contains some quantified performance numbers.", category="Experience"))
        else:
            impact_score = 45
            weaknesses.append("Missing quantifiable metrics (percentages, dollar values, efficiency improvements).")
            reasons.append(ScoringReason(type="negative", message="No clear metrics or percentages found in achievements.", category="Experience"))

        # 4. ATS Formatting Risks & Keyword Check
        ats_score = 85
        if not has_email or not has_phone:
            ats_score -= 20
        if re.search(r"[\u25a0-\u25ff\u2600-\u26ff]", raw_text): # Unusual geometric shapes/symbols
            ats_score -= 10
            warnings.append("Unusual graphical symbols detected which may distort ATS parsing.")
            reasons.append(ScoringReason(type="warning", message="Unusual unicode symbols found.", category="ATS Compatibility"))

        words = raw_text.split()
        word_count = len(words)
        if word_count < 80:
            ats_score -= 15
            warnings.append("Resume text is very short (< 80 words).")
        elif word_count > 1500:
            ats_score -= 10
            warnings.append("Resume text is lengthy (> 1500 words). Consider condensing to 1-2 pages.")

        ats_score = max(30, min(100, ats_score))

        # 5. Skills Score
        all_candidate_skills = (
            structured_resume.skills.technical_skills
            + structured_resume.skills.tools_and_frameworks
            + structured_resume.skills.soft_skills
        )
        tech_skills_count = len(set(all_candidate_skills))
        if tech_skills_count >= 4:
            skills_score = 90
            strengths.append(f"Diverse technical skill presentation ({', '.join(all_candidate_skills[:4])}).")
        elif tech_skills_count >= 2:
            skills_score = 75
        else:
            skills_score = 50
            weaknesses.append("Technical skills section is sparse.")

        # 6. Projects Score
        proj_count = len(structured_resume.projects)
        if proj_count >= 2:
            projects_score = 85
        elif proj_count == 1:
            projects_score = 70
        else:
            projects_score = 50

        # 7. Education Score
        education_score = 85 if has_edu else 40

        return {
            "ats_compatibility_score": ats_score,
            "content_quality_score": int((action_verb_score * 0.5) + (impact_score * 0.5)),
            "skills_score": skills_score,
            "experience_score": impact_score,
            "projects_score": projects_score,
            "education_score": education_score,
            "completeness_score": completeness_score,
            "reasons": reasons,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "warnings": warnings,
        }
