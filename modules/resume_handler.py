import pypdf
import docx
from modules.ai_client import ask_mistral

def extract_resume_text(uploaded_file) -> str:
    """Extract raw text from uploaded PDF or DOCX."""
    
    if uploaded_file.name.endswith(".pdf"):
        reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    else:
        return ""


def parse_resume_with_ai(resume_text: str) -> dict:
    """Use Mistral to extract structured info from resume text."""
    
    prompt = f"""
    Extract the following from this resume and return as plain text with clear labels:
    
    SKILLS: (list the technical and soft skills)
    EXPERIENCE: (list job titles and companies)
    EDUCATION: (list degrees and institutions)
    SUMMARY: (write a 2 sentence professional summary)
    
    RESUME:
    {resume_text}
    """
    
    result = ask_mistral(prompt)
    return {"raw": resume_text, "parsed": result}