# FinSight AI - System Architecture

This document outlines the high-level system architecture for the FinSight AI platform.

## High-Level Architecture Flow

1. **Client Layer (Frontend)**
   - **Framework:** Flutter
   - **State Management:** GetX
   - **Responsibilities:** 
     - Presenting the dashboard and chat interfaces.
     - Handling CSV/Excel file uploads from the user.
     - Communicating with the backend via REST APIs.

2. **API Layer (Backend)**
   - **Framework:** Django & Django REST Framework (DRF)
   - **Responsibilities:**
     - Authentication and session management.
     - File parsing and initial validation (CSV data extraction).
     - Storing parsed financial records in the primary database.
     - Acting as a gateway to the AI and Analytics services.

3. **Data Layer**
   - **Relational Database:** PostgreSQL
     - Stores user profiles, transaction data, upload metadata, and analytical summaries.
   - **Vector Database:** ChromaDB
     - Stores embeddings of financial reports, past interactions, or text-heavy insights for semantic search and conversational memory.

4. **AI & Analytics Layer**
   - **Orchestration:** LangChain
   - **LLM Provider:** OpenAI API (with future-proofing for Ollama local LLMs)
   - **Responsibilities:**
     - **Data Analysis:** Anomaly detection, spending categorization, and basic fraud detection logic.
     - **Conversational Interface:** Interpreting user queries, fetching relevant data from PostgreSQL/ChromaDB using Retrieval-Augmented Generation (RAG) or SQL agents, and generating human-readable insights.
     - **Forecasting:** Simple predictive models on spending trends.

## Data Pipeline

1. **Ingestion:** User uploads a CSV.
2. **Processing:** Django parses the CSV, validates columns, and stores raw records in PostgreSQL.
3. **Analytics:** Background tasks or triggered services analyze the data to compute summaries (total spent, category breakdown).
4. **AI Embedding:** High-level insights are chunked, embedded, and stored in ChromaDB if necessary.
5. **Querying:** User asks a question ("How much did I spend on food?"). The AI Agent queries the SQL DB or Vector DB, synthesizes an answer, and returns it to the frontend.
