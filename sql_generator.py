import requests
from config import OLLAMA_URL, LLM_MODEL

def generate_sql(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()
