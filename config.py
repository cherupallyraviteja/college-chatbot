import os


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_URL_phi3 = 'http://localhost:11434'
LLM_MODEL = "anindya/prem1b-sql-ollama-fp116"
MODEL = "phi3:mini"

DB_CONFIG = {
    "dbname": "College_database",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": 5432
}

EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3
