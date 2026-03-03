from fastapi import APIRouter, File, UploadFile, HTTPException
from app.api.models.resume import ParseResponse
from app.pipeline.executor import process_resume

router = APIRouter()

@router.post("/parse", response_model=ParseResponse)
async def parse_resume(anonymize: bool = False, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Read the file contents into memory
    content = await file.read()
    
    try:
        # Pass the PDF bytes to the processing pipeline
        result = process_resume(content, file.filename, anonymize=anonymize)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
