from sqlalchemy import Column, Integer, String, DateTime, func
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

class Candidate(Base):
    __tablename__ = "hr_candidates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    status = Column(String(50), default="Pending")  # Passed, Pending, Failed

    # Marks (int out of 25 each — exactly matching DB schema)
    written_test = Column(Integer, default=0)
    technical_assessment = Column(Integer, default=0)
    pm_assessment = Column(Integer, default=0)
    hr_evaluation = Column(Integer, default=0)
    
    total_score = Column(Integer, default=0)
