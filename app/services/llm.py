import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

MAX_WHATSAPP_CHARS = 3500  # safe margin under 4096


class LLMError(Exception):
    pass


def generate_reply(user_text: str) -> str:
    if not GEMINI_API_KEY:
        raise LLMError("GEMINI_API_KEY is not set")

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are a WhatsApp assistant. "
                            "Keep responses clear, concise, and under 3000 characters.\n\n"
                            f"User: {user_text}"
                        )
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            GEMINI_ENDPOINT,
            params={"key": GEMINI_API_KEY},
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=20,
        )
    except requests.RequestException as e:
        print("LLM NETWORK ERROR:", repr(e))
        raise LLMError("Network error calling Gemini")

    if response.status_code != 200:
        print("LLM HTTP ERROR:", response.status_code, response.text)
        raise LLMError("Gemini HTTP failure")

    try:
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        text = text.strip()

        # 🔒 HARD CAP PROTECTION
        if len(text) > MAX_WHATSAPP_CHARS:
            text = text[:MAX_WHATSAPP_CHARS] + "\n\n(Reply truncated for length.)"

        return text

    except Exception as e:
        print("LLM PARSE ERROR:", repr(e))
        print("RAW:", response.text)
        raise LLMError("Malformed Gemini response")
