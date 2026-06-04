import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.models import Candidate as CandidateModel, User
from backend.schemas.candidate import Candidate, CandidateCreate, CandidateUpdate
from backend.database import get_db
from backend.services.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["candidates"])

@router.post("/add-candidate", response_model=Candidate)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if candidate with same email already exists
    existing = db.query(CandidateModel).filter(CandidateModel.email == candidate.email).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Candidate with email {candidate.email} already exists.")

    try:
        # Create model instance, converting scores to int explicitly
        db_candidate = CandidateModel(
            name=candidate.name,
            email=candidate.email,
            role=candidate.role,
            status=candidate.status,
            written_test=int(round(candidate.written_test or 0)),
            technical_assessment=int(round(candidate.technical_assessment or 0)),
            pm_assessment=int(round(candidate.pm_assessment or 0)),
            hr_evaluation=int(round(candidate.hr_evaluation or 0))
        )

        # Calculate total score internally
        db_candidate.total_score = (
            db_candidate.written_test +
            db_candidate.technical_assessment +
            db_candidate.pm_assessment +
            db_candidate.hr_evaluation
        )

        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        logger.info(f"✅ Candidate added: {db_candidate.name} (id={db_candidate.id})")
        return db_candidate
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/candidates", response_model=List[Candidate])
def read_candidates(skip: int = 0, limit: int = 5000, db: Session = Depends(get_db)):
    results = db.query(CandidateModel).offset(skip).limit(limit).all()
    logger.info(f"📋 GET /candidates → returned {len(results)} records (skip={skip}, limit={limit})")
    return results

@router.get("/candidates/{candidate_id}", response_model=Candidate)
def read_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.put("/candidates/{candidate_id}", response_model=Candidate)
def update_candidate(candidate_id: int, candidate_update: CandidateUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if db_candidate:
        update_data = candidate_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_candidate, key, value)
        
        # Recalculate total score
        total = (db_candidate.written_test or 0) + \
                (db_candidate.technical_assessment or 0) + \
                (db_candidate.pm_assessment or 0) + \
                (db_candidate.hr_evaluation or 0)
        db_candidate.total_score = total

        db.commit()
        db.refresh(db_candidate)
        # AI cache invalidation removed as AI fetches directly from DB now.
        return db_candidate
    raise HTTPException(status_code=404, detail="Candidate not found")

@router.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
        # AI cache invalidation removed as AI fetches directly from DB now.
        return {"message": "Candidate deleted successfully"}
    raise HTTPException(status_code=404, detail="Candidate not found")
