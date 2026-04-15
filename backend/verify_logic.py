import sys
import os

# Add backend to path to import analyzer
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from analyzer import extract_skills_from_text, calculate_gap

def test_extraction_and_scoring():
    print("--- 1. Testing HTML/CSS and C++ Extraction ---")
    text_with_special = "Skills: HTML/CSS, React, Node.js, C++, C#"
    res = extract_skills_from_text(text_with_special)
    extracted = list(res['skills'].keys())
    print(f"Extracted: {extracted}")
    
    missing = []
    for s in ["HTML/CSS", "React", "Node.js"]:
        if s not in extracted:
            missing.append(s)
            
    if not missing:
        print("✅ Special symbols correctly extracted!")
    else:
        print(f"❌ Missed special symbols: {missing}")

    print("\n--- 2. Testing Person A vs Person B Scoring (The Suitability Problem) ---")
    # Person A: Expert in 3 core skills (Full Stack Role)
    person_a_skills = {
        "React": {"score": 9.5, "category": "Frontend"},
        "JavaScript": {"score": 9.0, "category": "Frontend"},
        "Node.js": {"score": 9.0, "category": "Backend"}
    }
    
    # Person B: Beginner in 10 disconnected skills
    person_b_skills = {
        "HTML/CSS": {"score": 3.0}, "SQL": {"score": 3.0}, "Git": {"score": 3.0},
        "Python": {"score": 3.0}, "Docker": {"score": 3.0}, "MongoDB": {"score": 3.0},
        "Tableau": {"score": 3.0}, "Excel": {"score": 3.0}, "Communication": {"score": 3.0},
        "Power BI": {"score": 3.0}
    }
    
    # Job ID 3 (Full Stack Developer)
    gap_a = calculate_gap(person_a_skills, 3)
    gap_b = calculate_gap(person_b_skills, 3)

    print(f"Person A Suitability Score: {gap_a['suitability_score']}%")
    print(f"Person B Suitability Score: {gap_b['suitability_score']}%")

    if gap_a['suitability_score'] > gap_b['suitability_score']:
        print("✅ Person A (Specialist) scored higher than Person B (Generalist Beginner)!")
    else:
        print("❌ Person B still scores higher. Scoring logic needs tuning.")

def test_fresher_and_oop():
    print("\n--- 3. Testing Fresher Support and OOP Boost ---")
    # Fresher Resume (No 'Experience' header, just projects)
    fresher_text = """
    EDUCATION
    BS in Computer Science
    
    PROJECTS
    E-commerce App: Used React and Node.js. 
    Implemented Class Inheritance and Abstraction for the backend models.
    
    SKILLS
    JavaScript, HTML/CSS, SQL
    """
    res = extract_skills_from_text(fresher_text)
    print(f"Chunks detected: {res['chunks_detected']}")
    print(f"Is Fresher detected: {res['is_fresher']}")
    print(f"Check for OOP depth boost (Inheritance/Abstraction):")
    
    node_metadata = res['skills'].get("Node.js", {})
    print(f"Node.js Metadata: {node_metadata}")
    
    if node_metadata.get("score", 0) >= 5.0:
        print("✅ Depth boost applied correctly!")
    else:
        print("❌ Depth boost not apparent.")

if __name__ == "__main__":
    test_extraction_and_scoring()
    test_fresher_and_oop()
