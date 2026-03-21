from response_generator import generate_response
from sql_generator import generate_sql
from safety import validate_and_clean_sql
from sql_executor import execute_sql
from table_router import route_tables
from sql_prompt import build_sql_prompt
from auth import authenticate_student
from query_rewriter import rewrite_query
import re


def extract_roll_no(text: str):
    """"
    Extracts roll number like: 237Z1A6626, 20A31A05XX etc.
    """
    pattern = r"\b(2[0-9]|[3-9][0-9])7[zZ][A-Za-z0-9]{2}[0-9]{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def print_result(row_dict):
    print("Bot:- ",end="")
    for key, value in row_dict.items():
        if key == "password":
            continue  # skip password field
        print(f"{key} : {value}")

print("Welcome to NNRG AIML Chatbot")
print("Use 'Exit' to quit the chatbot \n")

while True:
    query = input("You:- ")
    if query.lower() == "exit":
        break
    user_query = query#rewrite_query(query).lower()
    tables = route_tables(user_query)
    if not tables:
        print("Bot:- Cannot determine relevant data source.")
        continue
    roll_no = None

    if "students" in tables:
        roll_no = extract_roll_no(user_query)

        if not roll_no:
            roll_no = input("   Enter roll number: ")
            user_query += f" for roll number {roll_no}"
        password = input("   Enter password (Use Capitals): ")

        if not authenticate_student(roll_no, password):
            print("Bot: Authentication failed.")
            continue

    prompt = build_sql_prompt(user_query, tables)
    raw_sql = generate_sql(prompt)

    is_valid, sql = validate_and_clean_sql(raw_sql)

    if not is_valid:
        print("Bot:- Cannot answer this question with available data.")
        continue

    try:
        cols, rows = execute_sql(sql)
        result = ""
        for row in rows:
            row_dict = dict(zip(cols, row))
           
            for key, value in row_dict.items():
                if key != "password":
                    result += f"{key}: {value}\n"
    except Exception as e:
        print("Bot:- Query execution failed due to ", str(e))

    print("Bot:- ", result.strip())
    print("Rewritten Query: ", user_query)
    print("Generated SQL: \n", sql)
    print("------------------------------")