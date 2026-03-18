from response_generator import generate_response
from sql_generator import generate_sql
from safety import validate_and_clean_sql
from sql_executor import execute_sql
from table_router import select_tables,route_tables
from sql_prompt import build_sql_prompt
from auth import authenticate_student
from query_rewriter import rewrite_query
import re
from requests import request, post
def extract_roll_no(text: str):
    """"
    Extracts roll number like: 237Z1A6626, 20A31A05XX etc.
    """
    pattern = r"\b(2[0-9]|[3-9][0-9])7Z[A-Za-z0-9]{2}\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def print_result(row_dict):
    for key, value in row_dict.items():
        print(f"Bot:- {key} : {value}")



print("Welcome to NNRG Chatbot \n")
print("Use 'Exit' to quit the chatbot \n")

while True:
    query = input("You:- ")
    if query.lower() == "exit":
        break
    user_query = rewrite_query(query)
    tables = select_tables(user_query)
    
    if not tables:
        print("Bot:- Cannot determine relevant data source.")
        continue
    roll_no = None

    if "students" in tables:
        roll_no = extract_roll_no(user_query)

        if not roll_no:
            roll_no = input("   Enter roll number: ")
            user_query += f" for roll number {roll_no}"
        password = input("  Enter password (Use Capitals): ")

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
        for row in rows:
            row_dict = dict(zip(cols, row))
            print_result(row_dict)
        print(rows)
    except Exception as e:
        print("Bot:- Query execution failed due to ", str(e))

    print("Generated SQL: \n", sql)
    print("------------------------------\n")

"""
import re
from response_generator import generate_response
from sql_generator import generate_sql
from safety import validate_and_clean_sql
from sql_executor import execute_sql
from table_router import select_tables
from sql_prompt import build_sql_prompt
from auth import authenticate_student
from meta_whatsapp import send_whatsapp_message


# In-memory session store (per WhatsApp number)
SESSION = {}


def extract_roll_no(text: str):
    pattern = r"\b(2[0-9]|[3-9][0-9])7Z[A-Za-z0-9]{2}\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def run_chatbot_pipeline(user_query: str, user_id: str) -> str:
    session = SESSION.setdefault(user_id, {})

    tables = select_tables(user_query)
    if not tables:
        return "Cannot determine relevant data source."

    # ---------- STUDENT AUTH FLOW ----------
    if "students" in tables:

        if "roll_no" not in session:
            roll_no = extract_roll_no(user_query)
            if not roll_no:
                return "Please send your roll number."
            session["roll_no"] = roll_no
            return "Please send your password."

        if not session.get("authenticated"):
            password = user_query.strip()
            if not authenticate_student(session["roll_no"], password):
                session.clear()
                return "Authentication failed. Please try again."
            session["authenticated"] = True
            return "Authentication successful. Please ask your question again."

    # ---------- SQL GENERATION ----------
    prompt = build_sql_prompt(user_query, tables)
    raw_sql = generate_sql(prompt)

    is_valid, sql = validate_and_clean_sql(raw_sql)
    if not is_valid:
        return "Cannot answer this question with available data."

    try:
        cols, rows = execute_sql(sql)
        if not rows:
            return "No data found."

        data = [dict(zip(cols, row)) for row in rows]
        return generate_response(data)

    except Exception:
        return "Query execution failed."


# ---------- META WHATSAPP WEBHOOK HANDLER ----------
def handle_whatsapp_message(message_payload: dict):
    message = message_payload["messages"][0]
    user_text = message["text"]["body"]
    from_number = message["from"]

    reply = run_chatbot_pipeline(user_text, from_number)
    send_whatsapp_message(from_number, reply)
"""