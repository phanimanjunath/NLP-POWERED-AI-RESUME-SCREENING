
import re
import spacy
from data.skills_db import SKILLS_DB

nlp = spacy.load("en_core_web_md")


def extract_skills(text: str) -> list:
    """
    Extracts skills from text using Skills Database.
    Handles abbreviations like ML, DL, TF, NLP.

    Args:
        text: Resume or job description text
    Returns:
        Sorted list of standard skill names
    """
    text_lower = text.lower()
    found      = set()

    for variation, standard_name in SKILLS_DB.items():
        pattern = r"\b" + re.escape(variation) + r"\b"
        if re.search(pattern, text_lower):
            found.add(standard_name)

    return sorted(list(found))


def extract_skills_pos(text: str) -> list:
    """
    Extracts skill candidates using POS tagging.
    Fallback for skills not in the database.
    Uses noun chunks to keep compound skills together.

    Args:
        text: Resume or job description text
    Returns:
        List of noun-based skill candidates
    """
    doc    = nlp(text.lower())
    skills = []

    for chunk in doc.noun_chunks:
        clean = " ".join([
            token.lemma_ for token in chunk
            if not token.is_stop
            and token.is_alpha
            and len(token.text) > 1
            and token.pos_ in ("NOUN", "PROPN", "ADJ")
        ])
        if clean and len(clean) > 2:
            skills.append(clean)

    return sorted(list(set(skills)))


def extract_all_skills(text: str) -> list:
    """
    Combines Skills DB + POS extraction.
    Most comprehensive skill extraction.

    Args:
        text: Resume or job description text
    Returns:
        Combined list of all skills found
    """
    db_skills  = extract_skills(text)
    pos_skills = extract_skills_pos(text)

    
    all_skills = list(set(db_skills + pos_skills))
    return sorted(all_skills)


def skill_gap_analysis(resume: str, job_desc: str) -> dict:
    """
    Compares resume skills against job description skills.
    Returns matched skills, missing skills, and match score.

    Args:
        resume:   Resume text
        job_desc: Job description text
    Returns:
        Dictionary with skill comparison results
    """
    resume_skills = set(extract_skills(resume))
    jd_skills     = set(extract_skills(job_desc))

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    extra   = resume_skills - jd_skills

    score = round(
        len(matched) / len(jd_skills) * 100, 1
    ) if jd_skills else 0.0

    return {
        "resume_skills":  sorted(resume_skills),
        "jd_skills":      sorted(jd_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "extra_skills":   sorted(extra),
        "skill_score":    score,
    }