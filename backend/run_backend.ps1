# Script to run the backend within the venv
Write-Host "Starting Flask Backend on http://localhost:5000 ..." -ForegroundColor Cyan
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
.\venv\Scripts\python.exe app.py
