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
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    .title-text {
        font-size: 2.3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle-text {
        font-size: 0.95rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }
    .badge-success {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    .badge-danger {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }
    .score-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 16px;
        padding: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }
    .score-number {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 5px 0;
    }
    .score-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #94A3B8;
    }
    .suggestion-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-radius: 4px;
        color: #1E293B;
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