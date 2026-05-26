# Technical Report — Fingo v12-REFACTORED
**Tim:** CC26-PSU217 | **Versi:** v12-REFACTORED | **Tanggal:** 2026

## Key Changes from v11
1. Direction threshold: 10% (was 5%) — more robust to noise
2. Synthetic generation: Autoregressive AR(1) with formula: income_t = 0.65*income_(t-1) + 0.30*expected + 0.05*trend + noise
3. Target normalization: log1p + MinMaxScaler (was RobustScaler + clip)
4. Enhanced features: 8 new lag/volatility/momentum features
5. Evaluation: Separated real/synthetic, segment-level analysis by gig_type, month, week_of_month
6. Baselines: Added Rolling Mean (regression) and Rule-based Momentum (classification)

## Data Sources
- Survey: 298 respondents (Mei 2026)
- BPS 2023-2025: regional income benchmarks
- Synthetic: 298 users x 52 weeks (AR1)

## Best Model (Real 4w)
- Regression: Random Forest (MAE=181228, Norm_MAE=0.0935)
- Classification: XGBoost (Accuracy=60.0%, F1=46.3%)

## Autocorrelation Check
Mean lag-1 autocorrelation in synthetic data: 0.6520 (expected ~0.65)

## Disclaimer
Real 4w data is the primary validation basis. Synthetic 52w is for simulation only.
