# Smart Skill Gap Analyzer & Learning Recommendation System

A full-stack web application that uses AI/NLP to analyze your skills against job roles and provides personalized learning paths.

## Tech Stack
- **Frontend**: React (Vite), Lucide Icons, Recharts, Vanilla CSS
- **Backend**: Python Flask, spaCy (NLP), Scikit-Learn
- **Database**: PostgreSQL

## Setup Instructions

### 1. Database Setup
- Install PostgreSQL and create a database named `postgres` (or as configured).
- Run the schema script:
  ```bash
  psql -U postgres -d postgres -f database/schema.sql
  ```

### 2. Backend Setup
- Navigate to the `backend` directory.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Download the spaCy model:
  ```bash
  python -m spacy download en_core_web_md
  ```
- Start the Flask server:
  ```bash
  python -m flask run --port 5000
  ```

### 3. Frontend Setup
- Navigate to the `frontend` directory.
- Install dependencies:
  ```bash
  npm install
  ```
- Start the development server:
  ```bash
  npm run dev
  ```
- Open `http://localhost:3000` in your browser.

## Features
- **Skill Extraction**: Paste your bio or resume text to automatically extract skills using NLP.
- **Gap Analysis**: Compare your skills against target roles (Full Stack, Data Scientist, etc.).
- **Dashboard**: Visualize your match percentage and identify missing skills.
- **Learning Path**: Get direct links to courses and resources for your skill gaps.
- **AI Career Mentor**: Chat with an AI assistant for career guidance.
