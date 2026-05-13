# Dataset Notes: Personal Finance ML Dataset

**Source:** [Kaggle - Personal Finance ML Dataset](https://www.kaggle.com/datasets/miadul/personal-finance-ml-dataset)

**Dataset Overview:**
This dataset is a synthetic but realistic collection of 32,424 individual financial records, representing real-world personal finance behaviors across income groups, regions, and loan statuses. It is ideal for EDA, financial modeling, credit risk prediction, and machine learning tasks.

## Key Important Fields (Columns) to Analyze

### Demographics
- `user_id`: Unique user identifier
- `age`: Age of individual (18–70) (Numeric)
- `gender`: Gender (Categorical)
- `education_level`: Highest education level (Categorical)
- `employment_status`: Employment type (Categorical)
- `job_title`: Job title or role (Categorical)
- `region`: Geographic region (Categorical)

### Financial Indicators
- `monthly_income_usd`: Approx. monthly income in USD (Numeric)
- `monthly_expenses_usd`: Approx. monthly expenses in USD (Numeric)
- `savings_usd`: Total savings (Numeric)

### Loan / Credit Specifics
- `has_loan`: Whether individual has a loan (Categorical: Yes/No)
- `loan_type`: Type of loan (Categorical)
- `loan_amount_usd`: Loan principal amount (Numeric)
- `loan_term_months`: Duration of loan (Numeric)
- `monthly_emi_usd`: Monthly installment (Numeric)
- `loan_interest_rate_pct`: Interest rate on loan (Numeric)
- `debt_to_income_ratio`: Ratio of debt payments to income (Numeric)
- `credit_score`: Synthetic credit score (300–850) (Numeric)
- `savings_to_income_ratio`: Ratio of savings to annual income (Numeric)

### Dates
- `record_date`: Record creation date (Date field)

## Areas to Focus On for Analytics

1. **Missing Values:**
   - Need to implement checks for missing values, especially in `loan_type` and loan-specific fields for users where `has_loan` is 'No'.
   
2. **Numeric Analysis:**
   - Aggregating total incomes and expenses.
   - Calculating average credit scores across demographics.
   
3. **Target Prediction Possibilities:**
   - **Credit Risk:** Predicting the `credit_score` based on financial behavior.
   - **Loan Approval:** Predicting likelihood of defaulting or ideal loan amount/terms.
   - **Expense Categorization:** Grouping users into clusters based on their `savings_to_income_ratio`.
   
4. **Action Items for Development:**
   - The CSV parser should correctly map these columns to a PostgreSQL schema.
   - Set up automated summary endpoints for these numeric fields so the LLM agent has immediate access to summaries.
