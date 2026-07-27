import streamlit as st
from ats import calculate_ats_score
from resume_parser import extract_resume_text
from skills import (
    compare_skills,
    extract_categorized_skills,
    extract_skills,
)

# Page Config
st.set_page_config(
    page_title="AI Resume Screener & ATS Matcher",
    page_icon="⚡",
    layout="wide",
)

# Styling
st.markdown(
    """
    <style>
    .main .block-container { max-width: 1100px; padding-top: 1.5rem; }
    .title-text { font-size: 2.3rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #2563EB, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .badge { display: inline-block; padding: 5px 12px; margin: 3px; border-radius: 15px; font-size: 13px; font-weight: 600; }
    .badge-success { background-color: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
    .badge-danger { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .category-box { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .score-card { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 16px; padding: 20px; color: white; text-align: center; margin-bottom: 20px; }
    .score-number { font-size: 3.5rem; font-weight: 900; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="title-text">⚡ AI Resume Screener & ATS Matcher</div>',
    unsafe_allow_html=True,
)
st.write("Smart ATS screening with section-by-section breakdown.")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("PDF or DOCX", type=["pdf", "docx"])

with col2:
    st.subheader("🎯 Job Description")
    job_desc = st.text_area("Paste job requirements...", height=180)

st.divider()

if st.button("🚀 Analyze Match", type="primary", use_container_width=True):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing parameters across all sections..."):
            resume_text = extract_resume_text(uploaded_file)

            # Categorized Skill Extractions
            resume_cat = extract_categorized_skills(resume_text)
            job_cat = extract_categorized_skills(job_desc)

            # Flat Skills for overall ATS Score
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_desc)

            matching_all, missing_all = compare_skills(resume_skills, job_skills)
            score = calculate_ats_score(resume_text, job_desc)

            # Score Card
            color = (
                "#22C55E"
                if score >= 70
                else ("#F59E0B" if score >= 40 else "#EF4444")
            )
            st.markdown(
                f'<div class="score-card"><div style="color:#94A3B8; text-transform:uppercase;">Overall ATS Match Score</div><div class="score-number" style="color: {color};">{score}%</div></div>',
                unsafe_allow_html=True,
            )
            st.progress(score / 100)
            st.write("")

            st.subheader("📊 Category-by-Category Analysis")

            # Iterate through each skill section separately
            for category in resume_cat.keys():
                r_skills = resume_cat[category]
                j_skills = job_cat[category]

                matched_cat = r_skills.intersection(j_skills)
                missing_cat = j_skills.difference(r_skills)

                # Only show category if the job description mentions skills from it
                if j_skills or r_skills:
                    with st.expander(f"📌 {category}", expanded=True):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**✅ Matched**")
                            if matched_cat:
                                badges = "".join(
                                    [
                                        f'<span class="badge badge-success">{s}</span>'
                                        for s in sorted(matched_cat)
                                    ]
                                )
                                st.markdown(badges, unsafe_allow_html=True)
                            else:
                                st.caption("None matched in this category")

                        with c2:
                            st.markdown("**❌ Missing**")
                            if missing_cat:
                                badges = "".join(
                                    [
                                        f'<span class="badge badge-danger">{s}</span>'
                                        for s in sorted(missing_cat)
                                    ]
                                )
                                st.markdown(badges, unsafe_allow_html=True)
                            else:
                                st.caption("No missing skills in this category")

            st.divider()

            # Suggestions block
            if missing_all:
                st.subheader("💡 Tailored Optimization Suggestions")
                st.info(
                    f"To improve match quality, consider explicitly mentioning missing requirements like: **{', '.join(sorted(list(missing_all))[:6])}**."
                )
    else:
        st.error("Please upload a resume and paste a job description.")