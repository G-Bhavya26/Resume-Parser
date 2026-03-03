# 🎓 CRMS - Intern Project Roadmap & Task Tracker

This document tracks the progress of the **Resume Parsing & Intelligence System (CRMS)** project. It is divided into three professional phases, progressing from base data extraction to intelligent candidate matching.

---

## 🏗️ Phase 1: The Foundation (Data Acquisition & Extraction)
**Goal:** Successfully convert raw PDF documents into structured, machine-readable text segments.

| Task ID | Task Name | Description | Status |
| :--- | :--- | :--- | :--- |
| **1.1** | **PDF Parsing Integration** | Use `PyMuPDF` & `pdfplumber` to extract all text from complex PDF layouts. | ✅ Done |
| **1.2** | **Section Classifier** | Regex-based logic to split text into "Education", "Skills", "Experience", etc. | 🟠 In-Progress |
| **1.3** | **Eligibility Engine** | Deterministic logic to filter candidates by CGPA, Branch, and Batch. | ⚪ Pending |
| **1.4** | **Async Pipeline** | Background processing using `Celery` + `Redis` for high-volume uploads. | ✅ Done |
| **1.5** | **Initial UI Dashboard** | Premium Glassmorphic UI with Century Gothic font for resume uploads. | ✅ Done |

---

## 🧠 Phase 2: The Logic (Standardization & Specialized AI)
**Goal:** Extract specific entities (Skills, Projects) and normalize them using a master taxonomy.

| Task ID | Task Name | Description | Status |
| :--- | :--- | :--- | :--- |
| **2.1** | **NER Data Annotation** | Label 500+ resumes with custom tags (SKILL, PROJECT, ORG) in Label Studio. | ⚪ Pending |
| **2.2** | **DistilBERT Fine-tuning** | Train a lightweight NLP model to detect entities with high confidence. | ⚪ Pending |
| **2.3** | **Skill Taxonomy Map** | Create a hierarchical JSON/DB structure of all technical skills & synonyms. | ✅ Done |
| **2.4** | **Skill Normalizer** | Map extracted terms (e.g., "JS") to their canonical names ("JavaScript"). | ✅ Done |

---

## 🚀 Phase 3: The Intelligence (Semantic Matching & Insights)
**Goal:** Use vector math to compare candidates against Job Descriptions and explain scores to HR.

| Task ID | Task Name | Description | Status |
| :--- | :--- | :--- | :--- |
| **3.1** | **Semantic Embeddings** | Generate 384-dimensional vectors using `Sentence-BERT` for comparison. | 🟠 In-Progress |
| **3.2** | **Weighted Scorer** | A 6-dimension algorithm to score candidates based on relevance and impact. | ⚪ Pending |
| **3.3** | **Explainability Layer** | Logic that generates "Why this score?" reasons for HR Review. | ⚪ Pending |
| **3.4** | **Full HR Dashboard** | Finalize ranking leaderboard, filters, and manual override controls. | ⚪ Pending |

---

## 📊 Project Health Summary
- **Overall Progress:** ~35% Complete
- **Current Focus:** Phase 1 (Section Classification) & Phase 3 (Embedding Optimization)
- **Tech Stack:** FastAPI, React, Redis, Celery, Sentence-BERT, PyMuPDF.

---
*Created by Antigravity (AI Co-pilot) for the CRMS Intern Team.*
