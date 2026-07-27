import re

# Skill Database divided into distinct categories
SKILL_CATEGORIES = {
    "Technical Skills & Languages": [
        "python",
        "java",
        "sql",
        "javascript",
        "html",
        "css",
        "c++",
        "r",
    ],
    "AI / ML & Frameworks": [
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
        "regression",
        "classification",
        "clustering",
        "nlp",
        "natural language processing",
        "deep learning",
        "machine learning",
        "computer vision",
    ],
    "Core Concepts & Analytics": [
        "data preprocessing",
        "eda",
        "exploratory data analysis",
        "feature engineering",
        "model deployment",
        "statistical analysis",
        "data visualization",
        "data analytics",
        "forensic technology",
        "genai",
        "generative ai",
        "llms",
        "rag",
        "ai agents",
    ],
    "Tools & Platforms": [
        "git",
        "github",
        "jupyter notebook",
        "vs code",
        "google colab",
        "docker",
        "netlify",
    ],
    "Soft Skills & Attributes": [
        "problem solving",
        "time management",
        "team leadership",
        "communication",
        "collaboration",
        "critical thinking",
    ],
}


def extract_categorized_skills(text):
    """Extracts skills grouped by category."""
    if not text:
        return {category: set() for category in SKILL_CATEGORIES}

    text_lower = text.lower()
    categorized_skills = {}

    for category, skills in SKILL_CATEGORIES.items():
        found = set()
        for skill in skills:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                found.add(skill.title())
        categorized_skills[category] = found

    return categorized_skills


def extract_skills(text):
    """Extracts all skills as a flat set for ATS scoring."""
    categorized = extract_categorized_skills(text)
    all_skills = set()
    for category_skills in categorized.values():
        all_skills.update(category_skills)
    return all_skills


def compare_skills(resume_skills, job_skills):
    """Compares flat skill sets."""
    matching = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)
    return matching, missing