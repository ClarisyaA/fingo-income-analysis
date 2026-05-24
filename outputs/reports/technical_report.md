# Technical Report — Fingo Weekly Income Forecasting for Gig Workers
**Tim:** CC26-PSU217 | **Versi:** v10-WEEKLY-FINAL | **Tanggal:** 2026

---

## 1. Executive Summary
Fingo adalah aplikasi financial planning untuk pekerja gig/informal Indonesia.
Notebook ini menghasilkan pipeline data lengkap untuk weekly income forecasting.

## 2. Problem Discovery
Pekerja gig sulit memperkirakan pendapatan minggu depan karena fluktuatif.

## 3. Business Questions
9 BQ dijawab melalui EDA dan explanatory analysis.

## 4. Data Sources
- Survei primer: 535 responden Google Form (Mei 2026)
- BPS 2023-2025: benchmark regional pendapatan sektor jasa

## 5. Data Gathering
Data survei dan BPS dimuat dari repo GitHub.

## 6. Data Assessing
15 masalah teridentifikasi: PII, multi-select encoding, outlier income, kategori tidak standar.

## 7. Data Cleaning
Rename kolom, drop PII, konversi numerik, clip, winsorize P2-P98, standardisasi kategori.

## 8. Form Mapping
20 kolom form di-mapping ke nama bersih. Mapping disimpan ke JSON.

## 9. Seasonal Feature Mapping
Seasonal features dari jawaban form: payday, weekend, Ramadan, Harbolnas, promo.
Natal/Tahun Baru = calendar-based, BUKAN dari form.

## 10. Feature Engineering
Fitur EDA: monthly income, CV, direction. Fitur training: lag, rolling, trend, calendar, context.

## 11. EDA
13+ visualisasi menjawab 9 business questions.

## 12. Weekly Forecasting Dataset
Wide → rolling long format. 3 row per responden (target_week 2,3,4). Anti-leakage ketat.

## 13. Baseline Modeling
Regression: Random Forest (MAE=154324, R²=0.5052)
Classification: XGBoost (Accuracy=58.9%)

## 14. A/B Testing Simulation
Simulasi offline. Treatment group menunjukkan uplift readiness score.

## 15. Dashboard Preparation
15 file CSV untuk Streamlit dashboard.

## 16. Data Dictionary
22 entri dengan leakage risk tagging.

## 17. AI Engineer Handover
4 file model contract: features, target, leakage rules, inference spec.

## 18. Limitation
- Cross-sectional survey (1 snapshot per responden)
- N=535 cukup untuk baseline, belum ideal untuk deep learning
- Convenience sampling via Google Form

## 19. Conclusion
Dataset weekly forecasting berhasil dibuat dengan anti-leakage ketat.

## 20. Recommendation
1. Deploy AI Engineer TensorFlow model
2. Kumpulkan data longitudinal >= 12 minggu
3. A/B test in-product setelah 200+ pengguna aktif
4. Update BPS benchmark tahunan
