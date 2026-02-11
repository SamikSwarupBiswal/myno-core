import os
from dotenv import load_dotenv

load_dotenv()

META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

# Phase 2.0 — debounce window (seconds)
DEBOUNCE_SECONDS = int(os.getenv("MYNO_DEBOUNCE_SECONDS", "3"))

# Phase 2.1 — fragment guard patience (seconds)
FRAGMENT_GUARD_TIMEOUT = int(os.getenv("MYNO_FRAGMENT_GUARD_TIMEOUT", "9"))

# Phase 2.2 — output rate limiting (seconds)
OUTPUT_RATE_LIMIT_SECONDS = int(os.getenv("MYNO_OUTPUT_RATE_LIMIT_SECONDS", "5"))
