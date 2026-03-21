from flask import Flask, request, jsonify
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


@app.route('/get-response', methods=['GET','POST'])
@app.route('/get-response', methods=['POST'])
def get_response():
    try:
        user_text = request.json.get('text')

        user_query = rewrite_query(user_text).lower()
        tables = route_tables(user_query)

        if not tables:
            return jsonify({"response": "Cannot determine relevant data source."})

        # 🚫 REMOVE input() completely
        roll_no = extract_roll_no(user_query)

        # (Optional) skip authentication for now
        # OR send roll/password from frontend later

        prompt = build_sql_prompt(user_query, tables)
        raw_sql = generate_sql(prompt)

        is_valid, sql = validate_and_clean_sql(raw_sql)

        if not is_valid:
            return jsonify({"response": "Invalid query generated."})

        cols, rows = execute_sql(sql)

        result = ""
        for row in rows:
            row_dict = dict(zip(cols, row))
            for key, value in row_dict.items():
                if key != "password":
                    result += f"{key}: {value}\n"

        if not result:
            result = "No data found."

        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"response": f"Server error: {str(e)}"})
    

if __name__ == '__main__':
    app.run(debug=True)
