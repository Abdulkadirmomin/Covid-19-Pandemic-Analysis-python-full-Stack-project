from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'covid.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/summary", methods=["GET"])
def summary():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT country,
                        SUM(confirmed) as confirmed,
                        SUM(deaths) as deaths,
                        SUM(recovered) as recovered
                    FROM covid
                    GROUP BY country
                    ORDER BY confirmed DESC
                """)
    rows = cur.fetchall()
    conn.close()
    result = [dict(r) for r in rows]
    return jsonify(result)

@app.route("/api/data", methods=["GET"])
def data():
    country = request.args.get('country')
    conn = get_db_connection()
    cur = conn.cursor()
    if country:
        cur.execute("""SELECT date, country, confirmed, deaths, recovered
                       FROM covid WHERE country = ? ORDER BY date""", (country,))
    else:
        cur.execute("""SELECT date, country, confirmed, deaths, recovered
                       FROM covid ORDER BY date LIMIT 100""")
    rows = cur.fetchall()
    conn.close()
    result = [dict(r) for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    # if DB does not exist, try to create it from sample CSV
    if not os.path.exists(DB_PATH):
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_covid_data.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            conn = sqlite3.connect(DB_PATH)
            df.to_sql('covid', conn, if_exists='replace', index=False)
            conn.close()
            print('Database created at', DB_PATH)
        else:
            print('No CSV found at', csv_path)
    app.run(host='0.0.0.0', port=5000, debug=True)
