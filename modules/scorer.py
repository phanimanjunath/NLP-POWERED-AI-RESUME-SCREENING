

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def tfidf_score(resume: str, job_desc: str) -> float:
    """
    Computes TF-IDF cosine similarity between resume and JD.
    Good for keyword matching.

    Args:
        resume:   Resume text
        job_desc: Job description text
    Returns:
        Similarity score 0.0 to 1.0
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf      = vectorizer.fit_transform([resume, job_desc])
    score      = cosine_similarity(tfidf[0], tfidf[1])[0][0]
    return round(float(score), 4)


def semantic_score(resume: str, job_desc: str) -> float:
    """
    Computes semantic similarity using Sentence Transformers.
    Understands meaning — best for overall matching.

    Args:
        resume:   Resume text
        job_desc: Job description text
    Returns:
        Similarity score 0.0 to 1.0
    """
    vec1  = model.encode([resume])
    vec2  = model.encode([job_desc])
    score = cosine_similarity(vec1, vec2)[0][0]
    return round(float(score), 4)


def hybrid_score(resume: str,
                 job_desc: str,
                 skill_score: float) -> dict:
    """
    Computes hybrid match score combining:
      Skills DB match  — 30%
      TF-IDF score     — 30%
      Semantic score   — 40%

    Args:
        resume:      Resume text
        job_desc:    Job description text
        skill_score: Skills match score 0-100
    Returns:
        Dictionary with all scores
    """
    tf  = tfidf_score(resume, job_desc)
    sem = semantic_score(resume, job_desc)

    
    skill_normalized = skill_score / 100

   
    final = (
        skill_normalized * 0.30 +
        tf               * 0.30 +
        sem              * 0.40
    )

    return {
        "skill_score":    round(skill_score, 1),
        "tfidf_score":    round(tf  * 100, 1),
        "semantic_score": round(sem * 100, 1),
        "final_score":    round(final * 100, 1),
    }


def batch_semantic_scores(job_desc: str,
                          resume_texts: list) -> list:
    """
    Computes semantic scores for multiple resumes at once.
    Faster than computing one by one.

    Args:
        job_desc:      Job description text
        resume_texts:  List of resume text strings
    Returns:
        List of similarity scores
    """
    jd_vector      = model.encode([job_desc])
    resume_vectors = model.encode(resume_texts)
    scores         = cosine_similarity(jd_vector, resume_vectors)[0]
    return [round(float(s), 4) for s in scores]