from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    match_score: float
    strengths: list[str]
    missing_skills: list[str]
    recommendations: list[str]
