from app.services.conversation import append_user_message
from app.services.debounce import schedule
from app.core.config import DEBOUNCE_SECONDS
from app.routing.intent_closure import should_reply_now
from app.services.llm import generate_reply
from app.services.guard_timeout import schedule_guard_timeout


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

    if os.getenv("MYNO_TEST_MODE") != "true":
        try:
            verify_meta_signature(request, body)
        except Exception:
            return PlainTextResponse("Unauthorized", status_code=401)

    try:
        data = json.loads(body)
        entry = data.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        value = change.get("value", {})
    except Exception:
        return {"status": "ignored_malformed"}

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

    if message_id in SEEN_MESSAGE_IDS:
        return {"status": "duplicate_ignored"}

    SEEN_MESSAGE_IDS.add(message_id)

    append_user_message(sender, text)

    async def on_debounce_fire(sender: str, messages: list[str]):
        combined = "\n".join(messages)

        allow, clarify = should_reply_now(sender, combined)

        if not allow:
        # Fragment detected → schedule ONE clarification after patience window
            async def send_clarification(s: str):
                send_message(s, "What would you like to know about?")

            await schedule_guard_timeout(sender, send_clarification)
            return

        if clarify:
            send_message(sender, "What would you like to know about?")
            return

        reply = generate_reply(combined)
        send_message(sender, reply)

    await schedule(sender, on_debounce_fire)

    return {"status": "ok"}
