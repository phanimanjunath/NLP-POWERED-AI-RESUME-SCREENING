

from modules.extractor import extract_resume_info
from modules.skills    import skill_gap_analysis
from modules.scorer    import hybrid_score, batch_semantic_scores


def rank_candidates(job_desc: str,
                    candidates: list) -> list:
    """
    Ranks multiple candidates against a job description.
    Uses hybrid scoring — Skills + TF-IDF + Semantic.

    Args:
        job_desc:   Job description text
        candidates: List of dicts with 'name' and 'text'
    Returns:
        Ranked list of candidates with full analysis
    """
    results = []

    resume_texts   = [c["text"] for c in candidates]
    semantic_scores = batch_semantic_scores(job_desc, resume_texts)

    for i, candidate in enumerate(candidates):
        name = candidate["name"]
        text = candidate["text"]

        
        info = extract_resume_info(text)

       
        gap  = skill_gap_analysis(text, job_desc)

        scores = hybrid_score(
            text,
            job_desc,
            gap["skill_score"]
        )

        
        final = scores["final_score"]
        if final >= 70:
            verdict = "Strong Match"
        elif final >= 50:
            verdict = "Partial Match"
        else:
            verdict = "Weak Match"

        results.append({
            "name":             name,
            "final_score":      final,
            "skill_score":      scores["skill_score"],
            "tfidf_score":      scores["tfidf_score"],
            "semantic_score":   scores["semantic_score"],
            "matched_skills":   gap["matched_skills"],
            "missing_skills":   gap["missing_skills"],
            "verdict":          verdict,
            "info":             info,
        })

   
    return sorted(
        results,
        key=lambda x: x["final_score"],
        reverse=True
    )


def rank_single(job_desc: str,
                resume_text: str,
                candidate_name: str = "Candidate") -> dict:
    """
    Analyzes a single resume against a job description.
    Used in Streamlit single resume mode.

    Args:
        job_desc:       Job description text
        resume_text:    Resume text
        candidate_name: Name of candidate
    Returns:
        Full analysis dictionary
    """
    results = rank_candidates(
        job_desc,
        [{"name": candidate_name, "text": resume_text}]
    )
    return results[0]