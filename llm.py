import requests
from config import OLLAMA_URL, LLM_MODEL

def generate_answer(context, question):
    prompt = f"""
Answer ONLY from the context.
Be factual and short.

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()
