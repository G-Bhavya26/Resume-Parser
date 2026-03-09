from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import schemas
from app.core.eligibility import check_eligibility
from app.core.scoring import calculate_score, calculate_batch_rankings

router = APIRouter(prefix="/candidates", tags=["Candidates & Validation"])

@router.get("/{job_id}/ranked")
def get_ranked_candidates(job_id: int, db: Session = Depends(get_db)):
    """
    Returns the leaderboard for Member 3's UI Dashboard.
    Sorts candidates dynamically based on Z-Score / Total Score.
    """
    # Verify job exists
    job = db.query(schemas.Job).filter(schemas.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = db.query(schemas.Candidate, schemas.ParsedResume, schemas.Score).join(
        schemas.ParsedResume, schemas.Candidate.id == schemas.ParsedResume.candidate_id
    ).join(
        schemas.Score, schemas.Candidate.id == schemas.Score.candidate_id
    ).filter(
        schemas.ParsedResume.job_id == job_id
    ).all()
    
    leaderboard = []
    
    # Normally, Celery processes this. For the API response, we format what's in the DB.
    for cand, resume, score in candidates:
        leaderboard.append({
            "candidate_id": cand.id,
            "name": cand.name,
            "email": cand.email,
            "total_score": score.total_score,
            "z_score": score.z_score,
            "percentile": score.percentile,
            "status": "Processed"
        })
        
    # Sort descending by total score
    leaderboard.sort(key=lambda x: x["total_score"], reverse=True)
    return leaderboard

@router.get("/{id}/breakdown")
def get_candidate_breakdown(id: int, db: Session = Depends(get_db)):
    """
    Returns the 6-dimension breakdown for a specific candidate.
    """
    score = db.query(schemas.Score).filter(schemas.Score.candidate_id == id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found for candidate")
        
    return {
        "candidate_id": id,
        "total_score": score.total_score,
        "breakdown": score.breakdown_json,
        "is_overridden": score.is_overridden
    }

@router.post("/{id}/override")
def override_candidate_score(id: int, new_score: float, reason: str, hr_user_id: int, db: Session = Depends(get_db)):
    """
    Member 3 UI calls this when HR manually overrides a score.
    Saves an immutable log in override_log.
    """
    score = db.query(schemas.Score).filter(schemas.Score.candidate_id == id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")

    old_score = score.total_score
    score.total_score = new_score
    score.is_overridden = True
    
    # Create the immutable audit trail
    log = schemas.OverrideLog(
        candidate_id=id,
        job_id=score.job_id,
        hr_user_id=hr_user_id,
        original_score=old_score,
        new_score=new_score,
        reason=reason
    )
    
    db.add(log)
    db.commit()
    
    return {"message": "Score overridden successfully and permanently logged."}

@router.post("/feedback/{id}/outcome")
def log_final_outcome(id: int, outcome: str, job_id: int, db: Session = Depends(get_db)):
    """
    Logs if the candidate was 'Selected', 'Rejected', or 'Interview'
    """
    # Enforce basic Enum checks
    if outcome not in ["Selected", "Rejected", "Interview"]:
        raise HTTPException(status_code=400, detail="Outcome must be Selected, Rejected, or Interview")
        
    feedback = schemas.FeedbackOutcome(
        candidate_id=id,
        job_id=job_id,
        final_outcome=outcome
    )
    db.add(feedback)
    db.commit()
    
    return {"message": f"Candidate {id} permanently marked as {outcome}."}
