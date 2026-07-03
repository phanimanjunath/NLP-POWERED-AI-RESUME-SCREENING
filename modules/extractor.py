

import re
import spacy

nlp = spacy.load("en_core_web_md")

# -----------------------------------------------
# BLOCKLISTS
# -----------------------------------------------

TECH_TERMS = {
    "postgresql", "tensorflow", "docker", "python",
    "kubernetes", "mongodb", "redis", "nginx",
    "scikit", "pytorch", "aws", "gcp", "azure",
    "pandas", "numpy", "matplotlib", "flask",
    "django", "fastapi", "spark", "kafka",
    "tableau", "powerbi", "excel", "sql",
    "java", "javascript", "html", "css",
    "keras", "spacy", "nltk", "bert", "gpt",
}

JOB_TITLES = {
    # Roles
    "data scientist", "ml engineer", "software engineer",
    "developer", "manager", "analyst", "architect",
    "engineer", "intern", "consultant", "researcher",
    "scientist", "specialist", "lead", "senior", "junior",
    # Resume sections
    "aiml student", "student", "profile", "education",
    "experience", "skills", "projects", "languages",
    "certificate", "certification", "enthusiast",
    "summary", "objective", "declaration", "reference",
    "achievement", "activity", "interest", "hobby",
    # Common noise
    "artificial intelligence", "data analysis",
    "github profile", "linkedin profile",
    "machine learning", "deep learning",
    "data science", "computer science",
}


def extract_contact(text: str) -> dict:
    """
    Extracts contact information using Regex patterns.

    Args:
        text: Raw resume text
    Returns:
        Dictionary with email, phone, linkedin
    """
    
    emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)

    
    phones = re.findall(r"(?:\+91[-\s]?)?\d{10}", text)

   
    linkedin = re.findall(r"linkedin\.com/in/[\w-]+", text)

    
    if not linkedin:
        if re.search(r"linkedin\s*profile", text, re.IGNORECASE):
            linkedin = ["linkedin.com/in/ (see PDF hyperlink)"]

    return {
        "email":    emails,
        "phone":    phones,
        "linkedin": linkedin,
    }




def extract_education(text: str) -> dict:
    """
    Extracts education details using Regex.

    Args:
        text: Raw resume text
    Returns:
        Dictionary with cgpa, graduation_year, experience_years
    """
  
    cgpa = re.findall(
        r"(\d\.\d{1,2})\s*(?:CGPA|GPA|cgpa|gpa)", text
    )
    if not cgpa:
        cgpa = re.findall(
            r"(?:CGPA|GPA|cgpa|gpa)\s*:?\s*(\d\.\d{1,2})", text
        )
    if not cgpa:
       
        cgpa = re.findall(
            r"\b([89]\.\d{1,2})\b", text
        )

   
    years = list(dict.fromkeys(
        re.findall(r"\b(20\d{2})\b", text)
    ))

    experience = re.findall(
        r"\d+\.?\d*\s+years?", text
    )

    return {
        "cgpa":             cgpa[:1],   # take first CGPA only
        "graduation_year":  years,
        "experience_years": experience,
    }




def extract_entities(text: str) -> dict:
    """
    Extracts named entities using spaCy NER.
    Handles candidate name, companies, locations.

    Args:
        text: Raw resume text
    Returns:
        Dictionary with name, companies, locations
    """
    doc = nlp(text)

    entities = {
        "name":      "",
        "companies": [],
        "locations": [],
    }

    for ent in doc.ents:
        clean = ent.text.strip()

       
        if clean.lower() in TECH_TERMS:
            continue

       
        if "\n" in clean:
            continue

        
        if len(clean) <= 2:
            continue

        
        if re.search(r"\d{4}", clean):
            continue

        if ent.label_ == "PERSON":
            if not entities["name"]:
                entities["name"] = clean

        elif ent.label_ in ("ORG", "FAC"):
            if clean.lower() not in JOB_TITLES:
                entities["companies"].append(clean)

        elif ent.label_ == "GPE":
            entities["locations"].append(clean)

   
    entities["companies"] = list(dict.fromkeys(entities["companies"]))
    entities["locations"]  = list(dict.fromkeys(entities["locations"]))

    return entities



def extract_resume_info(text: str) -> dict:
    """
    Complete resume information extractor.
    Combines Regex + spaCy NER for full extraction.

    Args:
        text: Raw resume text
    Returns:
        Dictionary with all extracted resume fields
    """
    contact   = extract_contact(text)
    education = extract_education(text)
    entities  = extract_entities(text)

    return {
        "name":             entities["name"],
        "email":            contact["email"][0]    if contact["email"]    else "",
        "phone":            contact["phone"][0]    if contact["phone"]    else "",
        "linkedin":         contact["linkedin"][0] if contact["linkedin"] else "",
        "companies":        entities["companies"],
        "locations":        entities["locations"],
        "cgpa":             education["cgpa"],
        "graduation_year":  education["graduation_year"],
        "experience_years": education["experience_years"],
    }