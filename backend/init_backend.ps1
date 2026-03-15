# Backend Setup Script for Skill Gap Analyzer
Write-Host "Creating Virtual Environment..." -ForegroundColor Cyan
python -m venv venv

Write-Host "Activating Virtual Environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

Write-Host "Upgrading Base Tools..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing Requirements (this may take a few minutes)..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "Downloading spaCy NLP model..." -ForegroundColor Cyan
python -m spacy download en_core_web_md

Write-Host "Setup Complete! You can now run 'python app.py' inside the venv." -ForegroundColor Green
