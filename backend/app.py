from flask import Flask, request, jsonify
from flask_cors import CORS
from db import query_db, execute_db
from analyzer import extract_skills_from_text, extract_skills_from_pdf, calculate_gap
from auth import register_user, login_user, decode_token
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:4173"])

# ── helpers ────────────────────────────────────────────────────────────
def current_user():
    auth = request.headers.get('Authorization', '')
    token = auth.replace('Bearer ', '').strip()
    if not token:
        return None
    return decode_token(token)

# ── AUTH ───────────────────────────────────────────────────────────────
@app.route('/api/auth/register', methods=['POST'])
def register():
    d = request.json
    token, err = register_user(d.get('username',''), d.get('email',''), d.get('password',''))
    if err:
        return jsonify({"error": err}), 400
    return jsonify({"token": token})

@app.route('/api/auth/login', methods=['POST'])
def login():
    d = request.json
    token, err = login_user(d.get('email',''), d.get('password',''))
    if err:
        return jsonify({"error": err}), 401
    return jsonify({"token": token})

# ── ROLES ──────────────────────────────────────────────────────────────
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = query_db("SELECT id, title, description, icon FROM job_roles ORDER BY id")
    return jsonify([dict(j) for j in jobs])

# ── RESUME UPLOAD (PDF) ────────────────────────────────────────────────
@app.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    f = request.files['file']
    if not f.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400
    pdf_bytes = f.read()
    skills = extract_skills_from_pdf(pdf_bytes)
    return jsonify({"extracted_skills": skills})

# ── TEXT-BASED SKILL EXTRACTION ────────────────────────────────────────
@app.route('/api/extract-skills', methods=['POST'])
def extract_from_text():
    d = request.json
    text = d.get('text', '')
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400
    skills = extract_skills_from_text(text)
    return jsonify({"extracted_skills": skills})

# ── GAP ANALYSIS ───────────────────────────────────────────────────────
@app.route('/api/analyze', methods=['POST'])
def analyze():
    d = request.json
    skills = d.get('skills', [])
    job_id = d.get('job_id')
    if not skills or not job_id:
        return jsonify({"error": "skills list and job_id are required"}), 400
    result = calculate_gap(skills, int(job_id))
    return jsonify(result)

# ── COMPANIES ──────────────────────────────────────────────────────────
@app.route('/api/companies', methods=['GET'])
def get_companies():
    job_id = request.args.get('job_id')
    if job_id:
        rows = query_db("""
            SELECT c.*, jr.title as role_title FROM companies c
            JOIN job_roles jr ON c.job_role_id = jr.id
            WHERE c.job_role_id = %s
        """, (job_id,))
    else:
        rows = query_db("SELECT * FROM companies")
    return jsonify([dict(r) for r in rows])

# ── MOCK TEST ──────────────────────────────────────────────────────────
@app.route('/api/mock-test', methods=['GET'])
def get_mock_test():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({"error": "job_id required"}), 400
    questions = query_db("""
        SELECT id, question, option_a, option_b, option_c, option_d
        FROM mock_questions WHERE job_id = %s ORDER BY RANDOM() LIMIT 10
    """, (job_id,))
    return jsonify([dict(q) for q in questions])

@app.route('/api/mock-test/submit', methods=['POST'])
def submit_mock_test():
    d = request.json
    answers = d.get('answers', {})   # {question_id: 'A'/'B'/'C'/'D'}
    job_id = d.get('job_id')
    question_ids = list(answers.keys())

    if not question_ids:
        return jsonify({"error": "No answers provided"}), 400

    placeholders = ','.join(['%s'] * len(question_ids))
    questions = query_db(
        f"SELECT id, correct_answer, explanation FROM mock_questions WHERE id IN ({placeholders})",
        tuple(int(x) for x in question_ids)
    )

    score = 0
    feedback = []
    for q in questions:
        user_ans = answers.get(str(q['id']), '').upper()
        correct = q['correct_answer'].upper()
        is_correct = user_ans == correct
        if is_correct:
            score += 1
        feedback.append({
            "question_id": q['id'],
            "your_answer": user_ans,
            "correct_answer": correct,
            "is_correct": is_correct,
            "explanation": q['explanation']
        })

    total = len(questions)
    passed = score >= round(total * 0.6)  # 60% to pass

    return jsonify({
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "passed": passed,
        "feedback": feedback
    })

# ── CHATBOT ────────────────────────────────────────────────────────────
ROADMAPS = {
    "data analyst": [
        "1️⃣ **Learn SQL** — Start with SELECT, JOIN, GROUP BY (2 weeks)",
        "2️⃣ **Python Basics** — Variables, loops, functions (3 weeks)",
        "3️⃣ **Pandas & NumPy** — Data manipulation in Python (2 weeks)",
        "4️⃣ **Statistics** — Mean, median, distributions, hypothesis testing (2 weeks)",
        "5️⃣ **Excel / Google Sheets** — Pivot tables, VLOOKUP (1 week)",
        "6️⃣ **Visualization** — Tableau or Power BI (3 weeks)",
        "7️⃣ **Capstone Project** — Analyze a real dataset and present insights",
    ],
    "data scientist": [
        "1️⃣ **Python + Pandas** — Data wrangling foundations (3 weeks)",
        "2️⃣ **Statistics & Probability** — Core math for ML (3 weeks)",
        "3️⃣ **Machine Learning Basics** — Scikit-learn, regression, classification (4 weeks)",
        "4️⃣ **Deep Learning** — Neural networks with TensorFlow/PyTorch (4 weeks)",
        "5️⃣ **NLP or Computer Vision** — Choose a specialization (4 weeks)",
        "6️⃣ **Model Deployment** — Flask API + Docker (2 weeks)",
        "7️⃣ **Build Portfolio** — 2-3 ML projects on GitHub",
    ],
    "full stack developer": [
        "1️⃣ **HTML/CSS Basics** — Layouts, flexbox, grid (2 weeks)",
        "2️⃣ **JavaScript** — ES6+, async/await, DOM (4 weeks)",
        "3️⃣ **React.js** — Components, hooks, state management (4 weeks)",
        "4️⃣ **Node.js + Express** — REST APIs and routing (3 weeks)",
        "5️⃣ **Databases** — SQL (PostgreSQL) + NoSQL (MongoDB) (2 weeks)",
        "6️⃣ **Git & Deployment** — GitHub, Vercel, Render (1 week)",
        "7️⃣ **Full Stack Project** — Build and deploy a complete app",
    ],
    "machine learning engineer": [
        "1️⃣ **Python + Algorithms** — DSA basics (3 weeks)",
        "2️⃣ **ML Fundamentals** — Scikit-learn (4 weeks)",
        "3️⃣ **Deep Learning** — TensorFlow or PyTorch (4 weeks)",
        "4️⃣ **MLOps Basics** — Experiment tracking, model versioning (3 weeks)",
        "5️⃣ **Docker & Kubernetes** — Containerization for ML (3 weeks)",
        "6️⃣ **Cloud Platforms** — AWS SageMaker or GCP Vertex AI (2 weeks)",
        "7️⃣ **Deploy a Production ML Model** — End-to-end project",
    ],
    "business analyst": [
        "1️⃣ **Excel / Google Sheets** — Formulas, pivot tables (2 weeks)",
        "2️⃣ **SQL** — Data querying for business reports (3 weeks)",
        "3️⃣ **Power BI or Tableau** — Dashboard creation (3 weeks)",
        "4️⃣ **Statistics** — Descriptive stats, trend analysis (2 weeks)",
        "5️⃣ **Business Communication** — Reports, presentations (ongoing)",
        "6️⃣ **Requirement Gathering** — User stories, BRD writing (2 weeks)",
        "7️⃣ **Case Study Project** — Analyze a business problem end-to-end",
    ],
}

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    d = request.json
    message = d.get('message', '').lower()
    role = d.get('role', '').lower()
    missing_skills = d.get('missing_skills', [])

    response = "I'm your AI Career Mentor. Ask me about your role, roadmap, courses, or skill gaps!"

    # Roadmap request
    if any(w in message for w in ['roadmap', 'path', 'how to', 'start', 'begin', 'steps', 'guide']):
        for role_key, steps in ROADMAPS.items():
            if role_key in message or (role and role_key in role):
                response = f"📍 **{role_key.title()} Roadmap:**\n\n" + "\n\n".join(steps)
                break
        else:
            if missing_skills:
                response = f"📌 You are missing: **{', '.join(missing_skills[:3])}**. Focus on these first!\n\nOr tell me your target role and I'll give you a full roadmap."
            else:
                response = "Tell me your target role (e.g. 'Data Scientist roadmap') and I'll give you a step-by-step plan!"

    # Skill gaps
    elif any(w in message for w in ['skill', 'gap', 'missing', 'learn', 'need']):
        if missing_skills:
            response = f"🔍 **Skills you need to develop:**\n• " + "\n• ".join(missing_skills) + "\n\nWant a full roadmap? Just ask!"
        else:
            response = "Upload your resume and select a role to see your skill gaps!"

    # Job / company
    elif any(w in message for w in ['job', 'company', 'apply', 'hire']):
        response = "💼 Once your skills match ≥70% of the role requirements, you'll see top companies hiring for that role. Run an analysis first!"

    # Mock test
    elif any(w in message for w in ['test', 'quiz', 'exam', 'mock', 'eligible']):
        response = "📝 After the skill analysis, you can take a **Mock Test** with 10 MCQ questions. Score ≥60% to be considered eligible for the role!"

    # Greetings
    elif any(w in message for w in ['hello', 'hi', 'hey', 'help']):
        response = "👋 Hello! I'm your **AI Career Mentor**.\n\nI can help you with:\n• 📍 Career roadmaps\n• 🔍 Skill gap analysis\n• 📝 Mock test tips\n• 💼 Company recommendations\n\nWhat would you like to know?"

    return jsonify({"response": response})

# ── RECOMMENDATIONS ────────────────────────────────────────────────────
@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    job_id = request.args.get('job_id')
    if job_id:
        recs = query_db("""
            SELECT r.*, s.name as skill_name FROM recommendations r
            JOIN skills s ON r.skill_id = s.id
            JOIN job_skills js ON js.skill_id = s.id
            WHERE js.job_id = %s
        """, (job_id,))
    else:
        recs = query_db("SELECT r.*, s.name as skill_name FROM recommendations r JOIN skills s ON r.skill_id=s.id")
    return jsonify([dict(r) for r in recs])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
