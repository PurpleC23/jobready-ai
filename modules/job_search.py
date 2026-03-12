import requests
from bs4 import BeautifulSoup
from modules.ai_client import ask_mistral

def search_jobs(skills_text: str) -> list:
    """Generate job search suggestions based on resume skills."""
    
    prompt = f"""
    Based on these skills and experience, suggest 8 specific job titles this person should apply for.
    Also suggest the best job boards to find them.
    
    Format your response as a numbered list like this:
    1. Job Title - Why it fits - Where to search
    2. Job Title - Why it fits - Where to search
    
    SKILLS AND EXPERIENCE:
    {skills_text}
    """
    
    result = ask_mistral(prompt)
    return result


def scrape_job_listings(job_title: str) -> str:
    """Generate a direct search URL for common job boards."""
    
    job_encoded = job_title.replace(" ", "+")
    
    boards = {
        # General
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={job_encoded}&f_WT=2",
        "Indeed": f"https://www.indeed.com/jobs?q={job_encoded}&l=remote",
        
        # Remote Specific
        "RemoteOK": f"https://remoteok.com/remote-{job_encoded}-jobs",
        "Wellfound": f"https://wellfound.com/jobs?q={job_encoded}",
        "WeWorkRemotely": f"https://weworkremotely.com/remote-jobs/search?term={job_encoded}",
        "Remote.co": f"https://remote.co/remote-jobs/search/?search_keywords={job_encoded}",
        
        # Tech Focused
        "Glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={job_encoded}&remoteWorkType=1",
        "Himalayas": f"https://himalayas.app/jobs?q={job_encoded}",
        
        # India + Global
        "Naukri": f"https://www.naukri.com/{job_encoded}-jobs",
        "Internshala": f"https://internshala.com/jobs/{job_encoded}",
    }
        
    return boards