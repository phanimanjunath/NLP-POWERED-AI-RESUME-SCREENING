# app.py
# AI Resume Screening System — Streamlit UI
# Built with NLP: spaCy + TF-IDF + Sentence Transformers

import streamlit as st
from modules.parser    import parse_resume_from_upload
from modules.extractor import extract_resume_info
from modules.skills    import skill_gap_analysis
from modules.scorer    import hybrid_score
from modules.ranker    import rank_candidates

# -----------------------------------------------
# PAGE CONFIG
# -----------------------------------------------

st.set_page_config(
    page_title = "AI Resume Screener",
    page_icon  = "✈️",
    layout     = "wide"
)

# -----------------------------------------------
# HEADER
# -----------------------------------------------

st.title("✈️ NLP-Powered AI Resume Screening System")
st.markdown(
    "Built with **spaCy · TF-IDF · Sentence Transformers** | "
    "By Yanna Phani Manjunath Reddy"
)
st.divider()

# -----------------------------------------------
# SIDEBAR — MODE SELECTION
# -----------------------------------------------

st.sidebar.title("⚙️ Settings")
mode = st.sidebar.radio(
    "Select Mode",
    ["Single Resume", "Multiple Resumes (Ranking)"]
)

st.sidebar.divider()
st.sidebar.markdown("### How Scoring Works")
st.sidebar.markdown("""
- **Skills Match** — 30%
- **TF-IDF Score** — 30%
- **Semantic Score** — 40%
""")

# -----------------------------------------------
# JOB DESCRIPTION INPUT
# -----------------------------------------------

st.subheader("📋 Job Description")
job_desc = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Looking for a Python ML Engineer with NLP experience..."
)

st.divider()

# -----------------------------------------------
# MODE 1 — SINGLE RESUME
# -----------------------------------------------

if mode == "Single Resume":

    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload PDF resume",
        type=["pdf"]
    )

    if uploaded_file and job_desc:

        with st.spinner("Analyzing resume..."):

            # Parse resume
            resume_text = parse_resume_from_upload(uploaded_file)

            # Extract info
            info   = extract_resume_info(resume_text)

            # Skill analysis
            gap    = skill_gap_analysis(resume_text, job_desc)

            # Compute scores
            scores = hybrid_score(
                resume_text,
                job_desc,
                gap["skill_score"]
            )

        # ── Candidate Info ──────────────────────────
        st.subheader("👤 Candidate Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**Name:** {info['name'] or 'Not found'}")
            st.markdown(f"**Email:** {info['email'] or 'Not found'}")

        with col2:
            st.markdown(f"**Phone:** {info['phone'] or 'Not found'}")
            st.markdown(f"**LinkedIn:** {info['linkedin'] or 'Not found'}")

        with col3:
            st.markdown(f"**Location:** {', '.join(info['locations']) or 'Not found'}")
            st.markdown(f"**CGPA:** {info['cgpa'][0] if info['cgpa'] else 'Not found'}")

        st.divider()

        # ── Match Scores ─────────────────────────────
        st.subheader("📊 Match Scores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 Final Score",    f"{scores['final_score']}%")
        with col2:
            st.metric("🔧 Skills Match",   f"{scores['skill_score']}%")
        with col3:
            st.metric("📝 TF-IDF Score",   f"{scores['tfidf_score']}%")
        with col4:
            st.metric("🧠 Semantic Score", f"{scores['semantic_score']}%")

        # Score bar
        final = scores["final_score"]
        st.progress(int(final))

        if final >= 70:
            st.success("✅ Strong Match — Recommended for interview")
        elif final >= 50:
            st.warning("⚠️ Partial Match — Consider with reservations")
        else:
            st.error("❌ Weak Match — Does not meet requirements")

        st.divider()

        # ── Skills Analysis ───────────────────────────
        st.subheader("🛠️ Skills Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Matched Skills")
            if gap["matched_skills"]:
                for skill in gap["matched_skills"]:
                    st.success(f"✅ {skill}")
            else:
                st.info("No matched skills found")

        with col2:
            st.markdown("### ❌ Missing Skills")
            if gap["missing_skills"]:
                for skill in gap["missing_skills"]:
                    st.error(f"❌ {skill}")
            else:
                st.success("No missing skills — Perfect match!")

        st.divider()

        # ── Resume Skills ─────────────────────────────
        st.subheader("📋 All Resume Skills")
        if gap["resume_skills"]:
            skills_text = "  •  ".join(gap["resume_skills"])
            st.markdown(skills_text)
        else:
            st.info("No skills detected")

        # ── Raw Text ──────────────────────────────────
        with st.expander("📄 View Extracted Resume Text"):
            st.text(resume_text)

    elif uploaded_file and not job_desc:
        st.warning("⚠️ Please enter a job description above")

    elif job_desc and not uploaded_file:
        st.info("📄 Please upload a resume PDF")

# -----------------------------------------------
# MODE 2 — MULTIPLE RESUMES RANKING
# -----------------------------------------------

elif mode == "Multiple Resumes (Ranking)":

    st.subheader("📄 Upload Multiple Resumes")
    uploaded_files = st.file_uploader(
        "Upload PDF resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and job_desc:

        with st.spinner(f"Analyzing {len(uploaded_files)} resumes..."):

            # Build candidates list
            candidates = []
            for file in uploaded_files:
                text = parse_resume_from_upload(file)
                name = extract_resume_info(text)["name"] or file.name
                candidates.append({
                    "name": name,
                    "text": text
                })

            # Rank all candidates
            results = rank_candidates(job_desc, candidates)

        # ── Ranking Table ─────────────────────────────
        st.subheader("🏆 Candidate Rankings")

        for i, result in enumerate(results):

            rank_emoji = ["🥇", "🥈", "🥉"]
            emoji      = rank_emoji[i] if i < 3 else f"#{i+1}"

            with st.expander(
                f"{emoji} {result['name']} — "
                f"{result['final_score']}% — {result['verdict']}"
            ):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Final Score",    f"{result['final_score']}%")
                with col2:
                    st.metric("Skills Match",   f"{result['skill_score']}%")
                with col3:
                    st.metric("TF-IDF",         f"{result['tfidf_score']}%")
                with col4:
                    st.metric("Semantic",       f"{result['semantic_score']}%")

                st.progress(int(result["final_score"]))

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**✅ Matched Skills:**")
                    if result["matched_skills"]:
                        for s in result["matched_skills"]:
                            st.success(f"✅ {s}")
                    else:
                        st.info("None")

                with col2:
                    st.markdown("**❌ Missing Skills:**")
                    if result["missing_skills"]:
                        for s in result["missing_skills"]:
                            st.error(f"❌ {s}")
                    else:
                        st.success("None — Perfect match!")

    elif uploaded_files and not job_desc:
        st.warning("⚠️ Please enter a job description above")

    elif job_desc and not uploaded_files:
        st.info("📄 Please upload resume PDFs")

# -----------------------------------------------
# FOOTER
# -----------------------------------------------

st.divider()
st.markdown(
    "**AI Resume Screening System** | "
    "Built with Python · spaCy · TF-IDF · "
    "Sentence Transformers · Streamlit"
)