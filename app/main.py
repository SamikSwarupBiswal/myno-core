from app.services.conversation import (
    get_conversation,
    append_user_message,
    append_myno_message
)

from dotenv import load_dotenv
load_dotenv()

import json
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.core.security import verify_meta_signature
from app.core.config import META_VERIFY_TOKEN
from app.services.whatsapp import send_message
import os

app = FastAPI()

# 🔒 Phase 1.1 — in-memory deduplication
SEEN_MESSAGE_IDS = set()


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.body()

    # 🔐 Signature check (bypassed only in test mode)
    if os.getenv("MYNO_TEST_MODE") != "true":
        try:
            verify_meta_signature(request, body)
        except Exception:
            return PlainTextResponse("Unauthorized", status_code=401)

    # 🔒 Parse payload safely
    try:
        data = json.loads(body)
        entry = data.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        value = change.get("value", {})
    except Exception:
        return {"status": "ignored_malformed"}

    # 🔕 Ignore non-message events
    messages = value.get("messages")
    if not isinstance(messages, list) or not messages:
        return {"status": "ignored_non_message"}

    message = messages[0]

    message_id = message.get("id")
    sender = message.get("from")
    text = message.get("text", {}).get("body", "")
    msg_type = message.get("type")

    if not message_id or not sender:
        return {"status": "ignored_invalid_message"}

    if msg_type != "text":
        return {"status": "ignored_non_text"}

    # 🔒 Deduplication
    if message_id in SEEN_MESSAGE_IDS:
        return {"status": "duplicate_ignored"}

    SEEN_MESSAGE_IDS.add(message_id)

    reply_text = "Signal Received"

    # 🚀 Send reply
    try:
        send_message(sender, reply_text)
    except Exception as e:
        print("SEND FAILED:", e)

    # 🧠 Update conversation state
    append_user_message(sender, text)
    append_myno_message(sender, reply_text)

    return {"status": "ok"}
