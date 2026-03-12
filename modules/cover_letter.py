from modules.ai_client import ask_mistral

def generate_cover_letter(resume_text: str, job_text: str, extra_info: str = "") -> str:
    """Generate a tailored cover letter for a specific job."""
    
    prompt = f"""
    Write a professional cover letter. 

    STRICT RULES — violations are not acceptable:
    - The very first word of the letter body MUST be the company name or role title. NOT "I". NOT "Dear". 
    - FORBIDDEN phrases (do not use any of these): "I am writing", "I am thrilled", "I am excited", "I am pleased", "I hope to", "I am confident", "please find", "to whom it may concern", "I am applying"
    - 3 paragraphs only, under 300 words
    - Paragraph 1: Start with the company or role name, say something specific about why this company/role stands out
    - Paragraph 2: Name drop 2 specific projects with real results, connect them to the job requirements
    - Paragraph 3: One sentence confident closing, no begging
    - Sound like a senior professional who is selective about where they apply
    - End with exactly this:
        Regards,
        [Full Name]
        
    - ALWAYS write exactly 3 full paragraphs. Never write less. Each paragraph must be minimum 3 sentences.
    - NEVER truncate or shorten the letter regardless of input length
    
    APPLICANT RESUME:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {job_text}
    
    EXTRA INFO FROM APPLICANT:
    {extra_info if extra_info else "None provided"}
    
    Remember: First word MUST be the company name or job title. Not "I".
    """
    
    return ask_mistral(prompt)