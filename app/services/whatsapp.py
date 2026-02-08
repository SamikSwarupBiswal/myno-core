import os
import requests

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

GRAPH_URL = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"


def send_message(to: str, text: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        GRAPH_URL,
        headers=headers,
        json=payload,
        timeout=3,
    )

    # 🔍 Observability only — NO raise
    print("OUTBOUND STATUS:", response.status_code)
    print("OUTBOUND RESPONSE:", response.text)

    return response
