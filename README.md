# Fingo — Weekly Income Forecasting for Gig Workers

**Tim:** CC26-PSU217 | **Role:** Data Scientist 2 — Clarisya Adeline  
**Branch:** `feat/income-predictor-final`  
**Repo:** [ClarisyaA/fingo-income-analysis](https://github.com/ClarisyaA/fingo-income-analysis)

---

## Daftar Isi

- [Overview](#overview)
- [Konteks & Latar Belakang](#konteks--latar-belakang)
- [Temporal Mapping income_w1–w4](#temporal-mapping-income_w1w4)
- [Struktur Pipeline](#struktur-pipeline)
- [Cara Menjalankan](#cara-menjalankan)
- [Detail Tiap Notebook](#detail-tiap-notebook)
  - [01 — Data Preparation](#01--data-preparation)
  - [02 — Temporal Mapping](#02--temporal-mapping)
  - [03 — EDA Survey](#03--eda-survey)
  - [04 — Synthetic Data Generation](#04--synthetic-data-generation)
  - [05 — Feature Engineering](#05--feature-engineering)
  - [06 — Model Dataset Split](#06--model-dataset-split)
  - [07 — Bias Validation](#07--bias-validation)
  - [08 — Documentation Export](#08--documentation-export)
  - [09 — Model Training & Evaluation](#09--model-training--evaluation)
  - [10 — A/B Testing Income Predictor & Budgeting](#10--ab-testing-income-predictor--budgeting)
- [Output untuk AI Engineer](#output-untuk-ai-engineer)
- [Struktur Direktori](#struktur-direktori)
- [Dokumentasi Lanjutan](#dokumentasi-lanjutan)

---

## Overview

Pipeline prediksi pendapatan mingguan untuk pekerja gig Indonesia. Proyek ini mencakup seluruh alur dari data survey mentah hingga model-ready dataset beserta evaluasi model dan simulasi A/B testing.

| Item | Detail |
|------|--------|
| **Dataset survey** | 384 responden pekerja gig Indonesia (Google Form, Mei 2026) |
| **Fungsi survey** | Distribusi acuan untuk generate 3.000 synthetic users |
| **Target prediksi** | `next_week_income` — pendapatan minggu berikutnya |
| **Target klasifikasi** | `next_week_direction` — arah perubahan (naik/turun/stabil) |
| **Synthetic dataset** | 3.000 users × 52 minggu = **156.000 rows** |
| **Split model** | Kronologis by `synthetic_user_id` (train 70% / val 15% / test 15%) |

---

## Konteks & Latar Belakang

Pekerja gig (ojek online, freelancer, kurir, dll.) mengalami fluktuasi pendapatan yang tinggi sehingga sulit membuat rencana anggaran yang realistis. Fingo membangun fitur **Income Predictor** untuk membantu pengguna memperkirakan pendapatan minggu depan agar budget planner mereka dapat disesuaikan secara adaptif — bukan berdasarkan rata-rata historis yang statis.

Survey dilakukan sebagai **bootstrap data**, bukan sebagai dataset training langsung. Distribusi demografis, tipe pekerjaan, domisili, dan profil income dari 384 responden digunakan sebagai acuan statistik untuk mensimulasikan 3.000 user sintetis dengan pola perilaku yang realistis.

---

## Temporal Mapping income_w1–w4

> ⚠️ **Penting — baca ini sebelum melihat data.**

`income_w1`–`income_w4` dalam survey **bukan** minggu 1–4 bulan kalender. Keempat kolom ini adalah **4 periode mingguan relatif** sebelum responden mengisi form:

| Kolom | Rentang Waktu | Keterangan |
|-------|--------------|------------|
| `income_w1` | H-7 s/d H-1 dari timestamp | Minggu terbaru |
| `income_w2` | H-14 s/d H-8 dari timestamp | — |
| `income_w3` | H-21 s/d H-15 dari timestamp | — |
| `income_w4` | H-28 s/d H-22 dari timestamp | Minggu terlama |

**Urutan kronologis yang benar untuk model:**

```
income_w4 → income_w3 → income_w2 → income_w1 → [PREDIKSI next_week_income]
   terlama                                terbaru
```

Urutan ini **wajib dijaga** di seluruh pipeline. Membalik urutan akan menyebabkan data leakage.

---

## Struktur Pipeline

```
Survey (384 responden)
        │
        ▼
01_Data_Preparation          ← Cleaning & standarisasi survey
        │
        ▼
02_Temporal_Mapping          ← Pemetaan w1–w4 ke tanggal absolut
        │
        ▼
03_EDA_Survey                ← Eksplorasi distribusi & pola income
        │
        ▼
04_Synthetic_Data_Generation ← Generate 3.000 users × 52 minggu
        │
        ▼
05_Feature_Engineering       ← Sliding window → supervised dataset
        │
        ▼
06_Model_Dataset_Split       ← Train/Val/Test split (kronologis by user)
        │
        ▼
07_Bias_Validation           ← Validasi data synthetic vs survey & BPS
        │
        ▼
08_Documentation_Export      ← Auto-generate README, notebook.md, data_dictionary.md
        │
        ▼
09_Model_Training_Evaluation ← Train & evaluasi model (regression + classification)
        │
        ▼
10_AB_Testing_…              ← Simulasi A/B test dampak income predictor ke budget planning
```

---

## Cara Menjalankan

### Prasyarat

- Google Colab (direkomendasikan) atau Python 3.10+
- `GITHUB_TOKEN` tersimpan di Colab Secrets (key: `GITHUB_TOKEN`)
- Akses ke repo `ClarisyaA/fingo-income-analysis` branch `feat/income-predictor-final`

### Urutan Eksekusi

Jalankan notebook **secara berurutan** dari 01 sampai 10. Setiap notebook melakukan:
1. **Auto-pull** dari GitHub di cell pertama
2. **Auto-push** ke GitHub di cell terakhir

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10
```

> Notebook 09 dan 10 dapat dijalankan **ulang secara independen** setelah notebook 01–08 selesai, karena inputnya berasal dari `outputs/model_contract/` dan `data/synthetic/` yang sudah tersimpan di GitHub.

### Flag Penting

```python
FRESH_CLONE = False  # Ganti True hanya untuk clone ulang dari nol
```

---

## Detail Tiap Notebook

---

### 01 — Data Preparation

**File:** `01_Data_Preparation.ipynb`

**Tujuan:** Membersihkan dan menstandarisasi data mentah dari Google Form survey sebelum digunakan di tahap berikutnya.

**Input:**
- `data/raw/form_responses.csv` — hasil export Google Form survey (384 baris)
- BPS files di `data/raw/` — referensi benchmark pendapatan per daerah

**Output:**
- `data/processed/survey_clean.csv`

**Yang dilakukan:**
- Normalisasi nama kolom (lowercase, snake_case)
- Parsing `timestamp` dan `timestamp_parsed` dari kolom waktu form (⚠️ **tidak boleh di-drop** — dibutuhkan oleh notebook 02)
- Standarisasi format nilai income (hapus karakter non-numerik, konversi ke float)
- Validasi range income: nilai < Rp 50.000/minggu dianggap tidak valid dan di-flag
- Penanganan missing values dan outlier ekstrem
- Standarisasi kolom kategorik (`gig_type`, `domisili`, dll.)

**Catatan penting:**
- Kolom `timestamp` dan `timestamp_parsed` **wajib dipertahankan** karena menjadi acuan kalkulasi tanggal absolut di notebook 02
- Income floor minimum: **Rp 50.000/minggu** (batas bawah yang masuk akal untuk pekerja gig Indonesia)

---

### 02 — Temporal Mapping

**File:** `02_Temporal_Mapping.ipynb`

**Tujuan:** Mengubah income_w1–w4 yang bersifat relatif menjadi tanggal absolut berdasarkan timestamp responden, lalu menghasilkan format long untuk analisis time-series.

**Input:**
- `data/processed/survey_clean.csv`

**Output:**
- `data/processed/survey_temporal_mapped.csv` — format wide, dengan kolom tanggal absolut tiap minggu
- `data/processed/survey_weekly_income_long.csv` — format long (1 baris per responden per minggu)

**Logika pemetaan:**

```
timestamp responden → T (hari H)

income_w1 → [T-7, T-1]   (minggu terbaru)
income_w2 → [T-14, T-8]
income_w3 → [T-21, T-15]
income_w4 → [T-28, T-22] (minggu terlama)
```

**Yang dilakukan:**
- Kalkulasi `week_start` dan `week_end` absolut untuk setiap w1–w4 per responden
- Generate format long: satu baris per (responden, minggu) dengan kolom `week_number`, `week_start`, `income`
- Validasi bahwa urutan kronologis w4 → w3 → w2 → w1 terjaga
- Verifikasi tidak ada tanggal yang tumpang tindih antar periode

---

### 03 — EDA Survey

**File:** `03_EDA_Survey.ipynb`

**Tujuan:** Eksplorasi mendalam distribusi data survey untuk memahami karakteristik responden dan pola income sebelum data sintetis dibuat.

**Input:**
- `data/processed/survey_temporal_mapped.csv`
- `data/processed/survey_weekly_income_long.csv`

**Output:**
- Chart ke `outputs/charts/` — visualisasi distribusi dan tren
- Dashboard CSV ke `outputs/dashboard/` — ringkasan statistik untuk keperluan dashboard
- `outputs/reports/survey_eda_summary.md` — laporan naratif hasil EDA

**Yang dilakukan:**
- Distribusi demografis: `gig_type`, `domisili`, jenis kelamin, usia
- Analisis distribusi income per minggu (w1–w4): mean, median, std, skewness
- Pola volatilitas income: perubahan w4→w1 per responden
- Analisis musiman: apakah ada pola income berdasarkan bulan atau event kalender (Ramadan, Lebaran)
- Korelasi antar minggu: seberapa prediktif income minggu lalu terhadap minggu ini
- Segmentasi: profil income berbeda-beda per `gig_type` dan `domisili`
- Outlier analysis: identifikasi responden dengan pola income tidak wajar

---

### 04 — Synthetic Data Generation

**File:** `04_Synthetic_Data_Generation.ipynb`

**Tujuan:** Membuat dataset sintetis 52 minggu untuk 3.000 user menggunakan distribusi dari data survey sebagai acuan statistik.

**Input:**
- `data/processed/survey_temporal_mapped.csv`

**Output:**
- `data/synthetic/synthetic_52week_user_income.csv` — 3.000 users × 52 minggu = 156.000 rows
- `data/synthetic/synthetic_params.json` — parameter distribusi yang digunakan untuk generate data

**Yang dilakukan:**
- Estimasi parameter distribusi income per segmen (`gig_type` × `domisili`): mean, std, dan koefisien variasi dari data survey
- Generate profil user sintetis: distribusi `gig_type` dan `domisili` mengikuti proporsi survey
- Simulasi time-series 52 minggu per user dengan mempertahankan:
  - **Autocorrelation**: income minggu ini bergantung pada minggu sebelumnya
  - **Seasonality**: kenaikan income saat event musiman (Ramadan, Lebaran, akhir tahun)
  - **Volatilitas per gig_type**: freelancer lebih volatile dibanding driver ojek
- Income floor enforcement: setiap nilai income di-clamp ke minimum **Rp 50.000/minggu**
- Simpan `synthetic_params.json` sebagai dokumentasi reproducibility

**Validasi bawaan:**
- Fail-fast jika ada income < Rp 50.000 lolos ke output
- Cek distribusi mean synthetic vs mean survey (harus dalam toleransi ±20%)

---

### 05 — Feature Engineering

**File:** `05_Feature_Engineering.ipynb`

**Tujuan:** Mengubah time-series 52 minggu menjadi supervised learning dataset menggunakan sliding window 4 minggu, dengan target prediksi minggu berikutnya.

**Input:**
- `data/synthetic/synthetic_52week_user_income.csv`
- `data/processed/survey_temporal_mapped.csv` (untuk merge atribut user)

**Output:**
- `data/processed/income_features.csv` — supervised dataset siap untuk model

**Urutan kronologis fitur (wajib dijaga):**

```
income_w4 (terlama) → income_w3 → income_w2 → income_w1 (terbaru) → next_week_income (target)
```

**Yang dilakukan:**
- **Sliding window 4 minggu**: untuk setiap user, generate semua window `[w4, w3, w2, w1] → next` dari 52 minggu historis
- **Fitur income lag**: `income_w1`, `income_w2`, `income_w3`, `income_w4`
- **Fitur statistik**: rolling mean, rolling std, rolling min/max atas window 4 minggu
- **Fitur trend**: delta income (w1−w2, w2−w3, w3−w4), pct_change
- **Fitur user**: `gig_type`, `domisili`, dan atribut demografis lain dari survey
- **Target regresi**: `next_week_income` (nilai kontinu)
- **Target klasifikasi**: `next_week_direction` (up/down/flat berdasarkan threshold %)
- **Anti-leakage check** (Cell 05.5): verifikasi bahwa tidak ada fitur dari `next_week_income` yang bocor ke feature set

**Fail-fast validation:**
- Semua kolom income harus ≥ Rp 50.000. Notebook berhenti jika ditemukan pelanggaran (akar masalah seharusnya sudah ditangani di notebook 04).

---

### 06 — Model Dataset Split

**File:** `06_Model_Dataset_Split.ipynb`

**Tujuan:** Membagi dataset fitur menjadi train/validation/test secara kronologis per user, lalu menyimpan scaler dan model contract untuk AI Engineer.

**Input:**
- `data/processed/income_features.csv`

**Output:**

| File | Keterangan |
|------|-----------|
| `outputs/model_contract/income_train.csv` | Data training |
| `outputs/model_contract/income_val.csv` | Data validasi |
| `outputs/model_contract/income_test.csv` | Data test (held-out) |
| `outputs/model_contract/income_scalers.pkl` | StandardScaler fitted on train only |
| `outputs/model_contract/feature_columns.json` | Daftar kolom fitur yang digunakan |
| `outputs/model_contract/model_contract.json` | Metadata lengkap pipeline untuk AI Engineer |

**Strategi split — kronologis by user:**

```
Split bukan random row, melainkan per synthetic_user_id:
- Train : user ID ke-1   s/d ke-2.100  (70%)
- Val   : user ID ke-2.101 s/d ke-2.550 (15%)
- Test  : user ID ke-2.551 s/d ke-3.000 (15%)
```

Dengan split ini, **tidak ada overlap user** antara train, val, dan test — menghindari data leakage level user.

**Yang dilakukan:**
- Sort user secara deterministik sebelum split
- Fit `StandardScaler` **hanya pada train set**, lalu transform val dan test (tidak ada train-test contamination)
- Generate `model_contract.json` berisi: daftar fitur, target kolom, scaler path, ukuran split, dan metadata pipeline
- Final validation (Cell 06.8): fail-fast jika ada income < Rp 50.000 di manapun dalam split

---

### 07 — Bias Validation

**File:** `07_Bias_Validation.ipynb`

**Tujuan:** Memvalidasi apakah data sintetis secara statistik masih representatif terhadap data survey asli dan benchmark BPS.

**Input:**
- `data/processed/income_features.csv`
- `data/processed/survey_temporal_mapped.csv`
- `data/synthetic/synthetic_52week_user_income.csv`

**Output:**
- `outputs/reports/bias_validation_report.md` — laporan bias lengkap dengan tabel pass/fail
- Charts ke `outputs/charts/` — visualisasi distribusi, autokorelasi, dan tren musiman

**Bias tests yang dijalankan:**

| Test | Cell | Penjelasan |
|------|------|-----------|
| **Bias Test 0**: Income Floor Sanity | 07.3b | Fail-fast: tidak boleh ada income < Rp 50.000 |
| **Bias Test 1**: Mean vs benchmark BPS | 07.4 | Mean synthetic harus dalam toleransi benchmark BPS per domisili |
| **Bias Test 2**: Distribution test (KS-like) | 07.5 | Distribusi synthetic vs survey tidak boleh terlalu divergen |
| **Bias Test 3**: Seasonal direction | 07.6 | Arah perubahan income saat event musiman (Ramadan, dll.) harus konsisten |
| **Bias Test 4**: Autocorrelation | 07.7 | Autokorelasi time-series synthetic harus realistis |
| **Bias Test 5**: BPS range per domisili | 07.8 | Income synthetic harus masuk rentang BPS per daerah |
| **Bias Test 6**: Income per gig_type vs survey | 07.9 | Distribusi per segmen pekerjaan harus proporsional terhadap survey |

> **Catatan:** Bias Test 0 dijalankan sebelum test lain dan bersifat blocking — notebook berhenti jika FAIL.

---

### 08 — Documentation Export

**File:** `08_Documentation_Export.ipynb`

**Tujuan:** Auto-generate dokumentasi repo yang selalu sinkron dengan kondisi pipeline terkini.

**Output:**
- `notebook.md` — alur modular lengkap seluruh pipeline (deskripsi tiap notebook dan sel utama)
- `data_dictionary.md` — definisi semua kolom di semua file output
- `README.md` — README utama repo (di-overwrite oleh notebook ini)

**Yang dilakukan:**
- Baca metadata dari setiap notebook (nama, input, output, deskripsi)
- Generate `data_dictionary.md` secara programatik dari schema `income_features.csv` dan `model_contract.json`
- Tulis ulang `README.md` dengan format standar tim

> Notebook ini dijalankan **terakhir sebelum hand-off** ke AI Engineer untuk memastikan semua dokumentasi up-to-date.

---

### 09 — Model Training & Evaluation

**File:** `09_Model_Training_Evaluation.ipynb`

**Tujuan:** Melatih dan mengevaluasi baseline model regresi (prediksi nilai income) dan klasifikasi (prediksi arah perubahan income), lalu menyimpan model terbaik beserta metrik evaluasi.

**Input:**
- `outputs/model_contract/income_train.csv`
- `outputs/model_contract/income_val.csv`
- `outputs/model_contract/income_test.csv`
- `outputs/model_contract/feature_columns.json`
- `outputs/model_contract/income_scalers.pkl`
- `outputs/model_contract/model_contract.json`

**Output:**

| File | Keterangan |
|------|-----------|
| `outputs/model_results/best_income_regressor.pkl` | Model regresi terbaik |
| `outputs/model_results/best_direction_classifier.pkl` | Model klasifikasi terbaik |
| `outputs/model_results/regression_metrics.csv` | Metrik semua model regresi (RMSE, MAE, R²) |
| `outputs/model_results/classification_metrics.csv` | Metrik semua model klasifikasi (accuracy, F1, dll.) |
| `outputs/model_results/predictions_test.csv` | Prediksi vs aktual di test set |
| `outputs/model_results/model_evaluation_report.md` | Laporan evaluasi lengkap |
| `outputs/charts/regression_prediction_vs_actual.png` | Scatter plot actual vs predicted |
| `outputs/charts/regression_residual_distribution.png` | Distribusi residual |
| `outputs/charts/classification_confusion_matrix.png` | Confusion matrix klasifikasi |
| `outputs/charts/feature_importance_best_model.png` | Top 20 feature importance |
| `outputs/charts/regression_error_by_gig_type.png` | Error breakdown per gig type |

**Alur training (per cell):**

| Cell | Isi |
|------|-----|
| 09.3 | Load dataset dan validasi model contract |
| 09.4 | Prepare X (fitur) dan y (target regresi & klasifikasi) |
| 09.5 | Train baseline regression models (Linear Regression, Random Forest, Gradient Boosting, dll.) |
| 09.6 | Evaluasi model regresi terbaik di test set (RMSE, MAE, MAPE, R²) |
| 09.7 | Train baseline classification models (Logistic Regression, Random Forest, dll.) |
| 09.8 | Evaluasi model klasifikasi terbaik di test set (accuracy, precision, recall, F1) |
| 09.9 | Ekstrak feature importance dari model terbaik |
| 09.10 | Visualisasi: actual vs predicted, residual, confusion matrix, feature importance, error by gig type |
| 09.11 | Simpan model dan metrik ke disk |
| 09.12 | Generate `model_evaluation_report.md` |
| 09.13 | Final validation (cek semua file output tersimpan) |
| 09.14 | Git push output ke GitHub |

---

### 10 — A/B Testing Income Predictor & Budgeting

**File:** `10_AB_Testing_Income_Predictor_Budgeting.ipynb`

> ⚠️ **Catatan:** Notebook ini menggunakan **synthetic dataset** untuk mensimulasikan pipeline evaluasi fitur. Seluruh hasil harus diinterpretasikan sebagai **proof-of-concept**, bukan sebagai bukti kausalitas atau efektivitas fitur di dunia nyata.

**Tujuan:** Menguji secara simulasi apakah pengguna yang mendapat bantuan prediksi income menghasilkan perencanaan budget yang lebih akurat dibandingkan pengguna yang membuat budget berdasarkan rata-rata historis manual.

> Income Predictor tidak secara langsung mengubah perilaku pengeluaran user — melainkan menghasilkan **planned budget** yang lebih mendekati kemampuan finansial aktual.

**Input:**
- `data/synthetic/synthetic_52week_user_income.csv`
- `outputs/model_results/predictions_test.csv` *(opsional — jika tersedia dari notebook 09)*

**Output:**
- `outputs/reports/ab_testing_report.md` — laporan lengkap hasil A/B test
- Charts ke `outputs/charts/` — distribusi metrik, comparison bar chart

**Desain eksperimen:**

| Elemen | Deskripsi |
|--------|-----------|
| **Control Group** | Budget manual = 70% dari rolling mean 4 minggu income historis |
| **Treatment Group** | Budget adaptif = 70% dari predicted income (Income Predictor) |
| **Assignment** | Stratified random 50:50 per `gig_type` |
| **Primary Metric** | `mean_budget_error` — rata-rata selisih absolut antara planned budget dan ideal budget (actual_income × 70%) |
| **Secondary Metrics** | `budget_adherence_rate`, `over_budget_rate`, `expense_to_income_ratio`, `saving_allocation_rate`, `budget_gap` |

**Hipotesis:**
- **H₀**: `mean_budget_error` Treatment = Control
- **H₁**: `mean_budget_error` Treatment < Control *(one-tailed, α = 0.05)*

**Alur analisis (per cell):**

| Cell | Isi |
|------|-----|
| 10.3 | Load data, deteksi kolom fleksibel, load predictions dari NB09, bangun dataset per user-week, stratified assignment |
| 10.4 | Simulasi planned budget (rolling mean vs predicted), actual expense dengan volatilitas per gig_type, kalkulasi metrik per minggu |
| 10.5 | Agregasi metrik per user (mean_budget_error, derived metrics) |
| 10.6 | Visualisasi distribusi metrik: histogram, boxplot, bar chart CI untuk primary & secondary metrics |
| 10.7 | Uji asumsi: normalitas (Shapiro-Wilk / Lilliefors) dan homogenitas variansi (Levene) → tentukan apakah pakai t-test atau Mann-Whitney U |
| 10.8 | Uji hipotesis utama + effect size (Cohen's d / rank-biserial) |
| 10.9 | Analisis secondary metrics (budget adherence, over-budget rate, dll.) |
| 10.10 | Subgroup analysis per `gig_type` *(eksploratorif, bukan konklusif)* |
| 10.11 | Power analysis & kalkulasi sample size minimum |
| 10.12 | Summary visualization ringkasan A/B test |
| 10.13 | Generate laporan Markdown |
| 10.14 | Final validation |
| 10.15 | Git push ke GitHub |

**Decision rule uji statistik:**
- Data normal → **Welch's t-test** sebagai uji utama
- Data tidak normal → **Mann-Whitney U** sebagai uji utama (lebih robust)

---

## Output untuk AI Engineer

Semua file yang diperlukan AI Engineer untuk melatih dan mendeploy model tersimpan di:

```
outputs/model_contract/
├── income_train.csv        ← Training set (70% users, kronologis)
├── income_val.csv          ← Validation set (15% users)
├── income_test.csv         ← Test set held-out (15% users)
├── income_scalers.pkl      ← StandardScaler fitted on train only
├── feature_columns.json    ← Daftar kolom fitur yang digunakan model
└── model_contract.json     ← Metadata pipeline lengkap (schema, target, split info)
```

Model baseline dan hasil evaluasi tersedia di:

```
outputs/model_results/
├── best_income_regressor.pkl       ← Model regresi terbaik
├── best_direction_classifier.pkl   ← Model klasifikasi terbaik
├── regression_metrics.csv          ← RMSE, MAE, MAPE, R² per model
├── classification_metrics.csv      ← Accuracy, F1, Precision, Recall per model
├── predictions_test.csv            ← Prediksi vs aktual di test set
└── model_evaluation_report.md      ← Laporan evaluasi naratif
```

---

## Struktur Direktori

```
fingo-income-analysis/
├── notebooks/
│   ├── 01_Data_Preparation.ipynb
│   ├── 02_Temporal_Mapping.ipynb
│   ├── 03_EDA_Survey.ipynb
│   ├── 04_Synthetic_Data_Generation.ipynb
│   ├── 05_Feature_Engineering.ipynb
│   ├── 06_Model_Dataset_Split.ipynb
│   ├── 07_Bias_Validation.ipynb
│   ├── 08_Documentation_Export.ipynb
│   ├── 09_Model_Training_Evaluation.ipynb
│   └── 10_AB_Testing_Income_Predictor_Budgeting.ipynb
│
├── data/
│   ├── raw/
│   │   ├── form_responses.csv          ← Survey Google Form (384 responden)
│   │   └── bps_*.csv                   ← Data referensi BPS
│   ├── processed/
│   │   ├── survey_clean.csv
│   │   ├── survey_temporal_mapped.csv
│   │   ├── survey_weekly_income_long.csv
│   │   └── income_features.csv
│   └── synthetic/
│       ├── synthetic_52week_user_income.csv
│       └── synthetic_params.json
│
├── outputs/
│   ├── model_contract/                 ← Hand-off ke AI Engineer
│   ├── model_results/                  ← Hasil training & evaluasi
│   ├── charts/                         ← Visualisasi
│   ├── dashboard/                      ← Dashboard CSV
│   └── reports/                        ← Laporan Markdown
│ 
├── streamlit/
│   ├── app.py/  
│   └── requirements.txt/                           
│
├── README.md                           ← File ini
├── notebook.md                         ← Alur modular lengkap
└── data_dictionary.md                  ← Definisi semua kolom
```

---

## Dokumentasi Lanjutan

- [notebook.md](notebook.md) — alur modular lengkap, deskripsi tiap cell per notebook
- [data_dictionary.md](data_dictionary.md) — definisi semua kolom di semua file output

---

*Generated by `08_Documentation_Export.ipynb` | Last updated: Mei 2026 | Tim CC26-PSU217*