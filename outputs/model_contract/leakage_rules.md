# Leakage Rules — Fingo v12
## FORBIDDEN in FEATURE_COLS
next_week_income, next_week_income_norm, next_week_direction, monthly_income, avg_weekly_income, income_std_4w, income_cv_4w, income_range_4w, income_w1-w4, synthetic_weekly_income
## Split Rules
- Split by respondent_id (not random rows)
- Scaler fit on train ONLY
## Direction Threshold
- 10% (DIRECTION_THRESHOLD = 0.10)
## Normalization
- log1p -> MinMaxScaler (not RobustScaler)
