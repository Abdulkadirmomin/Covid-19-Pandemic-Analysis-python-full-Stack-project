COVID-19 Analysis - Backend (Flask)
----------------------------------
Requirements:
  - Python 3.8+
  - pip install -r requirements.txt

Quick start:
  cd backend
  pip install -r requirements.txt
  python init_db.py   # creates covid.db from sample CSV
  python app.py       # starts the Flask API on port 5000

Endpoints:
  GET /api/summary        -> JSON summary grouped by country
  GET /api/data           -> JSON rows; optional ?country=India to filter

Notes:
  - This project ships with a tiny sample CSV in backend/data.
  - For real analysis, replace the CSV with a larger dataset (e.g., Johns Hopkins CSSE).
