import jwt
import os
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from db import query_db, execute_db

SECRET_KEY = os.getenv('JWT_SECRET', 'skillgap-super-secret-2026')

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def generate_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(username, email, password):
    existing = query_db(
        "SELECT id FROM users WHERE email=%s OR username=%s", (email, username), one=True
    )
    if existing:
        return None, "User already exists"
    hashed = hash_password(password)
    execute_db(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, hashed)
    )
    user = query_db("SELECT id FROM users WHERE email=%s", (email,), one=True)
    token = generate_token(user['id'], username)
    return token, None

def login_user(email, password):
    user = query_db(
        "SELECT id, username, password_hash FROM users WHERE email=%s", (email,), one=True
    )
    if not user:
        return None, "User not found"
    if not verify_password(password, user['password_hash']):
        return None, "Invalid credentials"
    token = generate_token(user['id'], user['username'])
    return token, None
