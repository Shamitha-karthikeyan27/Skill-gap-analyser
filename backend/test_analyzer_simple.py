from analyzer import extract_skills_from_text
import json

test_text = """
Experienced Python Developer with expertise in SQL and Machine Learning.
Skilled in React and Node.js.
Worked at Google for 3 years.
"""

try:
    res = extract_skills_from_text(test_text)
    print("SUCCESS")
    print(json.dumps(res, indent=2))
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
