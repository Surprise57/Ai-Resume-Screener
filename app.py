import streamlit as st
from ats import calculate_ats_score
from resume_parser import extract_text_from_file
from skills import compare_skills, extract_skills

# Set Page Config
st.set_page_config(
    page_title="AI Resume Screener", page_icon="📄", layout="wide"
)

st.title("📄 AI Resume Screener & ATS Matcher")
st.write(
    "Upload a candidate's resume and paste the job description to get a real-time match score."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose PDF or DOCX file", type=["pdf", "docx"]
    )

with col2:
    st.subheader("2. Paste Job Description")
    job_desc = st.text_area("Job Requirements", height=200)

if st.button("Analyze Match", type="primary"):
    if uploaded_file and job_desc:
        # Extract Resume Text
        resume_text = extract_text_from_file(uploaded_file)

        # Extract Skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)
        matching, missing = compare_skills(resume_skills, job_skills)

        # Calculate ATS Score
        score = calculate_ats_score(resume_text, job_desc)

        st.divider()

        # Display Metrics
        st.metric("ATS Match Score", f"{score}%")
        st.progress(score / 100)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("✅ Matching Skills")
            if matching:
                st.write(", ".join(f"`{s}`" for s in matching))
            else:
                st.info("No explicit skill matches found.")

        with c2:
            st.subheader("❌ Missing Skills")
            if missing:
                st.write(", ".join(f"`{s}`" for s in missing))
            else:
                st.success("No missing skills detected!")

        # Downloadable Summary Report
        report = f"""--- AI RESUME SCREENER REPORT ---
Match Score: {score}%
Matching Skills: {', '.join(matching) if matching else 'None'}
Missing Skills: {', '.join(missing) if missing else 'None'}
"""
        st.download_button(
            label="📥 Download Match Report",
            data=report,
            file_name="ATS_Report.txt",
            mime="text/plain",
        )
    else:
        st.warning("Please upload a resume and provide a job description.")