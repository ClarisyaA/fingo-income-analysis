# Fingo — Weekly Income Forecasting for Gig Workers
**Tim:** CC26-PSU217 | **Role:** Data Scientist 2 — Clarisya Adeline
**Branch:** feat/income-predictor-final

---

## Overview
Pipeline prediksi pendapatan mingguan untuk pekerja gig Indonesia.

- **Dataset survey:** 384 responden pekerja gig Indonesia (Google Form Mei 2026)
- **Survey digunakan sebagai:** distribusi acuan untuk generate 3.000 synthetic users
- **Target utama:** weekly income forecasting (prediksi pendapatan minggu depan)
- **Synthetic dataset:** 3.000 users × 52 minggu = 156.000 rows

## Penting: Temporal Mapping income_w1–w4
income_w1–w4 dalam survey **bukan** minggu 1–4 bulan kalender. Mereka adalah
4 periode mingguan relatif sebelum responden mengisi form:
- `income_w1` = H-7 s/d H-1 dari timestamp (terbaru)
- `income_w4` = H-28 s/d H-22 dari timestamp (terlama)

**Urutan kronologis model:** `income_w4 → income_w3 → income_w2 → income_w1`

## Cara Menjalankan
Jalankan notebook secara berurutan dari 01 sampai 08.
Setiap notebook auto-pull dari GitHub di awal dan push ke GitHub di akhir.

```
notebooks/
├── 01_Data_Preparation.ipynb
├── 02_Temporal_Mapping.ipynb
├── 03_EDA_Survey.ipynb
├── 04_Synthetic_Data_Generation.ipynb
├── 05_Feature_Engineering.ipynb
├── 06_Model_Dataset_Split.ipynb
├── 07_Bias_Validation.ipynb
└── 08_Documentation_Export.ipynb
```

## Output untuk AI Engineer
```
outputs/model_contract/
├── income_train.csv
├── income_val.csv
├── income_test.csv
├── income_scalers.pkl
├── feature_columns.json
└── model_contract.json
```

## Dokumentasi
- [notebook.md](notebook.md) — alur modular lengkap
- [data_dictionary.md](data_dictionary.md) — definisi semua kolom
