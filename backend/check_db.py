import sqlite3
import os

DB_PATH = 'skillgap.db'

def check_db():
    if not os.path.exists(DB_PATH):
        print(f"File {DB_PATH} does not exist.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    for table in [t[0] for t in tables]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"Table {table}: {count} rows")
    
    conn.close()

if __name__ == "__main__":
    check_db()
