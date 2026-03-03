import re
import io
import fitz # PyMuPDF
import pdfplumber

def extract_text_from_pdf(content: bytes) -> str:
    """Extracts text from a PDF document."""
    try:
        # Wrap bytes in BytesIO since pdfplumber requires a file-like object
        pdf_stream = io.BytesIO(content)
        
        # First attempt with pdfplumber for better layout retention
        with pdfplumber.open(pdf_stream) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            if len(text.strip()) > 50:
                return text
                
        # Fallback to PyMuPDF if pdfplumber fails to extract meaningful text
        doc = fitz.open(stream=content, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
