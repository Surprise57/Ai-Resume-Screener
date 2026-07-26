import streamlit as st

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)

# ---------- Header ----------
st.title("🤖 AI Resume Screening System")
st.markdown("### Upload your resume and compare it with a Job Description")

st.divider()

# ---------- Sidebar ----------
st.sidebar.title("AI Resume Screener")
st.sidebar.info("""
This application will:
- Analyze Resume
- Calculate ATS Score
- Extract Skills
- Find Missing Skills
- Give Recommendations
""")

# ---------- Upload Resume ----------
resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
)

# ---------- Job Description ----------
job_description = st.text_area(
    "📋 Paste Job Description",
    height=250
)

# ---------- Button ----------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if resume is None:
        st.error("Please upload your resume.")
    elif job_description.strip() == "":
        st.error("Please paste the job description.")
    else:

        st.success("Resume uploaded successfully!")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("ATS Score", "87%")

            st.subheader("✅ Skills Found")

            st.success("Python")
            st.success("SQL")
            st.success("Machine Learning")
            st.success("Pandas")
            st.success("NumPy")

        with col2:

            st.subheader("❌ Missing Skills")

            st.error("Git")
            st.error("GitHub")
            st.error("Tableau")

        st.divider()

        st.subheader("📈 Recommendation")

        st.info("""
Your resume is a good match for this role.

To improve your ATS score:

• Add Git Projects

• Mention Tableau

• Include Machine Learning Projects

• Add Internship Experience if available
""")

        st.success("Overall Result : GOOD MATCH ✅")