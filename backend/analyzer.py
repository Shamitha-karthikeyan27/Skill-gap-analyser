import spacy
from db import query_db

try:
    nlp = spacy.load("en_core_web_md")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
    nlp = spacy.load("en_core_web_md")


def extract_skills_from_text(text):
    """Extract skills from plain text using spaCy keyword matching."""
    master_skills = query_db("SELECT id, name FROM skills")
    skill_map = {s['name'].lower(): s['name'] for s in master_skills}

    doc = nlp(text.lower())
    found = set()

    # Token-by-token match
    for token in doc:
        if token.text in skill_map:
            found.add(skill_map[token.text])

    # Multi-word phrase match
    for skill_lower, skill_original in skill_map.items():
        if ' ' in skill_lower and skill_lower in text.lower():
            found.add(skill_original)

    return list(found)


def extract_text_from_pdf(file_bytes):
    """Extract raw text from PDF bytes using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    except Exception as e:
        return ""


def extract_skills_from_pdf(file_bytes):
    """Full pipeline: PDF bytes -> text -> skills."""
    text = extract_text_from_pdf(file_bytes)
    if not text:
        return []
    return extract_skills_from_text(text)


def calculate_gap(user_skill_names, target_job_id):
    """Calculate skill gap between user skills and role requirements."""
    required = query_db("""
        SELECT s.name FROM job_skills js
        JOIN skills s ON js.skill_id = s.id
        WHERE js.job_id = %s
    """, (target_job_id,))

    required_names = [r['name'] for r in required]
    user_lower = [s.lower() for s in user_skill_names]

    matched = [s for s in required_names if s.lower() in user_lower]
    missing = [s for s in required_names if s.lower() not in user_lower]

    pct = round((len(matched) / len(required_names)) * 100, 1) if required_names else 0

    # Get recommendations for missing skills
    recs = []
    if missing:
        placeholders = ','.join(['%s'] * len(missing))
        recs = query_db(f"""
            SELECT r.*, s.name as skill_name FROM recommendations r
            JOIN skills s ON r.skill_id = s.id
            WHERE s.name IN ({placeholders})
        """, tuple(missing))

    return {
        "match_percentage": pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": [dict(r) for r in recs]
    }
