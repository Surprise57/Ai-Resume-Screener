import re

# Dictionary mapping skill variations/aliases to a clean Display Name
SKILL_ALIASES = {
    # Tools & Platforms (Fixes Google Colab / Collab / Colab variations)
    "google colab": "Google Colab",
    "colab": "Google Colab",
    "collab": "Google Colab",
    "google collab": "Google Colab",
    "vs code": "VS Code",
    "vscode": "VS Code",
    "visual studio code": "VS Code",
    "jupyter": "Jupyter Notebook",
    "jupyter notebook": "Jupyter Notebook",
    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",
    "netlify": "Netlify",
    # Languages (Case-Insensitive)
    "python": "Python",
    "java": "Java",
    "sql": "SQL",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "c++": "C++",
    "r": "R",
    # Frameworks & Libraries
    "numpy": "NumPy",
    "pandas": "Pandas",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",
    "keras": "Keras",
    "opencv": "OpenCV",
    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",
    "nltk": "NLTK",
    "xgboost": "XGBoost",
    "streamlit": "Streamlit",
    # Concepts & ML
    "regression": "Regression",
    "classification": "Classification",
    "clustering": "Clustering",
    "data preprocessing": "Data Preprocessing",
    "eda": "Exploratory Data Analysis (EDA)",
    "exploratory data analysis": "Exploratory Data Analysis (EDA)",
    "feature engineering": "Feature Engineering",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "model deployment": "Model Deployment",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "computer vision": "Computer Vision",
    "statistical analysis": "Statistical Analysis",
    "data visualization": "Data Visualization",
    "data analytics": "Data Analytics",
    "forensic technology": "Forensic Technology",
    "genai": "Generative AI",
    "generative ai": "Generative AI",
    "llms": "LLMs",
    "rag": "RAG",
    "ai agents": "AI Agents",
    # Soft Skills
    "problem solving": "Problem Solving",
    "time management": "Time Management",
    "team leadership": "Team Leadership",
    "communication": "Communication",
    "collaboration": "Collaboration",
}

# Skill Categorization for the UI
SKILL_CATEGORIES = {
    "Technical Skills & Languages": ["Python", "Java", "SQL", "JavaScript", "HTML", "CSS", "C++", "R"],
    "AI / ML & Frameworks": [
        "NumPy", "Pandas", "Scikit-Learn", "TensorFlow", "Keras", "OpenCV", 
        "Hugging Face", "NLTK", "XGBoost", "Streamlit", "Regression", 
        "Classification", "Clustering", "NLP", "Deep Learning", "Machine Learning", "Computer Vision"
    ],
    "Core Concepts & Analytics": [
        "Data Preprocessing", "Exploratory Data Analysis (EDA)", "Feature Engineering", 
        "Model Deployment", "Statistical Analysis", "Data Visualization", 
        "Data Analytics", "Forensic Technology", "Generative AI", "LLMs", "RAG", "AI Agents"
    ],
    "Tools & Platforms": ["Git", "GitHub", "Jupyter Notebook", "VS Code", "Google Colab", "Docker", "Netlify"],
    "Soft Skills & Attributes": ["Problem Solving", "Time Management", "Team Leadership", "Communication", "Collaboration"]
}


def extract_skills(text):
    """Extracts all skills from text, completely case-insensitive and mapped to canonical names."""
    if not text:
        return set()

    # Convert whole text to lower case for case-insensitive matching
    text_lower = text.lower()
    found_skills = set()

    for alias, canonical_name in SKILL_ALIASES.items():
        # Match exact word boundaries regardless of upper/lowercase
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(canonical_name)

    return found_skills


def extract_categorized_skills(text):
    """Groups extracted skills into their respective UI categories."""
    all_found = extract_skills(text)
    categorized = {cat: set() for cat in SKILL_CATEGORIES}

    for skill in all_found:
        for category, cat_skills in SKILL_CATEGORIES.items():
            if skill in cat_skills:
                categorized[category].add(skill)

    return categorized


def compare_skills(resume_skills, job_skills):
    """Compares matched vs missing skills."""
    matching = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)
    return matching, missing