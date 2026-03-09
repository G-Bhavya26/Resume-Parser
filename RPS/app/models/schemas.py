from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    cgpa = Column(Float)
    degree = Column(String)
    batch = Column(Integer)
    resume_url = Column(String)
    source_mode = Column(String)  # 'auto_fetched' or 'manual_upload'

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    min_cgpa = Column(Float, default=0.0)
    allowed_degrees = Column(JSON)  # e.g. ["B.Tech", "M.Tech"]
    batch_year = Column(Integer)
    required_skills_json = Column(JSON)

class EligibilityResult(Base):
    __tablename__ = "eligibility_results"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    passed = Column(Boolean)
    failed_rules_json = Column(JSON) # e.g. ["CGPA 6.5 < 7.0"]

class ParsedResume(Base):
    __tablename__ = "parsed_resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    extracted_json = Column(JSON)
    confidence = Column(Float)
    parse_status = Column(String) # 'SUCCESS', 'PARTIAL', 'FAILED'
    source_mode = Column(String)

class Score(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    total_score = Column(Float)
    breakdown_json = Column(JSON) # The 6-dimension scores
    z_score = Column(Float)
    percentile = Column(String)
    is_overridden = Column(Boolean, default=False)

class OverrideLog(Base):
    __tablename__ = "override_log"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    hr_user_id = Column(String)
    original_score = Column(Float)
    new_score = Column(Float)
    reason = Column(Text, nullable=False) # Immutable recording

class FeedbackOutcome(Base):
    __tablename__ = "feedback_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    outcome = Column(String) # 'Selected', 'Interview', 'Rejected'
    marked_by = Column(String)
    marked_at = Column(DateTime(timezone=True), server_default=func.now())
