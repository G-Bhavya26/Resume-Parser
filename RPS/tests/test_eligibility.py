from app.core.eligibility import check_eligibility

class MockJob:
    def __init__(self, min_cgpa=None, allowed_degrees=None, batch_year=None):
        self.min_cgpa = min_cgpa
        self.allowed_degrees = allowed_degrees
        self.batch_year = batch_year

class MockCandidate:
    def __init__(self, cgpa=None, degree=None, batch=None):
        self.cgpa = cgpa
        self.degree = degree
        self.batch = batch

def test_eligibility_all_pass():
    job = MockJob(min_cgpa=8.0, allowed_degrees=["B.Tech"], batch_year=2024)
    candidate = MockCandidate(cgpa=8.5, degree="B.Tech", batch=2024)
    result = check_eligibility(candidate, job)
    
    assert result["passed"] is True
    assert len(result["failed_rules_json"]) == 0

def test_eligibility_fails_cgpa():
    job = MockJob(min_cgpa=8.0)
    candidate = MockCandidate(cgpa=7.5)
    result = check_eligibility(candidate, job)
    
    assert result["passed"] is False
    assert result["failed_rules_json"][0]["rule_name"] == "CGPA Threshold"

def test_eligibility_fails_multiple():
    job = MockJob(min_cgpa=8.0, allowed_degrees=["B.Tech"], batch_year=2024)
    candidate = MockCandidate(cgpa=7.5, degree="B.Sc", batch=2023)
    result = check_eligibility(candidate, job)
    
    assert result["passed"] is False
    assert len(result["failed_rules_json"]) == 3
