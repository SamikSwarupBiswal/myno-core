import hashlib
from collections import deque

# Max messages to keep per user
MAX_TURNS = 6

# In-memory conversation store
# { user_hash: deque([...]) }
_CONVERSATIONS = {}


def _hash_user(phone: str) -> str:
    return hashlib.sha256(phone.encode()).hexdigest()


def get_conversation(phone: str):
    """Read-only access to recent conversation"""
    user = _hash_user(phone)
    return list(_CONVERSATIONS.get(user, []))


def append_user_message(phone: str, text: str):
    """Append a user message AFTER Myno decides to reply"""
    user = _hash_user(phone)

    if user not in _CONVERSATIONS:
        _CONVERSATIONS[user] = deque(maxlen=MAX_TURNS)

    _CONVERSATIONS[user].append({
        "role": "user",
        "content": text
    })


def append_myno_message(phone: str, text: str):
    """Append Myno reply AFTER sending"""
    user = _hash_user(phone)

    if user not in _CONVERSATIONS:
        _CONVERSATIONS[user] = deque(maxlen=MAX_TURNS)

    _CONVERSATIONS[user].append({
        "role": "assistant",
        "content": text
    })
