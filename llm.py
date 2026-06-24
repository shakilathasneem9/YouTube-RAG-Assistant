import os
import requests

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
LM_MODEL = os.getenv("LM_MODEL")

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_MODEL = os.getenv("GROK_MODEL")


def call_llm(messages, provider="lm"):

    if provider == "lm":

        url = f"{LM_STUDIO_URL}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        payload = {
            "model": LM_MODEL,
            "messages": messages,
            "temperature": 0.3
        }

    else:  # grok

        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROK_API_KEY}"
        }

        payload = {
            "model": GROK_MODEL,
            "messages": messages,
            "temperature": 0.3
        }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]