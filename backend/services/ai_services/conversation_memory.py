"""conversation_memory.py

A very lightweight in‑memory store that keeps the last N messages per user.
The store is deliberately simple because the MVP uses the in‑memory option
(as requested).  In a production setting you would replace this with a
Redis‑backed implementation.

Public API
-----------
* ``add_message(user_id: int, role: str, content: str)`` – append a new message.
* ``get_history(user_id: int, limit: int = 10)`` – retrieve the most recent
  messages (chronological order).
* ``clear_history(user_id: int)`` – wipe the stored history for a user.

The implementation stores a list of dicts ``{"role": ..., "content": ...}``
under a ``defaultdict(list)`` keyed by ``user_id``.
"""

from collections import defaultdict
from typing import List, Dict

# In‑memory store – key = user_id, value = list of message dicts.
_memory_store: Dict[int, List[Dict[str, str]]] = defaultdict(list)

# How many messages we keep per user (to stay within token limits).
MAX_MESSAGES = 10


def add_message(user_id: int, role: str, content: str) -> None:
    """Append a new message to the user's history.

    Parameters
    ----------
    user_id: int – ``request.user.id``
    role: str – ``"user"`` or ``"assistant"`` (mirrors OpenAI chat format)
    content: str – the raw message text
    """
    if role not in {"user", "assistant", "system"}:
        raise ValueError("role must be 'user', 'assistant', or 'system'")
    _list = memory_store[user_id]
    _list.append({"role": role, "content": content})
    # Trim old messages – keep the most recent MAX_MESSAGES.
    if len(_list) > MAX_MESSAGES:
        memory_store[user_id] = _list[-MAX_MESSAGES:]


def get_history(user_id: int, limit: int = MAX_MESSAGES) -> List[Dict[str, str]]:
    """Return the most recent *limit* messages for *user_id*.
    The list is ordered from oldest to newest (chronological) because the
    OpenAI API expects that order.
    """
    return memory_store[user_id][-limit:]


def clear_history(user_id: int) -> None:
    """Remove all stored messages for the given user."""
    memory_store.pop(user_id, None)

# End of conversation_memory.py
