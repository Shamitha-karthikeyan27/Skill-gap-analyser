import sqlite3
import os

DB = 'c:/Users/shamitha/Desktop/Skill gap analyser/backend/skillgap.db'

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

print("--- JOB ROLES ---")
for r in conn.execute("SELECT id, title FROM job_roles").fetchall():
    print(f"[{r[0]}] {r[1]}")

print("\n--- SKILLS FOR DATA ANALYST (Role 1) ---")
for s in conn.execute("""
    SELECT s.name FROM skills s 
    JOIN job_skills js ON js.skill_id = s.id 
    WHERE js.job_id = 1
""").fetchall():
    print(f"- {s[0]}")

print("\n--- ALL SKILLS ---")
skills = conn.execute("SELECT name FROM skills LIMIT 50").fetchall()
print(", ".join([s[0] for s in skills]))
conn.close()
