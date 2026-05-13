import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Expected response structure from LLM
EXPECTED_KEYS = {"summary", "key_insights", "recommendations", "risk_level"}


def safe_json_load(text: str) -> Dict[str, Any]:
    """Attempt to parse a string into JSON.
    If parsing fails, return an empty dict and log the error.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"LLM response not valid JSON: {e}")
        return {}


def format_response(raw_text: str) -> Dict[str, Any]:
    """Take raw LLM output (string) and produce a validated response dict.

    The function extracts the required keys. Missing keys are filled with sensible defaults
    and a warning is logged. If the LLM output cannot be parsed, a fallback response is
    returned.
    """
    data = safe_json_load(raw_text)
    if not data:
        # Fallback safe response
        return {
            "summary": "Unable to generate a detailed answer at the moment.",
            "key_insights": [],
            "recommendations": [],
            "risk_level": "unknown",
        }

    missing = EXPECTED_KEYS - data.keys()
    if missing:
        logger.warning(f"LLM response missing keys: {missing}")
        # Fill missing with defaults
        for key in missing:
            if key == "summary":
                data[key] = "No summary provided."
            elif key in {"key_insights", "recommendations"}:
                data[key] = []
            elif key == "risk_level":
                data[key] = "unknown"
    # Ensure correct types
    data["key_insights"] = list(data.get("key_insights", []))
    data["recommendations"] = list(data.get("recommendations", []))
    data["risk_level"] = str(data.get("risk_level", "unknown"))
    data["summary"] = str(data.get("summary", ""))
    return data
