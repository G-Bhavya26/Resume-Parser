from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import parse

app = FastAPI(
    title="Resume Parsing Service (RPS)",
    description="Microservice for extracting structured data and semantic embeddings from Resume PDFs.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parse.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "RPS"}
