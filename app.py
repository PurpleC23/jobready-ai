import streamlit as st
from modules.resume_handler import extract_resume_text, parse_resume_with_ai
from modules.job_search import search_jobs, scrape_job_listings
from modules.job_analyzer import scrape_job, analyze_match
from modules.cover_letter import generate_cover_letter
from modules.interview_prep import generate_interview_questions
from modules.airtable_logger import log_job_to_airtable
from modules.job_analyzer import scrape_job, analyze_match, extract_job_details
# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Ready",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Session State (memory between tabs) ───────────────────────────────────────
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = ""
if "job_text" not in st.session_state:
    st.session_state.job_text = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "Your Name"

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Job Ready 🎯")
    st.caption("A personal job hunting assistant")
    st.divider()
    
    if st.session_state.resume_text:
        st.success("✅ Resume loaded")
    else:
        st.warning("⚠️ No resume uploaded yet")
    
    if st.session_state.job_text:
        st.success("✅ Job loaded")
    else:
        st.info("ℹ️ No job analyzed yet")
    
    st.divider()
    st.caption("Running 100% locally on Mistral")

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Resume",
    "🔍 Job Search", 
    "📈 Job Analyzer",
    "✉️ Cover Letter",
    "💼 Interview Prep"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUME
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("📄 Upload Your Resume")
    st.caption("Upload once — all other features use this automatically.")
    
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    st.session_state.user_name = st.text_input("Your Full Name:", placeholder="e.g. Sam Wright")
    if uploaded_file:
        with st.spinner("Reading your resume..."):
            raw_text = extract_resume_text(uploaded_file)
            st.session_state.resume_text = raw_text
        
        st.success("Resume uploaded successfully!")
        
        if st.button("🧠 Parse with AI", type="primary"):
            with st.spinner("Mistral is analyzing your resume..."):
                parsed = parse_resume_with_ai(raw_text)
                st.session_state.parsed_resume = parsed["parsed"]
            
            st.subheader("What Mistral sees:")
            st.markdown(st.session_state.parsed_resume)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — JOB SEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("🔍 Job Search")
    st.caption("Based on your resume, find jobs that match your profile.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    else:
        if st.button("🔍 Find Matching Jobs", type="primary"):
            with st.spinner("Mistral is finding the best jobs for you..."):
                suggestions = search_jobs(st.session_state.parsed_resume or st.session_state.resume_text)
            
            st.subheader("Recommended Jobs For You:")
            st.markdown(suggestions)
        
        st.divider()
        st.subheader("🔗 Search on Job Boards")
        job_title_input = st.text_input("Enter a job title to search:", placeholder="e.g. Data Analyst")
        
        if job_title_input:
            links = scrape_job_listings(job_title_input)
            cols = st.columns(len(links))
            for i, (board, url) in enumerate(links.items()):
                with cols[i]:
                    st.link_button(f"Search {board}", url)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — JOB ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("🎯 Job Analyzer")
    st.caption("Paste any job URL — we scrape it and score your match.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    else:
        job_url = st.text_input("Paste job posting URL:", placeholder="https://...")
        
        if job_url:
            if st.button("⚡ Analyze This Job", type="primary"):
                with st.spinner("Scraping job posting..."):
                    job_text = scrape_job(job_url)
                    st.session_state.job_text = job_text
                
                with st.spinner("Mistral is scoring your match..."):
                    analysis = analyze_match(
                        st.session_state.resume_text,
                        st.session_state.job_text
                    )
                
                st.subheader("Match Analysis:")
                st.markdown(analysis)
                # Extract match score from analysis
                score = ""
                for line in analysis.split("\n"):
                    if "MATCH SCORE" in line:
                        digits = ''.join(filter(str.isdigit, line))
                        score = digits[:2] if len(digits) > 2 else digits
                        break

                # Log to Airtable
                details = extract_job_details(st.session_state.job_text)

                logged = log_job_to_airtable(
                    job_title=details["job_title"],
                    company=details["company"],
                    job_url=job_url,
                    match_score=score,
                    notes=analysis
                )

                if logged:
                    st.success("✅ Job logged to Airtable!")
                else:
                    st.warning("⚠️ Airtable logging failed — check your token.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — COVER LETTER
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("✉️ Cover Letter Generator")
    st.caption("Tailored to the specific job — not a generic template.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    elif not st.session_state.job_text:
        st.warning("Please analyze a job in the Job Analyzer tab first.")
    else:
        extra_info = st.text_area(
            "Any extra context to include? (optional)",
            placeholder="e.g. I've used their product for 2 years, mention my freelance experience..."
        )
        
        if st.button("✉️ Generate Cover Letter", type="primary"):
            with st.spinner("Writing your cover letter..."):
                letter = generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.job_text,
                    extra_info
                )
            if "Regards" in letter:
                 letter = letter.split("Regards")[0] + f"Regards,\n\n{st.session_state.user_name}"
            
            # Update Airtable with cover letter
            if st.session_state.job_text:
                log_job_to_airtable(
                    job_title="Cover Letter Generated",
                    company="See Notes",
                    job_url="N/A",
                    match_score="0",
                    cover_letter=letter,
                    notes="Cover letter generated"
                )

            st.subheader("Your Cover Letter:")
            st.markdown(letter)
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=25)
            pdf.set_font("Courier", size=11)

            page_width = pdf.w - 20
            for line in letter.split("\n"):
                if line.strip() == "":
                    pdf.ln(4)
                else:
                    safe_line = line.strip().encode("latin-1", errors="replace").decode("latin-1")
                    pdf.multi_cell(page_width, 7, safe_line)
            
            pdf.ln(10)
            pdf_bytes = bytes(pdf.output())

            st.download_button(
                "⬇️ Download as PDF",
                data=pdf_bytes,
                file_name="cover_letter.pdf",
                mime="application/pdf"
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — INTERVIEW PREP
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("🎤 Interview Prep")
    st.caption("Predicted questions with tailored answer frameworks.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    elif not st.session_state.job_text:
        st.warning("Please analyze a job in the Job Analyzer tab first.")
    else:
        if st.button("🎤 Generate Interview Questions", type="primary"):
            with st.spinner("Mistral is predicting your interview questions..."):
                questions = generate_interview_questions(
                    st.session_state.resume_text,
                    st.session_state.job_text
                )
            
            st.subheader("Your Interview Prep Guide:")
            st.markdown(questions)
            st.download_button(
                "⬇️ Download as TXT",
                questions,
                file_name="interview_prep.txt",
                mime="text/plain"
            )