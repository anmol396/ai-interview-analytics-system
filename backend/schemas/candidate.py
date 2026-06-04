from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    email: str
    role: str
    status: str = "Pending"

class CandidateCreate(CandidateBase):
    written_test: int = 0
    technical_assessment: int = 0
    pm_assessment: int = 0
    hr_evaluation: int = 0

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    written_test: Optional[int] = None
    technical_assessment: Optional[int] = None
    pm_assessment: Optional[int] = None
    hr_evaluation: Optional[int] = None

class Candidate(CandidateBase):
    id: int
    written_test: int
    technical_assessment: int
    pm_assessment: int
    hr_evaluation: int
    total_score: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
