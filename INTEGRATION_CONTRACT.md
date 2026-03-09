# 🤝 CRMS: Finalized Integration Contract
**Project**: Resume Parsing Module
**Status**: 🔒 LOCKED & ALIGNED (Matches 15-Page Blueprint)

---

## 1. The AI Handshake (Member 2 ➡️ You)
*Member 2 parses a resume and POSTs this JSON to your `/ai/callback` endpoint.*
*This EXACT structure is mandated by the blueprint for Member 2's Output JSON (Task 2: AI Pipeline Deliverable).*

```json
{
  "candidate_id": 12345,
  "parse_status": "SUCCESS", 
  "parse_confidence": 0.89,
  "name": "John Doe",
  "college": "IIT Delhi",
  "degree": "B.Tech",
  "cgpa": 8.5,
  "skills_raw": ["reactjs", "ML", "python"],
  "skills_normalized": ["React", "Machine Learning", "Python"],
  "projects": [
    {
      "title": "Stock Price Alert",
      "tech_stack": ["Python", "WebSockets"],
      "complexity": "High"
    }
  ],
  "internships": [
    {
      "company": "Google",
      "role": "SDE Intern",
      "duration_months": 3
    }
  ],
  "similarity_scores": {
    "projects": 0.82,
    "skills": 0.75,
    "experience": 0.60,
    "global": 0.78
  },
  "authenticity_score": 0.85,
  "source_mode": "manual_upload"
}
```

---

## 2. The Dashboard Handshake (You ➡️ Member 3)
*You provide this JSON for the Leaderboard and Candidate Profile.*
*This data maps directly to your `scores` and `eligibility_results` tables.*

### Candidate Score Object
```json
{
  "total_score": 85.5,
  "z_score": 1.25,
  "percentile": "Top 8%",
  "is_overridden": false,
  "breakdown_json": {
    "project_relevance": 21.5,  /* Max 25 */
    "skill_coverage": 18.0,     /* Max 20 */
    "authenticity_trust": 15.0, /* Max 15 */
    "internship_relevance": 12.0, /* Max 15 */
    "education_quality": 14.0,  /* Max 15 */
    "semantic_alignment": 5.0   /* Max 10 */
  },
  "eligibility": {
    "passed": true,
    "failed_rules": []
  }
}
```

---

## 🌐 Endpoint Specification
| Endpoint | Method | Blueprint Requirement |
| :--- | :--- | :--- |
| `/intake/auto-fetch/{job_id}` | POST | Trigger Mode 1 batch processing |
| `/intake/manual-upload/{job_id}`| POST | Accept Mode 2 multipart file upload |
| `/jobs/{job_id}/status` | GET | Processing % progress tracker |
| `/candidates/{job_id}/ranked` | GET | Ranked leaderboard list with scores |
| `/candidates/{id}/breakdown` | GET | Full score breakdown for Dashboard Profile |
| `/candidates/{id}/override` | POST | HR manual score adjustment (Immutable Log) |
| `/feedback/{id}/outcome` | POST | Log final selection (Selected/Interview/Rejected) |

**Authentication**: All requests require `Authorization: Bearer <JWT_TOKEN>`.

---
*Sign-off: This contract is now the definitive guide for Member 1, 2, and 3.*
