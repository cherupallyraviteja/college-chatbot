import requests
from config import OLLAMA_URL_phi3, MODEL

def rewrite_query(query: str) -> str:
    """
    Uses Ollama to fix spelling mistakes
    Returns a rewritten query.
    """

    prompt = f"""
    You are a query spelling corrector.

    STRICT RULES:
    - Correct spelling
    - DO NOT add any new words
    - DO NOT expand abbreviations
    - DO NOT change meaning
    - Keep query as close to original as possible

    IMPORTANT 
    - DO NOT add any new words
    Return ONLY the corrected query.

    Query:
    {query}

    Rewritten query:
    """

    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0}
    }

    try:
        r = requests.post(f"{OLLAMA_URL_phi3}/api/generate", json=body, timeout=60)
        result = r.json()["response"].strip()
        result = str(result)
        print("Rewritten query:", result)
        return result

    except Exception as e:
        print("Rewrite error:", e)
        return query

if __name__ == "__main__":
    while True:        
        query=input("Enter your query: ")
        rewritten_query = rewrite_query(query)
        print("Rewritten query:", rewritten_query)