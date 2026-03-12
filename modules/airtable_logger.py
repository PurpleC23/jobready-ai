import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = "Job Tracker"

def log_job_to_airtable(
    job_title: str,
    company: str,
    job_url: str,
    match_score: str,
    cover_letter: str = "",
    notes: str = ""
):
    """Log a job application to Airtable."""
    
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "fields": {
            "Job Title": job_title,
            "Company": company,
            "Job URL": job_url,
            "Match Score": int(match_score) if match_score.isdigit() else 0,
            "Date Applied": datetime.now().strftime("%Y-%m-%d"),
            "Status": "Saved",
            "Cover Letter": cover_letter,
            "Notes": notes,
            "Response": "Awaiting"
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Airtable response: {response.status_code}")
    print(f"Airtable error: {response.text}")
    return response.status_code == 200