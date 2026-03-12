from modules.ai_client import ask_mistral

def generate_interview_questions(resume_text: str, job_text: str) -> str:
    """Predict likely interview questions and suggest answers."""
    
    prompt = f"""
    You are an expert interview coach. Based on this job description and candidate resume,
    predict the 20 most likely interview questions they will be asked.
    
    For each question provide:
    - The question
    - Why interviewers ask it for this role
    - A strong answer framework using the candidate's actual experience
    
    Format exactly like this:
    
    Q1: (question)
    WHY THEY ASK: (reason)
    HOW TO ANSWER: (tailored advice using their background)
    
    Q2: (question)
    WHY THEY ASK: (reason)
    HOW TO ANSWER: (tailored advice using their background)
    
    ...and so on.
    
    Include a mix of:
    - Technical/skills questions
    - Behavioral questions
    - Role-specific scenario questions
    - Market and Trends based questions
    
    RESUME:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {job_text}
    """
    
    return ask_mistral(prompt)