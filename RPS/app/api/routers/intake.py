from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import schemas
import json

router = APIRouter(prefix="/intake", tags=["Intake Pipeline"])

# ==========================================
# PYDANTIC SCHEMAS (Matches Member 2 Contract)
# ==========================================
class AIHandshakePayload(BaseModel):
    job_id: int = Field(..., description="ID of the job posting")
    source_mode: str = Field(..., description="'manual_upload' or 'auto_fetched'")
    parse_status: str = Field(..., description="'SUCCESS' or 'FAILED'")
    
    candidate_profile: Dict[str, Any] = Field(..., description="Basic details: name, email, cgpa, degree, batch")
    similarity_scores: Dict[str, float] = Field(
        ..., 
        description="Must contain keys: projects, skills, experience, global. Range 0.0-1.0"
    )
    extracted_json: Dict[str, Any] = Field(..., description="The full 80+ node parsed resume")
    authenticity_score: float = Field(1.0, description="1.0 means perfect trust")
    
    has_hidden_text: bool = Field(False)
    has_date_overlap: bool = Field(False)
    has_keyword_stuffing: bool = Field(False)
    unverified_skills_count: int = Field(0)

# ==========================================
# ENDPOINTS
# ==========================================
@router.post("/auto-fetch/{job_id}", summary="Member 2 Automated Upload Endpoint")
def intake_auto_fetch(job_id: int, payload: AIHandshakePayload, db: Session = Depends(get_db)):
    """
    Endpoint for Member 2's AI to upload parsed results automatically.
    This saves exactly to the candidate and parsed_resume tables.
    """
    try:
        # 1. Create the Candidate securely
        new_candidate = schemas.Candidate(
            name=payload.candidate_profile.get("name", "Unknown"),
            email=payload.candidate_profile.get("email"),
            cgpa=payload.candidate_profile.get("cgpa"),
            degree=payload.candidate_profile.get("degree"),
            batch=payload.candidate_profile.get("batch"),
            source_mode="auto_fetched"
        )
        db.add(new_candidate)
        db.flush() # Securely get the ID before committing
        
        # 2. Save the AI's Brain Dump
        new_resume = schemas.ParsedResume(
            candidate_id=new_candidate.id,
            job_id=job_id,
            extracted_json=payload.extracted_json,
            parse_status=payload.parse_status,
            ai_confidence=payload.authenticity_score
        )
        db.add(new_resume)
        
        # In a real async system, we would trigger the Celery task here to calculate scores.
        # For now, we commit to the database.
        db.commit()
        
        return {
            "status": "received", 
            "candidate_id": new_candidate.id, 
            "message": "AI successfully saved the candidate profile and parsed resume."
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/manual-upload/{job_id}", summary="Member 3 Manual Upload Relay")
def intake_manual_upload(job_id: int, payload: AIHandshakePayload, db: Session = Depends(get_db)):
    """
    Identical perfectly to auto-fetch, but flags the candidate source_mode as manual_upload.
    """
    payload.source_mode = "manual_upload"
    return intake_auto_fetch(job_id, payload, db)
