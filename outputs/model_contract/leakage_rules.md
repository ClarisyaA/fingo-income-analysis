# Leakage Rules — Fingo Weekly Forecasting

## Kolom DILARANG masuk FEATURE_COLS
| Kolom | Alasan |
|-------|--------|
| next_week_income | Target regresi |
| next_week_income_norm | Target normalized |
| next_week_direction | Target klasifikasi |
| monthly_income | Menggunakan semua W1-W4 |
| income_w1-w4 | Harus diubah ke lag features |

## Split Rules
- Split HARUS berbasis respondent_id
- Scaler fit HANYA pada train set
