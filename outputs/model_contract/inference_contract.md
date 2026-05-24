# Inference Contract — Fingo Weekly Income Forecasting

## Contoh Input
```json
{
  "target_week": 4,
  "income_history": [700000, 850000, 900000],
  "target_date": "2026-06-01",
  "usia": 21,
  "gig_type": "ojek_online",
  "domisili_code": "jabodetabek",
  "experience_months": 12,
  "hari_kerja_per_minggu": 6,
  "jam_kerja_per_hari": 8,
  "waktu_ramai": ["Akhir pekan / Sabtu-Minggu", "Akhir bulan / tanggal gajian"],
  "faktor_fluktuasi": ["Cuaca", "Jumlah pesanan atau project yang masuk"]
}
```

## Contoh Output
```json
{
  "predicted_next_week_income": 920000,
  "predicted_direction": "Up",
  "target_week": 4,
  "confidence": 0.78,
  "insight": "Pendapatan minggu depan diprediksi naik dibanding minggu terakhir."
}
```

## Feature Pipeline
1. Hitung lag features dari income_history
2. Hitung rolling statistics
3. Encode gig_type (8 kategori OHE)
4. Tambah calendar features dari target_date
5. Encode seasonal preference dari waktu_ramai dan faktor_fluktuasi
6. Normalize menggunakan weekly_target_scaler.pkl
7. Predict next_week_income_norm → inverse transform → Rupiah
8. Classify direction: Up/Stable/Down

## Files yang dibutuhkan AI Engineer
- data/processed/real_4w_train.csv (training data)
- data/processed/real_4w_test.csv (eval data)
- data/synthetic/synthetic_52w_train.csv (prototyping)
- outputs/preprocessors/weekly_target_scaler.pkl
- outputs/preprocessors/weekly_feature_scaler.pkl
- outputs/preprocessors/gig_label_encoder.pkl
- outputs/model_contract/final_weekly_features.json
- outputs/model_contract/target_contract.json
- outputs/model_contract/leakage_rules.md
