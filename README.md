# AI-Powered COD RTO Decision Engine

Take-home assignment prototype for a D2C haircare brand.

## What it does
- Scores every COD order for estimated RTO risk.
- Routes the order to **Ship as-is / Ship after confirmation / Nudge to prepaid / Hold-cancel**.
- Uses deterministic numerical features for maths and risk scoring.
- Keeps an AI boundary for messy human-language checks: suspicious names and incomplete/landmark-style addresses.
- Stores thresholds in `config.yaml` so operations can change policy without touching Python.
- Includes a Streamlit mock for the decision engine, WhatsApp flows and founder dashboard.
- Includes a business memo, decision log and AI usage log.

## Dataset
`orders_sample.csv` contains 2,018 historical COD orders.

Observed RTO rate: **28.2%**.

## Model
A leakage-aware temporal feature set is used with logistic regression. A chronological 80/20 holdout produced ROC-AUC **0.724**. The final model is retrained on all historical data for the demo.

This is intentionally a simple, explainable baseline rather than an unnecessarily complex model.

## Economics
RTO cost:
₹65 forward + ₹65 return + ₹25 handling + 8% × ₹180 damage exposure = **₹169.40**.

Prepaid discount: **₹30**. The memo explains the trade-off.

## Run in under 10 minutes

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — Streamlit demo
- `decision_engine.py` — scoring and action logic
- `config.yaml` — non-technical policy thresholds
- `rto_model.joblib` — trained model
- `reference_stats.json` — historical risk rates
- `orders_sample.csv` — supplied dataset
- `business_memo.pdf` — founder memo
- `decision_log.md` — important choices and alternatives
- `ai_usage_log.md` — AI usage and corrections
- `last_month_policy_buckets.csv` — September 2026 historical simulation
- `metrics.json` — reproducible summary metrics

## Important assumptions
The policy simulation uses conservative assumptions for confirmation and prepaid RTO reduction, documented in `config.yaml`. These are **planning assumptions**, not claimed causal results. A production system should A/B test them.

## Design principle
The system deliberately does not let the LLM perform numerical risk scoring. Numerical features and thresholds are deterministic and reproducible; the LLM boundary is reserved for ambiguous natural language.
