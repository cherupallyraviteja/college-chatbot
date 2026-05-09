import psycopg2
from config import DB_CONFIG

def execute_sql(sql):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    result = ""
    for row in rows:
            row_dict = dict(zip(cols, row))
            for key, value in row_dict.items():
                if key != "password":
                    result += f"{key}: {value}\n"
    return result

if __name__ == "__main__":
    sql = "SELECT * FROM admission_process WHERE program = 'Btech CSE' AND description LIKE '%admission%';"
    print(execute_sql(sql))