"""prompt_builder.py

Utility functions for constructing prompts sent to the OpenAI LLM.

This module provides professional AI prompt templates for multiple analytics
use cases: monthly summaries, recommendations, risk analysis, forecasting,
and question answering.
"""

import os
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Core system prompt – shared by all interactions
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are FinSight AI, a professional financial intelligence assistant. "
    "Provide clear, data-driven insights using only the user's financial context. "
    "Use professional language, avoid generic advice, and keep recommendations practical."
)


def _format_currency(value: Any) -> str:
    """Format a numeric value as USD currency, with safe fallback."""
    try:
        amount = float(value)
        return f"${amount:,.2f}"
    except Exception:
        return str(value)


def _context_excerpt(context: Dict[str, Any]) -> str:
    excerpt = []
    if "total_income" in context:
        excerpt.append(f"income: {_format_currency(context['total_income'])}")
    if "total_expense" in context:
        excerpt.append(f"expense: {_format_currency(context['total_expense'])}")
    if "savings" in context:
        excerpt.append(f"savings: {_format_currency(context['savings'])}")
    if "risk_level" in context:
        excerpt.append(f"risk level: {context['risk_level']}")
    return "; ".join(excerpt) or "no financial context provided"


def summary_prompt(context: Dict[str, Any]) -> str:
    month = context.get("month", "the latest period")
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Create a professional monthly financial summary for {month}. "
        f"Include total income, total expense, savings, and any notable category trends. "
        "Use only the provided financial context and keep the response factual and concise."
    )


def recommendations_prompt(context: Dict[str, Any]) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        "Review the user's spending behavior and provide personalized savings recommendations. "
        "Focus on practical steps the user can take to improve cash flow and reduce unnecessary costs. "
        "Avoid generic statements and use only the provided context."
    )


def risk_analysis_prompt(context: Dict[str, Any]) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        "Analyze the user's financial risk profile and highlight any unusual spending patterns. "
        "Explain risks clearly, identify potential concerns, and make the explanation actionable. "
        "Use only the provided context; do not invent data."
    )


def forecast_prompt(context: Dict[str, Any]) -> str:
    return (
        f"{SYSTEM_PROMPT}\n\n"
        "Predict the user's financial outlook for the near future based on current income and expense behavior. "
        "Describe likely spending trends, savings expectations, and any areas to watch. "
        "Keep the forecast rooted in the provided financial context only."
    )


def question_prompt(user_question: str, context: Dict[str, Any]) -> str:
    excerpt = _context_excerpt(context)
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"User question: {user_question}\n"
        f"Financial context: {excerpt}\n"
        "Answer this question precisely and professionally. Use the provided context only."
    )

__all__ = [
    "summary_prompt",
    "recommendations_prompt",
    "risk_analysis_prompt",
    "forecast_prompt",
    "question_prompt",
]
