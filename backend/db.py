import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# We use SQLite (file-based) for now — no server needed.
DB_PATH = os.path.join(os.path.dirname(__file__), 'skillgap.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # returns dict-like rows
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def query_db(query, args=(), one=False):
    """Run a SELECT and return list of dicts (or single dict if one=True)."""
    # Translate %s placeholders → ? for SQLite
    query = query.replace('%s', '?')
    # Remove PostgreSQL-specific clauses that break SQLite
    query = query.replace('ORDER BY RANDOM()', 'ORDER BY RANDOM()')
    with get_conn() as conn:
        cur = conn.execute(query, args)
        rows = [dict(r) for r in cur.fetchall()]
    return (rows[0] if rows else None) if one else rows


def execute_db(query, args=()):
    """Run an INSERT/UPDATE/DELETE."""
    query = query.replace('%s', '?')
    with get_conn() as conn:
        conn.execute(query, args)
        conn.commit()
