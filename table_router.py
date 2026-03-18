import requests
""""
OLLAMA_URL = "http://localhost:11434/api/generate"
ROUTER_MODEL = "phi3:mini"

ALLOWED_TABLES = {
    "students",
    "faculty",
    "fee_details",
    "admission_process",
    "admission_documents",
    "transport_details",
    "route_pickup_points",
    "placements",
}

def route_tables(user_query: str) -> list[str]:
    prompt = f""
You are a table selection system.

Given a user question, select all database tables required
to answer the question.

Rules:
- Choose ONLY from the allowed tables
- Output ONLY table names, one per line
- Do NOT explain anything
- If no table applies, output NONE

Allowed tables:
- students
- faculty
- fee_details
- admission_process
- admission_documents
- transport_details
- route_pickup_points
- placements

User question:
{user_query}

Tables:
""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": ROUTER_MODEL,
            "prompt": prompt,
            "stream": False
        }
    ).json()["response"]

    tables = [
        line.strip()
        for line in response.splitlines()
        if line.strip() in ALLOWED_TABLES
    ]

    return tables

"""
TABLE_KEYWORDS = {
    "faculty": ["faculty", "hod", "professor", "teacher"],
    "students": ["student", "roll", "attendance", "marks", "cgpa","fee status"],
    "fee_details": ["fee", "fees", "payment"],
    "placements": ["placement", "package", "company"],
    "transport_details": ["transport", "bus", "driver", "route", "bus number"],
    "route_pickup_points": ["pickup", "stop", "bus stop","bus timings", "pickup time"],
    "admission_programs": ["admission program", "degree program", "intake"],
    "admission_process": ["admission process", "admission steps", "how to apply"],
    "placements": ["placement", "package", "company","placed"],
    "admission_documents" : ["admission documents", "required documents", "documents needed","documents list","documents required"],
}

def select_tables(user_query: str):
    q = user_query.lower()
    selected = []

    for table, keys in TABLE_KEYWORDS.items():
        if any(k in q for k in keys):
            selected.append(table)

    return selected
