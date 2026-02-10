import time
from typing import Tuple
from app.core.config import FRAGMENT_GUARD_TIMEOUT

FRAGMENTS = {
    "to", "about", "for", "with", "on", "and", "but", "so"
}

OVERRIDES = {
    "go on", "that's it", "done", "ok", "okay"
}

# sender -> first time we noticed a fragment block
_FRAGMENT_BLOCK_TS = {}

def _last_token(text: str) -> str:
    parts = text.strip().lower().split()
    return parts[-1] if parts else ""

def _has_override(text: str) -> bool:
    t = text.strip().lower()
    return any(t.endswith(o) or t == o for o in OVERRIDES)

def _is_fragment(text: str) -> bool:
    return _last_token(text) in FRAGMENTS

def should_reply_now(sender: str, combined_text: str) -> Tuple[bool, bool]:
    """
    Returns (allow_reply, ask_clarification)

    - allow_reply=True, ask_clarification=False  -> proceed to LLM
    - allow_reply=False, ask_clarification=False -> wait
    - allow_reply=True, ask_clarification=True   -> send ONE clarification
    """
    now = time.time()

    # Explicit override always wins
    if _has_override(combined_text):
        _FRAGMENT_BLOCK_TS.pop(sender, None)
        return True, False

    # No fragment -> safe to reply
    if not _is_fragment(combined_text):
        _FRAGMENT_BLOCK_TS.pop(sender, None)
        return True, False

    # Fragment present -> apply guard timeout
    first_seen = _FRAGMENT_BLOCK_TS.get(sender)
    if first_seen is None:
        _FRAGMENT_BLOCK_TS[sender] = now
        return False, False

    if now - first_seen >= FRAGMENT_GUARD_TIMEOUT:
        _FRAGMENT_BLOCK_TS.pop(sender, None)
        return True, True  # clarification

    return False, False
