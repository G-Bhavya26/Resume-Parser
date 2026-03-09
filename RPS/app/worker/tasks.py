import logging
from .celery_app import celery_app
from app.database import SessionLocal
from app.models import schemas
from app.core.eligibility import check_eligibility
from app.core.scoring import calculate_score

logger = logging.getLogger(__name__)

@celery_app.task(name="process_resume_pipeline", bind=True, max_retries=3)
def process_resume_pipeline(self, candidate_id: int, job_id: int):
    """
    The orchestrator task.
    1. Checks candidate eligibility.
    2. If eligible, runs the 6-dimension scoring engine.
    3. Saves results back to database.
    """
    logger.info(f"Starting pipeline for Candidate {candidate_id} on Job {job_id}")
    
    db = SessionLocal()
    try:
        candidate = db.query(schemas.Candidate).filter(schemas.Candidate.id == candidate_id).first()
        job = db.query(schemas.Job).filter(schemas.Job.id == job_id).first()
        resume = db.query(schemas.ParsedResume).filter(
            schemas.ParsedResume.candidate_id == candidate_id,
            schemas.ParsedResume.job_id == job_id
        ).first()

        if not candidate or not job or not resume:
            logger.error(f"Missing DB records for Candidate {candidate_id}")
            return False

        # --- LAYER 1: STRICT ELIGIBILITY ---
        elig_result = check_eligibility(candidate, job)
        
        db_eligibility = schemas.EligibilityResult(
            candidate_id=candidate_id,
            job_id=job_id,
            passed=elig_result["passed"],
            failed_rules_json=elig_result["failed_rules_json"]
        )
        db.add(db_eligibility)

        # Skip scoring if they failed hard rules
        if not elig_result["passed"]:
            logger.info(f"Candidate {candidate_id} failed eligibility. Stopping pipeline.")
            db.commit()
            # In a real system, you might trigger an email notification here
            return False

        # --- LAYER 5: SCORING ENGINE ---
        score_result = calculate_score(resume.extracted_json, job)
        
        db_score = schemas.Score(
            candidate_id=candidate_id,
            job_id=job_id,
            total_score=score_result["total_score"],
            breakdown_json=score_result["breakdown_json"],
            is_overridden=score_result["is_overridden"]
        )
        db.add(db_score)

        db.commit()
        logger.info(f"Pipeline complete for Candidate {candidate_id}. Score: {score_result['total_score']}")
        return True

    except Exception as exc:
        db.rollback()
        logger.error(f"Pipeline failed for Candidate {candidate_id}: {str(exc)}")
        # If it's a temporary DB lock issue, retry
        raise self.retry(exc=exc, countdown=5)
    
    finally:
        db.close()
