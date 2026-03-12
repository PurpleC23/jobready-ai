import requests
from bs4 import BeautifulSoup
from modules.ai_client import ask_mistral

def scrape_job(url: str) -> str:
    """Scrape job description text from a URL."""
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        
        # Remove junk tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        text = soup.get_text(separator="\n", strip=True)
        
        # Return first 3000 chars to keep prompt manageable
        return text[:3000]
    
    except Exception as e:
        return f"Error scraping job: {str(e)}"


def analyze_match(resume_text: str, job_text: str) -> str:
    """Score how well the resume matches the job description."""
    
    prompt = f"""
    You are a hiring expert. Compare this resume against the job description.
    
    Give your response in this exact format:
    
    MATCH SCORE: (X/100)
    
    STRONG MATCHES:
    - (skills/experience that align well)
    
    GAPS:
    - (what the job wants that the resume lacks)
    
    VERDICT:
    (2 sentence honest assessment of their chances)
    
    RESUME:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {job_text}
    """
    
    return ask_mistral(prompt)

def extract_job_details(job_text: str) -> dict:
    """Extract job title and company name from job description."""
    
    prompt = f"""
    Extract the following from this job posting and return exactly in this format:
    
    JOB TITLE: (exact job title)
    COMPANY: (exact company name)
    
    JOB POSTING:
    {job_text[:1000]}
    """
    
    result = ask_mistral(prompt)
    
    details = {"job_title": "Unknown", "company": "Unknown"}
    
    for line in result.split("\n"):
        if "JOB TITLE:" in line:
            details["job_title"] = line.replace("JOB TITLE:", "").strip()
        if "COMPANY:" in line:
            details["company"] = line.replace("COMPANY:", "").strip()
    
    return details