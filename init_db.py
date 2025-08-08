# Helper to initialize the SQLite DB from the sample CSV.
import pandas as pd
import sqlite3, os
here = os.path.dirname(__file__)
csv_path = os.path.join(here, 'data', 'sample_covid_data.csv')
db_path = os.path.join(here, 'covid.db')
df = pd.read_csv(csv_path)
conn = sqlite3.connect(db_path)
df.to_sql('covid', conn, if_exists='replace', index=False)
conn.close()
print('Initialized DB at', db_path)
