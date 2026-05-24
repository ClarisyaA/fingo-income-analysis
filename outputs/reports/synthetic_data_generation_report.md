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
  Mean  488042.62  432798.24
Median  430000.00  399059.00
   Std  300462.40  230289.89
    CV       0.62       0.53
   Min    6800.00   22391.00
   Max 1350000.00 1324678.00

## Autocorrelation
Mean lag-1: 0.6535

## Users: 535, Rows: 27820
