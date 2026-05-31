# Model Evaluation Report
**Fingo Income Predictor** | Tim CC26-PSU217 | DS2 Clarisya Adeline

---

## 1. Overview
Notebook ini melatih dan mengevaluasi model baseline ML untuk prediksi pendapatan mingguan pekerja gig economy. Baseline digunakan sebagai benchmark sebelum AI Engineer mengembangkan model sequence/LSTM.

---

## 2. Dataset Split Summary

| Split | Baris |
|---|---|
| Train | 100,800 |
| Validation | 21,600 |
| Test | 21,600 |

Split dilakukan **by `synthetic_user_id`**, bukan random row — tidak ada overlap user antar subset.

---

## 3. Feature Count

Jumlah fitur: **58 fitur**  
Anti-leakage check: **PASSED**

---

## 4. Regression Model Comparison (Validation)

| Model | Val MAE | Val RMSE | Val MAPE | Val R2 |
|---|---|---|---|---|
| XGBRegressor | Rp 42.702 | Rp 90.524 | 11.92% | 0.9011 |
| GradientBoostingRegressor | Rp 43.702 | Rp 90.929 | 12.17% | 0.9002 |
| RandomForestRegressor | Rp 44.026 | Rp 91.918 | 12.24% | 0.8980 |
| Ridge | Rp 99.119 | Rp 195.555 | 25.75% | 0.5383 |
| LinearRegression | Rp 99.121 | Rp 195.565 | 25.75% | 0.5382 |

---

## 5. Best Regression Model

**XGBRegressor** — dipilih berdasarkan MAE terkecil di validation set.

---

## 6. Regression Test Metrics

| Metric | Value |
|---|---|
| MAE | Rp 42.931 |
| RMSE | Rp 90.468 |
| MAPE | 11.96% |
| R2 | 0.9091 |

---

## 7. Classification Model Comparison (Validation)

| Model | Val Accuracy | Val Prec | Val Recall | Val F1 |
|---|---|---|---|---|
| RandomForestClassifier | 0.7469 | 0.6208 | 0.6172 | 0.6181 |
| XGBClassifier | 0.7955 | 0.7535 | 0.5751 | 0.6153 |
| GradientBoostingClassifier | 0.7917 | 0.7452 | 0.5690 | 0.6080 |
| LogisticRegression | 0.6891 | 0.5729 | 0.6139 | 0.5859 |

---

## 8. Best Classification Model

**RandomForestClassifier** — dipilih berdasarkan macro F1 tertinggi di validation set.

---

## 9. Classification Test Metrics

| Metric | Value |
|---|---|
| Accuracy | 0.7489 |
| Macro Precision | 0.6250 |
| Macro Recall | 0.6207 |
| Macro F1 | 0.6221 |

---

## 10. Top Feature Importance (Best Regressor)

| Feature | Importance |
|---|---|
| lag_1_income | 0.609652 |
| rolling_mean_2w | 0.239554 |
| rolling_mean_8w | 0.060533 |
| rolling_mean_4w | 0.020814 |
| rolling_max_4w | 0.017025 |
| rolling_median_4w | 0.010551 |
| rolling_range_4w | 0.002842 |
| gig_kurir | 0.002247 |
| rolling_std_4w | 0.001973 |
| rolling_std_8w | 0.001737 |

---

## 11. Interpretasi

- **MAE** model terbaik di test set adalah **Rp 42.931**.
- **MAPE** sebesar **11.96%** menunjukkan rata-rata error relatif terhadap income aktual.
- Model baseline sudah cukup baik sebagai acuan awal (R2 = 0.9091).
- Model sequence seperti **LSTM sangat layak dicoba** karena data income bersifat temporal dan berurutan per user.
- Fitur lag/rolling yang penting: lag_1_income, rolling_mean_2w, rolling_mean_8w, rolling_mean_4w, rolling_max_4w
- Split sudah dilakukan by user — tidak ada data leakage antar split.
- Anti-leakage check sudah diverifikasi sebelum training.

---

## 12. Rekomendasi untuk AI Engineer

1. Gunakan baseline ini (MAE, RMSE, MAPE, R2) sebagai benchmark minimum yang harus dilewati LSTM.
2. Pertahankan split by `synthetic_user_id` agar evaluasi tetap fair.
3. Load `outputs/model_contract/income_scalers.pkl` untuk scaler yang konsisten.
4. Load `outputs/model_contract/feature_columns.json` untuk daftar fitur.
5. Target regression: `next_week_income` (latih log1p, evaluasi rupiah asli).
6. Target classification: `next_week_direction` (Down=0, Stable=1, Up=2).
7. Perhatikan distribusi kelas yang tidak seimbang pada classification.
8. Model terbaik tersimpan di `outputs/model_results/` siap untuk perbandingan.
