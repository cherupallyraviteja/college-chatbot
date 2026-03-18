import pandas as pd
import psycopg2
import bcrypt

# ---------- CONFIG ----------
EXCEL_FILE = "students_data.xlsx"
SHEET_NAME = "Sheet1"


DB_CONFIG = {
    "dbname": "College_database",
    "user": "postgres",
    "password": "Gmail.com#1",
    "host": "localhost",
    "port": "5432"
}


# ---------- PASSWORD HASH FUNCTION ----------
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

# ---------- READ EXCEL ----------
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

print("Before normalization:", df.columns.tolist())

df.columns = (
    df.columns
      .astype(str)
      .str.strip()
      .str.lower()
      .str.replace(r"\s+", "_", regex=True)
)

print("After normalization:", df.columns.tolist())

# ---------- DB CONNECTION ----------
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

insert_query = """
INSERT INTO students(roll_no, name, year, semester, department, cgpa, fee_status, password, attendance)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (roll_no) DO NOTHING;
"""

# ---------- INSERT DATA ----------
for _, row in df.iterrows():
    hashed_pwd = hash_password(row["password"])

    cursor.execute(
        insert_query,
        (
            row["roll_no"],
            row["student_names"],
            row["year"],
            row["semester"],
            row["department"],
            row["cgpa"],
            row["fee_status"],
            hashed_pwd,
            row["attendance"]
        )

    )

conn.commit()
cursor.close()
conn.close()

print("Data inserted with hashed passwords.")
