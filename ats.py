from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_ats_score(resume_text, job_description):
    """Calculates cosine similarity between resume and job description."""
    if not resume_text or not job_description:
        return 0.0

    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_matrix = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:2]
    )
    score = round(similarity_matrix[0][0] * 100, 2)

    return score