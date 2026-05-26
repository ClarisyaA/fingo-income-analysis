# Leakage Rules — Fingo v13
## FORBIDDEN in FEATURE_COLS
next_week_income, next_week_direction, monthly_income, avg_weekly_income,
income_std_4w, income_cv_4w, income_range_4w, income_w1-w4, synthetic_weekly_income

## Income Sequence Ordering
- income_w4 = TERLAMA (4 minggu lalu)
- income_w1 = TERBARU (minggu lalu)
- Kronologis: w4 → w3 → w2 → w1

## Direction Threshold
- 10% (DIRECTION_THRESHOLD = 0.10)
- Pakai >= dan <= bukan > dan <
- Up jika pct >= 0.10, Down jika pct <= -0.10, Stable otherwise

## Split Rules
- Split by synthetic_user_id (not random rows!)
- Scaler fit on train ONLY

## Normalization
- log1p -> MinMaxScaler (not RobustScaler)

## Survey Role
- Survey 384 responden = acuan distribusi, bukan training utama
- Synthetic 3000 users = dataset training utama
