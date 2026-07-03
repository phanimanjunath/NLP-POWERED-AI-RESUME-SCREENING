# ✈️ NLP-Powered AI Resume Screening System

> Built with Python · spaCy · TF-IDF · Sentence Transformers · Streamlit

An intelligent resume screening and job matching system that parses PDF resumes, extracts structured information using NLP, and ranks candidates against job descriptions using hybrid AI scoring.

---

## Features

- **PDF Parsing** — Extracts raw text from PDF resumes using pdfplumber
- **Information Extraction** — Extracts name, email, phone, companies, locations, CGPA using spaCy NER + Regex
- **Skill Extraction** — Matches 100+ skill variations using custom Skills Database
- **Hybrid Scoring** — Combines Skills Match (30%) + TF-IDF (30%) + Semantic (40%)
- **Semantic Matching** — Understands that "neural networks" ≈ "deep learning" using Sentence Transformers
- **Skill Gap Analysis** — Shows matched and missing skills clearly
- **Candidate Ranking** — Ranks multiple candidates with medal system
- **Web Interface** — Clean Streamlit UI with single and multi-resume modes

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| NLP Pipeline | spaCy (en_core_web_md) |
| Semantic Matching | Sentence Transformers (all-MiniLM-L6-v2) |
| Keyword Matching | scikit-learn TF-IDF + Cosine Similarity |
| PDF Parsing | pdfplumber |
| Web UI | Streamlit |
| Information Extraction | Regex (re module) |

---

## How Scoring Works

```
Final Score = Skills Match (30%) + TF-IDF Score (30%) + Semantic Score (40%)

Skills Match   →  Exact skill keyword matching using Skills Database
TF-IDF Score   →  Important word frequency matching
Semantic Score →  Meaning-based matching using Sentence Transformers
```

**Score Interpretation:**
- ✅ 70%+ → Strong Match — Recommended for interview
- ⚠️ 50-70% → Partial Match — Consider with reservations
- ❌ Below 50% → Weak Match — Does not meet requirements

---

## Project Structure

```
resume_screener/
├── app.py                 ← Streamlit web interface
├── requirements.txt       ← Python dependencies
├── data/
│   └── skills_db.py       ← 100+ skill variations database
├── modules/
│   ├── __init__.py
│   ├── parser.py          ← PDF text extraction
│   ├── extractor.py       ← NER + Regex information extraction
│   ├── skills.py          ← Skills DB + POS skill matching
│   ├── scorer.py          ← TF-IDF + Semantic scoring
│   └── ranker.py          ← Candidate ranking pipeline
└── sample_resumes/        ← Test PDF resumes
```

---

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

---

## Run

```bash
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## NLP Pipeline

```
PDF Resume
    ↓
Text Extraction (pdfplumber)
    ↓
Tokenization + Cleaning (spaCy)
    ↓
Named Entity Recognition  →  name, companies, locations
Regex Extraction          →  email, phone, CGPA
Skills Extraction         →  matched against Skills Database
    ↓
TF-IDF Vectorization      →  keyword matching score
Sentence Transformer      →  semantic similarity score
    ↓
Hybrid Score              →  final match percentage
    ↓
Candidate Ranking
```

---

## Author

**Yanna Phani Manjunath Reddy**
AIML Student | VIT-AP University
Aspiring Aviation AI Engineer ✈️

---

*"Hardwork at evenings. Boosts at morning. Shine and rise at future."*
