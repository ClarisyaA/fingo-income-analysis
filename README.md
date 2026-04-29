# Fingo — Income Analysis Pipeline (DS2)

> Pipeline data science end-to-end untuk fitur **Income Predictor** Fingo. Menghasilkan dataset bersih dan siap-train (`income_clean.csv`) untuk model time-series LSTM, lengkap dengan validasi bias, dashboard interaktif, dan dokumentasi penuh.

**Program:** Coding Camp 2026 × DBS Foundation
**Tim:** CC26-PSU217
**Role:** Data Scientist 2 — Clarisya Adeline
**Downstream consumer:** AI Engineer (Martha) — model LSTM forecasting

---

## Daftar Isi

1. [Konteks Proyek](#1-konteks-proyek)
2. [Ringkasan Hasil](#2-ringkasan-hasil)
3. [Sumber Data](#3-sumber-data)
4. [Struktur Repository](#4-struktur-repository)
5. [Pipeline 14 Tahap](#5-pipeline-14-tahap)
6. [Setup & Cara Menjalankan](#6-setup--cara-menjalankan)
7. [Dashboard Streamlit](#7-dashboard-streamlit)
8. [Bias Test & Validasi](#8-bias-test--validasi)
9. [Schema Dataset Akhir](#9-schema-dataset-akhir)
10. [Business Questions yang Dijawab](#10-business-questions-yang-dijawab)
11. [Reproduksibilitas](#11-reproduksibilitas)
12. [Tim & Lisensi](#12-tim--lisensi)

---

## 1. Konteks Proyek

Fingo adalah aplikasi keuangan yang membantu **gig worker Indonesia** (ojek online, kurir, freelancer, content creator, dll.) merencanakan keuangan di tengah pendapatan yang tidak menentu. Fitur ketiga produk — **Income Predictor** — memprediksi pendapatan mingguan user 1 minggu ke depan berdasarkan history 4 minggu terakhir.

Tantangan utama: **tidak ada satu pun dataset publik** yang berisi pendapatan mingguan gig worker Indonesia selama setahun. Maka pipeline ini memilih pendekatan **kalibrasi + generasi sintetis**: parameter distribusi (mean, std, volatilitas, seasonal, autokorelasi) di-extract dari multi-sumber publik (Kaggle global + BPS Indonesia), divalidasi silang dengan survei primer, lalu dipakai untuk men-generate 300 user × 52 minggu data sintetis yang secara statistik tidak bias terhadap benchmark Indonesia.

---

## 2. Ringkasan Hasil

| Metrik | Nilai |
|---|---|
| Total baris dataset final | 16,796 |
| Total user unik | 323 (300 sintetis + 23 valid survey) |
| Periode | 52 minggu (1 tahun penuh) |
| Jumlah fitur | 32 kolom (raw + engineered) |
| Jenis pekerjaan tercakup | 6 (ojek_online, kurir, jualan_online, freelancer_it, freelancer_desain, content_creator) |
| Distribusi income | Log-Normal AR(1), φ = 0.45 (log-space) |
| Mean pendapatan mingguan | Rp 899rb |
| Sumber kalibrasi | 4 Kaggle + 4 BPS + IDinsight 2025 + Sakernas Jakarta 2023 + CELIOS 2024 |
| Bias test PASS | 5 / 6 PASS PENUH (1 PARTIAL untuk KS-test, expected karena seasonal shift) |
| Train / Val / Test split | Minggu 1-36 / 37-44 / 45-52 (kronologis, no leakage) |

---

## 3. Sumber Data

### 3.1 Sumber Sekunder (Public)

| Sumber | Dataset | Peran dalam pipeline |
|---|---|---|
| Kaggle | Freelancer_Work_Patterns_Income_Prediction_Dataset | Pola jam kerja & income freelancer |
| Kaggle | freelancer_earnings_bd | Distribusi earnings global (USD → IDR) |
| Kaggle | delivery_boy_salary | Benchmark kurir/delivery (INR → IDR + faktor adaptasi 0.55) |
| Kaggle | freelancer_earnings_vs_skillstack | Skill premium ratio |
| BPS | Pekerja Bebas 2024 & 2025 (per provinsi) | Range nasional & DKI Jakarta |
| BPS | Pekerja Informal 2023 & 2025 (per provinsi) | Cross-check range absolut |

Konstanta konversi: **1 USD = Rp 17,252** | **1 INR = Rp 183 × faktor adaptasi 0.55**

### 3.2 Sumber Primer (Original)

`form_responses.csv` — Google Form survei terhadap gig worker (1,196 baris valid masuk merge setelah cleaning consent + fuzzy matching kolom).

### 3.3 Benchmark Indonesia per Gig Type

| Gig Type | Mean / Minggu | Sumber benchmark |
|---|---|---|
| ojek_online | Rp 700rb | IDinsight 2025 net + Sakernas Jakarta transport |
| kurir | Rp 730rb | IDinsight 2025 net + CELIOS 2024 |
| freelancer_it | Rp 1.6jt | Sakernas Jakarta 2023 (informasi & komunikasi) |
| freelancer_desain | Rp 1.2jt | Sakernas Jakarta 2023 (jasa perusahaan) |
| content_creator | Rp 1.1jt | Estimasi midpoint transport & skilled |
| jualan_online | Rp 900rb | IDinsight 2025 casual + self-employed avg |

---

## 4. Struktur Repository

```
fingo-income-analysis/
├── data/
│   ├── raw/                                # Dataset publik mentah
│   │   ├── Freelancer_Work_Patterns_*.csv  # Kaggle 1
│   │   ├── freelancer_earnings_bd.csv      # Kaggle 2
│   │   ├── delivery_boy_salary.csv         # Kaggle 3
│   │   ├── freelancer_earnings_vs_*.csv    # Kaggle 4
│   │   ├── Rata-Rata Pendapatan ... 2023..2025.csv  # BPS x4
│   │   └── form_responses.csv              # Survei primer
│   ├── processed/                          # Output siap-train
│   │   ├── income_clean.csv                # *** FILE UTAMA ***
│   │   ├── income_train.csv                # Minggu 1-36
│   │   ├── income_val.csv                  # Minggu 37-44
│   │   ├── income_test.csv                 # Minggu 45-52
│   │   ├── income_scalers.pkl              # MinMaxScaler per user
│   │   ├── kaggle_calibration.csv          # Parameter benchmark
│   │   ├── data_dictionary.csv             # Schema (CSV)
│   │   └── data_dictionary.md              # Schema (Markdown)
│   └── synthetic/
│       ├── synthetic_income_raw.csv        # Pre-merge survei
│       └── synthetic_params.json           # Parameter generator (reproducible)
├── notebooks/
│   └── notebook.ipynb                      # Pipeline lengkap 14 tahap
├── streamlit/
│   ├── app.py                              # Dashboard interaktif
│   └── requirements.txt
├── outputs/
│   ├── synthetic_proportion_report.md      # Laporan proporsi + bias
│   └── charts/                             # 11 chart EDA & bias test
│       ├── 00_cov_calibration.png
│       ├── 01_kaggle_vs_benchmark.png
│       ├── 02_boxplot_delivery.png
│       ├── 02b_skillstack_eda.png
│       ├── 02c_bps_benchmark_provinsi.png
│       ├── 03_mean_income_by_gig.png
│       ├── 04_income_by_gig_experience.png
│       ├── 05_timeseries_by_gig.png
│       ├── 06_heatmap_gig_week_of_month.png
│       ├── 07_volatility_by_gig.png
│       ├── 08_correlation_heatmap.png
│       └── 09_bias_test_mean.png
├── README.md
├── data-dictionary.md
├── requirements.txt
└── .gitignore
```

---

## 5. Pipeline 14 Tahap

| # | Tahap | Output utama |
|---|---|---|
| 0 | Setup & clone GitHub | Working dir tersinkron |
| 1 | **Gathering** — load 4 Kaggle + 4 BPS + survey | 9 dataframe mentah |
| 2 | **Assessing** — missing, duplikat, isu utama | Ringkasan kualitas |
| 3 | **Cleaning & Domain Adaptation** — konversi USD/INR → IDR, parsing BPS, deteksi kolom robust | Dataset ter-normalisasi |
| 4 | **Kalibrasi Parameter** — μ, σ, CoV, Log-Normal params per gig | `ID_BENCHMARK` table |
| 5 | **EDA Kaggle** — bar, boxplot, skill premium, BPS provincial | 5 chart EDA |
| 6 | **Generate Sintetis** — 300 user × 52 minggu, AR(1) **proper di log-space** | `synthetic_income_raw.csv` |
| 7 | **Feature Engineering** — rolling mean/std (4w, 8w), lag (1w, 2w, 4w), volatility, growth | 13 fitur baru |
| 8 | **Merge Survey** — fuzzy column matching, em-dash handling, 4-week history fallback | +1,196 baris real |
| 9 | **EDA Final** — time series, heatmap week-of-month, correlation | 4 chart insight |
| 10 | **Bias Test** — 6 test: mean, KS, seasonal, experience, AR(1), BPS range | Laporan validasi |
| 11 | **Normalisasi** — MinMaxScaler **per user** + kolom target | `income_normalized`, `target_next_week` |
| 12 | **Export** — chronological split train/val/test | 4 CSV siap-train |
| 13 | **Data Dictionary** — schema lengkap (CSV + MD) | Dokumentasi |
| 14 | Push GitHub | Repo updated |

### Catatan Teknis Penting

- **AR(1) di log-space.** Persamaan: `log_inc[w] = μ + φ·(log_inc[w-1] − μ) + ε`, dengan `σ_innov = σ × √(1 − φ²)` agar varian stationary tetap σ². Ini memberi lag-1 autocorrelation 0.30–0.40 (range valid 0.20–0.60).
- **MinMaxScaler per user**, bukan global. Tujuannya: skala pendapatan antar-user yang sangat berbeda (Rp 100rb vs Rp 7jt) tidak menutupi pola temporal individu.
- **Split kronologis, bukan random.** Random split akan menyebabkan data leakage (LSTM "intip" masa depan via minggu yang sama dari user lain).
- **Survey merge fuzzy.** Output Google Form sering pakai em-dash `–` (U+2013), bukan hyphen `-`. Kolom dideteksi pakai keyword matching, bukan exact match, agar tahan whitespace/double-newline.

---

## 6. Setup & Cara Menjalankan

### 6.1 Requirement

- Python 3.9+ (testing pakai 3.11)
- pip / virtualenv

### 6.2 Instalasi

```bash
git clone https://github.com/ClarisyaA/fingo-income-analysis.git
cd fingo-income-analysis
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 6.3 Reproduksi Pipeline End-to-End

```bash
jupyter notebook notebooks/notebook.ipynb
```

Jalankan semua sel berurutan dari CELL 0.1 → CELL 14.3. Output akan ter-generate di `data/processed/`, `data/synthetic/`, dan `outputs/charts/`. Random seed sudah di-set ke `42` di CELL 0.3 sehingga hasilnya deterministik.

### 6.4 Loading Dataset Final di Python

```python
import pandas as pd
import pickle

df = pd.read_csv("data/processed/income_clean.csv")
df_train = pd.read_csv("data/processed/income_train.csv")

with open("data/processed/income_scalers.pkl", "rb") as f:
    scalers = pickle.load(f)              # dict: {user_id: MinMaxScaler}
```

---

## 7. Dashboard Streamlit

Dashboard interaktif untuk menampilkan insight dan kesimpulan analisis ada di `streamlit/app.py`. Layout-nya dibagi menjadi 6 tab tematik dengan sidebar filter.

### 7.1 Cara Menjalankan

```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
```

Browser akan otomatis terbuka di `http://localhost:8501`.

### 7.2 Tab yang Tersedia

| Tab | Isi |
|---|---|
| **Overview** | KPI cards, komposisi data source, distribusi gig type |
| **Distribusi Income** | Histogram, mean per gig, mean per experience tier |
| **Pola Temporal** | Time series 52 minggu, efek minggu gajian, dampak event musiman |
| **Volatilitas & Fitur** | CoV per gig, korelasi fitur engineered |
| **Validasi Bias** | Hasil 6 bias test divisualisasikan |
| **Insight & Kesimpulan** | Jawaban Business Question + rekomendasi untuk model |

### 7.3 Filter Global (Sidebar)

- Gig type (multi-select)
- Experience tier
- Data source (synthetic / survey / both)
- Range minggu (slider 1-52)
- Seasonal label

Filter berlaku ke semua tab kecuali Validasi Bias (yang harus pakai full dataset agar test valid).

---

## 8. Bias Test & Validasi

Enam test memastikan data sintetis tidak menyimpang dari realita Indonesia:

| Test | Threshold | Hasil | Status |
|---|---|---|---|
| 1. Mean vs Benchmark | ±15% dari μ benchmark | 6/6 PASS | PASS |
| 2. KS Test Distribusi | p-value > 0.01 | Beberapa WARN | PARTIAL (expected karena seasonal shift menggeser distribusi) |
| 3. Seasonal Direction | Arah multiplier benar | 100% direction match | PASS |
| 4. Experience Multiplier | ±25% dari ratio target (2.23x) | 6/6 PASS | PASS |
| 5. AR(1) Autocorrelation | mean 0.20 ≤ ρ ≤ 0.60 | mean ρ ≈ 0.35 | PASS |
| 6. BPS Range | Rp 0.5jt – 8jt / bulan | 6/6 PASS | PASS |

Skor akhir: **5/6 PASS PENUH**, 1 PARTIAL yang justru expected dan menunjukkan seasonal multiplier bekerja.

---

## 9. Schema Dataset Akhir

Schema lengkap tersedia di [`data-dictionary.md`](data-dictionary.md). Ringkasan kolom utama:

| Grup | Kolom | Tipe | Peran |
|---|---|---|---|
| Identitas | `user_id`, `gig_type`, `region`, `experience_tier`, `platform` | string | Profil user |
| Waktu | `week_number`, `week_of_month`, `seasonal_label`, `is_payday_week` | int / string | Konteks temporal |
| Income | `income_amount`, `income_normalized`, `income_growth_1w`, `income_vs_rolling` | float | Target & turunannya |
| Rolling | `rolling_mean_4w`, `rolling_std_4w`, `rolling_cov_8w`, `income_volatility` | float | Statistik bergerak |
| Lag | `lag_1w`, `lag_2w`, `lag_4w` | float | Memory untuk LSTM |
| One-hot | `gig_*` (6), `exp_*` (3) | int | Kategori siap-train |
| Target | `target_next_week` | float | Yang diprediksi (shift -1) |
| Metadata | `data_source` | string | synthetic / survey |

Total: **32 kolom**.

---

## 10. Business Questions yang Dijawab

### BQ4 — Apakah ada pola musiman pendapatan gig worker?

**Ya, sangat signifikan**. Pipeline mengidentifikasi 5 periode dengan multiplier berbeda-beda per gig:

- **Ramadan (minggu 10-13):** Naik untuk delivery & jualan online (+10-20%), netral untuk freelancer
- **Lebaran (minggu 14):** Spike +30-40% untuk ojek_online dan kurir
- **Harbolnas (minggu 45-46):** Spike +40-50% untuk freelancer_desain & content_creator
- **Yearend (minggu 49-52):** Naik +20-30% di mayoritas gig
- **Low season Jan-Feb (minggu 1-6):** Drop -10-15% di semua gig

Pola ini yang **wajib dipelajari LSTM** untuk akurat — model dengan input window 4 minggu sudah cukup menangkap transisi event-to-event.

### BQ5 — Fitur apa yang paling membantu prediksi?

Berdasarkan correlation matrix dan analisis volatilitas:

1. **`rolling_mean_4w`** — korelasi tertinggi dengan `income_amount` (~0.85+)
2. **`lag_1w`** — strong autocorrelation
3. **`lag_4w`** — menangkap siklus bulanan (efek payday)
4. **`seasonal_income_pattern`** — kategorikal yang carry seasonal info
5. **`is_payday_week`** — minggu ke-4 konsisten lebih tinggi
6. **`income_volatility`** (CoV per user) — penanda risiko/profil user

Volatilitas tertinggi ada di **freelancer_desain (CoV ≈ 0.62)** dan **content_creator (CoV ≈ 0.57)**. Ojek dan kurir paling stabil (CoV ≈ 0.27-0.31). Implikasi: LSTM mungkin perlu **per-gig output head** atau loss yang weighted-by-volatility agar high-CoV gig tidak mendominasi error.

---

## 11. Reproduksibilitas

- **Random seed:** `42` (numpy + Faker, lihat CELL 0.3)
- **Versi library:** lihat `requirements.txt` (pinned versi minor)
- **Parameter sintetis:** semua tersimpan di `data/synthetic/synthetic_params.json` — termasuk distribusi gig, multiplier experience, koefisien AR(1), volatility map, dan sumber benchmark
- **Determinisme:** menjalankan ulang notebook akan menghasilkan dataset yang identical sampai byte level

---

## 12. Tim & Lisensi

**Capstone:** Coding Camp 2026 (DBS Foundation × Dicoding)
**Tim:** CC26-PSU217
**Data Scientist 2:** Clarisya Adeline ([@ClarisyaA](https://github.com/ClarisyaA))
**Repo:** [github.com/ClarisyaA/fingo-income-analysis](https://github.com/ClarisyaA/fingo-income-analysis)

Dataset publik (Kaggle, BPS) tetap dipegang oleh pemilik aslinya. Kode pipeline dan dataset hasil olahan/sintetis di-license di bawah MIT untuk keperluan akademik program Coding Camp.

---

*Dokumen ini di-generate sebagai bagian dari Capstone Project. Untuk pertanyaan teknis silakan buka issue di repo GitHub.*
