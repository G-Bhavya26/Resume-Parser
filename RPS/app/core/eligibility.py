from typing import Dict, Any

def check_eligibility(candidate, job) -> Dict[str, Any]:
    """
    Layer 1 Eligibility Filter (Deterministic)
    Evaluates hard rules: CGPA, Degree, Batch.
    Note: Backlogs and Branch are skipped as they are not defined in the strictly validated 7-table schema.
    
    Args:
        candidate: Candidate SQLAlchemy model or dot-accessible object.
        job: Job SQLAlchemy model or dot-accessible object.
        
    Returns:
        A dictionary matching the 'eligibility_results' schema requirements:
        {
            "passed": bool,
            "failed_rules_json": list of dicts with reasons
        }
    """
    passed = True
    failed_rules = []

    # 1. CGPA Threshold Check
    if getattr(job, "min_cgpa", None) is not None:
        cand_cgpa = getattr(candidate, "cgpa", None)
        if cand_cgpa is None or float(cand_cgpa) < float(job.min_cgpa):
            passed = False
            failed_rules.append({
                "rule_name": "CGPA Threshold",
                "candidate_value": cand_cgpa,
                "required_value": job.min_cgpa,
                "reason_string": f"CGPA {cand_cgpa} below required {job.min_cgpa}"
            })

    # 2. Degree Type Check
    allowed_degrees = getattr(job, "allowed_degrees", None)
    if allowed_degrees:
        cand_degree = getattr(candidate, "degree", None)
        # Handle case insensitivity optionally, but here we do strict string match per blueprint
        if not cand_degree or cand_degree not in allowed_degrees:
            passed = False
            failed_rules.append({
                "rule_name": "Degree Type",
                "candidate_value": cand_degree,
                "required_value": allowed_degrees,
                "reason_string": f"Degree {cand_degree} not in allowed list for this job"
            })

    # 3. Graduation Batch Check
    req_batch = getattr(job, "batch_year", None)
    if req_batch is not None:
        cand_batch = getattr(candidate, "batch", None)
        if not cand_batch or int(cand_batch) != int(req_batch):
            passed = False
            failed_rules.append({
                "rule_name": "Graduation Batch",
                "candidate_value": cand_batch,
                "required_value": req_batch,
                "reason_string": f"Batch year {cand_batch} does not match required {req_batch}"
            })

    return {
        "passed": passed,
        "failed_rules_json": failed_rules
    }
