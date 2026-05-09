import psycopg2
import bcrypt
from config import DB_CONFIG

def authenticate_student(roll_no: str, password: str) -> bool:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT password
        FROM students
        WHERE roll_no = %s
        """,
        (roll_no,)
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return False

    stored_hash = row[0]  
    boll=bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )
    print("bcrypt check result: ", boll)
    return boll
