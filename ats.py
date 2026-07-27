from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import compare_skills, extract_skills


def calculate_ats_score(resume_text, job_description):
    """Calculates a realistic ATS score using a hybrid of Skill Matching (60%) and TF-IDF Text Similarity (40%)."""
    if not resume_text or not job_description:
        return 0.0

    # 1. Calculate Skill Match Percentage (60% Weight)
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matching, _ = compare_skills(resume_skills, job_skills)

    if len(job_skills) > 0:
        skill_score = (len(matching) / len(job_skills)) * 100
    else:
        skill_score = 50.0  # Default fallback if no skills found in JD

    # 2. Calculate TF-IDF Text Similarity Percentage (40% Weight)
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    text_score = similarity[0][0] * 100

    # 3. Combine both scores (60% skills + 40% text match)
    final_score = (skill_score * 0.60) + (text_score * 0.40)

    return round(final_score, 2)