from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Skill(BaseModel):
    name: str
    confidence: float
    proficiency: Optional[str] = None

class Project(BaseModel):
    title: str
    description: str
    technologies: List[str] = []
    duration: Optional[str] = None
    has_deployment: bool = False
    github_url: Optional[str] = None
    confidence: float

class Internship(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: str
    technologies: List[str] = []
    confidence: float

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    cgpa: Optional[float] = None
    batch: Optional[int] = None
    confidence: float

class Certification(BaseModel):
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    confidence: float

class ParseResponse(BaseModel):
    resume_id: str
    parse_status: str
    parse_confidence: float
    is_anonymized: bool = False
    
    # Personal Info (Hidden if is_anonymized=True)
    student_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    education: Optional[Education] = None
    skills: List[Skill] = []
    unknown_skills: List[str] = [] # Skills not found in taxonomy
    projects: List[Project] = []
    internships: List[Internship] = []
    certifications: List[Certification] = []
    achievements: List[str] = []
    
    # 384-dimensional embeddings as lists of floats
    skills_embedding: Optional[List[float]] = None
    projects_embedding: Optional[List[float]] = None
    experience_embedding: Optional[List[float]] = None
    overall_embedding: Optional[List[float]] = None
