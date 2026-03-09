from app.core.scoring import calculate_score

def test_perfect_candidate_score():
    ai_output = {
        "similarity_scores": {
            "projects": 1.0,
            "skills": 1.0,
            "experience": 1.0,
            "global": 1.0
        },
        "authenticity_score": 1.0,
        "cgpa": 10.0,
        "has_hidden_text": False
    }
    
    result = calculate_score(ai_output)
    
    # 25 + 20 + 15 + 15 + 15 + 10 = 100
    assert result["total_score"] == 100.0
    assert result["is_overridden"] is False
    
    breakdown = result["breakdown_json"]
    assert breakdown["project_relevance"] == 25.0
    assert breakdown["skill_coverage"] == 20.0
    assert breakdown["authenticity_trust"] == 15.0
    assert breakdown["internship_relevance"] == 15.0
    assert breakdown["education_quality"] == 15.0
    assert breakdown["semantic_alignment"] == 10.0

def test_cheating_candidate_hidden_text():
    ai_output = {
        "similarity_scores": {
            "projects": 1.0, # Looks perfect on paper!
            "skills": 1.0,
        },
        "has_hidden_text": True # But trying to game the system
    }
    
    result = calculate_score(ai_output)
    
    # Needs to be a definitive 0 across the board
    assert result["total_score"] == 0.0
    assert result["breakdown_json"]["project_relevance"] == 0.0

def test_candidate_trust_penalties():
    ai_output = {
        "similarity_scores": {
            "projects": 0.5,
            "skills": 0.5,
            "experience": 0.5,
            "global": 0.5
        },
        "authenticity_score": 1.0, # Base 1.0
        "cgpa": 5.0,
        "has_date_overlap": True, # -0.20 deduction
        "unverified_skills_count": 2 # -0.20 deduction
    }

    result = calculate_score(ai_output)
    breakdown = result["breakdown_json"]
    
    # 1.0 - 0.20 - 0.20 = 0.60 Trust Score
    # Final dimension weight: 0.60 * 15.0 max points = 9.0
    assert breakdown["authenticity_trust"] == 9.0

def test_batch_rankings():
    from app.core.scoring import calculate_batch_rankings
    
    batch = [
        {"total_score": 50.0},
        {"total_score": 75.0},
        {"total_score": 100.0}
    ]
    
    # Mean = 75.0
    # Variance = ((50 - 75)^2 + (75 - 75)^2 + (100 - 75)^2) / 3 = (625 + 0 + 625) / 3 = 416.66
    # Std Dev = ~20.41
    
    results = calculate_batch_rankings(batch)
    
    assert results[0]["z_score"] < 0
    assert results[1]["z_score"] == 0.0
    assert results[2]["z_score"] > 0
    
    assert "Top" in results[0]["percentile"]
    assert "Top" in results[2]["percentile"]
