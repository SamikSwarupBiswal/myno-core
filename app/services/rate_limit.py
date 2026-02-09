import time
import hashlib

# seconds
RATE_LIMIT_WINDOW = 1

_last_reply_at = {}


def _hash_user(phone: str) -> str:
    return hashlib.sha256(phone.encode()).hexdigest()


def can_reply(phone: str) -> bool:
    user = _hash_user(phone)
    now = time.time()

    last = _last_reply_at.get(user)
    if last is None:
        return True

    return (now - last) >= RATE_LIMIT_WINDOW


def mark_replied(phone: str):
    user = _hash_user(phone)
    _last_reply_at[user] = time.time()
