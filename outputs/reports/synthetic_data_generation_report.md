# Synthetic Data Generation Report

## Metode
- Base income: rata-rata income_w1-w4 per user (fallback: median per gig_type)
- Volatility: CV dari income_w1-w4 (minimum CV = 0.15)
- Seasonal multipliers: dari preferensi form + calendar events
- Noise: lognormal, clipped [0.5, 1.8]
- Income cap: P98 per gig_type

## Output
- synthetic_52week_user_income.csv: 27820 rows
- synthetic_52week_weekly_forecasting_dataset.csv: 25680 rows

## Disclaimer
Synthetic data is for simulation and prototyping ONLY. Not real observed income data.
