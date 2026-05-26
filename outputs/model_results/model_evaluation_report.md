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
| XGBRegressor | Rp 63.173 | Rp 121.460 | 119.95% | 0.8240 |
| GradientBoostingRegressor | Rp 64.266 | Rp 121.263 | 126.58% | 0.8246 |
| RandomForestRegressor | Rp 65.075 | Rp 124.156 | 109.47% | 0.8161 |
| Ridge | Rp 108.027 | Rp 201.323 | 125.93% | 0.5166 |
| LinearRegression | Rp 108.027 | Rp 201.323 | 125.93% | 0.5166 |

---

## 5. Best Regression Model

**XGBRegressor** — dipilih berdasarkan MAE terkecil di validation set.

---

## 6. Regression Test Metrics

| Metric | Value |
|---|---|
| MAE | Rp 64.557 |
| RMSE | Rp 125.159 |
| MAPE | 113.81% |
| R2 | 0.8279 |

---

## 7. Classification Model Comparison (Validation)

| Model | Val Accuracy | Val Prec | Val Recall | Val F1 |
|---|---|---|---|---|
| RandomForestClassifier | 0.7720 | 0.6694 | 0.6393 | 0.6506 |
| XGBClassifier | 0.8029 | 0.7705 | 0.6108 | 0.6418 |
| GradientBoostingClassifier | 0.7990 | 0.7617 | 0.6057 | 0.6353 |
| LogisticRegression | 0.7117 | 0.6183 | 0.6335 | 0.6199 |

---

## 8. Best Classification Model

**RandomForestClassifier** — dipilih berdasarkan macro F1 tertinggi di validation set.

---

## 9. Classification Test Metrics

| Metric | Value |
|---|---|
| Accuracy | 0.7692 |
| Macro Precision | 0.6650 |
| Macro Recall | 0.6371 |
| Macro F1 | 0.6478 |

---

## 10. Top Feature Importance (Best Regressor)

| Feature | Importance |
|---|---|
| lag_1_income | 0.423948 |
| rolling_mean_4w | 0.187612 |
| rolling_mean_8w | 0.092991 |
| rolling_mean_2w | 0.089400 |
| rolling_max_4w | 0.027749 |
| gig_content_creator | 0.007809 |
| income_growth_1w | 0.007793 |
| gig_pekerja_harian | 0.006975 |
| rolling_median_4w | 0.006845 |
| rolling_std_8w | 0.006721 |

---

## 11. Interpretasi

- **MAE** model terbaik di test set adalah **Rp 64.557**.
- **MAPE** sebesar **113.81%** menunjukkan rata-rata error relatif terhadap income aktual.
- Model baseline sudah cukup baik sebagai acuan awal (R2 = 0.8279).
- Model sequence seperti **LSTM sangat layak dicoba** karena data income bersifat temporal dan berurutan per user.
- Fitur lag/rolling yang penting: lag_1_income, rolling_mean_4w, rolling_mean_8w, rolling_mean_2w, rolling_max_4w
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
