import os
import requests

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234")
LM_MODEL = os.getenv("LM_MODEL", "llama-3.2-3b-instruct")

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-beta")


def answer_question(question, context, provider="lm"):
    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.

CONTEXT:
{context}

QUESTION:
{question}
"""

    messages = [
        {"role": "user", "content": prompt}
    ]

    # -------------------------
    # LM STUDIO (LOCAL)
    # -------------------------
    if provider == "lm":

        url = f"{LM_STUDIO_URL}/v1/chat/completions"

        payload = {
            "model": LM_MODEL,
            "messages": messages,
            "temperature": 0.3
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    # -------------------------
    # GROK (CLOUD)
    # -------------------------
    else:

        url = "https://api.x.ai/v1/chat/completions"

        payload = {
            "model": GROK_MODEL,
            "messages": messages,
            "temperature": 0.3
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROK_API_KEY}"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]