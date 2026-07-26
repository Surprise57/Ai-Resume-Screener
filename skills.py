import re

# Common skills database (You can add more skills to this set!)
COMMON_SKILLS = {
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "node.js",
    "django",
    "flask",
    "fastapi",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "excel",
    "power bi",
    "tableau",
    "rest api",
    "graphql",
    "agile",
    "scrum",
}


def extract_skills(text):
    """Extracts known skills from raw text using regex pattern matching."""
    if not text:
        return set()

    text_lower = text.lower()
    found_skills = set()

    for skill in COMMON_SKILLS:
        # Use regex to match whole words so "c" doesn't match inside "css"
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())

    return found_skills


def compare_skills(resume_skills, job_skills):
    """Compares resume skills against job requirements."""
    matching_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    return matching_skills, missing_skills