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
  Mean  470113.55  413086.40
Median  390000.00  342341.50
   Std  308008.96  265611.07
    CV       0.66       0.64
   Min   60000.00   56598.00
   Max 1382000.00 1382000.00

## Autocorrelation
Mean lag-1: 0.6794

## Users: 384, Rows: 19968
