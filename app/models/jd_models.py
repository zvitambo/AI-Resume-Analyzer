from pydantic import BaseModel
from typing import List


class JobDescriptionData(BaseModel):
    title: str | None = None
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    responsibilities: list[str] = []