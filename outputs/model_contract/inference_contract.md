# Inference Contract — Fingo Weekly Income Forecasting

## Contoh Input
```json
{
  "target_week": 4,
  "income_history": [700000, 850000, 900000],
  "usia": 21,
  "gig_type": "ojek_online",
  "domisili_code": "jabodetabek",
  "experience_months": 12,
  "hari_kerja_per_minggu": 6,
  "jam_kerja_per_hari": 8,
  "waktu_ramai": ["Akhir pekan / Sabtu-Minggu", "Akhir bulan / tanggal gajian"],
  "faktor_fluktuasi": ["Cuaca", "Jumlah pesanan atau project yang masuk"],
  "target_date": "2026-06-01"
}
```

## Contoh Output
```json
{
  "predicted_next_week_income": 920000,
  "predicted_direction": "Up",
  "target_week": 4,
  "insight": "Pendapatan minggu depan diprediksi naik."
}
```
