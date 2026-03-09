from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import intake, candidates

app = FastAPI(
    title="CRMS Resume Parsing Pipeline API",
    description="Backend API for Member 1 of the CRMS system to handle and score parsed resumes.",
    version="1.0.0"
)

# Crucial for Member 3 (UI Designer) doing local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routers
app.include_router(intake.router)
app.include_router(candidates.router)

@app.get("/", tags=["Health"])
def health_check():
    """
    Simple health check endpoint so the UI knows the Pipeline is active.
    """
    return {"status": "ok", "service": "CRMS Resume Parsing Pipeline v1.0.0"}
