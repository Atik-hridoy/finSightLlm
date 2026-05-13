"""llm_client.py

Utility module that wraps the OpenAI ChatCompletion API.

Features
--------
* Reads configuration from environment variables via ``django-environ`` (or ``os.getenv`` fallback).
* Supports the ``gpt-4o`` model (default) with configurable temperature.
* Implements a simple exponential‑backoff retry strategy (max 3 attempts).
* Returns a tuple ``(response_text, usage_dict)`` where ``usage_dict`` contains ``prompt_tokens`` and ``completion_tokens``.
* Provides a safe fallback message when the API fails after all retries.
"""

import os
import time
import logging
from typing import Tuple, Dict, Any

import openai
from django.conf import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration (environment variables are loaded in ``settings.py``)
# ---------------------------------------------------------------------------
OPENAI_API_KEY = getattr(settings, "OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = getattr(settings, "OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o"))
OPENAI_TEMPERATURE = float(
    getattr(settings, "OPENAI_TEMPERATURE", os.getenv("OPENAI_TEMPERATURE", "0.7")))
MAX_RETRIES = 3
BASE_BACKOFF = 1  # seconds

# ---------------------------------------------------------------------------
# Helper – safe fallback response used when the LLM cannot be reached.  
# ---------------------------------------------------------------------------
SAFE_FALLBACK = (
    "We’re experiencing technical difficulties processing your request. "
    "Please try again later."
)


def _call_openai(messages: list) -> Tuple[str, Dict[str, Any]]:
    """Direct call to ``openai.ChatCompletion.create``.

    Parameters
    ----------
    messages: list
        A list of message dicts as required by the OpenAI API.

    Returns
    -------
    Tuple[str, dict]
        The assistant's content and the usage information returned by OpenAI.
    """
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=OPENAI_TEMPERATURE,
    )
    output = response["choices"][0]["message"]["content"].strip()
    usage = response.get("usage", {"prompt_tokens": 0, "completion_tokens": 0})
    return output, usage


def generate_response(messages: list) -> Tuple[str, Dict[str, Any]]:
    """Public API used by the AI services.

    Parameters
    ----------
    messages: list
        Chat messages supplied to the LLM (system + user + optional context).

    Returns
    -------
    Tuple[str, dict]
        The response text and a usage dictionary.
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key not configured.")
        return SAFE_FALLBACK, {"prompt_tokens": 0, "completion_tokens": 0}

    openai.api_key = OPENAI_API_KEY
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            logger.debug("Calling OpenAI (attempt %s)", attempt + 1)
            return _call_openai(messages)
        except Exception as exc:  # Broad catch – we only need a graceful fallback
            attempt += 1
            backoff = BASE_BACKOFF * (2 ** (attempt - 1))
            logger.warning(
                "OpenAI request failed (attempt %s/%s): %s – retrying in %s seconds",
                attempt,
                MAX_RETRIES,
                exc,
                backoff,
            )
            time.sleep(backoff)

    # All retries exhausted – return safe fallback
    logger.error("OpenAI request failed after %s attempts – returning fallback.", MAX_RETRIES)
    return SAFE_FALLBACK, {"prompt_tokens": 0, "completion_tokens": 0}

# End of llm_client.py
