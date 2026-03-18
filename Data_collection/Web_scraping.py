import psycopg2
from bs4 import BeautifulSoup
import requests

DB_CONFIG = {
    "dbname": "College_database",
    "user": "postgres",
    "password": "Gmail.com#1",
    "host": "localhost",
    "port": "5432"
}
def yes_no_to_bool(val):
    return val.strip().upper() == "YES"

response = requests.get("https://nnrg.edu.in/admission-process.php")
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find("div", id="about").find_all("table")

doc_table = tables[-1]
rows = doc_table.find_all("tr")[1:]  

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

insert_query = """
INSERT INTO admission_documents
(document_name, ap_ts_students_required, national_students_required)
VALUES (%s, %s, %s)
"""

for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all("td")]
    if len(cols) < 4:
        continue

    doc_name = cols[1]
    ap_ts = yes_no_to_bool(cols[2])
    national = yes_no_to_bool(cols[3])

    cur.execute(insert_query, (doc_name, ap_ts, national))

conn.commit()
cur.close()
conn.close()


print("Admission documents inserted")
