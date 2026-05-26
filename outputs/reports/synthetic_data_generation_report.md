# Synthetic Data Generation Report — Fingo v12
## Method: Autoregressive AR(1)
Formula: income_t = 0.65 * income_(t-1) + 0.30 * expected_income_t + 0.05 * trend + noise
- Base income: user average W1-W4 (fallback to gig_type median)
- CV clamped [0.15, 0.70]
- Income non-negative, capped at P98 per gig_type
- Seasonal multiplier via get_total_seasonal_multiplier() clamped [0.50, 1.80]
- Seed: 42

## Quality Metrics
metric       real  synthetic
  Mean  413522.62  364634.16
Median  275000.00  235911.50
   Std  413271.63  343501.36
    CV       1.00       0.94
   Min   25000.00   17938.00
   Max 1832500.00 1675491.00

## Autocorrelation
Mean lag-1: 0.6520

## Users: 298, Rows: 15496
