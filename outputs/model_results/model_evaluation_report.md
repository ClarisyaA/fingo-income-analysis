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
| XGBRegressor | Rp 63.020 | Rp 120.887 | 121.06% | 0.8257 |
| GradientBoostingRegressor | Rp 64.180 | Rp 121.182 | 126.79% | 0.8248 |
| RandomForestRegressor | Rp 65.064 | Rp 124.284 | 110.68% | 0.8158 |
| Ridge | Rp 108.053 | Rp 200.575 | 125.81% | 0.5202 |
| LinearRegression | Rp 108.053 | Rp 200.576 | 125.81% | 0.5202 |

---

## 5. Best Regression Model

**XGBRegressor** — dipilih berdasarkan MAE terkecil di validation set.

---

## 6. Regression Test Metrics

| Metric | Value |
|---|---|
| MAE | Rp 64.440 |
| RMSE | Rp 124.801 |
| MAPE | 112.17% |
| R2 | 0.8289 |

---

## 7. Classification Model Comparison (Validation)

| Model | Val Accuracy | Val Prec | Val Recall | Val F1 |
|---|---|---|---|---|
| RandomForestClassifier | 0.7709 | 0.6675 | 0.6380 | 0.6491 |
| XGBClassifier | 0.8029 | 0.7703 | 0.6108 | 0.6418 |
| GradientBoostingClassifier | 0.7994 | 0.7616 | 0.6063 | 0.6360 |
| LogisticRegression | 0.7100 | 0.6186 | 0.6346 | 0.6198 |

---

## 8. Best Classification Model

**RandomForestClassifier** — dipilih berdasarkan macro F1 tertinggi di validation set.

---

## 9. Classification Test Metrics

| Metric | Value |
|---|---|
| Accuracy | 0.7693 |
| Macro Precision | 0.6646 |
| Macro Recall | 0.6372 |
| Macro F1 | 0.6477 |

---

## 10. Top Feature Importance (Best Regressor)

| Feature | Importance |
|---|---|
| lag_1_income | 0.434965 |
| rolling_mean_4w | 0.176070 |
| rolling_mean_2w | 0.094050 |
| rolling_mean_8w | 0.089255 |
| rolling_max_4w | 0.026297 |
| gig_content_creator | 0.008012 |
| gig_pekerja_harian | 0.007272 |
| rolling_median_4w | 0.007262 |
| rolling_std_4w | 0.006799 |
| rolling_std_8w | 0.006660 |

---

## 11. Interpretasi

- **MAE** model terbaik di test set adalah **Rp 64.440**.
- **MAPE** sebesar **112.17%** menunjukkan rata-rata error relatif terhadap income aktual.
- Model baseline sudah cukup baik sebagai acuan awal (R2 = 0.8289).
- Model sequence seperti **LSTM sangat layak dicoba** karena data income bersifat temporal dan berurutan per user.
- Fitur lag/rolling yang penting: lag_1_income, rolling_mean_4w, rolling_mean_2w, rolling_mean_8w, rolling_max_4w
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
