from entity_extractor import extract_entities
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


def generate_result(user_query):
    tables = route_tables(user_query)
    if not tables:
        return "Cannot determine relevant data source.", None
    entities = extract_entities(user_query)

    # ---- FORCE LOGIC FOR NAME ----
    if "name" in entities and tables:
        name = entities["name"]
        table = tables[0]

        sql = f"""
        SELECT *
        FROM {table}
        WHERE REPLACE(name, '.', '') % '{name}'
        ORDER BY similarity(REPLACE(name, '.', ''), '{name}') DESC;
        """
        user_query = rewrite_query(user_query)

    else:
        user_query = user_query.lower()
        prompt = build_sql_prompt(user_query, tables)
        print("Generated Prompt: \n", prompt)
        raw_sql = generate_sql(prompt)

        is_valid, sql = validate_and_clean_sql(raw_sql)
        if not is_valid:
            return "Cannot answer this question with available data.", sql
    result = ""
    try:
        result = execute_sql(sql)
    except Exception as e:
        print(f"Error executing SQL: {str(e)}")
        return f"Sorry, I need more information to answer that.", sql
 
    return result, sql

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            break
        result, sql = generate_result(query)
        print("Bot:- ", result)
        print("Generated SQL: \n", sql)
        print("------------------------------")