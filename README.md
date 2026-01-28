# SaaS FP&A Narrative Reporting Copilot

## Overview
This project builds an AI-powered copilot that generates executive-ready
monthly FP&A narratives for SaaS businesses using structured financial data.

The copilot converts P&L and Balance Sheet data into:
- Variance analysis and key drivers
- Draft FP&A commentary
- Leadership summary
- Review-mode feedback highlighting risks and missing context

## Data Disclaimer
All financial data used in this project is synthetic and illustrative.
The structure and directional trends are inspired by publicly available
SaaS company disclosures (e.g., Salesforce) but do not represent actual
company performance.

## Scope
- Monthly P&L (Actual vs Budget)
- Balance Sheet (Month-over-Month change)
- SaaS-focused financial metrics
- Narrative generation grounded in finance definitions and reporting rules

Out of Scope:
- Cash Flow Statement
- Customer metrics (churn, CAC, LTV)
- Forecasting and scenario modeling

## Architecture (High-Level)
Planner → Compute Engine → RAG (Finance Glossary) → Narrative Draft → Review Mode → Final Output


## Security Notes
- API keys are loaded via environment variables
- No secrets are stored in code or committed to GitHub


## Limitations
- Uses synthetic data
- No operational drivers (e.g., churn or pipeline data)
- Narrative explanations avoid causal claims unless supported by data
