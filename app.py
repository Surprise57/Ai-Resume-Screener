import streamlit as st
from ats import calculate_ats_score
from resume_parser import extract_resume_text
from skills import compare_skills, extract_skills

# 1. Page Config
st.set_page_config(
    page_title="AI Resume Screener & ATS Matcher",
    page_icon="⚡",
    layout="wide",
)

# 2. Advanced Modern CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 15% 0%, #F5F7FF 0%, #FFFFFF 35%, #F8FAFC 100%);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1120px;
    }

    /* Header */
    .title-text {
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        background: -webkit-linear-gradient(45deg, #2563EB, #7C3AED 55%, #DB2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        line-height: 1.15;
    }
    .subtitle-text {
        font-size: 1.02rem;
        color: #64748B;
        margin-bottom: 1.8rem;
        font-weight: 500;
    }

    /* Section labels */
    .stSubheader, h3 {
        font-weight: 700 !important;
        color: #0F172A !important;
    }

    /* Card wrapper for inputs */
    div[data-testid="stFileUploader"], div[data-testid="stTextArea"] {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 4px;
    }

    div[data-testid="stFileUploaderDropzone"] {
        border-radius: 14px !important;
        border: 2px dashed #C7D2FE !important;
        background: #F8FAFF !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #7C3AED !important;
        background: #F3F0FF !important;
    }

    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #E2E8F0 !important;
        font-size: 0.95rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12) !important;
    }

    /* Primary button */
    div[data-testid="stButton"] button {
        background: linear-gradient(90deg, #2563EB, #7C3AED) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
        padding: 0.7rem 1rem !important;
        box-shadow: 0 8px 20px -6px rgba(124, 58, 237, 0.55) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -6px rgba(124, 58, 237, 0.65) !important;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 7px 16px;
        margin: 4px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.01em;
        transition: transform 0.15s ease;
    }
    .badge:hover {
        transform: translateY(-2px) scale(1.03);
    }
    .badge-success {
        background: linear-gradient(135deg, #D1FAE5, #A7F3D0);
        color: #065F46;
        border: 1px solid #6EE7B7;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.15);
    }
    .badge-danger {
        background: linear-gradient(135deg, #FEE2E2, #FECACA);
        color: #991B1B;
        border: 1px solid #FCA5A5;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.15);
    }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 55%, #312E81 100%);
        border-radius: 20px;
        padding: 32px 24px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px -12px rgba(30, 27, 75, 0.45);
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .score-number {
        font-size: 4rem;
        font-weight: 900;
        margin: 6px 0;
        text-shadow: 0 4px 14px rgba(0,0,0,0.35);
    }
    .score-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #A5B4FC;
        font-weight: 700;
    }

    /* Progress bar */
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #2563EB, #7C3AED, #DB2777) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stProgress"] > div {
        background-color: #E2E8F0 !important;
        border-radius: 10px !important;
        height: 10px !important;
    }

    /* Suggestion box */
    .suggestion-box {
        background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
        border-left: 4px solid #3B82F6;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-radius: 10px;
        color: #1E293B;
        font-size: 0.98rem;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.08);
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* Divider */
    hr {
        margin: 1.6rem 0 !important;
        border-color: #E2E8F0 !important;
    }

    /* Download button */
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(90deg, #0F172A, #1E293B) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.7rem 1rem !important;
        transition: transform 0.15s ease !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Header Section
st.markdown(
    '<div class="title-text">⚡ AI Resume Screener & ATS Matcher</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle-text">Smart ATS screening with real-time skill gap analysis and action suggestions.</div>',
    unsafe_allow_html=True,
)

# 4. Inputs
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX format", type=["pdf", "docx"]
    )

with col2:
    st.subheader("🎯 Job Description")
    job_desc = st.text_area(
        "Paste the job requirements here...", height=200
    )

st.divider()

# 5. Analysis Logic
analyze_btn = st.button("🚀 Analyze Match", type="primary", use_container_width=True)

if analyze_btn:
    if uploaded_file and job_desc:
        with st.spinner("Analyzing resume and extracting skill insights..."):
            resume_text = extract_resume_text(uploaded_file)
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_desc)

            matching, missing = compare_skills(resume_skills, job_skills)
            score = calculate_ats_score(resume_text, job_desc)

            # Score Card
            color = (
                "#22C55E"
                if score >= 70
                else ("#F59E0B" if score >= 40 else "#EF4444")
            )
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="score-label">Overall ATS Match Score</div>
                    <div class="score-number" style="color: {color};">{score}%</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.progress(score / 100)
            st.write("")

            # Skill Breakdowns
            c1, c2 = st.columns(2, gap="large")

            with c1:
                st.subheader("✅ Matching Skills")
                if matching:
                    badge_html = "".join(
                        [
                            f'<span class="badge badge-success">{s}</span>'
                            for s in sorted(matching)
                        ]
                    )
                    st.markdown(badge_html, unsafe_allow_html=True)
                else:
                    st.info("No explicit skills matched.")

            with c2:
                st.subheader("❌ Missing Skills")
                if missing:
                    badge_html = "".join(
                        [
                            f'<span class="badge badge-danger">{s}</span>'
                            for s in sorted(missing)
                        ]
                    )
                    st.markdown(badge_html, unsafe_allow_html=True)
                else:
                    st.success("All required skills found!")

            st.divider()

            # 💡 Suggestions Section
            st.subheader("💡 ATS Optimization Suggestions")

            if missing:
                st.write(
                    "To increase the candidate's ATS score, consider adding or highlighting the following missing key skills in the project or experience section:"
                )

                missing_list = sorted(list(missing))
                top_missing = missing_list[:5]  # Highlight top missing skills

                st.markdown(
                    f"""
                    <div class="suggestion-box">
                        📌 <b>Key Priority Skills to Add:</b> {', '.join([f'<b>{s}</b>' for s in top_missing])}
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                if score < 50:
                    st.warning(
                        "⚠️ **Low Match Score:** Try tailoring the project descriptions and technical summaries to mirror the wording used in the job description."
                    )
                elif score < 75:
                    st.info(
                        "💡 **Moderate Match Score:** The resume covers key competencies, but incorporating the missing tools and frameworks above will help bypass automated ATS filters."
                    )
                else:
                    st.success(
                        "🌟 **Strong Match Score:** The resume aligns well with the job description!"
                    )
            else:
                st.success(
                    "🎉 Perfect match! No missing skill gaps were detected for this job profile."
                )

            st.divider()

            # Download Report
            report = f"""=====================================
    AI RESUME SCREENER REPORT
=====================================
Overall Match Score: {score}%

MATCHING SKILLS ({len(matching)}):
{', '.join(sorted(matching)) if matching else 'None'}

MISSING SKILLS ({len(missing)}):
{', '.join(sorted(missing)) if missing else 'None'}

SUGGESTIONS:
{f"Add key skills: {', '.join(sorted(missing))}" if missing else "Resume matches all job requirements perfectly!"}
=====================================
"""
            st.download_button(
                label="📥 Download Detailed Match Report",
                data=report,
                file_name=f"ATS_Report_{uploaded_file.name}.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.error("Please upload a resume and provide a job description first.")