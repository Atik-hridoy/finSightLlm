from services.ai_services.insight_generator import ask_financial_ai


def generate_summary(user):
    question = (
        "Generate a professional monthly financial summary for this user's financial activity. "
        "Use the provided financial context only, keep the language professional, and focus on the latest trends."
    )
    return ask_financial_ai(user, question)


def generate_recommendations(user):
    question = (
        "Analyze the user's spending behavior and provide personalized savings recommendations. "
        "Use the provided financial context only, and make the advice specific, practical, and actionable."
    )
    return ask_financial_ai(user, question)


def generate_risk_analysis(user):
    question = (
        "Analyze the user's financial risks, unusual spending patterns, and potential concerns. "
        "Explain risk clearly and professionally using only the provided financial context."
    )
    return ask_financial_ai(user, question)


def generate_forecast(user):
    question = (
        "Predict future financial trends based on the user's current income and expense behavior. "
        "Use only the provided financial context, and describe the likely outlook for the next month."
    )
    return ask_financial_ai(user, question)
