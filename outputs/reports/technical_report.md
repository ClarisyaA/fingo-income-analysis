# Technical Report — Fingo Weekly Income Forecasting for Gig Workers
**Tim:** CC26-PSU217 | **Versi:** v11-WEEKLY-FINAL | **Tanggal:** 2026

---

## 1. Executive Summary
Fingo adalah aplikasi financial planning untuk pekerja gig/informal Indonesia. Notebook ini membangun pipeline data science lengkap untuk weekly income forecasting, mencakup data real 4 minggu dan data sintetis 52 minggu.

**Data real 4w** adalah dasar validitas utama. **Data sintetis 52w** digunakan untuk simulasi longitudinal dashboard dan prototyping AI Engineer.

## 2. Problem Discovery
Pekerja gig sulit memperkirakan pendapatan minggu depan karena fluktuatif dari minggu ke minggu.

## 3. Business Questions
9 BQ dijawab melalui EDA dan explanatory analysis (BQ1–BQ9).

## 4. Data Sources
- Survei primer: 535 responden Google Form (Mei 2026)
- BPS 2023-2025: benchmark regional pendapatan sektor jasa per provinsi

## 5. Data Gathering
Data survei dan BPS dimuat dengan robust loader yang menangani berbagai format file.

## 6. Data Assessing
16 masalah teridentifikasi: PII (kontak, consent), multi-select encoding, outlier income, kategori tidak standar, timestamp untuk calendar features.

## 7. Data Cleaning
Rename kolom, drop PII (consent + kontak_gopay), konversi numerik, median imputation, clip, winsorize P2-P98, standardisasi 8 kategori gig_type.

## 8. Form Mapping
20 kolom form di-mapping ke nama bersih berdasarkan posisi kolom. Mapping disimpan ke JSON.

## 9. Gig Type Preservation
**8 kategori asli dari form dipertahankan:**
- jualan_online: 97 responden
- pekerja_harian: 91 responden
- freelance_desain: 82 responden
- ojek_online: 77 responden
- kurir: 55 responden
- freelance_it: 48 responden
- tutor: 47 responden
- content_creator: 38 responden

## 10. Seasonal Feature Mapping
Seasonal features dari jawaban form: pref_payday, pref_weekend, pref_ramadan_lebaran, pref_harbolnas, pref_promo_aplikasi, pref_awal_bulan.
Natal/Tahun Baru = calendar-based (BUKAN dari form). Bernilai 0 untuk data Mei 2026.

## 11. Real 4-Week Dataset Formulation
Wide → rolling long format. 3 row per responden (target_week 2, 3, 4). Anti-leakage ketat.
Total: 1605 rows dari 535 responden.

## 12. Synthetic 52-Week Dataset Generation
52 minggu per user dari awal 2026. Base income dari rata-rata W1-W4 actual. Seasonal multipliers berdasarkan preferensi form.
Total: 27820 rows (535 users × 52 weeks).

## 13. Feature Engineering
Fitur EDA: monthly_income, CV, direction. Fitur training: lag, rolling, trend, calendar, context, OHE 8 gig_type.

## 14. EDA (BQ1–BQ7)
13+ visualisasi. Insight utama:
- Freelance IT & Desain memiliki income tertinggi
- Content creator paling volatil (CV tertinggi)
- Jumlah pesanan/order = faktor fluktuasi utama
- Income survei umumnya di bawah benchmark BPS formal

## 15. Baseline Modeling — Real 4w
- Regression best: Random Forest (MAE=154191, R²=0.5063, Norm_MAE=0.1656)
- Classification best: XGBoost (Accuracy=57.9%, F1=47.7%)

## 16. Synthetic Data Disclaimer
Synthetic 52-week data dibuat untuk simulasi longitudinal dan prototyping AI Engineer. Performa model pada synthetic TIDAK diklaim sebagai real-world performance final.

## 17. A/B Testing Simulation
Simulasi offline. Treatment group menunjukkan readiness score lebih tinggi (2.1% uplift, p=0.3225).

## 18. Dashboard Preparation
14+ file CSV untuk Streamlit dashboard (outputs/dashboard/).

## 19. Data Leakage Prevention
- next_week_income/direction tidak pernah masuk fitur
- monthly_income tidak pernah masuk training
- Split berbasis respondent_id (bukan random row)
- Scaler fit hanya pada train set

## 20. AI Engineer Handover
4 file model contract: final_weekly_features.json, target_contract.json, leakage_rules.md, inference_contract.md.

## 21. Limitations
- Cross-sectional survey (1 snapshot per responden) — bukan longitudinal nyata
- N=535 cukup untuk baseline, belum ideal untuk deep learning
- Convenience sampling via Google Form (Mei 2026)
- Synthetic data hanya simulasi — bukan pengganti longitudinal nyata

## 22. Conclusion
Dataset weekly forecasting berhasil dibuat dengan anti-leakage ketat, 8 gig_type dipertahankan, dan package handover lengkap untuk AI Engineer.

## 23. Recommendation
1. AI Engineer: Kembangkan TensorFlow model (LSTM/Transformer) menggunakan real_4w_train.csv
2. Data: Kumpulkan data longitudinal >= 12 minggu per pengguna
3. A/B Test: Lakukan in-product experiment setelah 200+ pengguna aktif Fingo
4. BPS: Update bps_jasa_weekly tahunan saat SAKERNAS terbaru rilis
