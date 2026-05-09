from flask import Flask, request, jsonify, session
from entity_extractor import extract_entities
from main import generate_result
from sql_generator import generate_sql
from safety import validate_and_clean_sql
from sql_executor import execute_sql
from table_router import route_tables
from sql_prompt import build_sql_prompt
from auth import authenticate_student
from query_rewriter import rewrite_query
import re
from flask_cors import CORS  
app = Flask(__name__)
CORS(app)

user_sessions = {}
STATE_IDLE = "idle"
STATE_AWAITING_ROLL = "awaiting_roll"
STATE_AWAITING_PASSWORD = "awaiting_password"

def extract_roll_no(text: str):
    """"
    Extracts roll number like: 237Z1A6626, 20A31A05XX etc.
    """
    pattern = r"\b(2[0-9]|[3-9][0-9])7[zZ][A-Za-z0-9]{2}[0-9]{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def print_result(row_dict):
    result = ""
    print("Bot:- ",end="")
    for key, value in row_dict.items():
        if key == "password":
            continue  # skip password field
        result += f"{key} : {value}\n"

def requires_auth(query: str) -> bool:
    q = query.lower()

    personal_keywords = ["my", "mine", "me"]
    sensitive_fields = ["attendance", "cgpa", "fee"]

    # must contain BOTH:
    # 1. personal reference
    # 2. sensitive field
    return any(p in q for p in personal_keywords) and any(f in q for f in sensitive_fields)


def handle_conversation(session, user_text):
    # ---------------- STATE: AWAITING ROLL ----------------
    if session["state"] == STATE_AWAITING_ROLL:
        session["roll_no"] = user_text.strip()
        session["state"] = STATE_AWAITING_PASSWORD
        return "Enter password", session, False

    # ---------------- STATE: AWAITING PASSWORD ----------------
    if session["state"] == STATE_AWAITING_PASSWORD:
        roll_no = session["roll_no"]
        password = user_text.strip()

        if not authenticate_student(roll_no, password):
            return "Authentication failed.", {
                "state": STATE_IDLE,
                "original_query": None,
                "roll_no": None
            }, False

        # success → resume query
        query = session["original_query"]

        return query, {
            "state": STATE_IDLE,
            "original_query": None,
            "roll_no": roll_no
        }, True   # proceed to SQL

    # ---------------- STATE: IDLE ----------------
    if requires_auth(user_text):
        session["state"] = STATE_AWAITING_ROLL
        session["original_query"] = user_text
        return "Enter roll number", session, False

    # normal query
    return user_text, session, True

@app.route('/get-response', methods=['GET','POST'])
def get_response():
    try:
        user_text = request.json.get('text')

        # ---- SESSION ----
        session_id = request.remote_addr
        session = user_sessions.get(session_id, {
            "state": STATE_IDLE,
            "original_query": None,
            "roll_no": None
        })

        # ---- FSM ----
        result, session, proceed = handle_conversation(session, user_text)
        user_sessions[session_id] = session

        if not proceed:
            return jsonify({"response": result})
        
        # ---- USE FSM RESULT ----
        user_query=result #rewrite_query(query).lower()

        response, sql = generate_result(user_query)

        roll_no = session.get("roll_no")
        if roll_no :#and "students" in tables:
            print("User is authenticated. Generating SQL for students table.")
            # detect what column is needed
            if "attendance" in user_query:
                sql = f"SELECT attendance FROM students WHERE roll_no = '{roll_no}';"
            elif "cgpa" in user_query:
                sql = f"SELECT cgpa FROM students WHERE roll_no = '{roll_no}';"
            elif "fee" in user_query:
                sql = f"SELECT fee_status FROM students WHERE roll_no = '{roll_no}';"
            else:
                sql = f"SELECT * FROM students WHERE roll_no = '{roll_no}';"
            response = execute_sql(sql)
        
        user_sessions[session_id] = {
            "state": STATE_IDLE,
            "original_query": None,
            "roll_no": None
        }
        
        print("Generated SQL:", sql)
        if not response.strip():
            result = "No data found. Please provide more specific query"
        else:
            result=response
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"response": f"Server error: {str(e)}"})
    
    
if __name__ == '__main__':
    app.run(debug=True)
