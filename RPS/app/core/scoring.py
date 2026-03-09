import math
from typing import Dict, Any, List

def calculate_score(parsed_data: Dict[str, Any], job: Any = None) -> Dict[str, Any]:
    """
    Layer 5: Evidence-Based Scoring
    Computes a final score out of 100 based on the 6-dimension weighted formula.
    Also calculates the discrete dimension values for the Dashboard JSON.
    """
    
    # 1. Immediate Disqualification Check (Hidden Text)
    # If the AI flagged hidden text, the candidate is immediately disqualified.
    if parsed_data.get("has_hidden_text", False):
        return __zero_score_response()

    # Base raw scores (0.0 to 1.0)
    sim_scores = parsed_data.get("similarity_scores", {})
    
    raw_proj = sim_scores.get("projects", 0.0)
    raw_skill = sim_scores.get("skills", 0.0)
    raw_exp = sim_scores.get("experience", 0.0)
    raw_global = sim_scores.get("global", 0.0)
    
    # Education heuristic (CGPA normalized to 10.0 scale)
    cgpa = parsed_data.get("cgpa", 0.0)
    raw_edu = min(cgpa / 10.0, 1.0) if cgpa else 0.0

    # Base Authenticity / Trust score
    raw_trust = parsed_data.get("authenticity_score", 1.0)
    
    # Apply Anti-Gaming Deductions to Trust Score
    if parsed_data.get("has_date_overlap", False):
        raw_trust -= 0.20
    
    unverified_skills = parsed_data.get("unverified_skills_count", 0)
    if unverified_skills > 0:
        raw_trust -= (0.10 * unverified_skills)
        
    if parsed_data.get("has_buzzword_stuffing", False):
        raw_trust -= 0.15
        
    if parsed_data.get("has_keyword_stuffing", False):
        raw_trust -= 0.10

    # Floor the trust score at 0.0 so it doesn't go negative
    raw_trust = max(raw_trust, 0.0)

    # 2. Apply Blueprint Weights (Out of 100 max)
    # Project: 25%, Skill: 20%, Trust: 15%, Intern: 15%, Edu: 15%, Semantic: 10%
    dim_proj = raw_proj * 25.0
    dim_skill = raw_skill * 20.0
    dim_trust = raw_trust * 15.0
    dim_exp = raw_exp * 15.0
    dim_edu = raw_edu * 15.0
    dim_global = raw_global * 10.0

    total_score = dim_proj + dim_skill + dim_trust + dim_exp + dim_edu + dim_global

    # Construct the JSON exactly as requested in the Integration Contract
    breakdown_json = {
        "project_relevance": round(dim_proj, 2),
        "skill_coverage": round(dim_skill, 2),
        "authenticity_trust": round(dim_trust, 2),
        "internship_relevance": round(dim_exp, 2),
        "education_quality": round(dim_edu, 2),
        "semantic_alignment": round(dim_global, 2)
    }

    return {
        "total_score": round(total_score, 2),
        "breakdown_json": breakdown_json,
        "is_overridden": False
    }

def __zero_score_response():
    """Helper to return a definitive zero score for cheating candidates."""
    return {
        "total_score": 0.0,
        "breakdown_json": {
            "project_relevance": 0.0,
            "skill_coverage": 0.0,
            "authenticity_trust": 0.0,
            "internship_relevance": 0.0,
            "education_quality": 0.0,
            "semantic_alignment": 0.0
        },
        "is_overridden": False
    }

def calculate_batch_rankings(batch_scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes Z-Score and Percentile dynamically across a batch of candidates.
    Modifies the dictionaries in place and returns them.
    """
    if not batch_scores:
        return batch_scores

    scores = [s.get("total_score", 0.0) for s in batch_scores]
    n = len(scores)
    
    mean = sum(scores) / n
    variance = sum((x - mean) ** 2 for x in scores) / n
    std_dev = math.sqrt(variance)
    
    for c_score in batch_scores:
        val = c_score.get("total_score", 0.0)
        
        # Z-Score
        z = (val - mean) / std_dev if std_dev > 0 else 0.0
        c_score["z_score"] = round(z, 2)
        
        # Percentile Rank
        count_less_or_equal = sum(1 for x in scores if x <= val)
        percentile_val = (count_less_or_equal / n) * 100
        top_percent = max(1, 100 - int(percentile_val) + 1)
        c_score["percentile"] = f"Top {top_percent}%"
        
    return batch_scores
