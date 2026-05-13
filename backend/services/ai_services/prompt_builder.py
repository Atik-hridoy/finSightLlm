"""prompt_builder.py

Utility functions for constructing the various prompts sent to the OpenAI LLM.

All prompts are simple f‑strings as per the project decision.
The module provides:
* ``system_prompt`` – the base system instruction for the assistant.
* ``summary_prompt`` – builds a prompt to ask the model for a monthly financial summary.
* ``insight_prompt`` – builds a prompt to generate actionable insights from a context dict.
* ``question_prompt`` – builds a prompt to answer a free‑form user question using the enriched financial context.
"""

import os
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Core system prompt – shared by all interactions
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are **FinSight AI**, a professional financial intelligence assistant. "
    "Provide clear, data‑driven insights based on the user's financial information. "
    "Always be concise, use bullet points when appropriate, and respond in JSON when asked."
)


def _format_currency(value: Any) -> str:
    """Return a nicely formatted currency string.
    The function is defensive – if ``value`` cannot be interpreted as a number it simply
    returns the original representation.
    """
    try:
        amount = float(value)
        return f"${amount:,.2f}"
    except Exception:
        return str(value)


def summary_prompt(context: Dict[str, Any]) -> str:
    """Create a prompt that asks the model to generate a monthly summary.
    Expected keys in ``context``: ``month``, ``total_expense``, ``total_income``, ``top_categories``.
    """
    month = context.get("month", "the last month")
    total_expense = _format_currency(context.get("total_expense", 0))
    total_income = _format_currency(context.get("total_income", 0))
    top_cats = context.get("top_categories", [])
    cats_str = ", ".join([f"{cat}: {_format_currency(amt)}" for cat, amt in top_cats[:5]])
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Provide a concise financial summary for **{month}**. "
        f"Total expense: {total_expense}. Total income: {total_income}. "
        f"Top spending categories: {cats_str}. "
        "Give the summary in plain English (no JSON)."
    )


def insight_prompt(context: Dict[str, Any]) -> str:
    """Prompt the model to generate actionable insights.
    ``context`` may also contain ``savings_rate`` and ``anomalies``.
    """
    month = context.get("month", "the last month")
    savings_rate = context.get("savings_rate")
    anomalies = context.get("anomalies", [])
    anomalies_str = ", ".join(anomalies) if anomalies else "none"
    savings_str = f"{savings_rate:.2f}%" if isinstance(savings_rate, (int, float)) else "unknown"
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Based on the user's financial data for **{month}**, generate up to three actionable insights. "
        f"Include any detected anomalies (currently: {anomalies_str}) and the user's savings rate ({savings_str}). "
        "Return the insights as a JSON array under the key ``insights``."
    )


def question_prompt(user_question: str, context: Dict[str, Any]) -> str:
    """Create a prompt that answers a free‑form user question using the supplied context.
    ``context`` is a dict produced by ``financial_context``.
    """
    excerpt_items = []
    if "total_expense" in context:
        excerpt_items.append(f"total expense: {_format_currency(context['total_expense'])}")
    if "total_income" in context:
        excerpt_items.append(f"total income: {_format_currency(context['total_income'])}")
    if "top_categories" in context:
        top = ", ".join([cat for cat, _ in context["top_categories"][:3]])
        excerpt_items.append(f"top categories: {top}")
    excerpt = "; ".join(excerpt_items) or "no summary available"
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"User question: {user_question}\n"
        f"Financial context (excerpt): {excerpt}\n"
        "Answer the question concisely and in a user‑friendly manner. "
        "If the answer requires a numeric value, format it as a currency."
    )

__all__ = ["summary_prompt", "insight_prompt", "question_prompt"]
