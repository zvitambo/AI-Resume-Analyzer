"""
app/services/scoring_service.py

Resume-to-Job Description Scoring Service

Responsibilities
----------------
- Compare resume skills against required and preferred job skills.
- Calculate an overall match score.
- Return detailed scoring information that can be used by the LLM
  to generate explanations.

This module is intentionally independent from any LLM provider.
"""

from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------

@dataclass
class SkillMatchResult:
    """
    Detailed results of the skill comparison.
    """

    score: float

    matched_required: List[str]
    missing_required: List[str]

    matched_preferred: List[str]
    missing_preferred: List[str]


# ---------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------

def normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalize skills to make comparison more reliable.

    Example:
        [" Python ", "FASTAPI", "docker"]
        ->
        ["python", "fastapi", "docker"]
    """

    return sorted(
        {
            skill.strip().lower()
            for skill in skills
            if skill and skill.strip()
        }
    )


# ---------------------------------------------------------------------
# Core Scoring Logic
# ---------------------------------------------------------------------

def calculate_skill_match(
    resume_skills: List[str],
    required_skills: List[str],
) -> float:
    """
    Calculate percentage match using only required skills.

    Returns:
        float between 0 and 100
    """

    resume = set(normalize_skills(resume_skills))
    required = set(normalize_skills(required_skills))

    if not required:
        return 100.0

    matched = resume.intersection(required)

    return round((len(matched) / len(required)) * 100, 2)


# ---------------------------------------------------------------------
# Weighted Match
# ---------------------------------------------------------------------

def calculate_weighted_match(
    resume_skills: List[str],
    required_skills: List[str],
    preferred_skills: List[str] | None = None,
    required_weight: float = 0.80,
    preferred_weight: float = 0.20,
) -> SkillMatchResult:
    """
    Calculate a weighted score.

    Default weights:

        Required Skills  -> 80%
        Preferred Skills -> 20%

    Example:

        Required:
            Python
            FastAPI
            Docker

        Preferred:
            Azure
            Kubernetes

        Resume:
            Python
            FastAPI
            Azure

        Required score = 2 / 3 = 66.7%

        Preferred score = 1 / 2 = 50%

        Final score =
            (66.7 * 0.8) +
            (50 * 0.2)

            = 63.36
    """

    preferred_skills = preferred_skills or []

    resume = set(normalize_skills(resume_skills))
    required = set(normalize_skills(required_skills))
    preferred = set(normalize_skills(preferred_skills))

    # -----------------------------
    # Required Skills
    # -----------------------------

    matched_required = sorted(resume & required)
    missing_required = sorted(required - resume)

    if required:
        required_score = (
            len(matched_required) / len(required)
        ) * 100
    else:
        required_score = 100

    # -----------------------------
    # Preferred Skills
    # -----------------------------

    matched_preferred = sorted(resume & preferred)
    missing_preferred = sorted(preferred - resume)

    if preferred:
        preferred_score = (
            len(matched_preferred) / len(preferred)
        ) * 100
    else:
        preferred_score = 100

    # -----------------------------
    # Final Weighted Score
    # -----------------------------

    final_score = (
        required_score * required_weight
        + preferred_score * preferred_weight
    )

    return SkillMatchResult(
        score=round(final_score, 2),
        matched_required=matched_required,
        missing_required=missing_required,
        matched_preferred=matched_preferred,
        missing_preferred=missing_preferred,
    )