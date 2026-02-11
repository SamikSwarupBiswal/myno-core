import time
from typing import Tuple
from app.core.config import FRAGMENT_GUARD_TIMEOUT


def normalize_edge_spacing(text: str) -> str:
    """
    Allow at most one extra space on each edge.
    Internal spacing is preserved.
    """
    return text.strip()


PHRASE_FRAGMENTS = {
    "tell me about",
    "explain",
    "explain about",
    "i want to know",
    "i want to know about",
    "help me with",
    "help me",
    "can you explain",
    "can you tell me",
    "what is",
    "what are",
    "how does",
    "how do",
    "why does",
    "why do",
    "give me",
    "give me information",
    "information about",
}

TERMINAL_CONNECTORS = {
    "about",
    "to",
    "for",
    "with",
    "on",
}

OVERRIDES = {
    "go on",
    "that's it",
    "done",
    "continue",
    "continue please",
    "you can continue",
    "finish",
    "complete it",
    "proceed",
    "yes go on",
    "okay continue",
    "ok continue",
}

# sender -> first time we noticed a fragment block
_FRAGMENT_BLOCK_TS = {}


def _has_override(text: str) -> bool:
    t = normalize_edge_spacing(text.lower())
    return any(t == o or t.endswith(o) for o in OVERRIDES)


def is_fragment(text: str) -> bool:
    text = normalize_edge_spacing(text.lower())

    # 1️⃣ Phrase-level fragments
    if text in PHRASE_FRAGMENTS:
        return True

    words = text.split()

    # 2️⃣ Terminal connector fragments (only at end, only if >1 word)
    if len(words) > 1 and words[-1] in TERMINAL_CONNECTORS:
        return True

    return False


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
    if not is_fragment(combined_text):
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
