# FinSight AI

**Tagline:** LLM-Powered Financial Analytics & Conversational Insight Platform

## Project Goal
Build a modern AI-powered financial analytics platform that allows users to upload financial datasets (CSV/Excel), analyze spending patterns, detect anomalies, generate AI insights, and interact with data through a conversational LLM interface.

## Tech Stack
- **Frontend:** Flutter, GetX
- **Backend:** Django, Django REST Framework (DRF)
- **AI Stack:** OpenAI API, LangChain (Optional Future Upgrade: Ollama Local LLM)
- **Database:** PostgreSQL
- **Vector Database:** ChromaDB

## Project Structure
- `backend/` - Django REST API + AI services
- `frontend/` - Flutter application
- `datasets/` - Kaggle datasets and processed data
- `ai_models/` - ML/LLM related scripts and models
- `notebooks/` - Data analysis and experimentation
- `docs/` - Architecture diagrams, API docs, planning

## Setup Guide

### 1. Dataset Preparation
Download the "Personal Finance ML Dataset" from Kaggle:
[Dataset Link](https://www.kaggle.com/datasets/miadul/personal-finance-ml-dataset)

Extract the CSV files and place them in the `datasets/` directory.

*(Further setup instructions for Backend and Frontend will be added as they are developed.)*
