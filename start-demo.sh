#!/bin/bash
set -e

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "WARNING: .env file not found. Using default values."
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "WARNING: Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Install dependencies
pip install -r requirements.txt

# Run database seed script
python3 scripts/seed_db.py

# Start Flask application
python3 app.py
