from pydantic import BaseModel
from typing import List

class ResumeData(BaseModel):
    name: str | None = None
    skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []