@echo off
setlocal

echo Loading environment variables from .env...
if exist .env (
    for /F "tokens=*" %%A in (.env) do set %%A
) else (
    echo WARNING: .env file not found. Using default values.
)

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found. Please run: python -m venv venv
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo Running database seed script...
python scripts\seed_db.py
if errorlevel 1 (
    echo Error seeding database
    exit /b 1
)

echo Starting Flask application...
python app.py