import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def generate_reply(user_text: str) -> str:
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_text}]
            }
        ]
    }

    params = {"key": GEMINI_API_KEY}
    headers = {"Content-Type": "application/json"}

    r = requests.post(
        GEMINI_ENDPOINT,
        params=params,
        headers=headers,
        json=payload,
        timeout=10,
    )

    if r.status_code != 200:
        return "I’m having trouble responding right now. Please try again."

    data = r.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return "I’m having trouble responding right now. Please try again."
