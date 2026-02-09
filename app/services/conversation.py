import hashlib
from collections import deque

MAX_TURNS = 6
_CONVERSATIONS = {}


def _hash_user(phone: str) -> str:
    return hashlib.sha256(phone.encode()).hexdigest()


def get_conversation(phone: str):
    user = _hash_user(phone)
    return list(_CONVERSATIONS.get(user, []))


def append_user_message(phone: str, text: str):
    user = _hash_user(phone)
    if user not in _CONVERSATIONS:
        _CONVERSATIONS[user] = deque(maxlen=MAX_TURNS)
    _CONVERSATIONS[user].append({
        "role": "user",
        "content": text
    })


def append_myno_message(phone: str, text: str):
    user = _hash_user(phone)
    if user not in _CONVERSATIONS:
        _CONVERSATIONS[user] = deque(maxlen=MAX_TURNS)
    _CONVERSATIONS[user].append({
        "role": "assistant",
        "content": text
    })
