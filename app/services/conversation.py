import time
from collections import defaultdict
from typing import List, Optional
from app.services.guard_timeout import cancel_guard_timeout


# sender -> { messages: [str], last_ts: float }
_CONVERSATIONS = defaultdict(lambda: {
    "messages": [],
    "last_ts": 0.0
})

def append_user_message(sender: str, text: str):
    cancel_guard_timeout(sender)  # NEW: user activity cancels clarification

    convo = _CONVERSATIONS[sender]
    convo["messages"].append(text)
    convo["last_ts"] = time.time()


def pop_if_stable(sender: str, debounce_seconds: int) -> Optional[List[str]]:
    convo = _CONVERSATIONS.get(sender)
    if not convo:
        return None

    now = time.time()
    if now - convo["last_ts"] >= debounce_seconds:
        messages = convo["messages"][:]
        _CONVERSATIONS.pop(sender, None)
        return messages

    return None
