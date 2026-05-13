# FinSight AI - Feature Roadmap

## Version 1 Core Features

The primary objective of v1 is to establish a working baseline for data ingestion, analytics, and basic AI-powered conversational insights.

- **CSV Upload System**
  - Users can upload their financial data in CSV format.
  - Basic mapping of columns to system fields.
- **Financial Data Storage**
  - Robust relational schema to securely store uploaded data.
- **Dashboard Analytics**
  - High-level overview of income vs. expenses.
  - Key metrics visualization.
- **AI Financial Chat**
  - A chat interface powered by an LLM (OpenAI via LangChain) to query personal data naturally.
- **Spending Insights**
  - Automatic categorization and highlighting of major spending areas.
- **Expense Summaries**
  - Monthly and weekly summaries generated via basic aggregations.
- **Basic Fraud Detection**
  - Rule-based or simple anomaly detection on transaction amounts.
- **Financial Forecasting**
  - Simple predictive trends on spending for the next month based on historical data.

## Future Upgrades (Post v1)

- **Ollama Local LLM Support:** For users who want complete privacy by running models locally.
- **Advanced Predictive Modeling:** More robust ML models for forecasting and credit risk scoring.
- **Multi-Bank Plaid Integration:** Live syncing of data instead of manual CSV uploads.
- **Custom Budgeting Alerts:** Proactive notifications when nearing budget limits.
