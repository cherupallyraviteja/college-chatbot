import requests
from config import OLLAMA_URL

def generate_response(data_rows):
    """
    data_rows: list of dicts from DB
    """
    prompt = f"""
You are given structured data retrieved from a database.
Your task is to convert this data into a clear, user-friendly response.

Rules:
- Use ONLY the data provided.
- Do NOT add new information.
- Do NOT remove any data items.
- Do NOT infer facts that are not explicitly present.
- Preserve the meaning of all values exactly.
- Organize the information logically for readability.
- Use simple, clear language.

Data:
{data_rows}

Response:
"""

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"].strip()
