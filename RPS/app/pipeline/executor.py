from typing import Dict, Any, List, Optional
from app.api.models.resume import ParseResponse, Skill, Project, Education, Internship, Certification
from app.extractor.pdf_parser import extract_text_from_pdf
from app.extractor.classifier import classify_sections
from app.pipeline.normalizer import SkillNormalizer
from app.pipeline.embedder import embedder

# Initialize standard skill normalizer
skill_normalizer = SkillNormalizer()

# NOTE: In a real system, the DL models (DistilBERT / SBERT) would be loaded once at startup.
# For now, we mock the extraction pipeline results until PyTorch dependencies finish downloading.

def process_resume(content: bytes, filename: str, anonymize: bool = False) -> ParseResponse:
    """
    Main orchestration function that runs the Resume through all layers:
    1. Extract PDF text
    2. Classify text into headers (Education, Skills, etc)
    3. Run DistilBERT NER (Mocked for now)
    4. Normalize skills via taxonomy and collect unknown entities
    5. Generate Sentence-BERT embeddings (with chunking)
    """
    
    # 1. Text Extraction Layer
    raw_text = extract_text_from_pdf(content)
    if not raw_text:
        return _build_failed_response(filename)
        
    # 2. Section Classification Layer
    sections = classify_sections(raw_text)
    
    # 3. Entity Extraction Layer (NER)
    # TODO: Load and invoke the fine-tuned DistilBERT models here for each chunk.
    # Currently mocking the extracted outputs to avoid startup latency during dev.
    
    # 4. Skill Normalization Layer & Skill Harvesting (Fix #3)
    # Assuming the mock NER extracted "React", "Python", "K8s", "LangChain"
    raw_skills = ["React.js", "python3", "K8s", "Docker", "LangChain"]
    normalized_skills = []
    unknown_skills = []
    
    for raw in raw_skills:
        canonical, is_known = skill_normalizer.normalize(raw)
        if is_known:
            normalized_skills.append(Skill(name=canonical, confidence=0.95))
        else:
            unknown_skills.append(canonical)
            
    # Fix #2: Blind Recruiting / Anonymization
    personal_info = {
         "student_name": "Candidate Example",
         "email": "example@college.edu",
         "phone": "+1234567890"
    }
    
    if anonymize:
         personal_info = {
              "student_name": "Candidate A",  # Or mapped ID
              "email": "[HIDDEN]",
              "phone": "[HIDDEN]"
         }
            
    # 5. Semantic Embedding Layer
    # Generate true 384-dimensional vectors via Sentence-BERT
    skills_text = sections.get("skills", "")
    projects_text = sections.get("projects", "")
    experience_text = sections.get("experience", "")
    overall_text = "\n".join(sections.values())
    
    skills_emb = embedder.embed_text(skills_text) if skills_text else None
    projects_emb = embedder.embed_text(projects_text) if projects_text else None
    experience_emb = embedder.embed_text(experience_text) if experience_text else None
    overall_emb = embedder.embed_text(overall_text) if overall_text else None
    
    # Assemble final response
    return ParseResponse(
        resume_id="RES-001",
        parse_status="PARSED",
        parse_confidence=0.92,
        is_anonymized=anonymize,
        **personal_info,
        
        skills=normalized_skills,
        unknown_skills=unknown_skills,
        
        projects=[
           Project(title="Mock Project", description="Parsed from PDF", confidence=0.88) 
        ],
        
        skills_embedding=skills_emb,
        projects_embedding=projects_emb,
        experience_embedding=experience_emb,
        overall_embedding=overall_emb
    )


def _build_failed_response(filename: str) -> ParseResponse:
     return ParseResponse(
            resume_id=filename,
            parse_status="FAILED",
            parse_confidence=0.0,
            skills=[],
            projects=[]
     )
