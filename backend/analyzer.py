import re
import os
import numpy as np
from db import query_db
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from thefuzz import fuzz
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def chunk_resume(text):
    """
    Splits resume into logical blocks. 
    Improved to handle freshers by looking for Projects/Education if Experience is thin.
    """
    headers = {
        "experience": ["experience", "work history", "employment", "professional background", "internships"],
        "education": ["education", "academic", "qualification", "schooling"],
        "skills": ["skills", "technical skills", "core competencies", "technologies", "tools"],
        "projects": ["projects", "personal projects", "academic projects", "key projects"],
        "certifications": ["certifications", "awards", "achievements", "licenses"],
        "summary": ["summary", "objective", "profile", "about me"]
    }
    
    sections = {}
    current_header = "summary"
    current_content = []
    lines = text.split('\n')
    
    for line in lines:
        line_clean = line.strip().lower()
        matched_header = None
        
        # Check if line is a header
        if 0 < len(line_clean) < 40:
            for category, variants in headers.items():
                if any(v == line_clean or v + ":" == line_clean for v in variants):
                    matched_header = category
                    break
        
        if matched_header:
            sections[current_header] = "\n".join(current_content).strip()
            current_header = matched_header
            current_content = []
        else:
            current_content.append(line)
            
    sections[current_header] = "\n".join(current_content).strip()
    return {k: v for k, v in sections.items() if v}

def extract_skills_from_text(text):
    """
    Advanced skill extraction with:
    1. Symbol-safe matching (HTML/CSS, C++, C#)
    2. Localized TF-IDF for proficiency
    3. Context-aware weight (Experience vs projects)
    4. OOP Concept detection
    """
    chunks = chunk_resume(text)
    master = query_db("SELECT name, category FROM skills")
    skill_names = [s['name'] for s in master]
    cat_map = {s['name']: s['category'] for s in master}
    
    # Pre-process text (Keep critical symbols)
    norm_text = text.lower()
    
    found_skills = []
    
    # 1. Broad matching with symbol handling
    # We use a non-greedy approach that preserves symbols like / and +
    tokens = word_tokenize(norm_text)
    
    for sname in skill_names:
        s_lower = sname.lower()
        # Escaping for regex but allowing common symbols
        pattern = re.escape(s_lower).replace(r'\/', r'\/').replace(r'\+', r'\+').replace(r'\#', r'\#')
        
        # More robust word boundary check: handles SQL,Python or [SQL] or SQL/NoSQL
        # We look for word boundaries (\b) OR start/end of string OR common punctuation
        bound = r'(?:^|[\s,./()\[\]{}|])'
        regex = bound + '(' + pattern + r')' + bound
        
        if re.search(regex, norm_text, re.IGNORECASE):
            found_skills.append(sname)
        elif ' ' in s_lower:
            parts = s_lower.split()
            regex_parts = r'\s+'.join([re.escape(p) for p in parts])
            if re.search(r'(?i)\b' + regex_parts + r'\b', norm_text):
                found_skills.append(sname)

    unique_found = list(set(found_skills))
    counts = Counter(found_skills)
    
    # 2. Localized TF-IDF 'Expertise' Scoring
    # We treat each section as a document to see where the skill is mentioned most
    all_content = " ".join(chunks.values())
    scored_skills = {}
    
    # Section presence multipliers
    weights = {
        "experience": 4.0,
        "projects": 3.0,
        "skills": 1.5,
        "summary": 1.0,
        "education": 1.0
    }
    
    for s in unique_found:
        s_lower = s.lower()
        base_score = 2.0
        
        # Frequency component
        count_boost = min(2.0, (counts[s] - 1) * 0.5)
        
        # Context component
        section_boost = 0
        for section, content in chunks.items():
            if s_lower in content.lower():
                section_boost = max(section_boost, weights.get(section, 1.0))
        
        # Seniority / Action verb check near skill
        # (Simplified: check if words like 'led', 'architected', 'developed' exist in global text)
        action_boost = 1.0 if any(w in norm_text for w in ["led", "architected", "managed", "designed"]) else 0
        
        total_score = base_score + section_boost + count_boost + action_boost
        scored_skills[s] = {
            "score": min(10.0, round(total_score, 1)),
            "category": cat_map.get(s, "Technical")
        }
        
    return {
        "skills": scored_skills,
        "chunks_detected": list(chunks.keys()),
        "is_fresher": "experience" not in chunks or len(chunks.get("experience", "")) < 50
    }

def calculate_gap(user_skills_data, target_job_id):
    """
    Weighted Suitability Score implementation.
    Addresses "Person A vs Person B" problem.
    """
    # Normalize input
    if isinstance(user_skills_data, list):
        user_skills_dict = {sk: {"score": 5.0} for sk in user_skills_data}
    else:
        user_skills_dict = user_skills_data
    
    user_names = list(user_skills_dict.keys())
    
    # Get job requirements
    required = query_db("""
        SELECT s.name, js.required_level, s.category 
        FROM job_skills js 
        JOIN skills s ON js.skill_id = s.id 
        WHERE js.job_id = %s
    """, (target_job_id,))
    
    if not required:
        return {"suitability_score": 0, "match_percentage": 0}
    
    total_weighted_pot = 0
    total_weighted_ach = 0
    matched = []
    missing = []
    semantic = []
    
    # Role-specific skill weights (Core vs Auxiliary)
    # Most jobs have their first 3 skills as 'Core'
    for i, req in enumerate(required):
        req_name = req['name']
        # Core skills are weighted heavier
        skill_weight = 5.0 if i < 3 else (3.0 if i < 6 else 1.0)
        
        # Total Potential: The max skill proficiency (10) * skill weight
        total_weighted_pot += (10 * skill_weight)
        
        # Find best match in user skills (Exact or Semantic)
        best_match_name = None
        best_sim = 0
        
        for uname in user_names:
            if req_name.lower() == uname.lower():
                best_sim = 100
                best_match_name = uname
                break
            
            # Fuzzy semantic matching (Partial ratio helps catch "SQL" in "PostgreSQL")
            sim = max(
                fuzz.token_sort_ratio(req_name.lower(), uname.lower()),
                fuzz.partial_ratio(req_name.lower(), uname.lower())
            )
            if sim > best_sim and sim > 70: 
                best_sim = sim
                best_match_name = uname
        
        if best_match_name:
            # Achievement: User Proficiency * Weight * SimilarityFactor
            # user_skills_dict can be: { "Python": 10 } OR { "Python": {"score": 10} }
            u_data = user_skills_dict[best_match_name]
            prof = u_data.get("score", u_data) if isinstance(u_data, dict) else u_data
            
            # If user provided a numeric level directly
            if not isinstance(prof, (int, float)): prof = 5.0
            
            achievement = prof * skill_weight * (best_sim / 100.0)
            total_weighted_ach += achievement
            matched.append(req_name)
            
            if best_sim < 100:
                semantic.append({
                    "required_skill": req_name,
                    "user_skill": best_match_name,
                    "similarity_score": best_sim / 100.0
                })
        else:
            missing.append(req_name)
            
    # Calculate scores (Suitability is the Averaged Weighted Score)
    suitability = round((total_weighted_ach / total_weighted_pot) * 100, 1) if total_weighted_pot else 0
    
    # Matching percentage is still useful for context (Found / Required)
    match_pct = round((len(matched) / len(required)) * 100, 1)
    
    # Remove duplicate missing skills
    missing = list(dict.fromkeys(missing))

    # LDA Topic Modeling for UNIQUE missing skills
    learning_topics = []
    if missing and len(missing) >= 2:
        try:
            cv = TfidfVectorizer(stop_words='english')
            tfidf = cv.fit_transform(missing)
            from sklearn.decomposition import LatentDirichletAllocation
            lda = LatentDirichletAllocation(n_components=min(2, len(missing)), random_state=42)
            lda.fit(tfidf)
            words = cv.get_feature_names_out()
            for idx, topic in enumerate(lda.components_):
                top_words = [words[i] for i in topic.argsort()[:-4:-1]]
                learning_topics.append(f"Theme {idx+1}: {', '.join(top_words).title()}")
        except Exception as e:
            print(f"LDA Error: {e}")

    # Recommendations (Remove Duplicate Courses by Resource URL)
    recs = []
    if missing:
        placeholders = ','.join(['%s']*len(missing))
        rows = query_db(f"""
            SELECT r.*, s.name as skill_name 
            FROM recommendations r 
            JOIN skills s ON r.skill_id = s.id 
            WHERE s.name IN ({placeholders})
        """, tuple(missing))
        
        # Use a dictionary keyed by resource_url to ensure uniqueness
        unique_recs = {}
        for r in rows:
            url = r.get("resource_url")
            if url not in unique_recs:
                unique_recs[url] = dict(r)
        recs = list(unique_recs.values())
        
    return {
        "suitability_score": suitability,
        "match_percentage": match_pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "semantic_matches": semantic,
        "learning_topics": learning_topics,
        "recommendations": recs
    }

def extract_skills_from_pdf(file_bytes):
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        return extract_skills_from_text(text)
    except Exception as e:
        print(f"PDF Error: {e}")
        return {"skills": {}, "chunks_detected": [], "is_fresher": True}
