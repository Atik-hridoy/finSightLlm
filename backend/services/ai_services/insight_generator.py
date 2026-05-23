from typing import Any, Dict

from .financial_context import get_financial_context
from .prompt_builder import question_prompt
from .llm_client import generate_response
from .response_formatter import format_response


def ask_financial_ai(user: Any, question: str) -> Dict[str, Any]:
    """Generate a financial AI answer for the authenticated user.

    The response uses the user's financial context and returns both the
    generated answer and the context that was used to build the prompt.
    """
    context = get_financial_context(user)
    prompt = question_prompt(question, context)

    messages = [
        {
            "role": "system",
            "content": (
                "You are FinSight AI, a financial assistant. Use the provided user financial "
                "context to answer the question accurately and concisely. Do not hallucinate." 
            ),
        },
        {"role": "user", "content": prompt},
    ]

    raw_response, usage = generate_response(messages)
    structured = format_response(raw_response)

    return {
        "response": structured["summary"],
        "context": context,
        "usage": usage,
        "raw_response": raw_response,
        "structured": structured,
    }
