import os
import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
LM_MODEL = os.getenv("LM_MODEL")

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-beta")


def summarize_text(text: str, provider="lm") -> str:

    messages = [
        {
            "role": "system",
            "content": "Summarize the transcript in 5 bullet points. Keep the response under 150 words."
        },
        {
            "role": "user",
            "content": text[:8000]
        }
    ]

    try:

        # -------------------------
        # LM STUDIO
        # -------------------------
        if provider == "lm":

            payload = {
                "model": LM_MODEL,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 200
            }

            response = requests.post(
                LM_STUDIO_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                },
                timeout=300
            )

        # -------------------------
        # GROK
        # -------------------------
        else:

            payload = {
                "model": GROK_MODEL,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 200
            }

            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {GROK_API_KEY}"
                },
                timeout=300
            )

        response.raise_for_status()

        data = response.json()

        if "choices" not in data:
            return f"Unexpected response: {data}"

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Request failed: {e}"