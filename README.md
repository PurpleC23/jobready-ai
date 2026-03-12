# 🎯 JobReady — Local AI Job Hunting Assistant

A fully local, zero-cost AI-powered job hunting assistant built with Python, Streamlit, and Mistral. Goes from "I need a job" to "I'm ready to apply" in minutes — no API costs, no data sent to the cloud.

---

## What It Does

JobReady is a 5-feature app that guides you through the entire job application process:

1. **Resume Parser** — Upload your resume once (PDF or DOCX). Mistral reads it and extracts your skills, experience, and education into a clean structured format. Every other feature uses this automatically.

2. **Job Search** — Based on your parsed resume, Mistral suggests the best job titles for your profile and generates direct search links to 10+ job boards including LinkedIn, Indeed, RemoteOK, Wellfound, WeWorkRemotely, Naukri and more.

3. **Job Analyzer** — Paste any job posting URL. JobReady scrapes the page using BeautifulSoup, strips out noise, and sends the job description + your resume to Mistral. You get a match score out of 100, your strong matches, your gaps, and an honest verdict.

4. **Cover Letter Generator** — Using your resume and the scraped job description, Mistral writes a tailored 3-paragraph cover letter specific to that company and role. No generic templates. Downloadable as PDF.

5. **Interview Prep** — Mistral predicts 20 likely interview questions based on the job description and your background. Each question comes with why interviewers ask it and a tailored answer framework using your actual projects and experience.

Every analyzed job is automatically logged to Airtable as a job application tracker — with match score, job URL, company, and cover letter saved for reference.

---

## How It Works — The Flow
```
Your Resume (PDF/DOCX)
        ↓
  Mistral extracts skills, experience, education
        ↓
    ┌───────────────────────────────┐
    │                               │
    ▼                               ▼
Job Search                    Job Analyzer
(suggests roles               (paste any URL →
+ board links)                BeautifulSoup scrapes it)
                                    ↓
                             Match Score (X/100)
                             Strong Matches
                             Gaps identified
                                    ↓
                    ┌───────────────────────────┐
                    │                           │
                    ▼                           ▼
          Cover Letter Generator        Interview Prep
          (tailored 3 paragraphs)      (20 predicted Q&A)
                    ↓
             Download as PDF
                    ↓
          Auto-logged to Airtable
          (Job Title, Company, Score,
           Cover Letter, Status)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Ollama + Mistral 7B | Local AI brain |
| LangChain | AI orchestration |
| BeautifulSoup + lxml | Job page scraping |
| fpdf2 | PDF export |
| Airtable API | Job application tracking |
| python-docx + pypdf | Resume file parsing |

---

## Why Local?

- ✅ Zero ongoing costs — no OpenAI API bills
- ✅ Complete data privacy — your resume never leaves your machine
- ✅ Works offline — only Airtable logging needs internet
- ✅ No rate limits

---

## Setup & Installation

**Requirements:**
- Python 3.10+
- Ollama installed with Mistral pulled

**Steps:**
```bash
# Clone the repo
git clone https://github.com/yourusername/jobready.git
cd jobready

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install streamlit langchain langchain-community langchain-core langchain-ollama beautifulsoup4 requests pypdf python-docx lxml fpdf2 python-dotenv airtable-python-wrapper

# Pull Mistral if you haven't
ollama pull mistral

# Run the app
streamlit run app.py
```

---

## Project Structure
```
jobready/
│
├── app.py                  # Main Streamlit UI
├── README.md
│
└── modules/
    ├── ai_client.py        # Connects to local Mistral via Ollama
    ├── resume_handler.py   # Extracts + parses resume with AI
    ├── job_search.py       # Job suggestions + board links
    ├── job_analyzer.py     # Scrapes job URLs + scores match
    ├── cover_letter.py     # Generates tailored cover letters
    ├── interview_prep.py   # Predicts interview questions
    └── airtable_logger.py  # Logs applications to Airtable
```

---

## Built By

Chahal Tilak — Self-taught AI developer building practical AI tools.

[GitHub](https://github.com/PurpleC23) • [LinkedIn](https://linkedin.com/in/chahal-tilak-a248a9271)