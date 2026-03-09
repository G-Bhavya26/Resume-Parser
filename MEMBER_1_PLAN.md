# 📋 CRMS: Member 1 Implementation Roadmap (Systems & Logic)
**Project**: Campus Recruitment Intelligence System (Resume Parsing Module)
**Role**: Member 1 — Systems & Logic Engineer
**Status**: 🟢 INITIALIZED
**Last Updated**: March 2026

---

## 🎯 Primary Objectives
1. **Foundation**: Build the PostgreSQL database and SQLAlchemy models.
2. **Layer 1 (The Gatekeeper)**: Implement hard-rule eligibility filtering.
3. **Layer 5 (The Judge)**: Implement the 6-dimension weighted scoring engine.
4. **Infrastructure**: Set up FastAPI endpoints and Celery/Redis for async processing.

---

## 🛠️ Phase 1: The Integration Contract (WEEK 1)
*Crucial for parallel development. Member 2 and 3 depend on this.*

- [ ] **Finalize JSON Contract**: Agree on the data structure for AI-extracted entities.
- [ ] **API Endpoint Spec**: Define the POST/GET paths for the dashboard to fetch data.
- [ ] **Data Types**: Freeze field types (e.g., CGPA as Float, Skills as List[String]).

---

## 🗄️ Task 1: Database Architecture (WEEK 2)
- [ ] Initialize **SQLAlchemy** models for the finalized schema:
    - **`candidates`**: `id`, `name`, `email`, `cgpa`, `degree`, `batch`, `resume_url`, `source_mode`
    - **`jobs`**: `id`, `title`, `min_cgpa`, `allowed_degrees`, `batch_year`, `required_skills_json`
    - **`eligibility_results`**: `candidate_id`, `job_id`, `passed`, `failed_rules_json`
    - **`parsed_resumes`**: `candidate_id`, `extracted_json`, `confidence`, `parse_status`, `source_mode`
    - **`scores`**: `candidate_id`, `job_id`, `total_score`, `breakdown_json`, `z_score`, `percentile`, `is_overridden`
    - **`override_log`**: `candidate_id`, `job_id`, `hr_user_id`, `original_score`, `new_score`, `reason` (**IMMUTABLE**)
    - **`feedback_outcomes`**: `candidate_id`, `job_id`, `outcome`, `marked_by`, `marked_at`
- [ ] Set up **Alembic** migrations.

---

## ⚖️ Task 2: Layer 1 — Eligibility Filter (WEEK 2)
*Hard logic only. No AI.*

- [ ] Implement `check_eligibility()` logic.
- [ ] **Rules**:
    - [ ] `CGPA >= Job.min_cgpa`
    - [ ] `Degree in Job.allowed_degrees`
    - [ ] `Batch == Job.required_batch`
    - [ ] `Backlogs <= Job.max_backlogs`
- [ ] **Auditability**: Ensure every rejection stores a specific reason string.

---

## 评 Task 3: Layer 5 — Scoring Engine (WEEK 3)
- [ ] **Weighted Formula**: 
  - Projects (25%), Skills (20%), Trust (15%), Internship (15%), Education (15%), Semantic (10%).
- [ ] **Normalization**: Build the Z-score calculation across candidate batches.
- [ ] **Authenticity**: 
    - [ ] Hidden text detection -> Auto-disqualification.
    - [ ] Date overlap -> Point deduction.
    - [ ] Buzzword stuffing -> Point deduction.

---

## 🚀 Task 4 & 5: FastAPI & Celery Infrastructure (WEEKS 4-5)
- [ ] **REST Endpoints**:
    - `POST /intake/auto-fetch`: Trigger system matching.
    - `POST /intake/manual-upload`: HR drag-and-drop handler.
    - `GET /ranked-leaderboard`: Sorted results list.
- [ ] **Task Queue**: Set up Redis broker and Celery workers for 300-400 res/hr throughput.
- [ ] **Status Tracker**: Endpoint to show % progress during batch processing.

---

## 🤝 Integration Points
- **With Member 2 (AI)**: You receive their `ParsedResult` JSON and store it in your DB.
- **With Member 3 (UI)**: You provide the API endpoints that power the dashboard.

---
*Confidential – Team Use Only*
