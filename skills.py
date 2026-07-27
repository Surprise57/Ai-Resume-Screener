import re

# Comprehensive skill dictionary covering Technical, Tools, Frameworks, Concepts, and Soft Skills
SKILL_DATABASE = [
    # Programming Languages
    "python",
    "java",
    "sql",
    "javascript",
    "html",
    "css",
    "c++",
    "r",
    # AI / ML / Data Science Concepts
    "regression",
    "classification",
    "clustering",
    "data preprocessing",
    "eda",
    "exploratory data analysis",
    "feature engineering",
    "nlp",
    "natural language processing",
    "model deployment",
    "machine learning",
    "deep learning",
    "computer vision",
    "sentiment analysis",
    "statistical analysis",
    "data visualization",
    "data analytics",
    "forensic technology",
    # GenAI & Advanced Concepts
    "genai",
    "generative ai",
    "llms",
    "rag",
    "ai agents",
    # Libraries & Frameworks
    "numpy",
    "pandas",
    "scikit-learn",
    "tensorflow",
    "keras",
    "opencv",
    "hugging face",
    "nltk",
    "xgboost",
    "streamlit",
    # Tools & Platforms
    "git",
    "github",
    "jupyter notebook",
    "vs code",
    "google colab",
    "docker",
    "netlify",
    # Soft Skills & Professional Attributes
    "problem solving",
    "time management",
    "team leadership",
    "communication",
    "collaboration",
    "critical thinking",
]


def extract_skills(text):
    """Extracts all matched skills (technical, tools, concepts, soft skills) from text."""
    if not text:
        return set()

    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_DATABASE:
        # Use regex boundary matching to find exact skill words
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())

    return found_skills


def compare_skills(resume_skills, job_skills):
    """Compares resume skills against job description requirements."""
    matching = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)

    return matching, missing